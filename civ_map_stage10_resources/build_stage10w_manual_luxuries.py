#!/usr/bin/env python3
"""
Stage 10W: documentary source-region evidence for remaining terrestrial
luxury resources: DYES, INCENSE, SILK, TRUFFLES, PERFUME.

PERFUME means raw fragrance-material source regions, not locations of finished
perfume manufacture.

Centers and radii are explicit game-scale approximations around documented
source/production regions. Evidence decays linearly with distance inside each
radius and overlapping documentary regions add.

Evidence only. No final resource placement or gameplay thinning.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

RESOURCES=["DYES","INCENSE","SILK","TRUFFLES","PERFUME"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("sources_csv")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10W_MANUAL_LUXURIES")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    if len(land)!=68048:
        raise RuntimeError(f"LAND count changed: {len(land)}")
    cent=land.copy()
    cent["geometry"]=land.geometry.centroid

    src=pd.read_csv(a.sources_csv)
    req={"resource","id","name","lat","lon","radius_km","weight","source_short","source_url"}
    miss=req-set(src.columns)
    if miss:
        raise RuntimeError(f"missing source columns: {sorted(miss)}")
    unknown=set(src.resource)-set(RESOURCES)
    if unknown:
        raise RuntimeError(f"unknown resources: {sorted(unknown)}")
    missing_res=set(RESOURCES)-set(src.resource)
    if missing_res:
        raise RuntimeError(f"resources without source rows: {sorted(missing_res)}")

    srcg=gpd.GeoDataFrame(
        src,geometry=gpd.points_from_xy(src.lon,src.lat),crs=4326
    ).to_crs(board.crs)

    evidence=land[["id"]].copy()
    audits=[]
    for resource in RESOURCES:
        score=pd.Series(0.0,index=land.index,dtype="float64")
        count=pd.Series(0,index=land.index,dtype="int16")
        maxw=pd.Series(0.0,index=land.index,dtype="float64")
        sub=srcg.loc[srcg.resource.eq(resource)]
        src_audit=[]

        for _,r in sub.iterrows():
            rad=float(r.radius_km)*1000.0
            if rad<=0:
                raise RuntimeError(f"{r.id}: non-positive radius")
            d=cent.geometry.distance(r.geometry)
            hit=d.le(rad)
            if hit.any():
                frac=(1-d.loc[hit]/rad).clip(lower=0,upper=1)
                ev=float(r.weight)*(0.35+0.65*frac)
                score.loc[hit]+=ev
                count.loc[hit]+=1
                maxw.loc[hit]=np.maximum(maxw.loc[hit],float(r.weight))
            src_audit.append({
                "id":str(r.id),
                "name":str(r["name"]),
                "radius_km":float(r.radius_km),
                "weight":float(r.weight),
                "hexes":int(hit.sum()),
                "source_short":str(r.source_short),
                "source_url":str(r.source_url),
            })

        evidence[f"{resource}_DOC_SCORE"]=score.to_numpy()
        evidence[f"{resource}_DOC_SOURCE_N"]=count.to_numpy()
        evidence[f"{resource}_DOC_MAX_WEIGHT"]=maxw.to_numpy()
        evidence[f"{resource}_DOC_ANY"]=(score.to_numpy()>0).astype("uint8")
        audits.append({
            "resource":resource,
            "source_regions":int(len(sub)),
            "evidence_hexes":int((score>0).sum()),
            "max_score":float(score.max()),
            "sources":src_audit,
        })

    evcols=[c for c in evidence.columns if c!="id"]
    overlap=[c for c in evcols if c in board.columns]
    if overlap:
        board=board.drop(columns=overlap)
    board=board.merge(evidence,on="id",how="left",validate="one_to_one")
    for c in evcols:
        board[c]=board[c].fillna(0)

    board.to_file(
        a.prefix+".gpkg",
        layer="game_map_stage10w_manual_luxuries",
        driver="GPKG"
    )
    evidence.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    summary={
        "stage":"10W",
        "resources":audits,
        "policy":"documented source/production regions; center and radius are explicit game-scale spatial approximations",
        "perfume_policy":"PERFUME represents raw fragrance-material source regions only, not finished-product manufacture",
        "final_placement":False,
        "gameplay_thinning_applied":False,
        "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8"
    )
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
