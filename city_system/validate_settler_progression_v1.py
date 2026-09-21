#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROG = ROOT / "city_system" / "SETTLER_PROGRESSION_V1.csv"
BUILDINGS = ROOT / "city_system" / "FINAL_GENERIC_BUILDING_ROSTER_V1.csv"

ERA_ORDER = [
    "Ancient","Classical","Late Antiquity","Early Medieval","High Medieval",
    "Renaissance","Exploration","Enlightenment","Industrial","Modern","Atomic","Information"
]

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

rows = read_csv(PROG)
buildings = read_csv(BUILDINGS)
bmap = {r["BUILDING_EN"]: r for r in buildings}
errors = []

expected_units = ["Settler", "Pioneer", "Colonist", "Urban Planner"]
if [r["UNIT_EN"] for r in rows] != expected_units:
    errors.append("Unexpected settler progression order or membership")

expected_pop = {"Settler":"1","Pioneer":"2","Colonist":"3","Urban Planner":"4"}
for r in rows:
    if r["STARTING_POPULATION"] != expected_pop[r["UNIT_EN"]]:
        errors.append(f"{r['UNIT_EN']}: unexpected population {r['STARTING_POPULATION']}")
    if r["TERRITORY_RULE"] != "SAME_BASE_TERRITORY":
        errors.append(f"{r['UNIT_EN']}: territory rule changed")

for r in rows:
    if r["UNIT_EN"] == "Settler":
        continue
    core = [x.strip() for x in r["CORE_FREE_BUILDING_PACKAGE"].split(";") if x.strip()]
    cutoff = ERA_ORDER.index(r["PACKAGE_CUTOFF_ERA"])
    for name in core:
        if name not in bmap:
            errors.append(f"{r['UNIT_EN']}: unknown building {name}")
            continue
        era = bmap[name]["PROJECT_ERA"]
        if era in ERA_ORDER and ERA_ORDER.index(era) > cutoff:
            errors.append(f"{r['UNIT_EN']}: {name} is after cutoff {r['PACKAGE_CUTOFF_ERA']}")
        prereq = bmap[name]["PREREQUISITE"]
        if prereq and " or " not in prereq and prereq not in core:
            errors.append(f"{r['UNIT_EN']}: prerequisite chain missing {name} <- {prereq}")

urban = next(r for r in rows if r["UNIT_EN"] == "Urban Planner")
urban_core = set(x.strip() for x in urban["CORE_FREE_BUILDING_PACKAGE"].split(";") if x.strip())
for required in ("Factory","Hospital","Sewer","Food Market","Power Plant"):
    if required not in urban_core:
        errors.append(f"Urban Planner missing required Industrial core building: {required}")

print(f"settler_tiers={len(rows)}")
for r in rows:
    core = [x.strip() for x in r["CORE_FREE_BUILDING_PACKAGE"].split(";") if x.strip() and x.strip() != "NONE"]
    print(f"{r['UNIT_EN']}_starting_population={r['STARTING_POPULATION']}")
    print(f"{r['UNIT_EN']}_core_buildings={len(core)}")
print("same_territory_rule=" + str(all(r["TERRITORY_RULE"]=="SAME_BASE_TERRITORY" for r in rows)).lower())
print("factory_hospital_in_urban_planner=" + str({"Factory","Hospital"}.issubset(urban_core)).lower())

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
