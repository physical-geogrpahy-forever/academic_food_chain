#!/usr/bin/env python3
"""
Stage 10R: aggregate GLW 2015 cattle and sheep density rasters to canonical
50-km LAND hexes.

The rasters are treated as spatial evidence only. Final bonus-resource
placement and thinning happen later.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

RESOURCES={
    "CATTLE":"cattle_tif",
    "SHEEP":"sheep_tif",
}

def aggregate(board, tif, rid):
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    with rasterio.open(tif) as src:
        meta={
            "width":src.width,"height":src.height,"count":src.count,
            "crs":str(src.crs),"bounds":list(src.bounds),
            "dtype":src.dtypes[0],"nodata":src.nodata,
            "description":src.descriptions[0] if src.descriptions else None,
            "tags":src.tags(1),
        }
        gg=land.rename(columns={"id":"HEX_ID"}).to_crs(src.crs)
        x=exact_extract(tif,gg,["mean","max"],include_cols=["HEX_ID"],
                        output="pandas",strategy="raster-sequential")
    if "id" in x.columns:
        x=x.drop(columns=["id"])
    x=x.rename(columns={
        "HEX_ID":"id",
        "mean":f"{rid}_GLW_MEAN",
        "max":f"{rid}_GLW_MAX",
    })
    x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
    x[f"{rid}_GLW_MEAN"]=pd.to_numeric(x[f"{rid}_GLW_MEAN"],errors="coerce").fillna(0).clip(lower=0)
    x[f"{rid}_GLW_MAX"]=pd.to_numeric(x[f"{rid}_GLW_MAX"],errors="coerce").fillna(0).clip(lower=0)
    x[f"{rid}_GLW_ANY"]=(x[f"{rid}_GLW_MAX"]>0).astype("uint8")
    summary={
        "resource":rid,
        "raster":meta,
        "evidence_hexes":int(x[f"{rid}_GLW_ANY"].sum()),
        "mean_of_hex_means":float(x[f"{rid}_GLW_MEAN"].mean()),
        "max_hex_mean":float(x[f"{rid}_GLW_MEAN"].max()),
        "max_source_value_in_hexes":float(x[f"{rid}_GLW_MAX"].max()),
    }
    return x,summary

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("cattle_tif")
    ap.add_argument("sheep_tif")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10R_GLW_LIVESTOCK")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    if int(board.SURFACE.eq("LAND").sum())!=68048:
        raise RuntimeError("LAND count changed")

    audits=[]
    for rid,tif in [("CATTLE",a.cattle_tif),("SHEEP",a.sheep_tif)]:
        x,s=aggregate(board,tif,rid)
        audits.append(s)
        evcols=[c for c in x.columns if c!="id"]
        overlap=[c for c in evcols if c in board.columns]
        if overlap:
            board=board.drop(columns=overlap)
        board=board.merge(x,on="id",how="left",validate="one_to_one")
        for c in evcols:
            board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10r_glw_livestock",driver="GPKG")
    cols=["id","SURFACE"]+[c for c in board.columns if c.startswith("CATTLE_") or c.startswith("SHEEP_")]
    board.loc[board.SURFACE.eq("LAND"),cols].to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)

    summary={
      "stage":"10R",
      "source":"FAO Gridded Livestock of the World / Harvard Dataverse 2015 distribution rasters",
      "resources":audits,
      "placement_policy":"Evidence only; no biome filtering, random placement, or gameplay thinning.",
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
