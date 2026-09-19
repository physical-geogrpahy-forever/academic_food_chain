#!/usr/bin/env python3
"""
Stage 10N: add MAPSPAM 2020 physical-area evidence for Civ resources omitted
from the earlier Stage 10H grouping.

Current additions:
  MAIZE   band 3
  TOBACCO band 36

Evidence only. No final placement or thinning.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

GROUPS={"MAIZE":[3],"TOBACCO":[36]}

def write_group(src,bands,out):
    prof=src.profile.copy()
    prof.pop("blockxsize",None); prof.pop("blockysize",None)
    prof.update(count=1,dtype="float32",nodata=-9999.0,compress="DEFLATE",tiled=False)
    with rasterio.open(out,"w",**prof) as dst:
        for _,win in src.block_windows(1):
            total=np.zeros((int(win.height),int(win.width)),dtype=np.float32)
            valid_any=np.zeros(total.shape,dtype=bool)
            for b in bands:
                a=src.read(b,window=win,masked=True)
                valid=~np.ma.getmaskarray(a)
                z=np.asarray(a.filled(0),dtype=np.float32)
                z=np.where(z>0,z,0)
                total+=z; valid_any|=valid
            dst.write(np.where(valid_any,total,-9999).astype("float32"),1,window=win)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("mapspam_tif")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--work",default="stage10n_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10N_MAPSPAM_EXTRA")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    if len(land)!=68048:
        raise RuntimeError(f"LAND count {len(land)}")
    land["HEX_HA"]=land.geometry.area/10000
    land4326=land[["id","geometry"]].rename(columns={"id":"HEX_ID"}).to_crs(4326)

    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    out=land[["id","HEX_HA"]].copy()
    audit=[]
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
        with rasterio.open(a.mapspam_tif) as src:
            for group,bands in GROUPS.items():
                meta=[]
                for b in bands:
                    meta.append({
                      "band":b,
                      "description":src.descriptions[b-1],
                      "long_name":src.tags(b).get("long_name",""),
                    })
                p=work/f"{group.lower()}.tif"
                write_group(src,bands,p)
                x=exact_extract(str(p),land4326,["sum"],include_cols=["HEX_ID"],
                                output="pandas",strategy="raster-sequential")
                if "id" in x.columns:x=x.drop(columns=["id"])
                x=x.rename(columns={"HEX_ID":"id","sum":group+"_SPAM_HA"})
                x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
                out=out.merge(x,on="id",how="left",validate="one_to_one")
                out[group+"_SPAM_HA"]=out[group+"_SPAM_HA"].fillna(0).clip(lower=0)
                out[group+"_SPAM_FRAC"]=(out[group+"_SPAM_HA"]/out.HEX_HA).clip(0,1)
                out[group+"_SPAM_ANY"]=(out[group+"_SPAM_HA"]>0).astype("uint8")
                audit.append({
                  "group":group,"bands":bands,"band_metadata":meta,
                  "hexes_with_evidence":int(out[group+"_SPAM_ANY"].sum()),
                  "total_physical_area_ha":float(out[group+"_SPAM_HA"].sum()),
                  "max_hex_area_ha":float(out[group+"_SPAM_HA"].max()),
                  "max_hex_fraction":float(out[group+"_SPAM_FRAC"].max()),
                })
                p.unlink(missing_ok=True)

    evcols=[c for c in out.columns if c not in ["id","HEX_HA"]]
    overlap=[c for c in evcols if c in board.columns]
    if overlap:board=board.drop(columns=overlap)
    board=board.merge(out[["id"]+evcols],on="id",how="left",validate="one_to_one")
    for c in evcols:board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10n_mapspam_extra",driver="GPKG")
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    summary={
      "stage":"10N",
      "source":"MAPSPAM 2020 v2r2 global physical area, 5 arc-minute",
      "groups":audit,
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
