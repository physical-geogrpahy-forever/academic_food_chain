#!/usr/bin/env python3
"""
Stage 10O: aggregate EarthStat/Monfreda circa-2000 harvested-area rasters to
Civ non-strategic resource evidence.

Groups:
  OLIVES = olive
  WINE   = grape
  SPICES = pepper + clove + nutmeg + cinnamon + ginger + spicenes
           + pimento + aniseetc + vanilla

The SPICES group intentionally represents the game's generic spice luxury,
including pepper, cloves, nutmeg/mace/cardamom and other major spice crops.

Evidence only. No final placement or gameplay thinning.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

GROUPS={
  "OLIVES":["olive"],
  "WINE":["grape"],
  "SPICES":["pepper","clove","nutmeg","cinnamon","ginger","spicenes","pimento","aniseetc","vanilla"],
}

def find_crop(root,crop):
    hits=list(Path(root).rglob(f"{crop}_HarvestedAreaHectares.tif"))
    if len(hits)!=1:
        raise RuntimeError(f"{crop}: expected exactly one harvested-area tif, found {hits}")
    return hits[0]

def build_sum(paths,out):
    srcs=[rasterio.open(p) for p in paths]
    try:
        base=srcs[0]
        for s in srcs[1:]:
            if (s.width,s.height,s.crs,s.transform)!=(base.width,base.height,base.crs,base.transform):
                raise RuntimeError("Monfreda rasters are not aligned")
        prof=base.profile.copy()
        prof.pop("blockxsize",None); prof.pop("blockysize",None)
        prof.update(count=1,dtype="float32",nodata=-9999.0,compress="DEFLATE",tiled=False)
        with rasterio.open(out,"w",**prof) as dst:
            for _,win in base.block_windows(1):
                z=np.zeros((int(win.height),int(win.width)),dtype=np.float32)
                valid_any=np.zeros(z.shape,dtype=bool)
                for s in srcs:
                    a=s.read(1,window=win,masked=True)
                    valid=~np.ma.getmaskarray(a)
                    q=np.asarray(a.filled(0),dtype=np.float32)
                    q=np.where(q>0,q,0)
                    z+=q
                    valid_any|=valid
                dst.write(np.where(valid_any,z,-9999).astype("float32"),1,window=win)
    finally:
        for s in srcs:s.close()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("monfreda_dir")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--work",default="stage10o_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10O_MONFREDA_EVIDENCE")
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

    for group,crops in GROUPS.items():
        paths=[find_crop(a.monfreda_dir,c) for c in crops]
        tmp=work/f"{group.lower()}_harvested_area.tif"
        build_sum(paths,tmp)
        x=exact_extract(str(tmp),land4326,["sum"],include_cols=["HEX_ID"],
                        output="pandas",strategy="raster-sequential")
        if "id" in x.columns:x=x.drop(columns=["id"])
        x=x.rename(columns={"HEX_ID":"id","sum":group+"_MONFREDA_HA"})
        x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
        out=out.merge(x,on="id",how="left",validate="one_to_one")
        out[group+"_MONFREDA_HA"]=out[group+"_MONFREDA_HA"].fillna(0).clip(lower=0)
        out[group+"_MONFREDA_FRAC"]=(out[group+"_MONFREDA_HA"]/out.HEX_HA).clip(0,1)
        out[group+"_MONFREDA_ANY"]=(out[group+"_MONFREDA_HA"]>0).astype("uint8")
        audit.append({
          "group":group,
          "crops":crops,
          "hexes_with_evidence":int(out[group+"_MONFREDA_ANY"].sum()),
          "total_harvested_area_ha":float(out[group+"_MONFREDA_HA"].sum()),
          "max_hex_area_ha":float(out[group+"_MONFREDA_HA"].max()),
          "max_hex_fraction":float(out[group+"_MONFREDA_FRAC"].max()),
          "source_files":[str(p) for p in paths],
        })
        tmp.unlink(missing_ok=True)

    evcols=[c for c in out.columns if c not in ["id","HEX_HA"]]
    overlap=[c for c in evcols if c in board.columns]
    if overlap: board=board.drop(columns=overlap)
    board=board.merge(out[["id"]+evcols],on="id",how="left",validate="one_to_one")
    for c in evcols:board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10o_monfreda_evidence",driver="GPKG")
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    summary={
      "stage":"10O",
      "source":"EarthStat / Monfreda et al. 2008 harvested area for 175 crops, circa 2000, 5 arc-minute",
      "groups":audit,
      "spices_policy":"generic Civ spices = combined documented spice crop harvested area",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
