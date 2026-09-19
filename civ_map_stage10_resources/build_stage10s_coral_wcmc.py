#!/usr/bin/env python3
"""
Stage 10S: aggregate UNEP-WCMC global warm-water coral reef data to canonical
COAST/OCEAN hexes.

Source:
  Global Distribution of Coral Reefs, WCMC-008, v4.1.
  ArcGIS FeatureServer exposes:
    layer 0 = point reefs
    layer 1 = polygon reefs

The script queries public GeoJSON pages directly. Raw UNEP-WCMC data are not
redistributed in the artifact; only aggregated hex evidence is retained.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import requests
import pandas as pd
import geopandas as gpd

BASE="https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer"

def fetch_layer(layer, page_size=2000):
    feats=[]
    offset=0
    while True:
        params={
          "where":"1=1",
          "outFields":"*",
          "returnGeometry":"true",
          "outSR":"4326",
          "f":"geojson",
          "resultOffset":offset,
          "resultRecordCount":page_size,
        }
        r=requests.get(f"{BASE}/{layer}/query",params=params,timeout=120)
        r.raise_for_status()
        js=r.json()
        batch=js.get("features",[])
        feats.extend(batch)
        print("layer",layer,"offset",offset,"batch",len(batch),"total",len(feats),flush=True)
        if len(batch)<page_size:
            break
        offset+=len(batch)
        time.sleep(0.05)
    return {"type":"FeatureCollection","features":feats}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10S_CORAL_WCMC")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")

    water=board.loc[board.SURFACE.isin(["COAST","OCEAN"]),["id","SURFACE","geometry"]].copy()
    if len(water)==0:
        raise RuntimeError("no water hexes")

    fc_pt=fetch_layer(0)
    fc_py=fetch_layer(1)

    pt=gpd.GeoDataFrame.from_features(fc_pt,crs=4326)
    py=gpd.GeoDataFrame.from_features(fc_py,crs=4326)
    if len(pt): pt=pt.to_crs(board.crs)
    if len(py): py=py.to_crs(board.crs)

    out=water[["id"]].copy()

    if len(pt):
        j=gpd.sjoin(water,pt[["geometry"]],predicate="intersects",how="inner")
        pc=j.groupby("id").size().rename("CORAL_WCMC_POINT_N").reset_index()
        out=out.merge(pc,on="id",how="left")
    else:
        out["CORAL_WCMC_POINT_N"]=0

    if len(py):
        # Intersection area gives stronger evidence than simple polygon count.
        pairs=gpd.sjoin(water,py[["geometry"]],predicate="intersects",how="inner")
        vals=[]
        for hid,g in pairs.groupby("id"):
            hgeom=water.loc[water.id.eq(hid),"geometry"].iloc[0]
            idxs=g.index_right.dropna().astype(int).unique()
            area=0.0
            for ix in idxs:
                geom=py.loc[ix,"geometry"]
                if geom is not None and not geom.is_empty:
                    area += hgeom.intersection(geom).area/1e6
            vals.append({"id":int(hid),"CORAL_WCMC_POLY_N":int(len(idxs)),"CORAL_WCMC_AREA_KM2":float(area)})
        pa=pd.DataFrame(vals)
        out=out.merge(pa,on="id",how="left")
    else:
        out["CORAL_WCMC_POLY_N"]=0
        out["CORAL_WCMC_AREA_KM2"]=0.0

    for c in ["CORAL_WCMC_POINT_N","CORAL_WCMC_POLY_N","CORAL_WCMC_AREA_KM2"]:
        out[c]=pd.to_numeric(out[c],errors="coerce").fillna(0)
    out["CORAL_WCMC_SCORE"]=(
        out["CORAL_WCMC_POINT_N"]+
        out["CORAL_WCMC_POLY_N"]+
        out["CORAL_WCMC_AREA_KM2"].clip(lower=0)
    )
    out["CORAL_WCMC_ANY"]=(out.CORAL_WCMC_SCORE>0).astype("uint8")

    overlap=[c for c in out.columns if c!="id" and c in board.columns]
    if overlap: board=board.drop(columns=overlap)
    board=board.merge(out,on="id",how="left",validate="one_to_one")
    for c in out.columns:
        if c!="id": board[c]=board[c].fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10s_coral_wcmc",driver="GPKG")
    board.loc[board.CORAL_WCMC_ANY.gt(0),
              ["id","SURFACE","CORAL_WCMC_POINT_N","CORAL_WCMC_POLY_N","CORAL_WCMC_AREA_KM2","CORAL_WCMC_SCORE"]].to_csv(
        a.prefix+"_EVIDENCE.csv",index=False
    )
    summary={
      "stage":"10S",
      "source":"UNEP-WCMC Global Distribution of Coral Reefs, WCMC-008 v4.1",
      "feature_service":BASE,
      "point_features":int(len(pt)),
      "polygon_features":int(len(py)),
      "coral_evidence_hexes":int(out.CORAL_WCMC_ANY.sum()),
      "surface_counts":board.loc[board.CORAL_WCMC_ANY.gt(0),"SURFACE"].value_counts().to_dict(),
      "raw_data_redistributed":False,
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
