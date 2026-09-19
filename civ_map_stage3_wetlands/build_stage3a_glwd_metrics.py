#!/usr/bin/env python3
"""
Stage 3A: GLWD v2 wetland metrics on the canonical Civilization-style 50 km LAND hexes.

Source:
  GLWD v2.0 combined-classes GeoTIFF package (Lehner et al. 2025)
  Figshare file id 54001814.

Method:
  1. Download and MD5-verify the official ZIP.
  2. Extract GLWD_v2_0_area_pct and GLWD_v2_0_main_class only.
  3. Convert the native 15" rasters into 2' (= 8x8 native cells) category
     coverage rasters by averaging GLWD total wetland percentage after masking
     pixels by their dominant GLWD class.
  4. Exact area-weighted zonal statistics for canonical LAND hexes.

IMPORTANT:
  The category metrics are dominant-class-weighted GLWD coverage proxies, not
  sums of the 33 individual class-fraction rasters. They are suitable for
  Stage 3A QA and candidate mapping. They do NOT silently replace the original
  GLWD class fractions.
"""
from __future__ import annotations

import argparse, hashlib, json, math, os, sys, zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import rasterio
from rasterio.windows import Window
from affine import Affine
import geopandas as gpd
from exactextract import exact_extract

GLWD_URL = "https://ndownloader.figshare.com/files/54001814"
GLWD_MD5 = "aea80ff46211b349ffbaa871442fd0ed"

OPEN_WETLAND = {9,11,13,15,17,19,21,23,25,27,29,30,31,32}
FOREST_WETLAND = {8,10,12,14,16,18,20,22,24,26,28}
NATURAL_WETLAND = set(range(8,33))
OPEN_WATER = set(range(1,8))
RICE = {33}

QA_BOXES = [
    ("Pantanal", -60.8, -54.0, -22.5, -14.5),
    ("Okavango", 20.5, 24.8, -20.8, -17.0),
    ("Sudd", 29.0, 33.5, 5.0, 10.5),
    ("Everglades", -81.8, -79.8, 24.2, 26.8),
    ("Bangladesh delta", 88.0, 92.5, 20.5, 25.5),
    ("West Siberian wetlands", 60.0, 90.0, 55.0, 67.0),
    ("Amazon broad", -72.0, -48.0, -12.0, 3.0),
    ("Sahara", -15.0, 35.0, 18.0, 32.0),
    ("Central Australia", 125.0, 140.0, -30.0, -20.0),
]

def md5(path: Path) -> str:
    h=hashlib.md5()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(8<<20), b""):
            h.update(b)
    return h.hexdigest()

def download(url: str, dst: Path):
    if dst.exists() and dst.stat().st_size > 900_000_000:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total=int(r.headers.get("content-length",0) or 0)
        got=0
        with dst.open("wb") as f:
            for chunk in r.iter_content(8<<20):
                if not chunk: continue
                f.write(chunk); got += len(chunk)
                if total:
                    print(f"download {got/1e6:.1f}/{total/1e6:.1f} MB ({100*got/total:.1f}%)", flush=True)

def find_member(z: zipfile.ZipFile, suffix: str) -> str:
    cand=[n for n in z.namelist() if n.lower().endswith(suffix.lower())]
    if len(cand)!=1:
        raise RuntimeError(f"Expected exactly one {suffix}; got {cand[:20]}")
    return cand[0]

def extract_sources(zip_path: Path, work: Path):
    out_area=work/"GLWD_v2_0_area_pct.tif"
    out_main=work/"GLWD_v2_0_main_class.tif"
    if out_area.exists() and out_main.exists():
        return out_area,out_main
    with zipfile.ZipFile(zip_path) as z:
        a=find_member(z,"GLWD_v2_0_area_pct.tif")
        m=find_member(z,"GLWD_v2_0_main_class.tif")
        print("ZIP area member:",a, flush=True)
        print("ZIP main member:",m, flush=True)
        for src,dst in [(a,out_area),(m,out_main)]:
            with z.open(src) as fi, dst.open("wb") as fo:
                while True:
                    b=fi.read(8<<20)
                    if not b: break
                    fo.write(b)
    return out_area,out_main

def class_mask(arr, classes):
    out=np.zeros(arr.shape,dtype=bool)
    for k in classes:
        out |= (arr==k)
    return out

def build_2min_category_rasters(area_path: Path, main_path: Path, work: Path):
    outs={
        "WET": work/"glwd2min_wetland_domweighted_pct.tif",
        "OPEN": work/"glwd2min_openwet_domweighted_pct.tif",
        "FOREST": work/"glwd2min_forestwet_domweighted_pct.tif",
        "WATER": work/"glwd2min_water_domweighted_pct.tif",
        "RICE": work/"glwd2min_rice_domweighted_pct.tif",
    }
    if all(p.exists() for p in outs.values()):
        return outs
    factor=8
    with rasterio.open(area_path) as a, rasterio.open(main_path) as m:
        if (a.width,a.height)!=(m.width,m.height):
            raise RuntimeError("GLWD source dimensions differ")
        if a.width%factor or a.height%factor:
            raise RuntimeError(f"GLWD dims not divisible by {factor}: {a.width}x{a.height}")
        if not (abs(a.bounds.left+180)<1e-4 and abs(a.bounds.right-180)<1e-4):
            raise RuntimeError(f"unexpected GLWD lon bounds {a.bounds}")
        out_w=a.width//factor; out_h=a.height//factor
        out_transform=a.transform * Affine.scale(factor,factor)
        profile=a.profile.copy()
        profile.update(width=out_w,height=out_h,transform=out_transform,
                       dtype="float32",count=1,nodata=-9999.0,
                       compress="DEFLATE",predictor=3,tiled=True,
                       blockxsize=256,blockysize=256)
        writers={k:rasterio.open(p,"w",**profile) for k,p in outs.items()}
        try:
            chunk_out_rows=16
            chunk_in_rows=chunk_out_rows*factor
            for y0 in range(0,a.height,chunk_in_rows):
                h=min(chunk_in_rows,a.height-y0)
                if h%factor:
                    raise RuntimeError("unexpected tail rows")
                aa=a.read(1,window=Window(0,y0,a.width,h),masked=True).filled(0).astype(np.float32)
                mm=m.read(1,window=Window(0,y0,m.width,h),masked=True).filled(0).astype(np.uint8)
                cats={
                    "WET": class_mask(mm,NATURAL_WETLAND),
                    "OPEN": class_mask(mm,OPEN_WETLAND),
                    "FOREST": class_mask(mm,FOREST_WETLAND),
                    "WATER": class_mask(mm,OPEN_WATER),
                    "RICE": class_mask(mm,RICE),
                }
                oh=h//factor
                for key,mask in cats.items():
                    v=aa*mask
                    # exact arithmetic mean of the 64 native 15" cells.
                    v=v.reshape(oh,factor,out_w,factor).mean(axis=(1,3),dtype=np.float64).astype(np.float32)
                    writers[key].write(v,1,window=Window(0,y0//factor,out_w,oh))
                if (y0//chunk_in_rows)%50==0:
                    print(f"aggregate input row {y0}/{a.height}",flush=True)
        finally:
            for w in writers.values(): w.close()
    return outs

def zonal(raster: Path, land4326: gpd.GeoDataFrame, prefix: str):
    ops=["mean","quantile(q=0.9)","max"]
    x=exact_extract(str(raster),land4326,ops,include_cols=["HEX_ID"],output="pandas",
                    strategy="raster-sequential")
    if "id" in x.columns:
        x=x.drop(columns=["id"])
    ren={}
    for c in x.columns:
        lc=c.lower()
        if c=="HEX_ID": continue
        if lc=="mean": ren[c]=prefix+"_MEAN"
        elif "quantile" in lc: ren[c]=prefix+"_P90"
        elif lc=="max": ren[c]=prefix+"_MAX"
    x=x.rename(columns=ren)
    return x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stage2b",required=True)
    ap.add_argument("--layer",default="game_map_stage2b_biomes")
    ap.add_argument("--work",default="stage3_glwd_work")
    ap.add_argument("--out",default="CIV_GAME_MAP_STAGE3A_GLWD_METRICS.csv")
    a=ap.parse_args()
    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)

    z=work/"GLWD_v2_0_combined_classes_tif.zip"
    download(GLWD_URL,z)
    got=md5(z)
    print("GLWD ZIP MD5",got,flush=True)
    if got.lower()!=GLWD_MD5:
        raise RuntimeError(f"GLWD MD5 mismatch {got} != {GLWD_MD5}")

    area,mainc=extract_sources(z,work)
    derived=build_2min_category_rasters(area,mainc,work)

    board=gpd.read_file(a.stage2b,layer=a.layer)
    land=board.loc[board["SURFACE"].eq("LAND"),["id","LON","LAT","RELIEF","TERRAIN","FEATURE_GAME","geometry"]].copy()
    if len(land)!=68048 or not land["id"].is_unique:
        raise RuntimeError(f"canonical LAND check failed n={len(land)} unique={land['id'].is_unique}")
    land=land.rename(columns={"id":"HEX_ID"}).to_crs("EPSG:4326")

    out=None
    for key,path in derived.items():
        zz=zonal(path,land,key)
        out=zz if out is None else out.merge(zz,on="HEX_ID",how="outer",validate="one_to_one")
    out=out.rename(columns={"HEX_ID":"id"})
    out["id"]=pd.to_numeric(out["id"],errors="raise").astype(np.int64)
    # Restore canonical centroid/relief attributes for QA.
    meta=board.loc[board["SURFACE"].eq("LAND"),["id","LON","LAT","RELIEF","TERRAIN","FEATURE_GAME"]].copy()
    out=meta.merge(out,on="id",how="left",validate="one_to_one")
    out.to_csv(a.out,index=False)

    qa=[]
    for name,x0,x1,y0,y1 in QA_BOXES:
        s=out[(out.LON>=x0)&(out.LON<=x1)&(out.LAT>=y0)&(out.LAT<=y1)]
        qa.append({
            "region":name,"n":len(s),
            "OPEN_MEAN":float(s.OPEN_MEAN.mean()) if len(s) else None,
            "OPEN_P90":float(s.OPEN_P90.mean()) if len(s) else None,
            "FOREST_MEAN":float(s.FOREST_MEAN.mean()) if len(s) else None,
            "WET_MEAN":float(s.WET_MEAN.mean()) if len(s) else None,
            "WATER_MEAN":float(s.WATER_MEAN.mean()) if len(s) else None,
            "RICE_MEAN":float(s.RICE_MEAN.mean()) if len(s) else None,
        })
    pd.DataFrame(qa).to_csv("CIV_GAME_MAP_STAGE3A_GLWD_QA.csv",index=False)

    summary={
        "source":"GLWD v2.0 combined_classes GeoTIFF",
        "source_url":GLWD_URL,
        "source_md5":got,
        "native_resolution_arcsec":15,
        "derived_resolution_arcmin":2,
        "land_hexes":int(len(out)),
        "method":"area_pct multiplied by dominant-class category mask at 15 arcsec, then exact 8x8 mean to 2 arcmin, then exactextract polygon zonal stats",
        "limitations":"Stage 3A dominant-class-weighted proxy. Does not equal a sum of individual GLWD class-fraction rasters.",
        "open_wetland_classes":sorted(OPEN_WETLAND),
        "forested_wetland_classes":sorted(FOREST_WETLAND),
        "water_classes":sorted(OPEN_WATER),
        "rice_class":33,
    }
    Path("CIV_GAME_MAP_STAGE3A_GLWD_METADATA.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(pd.DataFrame(qa).to_string(index=False))

if __name__=="__main__":
    main()
