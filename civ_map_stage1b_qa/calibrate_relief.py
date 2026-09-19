#!/usr/bin/env python3
"""
Calibrate FLAT/HILL/MOUNTAIN from native-resolution Stage 1B per-hex DEM statistics.

Important:
- No Stage 1A 1-degree relief is read or reused.
- Classification is driven primarily by within-hex relief and slope.
- Absolute elevation is reported for QA but is not sufficient by itself to make MOUNTAIN.
- Thresholds are selected by regional QA + global class-balance constraints.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from pyproj import Transformer

ROWS=335; COLS=781
HEX_W=57735.0269189626; HEX_H=50000.0; X_STEP=HEX_W*0.75
BASE_LEFT=-16920565.0448; BASE_TOP=8315130.3484

# Regional QA boxes: lon_min, lon_max, lat_min, lat_max.
# Expectations are intentionally broad because 50-km game hexes contain mixed terrain.
REGIONS = [
    ("Himalaya",                 75,  95,  26,  35, "MOUNTAIN"),
    ("Tibetan margins",          78, 102,  27,  36, "MOUNTAIN"),
    ("Central Andes",           -75, -66, -35, -10, "MOUNTAIN"),
    ("Rockies",                -120,-105,  30,  55, "MOUNTAIN"),
    ("Alps",                      5,  16,  43,  49, "MOUNTAIN"),
    ("Caucasus",                 38,  50,  39,  45, "MOUNTAIN"),
    ("Ethiopian Highlands",      35,  41,   5,  14, "MOUNTAIN"),
    ("Japanese mountains",      135, 141,  33,  40, "MOUNTAIN"),
    ("Korean mountains",        128, 129.5,  37, 38.6, "MOUNTAIN"),
    # Appalachian ridge core; the wider -84..-77 / 33..42 box includes large
    # Piedmont/valley/lowland areas and is inappropriate for a HILL-only QA gate.
    ("Appalachians",          -82.5, -78,  35, 40.5, "HILL"),
    ("Korean Peninsula",        126, 130,  34,  40, "HILL"),
    ("Eastern Australia",       145, 153, -39, -27, "HILL"),
    ("East African plateau",     29,  40, -10,  10, "HILL"),
    ("Amazon lowland",          -70, -50, -10,   2, "FLAT"),
    ("Congo basin",              15,  30,  -6,   5, "FLAT"),
    ("Great Plains",           -105, -95,  30,  50, "FLAT"),
    ("West Siberian Plain",      60,  90,  50,  65, "FLAT"),
    ("Sahara flat sector",      -10,  30,  20,  30, "FLAT"),
    ("Central Australia",       125, 140, -30, -20, "FLAT"),
    ("Greenland interior",      -50, -30,  70,  80, "POLAR_NOT_ALL_MOUNTAIN"),
    ("Antarctica interior",       0,  90, -85, -75, "POLAR_NOT_ALL_MOUNTAIN"),
    # Explicit anti-wall checks motivated by the old 1-degree failure: Peru and
    # Chile must retain substantial non-mountain hexes for playable settlement.
    ("Peru broad",               -81, -68, -18,  -4, "NOT_ALL_MOUNTAIN"),
    ("Peru coastal belt",        -81, -75, -18,  -4, "NOT_ALL_MOUNTAIN"),
    ("Chile broad",              -75, -66, -55, -17, "NOT_ALL_MOUNTAIN"),
    ("Central Chile",          -73.5, -70, -38, -30, "NOT_ALL_MOUNTAIN"),
]

def add_lonlat(df):
    ids=df["id"].astype(np.int64).to_numpy()
    cols=(ids-1)//ROWS
    rows=(ids-1)%ROWS
    left=BASE_LEFT+cols*X_STEP
    top=BASE_TOP-rows*HEX_H-(cols%2)*(HEX_H/2.0)
    x=left+HEX_W/2.0
    y=top-HEX_H/2.0
    inv=Transformer.from_crs(8857,4326,always_xy=True)
    lon,lat=inv.transform(x,y)
    df=df.copy()
    df["lon"]=np.asarray(lon)
    df["lat"]=np.asarray(lat)
    return df

def in_box(df,box):
    _,lo0,lo1,la0,la1,_=box
    return (df.lon>=lo0)&(df.lon<=lo1)&(df.lat>=la0)&(df.lat<=la1)

def classify(df,q_r_main,q_p75_main,q_med_main,q_ext):
    # GAME-MAP mountain core: large within-hex relief plus broadly steep terrain.
    # This deliberately avoids calling a tile MOUNTAIN merely because its steepest
    # 10% is extreme. Mixed lowland+mountain hexes therefore tend to become HILL.
    r=df["RELIEF_P90P10"].fillna(0).to_numpy(float)
    p90=df["SLOPE_P90"].fillna(0).to_numpy(float)
    p75=df["SLOPE_P75"].fillna(0).to_numpy(float)
    med=df["SLOPE_MED"].fillna(0).to_numpy(float)
    valid=np.isfinite(r)&np.isfinite(p90)&np.isfinite(p75)&np.isfinite(med)
    rv=r[valid]; p90v=p90[valid]; p75v=p75[valid]; medv=med[valid]

    Qr=lambda q: float(np.quantile(rv,q))
    Q90=lambda q: float(np.quantile(p90v,q))
    Q75=lambda q: float(np.quantile(p75v,q))
    Qm=lambda q: float(np.quantile(medv,q))

    # Main mountain core requires the majority of the tile to be rugged.
    m_main=(r>=Qr(q_r_main)) & (p75>=Q75(q_p75_main)) & (med>=Qm(q_med_main))

    # Extremely rugged tiles can still qualify with slightly lower median-slope
    # support. This preserves sharp alpine/island ranges without recreating
    # continuous walls from a single extreme flank.
    support=max(0.55, q_med_main-0.15)
    m_ext_relief=(r>=Qr(q_ext)) & (p75>=Q75(max(0.65,q_p75_main-0.10))) & (med>=Qm(support))
    m_ext_steep=(p75>=Q75(q_ext)) & (r>=Qr(max(0.65,q_r_main-0.10))) & (med>=Qm(support))
    m=m_main | m_ext_relief | m_ext_steep

    # HILL remains broad. Mountain candidates are cut from this set afterwards.
    h=((r>=Qr(0.50))&(p90>=Q90(0.50))) | (r>=Qr(0.78)) | (p90>=Q90(0.78)) | (med>=Qm(0.65))
    h &= ~m

    cls=np.full(len(df),"FLAT",dtype=object)
    cls[h]="HILL"; cls[m]="MOUNTAIN"
    thresholds={
      "q_r_main":q_r_main,"q_p75_main":q_p75_main,"q_med_main":q_med_main,"q_ext":q_ext,
      "relief_main":Qr(q_r_main),"slope_p75_main":Q75(q_p75_main),"slope_med_main":Qm(q_med_main),
      "relief_extreme":Qr(q_ext),"slope_p75_extreme":Q75(q_ext),
      "hill_relief_mid":Qr(0.50),"hill_slope_p90_mid":Q90(0.50),
    }
    return cls,thresholds

def region_metrics(df,cls):
    out=[]
    for reg in REGIONS:
        mask=in_box(df,reg)
        n=int(mask.sum())
        if n==0:
            out.append(dict(region=reg[0],expectation=reg[-1],n=0,flat=np.nan,hill=np.nan,mountain=np.nan))
            continue
        c=cls[mask]
        out.append(dict(
            region=reg[0], expectation=reg[-1], n=n,
            flat=float(np.mean(c=="FLAT")),
            hill=float(np.mean(c=="HILL")),
            mountain=float(np.mean(c=="MOUNTAIN")),
            elev_mean=float(df.loc[mask,"ELEV_MEAN"].mean()),
            relief_mean=float(df.loc[mask,"RELIEF_P90P10"].mean()),
            slope_p90_mean=float(df.loc[mask,"SLOPE_P90"].mean()),
        ))
    return pd.DataFrame(out)

def score_candidate(rm,global_shares):
    # Higher is better. QA combines physical recognizability and game playability.
    score=0.0
    for row in rm.itertuples():
        if row.n==0:
            score-=5; continue
        if row.expectation=="MOUNTAIN":
            target=0.18 if row.region=="Korean mountains" else 0.25
            score += min(row.mountain/target,1.0)*2.0
            score += min((row.mountain+row.hill)/0.72,1.0)*1.5
            score -= max(row.flat-0.35,0)*5.0
        elif row.expectation=="HILL":
            score += min((row.hill+row.mountain)/0.55,1.0)*1.5
            score += min(row.hill/0.38,1.0)
            score -= max(row.mountain-0.35,0)*3.0
        elif row.expectation=="FLAT":
            score += min(row.flat/0.68,1.0)*1.5
            score -= max(row.mountain-0.10,0)*6.0
        elif row.expectation=="POLAR_NOT_ALL_MOUNTAIN":
            score += min((1-row.mountain)/0.80,1.0)
            score -= max(row.mountain-0.25,0)*8.0
        else:  # NOT_ALL_MOUNTAIN
            # Explicitly penalize the old Andes wall. The classification rule is
            # global; Peru/Chile are only QA regions, not geographic exceptions.
            cap=0.50 if row.region in ("Peru coastal belt","Central Chile") else 0.42
            score += min((1-row.mountain)/(1-cap),1.0)*1.5
            score -= max(row.mountain-cap,0)*12.0

    f,h,m=global_shares
    # A Civilization-style board needs mountains to be selective obstacles,
    # with most rugged-but-traversable terrain represented as HILL.
    if not (0.055 <= m <= 0.14): score -= abs(m-0.09)*35
    if not (0.25 <= h <= 0.45): score -= abs(h-0.35)*20
    if not (0.40 <= f <= 0.65): score -= abs(f-0.52)*18
    return score

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stats_csv")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE1B_RELIEF")
    a=ap.parse_args()
    df=pd.read_csv(a.stats_csv)
    need=["id","ELEV_MEAN","ELEV_MAX","RELIEF_P90P10","SLOPE_MEAN","SLOPE_MED","SLOPE_P75","SLOPE_P90"]
    miss=[c for c in need if c not in df.columns]
    if miss: raise SystemExit("Missing columns: "+",".join(miss))
    df=add_lonlat(df)

    candidates=[]
    best=None
    for q_r_main in [0.78,0.81,0.84,0.87,0.90]:
      for q_p75_main in [0.72,0.76,0.80,0.84,0.88]:
        for q_med_main in [0.60,0.65,0.70,0.75,0.80]:
          for q_ext in [0.93,0.95,0.97]:
            if q_ext<=q_r_main or q_ext<=q_p75_main: continue
            cls,thr=classify(df,q_r_main,q_p75_main,q_med_main,q_ext)
            f=float(np.mean(cls=="FLAT")); h=float(np.mean(cls=="HILL")); m=float(np.mean(cls=="MOUNTAIN"))
            rm=region_metrics(df,cls)
            sc=score_candidate(rm,(f,h,m))
            rec=dict(score=sc,flat=f,hill=h,mountain=m,**thr)
            candidates.append(rec)
            if best is None or sc>best[0]:
                best=(sc,rec,cls,rm)

    cand=pd.DataFrame(candidates).sort_values("score",ascending=False)
    cand.to_csv(a.prefix+"_THRESHOLD_SEARCH.csv",index=False)
    sc,rec,cls,rm=best
    df["RELIEF"]=cls
    df.to_csv(a.prefix+"_CLASSIFIED.csv",index=False)
    rm.to_csv(a.prefix+"_QA.csv",index=False)

    summary={
      "source_stats":str(a.stats_csv),
      "land_hexes":int(len(df)),
      "best":{k:(float(v) if isinstance(v,(np.floating,float)) else v) for k,v in rec.items()},
      "counts":{k:int(np.sum(cls==k)) for k in ["FLAT","HILL","MOUNTAIN"]},
      "rules":{
        "MOUNTAIN":"global mountain-core rule using RELIEF_P90P10 + SLOPE_P75 + SLOPE_MED; extreme branches still require median-slope support",
        "HILL":"broad rugged-terrain rule using relief and slope; excludes MOUNTAIN",
        "absolute_elevation":"QA/reporting only; never sufficient by itself",
        "playability":"Peru/Chile are QA constraints only; there are no country-specific classification overrides"
      }
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")

    # Simple regional QA gate
    failures=[]
    for row in rm.itertuples():
      if row.expectation=="MOUNTAIN" and not (row.mountain>=0.18 and row.flat<=0.45): failures.append(row.region)
      if row.expectation=="HILL" and not ((row.hill+row.mountain)>=0.45 and row.mountain<=0.40): failures.append(row.region)
      if row.expectation=="FLAT" and not (row.flat>=0.55 and row.mountain<=0.15): failures.append(row.region)
      if row.expectation=="POLAR_NOT_ALL_MOUNTAIN" and not (row.mountain<=0.40): failures.append(row.region)
      if row.expectation=="NOT_ALL_MOUNTAIN" and not (row.mountain<=0.65): failures.append(row.region)
    Path(a.prefix+"_QA_GATE.txt").write_text(
        ("PASS\n" if not failures else "REVIEW\n") + "\n".join(failures) + "\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(rm.to_string(index=False))
    print("QA failures:", failures)

if __name__=="__main__":
    main()
