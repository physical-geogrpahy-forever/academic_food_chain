#!/usr/bin/env python3
"""
Stage 10M: aggregate IAEA UThDEPO uranium-deposit evidence to canonical LAND hexes.

UThDEPO resourceRange is categorical (for example >=5000 - <10000 tU), not a
precise deposit reserve. We convert each category to a representative value only
for within-uranium ranking:
  bounded range -> geometric midpoint
  <X            -> 0.5*X
  >=X           -> 1.5*X

The representative value is a ranking proxy, not a claim of exact reserves.
"""
from __future__ import annotations
import argparse,json,re,math
from pathlib import Path
import pandas as pd
import geopandas as gpd

def resource_proxy(text):
    s=str(text or "").strip().replace(",","")
    if not s:
        return 0.0
    nums=[float(x) for x in re.findall(r"\d+(?:\.\d+)?",s)]
    if len(nums)>=2:
        lo,hi=nums[0],nums[1]
        if lo>0 and hi>0:
            return math.sqrt(lo*hi)
        return (lo+hi)/2
    if len(nums)==1:
        x=nums[0]
        if x<=0:
            return 0.0
        if ("≥" in s) or (">=" in s) or (">" in s and "<" not in s):
            return 1.5*x
        if ("<" in s) or ("≤" in s):
            return 0.5*x
        return x
    return 0.0

def is_uranium(d):
    cid=d.get("commodityId")
    typ=str(d.get("type") or "").strip().upper()
    # Public-map payload currently uses commodityId 1 for uranium; the type
    # prefix is retained as an additional transparent guard.
    return cid==1 or typ.startswith("U-")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("uthdepo_json")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10M_UTHDEPO_EVIDENCE")
    a=ap.parse_args()

    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board.loc[board.SURFACE.eq("LAND"),["id","geometry"]].copy()

    obj=json.loads(Path(a.uthdepo_json).read_text(encoding="utf-8"))
    deps=obj.get("depositMapDtos",[])
    rows=[]
    for d in deps:
        if not is_uranium(d):
            continue
        try:
            lat=float(d.get("latitude"))
            lon=float(d.get("longitude"))
        except Exception:
            continue
        if not (-90<=lat<=90 and -180<=lon<=180):
            continue
        rr=str(d.get("resourceRange") or "").strip()
        rows.append({
            "UTH_ID":d.get("id"),
            "UTH_NAME":d.get("name"),
            "COUNTRY":d.get("country"),
            "COMMODITY_ID":d.get("commodityId"),
            "DEPOSIT_TYPE":d.get("type"),
            "RESOURCE_RANGE":rr,
            "RESOURCE_PROXY_TU":resource_proxy(rr),
            "GRADE_RANGE":d.get("gradeRange"),
            "lat":lat,"lon":lon,
        })
    src=pd.DataFrame(rows)
    if len(src)==0:
        raise RuntimeError("no uranium records parsed from UThDEPO payload")
    srcg=gpd.GeoDataFrame(
        src,geometry=gpd.points_from_xy(src.lon,src.lat),crs=4326
    ).to_crs(board.crs)

    joined=gpd.sjoin(srcg,land,predicate="within",how="inner")
    if len(joined)==0:
        raise RuntimeError("no UThDEPO uranium deposits joined to LAND hexes")

    agg=joined.groupby("id",as_index=False).agg(
        URANIUM_UTHDEPO_DEPOSITS=("UTH_ID","nunique"),
        URANIUM_UTHDEPO_RESOURCE_TU=("RESOURCE_PROXY_TU","sum"),
        URANIUM_UTHDEPO_RESOURCE_MAX_TU=("RESOURCE_PROXY_TU","max"),
        URANIUM_UTHDEPO_WITH_RESOURCE_N=("RESOURCE_PROXY_TU",lambda x:int((x>0).sum())),
    )
    agg["URANIUM_UTHDEPO_ANY"]=1

    overlap=[c for c in agg.columns if c!="id" and c in board.columns]
    if overlap:
        board=board.drop(columns=overlap)
    board=board.merge(agg,on="id",how="left",validate="one_to_one")
    evcols=[c for c in agg.columns if c!="id"]
    for c in evcols:
        board[c]=pd.to_numeric(board[c],errors="coerce").fillna(0)

    board.to_file(a.prefix+".gpkg",layer="game_map_stage10m_uthdepo_evidence",driver="GPKG")
    board.loc[board.URANIUM_UTHDEPO_ANY.gt(0),
              ["id","SURFACE"]+evcols].to_csv(a.prefix+"_EVIDENCE.csv",index=False)

    rr=src.RESOURCE_RANGE.value_counts(dropna=False).to_dict()
    summary={
        "stage":"10M UThDEPO uranium evidence",
        "source":"IAEA UThDEPO public map payload",
        "map_payload_deposits_all_commodities":int(len(deps)),
        "uranium_records_with_valid_coordinates":int(len(src)),
        "uranium_records_joined_to_land":int(len(joined)),
        "uranium_evidence_hexes":int(len(agg)),
        "records_with_resource_range":int((src.RESOURCE_PROXY_TU>0).sum()),
        "resource_range_counts":{str(k):int(v) for k,v in rr.items()},
        "resource_proxy_policy":"bounded range geometric midpoint; <X -> 0.5X; >=X -> 1.5X; used only for within-uranium ranking",
        "locations_note":"UThDEPO map locations are approximate; preserve this limitation in final metadata.",
        "final_placement":False,
        "gameplay_thinning_applied":False,
        "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
