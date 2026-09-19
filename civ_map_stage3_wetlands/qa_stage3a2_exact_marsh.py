#!/usr/bin/env python3
"""QA and threshold selection for Stage 3A2 exact GLWD class-fraction metrics."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

CORE_REGIONS=[
 ("Everglades",-81.8,-79.8,24.2,26.8),
 ("West Siberian peatlands",60.0,90.0,55.0,67.0),
]
RIVERINE_REGIONS=[
 ("Pantanal",-60.8,-54.0,-22.5,-14.5),
 ("Okavango",20.5,24.8,-20.8,-17.0),
 ("Sudd",29.0,33.5,5.0,10.5),
]
DRY_REGIONS=[
 ("Sahara",-15.0,35.0,18.0,32.0),
 ("Arabia",35.0,58.0,16.0,30.0),
 ("Central Australia",125.0,140.0,-30.0,-20.0),
 ("Atacama",-72.0,-68.0,-28.0,-18.0),
]

def box(df,b):
    _,x0,x1,y0,y1=b
    return (df.LON>=x0)&(df.LON<=x1)&(df.LAT>=y0)&(df.LAT<=y1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stats")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A2_MARSH_QA")
    a=ap.parse_args()
    df=pd.read_csv(a.stats)
    need=["id","LON","LAT","RELIEF","TERRAIN","CORE_MARSH_PCT","RIVERINE_WET_PCT","FOREST_WET_PCT","EPHEMERAL_SALINE_PCT"]
    miss=[c for c in need if c not in df.columns]
    if miss: raise SystemExit("missing "+",".join(miss))
    if len(df)!=68048 or not df.id.is_unique:
        raise SystemExit("canonical LAND audit failed")

    thresholds=[1,2,3,5,7.5,10,12.5,15,20,25,30,40]
    rows=[]; regrows=[]
    for t in thresholds:
        cand=(df.CORE_MARSH_PCT.fillna(0)>=t)&~df.RELIEF.eq("MOUNTAIN")&~df.TERRAIN.eq("SNOW")
        core_scores=[]; dry_scores=[]
        for b in CORE_REGIONS:
            m=box(df,b); n=int(m.sum()); nc=int((cand&m).sum())
            sh=nc/n if n else np.nan
            core_scores.append(min(sh/0.12,1.0) if n else 0)
            regrows.append(dict(threshold=t,region=b[0],kind="core_marsh",n=n,candidates=nc,candidate_share=sh,
                                core_mean=float(df.loc[m,"CORE_MARSH_PCT"].mean()) if n else np.nan,
                                riverine_mean=float(df.loc[m,"RIVERINE_WET_PCT"].mean()) if n else np.nan,
                                forest_mean=float(df.loc[m,"FOREST_WET_PCT"].mean()) if n else np.nan,
                                ephemeral_saline_mean=float(df.loc[m,"EPHEMERAL_SALINE_PCT"].mean()) if n else np.nan))
        for b in DRY_REGIONS:
            m=box(df,b); n=int(m.sum()); nc=int((cand&m).sum())
            sh=nc/n if n else np.nan
            dry_scores.append(max(0,1-sh/0.03) if n else 0)
            regrows.append(dict(threshold=t,region=b[0],kind="dry",n=n,candidates=nc,candidate_share=sh,
                                core_mean=float(df.loc[m,"CORE_MARSH_PCT"].mean()) if n else np.nan,
                                riverine_mean=float(df.loc[m,"RIVERINE_WET_PCT"].mean()) if n else np.nan,
                                forest_mean=float(df.loc[m,"FOREST_WET_PCT"].mean()) if n else np.nan,
                                ephemeral_saline_mean=float(df.loc[m,"EPHEMERAL_SALINE_PCT"].mean()) if n else np.nan))
        share=float(cand.mean())
        # Selective game feature; score is only for threshold choice, not a scientific claim.
        balance=1.0 if 0.005<=share<=0.06 else max(0,1-abs(share-0.03)/0.08)
        score=2*np.mean(core_scores)+2*np.mean(dry_scores)+0.5*balance
        rows.append(dict(threshold=t,marsh_candidates=int(cand.sum()),share_land_pct=share*100,
                         core_region_score=float(np.mean(core_scores)),dry_region_score=float(np.mean(dry_scores)),
                         balance_score=balance,total_score=score))

    scan=pd.DataFrame(rows).sort_values(["total_score","threshold"],ascending=[False,True])
    best=float(scan.iloc[0].threshold)
    cand=(df.CORE_MARSH_PCT.fillna(0)>=best)&~df.RELIEF.eq("MOUNTAIN")&~df.TERRAIN.eq("SNOW")
    df["MARSH_CORE_CAND"]=cand.astype("uint8")

    # Riverine QA is diagnostic for the later Flood Plains stage.
    river=[]
    for b in RIVERINE_REGIONS:
        m=box(df,b); s=df.loc[m]
        river.append(dict(region=b[0],n=int(m.sum()),
                          riverine_mean=float(s.RIVERINE_WET_PCT.mean()),
                          riverine_max=float(s.RIVERINE_WET_PCT.max()),
                          core_marsh_mean=float(s.CORE_MARSH_PCT.mean()),
                          forest_wet_mean=float(s.FOREST_WET_PCT.mean())))

    d=pd.DataFrame(regrows)
    chosen=d[d.threshold.eq(best)]
    failures=[]
    for r in chosen.itertuples():
        if r.kind=="core_marsh" and r.candidates<1: failures.append(r.region+": no core-marsh candidate")
        if r.kind=="dry" and r.candidate_share>0.05: failures.append(r.region+f": dry false-positive share {r.candidate_share:.3f}")
    for r in river:
        if r["riverine_max"]<=0: failures.append(r["region"]+": no riverine GLWD signal")

    summary={"best_threshold_pct":best,"marsh_candidates":int(cand.sum()),"share_land_pct":float(cand.mean()*100),
             "qa_gate":"PASS" if not failures else "REVIEW","qa_failures":failures,
             "definition":"CORE_MARSH_PCT threshold; MOUNTAIN and SNOW excluded",
             "riverine_policy":"RIVERINE_WET_PCT is preserved for later river + Flood Plains logic, not silently converted to Marsh",
             "forested_policy":"FOREST_WET_PCT remains separate from Marsh"}
    scan.to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    chosen.to_csv(a.prefix+"_REGIONAL_QA.csv",index=False)
    pd.DataFrame(river).to_csv(a.prefix+"_RIVERINE_QA.csv",index=False)
    df.to_csv(a.prefix+"_CLASSIFIED.csv",index=False)
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    Path(a.prefix+"_GATE.txt").write_text(summary["qa_gate"]+"\n"+("\n".join(failures) if failures else ""),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(scan.to_string(index=False))
    print(chosen.to_string(index=False))
    print(pd.DataFrame(river).to_string(index=False))

if __name__=="__main__":
    main()
