#!/usr/bin/env python3
"""
Stage 10F: aggregate Global Energy Monitor GOGET March 2026 oil/gas field
evidence to canonical 50-km hexes.

Civ-style OIL evidence includes fuel types "oil" and "oil and gas".
Gas evidence is retained separately for provenance/custom gameplay.

Status weights:
  operating=4, in-development=3, discovered=2, mothballed=1.
Cancelled, abandoned, decommissioning, storage and unknown do not contribute.

Field outline WKT is used when parseable; otherwise the published coordinate is
used as a point. No random resource placement is performed.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point

STATUS_W={
 "operating":4,
 "in-development":3,
 "discovered":2,
 "mothballed":1,
}

def parse_geom(row):
    s=str(row.get("Field outline (WKT)","") or "").strip()
    if s and s.lower()!="nan":
        try:
            g=wkt.loads(s)
            if g is not None and not g.is_empty:
                return g
        except Exception:
            pass
    try:
        x=float(row["Longitude"]); y=float(row["Latitude"])
        if -180<=x<=180 and -90<=y<=90:
            return Point(x,y)
    except Exception:
        pass
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("goget_csv")
    ap.add_argument("--layer",default="game_map_stage10c_mrds_evidence")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10F_GOGET_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    active=board[board.SURFACE.isin(["LAND","COAST","OCEAN"])][["id","SURFACE","geometry"]].copy()

    df=pd.read_csv(a.goget_csv,low_memory=False,encoding_errors="replace")
    df["STATUS_N"]=df["Status"].fillna("").astype(str).str.lower().str.strip()
    df["STATUS_W"]=df["STATUS_N"].map(STATUS_W).fillna(0).astype("int16")
    df["FUEL_N"]=df["Fuel type"].fillna("").astype(str).str.lower().str.strip()
    keep=df["STATUS_W"].gt(0)
    df=df.loc[keep].copy()
    geoms=df.apply(parse_geom,axis=1)
    ok=geoms.notna()
    df=df.loc[ok].copy()
    geoms=geoms.loc[ok]
    src=gpd.GeoDataFrame(df,geometry=list(geoms),crs=4326).to_crs(board.crs)

    # Spatial intersection. A polygon field may touch multiple game hexes.
    pairs=gpd.sjoin(active,src[["Fuel type","FUEL_N","STATUS_N","STATUS_W","Unit ID","Unit Name","geometry"]],
                    predicate="intersects",how="inner")
    if len(pairs)==0:
        raise RuntimeError("no GOGET intersections")

    p=pairs.copy()
    p["OIL_HIT"]=p["FUEL_N"].isin(["oil","oil and gas"]).astype("int8")
    p["GAS_HIT"]=p["FUEL_N"].isin(["gas","gas and condensate","oil and gas"]).astype("int8")
    p["OIL_SCORE"]=p["OIL_HIT"]*p["STATUS_W"]
    p["GAS_SCORE"]=p["GAS_HIT"]*p["STATUS_W"]

    # De-duplicate the same source unit repeated in one hex by spatial join.
    p=p.drop_duplicates(subset=["id","Unit ID"])
    rows=[]
    for hid,g in p.groupby("id"):
        oil=g[g.OIL_HIT.eq(1)]
        gas=g[g.GAS_HIT.eq(1)]
        rows.append({
          "id":int(hid),
          "OIL_GEM_FIELDS":int(len(oil)),
          "OIL_GEM_SCORE":int(oil.OIL_SCORE.sum()),
          "GAS_GEM_FIELDS":int(len(gas)),
          "GAS_GEM_SCORE":int(gas.GAS_SCORE.sum()),
          "GOGET_FIELDS_ANY":int(g["Unit ID"].nunique()),
        })
    ev=pd.DataFrame(rows)
    for c in ["OIL_GEM_FIELDS","OIL_GEM_SCORE","GAS_GEM_FIELDS","GAS_GEM_SCORE","GOGET_FIELDS_ANY"]:
        ev[c]=ev[c].astype("int32")
    ev["OIL_GEM_ANY"]=(ev.OIL_GEM_SCORE>0).astype("uint8")
    ev["GAS_GEM_ANY"]=(ev.GAS_GEM_SCORE>0).astype("uint8")

    board=board.merge(ev,on="id",how="left",validate="one_to_one")
    cols=[c for c in ev.columns if c!="id"]
    for c in cols: board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10f_goget_evidence",driver="GPKG")
    board.loc[(board.OIL_GEM_ANY==1)|(board.GAS_GEM_ANY==1),
              ["id","SURFACE"]+cols].to_csv(a.prefix+"_EVIDENCE.csv",index=False)

    summary={
      "stage":"10F",
      "source":"Global Energy Monitor GOGET March 2026 field-level main data",
      "source_rows":int(len(pd.read_csv(a.goget_csv,low_memory=False))),
      "eligible_status_rows_with_geometry":int(len(src)),
      "hex_source_intersections":int(len(p)),
      "oil_evidence_hexes":int(board.OIL_GEM_ANY.sum()),
      "gas_evidence_hexes":int(board.GAS_GEM_ANY.sum()),
      "oil_surface_counts":board.loc[board.OIL_GEM_ANY.eq(1),"SURFACE"].value_counts().to_dict(),
      "gas_surface_counts":board.loc[board.GAS_GEM_ANY.eq(1),"SURFACE"].value_counts().to_dict(),
      "status_weights":STATUS_W,
      "oil_fuels":["oil","oil and gas"],
      "reserve_column":reserve_col,
      "production_column":production_col,
      "gas_fuels":["gas","gas and condensate","oil and gas"],
      "placement_policy":"Evidence only; no random placement and no gameplay thinning.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
