#!/usr/bin/env python3
"""
Stage 6A: Natural Earth 1:10m reef candidates on canonical water hexes.

This stage does NOT equate every reef with a Civ-style ATOLL. It preserves the
source as REEF_CANDIDATE and computes intersected reef length per water hex.
Final thinning / ATOLL promotion is deferred.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np

QA=[
 ("Great Barrier Reef",142,155,-25,-10),
 ("Coral Triangle",115,135,-12,10),
 ("Red Sea",32,44,12,30),
 ("Caribbean",-88,-60,8,25),
 ("Maldives",71,75,-1,8),
 ("Central Pacific",165,-150,-25,15),
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage5_gpkg")
    ap.add_argument("reef_shp")
    ap.add_argument("--layer",default="game_map_stage5a_hydro_features")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE6A_REEFS")
    a=ap.parse_args()

    board=gpd.read_file(a.stage5_gpkg,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    if board.crs.to_epsg()!=8857:
        board=board.to_crs(8857)

    reefs=gpd.read_file(a.reef_shp)
    if reefs.crs is None:
        reefs=reefs.set_crs(4326)
    reefs=reefs.to_crs(board.crs)

    water=board[board.SURFACE.isin(["COAST","OCEAN"])][["id","SURFACE","geometry"]].copy()
    # Spatial join candidates, then exact line/polygon intersection length.
    pairs=gpd.sjoin(water,reefs[["geometry"]],predicate="intersects",how="inner")
    rows=[]
    for ridx, grp in pairs.groupby(level=0):
        poly=water.loc[ridx].geometry
        length=0.0
        nsrc=0
        for j in grp.index_right.unique():
            inter=poly.intersection(reefs.loc[j].geometry)
            if not inter.is_empty:
                length += float(inter.length)
                nsrc += 1
        rows.append({"id":int(water.loc[ridx,"id"]),"REEF_LEN_M":length,"REEF_SRC_N":nsrc})

    metrics=pd.DataFrame(rows)
    board=board.merge(metrics,on="id",how="left",validate="one_to_one")
    board["REEF_LEN_M"]=board["REEF_LEN_M"].fillna(0.0)
    board["REEF_SRC_N"]=board["REEF_SRC_N"].fillna(0).astype("int16")
    board["REEF_CANDIDATE"]=((board["REEF_LEN_M"]>0)&board.SURFACE.isin(["COAST","OCEAN"])).astype("uint8")

    # QA uses centroid lon/lat already carried from Stage 2B when available.
    if "LON" not in board.columns or "LAT" not in board.columns:
        c=board.geometry.centroid
        ll=gpd.GeoSeries(c,crs=board.crs).to_crs(4326)
        board["LON"]=ll.x.to_numpy();board["LAT"]=ll.y.to_numpy()

    q=[]
    for name,x0,x1,y0,y1 in QA:
        if x0<=x1:
            m=(board.LON>=x0)&(board.LON<=x1)&(board.LAT>=y0)&(board.LAT<=y1)
        else:
            m=((board.LON>=x0)|(board.LON<=x1))&(board.LAT>=y0)&(board.LAT<=y1)
        n=int(board.loc[m,"REEF_CANDIDATE"].sum())
        q.append({"region":name,"reef_hexes":n,"pass":bool(n>0)})
    qa=pd.DataFrame(q)
    qa.to_csv(a.prefix+"_QA.csv",index=False)

    nonwater=int(board.loc[~board.SURFACE.isin(["COAST","OCEAN"]),"REEF_CANDIDATE"].sum())
    summary={
      "stage":"6A",
      "source":"Natural Earth 1:10m ne_10m_reefs",
      "source_features":int(len(reefs)),
      "candidate_water_hexes":int(board.REEF_CANDIDATE.sum()),
      "coast_candidates":int(board.loc[board.SURFACE.eq("COAST"),"REEF_CANDIDATE"].sum()),
      "ocean_candidates":int(board.loc[board.SURFACE.eq("OCEAN"),"REEF_CANDIDATE"].sum()),
      "nonwater_candidates":nonwater,
      "qa_pass":int(qa["pass"].sum()),
      "qa_total":int(len(qa)),
      "policy":"REEF_CANDIDATE only; no automatic ATOLL conversion or thinning yet",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    board.to_file(a.prefix+".gpkg",layer="game_map_stage6a_reef_candidates",driver="GPKG")
    board.loc[board.REEF_CANDIDATE.eq(1),
              ["id","SURFACE","REEF_LEN_M","REEF_SRC_N","LON","LAT"]].to_csv(a.prefix+"_CANDIDATES.csv",index=False)
    print(json.dumps(summary,indent=2))
    print(qa.to_string(index=False))

if __name__=="__main__":main()
