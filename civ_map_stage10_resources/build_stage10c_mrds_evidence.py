#!/usr/bin/env python3
"""
Stage 10C: aggregate USGS MRDS mineral evidence to canonical 50-km LAND hexes.

This does NOT finalize resource placement. It preserves transparent evidence:
  *_MRDS_PRIMARY_N
  *_MRDS_SECONDARY_N
  *_MRDS_TERTIARY_N
  *_MRDS_SCORE = 3*primary + 2*secondary + tertiary
  *_MRDS_SIZE_SUM / *_MRDS_SIZE_MAX when deposit-size information exists
  *_MRDS_ANY

Coal is retained only as a diagnostic because MRDS coal coverage is sparse and
is not considered sufficient for final coal placement.
"""
from __future__ import annotations
import argparse, json, zipfile, re
from pathlib import Path
import pandas as pd
import geopandas as gpd

GROUPS={
 "IRON":["iron"],
 "ALUMINUM":["aluminum","bauxite"],
 "URANIUM":["uranium"],
 "NITER_NATURAL":["nitrate","nitratite","niter","saltpeter","saltpetre"],
 "GOLD":["gold"],
 "SILVER":["silver"],
 "COPPER":["copper"],
 "SALT":["salt","halite"],
 "MARBLE":["marble"],
 "GEMS":["gemstone","diamond","emerald","ruby","sapphire"],
 "COAL_DIAG":["coal"],
}

def normcol(s):
    return s.fillna("").astype(str).str.lower()

def matches(series,keys):
    pat="|".join(re.escape(k) for k in keys)
    return series.str.contains(pat,regex=True,na=False)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("mrds_zip")
    ap.add_argument("--layer",default="game_map_stage9a_consolidated")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10C_MRDS_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board[board.SURFACE.eq("LAND")][["id","geometry"]].copy()
    if len(land)!=68048:
        raise RuntimeError(len(land))

    z=zipfile.ZipFile(a.mrds_zip)
    member=max((n for n in z.namelist() if n.lower().endswith(".csv")),
               key=lambda n:z.getinfo(n).file_size)
    with z.open(member) as f:
        df=pd.read_csv(f,low_memory=False,encoding_errors="replace")

    lat=pd.to_numeric(df.latitude,errors="coerce")
    lon=pd.to_numeric(df.longitude,errors="coerce")
    valid=lat.between(-90,90)&lon.between(-180,180)
    df=df.loc[valid].copy()
    df["latitude"]=lat[valid].to_numpy()
    df["longitude"]=lon[valid].to_numpy()

    for c in ["commod1","commod2","commod3"]:
        if c not in df.columns:
            raise RuntimeError(f"MRDS missing required commodity column: {c}")
        df[c+"_N"]=normcol(df[c])

    # MRDS historically stores relative deposit size as L/M/S in DEP_SIZE.
    size_col=next((c for c in df.columns if c.lower() in {"dep_size","deposit_size"}),None)
    if size_col:
        sz=normcol(df[size_col]).str.strip()
        df["DEP_SIZE_W"]=sz.map({
            "l":3,"large":3,
            "m":2,"medium":2,
            "s":1,"small":1,
        }).fillna(0).astype("int16")
    else:
        df["DEP_SIZE_W"]=0

    pts=gpd.GeoDataFrame(
        df,geometry=gpd.points_from_xy(df.longitude,df.latitude),crs=4326
    ).to_crs(board.crs)
    joined=gpd.sjoin(pts,land,predicate="within",how="inner")
    if "id" not in joined.columns:
        raise RuntimeError("canonical id missing after join")

    out=land[["id"]].copy()
    audit=[]
    for group,keys in GROUPS.items():
        p=matches(joined["commod1_N"],keys)
        s=matches(joined["commod2_N"],keys) & ~p
        t=matches(joined["commod3_N"],keys) & ~p & ~s
        hit=p|s|t

        tmp=pd.DataFrame({
            "id":joined["id"].astype("int64"),
            "P":p.astype("int8"),
            "S":s.astype("int8"),
            "T":t.astype("int8"),
            "SZ":joined["DEP_SIZE_W"].where(hit,0).astype("int16"),
        })
        agg=tmp.groupby("id",as_index=False).agg(
            P=("P","sum"), S=("S","sum"), T=("T","sum"),
            SZ_SUM=("SZ","sum"), SZ_MAX=("SZ","max"),
        )
        agg[group+"_MRDS_PRIMARY_N"]=agg.pop("P")
        agg[group+"_MRDS_SECONDARY_N"]=agg.pop("S")
        agg[group+"_MRDS_TERTIARY_N"]=agg.pop("T")
        agg[group+"_MRDS_SIZE_SUM"]=agg.pop("SZ_SUM")
        agg[group+"_MRDS_SIZE_MAX"]=agg.pop("SZ_MAX")

        out=out.merge(agg,on="id",how="left",validate="one_to_one")
        count_cols=[
            group+"_MRDS_PRIMARY_N",group+"_MRDS_SECONDARY_N",group+"_MRDS_TERTIARY_N",
            group+"_MRDS_SIZE_SUM",group+"_MRDS_SIZE_MAX",
        ]
        for c in count_cols:
            out[c]=out[c].fillna(0).astype("int32")

        out[group+"_MRDS_SCORE"]=(
            3*out[group+"_MRDS_PRIMARY_N"]+
            2*out[group+"_MRDS_SECONDARY_N"]+
            out[group+"_MRDS_TERTIARY_N"]
        ).astype("int32")
        out[group+"_MRDS_ANY"]=(out[group+"_MRDS_SCORE"]>0).astype("uint8")

        audit.append({
          "group":group,
          "matched_records":int(hit.sum()),
          "hexes_with_evidence":int(out[group+"_MRDS_ANY"].sum()),
          "max_score":int(out[group+"_MRDS_SCORE"].max()),
          "score_sum":int(out[group+"_MRDS_SCORE"].sum()),
          "size_evidence_sum":int(out[group+"_MRDS_SIZE_SUM"].sum()),
          "max_deposit_size_code":int(out[group+"_MRDS_SIZE_MAX"].max()),
        })

    audit=pd.DataFrame(audit)
    audit.to_csv(a.prefix+"_AUDIT.csv",index=False)
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)

    board=board.merge(out,on="id",how="left",validate="one_to_one")
    evcols=[c for c in out.columns if c!="id"]
    for c in evcols:
        board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10c_mrds_evidence",driver="GPKG")

    summary={
      "stage":"10C",
      "source":"USGS MRDS bulk CSV",
      "mrds_rows":int(len(df)),
      "mrds_points_joined_to_land_hexes":int(len(joined)),
      "land_hexes":68048,
      "groups":audit.to_dict(orient="records"),
      "deposit_size_column":size_col,
      "deposit_size_weights":{"small":1,"medium":2,"large":3},
      "coal_policy":"COAL_DIAG is diagnostic only; MRDS coverage is too sparse for final coal placement.",
      "placement_policy":"Evidence only. No random placement and no gameplay thinning yet.",
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(audit.to_string(index=False))

if __name__=="__main__":
    main()
