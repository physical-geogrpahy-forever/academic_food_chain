#!/usr/bin/env python3
import csv,pathlib,sys
from collections import defaultdict,deque
P=pathlib.Path(__file__).resolve().parent/"technology_tree_historical_v2.csv"
with P.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
nodes={r["TECH"]:r for r in rows}
succ=defaultdict(list);indeg={n:0 for n in nodes};errors=[]
for n,r in nodes.items():
    ps=[x.strip() for x in r["PREREQUISITES_AND"].split(";") if x.strip()]
    if len(ps)>2:
        errors.append(f"{n}: >2 prerequisites")
    for p in ps:
        if p not in nodes:
            errors.append(f"{n}: missing {p}")
            continue
        if int(nodes[p]["ERA_INDEX"])>int(r["ERA_INDEX"]):
            errors.append(f"{p}->{n}: backward era")
        succ[p].append(n);indeg[n]+=1
roots=[n for n,d in indeg.items() if d==0]
d=dict(indeg);q=deque(roots);top=[]
while q:
    x=q.popleft();top.append(x)
    for y in succ[x]:
        d[y]-=1
        if d[y]==0:q.append(y)
if len(top)!=len(nodes):
    errors.append("cycle")
reach=set();q=deque(roots)
while q:
    x=q.popleft()
    if x in reach: continue
    reach.add(x);q.extend(succ[x])
if len(reach)!=len(nodes):
    errors.append("unreachable="+",".join(sorted(set(nodes)-reach)))
if errors:
    print("FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("PASS")
print("nodes",len(nodes))
print("roots",", ".join(roots))
print("reachable",len(reach))
