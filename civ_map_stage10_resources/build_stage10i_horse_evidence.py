#!/usr/bin/env python3
"""
Stage 10I: aggregate the 2015 global horse distribution (GLW/Harvard Dataverse
DOI 10.7910/DVN/JJGCTX, 5_Ho_2015_Da.tif) to canonical 50-km LAND hexes.

The source is treated as spatial evidence only. No biome filtering, random
placement, or gameplay thinning is performed here.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("horse_tif")
    ap.add_argument("--layer",default="game_map_stage10h_mapspam_evidence")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10I_HORSE_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board[board.SURFACE.eq("LAND")][["id","geometry"]].copy()
    if len(land)!=68048:raise RuntimeError(len(land))

    with rasterio.open(a.horse_tif) as src:
        meta={
          "width":src.width,"height":src.height,"count":src.count,
          "crs":str(src.crs),"bounds":list(src.bounds),
          "dtype":src.dtypes[0],"nodata":src.nodata,
          "description":src.descriptions[0] if src.descriptions else None,
          "tags":src.tags(1),
        }
        gg=land.rename(columns={"id":"HEX_ID"}).to_crs(src.crs)
        x=exact_extract(a.horse_tif,gg,["mean","max"],include_cols=["HEX_ID"],
                        output="pandas",strategy="raster-sequential")
    if "id" in x.columns:x=x.drop(columns=["id"])
    x=x.rename(columns={"HEX_ID":"id","mean":"HORSE_GLW_MEAN","max":"HORSE_GLW_MAX"})
    x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
    x["HORSE_GLW_MEAN"]=pd.to_numeric(x["HORSE_GLW_MEAN"],errors="coerce").fillna(0).clip(lower=0)
    x["HORSE_GLW_MAX"]=pd.to_numeric(x["HORSE_GLW_MAX"],errors="coerce").fillna(0).clip(lower=0)
    x["HORSE_GLW_ANY"]=(x["HORSE_GLW_MAX"]>0).astype("uint8")

    board=board.merge(x,on="id",how="left",validate="one_to_one")
    for c in ["HORSE_GLW_MEAN","HORSE_GLW_MAX","HORSE_GLW_ANY"]:
        board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10i_horse_evidence",driver="GPKG")
    x.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)

    summary={
      "stage":"10I",
      "source":"Global horse distribution 2015, Harvard Dataverse DOI 10.7910/DVN/JJGCTX",
      "source_file":"5_Ho_2015_Da.tif",
      "source_file_id":6769681,
      "raster":meta,
      "land_hexes":68048,
      "hexes_with_horse_evidence":int(x.HORSE_GLW_ANY.sum()),
      "mean_of_hex_means":float(x.HORSE_GLW_MEAN.mean()),
      "max_hex_mean":float(x.HORSE_GLW_MEAN.max()),
      "max_source_value_in_hexes":float(x.HORSE_GLW_MAX.max()),
      "placement_policy":"Evidence only; no biome filtering, random placement, or gameplay thinning.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
