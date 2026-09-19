#!/usr/bin/env python3
"""
Stage 3A2: exact GLWD v2 individual class-fraction aggregation for 50-km LAND hexes.

Unlike the earlier dominant-class proxy, this reads the official per-class
percent rasters and sums class fractions directly at the native 15 arc-second
grid before hex zonal aggregation.

Categories deliberately remain separate:
  CORE_MARSH       open lacustrine/palustrine/peatland/coastal wetland
  RIVERINE_WET     riverine wetland + delta, reserved for Flood Plains logic
  FOREST_WET       forested swamp/peatland, retained separately from Marsh
  EPHEMERAL_SALINE ephemeral wetland + salt pan, not auto-Marsh
  OPEN_WATER       GLWD open-water classes 1-7
  RICE             paddy rice class 33
"""
from __future__ import annotations
import argparse, json, zipfile, shutil
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

CATEGORIES={
    "CORE_MARSH":[9,17,19,23,25,27,28,29,31],
    "RIVERINE_WET":[10,11,12,13,14,15,30],
    "FOREST_WET":[8,16,18,20,22,24,26],
    "EPHEMERAL_SALINE":[21,32],
    "OPEN_WATER":[1,2,3,4,5,6,7],
    "RICE":[33],
}
CLASS_NAMES={
  1:"Freshwater lake",2:"Saline lake",3:"Reservoir",4:"Large river",
  5:"Large estuarine river",6:"Other permanent waterbody",7:"Small streams",
  8:"Lacustrine, forested",9:"Lacustrine, non-forested",
  10:"Riverine, regularly flooded, forested",11:"Riverine, regularly flooded, non-forested",
  12:"Riverine, seasonally flooded, forested",13:"Riverine, seasonally flooded, non-forested",
  14:"Riverine, seasonally saturated, forested",15:"Riverine, seasonally saturated, non-forested",
  16:"Palustrine, regularly flooded, forested",17:"Palustrine, regularly flooded, non-forested",
  18:"Palustrine, seasonally saturated, forested",19:"Palustrine, seasonally saturated, non-forested",
  20:"Ephemeral, forested",21:"Ephemeral, non-forested",
  22:"Arctic/boreal peatland, forested",23:"Arctic/boreal peatland, non-forested",
  24:"Temperate peatland, forested",25:"Temperate peatland, non-forested",
  26:"Tropical/subtropical peatland, forested",27:"Tropical/subtropical peatland, non-forested",
  28:"Mangrove",29:"Saltmarsh",30:"Large river delta",31:"Other coastal wetland",
  32:"Salt pan, saline/brackish wetland",33:"Paddy rice"
}

def find_member(z, cid):
    suf=f"GLWD_v2_0_class_{cid:02d}_pct.tif"
    cand=[n for n in z.namelist() if n.endswith(suf)]
    if len(cand)!=1:
        raise RuntimeError(f"class {cid}: expected one {suf}, got {cand}")
    return cand[0]

def extract_needed(zip_path:Path, work:Path):
    need=sorted({c for vals in CATEGORIES.values() for c in vals})
    out={}
    work.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for cid in need:
            dst=work/f"class_{cid:02d}.tif"
            if not dst.exists():
                member=find_member(z,cid)
                print("extract",cid,member,flush=True)
                with z.open(member) as fi, dst.open("wb") as fo:
                    shutil.copyfileobj(fi,fo,length=8<<20)
            out[cid]=dst
    return out

def build_category(name, class_ids, srcs, out_path):
    readers=[rasterio.open(srcs[c]) for c in class_ids]
    try:
        base=readers[0]
        for r in readers[1:]:
            if r.shape!=base.shape or r.transform!=base.transform or r.crs!=base.crs:
                raise RuntimeError(f"unaligned class raster in {name}")
        prof=base.profile.copy()
        prof.update(dtype="uint8",nodata=0,compress="DEFLATE",tiled=True,
                    blockxsize=512,blockysize=512,BIGTIFF="YES")
        maxsum=0; clipped=0
        with rasterio.open(out_path,"w",**prof) as dst:
            for bi,win in base.block_windows(1):
                s=np.zeros((int(win.height),int(win.width)),dtype=np.uint16)
                for r in readers:
                    a=r.read(1,window=win,masked=True).filled(0).astype(np.uint16)
                    s += a
                mx=int(s.max()) if s.size else 0
                maxsum=max(maxsum,mx)
                clipped += int((s>100).sum())
                # Per-class percentages are rounded integers; cap rare rounding overflow.
                z=np.minimum(s,100).astype(np.uint8)
                dst.write(z,1,window=win)
                if bi[0]%250==0 and bi[1]==0:
                    print(name,"block row",bi[0],"maxsum",maxsum,"clipped",clipped,flush=True)
        return {"category":name,"classes":class_ids,"native_max_sum":maxsum,"cells_clipped_gt100":clipped}
    finally:
        for r in readers:r.close()

def zonal_mean(path, land):
    x=exact_extract(str(path),land,["mean"],include_cols=["HEX_ID"],output="pandas",strategy="raster-sequential")
    if "id" in x.columns:x=x.drop(columns=["id"])
    val=[c for c in x.columns if c!="HEX_ID"]
    if len(val)!=1: raise RuntimeError(f"unexpected exactextract columns {list(x.columns)}")
    return x.rename(columns={val[0]:Path(path).stem.upper()+"_PCT"})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage2b_gpkg")
    ap.add_argument("class_pct_zip")
    ap.add_argument("--layer",default="game_map_stage2b_biomes")
    ap.add_argument("--work",default="stage3a2_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A2_GLWD_EXACT")
    a=ap.parse_args()
    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)

    board=gpd.read_file(a.stage2b_gpkg,layer=a.layer)
    land=board.loc[board.SURFACE.eq("LAND"),
        ["id","LON","LAT","RELIEF","TERRAIN","FEATURE_GAME","geometry"]].copy()
    if len(land)!=68048 or not land.id.is_unique:
        raise RuntimeError(f"Stage2B LAND audit failed n={len(land)} unique={land.id.is_unique}")
    land4326=land.rename(columns={"id":"HEX_ID"}).to_crs(4326)

    srcs=extract_needed(Path(a.class_pct_zip),work/"classes")
    audits=[]
    out=None
    for name,ids in CATEGORIES.items():
        cat=work/f"{name.lower()}_15s.tif"
        audits.append(build_category(name,ids,srcs,cat))
        z=exact_extract(str(cat),land4326,["mean"],include_cols=["HEX_ID"],output="pandas",strategy="raster-sequential")
        if "id" in z.columns:z=z.drop(columns=["id"])
        z=z.rename(columns={"mean":name+"_PCT"})
        out=z if out is None else out.merge(z,on="HEX_ID",how="outer",validate="one_to_one")
        cat.unlink(missing_ok=True)

    out=out.rename(columns={"HEX_ID":"id"})
    out["id"]=pd.to_numeric(out.id,errors="raise").astype("int64")
    meta=land.drop(columns="geometry")
    out=meta.merge(out,on="id",how="left",validate="one_to_one")
    # Useful combined diagnostics; no final feature assignment here.
    out["ALL_NATURAL_WET_PCT"]=out[["CORE_MARSH_PCT","RIVERINE_WET_PCT","FOREST_WET_PCT","EPHEMERAL_SALINE_PCT"]].fillna(0).sum(axis=1)
    out.to_csv(a.prefix+"_HEX_STATS.csv",index=False)

    Path(a.prefix+"_CATEGORY_AUDIT.json").write_text(json.dumps(audits,indent=2),encoding="utf-8")
    meta_json={
      "source":"GLWD v2.0 official area_by_class_pct GeoTIFF archive",
      "source_resolution":"15 arc-second",
      "method":"sum official per-class percent rasters at native resolution, then exactextract mean per 50-km LAND hex",
      "categories":{k:[{"id":i,"name":CLASS_NAMES[i]} for i in v] for k,v in CATEGORIES.items()},
      "land_hexes":int(len(out)),
      "note":"Categories are intentionally separate. RIVERINE_WET is reserved for later river/floodplain logic; FOREST_WET is not silently converted to Marsh."
    }
    Path(a.prefix+"_README.json").write_text(json.dumps(meta_json,indent=2),encoding="utf-8")
    print(json.dumps(meta_json,indent=2))
    print(pd.DataFrame(audits).to_string(index=False))

if __name__=="__main__":
    main()
