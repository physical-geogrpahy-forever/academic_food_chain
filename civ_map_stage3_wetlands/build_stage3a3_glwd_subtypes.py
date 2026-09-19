#!/usr/bin/env python3
"""
Stage 3A3 GLWD wetland subtype diagnostics.

Purpose: split the previous CORE_MARSH bucket so desert false positives can be
identified without arbitrary regional masks. Uses official GLWD v2 individual
class-fraction rasters exactly.

Subtypes:
  LACUSTRINE_OPEN = class 9
  PALUSTRINE_OPEN = classes 17,19
  PEATLAND_OPEN   = classes 23,25,27
  COASTAL_MARSH   = classes 28,29,31
  RIVERINE_DELTA  = classes 10,11,12,13,14,15,30
"""
from __future__ import annotations
import argparse, json, zipfile, shutil
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from exactextract import exact_extract

CATS={
 "LACUSTRINE_OPEN":[9],
 "PALUSTRINE_OPEN":[17,19],
 "PEATLAND_OPEN":[23,25,27],
 "COASTAL_MARSH":[28,29,31],
 "RIVERINE_DELTA":[10,11,12,13,14,15,30],
}
REGIONS=[
 ("Everglades",-81.8,-79.8,24.2,26.8),
 ("West Siberian peatlands",60,90,55,67),
 ("Pantanal",-60.8,-54,-22.5,-14.5),
 ("Okavango",20.5,24.8,-20.8,-17),
 ("Sudd",29,33.5,5,10.5),
 ("Sahara",-15,35,18,32),
 ("Arabia",35,58,16,30),
 ("Central Australia",125,140,-30,-20),
 ("Atacama",-72,-68,-28,-18),
]

def member(z,c):
    suf=f"GLWD_v2_0_class_{c:02d}_pct.tif"
    m=[n for n in z.namelist() if n.endswith(suf)]
    if len(m)!=1: raise RuntimeError((c,m))
    return m[0]

def extract(zip_path,work):
    need=sorted({i for v in CATS.values() for i in v})
    out={}
    with zipfile.ZipFile(zip_path) as z:
        for i in need:
            p=work/f"class_{i:02d}.tif"
            if not p.exists():
                with z.open(member(z,i)) as fi,p.open("wb") as fo:
                    shutil.copyfileobj(fi,fo,8<<20)
            out[i]=p
    return out

def sum_rasters(name,ids,srcs,out):
    rs=[rasterio.open(srcs[i]) for i in ids]
    try:
        b=rs[0]; prof=b.profile.copy()
        prof.update(dtype="uint8",nodata=0,compress="DEFLATE",tiled=True,blockxsize=512,blockysize=512,BIGTIFF="YES")
        with rasterio.open(out,"w",**prof) as w:
            for bi,win in b.block_windows(1):
                s=np.zeros((int(win.height),int(win.width)),dtype=np.uint16)
                for r in rs:s+=r.read(1,window=win,masked=True).filled(0).astype(np.uint16)
                w.write(np.minimum(s,100).astype(np.uint8),1,window=win)
                if bi[0]%300==0 and bi[1]==0:print(name,bi[0],flush=True)
    finally:
        for r in rs:r.close()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage2b");ap.add_argument("zip")
    ap.add_argument("--layer",default="game_map_stage2b_biomes")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A3_GLWD_DIAG")
    ap.add_argument("--work",default="stage3a3_work")
    a=ap.parse_args(); work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    g=gpd.read_file(a.stage2b,layer=a.layer)
    land=g[g.SURFACE.eq("LAND")][["id","LON","LAT","RELIEF","TERRAIN","geometry"]].copy()
    if len(land)!=68048:raise RuntimeError(len(land))
    gg=land.rename(columns={"id":"HEX_ID"}).to_crs(4326)
    src=extract(Path(a.zip),work)
    out=None
    for name,ids in CATS.items():
        p=work/(name.lower()+".tif");sum_rasters(name,ids,src,p)
        x=exact_extract(str(p),gg,["mean"],include_cols=["HEX_ID"],output="pandas",strategy="raster-sequential")
        if "id" in x.columns:x=x.drop(columns=["id"])
        x=x.rename(columns={"mean":name+"_PCT"})
        out=x if out is None else out.merge(x,on="HEX_ID",validate="one_to_one")
        p.unlink(missing_ok=True)
    out=out.rename(columns={"HEX_ID":"id"});out.id=pd.to_numeric(out.id).astype("int64")
    out=land.drop(columns="geometry").merge(out,on="id",validate="one_to_one")
    out["INLAND_MARSH_PCT"]=out.PALUSTRINE_OPEN_PCT.fillna(0)+out.PEATLAND_OPEN_PCT.fillna(0)
    out["MARSH_NO_LACUSTRINE_PCT"]=out.INLAND_MARSH_PCT+out.COASTAL_MARSH_PCT.fillna(0)
    out.to_csv(a.prefix+"_HEX_STATS.csv",index=False)
    rows=[]
    for name,x0,x1,y0,y1 in REGIONS:
        s=out[(out.LON>=x0)&(out.LON<=x1)&(out.LAT>=y0)&(out.LAT<=y1)]
        r={"region":name,"n":len(s)}
        for c in [x for x in out.columns if x.endswith("_PCT")]:
            r[c+"_MEAN"]=float(s[c].mean());r[c+"_MAX"]=float(s[c].max())
        rows.append(r)
    pd.DataFrame(rows).to_csv(a.prefix+"_REGIONAL.csv",index=False)
    meta={"categories":CATS,"land_hexes":len(out),"purpose":"diagnose dry-region false positives without geography-specific masks"}
    Path(a.prefix+"_README.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(pd.DataFrame(rows).to_string(index=False))
if __name__=="__main__":main()
