#!/usr/bin/env python3
"""
Stage 10J: aggregate Global Energy Monitor Global Coal Mine Tracker May 2026
non-closed mine evidence to canonical 50-km LAND hexes.

Official source sheet ID is published in GEM's own tracker metadata repository.
All non-closed project statuses represent documented coal occurrences/projects;
status weights are retained transparently and capacity/production are preserved
as evidence rather than converted directly into final Civ resource placement.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd

STATUS_W={
 "Operating":4,
 "Mothballed":3,
 "Proposed":2,
 "Shelved":1,
 "Cancelled":1,
}

def num(s):
    return pd.to_numeric(s.replace({"-":None,"Unknown":None,"NA":None,"N/A":None}),errors="coerce")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("coal_csv")
    ap.add_argument("--layer",default="game_map_stage10i_horse_evidence")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10J_COAL_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board[board.SURFACE.eq("LAND")][["id","geometry"]].copy()
    if len(land)!=68048: raise RuntimeError(len(land))

    df=pd.read_csv(a.coal_csv,low_memory=False,encoding_errors="replace")
    required=["GEM Mine ID","Status","Latitude","Longitude"]
    miss=[c for c in required if c not in df.columns]
    if miss: raise RuntimeError("missing coal columns "+",".join(miss))
    lat=pd.to_numeric(df["Latitude"],errors="coerce")
    lon=pd.to_numeric(df["Longitude"],errors="coerce")
    valid=lat.between(-90,90)&lon.between(-180,180)
    df=df.loc[valid].copy()
    df["Latitude"]=lat[valid].to_numpy()
    df["Longitude"]=lon[valid].to_numpy()
    df["STATUS_W"]=df["Status"].map(STATUS_W).fillna(0).astype("int16")
    df=df[df.STATUS_W.gt(0)].copy()

    capcol=next((c for c in df.columns if c.strip().lower()=="capacity (mtpa)"),None)
    prodcol=next((c for c in df.columns if c.strip().lower()=="production (mt)"),None)
    if prodcol is None:
        prodcol=next((c for c in df.columns if "production" in c.lower() and "mt" in c.lower()),None)
    df["CAP_MTPA"]=num(df[capcol]) if capcol else 0.0
    df["PROD_MT"]=num(df[prodcol]) if prodcol else 0.0
    df["CAP_MTPA"]=pd.to_numeric(df["CAP_MTPA"],errors="coerce").fillna(0).clip(lower=0)
    df["PROD_MT"]=pd.to_numeric(df["PROD_MT"],errors="coerce").fillna(0).clip(lower=0)
    df["RESERVE_MT"]=pd.to_numeric(df["RESERVE_MT"],errors="coerce").fillna(0).clip(lower=0)
    df["RESOURCE_MT"]=pd.to_numeric(df["RESOURCE_MT"],errors="coerce").fillna(0).clip(lower=0)

    pts=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.Longitude,df.Latitude),crs=4326).to_crs(board.crs)
    join=gpd.sjoin(pts,land,predicate="within",how="inner")
    join=join.drop_duplicates(subset=["GEM Mine ID","id"])

    rows=[]
    for hid,g in join.groupby("id"):
        rows.append({
          "id":int(hid),
          "COAL_GEM_MINES":int(g["GEM Mine ID"].nunique()),
          "COAL_GEM_SCORE":int(g.STATUS_W.sum()),
          "COAL_GEM_CAP_MTPA":float(g.CAP_MTPA.sum()),
          "COAL_GEM_PROD_MT":float(g.PROD_MT.sum()),
          "COAL_GEM_RESERVE_MT":float(g.RESERVE_MT.sum()),
          "COAL_GEM_RESOURCE_MT":float(g.RESOURCE_MT.sum()),
          "COAL_GEM_OPERATING":int(g.Status.eq("Operating").sum()),
          "COAL_GEM_PROPOSED":int(g.Status.eq("Proposed").sum()),
          "COAL_GEM_MOTHBALLED":int(g.Status.eq("Mothballed").sum()),
        })
    ev=pd.DataFrame(rows)
    ev["COAL_GEM_ANY"]=(ev.COAL_GEM_SCORE>0).astype("uint8")

    board=board.merge(ev,on="id",how="left",validate="one_to_one")
    for c in [x for x in ev.columns if x!="id"]:board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10j_coal_evidence",driver="GPKG")
    ev.to_csv(a.prefix+"_EVIDENCE.csv",index=False)

    status_counts=df.Status.value_counts(dropna=False).to_dict()
    summary={
      "stage":"10J",
      "source":"Global Energy Monitor Global Coal Mine Tracker, May 2026, Non-closed mines",
      "official_sheet_id":"1YSlF9ADnRZH2ug9NwUGjp2bphbFZxkz1FnxSO1NV-ks",
      "source_rows_valid_coords":int(len(df)),
      "status_counts":status_counts,
      "status_weights":STATUS_W,
      "land_hexes_with_coal_evidence":int(ev.COAL_GEM_ANY.sum()),
      "mine_hex_intersections":int(len(join)),
      "total_capacity_mtpa":float(df.CAP_MTPA.sum()),
      "total_production_mt":float(df.PROD_MT.sum()),
      "capacity_column":capcol,
      "production_column":prodcol,
      "reserve_column":reservecol,
      "resource_column":resourcecol,
      "placement_policy":"Evidence only; no random placement and no gameplay thinning.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
