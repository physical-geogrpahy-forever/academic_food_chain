#!/usr/bin/env python3
"""
Stage 4B Flood Plains candidates.

Minimum conditions from the project handoff are enforced directly:
  - river adjacency (Stage 4A edge flags)
  - FLAT relief
  - dedicated floodplain/wetland evidence (GLWD v2 RIVERINE_DELTA_PCT)

This stage writes a separate FLOOD_PLAINS flag. It does not yet overwrite
FOREST/JUNGLE/MARSH feature precedence.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd

POS=[
 ("Lower Nile",29.0,32.8,22.0,31.5),
 ("Mesopotamia",43.0,48.8,29.0,34.8),
 ("Ganges-Brahmaputra",87.0,92.5,21.0,27.5),
 ("Lower Mississippi",-92.5,-88.0,28.5,34.0),
 ("Mekong Delta",104.0,107.0,8.0,12.5),
 ("Lower Indus",67.0,70.8,23.0,30.5),
 ("Pantanal",-60.8,-54.0,-22.5,-14.5),
 ("Sudd",29.0,33.5,5.0,10.5),
]
NEG=[
 ("Sahara west",-15.0,20.0,20.0,32.0),
 ("Central Australia",125.0,140.0,-30.0,-20.0),
 ("Atacama",-72.0,-68.0,-28.0,-18.0),
]
ALLOWED_TERRAIN={"GRASSLAND","PLAINS","DESERT"}

def box(df,b):
    _,x0,x1,y0,y1=b
    return (df.LON>=x0)&(df.LON<=x1)&(df.LAT>=y0)&(df.LAT<=y1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage4a_gpkg")
    ap.add_argument("glwd_subtype_csv")
    ap.add_argument("--layer",default="game_map_stage4a_rivers")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE4B_FLOODPLAINS")
    a=ap.parse_args()

    board=gpd.read_file(a.stage4a_gpkg,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("Stage4A canonical board audit failed")
    wet=pd.read_csv(a.glwd_subtype_csv)
    if len(wet)!=68048 or not wet.id.is_unique:
        raise RuntimeError("GLWD canonical LAND audit failed")
    cols=["id","RIVERINE_DELTA_PCT","PALUSTRINE_OPEN_PCT","PEATLAND_OPEN_PCT","COASTAL_MARSH_PCT"]
    land=board.loc[board.SURFACE.eq("LAND"),["id","LON","LAT","RELIEF","TERRAIN","RIVER_ANY"]].merge(
        wet[cols],on="id",how="left",validate="one_to_one")
    if len(land)!=68048:raise RuntimeError(len(land))

    thresholds=[1,2,3,5,7.5,10,12.5,15,20,25,30,40]
    rows=[]; reg=[]
    for t in thresholds:
        cand=(land.RIVER_ANY.eq(1)&land.RELIEF.eq("FLAT")&
              land.TERRAIN.isin(ALLOWED_TERRAIN)&
              (land.RIVERINE_DELTA_PCT.fillna(0)>=t))
        pos=[];neg=[]
        for b in POS:
            m=box(land,b);n=int(m.sum());nc=int((cand&m).sum());sh=nc/n if n else 0
            pos.append(1.0 if nc>0 else 0.0)
            reg.append({"threshold":t,"region":b[0],"kind":"positive","n":n,"candidate_hexes":nc,"candidate_share":sh,
                        "river_cells":int((land.RIVER_ANY.eq(1)&m).sum()),
                        "riverine_mean":float(land.loc[m,"RIVERINE_DELTA_PCT"].mean()) if n else None})
        for b in NEG:
            m=box(land,b);n=int(m.sum());nc=int((cand&m).sum());sh=nc/n if n else 0
            neg.append(max(0,1-sh/0.02))
            reg.append({"threshold":t,"region":b[0],"kind":"negative","n":n,"candidate_hexes":nc,"candidate_share":sh,
                        "river_cells":int((land.RIVER_ANY.eq(1)&m).sum()),
                        "riverine_mean":float(land.loc[m,"RIVERINE_DELTA_PCT"].mean()) if n else None})
        share=float(cand.mean())
        balance=1.0 if 0.002<=share<=0.04 else max(0,1-abs(share-0.02)/0.05)
        score=3*np.mean(pos)+2*np.mean(neg)+0.5*balance
        rows.append({"threshold":t,"floodplain_hexes":int(cand.sum()),"share_land_pct":100*share,
                     "positive_region_score":float(np.mean(pos)),"negative_region_score":float(np.mean(neg)),
                     "balance_score":balance,"total_score":score})

    scan=pd.DataFrame(rows).sort_values(["total_score","threshold"],ascending=[False,True])
    best=float(scan.iloc[0].threshold)
    cand=(land.RIVER_ANY.eq(1)&land.RELIEF.eq("FLAT")&
          land.TERRAIN.isin(ALLOWED_TERRAIN)&
          (land.RIVERINE_DELTA_PCT.fillna(0)>=best))
    land["FLOOD_PLAINS"]=cand.astype("uint8")
    land["FP_THRESHOLD_PCT"]=best

    chosen=pd.DataFrame(reg)
    chosen=chosen[chosen.threshold.eq(best)].copy()
    failures=[]
    for r in chosen.itertuples():
        if r.kind=="positive" and r.river_cells>0 and r.candidate_hexes<1:
            failures.append(r.region+": river present but no floodplain candidate")
        if r.kind=="negative" and r.candidate_share>0.03:
            failures.append(r.region+f": negative-region share {r.candidate_share:.3f}")

    board=board.merge(land[["id","RIVERINE_DELTA_PCT","FLOOD_PLAINS","FP_THRESHOLD_PCT"]],on="id",how="left",validate="one_to_one")
    board["FLOOD_PLAINS"]=board["FLOOD_PLAINS"].fillna(0).astype("uint8")
    bad_surface=int(board.loc[~board.SURFACE.eq("LAND"),"FLOOD_PLAINS"].sum())
    bad_relief=int(board.loc[board.FLOOD_PLAINS.eq(1)&~board.RELIEF.eq("FLAT")].shape[0])
    no_river=int(board.loc[board.FLOOD_PLAINS.eq(1)&~board.RIVER_ANY.eq(1)].shape[0])
    if bad_surface:failures.append(f"non-LAND floodplains {bad_surface}")
    if bad_relief:failures.append(f"non-FLAT floodplains {bad_relief}")
    if no_river:failures.append(f"floodplains without river {no_river}")

    summary={
      "stage":"4B",
      "threshold_pct":best,
      "floodplain_hexes":int(board.FLOOD_PLAINS.sum()),
      "share_land_pct":float(board.FLOOD_PLAINS.sum()/68048*100),
      "qa_gate":"PASS" if not failures else "REVIEW",
      "qa_failures":failures,
      "rule":"LAND + RIVER_ANY + FLAT + terrain in GRASSLAND/PLAINS/DESERT + GLWD RIVERINE_DELTA_PCT threshold",
      "feature_precedence":"not resolved here; FLOOD_PLAINS is a separate flag",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    scan.to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    chosen.to_csv(a.prefix+"_REGIONAL_QA.csv",index=False)
    land.to_csv(a.prefix+"_LAND.csv",index=False)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage4b_floodplains",driver="GPKG")
    print(json.dumps(summary,indent=2))
    print(scan.to_string(index=False))
    print(chosen.to_string(index=False))

if __name__=="__main__":main()
