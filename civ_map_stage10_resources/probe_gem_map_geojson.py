#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("geojson")
    ap.add_argument("--name",required=True)
    ap.add_argument("--prefix",required=True)
    a=ap.parse_args()
    obj=json.load(open(a.geojson,encoding="utf-8"))
    feats=obj.get("features",[])
    keys=sorted({k for f in feats for k in (f.get("properties") or {}).keys()})
    geom={}
    for f in feats:
        t=(f.get("geometry") or {}).get("type","NULL")
        geom[t]=geom.get(t,0)+1
    desired=[k for k in keys if any(x in k.lower() for x in ["prod","cap","reserve","resource","status","name","coal","oil","gas"])]
    samples=[]
    for f in feats[:10]:
        p=f.get("properties") or {}
        samples.append({k:p.get(k) for k in desired[:100]})
    out={"name":a.name,"feature_count":len(feats),"geometry_counts":geom,
         "property_keys":keys,"interesting_keys":desired,"samples":samples}
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False)[:50000])
if __name__=="__main__": main()
