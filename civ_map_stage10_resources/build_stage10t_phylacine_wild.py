#!/usr/bin/env python3
"""
Stage 10T: derive historical-game wild mammal resource evidence from
PHYLACINE v1.2.1 Present_natural ranges.

Resources:
  BISON  : extant Bison species
  DEER   : extant large/medium cervids
  IVORY  : extant elephants (Elephas, Loxodonta)
  FURS   : extant terrestrial fur-bearing mammals from selected genera

Present_natural ranges are used because this is a historical strategy game and
we want to reduce modern anthropogenic range-contraction bias. Species are
required to have a non-empty Current raster, so extinct PHYLACINE taxa are not
silently introduced.

Evidence only. No final resource placement or gameplay thinning.
"""
from __future__ import annotations
import argparse, json, zipfile, tempfile, re
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.io import MemoryFile
from exactextract import exact_extract

GROUP_GENERA={
  "BISON":{"Bison"},
  "DEER":{
    "Alces","Axis","Blastocerus","Capreolus","Cervus","Dama","Elaphodus",
    "Hippocamelus","Hydropotes","Mazama","Muntiacus","Odocoileus",
    "Ozotoceros","Pudu","Rangifer","Rucervus","Rusa",
  },
  "IVORY":{"Elephas","Loxodonta"},
  "FURS":{
    "Castor","Vulpes","Martes","Mustela","Neovison","Gulo",
    "Lutra","Lontra","Enhydra","Meles","Ondatra","Procyon",
    "Nyctereutes","Lynx","Chinchilla",
  },
}

PN_PREFIX="Data/Ranges/Present_natural/"
CUR_PREFIX="Data/Ranges/Current/"

def species_from_member(member):
    return Path(member).stem

def genus(sp):
    return sp.split("_",1)[0]

def current_nonempty(z, member):
    try:
        b=z.read(member)
    except KeyError:
        return False
    try:
        with MemoryFile(b) as mem:
            with mem.open() as src:
                a=src.read(1,masked=True)
                if a.count()==0:
                    return False
                vals=np.asarray(a.compressed())
                return bool(len(vals) and np.nanmax(vals)>0)
    except Exception:
        return False

def selected_members(z):
    names=set(z.namelist())
    pn=[n for n in names if n.startswith(PN_PREFIX) and n.lower().endswith(".tif")]
    bygroup={k:[] for k in GROUP_GENERA}
    skipped_extinct={k:[] for k in GROUP_GENERA}
    for n in pn:
        sp=species_from_member(n)
        g=genus(sp)
        groups=[rid for rid,genera in GROUP_GENERA.items() if g in genera]
        if not groups:
            continue
        cur=CUR_PREFIX+sp+".tif"
        alive=current_nonempty(z,cur) if cur in names else False
        for rid in groups:
            (bygroup[rid] if alive else skipped_extinct[rid]).append(n)
    return bygroup,skipped_extinct

def build_group_raster(z,members,out):
    if not members:
        raise RuntimeError(f"empty PHYLACINE group for {out}")
    src0_bytes=z.read(members[0])
    with MemoryFile(src0_bytes) as mem:
        with mem.open() as src0:
            profile=src0.profile.copy()
            shape=(src0.height,src0.width)
            crs=src0.crs
            transform=src0.transform
    richness=np.zeros(shape,dtype=np.float32)
    valid_any=np.zeros(shape,dtype=bool)

    for n in members:
        b=z.read(n)
        with MemoryFile(b) as mem:
            with mem.open() as src:
                if src.shape!=shape or src.crs!=crs or src.transform!=transform:
                    raise RuntimeError(f"unaligned PHYLACINE raster: {n}")
                a=src.read(1,masked=True)
                valid=~np.ma.getmaskarray(a)
                v=np.asarray(a.filled(0),dtype=np.float32)
                richness += np.where(valid & (v>0),1.0,0.0)
                valid_any |= valid

    profile.update(count=1,dtype="float32",nodata=-9999.0,compress="DEFLATE")
    with rasterio.open(out,"w",**profile) as dst:
        dst.write(np.where(valid_any,richness,-9999.0).astype(np.float32),1)

def aggregate_group(land,z,members,rid,work):
    tif=work/f"{rid.lower()}_phylacine_present_natural.tif"
    build_group_raster(z,members,tif)
    with rasterio.open(tif) as src:
        gg=land.rename(columns={"id":"HEX_ID"}).to_crs(src.crs)
        x=exact_extract(
            str(tif),gg,["mean","max"],include_cols=["HEX_ID"],
            output="pandas",strategy="raster-sequential"
        )
    if "id" in x.columns:x=x.drop(columns=["id"])
    x=x.rename(columns={
      "HEX_ID":"id",
      "mean":f"{rid}_PHYLACINE_MEAN_RICHNESS",
      "max":f"{rid}_PHYLACINE_MAX_RICHNESS",
    })
    x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
    for c in [f"{rid}_PHYLACINE_MEAN_RICHNESS",f"{rid}_PHYLACINE_MAX_RICHNESS"]:
        x[c]=pd.to_numeric(x[c],errors="coerce").fillna(0).clip(lower=0)
    x[f"{rid}_PHYLACINE_ANY"]=(x[f"{rid}_PHYLACINE_MAX_RICHNESS"]>0).astype("uint8")
    return x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("phylacine_zip")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--work",default="stage10t_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10T_PHYLACINE_WILD")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    if len(land)!=68048:
        raise RuntimeError(f"LAND count {len(land)}")

    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.phylacine_zip) as z:
        groups,skipped=selected_members(z)
        audits=[]
        for rid,members in groups.items():
            members=sorted(members)
            x=aggregate_group(land,z,members,rid,work)
            evcols=[c for c in x.columns if c!="id"]
            overlap=[c for c in evcols if c in board.columns]
            if overlap:board=board.drop(columns=overlap)
            board=board.merge(x,on="id",how="left",validate="one_to_one")
            for c in evcols:board[c]=board[c].fillna(0)
            audits.append({
              "resource":rid,
              "selected_extant_species_n":len(members),
              "selected_species":[species_from_member(n) for n in members],
              "excluded_noncurrent_taxa_n":len(skipped[rid]),
              "excluded_noncurrent_taxa":[species_from_member(n) for n in sorted(skipped[rid])],
              "evidence_hexes":int(board[f"{rid}_PHYLACINE_ANY"].sum()),
              "max_richness":float(board[f"{rid}_PHYLACINE_MAX_RICHNESS"].max()),
            })

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10t_phylacine_wild",driver="GPKG")
    cols=["id","SURFACE"]+[c for c in board.columns if "_PHYLACINE_" in c]
    board.loc[board.SURFACE.eq("LAND"),cols].to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    summary={
      "stage":"10T",
      "source":"PHYLACINE v1.2.1 official release",
      "range_type":"Present_natural",
      "extant_filter":"corresponding Current raster must contain positive cells",
      "resources":audits,
      "historical_game_rationale":"Present_natural reduces modern anthropogenic range-contraction bias without adding extinct taxa.",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
