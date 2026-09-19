#!/usr/bin/env python3
"""Select a global Marsh rule from GLWD subtype fractions without regional exceptions."""
import argparse, json
from pathlib import Path
import numpy as np, pandas as pd

CORE=[
 ("Everglades",-81.8,-79.8,24.2,26.8),
 ("West Siberian peatlands",60,90,55,67),
]
RIVER=[
 ("Pantanal",-60.8,-54,-22.5,-14.5),
 ("Okavango",20.5,24.8,-20.8,-17),
 ("Sudd",29,33.5,5,10.5),
]
DRY=[
 ("Sahara",-15,35,18,32),
 ("Arabia",35,58,16,30),
 ("Central Australia",125,140,-30,-20),
 ("Atacama",-72,-68,-28,-18),
]

def sel(df,b):
    _,x0,x1,y0,y1=b
    return (df.LON>=x0)&(df.LON<=x1)&(df.LAT>=y0)&(df.LAT<=y1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stats")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE3A4_MARSH")
    a=ap.parse_args()
    df=pd.read_csv(a.stats)
    need=["id","LON","LAT","RELIEF","TERRAIN","PALUSTRINE_OPEN_PCT","PEATLAND_OPEN_PCT","COASTAL_MARSH_PCT","LACUSTRINE_OPEN_PCT","RIVERINE_DELTA_PCT"]
    miss=[c for c in need if c not in df.columns]
    if miss: raise SystemExit("missing "+",".join(miss))
    if len(df)!=68048 or not df.id.is_unique: raise SystemExit("canonical LAND audit failed")
    df["MARSH_ECO_PCT"]=df[["PALUSTRINE_OPEN_PCT","PEATLAND_OPEN_PCT","COASTAL_MARSH_PCT"]].fillna(0).sum(axis=1)

    thresholds=[2,3,5,7.5,10,12.5,15,20,25,30,35,40]
    scan=[]; regional=[]
    for t in thresholds:
        cand=(df.MARSH_ECO_PCT>=t)&~df.RELIEF.eq("MOUNTAIN")&~df.TERRAIN.eq("SNOW")
        cscore=[]; dscore=[]
        for b in CORE:
            m=sel(df,b); n=int(m.sum()); sh=float((cand&m).sum()/n) if n else 0
            cscore.append(min(sh/0.10,1))
            regional.append({"threshold":t,"region":b[0],"kind":"marsh_reference","n":n,"candidate_share":sh,
                             "marsh_eco_mean":float(df.loc[m,"MARSH_ECO_PCT"].mean()) if n else None,
                             "lacustrine_mean":float(df.loc[m,"LACUSTRINE_OPEN_PCT"].mean()) if n else None,
                             "riverine_mean":float(df.loc[m,"RIVERINE_DELTA_PCT"].mean()) if n else None})
        for b in DRY:
            m=sel(df,b);n=int(m.sum());sh=float((cand&m).sum()/n) if n else 0
            dscore.append(max(0,1-sh/0.02))
            regional.append({"threshold":t,"region":b[0],"kind":"dry_reference","n":n,"candidate_share":sh,
                             "marsh_eco_mean":float(df.loc[m,"MARSH_ECO_PCT"].mean()) if n else None,
                             "lacustrine_mean":float(df.loc[m,"LACUSTRINE_OPEN_PCT"].mean()) if n else None,
                             "riverine_mean":float(df.loc[m,"RIVERINE_DELTA_PCT"].mean()) if n else None})
        share=float(cand.mean())
        # Civ-like feature should be selective globally, but ecological QA dominates.
        balance=1.0 if 0.005<=share<=0.05 else max(0,1-abs(share-0.025)/0.06)
        score=2.5*np.mean(cscore)+2.5*np.mean(dscore)+0.5*balance
        scan.append({"threshold":t,"marsh_hexes":int(cand.sum()),"share_land_pct":100*share,
                     "reference_score":float(np.mean(cscore)),"dry_score":float(np.mean(dscore)),
                     "balance_score":balance,"total_score":score})

    scan=pd.DataFrame(scan).sort_values(["total_score","threshold"],ascending=[False,True])
    best=float(scan.iloc[0].threshold)
    cand=(df.MARSH_ECO_PCT>=best)&~df.RELIEF.eq("MOUNTAIN")&~df.TERRAIN.eq("SNOW")
    df["MARSH"]=cand.astype("uint8")
    df["MARSH_SRC"]="GLWD_v2_exact_class_fractions"
    df["MARSH_THRESHOLD_PCT"]=best

    rr=[]
    for b in RIVER:
        m=sel(df,b);s=df.loc[m]
        rr.append({"region":b[0],"n":len(s),
                   "riverine_delta_mean":float(s.RIVERINE_DELTA_PCT.mean()),
                   "riverine_delta_max":float(s.RIVERINE_DELTA_PCT.max()),
                   "marsh_eco_mean":float(s.MARSH_ECO_PCT.mean()),
                   "marsh_share_at_selected":float(df.loc[m,"MARSH"].mean())})
    chosen=pd.DataFrame(regional)
    chosen=chosen[chosen.threshold.eq(best)]
    failures=[]
    for r in chosen.itertuples():
        if r.kind=="marsh_reference" and r.candidate_share<=0:
            failures.append(r.region+": no Marsh")
        if r.kind=="dry_reference" and r.candidate_share>0.03:
            failures.append(r.region+f": dry false-positive share {r.candidate_share:.3f}")
    for r in rr:
        if r["riverine_delta_max"]<=0: failures.append(r["region"]+": missing riverine signal")

    summary={
      "threshold_pct":best,
      "marsh_hexes":int(cand.sum()),
      "share_land_pct":float(cand.mean()*100),
      "qa_gate":"PASS" if not failures else "REVIEW",
      "qa_failures":failures,
      "rule":"PALUSTRINE_OPEN + PEATLAND_OPEN + COASTAL_MARSH >= threshold; exclude MOUNTAIN and SNOW",
      "excluded_from_marsh":["LACUSTRINE_OPEN","RIVERINE_DELTA","FOREST_WET","EPHEMERAL_SALINE"],
      "policy":"Lacustrine remains lake-associated wetland; riverine/delta reserved for Flood Plains; forested wetland remains a separate ecological flag. Dry-region QA uses interior desert boxes so genuine coastal marshes are not mislabeled as false positives."
    }
    df.to_csv(a.prefix+"_CLASSIFIED.csv",index=False)
    scan.to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    chosen.to_csv(a.prefix+"_REGIONAL_QA.csv",index=False)
    pd.DataFrame(rr).to_csv(a.prefix+"_RIVERINE_QA.csv",index=False)
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    Path(a.prefix+"_GATE.txt").write_text(summary["qa_gate"]+"\n"+("\n".join(failures) if failures else ""),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(scan.to_string(index=False))
    print(chosen.to_string(index=False))
    print(pd.DataFrame(rr).to_string(index=False))

if __name__=="__main__":main()
