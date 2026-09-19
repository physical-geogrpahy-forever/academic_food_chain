#!/usr/bin/env python3
"""
Stage 10K: aggregate current Global Energy Monitor public-map evidence to the
canonical ~50 km Civ hex board.

Sources:
  - GCMT public map GeoJSON, 2026-08: coal production/capacity and mine locations
  - GOGET public map GeoJSON, 2026-03: oil production and extraction-area points

This is evidence only. It does not perform final gameplay thinning.

For polygon coal mines, quantitative values are divided by the number of
intersected LAND hexes so one mine is not counted at full value in every hex.
Oil public-map data are points, so no polygon allocation is needed.

Existing OIL_GEM_FIELDS / OIL_GEM_SCORE from the field-level register are
retained as fallback evidence for known oil fields without current production.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

COAL_STATUS_W = {
    "operating": 4,
    "proposed": 3,
    "mothballed": 2,
    "shelved": 2,
    "closed": 1,
    "cancelled": 1,
}
OIL_STATUS_W = {
    "operating": 4,
    "in-development": 3,
    "discovered": 2,
    "mothballed": 1,
    "decommissioning": 1,
}

def num(s):
    return pd.to_numeric(s, errors="coerce").fillna(0.0).clip(lower=0)

def read_geojson(path):
    g = gpd.read_file(path)
    if g.crs is None:
        g = g.set_crs(4326)
    return g

def src_ids(g, field, prefix):
    if field in g.columns:
        base = g[field].fillna("").astype(str).str.strip()
    else:
        base = pd.Series("", index=g.index)
    fallback = pd.Series([f"{prefix}_{i}" for i in range(len(g))], index=g.index)
    return base.where(base.ne(""), fallback)

def aggregate_coal(board, coal_path):
    land = board.loc[board.SURFACE.eq("LAND"), ["id","geometry"]].copy()
    src = read_geojson(coal_path)
    src = src.loc[src.geometry.notna() & ~src.geometry.is_empty].copy()
    src["SRC_ID"] = src_ids(src, "project-id", "GCMT")
    src["COAL_PROD"] = num(src["prod-coal"]) if "prod-coal" in src.columns else 0.0
    src["COAL_CAP"] = num(src["capacity"]) if "capacity" in src.columns else 0.0
    status = src["status"].fillna("").astype(str).str.lower().str.strip() if "status" in src.columns else pd.Series("",index=src.index)
    src["COAL_STATUS_W_SRC"] = status.map(COAL_STATUS_W).fillna(1).astype("int16")
    src = src.to_crs(board.crs)

    use = src[["SRC_ID","COAL_PROD","COAL_CAP","COAL_STATUS_W_SRC","geometry"]]
    pairs = gpd.sjoin(land, use, predicate="intersects", how="inner")
    if len(pairs) == 0:
        raise RuntimeError("No GCMT coal features intersect canonical LAND hexes")
    pairs = pairs.drop_duplicates(subset=["id","SRC_ID"]).copy()

    nh = pairs.groupby("SRC_ID")["id"].transform("nunique").clip(lower=1)
    pairs["COAL_PROD_SHARE"] = pairs["COAL_PROD"] / nh
    pairs["COAL_CAP_SHARE"] = pairs["COAL_CAP"] / nh

    agg = pairs.groupby("id",as_index=False).agg(
        COAL_GEM_MINES=("SRC_ID","nunique"),
        COAL_GEM_PROD_MT=("COAL_PROD_SHARE","sum"),
        COAL_GEM_CAP_MTPA=("COAL_CAP_SHARE","sum"),
        COAL_GEM_SCORE=("COAL_STATUS_W_SRC","sum"),
    )
    agg["COAL_GEM_ANY"] = 1
    summary = {
        "source":"Global Energy Monitor Global Coal Mine Tracker public map 2026-08",
        "source_features":int(len(src)),
        "source_geometry_counts":src.geometry.geom_type.value_counts().to_dict(),
        "hex_feature_intersections":int(len(pairs)),
        "coal_evidence_hexes":int(len(agg)),
        "production_sum_after_allocation":float(agg.COAL_GEM_PROD_MT.sum()),
        "capacity_sum_after_allocation":float(agg.COAL_GEM_CAP_MTPA.sum()),
        "status_weights":COAL_STATUS_W,
        "polygon_allocation":"feature production/capacity divided equally across intersected LAND hexes",
    }
    return agg, summary

def aggregate_oil(board, oil_path):
    active = board.loc[board.SURFACE.isin(["LAND","COAST","OCEAN"]), ["id","SURFACE","geometry"]].copy()
    src = read_geojson(oil_path)
    src = src.loc[src.geometry.notna() & ~src.geometry.is_empty].copy()
    src["SRC_ID"] = src_ids(src, "project-id", "GOGET")
    src["OIL_PROD"] = num(src["prod-oil"]) if "prod-oil" in src.columns else 0.0
    status = src["status"].fillna("").astype(str).str.lower().str.strip() if "status" in src.columns else pd.Series("",index=src.index)
    src["OIL_LIVE_STATUS_W_SRC"] = status.map(OIL_STATUS_W).fillna(0).astype("int16")
    src = src.to_crs(board.crs)

    # Only direct oil-production evidence is used from the public map. Fields
    # with no prod-oil value are not inferred to be oil from their names.
    oil = src.loc[src.OIL_PROD.gt(0), ["SRC_ID","OIL_PROD","OIL_LIVE_STATUS_W_SRC","geometry"]].copy()
    pairs = gpd.sjoin(active, oil, predicate="intersects", how="inner")
    if len(pairs) == 0:
        raise RuntimeError("No GOGET prod-oil points intersect canonical board")
    pairs = pairs.drop_duplicates(subset=["id","SRC_ID"]).copy()

    # Current GOGET public map is point geometry. Keep general allocation
    # anyway, so the code remains safe if polygon features appear later.
    nh = pairs.groupby("SRC_ID")["id"].transform("nunique").clip(lower=1)
    pairs["OIL_PROD_SHARE"] = pairs["OIL_PROD"] / nh

    agg = pairs.groupby("id",as_index=False).agg(
        OIL_GEM_LIVE_PRODUCING_UNITS=("SRC_ID","nunique"),
        OIL_GEM_PROD_MBBL_Y=("OIL_PROD_SHARE","sum"),
        OIL_GEM_LIVE_STATUS_SCORE=("OIL_LIVE_STATUS_W_SRC","sum"),
    )
    agg["OIL_GEM_LIVE_ANY"] = 1
    tmp = active[["id","SURFACE"]].merge(agg[["id","OIL_GEM_LIVE_ANY"]],on="id",how="inner")
    summary = {
        "source":"Global Energy Monitor Global Oil and Gas Extraction Tracker public map 2026-03",
        "source_features":int(len(src)),
        "source_geometry_counts":src.geometry.geom_type.value_counts().to_dict(),
        "source_features_with_positive_prod_oil":int(src.OIL_PROD.gt(0).sum()),
        "hex_feature_intersections":int(len(pairs)),
        "oil_production_evidence_hexes":int(len(agg)),
        "oil_production_sum_after_allocation_million_bbl_y":float(agg.OIL_GEM_PROD_MBBL_Y.sum()),
        "surface_counts":tmp.SURFACE.value_counts().to_dict(),
        "status_weights":OIL_STATUS_W,
        "policy":"prod-oil > 0 is direct evidence; do not infer oil from names. Existing field-register evidence remains fallback.",
    }
    return agg, summary

def merge_evidence(board, ev):
    overlap = [c for c in ev.columns if c != "id" and c in board.columns]
    if overlap:
        board = board.drop(columns=overlap)
    board = board.merge(ev,on="id",how="left",validate="one_to_one")
    for c in ev.columns:
        if c != "id":
            board[c] = board[c].fillna(0)
    return board

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("coal_geojson")
    ap.add_argument("oil_geojson")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10K_GEM_LIVE_EVIDENCE")
    a=ap.parse_args()

    board = gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")

    coal, coal_summary = aggregate_coal(board,a.coal_geojson)
    oil, oil_summary = aggregate_oil(board,a.oil_geojson)
    board = merge_evidence(board,coal)
    board = merge_evidence(board,oil)

    outcols = ["id","SURFACE"] + [
        "COAL_GEM_MINES","COAL_GEM_PROD_MT","COAL_GEM_CAP_MTPA","COAL_GEM_SCORE","COAL_GEM_ANY",
        "OIL_GEM_LIVE_PRODUCING_UNITS","OIL_GEM_PROD_MBBL_Y","OIL_GEM_LIVE_STATUS_SCORE","OIL_GEM_LIVE_ANY",
    ]
    board[outcols].to_csv(a.prefix+"_EVIDENCE.csv",index=False)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10k_gem_live_evidence",driver="GPKG")

    summary = {
        "stage":"10K GEM live public-map evidence",
        "coal":coal_summary,
        "oil":oil_summary,
        "final_placement":False,
        "gameplay_thinning_applied":False,
        "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
