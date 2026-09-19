#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from pyproj import Transformer

ROWS=335
HEX_W=57735.0269189626
HEX_H=50000.0
X_STEP=HEX_W*0.75
BASE_LEFT=-16920565.0448
BASE_TOP=8315130.3484

REGIONS=[
 ("Pantanal",-60.8,-54.0,-22.5,-14.5,"wet"),
 ("Okavango",20.5,24.8,-20.8,-17.0,"wet"),
 ("Sudd",29.0,33.5,5.0,10.5,"wet"),
 ("Everglades",-81.8,-79.8,24.2,26.8,"wet"),
 ("West Siberian wetlands",60.0,90.0,55.0,67.0,"wet"),
 ("Sahara",-15.0,35.0,18.0,32.0,"dry"),
 ("Arabia",35.0,58.0,16.0,30.0,"dry"),
 ("Central Australia",125.0,140.0,-30.0,-20.0,"dry"),
 ("Atacama",-72.0,-68.0,-28.0,-18.0,"dry"),
]

def add_lonlat(df):
    ids=df["id"].astype(np.int64).to_numpy()
    cols=(ids-1)//ROWS
    rows=(ids-1)%ROWS
    left=BASE_LEFT+cols*X_STEP
    top=BASE_TOP-rows*HEX_H-(cols%2)*(HEX_H/2)
    x=left+HEX_W/2
    y=top-HEX_H/2
    inv=Transformer.from_crs(8857,4326,always_xy=True)
    lon,lat=inv.transform(x,y)
    df=df.copy()
    df["LON"]=lon
    df["LAT"]=lat
    return df

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stats")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A_MARSH_QA")
    a=ap.parse_args()

    df=pd.read_csv(a.stats)
    need=["id","MARSH_LIKE_PCT","RELIEF","TERRAIN"]
    miss=[x for x in need if x not in df.columns]
    if miss: raise SystemExit("missing columns "+",".join(miss))
    if len(df)!=68048 or not df.id.is_unique:
        raise SystemExit(f"canonical LAND check failed n={len(df)} unique={df.id.is_unique}")
    df=add_lonlat(df)
    thresholds=[5,10,15,20,25,30,40,50]
    rows=[]
    details=[]
    for t in thresholds:
        cand=(df.MARSH_LIKE_PCT.fillna(0)>=t)&~df.RELIEF.eq("MOUNTAIN")
        # Marsh should not be assigned to snow; tundra wetlands remain possible.
        cand &= ~df.TERRAIN.eq("SNOW")
        wet_scores=[]; dry_scores=[]
        for name,x0,x1,y0,y1,kind in REGIONS:
            m=(df.LON>=x0)&(df.LON<=x1)&(df.LAT>=y0)&(df.LAT<=y1)
            n=int(m.sum()); nc=int((cand&m).sum())
            share=(nc/n) if n else np.nan
            mean=float(df.loc[m,"MARSH_LIKE_PCT"].mean()) if n else np.nan
            mx=float(df.loc[m,"MARSH_LIKE_PCT"].max()) if n else np.nan
            details.append(dict(threshold_pct=t,region=name,kind=kind,n=n,candidate_hexes=nc,candidate_share=share,marsh_like_mean=mean,marsh_like_max=mx))
            if kind=="wet" and n: wet_scores.append(min(share/0.12,1.0))
            if kind=="dry" and n: dry_scores.append(max(0.0,1.0-share/0.03))
        wet=np.mean(wet_scores) if wet_scores else 0
        dry=np.mean(dry_scores) if dry_scores else 0
        global_share=float(cand.mean())
        # Keep marsh as a selective feature: broad target 1–8% of land hexes.
        balance=1.0 if 0.01<=global_share<=0.08 else max(0.0,1-abs(global_share-0.04)/0.08)
        score=2.0*wet+1.5*dry+0.5*balance
        rows.append(dict(threshold_pct=t,marsh_hexes=int(cand.sum()),share_land_pct=100*global_share,wet_region_score=wet,dry_region_score=dry,balance_score=balance,total_score=score))

    scan=pd.DataFrame(rows).sort_values(["total_score","threshold_pct"],ascending=[False,True])
    detail=pd.DataFrame(details)
    best=int(scan.iloc[0].threshold_pct)
    cand=(df.MARSH_LIKE_PCT.fillna(0)>=best)&~df.RELIEF.eq("MOUNTAIN")&~df.TERRAIN.eq("SNOW")
    df["MARSH_GLWD"] = cand.astype("uint8")
    df["FEATURE_STAGE3A"]=np.where(cand,"MARSH",df.get("FEATURE_GAME",pd.Series(["NONE"]*len(df))).fillna("NONE"))

    scan.to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    detail.to_csv(a.prefix+"_REGIONAL_QA.csv",index=False)
    df.to_csv(a.prefix+"_CLASSIFIED.csv",index=False)

    # Gate: all named wet regions must have at least one candidate; dry regions <=10%.
    gate=[]
    d=detail[detail.threshold_pct.eq(best)]
    for r in d.itertuples():
        if r.kind=="wet" and r.candidate_hexes<1:
            gate.append(f"{r.region}: no marsh candidate")
        if r.kind=="dry" and r.candidate_share>0.10:
            gate.append(f"{r.region}: excessive marsh share {r.candidate_share:.3f}")
    summary={
      "best_threshold_pct":best,
      "marsh_hexes":int(cand.sum()),
      "share_land_pct":float(cand.mean()*100),
      "qa_gate":"PASS" if not gate else "REVIEW",
      "qa_failures":gate,
      "definition":"GLWD v2 marsh-like dominant-class wetland percentage >= threshold, excluding MOUNTAIN and SNOW",
      "note":"Riverine and delta classes remain excluded for the later Flood Plains stage."
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    Path(a.prefix+"_GATE.txt").write_text(summary["qa_gate"]+"\n"+("\n".join(gate) if gate else ""),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(scan.to_string(index=False))
    print(d.to_string(index=False))

if __name__=="__main__":
    main()
