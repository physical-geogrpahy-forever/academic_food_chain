#!/usr/bin/env python3
"""
Stage 10P: aggregate USGS MRDS evidence for non-strategic Civ mineral resources.

Groups:
  COPPER, GOLD, SILVER, SALT, MARBLE, STONE, GEMS

Generic GEMS deliberately uses word-boundary patterns so "beryl" does not match
"beryllium". Amber, jade, and lapis lazuli are handled separately because MRDS
coverage is absent or too sparse for global placement.

Evidence only. No final placement or thinning.
"""
from __future__ import annotations
import argparse,json,re,zipfile
from pathlib import Path
import pandas as pd
import geopandas as gpd

GROUPS={
 "COPPER":[r"\bcopper\b"],
 "GOLD":[r"\bgold\b"],
 "SILVER":[r"\bsilver\b"],
 "SALT":[r"\bsalt\b",r"\bhalite\b"],
 "MARBLE":[r"\bmarble\b"],
 "STONE":[
   r"\bstone\b",r"\blimestone\b",r"\bgranite\b",
   r"\bsandstone\b",r"\bbasalt\b",r"\bflagstone\b",
 ],
 "GEMS":[
   r"\bgemstone\b",r"\bsemiprecious gemstone\b",
   r"\bdiamond\b",r"\bemerald\b",r"\bruby\b",r"\bsapphire\b",
   r"\bopal\b",r"\btopaz\b",r"\btourmaline\b",r"\bgarnet\b",
   r"\baquamarine\b",r"\bberyl\b",r"\bamethyst\b",
 ],
}

def norm(s): return s.fillna("").astype(str).str.lower()

def hit(series,pats):
    return series.str.contains("|".join(f"(?:{p})" for p in pats),regex=True,na=False)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("mrds_zip")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10P_MRDS_NONSTRATEGIC")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()

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
        df[c+"_N"]=norm(df[c])

    pts=gpd.GeoDataFrame(
        df,geometry=gpd.points_from_xy(df.longitude,df.latitude),crs=4326
    ).to_crs(board.crs)
    joined=gpd.sjoin(pts,land,predicate="within",how="inner")
    if len(joined)==0: raise RuntimeError("no MRDS points joined")

    out=land[["id"]].copy()
    audit=[]
    for group,pats in GROUPS.items():
        p=hit(joined.commod1_N,pats)
        s=hit(joined.commod2_N,pats)&~p
        t=hit(joined.commod3_N,pats)&~p&~s
        tmp=pd.DataFrame({
          "id":joined.id.astype("int64"),
          "P":p.astype("int16"),"S":s.astype("int16"),"T":t.astype("int16"),
        })
        agg=tmp.groupby("id",as_index=False)[["P","S","T"]].sum()
        agg=agg.rename(columns={
          "P":group+"_MRDS_PRIMARY_N",
          "S":group+"_MRDS_SECONDARY_N",
          "T":group+"_MRDS_TERTIARY_N",
        })
        agg[group+"_MRDS_SCORE"]=(
          3*agg[group+"_MRDS_PRIMARY_N"]+
          2*agg[group+"_MRDS_SECONDARY_N"]+
          agg[group+"_MRDS_TERTIARY_N"]
        ).astype("int32")
        agg[group+"_MRDS_ANY"]=(agg[group+"_MRDS_SCORE"]>0).astype("uint8")
        out=out.merge(agg,on="id",how="left",validate="one_to_one")
        cols=[
          group+"_MRDS_PRIMARY_N",group+"_MRDS_SECONDARY_N",group+"_MRDS_TERTIARY_N",
          group+"_MRDS_SCORE",group+"_MRDS_ANY",
        ]
        for c in cols:out[c]=out[c].fillna(0)
        audit.append({
          "group":group,
          "matched_records":int((p|s|t).sum()),
          "hexes_with_evidence":int(out[group+"_MRDS_ANY"].sum()),
          "score_sum":int(out[group+"_MRDS_SCORE"].sum()),
          "max_score":int(out[group+"_MRDS_SCORE"].max()),
        })

    evcols=[c for c in out.columns if c!="id"]
    overlap=[c for c in evcols if c in board.columns]
    if overlap:board=board.drop(columns=overlap)
    board=board.merge(out,on="id",how="left",validate="one_to_one")
    for c in evcols:board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10p_mrds_nonstrategic",driver="GPKG")
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)

    summary={
      "stage":"10P",
      "source":"USGS Mineral Resources Data System bulk CSV",
      "groups":audit,
      "gems_note":"word-boundary matcher; beryl does not match beryllium",
      "excluded_manual_resources":["AMBER","JADE","LAPIS_LAZULI"],
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
