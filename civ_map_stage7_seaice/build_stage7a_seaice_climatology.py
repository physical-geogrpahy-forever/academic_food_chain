#!/usr/bin/env python3
"""
Stage 7A: static sea-ice climatology candidates from NOAA/NSIDC Sea Ice Index v4.

Reference climatology: 1981-2010 monthly concentration GeoTIFFs.
For each hemisphere and calendar month, average valid monthly concentration
fields across 1981-2010. NSIDC values 0..1000 are concentration * 10; special
surface codes >1000 are excluded.

Derived pixel metrics:
  ICE_MONTHS15 = number of climatological months with mean concentration >=15%
  PERENNIAL    = ICE_MONTHS15 == 12
  TYPICAL      = ICE_MONTHS15 >= 6

These are aggregated to canonical COAST/OCEAN 50-km hexes. This stage preserves
both typical and perennial flags; it does not force a single final ICE rule.
"""
from __future__ import annotations
import argparse, io, json, time
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.io import MemoryFile
from exactextract import exact_extract

BASE="https://noaadata.apps.nsidc.org/NOAA/G02135"
ABBR=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
YEARS=range(1981,2011)

def fetch_bytes(url,tries=5):
    last=None
    for k in range(tries):
        try:
            r=requests.get(url,timeout=120)
            if r.status_code==404:
                return None
            r.raise_for_status()
            return r.content
        except Exception as e:
            last=e
            time.sleep(2*(k+1))
    raise RuntimeError(f"download failed {url}: {last}")

def monthly_climatology(hemi,work):
    tag="N" if hemi=="north" else "S"
    month_means=[]
    profile=None
    audit=[]
    for month in range(1,13):
        sm=None; ct=None; used=0; missing=[]
        d=f"{month:02d}_{ABBR[month-1]}"
        for y in YEARS:
            url=f"{BASE}/{hemi}/monthly/geotiff/{d}/{tag}_{y}{month:02d}_concentration_v4.0.tif"
            b=fetch_bytes(url)
            if b is None:
                missing.append(y); continue
            with MemoryFile(b) as mem, mem.open() as src:
                a=src.read(1)
                if profile is None:
                    profile=src.profile.copy()
                valid=(a<=1000)
                z=np.where(valid,a.astype(np.float64)/10.0,0.0)
                if sm is None:
                    sm=np.zeros(a.shape,np.float64)
                    ct=np.zeros(a.shape,np.uint16)
                sm += z
                ct += valid.astype(np.uint16)
                used += 1
        if sm is None:
            raise RuntimeError(f"{hemi} month {month}: no files")
        mean=np.divide(sm,ct,out=np.full(sm.shape,np.nan,dtype=np.float32),where=ct>0)
        month_means.append(mean.astype(np.float32))
        audit.append({"hemisphere":hemi,"month":month,"years_used":used,"missing_years":";".join(map(str,missing))})
        print(hemi,"month",month,"years",used,"missing",missing,flush=True)

    stack=np.stack(month_means,axis=0)
    months15=np.sum(stack>=15.0,axis=0).astype(np.uint8)
    perennial=(months15==12).astype(np.uint8)
    typical=(months15>=6).astype(np.uint8)
    annual=np.nanmean(stack,axis=0).astype(np.float32)

    outs={}
    for name,arr,dtype,nodata in [
        ("months15",months15,"uint8",255),
        ("perennial",perennial,"uint8",255),
        ("typical",typical,"uint8",255),
        ("annual_mean",annual,"float32",-9999.0),
    ]:
        p=work/f"{hemi}_{name}.tif"
        prof=profile.copy()
        # The NSIDC source GeoTIFF can carry strip/block dimensions that are
        # invalid when blindly reused for a newly tiled TIFF. Write derived
        # rasters as strips and remove inherited tile block keys.
        prof.pop("blockxsize",None); prof.pop("blockysize",None)
        prof.update(count=1,dtype=dtype,nodata=nodata,compress="DEFLATE",tiled=False)
        write=arr.copy()
        if name=="annual_mean":
            write=np.where(np.isfinite(write),write,nodata).astype(np.float32)
        with rasterio.open(p,"w",**prof) as dst:
            dst.write(write,1)
        outs[name]=p
    return outs,audit

def zonal(path,water3857,value_name):
    with rasterio.open(path) as src:
        g=water3857.to_crs(src.crs).rename(columns={"id":"HEX_ID"})
    x=exact_extract(str(path),g,["mean"],include_cols=["HEX_ID"],output="pandas",strategy="raster-sequential")
    if "id" in x.columns:x=x.drop(columns=["id"])
    return x.rename(columns={"mean":value_name})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage6_gpkg")
    ap.add_argument("--layer",default="game_map_stage6a_reef_candidates")
    ap.add_argument("--work",default="stage7a_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE7A_SEAICE")
    ap.add_argument("--hex-frac",type=float,default=0.25)
    a=ap.parse_args()
    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)

    board=gpd.read_file(a.stage6_gpkg,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    water=board[board.SURFACE.isin(["COAST","OCEAN"])][["id","LON","LAT","SURFACE","geometry"]].copy()
    if board.crs.to_epsg()!=8857:
        board=board.to_crs(8857);water=water.to_crs(8857)

    metrics=None;audit=[]
    for hemi in ["north","south"]:
        outs,au=monthly_climatology(hemi,work);audit.extend(au)
        pieces=[
            zonal(outs["perennial"],water,f"{hemi.upper()}_PERENNIAL_FRAC"),
            zonal(outs["typical"],water,f"{hemi.upper()}_TYPICAL_FRAC"),
            zonal(outs["months15"],water,f"{hemi.upper()}_ICE_MONTHS15"),
            zonal(outs["annual_mean"],water,f"{hemi.upper()}_ICE_ANNUAL_MEAN"),
        ]
        m=pieces[0]
        for p in pieces[1:]:m=m.merge(p,on="HEX_ID",how="outer",validate="one_to_one")
        m=m.rename(columns={"HEX_ID":"id"})
        metrics=m if metrics is None else metrics.merge(m,on="id",how="outer",validate="one_to_one")

    metrics["id"]=pd.to_numeric(metrics.id).astype("int64")
    board=board.merge(metrics,on="id",how="left",validate="one_to_one")
    for c in metrics.columns:
        if c!="id":board[c]=board[c].fillna(0)

    board["ICE_PERENNIAL_FRAC"]=board[["NORTH_PERENNIAL_FRAC","SOUTH_PERENNIAL_FRAC"]].max(axis=1)
    board["ICE_TYPICAL_FRAC"]=board[["NORTH_TYPICAL_FRAC","SOUTH_TYPICAL_FRAC"]].max(axis=1)
    board["ICE_MONTHS15"]=board[["NORTH_ICE_MONTHS15","SOUTH_ICE_MONTHS15"]].max(axis=1)
    board["ICE_PERENNIAL_CAND"]=((board.ICE_PERENNIAL_FRAC>=a.hex_frac)&board.SURFACE.isin(["COAST","OCEAN"])).astype("uint8")
    board["ICE_TYPICAL_CAND"]=((board.ICE_TYPICAL_FRAC>=a.hex_frac)&board.SURFACE.isin(["COAST","OCEAN"])).astype("uint8")

    # Hard QA.
    nonwater_p=int(board.loc[~board.SURFACE.isin(["COAST","OCEAN"]),"ICE_PERENNIAL_CAND"].sum())
    nonwater_t=int(board.loc[~board.SURFACE.isin(["COAST","OCEAN"]),"ICE_TYPICAL_CAND"].sum())
    trop=int(board.loc[board.LAT.abs()<30,"ICE_TYPICAL_CAND"].sum())
    north_p=int(board.loc[board.LAT>0,"ICE_PERENNIAL_CAND"].sum())
    south_p=int(board.loc[board.LAT<0,"ICE_PERENNIAL_CAND"].sum())
    north_t=int(board.loc[board.LAT>0,"ICE_TYPICAL_CAND"].sum())
    south_t=int(board.loc[board.LAT<0,"ICE_TYPICAL_CAND"].sum())
    failures=[]
    if nonwater_p or nonwater_t:failures.append("nonwater ice candidates")
    if trop:failures.append(f"tropical typical-ice candidates {trop}")
    if north_t==0 or south_t==0:failures.append("missing one hemisphere typical ice")
    if north_p==0 or south_p==0:failures.append("missing one hemisphere perennial ice")

    # Regional diagnostics, not hard-coded rules.
    regs=[
      ("Central Arctic",-180,180,80,90),
      ("Bering-Chukchi",160,-150,55,75),
      ("Greenland seas",-50,20,60,82),
      ("Weddell Sea",-60,20,-80,-60),
      ("Ross Sea",160,-150,-80,-60),
    ]
    q=[]
    for name,x0,x1,y0,y1 in regs:
        if x0<=x1:m=(board.LON>=x0)&(board.LON<=x1)&(board.LAT>=y0)&(board.LAT<=y1)
        else:m=((board.LON>=x0)|(board.LON<=x1))&(board.LAT>=y0)&(board.LAT<=y1)
        q.append({"region":name,"water_hexes":int((m&board.SURFACE.isin(["COAST","OCEAN"])).sum()),
                  "typical":int(board.loc[m,"ICE_TYPICAL_CAND"].sum()),
                  "perennial":int(board.loc[m,"ICE_PERENNIAL_CAND"].sum()),
                  "months15_mean":float(board.loc[m&board.SURFACE.isin(["COAST","OCEAN"]),"ICE_MONTHS15"].mean())})
    qa=pd.DataFrame(q)
    qa.to_csv(a.prefix+"_QA.csv",index=False)
    pd.DataFrame(audit).to_csv(a.prefix+"_DOWNLOAD_AUDIT.csv",index=False)

    summary={
      "stage":"7A",
      "source":"NOAA/NSIDC Sea Ice Index v4 monthly concentration GeoTIFFs (G02135)",
      "climatology":"1981-2010",
      "pixel_ice_threshold_pct":15,
      "hex_fraction_threshold":a.hex_frac,
      "typical_definition":"climatological ice >=15% in at least 6 of 12 months",
      "perennial_definition":"climatological ice >=15% in all 12 months",
      "typical_candidate_hexes":int(board.ICE_TYPICAL_CAND.sum()),
      "perennial_candidate_hexes":int(board.ICE_PERENNIAL_CAND.sum()),
      "north_typical":north_t,"south_typical":south_t,
      "north_perennial":north_p,"south_perennial":south_p,
      "tropical_typical":trop,
      "qa_gate":"PASS" if not failures else "REVIEW",
      "qa_failures":failures,
      "policy":"Preserve typical and perennial separately; no single final ICE promotion yet.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    board.to_file(a.prefix+".gpkg",layer="game_map_stage7a_seaice",driver="GPKG")
    board.loc[(board.ICE_TYPICAL_CAND==1)|(board.ICE_PERENNIAL_CAND==1),
              ["id","SURFACE","LON","LAT","ICE_TYPICAL_FRAC","ICE_PERENNIAL_FRAC","ICE_MONTHS15","ICE_TYPICAL_CAND","ICE_PERENNIAL_CAND"]].to_csv(a.prefix+"_CANDIDATES.csv",index=False)
    print(json.dumps(summary,indent=2))
    print(qa.to_string(index=False))

if __name__=="__main__":main()
