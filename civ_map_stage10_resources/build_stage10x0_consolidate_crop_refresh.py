#!/usr/bin/env python3
"""
Stage 10X0: consolidate the latest crop-evidence branch into the latest complete
resource-evidence board.

Reason:
  Stage 10P was originally chained to an older Stage 10N/O artifact. Later N/O
  reruns added/fixed crop groups (including BANANAS and other MAPSPAM fields),
  so downstream Q..W lacked some latest crop columns.

This script keeps the downstream W board geometry and all later evidence, while
replacing/adding only crop evidence columns from the latest Stage 10O board,
matched strictly by canonical hex id.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import pandas as pd
import geopandas as gpd

def is_crop_col(c):
    return (
        "_SPAM_" in c or
        "_MONFREDA_" in c
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("downstream_board")
    ap.add_argument("latest_crop_board")
    ap.add_argument("--downstream-layer",default="game_map_stage10w_manual_luxuries")
    ap.add_argument("--crop-layer",default="game_map_stage10o_monfreda_evidence")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10X0_CONSOLIDATED_EVIDENCE")
    a=ap.parse_args()

    dst=gpd.read_file(a.downstream_board,layer=a.downstream_layer)
    src=gpd.read_file(a.latest_crop_board,layer=a.crop_layer)

    for name,df in [("downstream",dst),("crop",src)]:
        if len(df)!=261635 or not df.id.is_unique:
            raise RuntimeError(f"{name} canonical board audit failed")
    if set(dst.id)!=set(src.id):
        raise RuntimeError("canonical id sets differ between branches")

    cropcols=[c for c in src.columns if c!="id" and c!="geometry" and is_crop_col(c)]
    if not cropcols:
        raise RuntimeError("no crop evidence columns found in latest crop board")

    expected_prefixes=[
      "WHEAT_","RICE_","MAIZE_","SUGAR_","COTTON_","COFFEE_","COCOA_",
      "TEA_","TOBACCO_","BANANAS_","CITRUS_","OLIVES_","WINE_","SPICES_"
    ]
    missing_groups=[
      p for p in expected_prefixes
      if not any(c.startswith(p) for c in cropcols)
    ]
    if missing_groups:
        raise RuntimeError(f"latest crop board missing expected groups: {missing_groups}")

    old_present=[c for c in cropcols if c in dst.columns]
    if old_present:
        dst=dst.drop(columns=old_present)

    merge=src[["id"]+cropcols].copy()
    dst=dst.merge(merge,on="id",how="left",validate="one_to_one")
    for c in cropcols:
        dst[c]=pd.to_numeric(dst[c],errors="coerce").fillna(0)

    # Strict post-merge check: every crop group must have positive evidence.
    audit=[]
    for p in expected_prefixes:
        rid=p[:-1]
        candidate=[c for c in cropcols if c.startswith(p) and (c.endswith("_HA") or c.endswith("_ANY"))]
        positive_cols=[]
        for c in candidate:
            n=int(pd.to_numeric(dst[c],errors="coerce").fillna(0).gt(0).sum())
            positive_cols.append({"column":c,"positive_hexes":n})
        if not any(x["positive_hexes"]>0 for x in positive_cols):
            raise RuntimeError(f"{rid}: no positive crop evidence after consolidation")
        audit.append({"resource":rid,"columns":positive_cols})

    dst.to_file(
      a.prefix+".gpkg",
      layer="game_map_stage10x0_consolidated_evidence",
      driver="GPKG"
    )
    summary={
      "stage":"10X0",
      "purpose":"merge latest Stage 10N/O crop evidence into downstream Stage 10W board",
      "replaced_existing_crop_columns":old_present,
      "crop_columns_merged":cropcols,
      "crop_column_count":len(cropcols),
      "resource_audit":audit,
      "downstream_evidence_preserved":True,
      "geometry_source":"Stage 10W downstream board",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
