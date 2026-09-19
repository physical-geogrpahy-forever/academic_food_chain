#!/usr/bin/env python3
"""
Stage 9A consolidated gameplay-candidate audit.

Input is Stage 8A, which inherits the canonical board plus terrain/relief,
vegetation, rivers, Flood Plains, Marsh, reefs, sea ice, and Oasis.

This stage does not silently collapse mutually exclusive Civ-style features.
Instead it preserves source-backed flags and adds transparent diagnostic
conflict fields for the later precedence decision.
"""
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("gpkg")
    ap.add_argument("--layer",default="game_map_stage8a_oasis")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE9A_CONSOLIDATED")
    a=ap.parse_args()

    g=gpd.read_file(a.gpkg,layer=a.layer)
    if len(g)!=261635 or not g.id.is_unique:
        raise RuntimeError(f"canonical board failed n={len(g)} unique={g.id.is_unique}")
    need=["SURFACE","RELIEF","TERRAIN","FEATURE_GAME","RIVER_ANY","FLOOD_PLAINS","MARSH",
          "REEF_CANDIDATE","ICE_TYPICAL_CAND","ICE_PERENNIAL_CAND","OASIS"]
    miss=[c for c in need if c not in g.columns]
    if miss: raise RuntimeError("missing fields: "+",".join(miss))

    flags=["FLOOD_PLAINS","MARSH","OASIS"]
    for c in flags:g[c]=g[c].fillna(0).astype("uint8")
    # Existing FOREST/JUNGLE is another tile feature candidate.
    g["VEG_FEATURE"]=(g["FEATURE_GAME"].fillna("NONE")!="NONE").astype("uint8")
    g["LAND_FEATURE_N"]=g[["FLOOD_PLAINS","MARSH","OASIS","VEG_FEATURE"]].sum(axis=1).astype("uint8")
    g["LAND_FEATURE_CONFLICT"]=(g["LAND_FEATURE_N"]>1).astype("uint8")

    audits=[]
    def add(name,value,expected,passed):
        audits.append({"check":name,"value":value,"expected":expected,"pass":bool(passed)})
    add("parent_cells",len(g),261635,len(g)==261635)
    add("land_cells",int(g.SURFACE.eq("LAND").sum()),68048,int(g.SURFACE.eq("LAND").sum())==68048)
    add("lake_cells",int(g.SURFACE.eq("LAKE").sum()),882,int(g.SURFACE.eq("LAKE").sum())==882)
    add("coast_cells",int(g.SURFACE.eq("COAST").sum()),8781,int(g.SURFACE.eq("COAST").sum())==8781)
    add("ocean_cells",int(g.SURFACE.eq("OCEAN").sum()),156201,int(g.SURFACE.eq("OCEAN").sum())==156201)
    add("void_cells",int(g.SURFACE.eq("VOID").sum()),27723,int(g.SURFACE.eq("VOID").sum())==27723)
    add("oasis_non_desert",int(((g.OASIS==1)&~g.TERRAIN.eq("DESERT")).sum()),0,int(((g.OASIS==1)&~g.TERRAIN.eq("DESERT")).sum())==0)
    add("reef_nonwater",int(((g.REEF_CANDIDATE==1)&~g.SURFACE.isin(["COAST","OCEAN"])).sum()),0,int(((g.REEF_CANDIDATE==1)&~g.SURFACE.isin(["COAST","OCEAN"])).sum())==0)
    add("ice_nonwater",int(((g.ICE_TYPICAL_CAND==1)&~g.SURFACE.isin(["COAST","OCEAN"])).sum()),0,int(((g.ICE_TYPICAL_CAND==1)&~g.SURFACE.isin(["COAST","OCEAN"])).sum())==0)
    audit=pd.DataFrame(audits)
    audit.to_csv(a.prefix+"_AUDIT.csv",index=False)

    summary={
      "stage":"9A",
      "rows":int(len(g)),
      "surface_counts":g.SURFACE.value_counts(dropna=False).to_dict(),
      "relief_counts":g.loc[g.SURFACE.eq("LAND"),"RELIEF"].value_counts(dropna=False).to_dict(),
      "terrain_counts":g.loc[g.SURFACE.eq("LAND"),"TERRAIN"].value_counts(dropna=False).to_dict(),
      "vegetation_counts":g.loc[g.SURFACE.eq("LAND"),"FEATURE_GAME"].value_counts(dropna=False).to_dict(),
      "river_cells":int(g.RIVER_ANY.sum()),
      "floodplain_cells":int(g.FLOOD_PLAINS.sum()),
      "marsh_cells":int(g.MARSH.sum()),
      "oasis_cells":int(g.OASIS.sum()),
      "reef_candidate_cells":int(g.REEF_CANDIDATE.sum()),
      "ice_typical_cells":int(g.ICE_TYPICAL_CAND.sum()),
      "ice_perennial_cells":int(g.ICE_PERENNIAL_CAND.sum()),
      "land_feature_conflicts":int(g.LAND_FEATURE_CONFLICT.sum()),
      "hard_audit":"PASS" if audit["pass"].all() else "FAIL",
      "feature_policy":"source-backed flags preserved separately; conflicts enumerated rather than silently resolved",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    # Conflict table is intentionally explicit for later rule selection.
    cols=["id","LON","LAT","TERRAIN","RELIEF","FEATURE_GAME","FLOOD_PLAINS","MARSH","OASIS","LAND_FEATURE_N"]
    g.loc[g.LAND_FEATURE_CONFLICT.eq(1),cols].to_csv(a.prefix+"_FEATURE_CONFLICTS.csv",index=False)
    g.to_file(a.prefix+".gpkg",layer="game_map_stage9a_consolidated",driver="GPKG")
    print(json.dumps(summary,indent=2))
    print(audit.to_string(index=False))
    if not audit["pass"].all(): raise SystemExit(1)

if __name__=="__main__": main()
