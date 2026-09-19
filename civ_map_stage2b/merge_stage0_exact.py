#!/usr/bin/env python3
"""
Merge Stage 2B LAND attributes into the exact preserved Stage 0 full-parent board.

This merge does no DEM/biome computation. It preserves the Stage 0 geometry and
water classes byte-for-byte in memory and only attaches Stage 2B attributes to
canonical LAND IDs. Intended for use where the exact Stage 0 GPKG is available.
"""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import to_wkb

SURFACE_EXPECTED={"LAND":68048,"LAKE":882,"COAST":8781,"OCEAN":156201,"VOID":27723}

def geom_digest(g):
    h=hashlib.sha256()
    for b in to_wkb(g.geometry.values, hex=False):
        h.update(len(b).to_bytes(4,"little")); h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage0_gpkg")
    ap.add_argument("stage2b_land_gpkg")
    ap.add_argument("--out",default="CIV_GAME_MAP_STAGE2B_BIOMES_HIGHRES_RELIEF.gpkg")
    ap.add_argument("--audit",default="CIV_GAME_MAP_STAGE2B_FULLBOARD_AUDIT.json")
    args=ap.parse_args()

    s0=gpd.read_file(args.stage0_gpkg,layer="stage0_full_parent_grid").sort_values("id").reset_index(drop=True)
    land=gpd.read_file(args.stage2b_land_gpkg,layer="stage2b_land_biomes").sort_values("id").reset_index(drop=True)

    if len(s0)!=261635 or not s0.id.is_unique:
        raise SystemExit("Stage0 parent-grid integrity failure")
    sc=s0.SURFACE.value_counts().to_dict()
    if sc!=SURFACE_EXPECTED:
        raise SystemExit(f"Stage0 surface counts changed: {sc}")
    if len(land)!=68048 or not land.id.is_unique:
        raise SystemExit("Stage2B LAND integrity failure")

    s0_land_ids=np.sort(s0.loc[s0.SURFACE.eq("LAND"),"id"].to_numpy(np.int64))
    land_ids=np.sort(land.id.to_numpy(np.int64))
    if not np.array_equal(s0_land_ids,land_ids):
        raise SystemExit("Stage2B LAND ID set differs from Stage0 LAND")

    before_geom=geom_digest(s0)
    baseline_cols=set(s0.columns)
    attrs=[c for c in land.columns if c not in {"geometry","row_index","col_index","lon","lat"}]
    attrs=[c for c in attrs if c!="id"]

    m=s0.merge(pd.DataFrame(land.drop(columns="geometry"))[["id"]+attrs],on="id",how="left",validate="one_to_one")
    out=gpd.GeoDataFrame(m,geometry="geometry",crs=s0.crs)

    # Water/void cells retain their Stage0 SURFACE and do not receive terrestrial biomes.
    nonland=~out.SURFACE.eq("LAND")
    out.loc[nonland,"TERRAIN"]=out.loc[nonland,"SURFACE"]
    for c in ["RELIEF","FEATURE_ECO","FEATURE_GAME","WWF_CODE","WWF_BIOME","DEM_SRC","BIO_SRC","BIO_STAGE"]:
        if c in out.columns: out.loc[nonland,c]=None
    if "MARSH_CAND" in out.columns: out.loc[nonland,"MARSH_CAND"]=0

    out.to_file(args.out,layer="stage2b_full_board",driver="GPKG")
    chk=gpd.read_file(args.out,layer="stage2b_full_board").sort_values("id").reset_index(drop=True)
    after_geom=geom_digest(chk)

    audit={
        "rows":int(len(chk)),
        "crs":str(chk.crs),
        "surface_counts":{str(k):int(v) for k,v in chk.SURFACE.value_counts().items()},
        "land_rows_with_terrain":int(chk.loc[chk.SURFACE.eq("LAND"),"TERRAIN"].notna().sum()),
        "nonland_rows_with_wwf_code":int(chk.loc[~chk.SURFACE.eq("LAND"),"WWF_CODE"].notna().sum()),
        "geometry_sha256_before":before_geom,
        "geometry_sha256_after":after_geom,
        "geometry_exact_preserved":bool(before_geom==after_geom),
        "id_order_exact":bool(np.array_equal(s0.id.to_numpy(),chk.id.to_numpy())),
        "surface_exact":bool(np.array_equal(s0.SURFACE.astype(str).to_numpy(),chk.SURFACE.astype(str).to_numpy())),
        "stage1a_1deg_used":False,
        "relief_source":"ETOPO2022 60 arc-second Stage1B",
        "biome_source":"verified Stage2 WWF/RESOLVE assignment on canonical LAND IDs"
    }
    Path(args.audit).write_text(json.dumps(audit,indent=2),encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__": main()
