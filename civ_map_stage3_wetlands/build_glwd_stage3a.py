#!/usr/bin/env python3
"""
Stage 3A GLWD v2 wetland statistics for Civilization-style 50-km LAND hexes.

Uses official GLWD v2 combined-class GeoTIFFs:
- total wetland area percent per 15-arc-second cell
- dominant wetland class per 15-arc-second cell

MARSH_LIKE_PCT is the mean percent of each game hex occupied by wetland pixels
whose dominant GLWD class is marsh/swamp/peatland/coastal-wetland-like.
Riverine floodplain and delta classes are intentionally excluded for the later
Flood Plains stage. Rice paddies and open-water classes are also excluded.
"""
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from exactextract import exact_extract

MARSH_CLASSES={9,17,19,21,23,25,27,28,29,31,32}
CLASS_NAMES={
9:"Lacustrine, non-forested",17:"Palustrine, regularly flooded, non-forested",
19:"Palustrine, seasonally saturated, non-forested",21:"Ephemeral, non-forested",
23:"Arctic/boreal peatland, non-forested",25:"Temperate peatland, non-forested",
27:"Tropical/subtropical peatland, non-forested",28:"Mangrove",29:"Saltmarsh",
31:"Other coastal wetland",32:"Salt pan, saline/brackish wetland"}

def build_marsh_raster(pct_path,cls_path,out):
    with rasterio.open(pct_path) as p, rasterio.open(cls_path) as c:
        if p.shape!=c.shape or p.transform!=c.transform:
            raise RuntimeError("GLWD grids do not align")
        prof=p.profile.copy()
        prof.update(dtype="uint8",nodata=0,compress="DEFLATE",tiled=True,blockxsize=512,blockysize=512,BIGTIFF="YES")
        with rasterio.open(out,"w",**prof) as dst:
            for bi,win in p.block_windows(1):
                pct=p.read(1,window=win)
                cls=c.read(1,window=win)
                z=np.where(np.isin(cls,list(MARSH_CLASSES)),pct,0).astype("uint8")
                dst.write(z,1,window=win)
                if bi[0]%250==0 and bi[1]==0: print("marsh raster block row",bi[0],flush=True)

def ex(rast,g,ops):
    o=exact_extract(str(rast),g,ops,include_cols=["HEX_ID"],output="pandas",strategy="raster-sequential")
    if "id" in o.columns:o=o.drop(columns=["id"])
    return o

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("land_gpkg"); ap.add_argument("wet_pct_tif"); ap.add_argument("main_class_tif")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A_GLWD2")
    a=ap.parse_args()
    g=gpd.read_file(a.land_gpkg,layer="stage2b_land_biomes")
    if len(g)!=68048: raise SystemExit("Expected 68048 LAND hexes")
    g4326=g[["id","RELIEF","TERRAIN","geometry"]].rename(columns={"id":"HEX_ID"}).to_crs(4326)
    mr=Path(a.prefix+"_MARSHLIKE_15S.tif")
    build_marsh_raster(a.wet_pct_tif,a.main_class_tif,mr)
    total=ex(a.wet_pct_tif,g4326,["mean"]).rename(columns={"mean":"WETLAND_PCT"})
    marsh=ex(mr,g4326,["mean"]).rename(columns={"mean":"MARSH_LIKE_PCT"})
    mode=ex(a.main_class_tif,g4326,["mode"]).rename(columns={"mode":"GLWD_MODE_CLASS"})
    out=total.merge(marsh,on="HEX_ID",how="outer").merge(mode,on="HEX_ID",how="outer")
    out["id"]=pd.to_numeric(out.pop("HEX_ID"),errors="raise").astype("int64")
    out=out.merge(g[["id","RELIEF","TERRAIN"]],on="id",how="left")
    out["GLWD_MODE_NAME"]=out["GLWD_MODE_CLASS"].round().astype("Int64").map(CLASS_NAMES).fillna("")
    out.to_csv(a.prefix+"_HEX_STATS.csv",index=False)

    # Threshold scan only; final threshold is chosen from regional QA.
    rows=[]
    for t in [5,10,15,20,25,30,40,50]:
        cand=(out.MARSH_LIKE_PCT.fillna(0)>=t)&~out.RELIEF.eq("MOUNTAIN")
        rows.append({"threshold_pct":t,"marsh_hexes":int(cand.sum()),"share_land_pct":float(cand.mean()*100)})
    pd.DataFrame(rows).to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    meta={"source":"GLWD v2.0 (Lehner et al. 2025) combined_classes GeoTIFF",
          "resolution":"15 arc-second","marsh_like_classes":sorted(MARSH_CLASSES),
          "excluded_for_later_floodplain":[10,11,12,13,14,15,30],
          "excluded_open_water":[1,2,3,4,5,6,7],"excluded_rice":[33],
          "land_hexes":int(len(out))}
    Path(a.prefix+"_README.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(json.dumps(meta,indent=2)); print(pd.DataFrame(rows).to_string(index=False))

if __name__=="__main__":main()
