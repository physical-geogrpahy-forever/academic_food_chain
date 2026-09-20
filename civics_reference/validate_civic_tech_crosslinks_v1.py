#!/usr/bin/env python3
import csv, pathlib, sys
P=pathlib.Path(__file__).resolve().parent/"civic_tech_crosslinks_v1.csv"
with P.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
err=[]
if len(rows)!=72: err.append(f"expected 72 rows, got {len(rows)}")
valid={"HARD","BOOST","NONE"}
for r in rows:
    rel=r["DIRECT_TECH_RELATION"]
    tech=r["DIRECT_TECH"].strip()
    if rel not in valid: err.append(f'{r["CIVIC_EN"]}: invalid relation {rel}')
    if rel in {"HARD","BOOST"} and not tech: err.append(f'{r["CIVIC_EN"]}: {rel} missing tech')
    if rel=="NONE" and tech: err.append(f'{r["CIVIC_EN"]}: NONE has direct tech {tech}')
if err:
    print("FAIL")
    for x in err: print("-",x)
    sys.exit(1)
from collections import Counter
c=Counter(r["DIRECT_TECH_RELATION"] for r in rows)
print("PASS",dict(c),"total",len(rows))
