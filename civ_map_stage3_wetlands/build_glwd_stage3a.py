#!/usr/bin/env python3
"""
Stage 3A GLWD v2 wetland statistics for Civilization-style 50-km LAND hexes.

Uses official GLWD v2 combined-class GeoTIFFs:
- total wetland area percent per 15-arc-second cell
- dominant wetland class per 15-arc-second cell

MARSH_LIKE_PCT is the mean percent of each game hex occupied by wetland pixels
whose dominant GLWD class is marsh/swamp/peatland/coastal-wetland-like.
Riverine non-forested wetland and delta classes are retained in the wetland
candidate metric; the later Flood Plains stage may override only qualifying
river-adjacent game cells. Rice paddies and open-water classes are excluded.
"""
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from exactextract import exact_extract

# Non-forested/inundated/saturated wetland classes used as game MARSH candidates.
# Riverine non-forested classes and large deltas are retained here so major
# wetlands (Pantanal, Sudd, Bangladesh delta) are not lost. A later Flood Plains
# stage may override qualifying desert/river-adjacent cells without discarding
# these GLWD diagnostics.
MARSH_CLASSES={9,11,13,15,17,19,21,23,25,27,28,29,30,31,32}
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
        # 0 is a real value ("no marsh-like wetland") and MUST NOT be nodata.
        # Use 255 outside the valid GLWD footprint.
        prof.update(dtype="uint8",nodata=255,compress="DEFLATE",tiled=True,blockxsize=512,blockysize=512,BIGTIFF="YES")
        with rasterio.open(out,"w",**prof) as dst:
            for bi,win in p.block_windows(1):
                pct=p.read(1,window=win,masked=True)
                cls=c.read(1,window=win,masked=True)
                valid=~np.ma.getmaskarray(pct) & ~np.ma.getmaskarray(cls)
                pv=np.asarray(pct.filled(0),dtype=np.uint8)
                cv=np.asarray(cls.filled(0),dtype=np.uint8)
                z=np.where(np.isin(cv,list(MARSH_CLASSES)),pv,0).astype("uint8")
                z=np.where(valid,z,255).astype("uint8")
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
    # Pointwise MARSH_LIKE_PCT is a masked subset of WETLAND_PCT, so the zonal
    # mean cannot exceed total wetland mean except for tiny numeric tolerance.
    bad=(out["MARSH_LIKE_PCT"] > out["WETLAND_PCT"] + 1e-6).fillna(False)
    if bad.any():
        raise RuntimeError(f"MARSH_LIKE_PCT exceeds WETLAND_PCT in {int(bad.sum())} hexes")
    out.to_csv(a.prefix+"_HEX_STATS.csv",index=False)

    qa_boxes=[
      ("Pantanal",-60.8,-54.0,-22.5,-14.5),
      ("Okavango",20.5,24.8,-20.8,-17.0),
      ("Sudd",29.0,33.5,5.0,10.5),
      ("Everglades",-81.8,-79.8,24.2,26.8),
      ("Bangladesh delta",88.0,92.5,20.5,25.5),
      ("West Siberian wetlands",60.0,90.0,55.0,67.0),
      ("Amazon broad",-72.0,-48.0,-12.0,3.0),
      ("Sahara",-15.0,35.0,18.0,32.0),
      ("Central Australia",125.0,140.0,-30.0,-20.0),
    ]
    # lon/lat are already canonical Stage2B hex-centre coordinates.
    ll=g[["id","lon","lat"]].copy()
    q=out.merge(ll,on="id",how="left",validate="one_to_one")
    qrows=[]
    for name,x0,x1,y0,y1 in qa_boxes:
        s=q[(q.lon>=x0)&(q.lon<=x1)&(q.lat>=y0)&(q.lat<=y1)]
        qrows.append({
          "region":name,"n":int(len(s)),
          "wetland_pct_mean":float(s.WETLAND_PCT.mean()) if len(s) else None,
          "marsh_like_pct_mean":float(s.MARSH_LIKE_PCT.mean()) if len(s) else None,
          "marsh_ge20_share":float((s.MARSH_LIKE_PCT>=20).mean()) if len(s) else None,
          "marsh_ge30_share":float((s.MARSH_LIKE_PCT>=30).mean()) if len(s) else None,
        })
    pd.DataFrame(qrows).to_csv(a.prefix+"_QA.csv",index=False)

    # Threshold scan only; final threshold is chosen from regional QA.
    rows=[]
    for t in [5,10,15,20,25,30,40,50]:
        cand=(out.MARSH_LIKE_PCT.fillna(0)>=t)&~out.RELIEF.eq("MOUNTAIN")
        rows.append({"threshold_pct":t,"marsh_hexes":int(cand.sum()),"share_land_pct":float(cand.mean()*100)})
    pd.DataFrame(rows).to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    meta={"source":"GLWD v2.0 (Lehner et al. 2025) combined_classes GeoTIFF",
          "resolution":"15 arc-second","marsh_like_classes":sorted(MARSH_CLASSES),
          "later_floodplain_override_classes":[11,13,15,30],
          "excluded_forested_riverine":[10,12,14],
          "excluded_open_water":[1,2,3,4,5,6,7],"excluded_rice":[33],
          "land_hexes":int(len(out))}
    Path(a.prefix+"_README.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(json.dumps(meta,indent=2)); print(pd.DataFrame(rows).to_string(index=False)); print(pd.DataFrame(qrows).to_string(index=False))

if __name__=="__main__":main()
