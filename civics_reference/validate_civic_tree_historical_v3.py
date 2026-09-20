#!/usr/bin/env python3
import csv, pathlib, sys
from collections import defaultdict, deque
P=pathlib.Path(__file__).resolve().parent/"civic_tree_historical_v3.csv"
with P.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
nodes={r["CIVIC_EN"]:r for r in rows}; succ=defaultdict(list); indeg={n:0 for n in nodes}; err=[]
for n,r in nodes.items():
    ps=[x.strip() for x in r["SOCIAL_PREREQUISITES_AND"].split(";") if x.strip()]
    if len(ps)>2: err.append(f"{n}: >2 social prerequisites")
    for p in ps:
        if p not in nodes: err.append(f"{n}: missing {p}"); continue
        if int(nodes[p]["ERA_INDEX"])>int(r["ERA_INDEX"]): err.append(f"{p}->{n}: backward era")
        succ[p].append(n); indeg[n]+=1
roots=[n for n,d in indeg.items() if d==0]
if roots!=["Code of Laws"]: err.append(f"roots={roots}")
d=dict(indeg); q=deque(roots); top=[]
while q:
    x=q.popleft(); top.append(x)
    for y in succ[x]:
        d[y]-=1
        if d[y]==0:q.append(y)
if len(top)!=len(nodes):err.append("cycle")
reach=set();q=deque(["Code of Laws"])
while q:
    x=q.popleft()
    if x in reach:continue
    reach.add(x);q.extend(succ[x])
if len(reach)!=len(nodes):err.append("unreachable="+",".join(sorted(set(nodes)-reach)))
if err:
    print("FAIL");[print("-",x) for x in err];sys.exit(1)
print("PASS")
print("nodes",len(nodes))
print("reachable",len(reach))
print("leaves",", ".join(n for n in nodes if not succ[n]))
