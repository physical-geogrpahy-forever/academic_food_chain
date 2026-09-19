#!/usr/bin/env python3
"""
Stage 5A: integrate independently audited hydrologic feature flags.

Inputs:
  - Stage 4B board: rivers + Flood Plains
  - Stage 3A4 CSV: final GLWD-derived Marsh flag

No precedence is silently imposed. MARSH and FLOOD_PLAINS remain separate flags;
existing Stage 2B FEATURE_GAME (FOREST/JUNGLE/NONE) is preserved unchanged.
"""
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage4b_gpkg")
    ap.add_argument("marsh_csv")
    ap.add_argument("--layer",default="game_map_stage4b_floodplains")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE5A_HYDRO_FEATURES")
    a=ap.parse_args()

    g=gpd.read_file(a.stage4b_gpkg,layer=a.layer)
    if len(g)!=261635 or not g.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    m=pd.read_csv(a.marsh_csv)
    if len(m)!=68048 or not m.id.is_unique:
        raise RuntimeError("marsh LAND audit failed")
    need=["id","MARSH","MARSH_ECO_PCT","MARSH_THRESHOLD_PCT"]
    miss=[c for c in need if c not in m.columns]
    if miss:raise RuntimeError("missing marsh fields "+",".join(miss))

    g=g.merge(m[need],on="id",how="left",validate="one_to_one")
    g["MARSH"]=g["MARSH"].fillna(0).astype("uint8")

    audits=[]
    def add(check,value,expected,ok):
        audits.append({"check":check,"value":value,"expected":expected,"pass":bool(ok)})
    add("parent_cells",len(g),261635,len(g)==261635)
    add("land_cells",int(g.SURFACE.eq("LAND").sum()),68048,int(g.SURFACE.eq("LAND").sum())==68048)
    add("marsh_nonland",int(g.loc[~g.SURFACE.eq("LAND"),"MARSH"].sum()),0,int(g.loc[~g.SURFACE.eq("LAND"),"MARSH"].sum())==0)
    add("marsh_mountain",int(((g.MARSH==1)&g.RELIEF.eq("MOUNTAIN")).sum()),0,int(((g.MARSH==1)&g.RELIEF.eq("MOUNTAIN")).sum())==0)
    add("marsh_snow",int(((g.MARSH==1)&g.TERRAIN.eq("SNOW")).sum()),0,int(((g.MARSH==1)&g.TERRAIN.eq("SNOW")).sum())==0)
    add("floodplain_nonland",int(g.loc[~g.SURFACE.eq("LAND"),"FLOOD_PLAINS"].sum()),0,int(g.loc[~g.SURFACE.eq("LAND"),"FLOOD_PLAINS"].sum())==0)
    add("floodplain_nonflat",int(((g.FLOOD_PLAINS==1)&~g.RELIEF.eq("FLAT")).sum()),0,int(((g.FLOOD_PLAINS==1)&~g.RELIEF.eq("FLAT")).sum())==0)
    add("floodplain_without_river",int(((g.FLOOD_PLAINS==1)&~g.RIVER_ANY.eq(1)).sum()),0,int(((g.FLOOD_PLAINS==1)&~g.RIVER_ANY.eq(1)).sum())==0)
    audit=pd.DataFrame(audits)
    audit.to_csv(a.prefix+"_AUDIT.csv",index=False)
    bad=audit[~audit["pass"]]
    if len(bad):
        print(bad.to_string(index=False))
        raise SystemExit(1)

    overlap=int(((g.MARSH==1)&(g.FLOOD_PLAINS==1)).sum())
    summary={
      "stage":"5A",
      "rows":len(g),
      "marsh_hexes":int(g.MARSH.sum()),
      "floodplain_hexes":int(g.FLOOD_PLAINS.sum()),
      "marsh_floodplain_overlap":overlap,
      "river_flagged_cells":int(g.RIVER_ANY.sum()),
      "feature_game_counts":g.loc[g.SURFACE.eq("LAND"),"FEATURE_GAME"].value_counts(dropna=False).to_dict(),
      "policy":"MARSH, FLOOD_PLAINS, and existing FEATURE_GAME are preserved as separate attributes; precedence unresolved",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    g.to_file(a.prefix+".gpkg",layer="game_map_stage5a_hydro_features",driver="GPKG")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
