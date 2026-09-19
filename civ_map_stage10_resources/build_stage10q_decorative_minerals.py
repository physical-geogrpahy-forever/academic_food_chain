#!/usr/bin/env python3
"""
Stage 10Q: build documented-source evidence for decorative mineral luxuries
not adequately covered by MRDS: JADE, AMBER, LAPIS_LAZULI.

The CSV contains named, source-backed districts/localities. Radius and weight are
game-evidence parameters, not reserve estimates. Evidence decays linearly with
distance from each documented source center.

Evidence only. No final placement or gameplay thinning.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("sources_csv")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10Q_DECORATIVE_MINERALS")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()
    cent=land.copy()
    cent["geometry"]=cent.geometry.centroid

    src=pd.read_csv(a.sources_csv)
    req={"resource","id","name","lat","lon","radius_km","weight","class","source_url"}
    miss=req-set(src.columns)
    if miss:
        raise RuntimeError(f"missing source columns: {sorted(miss)}")
    srcg=gpd.GeoDataFrame(src,geometry=gpd.points_from_xy(src.lon,src.lat),crs=4326).to_crs(board.crs)

    out=land[["id"]].copy()
    audit=[]
    for resource,g in srcg.groupby("resource"):
        score=pd.Series(0.0,index=land.index)
        count=pd.Series(0,index=land.index,dtype="int16")
        maxw=pd.Series(0.0,index=land.index)
        rows=[]
        for _,r in g.iterrows():
            radius=float(r.radius_km)*1000
            d=cent.geometry.distance(r.geometry)
            hit=d.le(radius)
            frac=(1.0-d.loc[hit]/radius).clip(lower=0)
            ev=float(r.weight)*(0.35+0.65*frac)
            score.loc[hit]+=ev
            count.loc[hit]+=1
            maxw.loc[hit]=np.maximum(maxw.loc[hit],float(r.weight))
            rows.append({
              "id":r.id,"name":r["name"],"class":r["class"],
              "radius_km":float(r.radius_km),"weight":float(r.weight),
              "hexes":int(hit.sum()),"source_url":r.source_url,
            })
        out[resource+"_DOC_SCORE"]=score.to_numpy()
        out[resource+"_DOC_SOURCE_N"]=count.to_numpy()
        out[resource+"_DOC_MAX_WEIGHT"]=maxw.to_numpy()
        out[resource+"_DOC_ANY"]=(score.to_numpy()>0).astype("uint8")
        audit.append({
          "resource":resource,
          "source_regions":int(len(g)),
          "evidence_hexes":int((score>0).sum()),
          "max_score":float(score.max()),
          "sources":rows,
        })

    evcols=[c for c in out.columns if c!="id"]
    overlap=[c for c in evcols if c in board.columns]
    if overlap: board=board.drop(columns=overlap)
    board=board.merge(out,on="id",how="left",validate="one_to_one")
    for c in evcols: board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10q_decorative_minerals",driver="GPKG")
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    summary={
      "stage":"10Q",
      "resources":audit,
      "policy":"documented source districts only; radius/weight are evidence parameters, not reserve estimates",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
