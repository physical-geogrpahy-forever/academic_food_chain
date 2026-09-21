#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "city_system" / "FINAL_GENERIC_UNIT_ROSTER_V1.csv"
NUMERIC = ROOT / "city_system" / "FINAL_UNIT_NUMERIC_BALANCE_V1.csv"
GRAPH = ROOT / "city_system" / "FINAL_UNIT_UPGRADE_GRAPH_V1.csv"
UPGRADE = ROOT / "city_system" / "FINAL_UNIT_UPGRADE_COSTS_V1.csv"

ERA_EQ = {
    "Ancient": 0,
    "Classical": 1,
    "Late Antiquity": 2,
    "Early Medieval": 2,
    "High Medieval": 2,
    "Renaissance": 3,
    "Exploration": 3,
    "Enlightenment": 4,
    "Industrial": 4,
    "Modern": 5,
    "Atomic": 6,
    "Information": 7,
    "Future": 8,
}

DEFERRED = {
    "Settler", "Pioneer", "Colonist", "Urban Planner",
    "Missionary", "Inquisitor", "Spy", "Naturalist", "Rock Band",
}

NONCOMBAT_LOCKED = {
    "Work Boat", "Worker", "Battering Ram", "Siege Tower",
    "Military Engineer", "Archaeologist", "Medic", "Supply Convoy",
    "Observation Balloon", "Drone", "Caravan", "Cargo Ship",
}

ANCHORS = {
    "Warrior": {"COMBAT": 8, "MOVES": 2, "PRODUCTION_COST": 40},
    "Swordsman": {"COMBAT": 14, "MOVES": 2, "PRODUCTION_COST": 75},
    "Archer": {"COMBAT": 5, "RANGED_COMBAT": 7, "RANGE": 2, "PRODUCTION_COST": 40},
    "Crossbowman": {"COMBAT": 13, "RANGED_COMBAT": 18, "RANGE": 2, "PRODUCTION_COST": 120},
    "Cavalry": {"COMBAT": 34, "MOVES": 4, "PRODUCTION_COST": 225},
    "Tank": {"COMBAT": 70, "MOVES": 5, "PRODUCTION_COST": 375},
    "Modern Armor": {"COMBAT": 100, "MOVES": 5, "PRODUCTION_COST": 425},
    "Artillery": {"COMBAT": 21, "RANGED_COMBAT": 28, "RANGE": 3, "PRODUCTION_COST": 250},
    "Rocket Artillery": {"COMBAT": 45, "RANGED_COMBAT": 60, "RANGE": 3, "PRODUCTION_COST": 425},
    "Frigate": {"COMBAT": 25, "RANGED_COMBAT": 28, "MOVES": 5, "PRODUCTION_COST": 185},
    "Battleship": {"COMBAT": 55, "RANGED_COMBAT": 65, "RANGE": 3, "PRODUCTION_COST": 375},
    "Missile Cruiser": {"COMBAT": 80, "RANGED_COMBAT": 100, "MOVES": 7, "PRODUCTION_COST": 425},
    "XCOM Squad": {"COMBAT": 100, "PARADROP_RANGE": 40, "PRODUCTION_COST": 400},
    "Giant Death Robot": {"COMBAT": 150, "RANGED_COMBAT": 100, "RANGE": 3, "MOVES": 5, "PRODUCTION_COST": 550},
}

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def intval(row, field):
    v = row[field].strip()
    return None if v == "" else int(float(v))

roster = read(ROSTER)
numeric = read(NUMERIC)
graph = read(GRAPH)
upgrade = read(UPGRADE)

rmap = {r["UNIT_EN"]: r for r in roster}
nmap = {r["UNIT_EN"]: r for r in numeric}
gmap = {r["UNIT_EN"]: r for r in graph}
errors = []

if len(roster) != 89:
    errors.append(f"roster rows expected 89, got {len(roster)}")
if len(numeric) != 89:
    errors.append(f"numeric rows expected 89, got {len(numeric)}")
if len(nmap) != len(numeric):
    errors.append("duplicate UNIT_EN in numeric table")
if set(nmap) != set(rmap):
    errors.append("numeric unit set differs from canonical roster")

# Row-level numeric and resource checks.
for name, r in rmap.items():
    n = nmap.get(name)
    if not n:
        continue

    if n["PROJECT_ERA"] != r["PROJECT_ERA"]:
        errors.append(f"{name}: era mismatch")
    if n["ROLE_FAMILY"] != r["ROLE_FAMILY"]:
        errors.append(f"{name}: role mismatch")
    if n["STRATEGIC_RESOURCE"] != r["RESOURCE_REQUIREMENT"]:
        errors.append(f"{name}: strategic-resource mismatch")

    has_res = bool(n["STRATEGIC_RESOURCE"].strip())
    if intval(n, "RESOURCE_SLOT_COST") != (1 if has_res else 0):
        errors.append(f"{name}: bad strategic-resource slot cost")
    if intval(n, "RESOURCE_UPKEEP_PER_TURN") != 0:
        errors.append(f"{name}: V1 unexpectedly introduces per-turn strategic upkeep")

    if name in DEFERRED:
        if n["NUMERIC_STATUS"] != "DEFERRED_SYSTEM_ECONOMY":
            errors.append(f"{name}: must be deferred-system economy")
        if n["PRODUCTION_COST"].strip():
            errors.append(f"{name}: deferred system unit unexpectedly has production cost")
        continue

    if n["NUMERIC_STATUS"] != "LOCKED_MILITARY_V1":
        errors.append(f"{name}: expected LOCKED_MILITARY_V1")

    if intval(n, "MOVES") is None:
        errors.append(f"{name}: missing movement")
    if intval(n, "PRODUCTION_COST") is None:
        errors.append(f"{name}: missing production cost")

    # Combat units need at least one combat value. Air/missile units use ranged strength.
    if name not in NONCOMBAT_LOCKED:
        if intval(n, "COMBAT") is None and intval(n, "RANGED_COMBAT") is None:
            errors.append(f"{name}: combat unit has no combat or ranged value")

    if n["GOLD_MAINTENANCE_RULE"] not in {
        "GLOBAL_CIV5_FORMULA", "GLOBAL_CIV5_FORMULA_TRADE_SUPPLY_EXEMPT"
    }:
        errors.append(f"{name}: unexpected maintenance rule")

# Deferred set must be exact.
actual_deferred = {r["UNIT_EN"] for r in numeric if r["NUMERIC_STATUS"] == "DEFERRED_SYSTEM_ECONOMY"}
if actual_deferred != DEFERRED:
    errors.append(
        f"deferred set mismatch expected={sorted(DEFERRED)} actual={sorted(actual_deferred)}"
    )

# Anchor values should not drift silently.
for name, expected in ANCHORS.items():
    n = nmap[name]
    for field, value in expected.items():
        actual = intval(n, field)
        if actual != value:
            errors.append(f"{name}: anchor {field} expected {value}, got {actual}")

# Direct-upgrade combat power should not decrease when both endpoints are combat-capable.
def power(row):
    vals = [intval(row, "COMBAT"), intval(row, "RANGED_COMBAT")]
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None

for g in graph:
    if g["UPGRADE_MODE"] in {"NO_UPGRADE", "NO_UNIT_UPGRADE", "PRODUCTION_REPLACEMENT"}:
        continue
    src = nmap[g["UNIT_EN"]]
    sp = power(src)
    for dst_name in [x.strip() for x in g["DIRECT_UPGRADE_TO"].split(";") if x.strip()]:
        dst = nmap[dst_name]
        dp = power(dst)
        if sp is not None and dp is not None and dp < sp:
            errors.append(f"combat power regression {g['UNIT_EN']}({sp}) -> {dst_name}({dp})")

# Upgrade-cost rows: reconstruct all eligible direct edges.
expected_edges = []
for g in graph:
    if g["UPGRADE_MODE"] in {"NO_UPGRADE", "NO_UNIT_UPGRADE", "PRODUCTION_REPLACEMENT"}:
        continue
    src = nmap[g["UNIT_EN"]]
    if not src["PRODUCTION_COST"].strip():
        continue
    for dst_name in [x.strip() for x in g["DIRECT_UPGRADE_TO"].split(";") if x.strip()]:
        dst = nmap[dst_name]
        if not dst["PRODUCTION_COST"].strip():
            continue
        expected_edges.append((g["UNIT_EN"], dst_name))

actual_edges = [(r["FROM_UNIT"], r["TO_UNIT"]) for r in upgrade]
if len(upgrade) != 55:
    errors.append(f"upgrade-cost rows expected 55, got {len(upgrade)}")
if len(set(actual_edges)) != len(actual_edges):
    errors.append("duplicate edge in upgrade-cost table")
if set(actual_edges) != set(expected_edges):
    errors.append("upgrade-cost edge set differs from numeric upgrade graph")

for row in upgrade:
    src = nmap[row["FROM_UNIT"]]
    dst = nmap[row["TO_UNIT"]]
    old = intval(src, "PRODUCTION_COST")
    new = intval(dst, "PRODUCTION_COST")
    eq = ERA_EQ[dst["PROJECT_ERA"]]
    base = 10 + max(0, 2 * (new - old))
    raw = base * (1 + 0.3 * eq)
    expected_gold = int(raw // 5) * 5

    if int(row["FROM_COST"]) != old or int(row["TO_COST"]) != new:
        errors.append(f"{row['FROM_UNIT']}->{row['TO_UNIT']}: cached production cost mismatch")
    if int(row["CIV5_EQUIVALENT_ERA_INDEX"]) != eq:
        errors.append(f"{row['FROM_UNIT']}->{row['TO_UNIT']}: bad equivalent era")
    if int(row["BASE_COST"]) != base:
        errors.append(f"{row['FROM_UNIT']}->{row['TO_UNIT']}: bad base cost")
    if int(row["FINAL_GOLD_COST"]) != expected_gold:
        errors.append(f"{row['FROM_UNIT']}->{row['TO_UNIT']}: upgrade Gold formula mismatch")
    if int(row["FINAL_GOLD_COST"]) % 5 != 0:
        errors.append(f"{row['FROM_UNIT']}->{row['TO_UNIT']}: Gold cost not rounded to 5")

# Founding production replacement must never leak into Gold upgrade table.
founding = {"Settler","Pioneer","Colonist"}
if any(r["FROM_UNIT"] in founding for r in upgrade):
    errors.append("founding production replacement incorrectly receives Gold upgrade row")

print(f"roster_rows={len(roster)}")
print(f"numeric_rows={len(numeric)}")
print(f"locked_numeric_rows={sum(r['NUMERIC_STATUS']=='LOCKED_MILITARY_V1' for r in numeric)}")
print(f"deferred_system_rows={sum(r['NUMERIC_STATUS']=='DEFERRED_SYSTEM_ECONOMY' for r in numeric)}")
print(f"upgrade_cost_rows={len(upgrade)}")
print(f"resource_upkeep_nonzero={sum(intval(r,'RESOURCE_UPKEEP_PER_TURN') not in (None,0) for r in numeric)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
