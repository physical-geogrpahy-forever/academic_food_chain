#!/usr/bin/env python3
import csv, pathlib, sys
from collections import defaultdict, deque
HERE=pathlib.Path(__file__).resolve().parent
CSV=HERE/"civic_tree_historical_v2.csv"
with CSV.open(encoding="utf-8-sig",newline="") as f:
    data=list(csv.DictReader(f))
nodes={r["CIVIC_EN"]:r for r in data}
succ=defaultdict(list); indeg={n:0 for n in nodes}; errors=[]
for n,r in nodes.items():
    ps=[x.strip() for x in r["SOCIAL_PREREQUISITES_AND"].split(";") if x.strip()]
    if len(ps)>2: errors.append(f"{n}: >2 prerequisites")
    for p in ps:
        if p not in nodes: errors.append(f"{n}: missing {p}"); continue
        if int(nodes[p]["ERA_INDEX"])>int(r["ERA_INDEX"]): errors.append(f"{p}->{n}: backward era")
        succ[p].append(n); indeg[n]+=1
roots=[n for n,d in indeg.items() if d==0]
if roots!=["Code of Laws"]: errors.append(f"roots={roots}")
deg=dict(indeg); q=deque(roots); topo=[]
while q:
    x=q.popleft(); topo.append(x)
    for y in succ[x]:
        deg[y]-=1
        if deg[y]==0:q.append(y)
if len(topo)!=len(nodes): errors.append("cycle detected")
reach=set(); q=deque(["Code of Laws"])
while q:
    x=q.popleft()
    if x in reach:continue
    reach.add(x); q.extend(succ[x])
if len(reach)!=len(nodes):errors.append("unreachable: "+", ".join(sorted(set(nodes)-reach)))
if errors:
    print("FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print(f"PASS: {len(nodes)} nodes")
print("root:",roots[0])
print("reachable:",len(reach))
print("leaves:",", ".join(n for n in nodes if not succ[n]))
