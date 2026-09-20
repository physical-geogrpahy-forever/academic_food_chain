#!/usr/bin/env python3
"""Validate the locked 72-civic project tree.

Checks:
- exactly one root
- all prerequisite names exist
- all nodes reachable from Code of Laws
- no directed cycles
- no backward-era edges
- at most two direct prerequisites
- no isolated node

The stored Future-civic edges are a reference topology.
Runtime may shuffle civic names through the documented A-E template without
changing these graph invariants.
"""
import csv, pathlib, sys
from collections import defaultdict, deque

HERE = pathlib.Path(__file__).resolve().parent
CSV = HERE / "civic_tree_locked_v1.csv"

with CSV.open(encoding="utf-8-sig", newline="") as f:
    data = list(csv.DictReader(f))

nodes = {r["CIVIC_EN"]: r for r in data}
succ = defaultdict(list)
indeg = {n: 0 for n in nodes}
errors = []

for n, r in nodes.items():
    prereqs = [x.strip() for x in r["PREREQUISITES_AND"].split(";") if x.strip()]
    if len(prereqs) > 2:
        errors.append(f"{n}: >2 prerequisites")
    for p in prereqs:
        if p not in nodes:
            errors.append(f"{n}: missing prerequisite {p}")
            continue
        if int(nodes[p]["ERA_INDEX"]) > int(r["ERA_INDEX"]):
            errors.append(f"{p} -> {n}: backward era edge")
        succ[p].append(n)
        indeg[n] += 1

roots = [n for n,d in indeg.items() if d == 0]
if roots != ["Code of Laws"]:
    errors.append(f"unexpected roots: {roots}")

q = deque(roots)
seen_topo = []
deg = dict(indeg)
while q:
    x = q.popleft()
    seen_topo.append(x)
    for y in succ[x]:
        deg[y] -= 1
        if deg[y] == 0:
            q.append(y)
if len(seen_topo) != len(nodes):
    errors.append("cycle detected")

reach = set()
q = deque(["Code of Laws"])
while q:
    x = q.popleft()
    if x in reach:
        continue
    reach.add(x)
    q.extend(succ[x])
if len(reach) != len(nodes):
    errors.append("unreachable: " + ", ".join(sorted(set(nodes) - reach)))

isolated = [n for n in nodes if indeg[n] == 0 and not succ[n]]
if isolated:
    errors.append("isolated: " + ", ".join(isolated))

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

leaves = [n for n in nodes if not succ[n]]
print(f"PASS: {len(nodes)} nodes")
print("roots:", roots)
print("reachable:", len(reach))
print("terminal branches:", ", ".join(leaves))
