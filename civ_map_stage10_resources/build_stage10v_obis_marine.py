#!/usr/bin/env python3
"""
Stage 10V: marine resource evidence from OBIS gridded occurrences.

Resources:
  FISH   = Actinopterygii
  CRAB   = Brachyura
  PEARLS = Pinctada (pearl-oyster genus)

OBIS grid precision 4 is used. Because the global Actinopterygii request hits
the 100,000-feature API cap, FISH is queried by recursively splitting the
world into WKT rectangles until each response is below the cap, then identical
grid polygons are de-duplicated.

These are occurrence-evidence scores, not abundance estimates. Record count n
is transformed with log1p before aggregation to reduce sampling-effort bias.
No final placement or gameplay thinning occurs here.
"""
from __future__ import annotations
import argparse,json,time,math
from pathlib import Path
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

BASE="https://api.obis.org/v3/occurrence/grid/4"
UA={"User-Agent":"civ-game-resource-map/1.0"}
CAP=100000

TAXA={"FISH":"Actinopterygii","CRAB":"Brachyura","PEARLS":"Pinctada"}

def rect_wkt(x0,y0,x1,y1):
    return f"POLYGON(({x0} {y0},{x1} {y0},{x1} {y1},{x0} {y1},{x0} {y0}))"

def request_grid(name,bbox=None):
    params={"scientificname":name}
    if bbox is not None:
        params["geometry"]=rect_wkt(*bbox)
    for attempt in range(5):
        try:
            r=requests.get(BASE,params=params,headers=UA,timeout=240)
            r.raise_for_status()
            js=r.json()
            if js.get("type")!="FeatureCollection":
                raise RuntimeError(f"unexpected OBIS response {js.keys()}")
            return js.get("features",[])
        except Exception:
            if attempt==4: raise
            time.sleep(2*(attempt+1))

def recursive_grid(name,bbox,depth=0,max_depth=8):
    feats=request_grid(name,bbox)
    print(name,"depth",depth,"bbox",bbox,"features",len(feats),flush=True)
    if len(feats)<CAP:
        return feats
    if depth>=max_depth:
        raise RuntimeError(f"OBIS grid cap persists at max depth: {bbox}")
    x0,y0,x1,y1=bbox
    if (x1-x0)>=(y1-y0):
        m=(x0+x1)/2
        boxes=[(x0,y0,m,y1),(m,y0,x1,y1)]
    else:
        m=(y0+y1)/2
        boxes=[(x0,y0,x1,m),(x0,m,x1,y1)]
    out=[]
    for b in boxes:
        out.extend(recursive_grid(name,b,depth+1,max_depth))
    return out

def canonicalize_features(feats):
    rows={}
    for f in feats:
        geom=shape(f["geometry"])
        if geom.is_empty: continue
        # OBIS precision-4 grid polygons have stable coordinate bounds.
        b=tuple(round(v,8) for v in geom.bounds)
        n=float((f.get("properties") or {}).get("n") or 0)
        old=rows.get(b)
        if old is None or n>old["n"]:
            rows[b]={"n":n,"geometry":geom}
    g=gpd.GeoDataFrame(list(rows.values()),geometry="geometry",crs=4326)
    return g

def aggregate(water,grid,rid):
    gg=grid.to_crs(water.crs).copy()
    gg["LOGN"]=gg["n"].clip(lower=0).map(math.log1p)
    pairs=gpd.sjoin(
        water[["id","geometry"]],
        gg[["n","LOGN","geometry"]],
        how="inner",predicate="intersects"
    )
    if pairs.empty:
        return pd.DataFrame({"id":water.id})
    out=pairs.groupby("id",as_index=False).agg(
        **{
          f"{rid}_OBIS_GRID_N":("index_right","nunique"),
          f"{rid}_OBIS_LOGN_MEAN":("LOGN","mean"),
          f"{rid}_OBIS_LOGN_MAX":("LOGN","max"),
          f"{rid}_OBIS_RECORD_N_MAX":("n","max"),
        }
    )
    out[f"{rid}_OBIS_ANY"]=1
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10V_OBIS_MARINE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    water=board.loc[board.SURFACE.isin(["COAST","OCEAN"]),["id","SURFACE","geometry"]].copy()
    if water.empty: raise RuntimeError("no water hexes")

    audits=[]
    for rid,name in TAXA.items():
        if rid=="FISH":
            feats=recursive_grid(name,(-180,-90,180,90))
        else:
            feats=request_grid(name)
            if len(feats)>=CAP:
                feats=recursive_grid(name,(-180,-90,180,90))
        grid=canonicalize_features(feats)
        x=aggregate(water,grid,rid)
        evcols=[c for c in x.columns if c!="id"]
        overlap=[c for c in evcols if c in board.columns]
        if overlap: board=board.drop(columns=overlap)
        board=board.merge(x,on="id",how="left",validate="one_to_one")
        for c in evcols: board[c]=board[c].fillna(0)
        anycol=f"{rid}_OBIS_ANY"
        audits.append({
          "resource":rid,
          "scientificname":name,
          "precision":4,
          "unique_obis_grid_cells":int(len(grid)),
          "evidence_hexes":int(board[anycol].sum()),
          "surface_counts":board.loc[board[anycol].gt(0),"SURFACE"].value_counts().to_dict(),
          "max_log1p_record_count":float(board[f"{rid}_OBIS_LOGN_MAX"].max()),
        })

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10v_obis_marine",driver="GPKG")
    cols=["id","SURFACE"]+[c for c in board.columns if "_OBIS_" in c]
    board.loc[board.SURFACE.isin(["COAST","OCEAN"]),cols].to_csv(a.prefix+"_WATER_EVIDENCE.csv",index=False)
    summary={
      "stage":"10V",
      "source":"Ocean Biodiversity Information System (OBIS) API v3 occurrence grid",
      "resources":audits,
      "fish_policy":"precision-4 global grid recovered by recursive geographic splitting to avoid 100,000-feature cap",
      "score_policy":"log1p occurrence-record count retained only as evidence strength; not interpreted as animal abundance",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
