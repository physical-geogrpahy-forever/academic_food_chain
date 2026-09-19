#!/usr/bin/env python3
"""
Stage 10U: historical whaling-ground evidence from PHYLACINE v1.2.1
Present_natural ranges.

The WHALES luxury represents major historically hunted large whales rather than
all Cetacea. Included genera:
  Balaena, Balaenoptera, Caperea, Eschrichtius, Eubalaena, Megaptera, Physeter

Only taxa with a non-empty Current raster are retained. Evidence is aggregated
to canonical COAST/OCEAN hexes. No final placement or gameplay thinning here.
"""
from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.io import MemoryFile
from exactextract import exact_extract

GENERa={"Balaena","Balaenoptera","Caperea","Eschrichtius","Eubalaena","Megaptera","Physeter"}
PN="Data/Ranges/Present_natural/"
CUR="Data/Ranges/Current/"

def spname(member): return Path(member).stem
def genus(sp): return sp.split("_",1)[0]

def raster_nonempty(z,name):
    if name not in z.namelist(): return False
    with MemoryFile(z.read(name)) as mem:
        with mem.open() as src:
            a=src.read(1,masked=True)
            if a.count()==0: return False
            v=np.asarray(a.compressed())
            return bool(len(v) and np.nanmax(v)>0)

def build_richness(z,members,out):
    with MemoryFile(z.read(members[0])) as mem:
        with mem.open() as s:
            profile=s.profile.copy(); shape=s.shape; crs=s.crs; transform=s.transform
    richness=np.zeros(shape,dtype=np.float32)
    valid_any=np.zeros(shape,dtype=bool)
    for n in members:
        with MemoryFile(z.read(n)) as mem:
            with mem.open() as s:
                if s.shape!=shape or s.crs!=crs or s.transform!=transform:
                    raise RuntimeError("unaligned PHYLACINE raster "+n)
                a=s.read(1,masked=True)
                valid=~np.ma.getmaskarray(a)
                v=np.asarray(a.filled(0),dtype=np.float32)
                richness+=np.where(valid & (v>0),1.0,0.0)
                valid_any|=valid
    profile.update(count=1,dtype="float32",nodata=-9999.0,compress="DEFLATE")
    with rasterio.open(out,"w",**profile) as dst:
        dst.write(np.where(valid_any,richness,-9999.0).astype(np.float32),1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("phylacine_zip")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10U_PHYLACINE_WHALES")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")

    water=board.loc[board.SURFACE.isin(["COAST","OCEAN"]),["id","SURFACE","geometry"]].copy()
    if water.empty: raise RuntimeError("no water hexes")

    with zipfile.ZipFile(a.phylacine_zip) as z:
        names=set(z.namelist())
        candidates=[]
        excluded=[]
        for n in sorted(names):
            if not n.startswith(PN) or not n.lower().endswith(".tif"): continue
            sp=spname(n)
            if genus(sp) not in GENERa: continue
            if raster_nonempty(z,CUR+sp+".tif"):
                candidates.append(n)
            else:
                excluded.append(n)
        if not candidates:
            raise RuntimeError("no whale species selected")
        tif=Path("whales_phylacine_present_natural.tif")
        build_richness(z,candidates,tif)

    with rasterio.open(tif) as src:
        ww=water[["id","geometry"]].rename(columns={"id":"HEX_ID"}).to_crs(src.crs)
        x=exact_extract(str(tif),ww,["mean","max"],include_cols=["HEX_ID"],
                        output="pandas",strategy="raster-sequential")
    if "id" in x.columns: x=x.drop(columns=["id"])
    x=x.rename(columns={
      "HEX_ID":"id",
      "mean":"WHALES_PHYLACINE_MEAN_RICHNESS",
      "max":"WHALES_PHYLACINE_MAX_RICHNESS",
    })
    x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
    for c in ["WHALES_PHYLACINE_MEAN_RICHNESS","WHALES_PHYLACINE_MAX_RICHNESS"]:
        x[c]=pd.to_numeric(x[c],errors="coerce").fillna(0).clip(lower=0)
    x["WHALES_PHYLACINE_ANY"]=(x.WHALES_PHYLACINE_MAX_RICHNESS>0).astype("uint8")

    for c in [c for c in x.columns if c!="id" and c in board.columns]:
        board=board.drop(columns=[c])
    board=board.merge(x,on="id",how="left",validate="one_to_one")
    for c in ["WHALES_PHYLACINE_MEAN_RICHNESS","WHALES_PHYLACINE_MAX_RICHNESS","WHALES_PHYLACINE_ANY"]:
        board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10u_phylacine_whales",driver="GPKG")
    cols=["id","SURFACE","WHALES_PHYLACINE_MEAN_RICHNESS","WHALES_PHYLACINE_MAX_RICHNESS","WHALES_PHYLACINE_ANY"]
    board.loc[board.WHALES_PHYLACINE_ANY.gt(0),cols].to_csv(a.prefix+"_EVIDENCE.csv",index=False)

    summary={
      "stage":"10U",
      "source":"PHYLACINE v1.2.1 official release",
      "range_type":"Present_natural",
      "resource":"WHALES",
      "included_genera":sorted(GENERa),
      "selected_extant_species_n":len(candidates),
      "selected_species":[spname(n) for n in candidates],
      "excluded_noncurrent_taxa_n":len(excluded),
      "excluded_noncurrent_taxa":[spname(n) for n in excluded],
      "evidence_hexes":int(board.WHALES_PHYLACINE_ANY.sum()),
      "surface_counts":board.loc[board.WHALES_PHYLACINE_ANY.gt(0),"SURFACE"].value_counts().to_dict(),
      "max_richness":float(board.WHALES_PHYLACINE_MAX_RICHNESS.max()),
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
