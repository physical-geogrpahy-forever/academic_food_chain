#!/usr/bin/env python3
"""
Stage 10L: add documentary historical/natural niter evidence to canonical 50-km LAND hexes.

The input CSV contains only documented production/source regions. It is not a
generic climate/population proxy. Each source is represented as a regional
center with an explicit radius and weight. Evidence decays linearly from the
center to the documentary radius and overlapping sources add.

Output:
  NITER_HIST_SCORE
  NITER_HIST_SOURCE_N
  NITER_HIST_MAX_WEIGHT
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("sources_csv")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10L_NITER_HIST_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")

    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    cent=land.copy()
    cent["geometry"]=land.geometry.centroid

    src=pd.read_csv(a.sources_csv)
    req={"id","name","lat","lon","radius_km","weight","evidence_type","source_short","source_url"}
    miss=req-set(src.columns)
    if miss:
        raise RuntimeError(f"source CSV missing columns: {sorted(miss)}")
    srcg=gpd.GeoDataFrame(
        src.copy(),
        geometry=gpd.points_from_xy(src.lon,src.lat),
        crs=4326,
    ).to_crs(board.crs)

    score=pd.Series(0.0,index=land.index)
    count=pd.Series(0,index=land.index,dtype="int16")
    maxw=pd.Series(0.0,index=land.index)

    audit=[]
    for _,r in srcg.iterrows():
        radius_m=float(r.radius_km)*1000.0
        # Board CRS is metric; distance to hex centroid is adequate at 50 km scale.
        d=cent.geometry.distance(r.geometry)
        hit=d.le(radius_m)
        if not hit.any():
            audit.append({"id":r.id,"name":r["name"],"hexes":0})
            continue
        frac=(1.0-d.loc[hit]/radius_m).clip(lower=0)
        ev=float(r.weight)*(0.35+0.65*frac)
        score.loc[hit]+=ev
        count.loc[hit]+=1
        maxw.loc[hit]=np.maximum(maxw.loc[hit],float(r.weight))
        audit.append({
            "id":r.id,"name":r["name"],
            "hexes":int(hit.sum()),
            "radius_km":float(r.radius_km),
            "weight":float(r.weight),
            "evidence_type":r.evidence_type,
        })

    ev=pd.DataFrame({
        "id":land.id.to_numpy(),
        "NITER_HIST_SCORE":score.to_numpy(),
        "NITER_HIST_SOURCE_N":count.to_numpy(),
        "NITER_HIST_MAX_WEIGHT":maxw.to_numpy(),
    })

    overlap=[c for c in ev.columns if c!="id" and c in board.columns]
    if overlap:
        board=board.drop(columns=overlap)
    board=board.merge(ev,on="id",how="left",validate="one_to_one")
    for c in ["NITER_HIST_SCORE","NITER_HIST_SOURCE_N","NITER_HIST_MAX_WEIGHT"]:
        board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10l_niter_hist_evidence",driver="GPKG")
    board.loc[board.NITER_HIST_SCORE.gt(0),
              ["id","SURFACE","NITER_HIST_SCORE","NITER_HIST_SOURCE_N","NITER_HIST_MAX_WEIGHT"]].to_csv(
        a.prefix+"_EVIDENCE.csv",index=False
    )

    summary={
        "stage":"10L niter documentary evidence",
        "source_file":Path(a.sources_csv).name,
        "source_records":int(len(src)),
        "evidence_hexes":int(board.NITER_HIST_SCORE.gt(0).sum()),
        "max_score":float(board.NITER_HIST_SCORE.max()),
        "audit":audit,
        "policy":"documented source/production regions only; no generic climate or population proxy",
        "final_placement":False,
        "gameplay_thinning_applied":False,
        "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
