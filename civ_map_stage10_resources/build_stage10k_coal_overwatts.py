#!/usr/bin/env python3
"""
Stage 10K provisional coal evidence from the public OverWatts API.

OverWatts republishes open Global Energy Monitor mine data and exposes a public
GeoJSON API. This stage is intentionally marked provisional because the current
GEM canonical release is August 2026 while the OverWatts source note may lag it.

Only features with mineral == coal are retained. Coordinates and production
values are treated as evidence, not final Civ placement.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

API="https://www.overwatts.com/api/public/assets"

STATUS_W={
    "operating":4,
    "construction":3,
    "under construction":3,
    "proposed":2,
    "idle":2,
    "mothballed":2,
    "shelved":1,
}

def fetch_all(limit=1000):
    feats=[]
    offset=0
    total=None
    sess=requests.Session()
    sess.headers.update({"User-Agent":"CIV-map-resource-research/1.0"})
    while total is None or offset < total:
        r=sess.get(API,params={"kind":"mine","limit":limit,"offset":offset},timeout=90)
        r.raise_for_status()
        obj=r.json()
        if total is None:
            meta=obj.get("meta",{})
            total=int(meta.get("total",meta.get("count",0)))
            if total <= 0:
                raise RuntimeError(f"invalid API total: {meta}")
        batch=obj.get("features",[])
        if not batch:
            break
        feats.extend(batch)
        offset += len(batch)
        print(f"fetched {offset}/{total}")
        if len(batch) < limit:
            break
        time.sleep(0.2)
    return feats,total

def num(v):
    try:
        x=float(v)
        return max(0.0,x)
    except Exception:
        return 0.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--layer",default="game_map_stage10i_horse_evidence")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10K_COAL_OVERWATTS")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board[board.SURFACE.eq("LAND")][["id","geometry"]].copy()
    if len(land)!=68048:
        raise RuntimeError(f"LAND count {len(land)}")

    feats,total=fetch_all()
    rows=[]
    geoms=[]
    for f in feats:
        p=f.get("properties") or {}
        mineral=str(p.get("mineral") or "").strip().lower()
        if mineral!="coal":
            continue
        g=f.get("geometry")
        if not g:
            continue
        try:
            geom=shape(g)
        except Exception:
            continue
        if geom.is_empty:
            continue
        status=str(p.get("status") or "").strip().lower()
        rows.append({
            "OW_ID":str(p.get("id") or f.get("id") or ""),
            "OW_NAME":str(p.get("name") or ""),
            "OW_STATUS":status,
            "OW_STATUS_W":STATUS_W.get(status,1),
            "OW_PROD_MTPA":num(p.get("productionMtpa")),
            "OW_SOURCE":str(p.get("source") or ""),
            "OW_GEMWIKI":str(p.get("gemWiki") or ""),
        })
        geoms.append(geom)

    src=gpd.GeoDataFrame(rows,geometry=geoms,crs=4326).to_crs(board.crs)
    # Mine API records are points in the derivative atlas.
    j=gpd.sjoin(src,land,predicate="within",how="inner")
    if len(j)==0:
        raise RuntimeError("no coal mine intersections")
    j=j.drop_duplicates(subset=["OW_ID","id"])

    agg=j.groupby("id",as_index=False).agg(
        COAL_OW_MINES=("OW_ID","nunique"),
        COAL_OW_SCORE=("OW_STATUS_W","sum"),
        COAL_OW_PROD_MTPA=("OW_PROD_MTPA","sum"),
        COAL_OW_OPERATING=("OW_STATUS",lambda s:int((s=="operating").sum())),
    )
    agg["COAL_OW_ANY"]=(agg.COAL_OW_MINES>0).astype("uint8")

    board=board.merge(agg,on="id",how="left",validate="one_to_one")
    for c in [x for x in agg.columns if x!="id"]:
        board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10k_coal_overwatts",driver="GPKG")
    agg.to_csv(a.prefix+"_EVIDENCE.csv",index=False)

    summary={
      "stage":"10K",
      "source":"OverWatts public API, mine assets; underlying mine source attributed by OverWatts to Global Energy Monitor",
      "source_api":API+"?kind=mine",
      "provisional":True,
      "reason_provisional":"Derivative public API is used because the latest GEM full mine-level download is form-gated; replace with GEM August 2026 original before final lock if obtainable.",
      "api_total_mine_features":int(total),
      "coal_features_retained":int(len(src)),
      "coal_features_joined":int(len(j)),
      "coal_hexes":int(agg.COAL_OW_ANY.sum()),
      "production_mtpa_sum":float(agg.COAL_OW_PROD_MTPA.sum()),
      "status_weights":STATUS_W,
      "coordinate_note":"OverWatts notes values are approximate; source provenance preserved.",
      "placement_policy":"Evidence only. No gameplay thinning.",
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
