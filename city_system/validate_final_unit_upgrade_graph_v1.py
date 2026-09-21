#!/usr/bin/env python3
import csv
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "city_system" / "FINAL_GENERIC_UNIT_ROSTER_V1.csv"
GRAPH = ROOT / "city_system" / "FINAL_UNIT_UPGRADE_GRAPH_V1.csv"

ERA = {
    "Ancient": 1,
    "Classical": 2,
    "Late Antiquity": 3,
    "Early Medieval": 4,
    "High Medieval": 5,
    "Renaissance": 6,
    "Exploration": 7,
    "Enlightenment": 8,
    "Industrial": 9,
    "Modern": 10,
    "Atomic": 11,
    "Information": 12,
    "Future": 13,
}

VALID_MODES = {
    "DIRECT",
    "DIRECT_CLASS_SHIFT",
    "DIRECT_SUPPORT",
    "DIRECT_SUPPORT_CLASS_SHIFT",
    "DIRECT_CLASS_EVOLUTION",
    "CONVERGENT_DIRECT",
    "CONVERGENT_DIRECT_CLASS_SHIFT",
    "BRANCH_CHOICE",
    "PRODUCTION_REPLACEMENT",
    "NO_UPGRADE",
    "NO_UNIT_UPGRADE",
}

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

units = read(ROSTER)
graph = read(GRAPH)
by_unit = {r["UNIT_EN"]: r for r in units}
errors = []

if len(units) != 89:
    errors.append(f"expected 89 roster units, got {len(units)}")
if len(graph) != 89:
    errors.append(f"expected 89 graph rows, got {len(graph)}")

names = [r["UNIT_EN"] for r in graph]
if len(set(names)) != len(names):
    errors.append("duplicate UNIT_EN rows in graph")

missing = sorted(set(by_unit) - set(names))
extra = sorted(set(names) - set(by_unit))
if missing:
    errors.append("missing graph rows: " + ", ".join(missing))
if extra:
    errors.append("unknown graph rows: " + ", ".join(extra))

adj = defaultdict(list)

for row in graph:
    name = row["UNIT_EN"]
    if row["UPGRADE_MODE"] not in VALID_MODES:
        errors.append(f"{name}: invalid mode {row['UPGRADE_MODE']}")
    if row["STATUS"] != "LOCKED_V1":
        errors.append(f"{name}: unexpected status {row['STATUS']}")

    successors = [x.strip() for x in row["DIRECT_UPGRADE_TO"].split(";") if x.strip()]

    if row["UPGRADE_MODE"] in {"NO_UPGRADE", "NO_UNIT_UPGRADE"} and successors:
        errors.append(f"{name}: no-upgrade row has successors")
    if row["UPGRADE_MODE"] == "PRODUCTION_REPLACEMENT" and len(successors) != 1:
        errors.append(f"{name}: production replacement must have exactly one successor")
    if row["UPGRADE_MODE"] == "BRANCH_CHOICE" and len(successors) < 2:
        errors.append(f"{name}: branch choice must have at least two successors")
    if row["UPGRADE_MODE"] not in {"NO_UPGRADE", "NO_UNIT_UPGRADE"} and row["UPGRADE_MODE"] != "PRODUCTION_REPLACEMENT" and not successors:
        errors.append(f"{name}: upgrade mode requires a successor")

    if name not in by_unit:
        continue

    for successor in successors:
        if successor not in by_unit:
            errors.append(f"{name}: unknown successor {successor}")
            continue
        if ERA[by_unit[successor]["PROJECT_ERA"]] < ERA[by_unit[name]["PROJECT_ERA"]]:
            errors.append(f"{name} -> {successor}: era regression")
        adj[name].append(successor)

# No directed cycles.
indeg = {name: 0 for name in by_unit}
for src, dsts in adj.items():
    for dst in dsts:
        indeg[dst] += 1
q = deque([n for n, d in indeg.items() if d == 0])
seen = 0
while q:
    n = q.popleft()
    seen += 1
    for dst in adj[n]:
        indeg[dst] -= 1
        if indeg[dst] == 0:
            q.append(dst)
if seen != len(by_unit):
    errors.append("directed cycle detected in unit upgrade graph")

g = {r["UNIT_EN"]: r for r in graph}

# Locked special decisions.
for a, b in [("Settler","Pioneer"),("Pioneer","Colonist"),("Colonist","Urban Planner")]:
    if a not in g or g[a]["UPGRADE_MODE"] != "PRODUCTION_REPLACEMENT" or g[a]["DIRECT_UPGRADE_TO"] != b:
        errors.append(f"{a}: founding progression must be production replacement -> {b}")

if g.get("Urban Planner", {}).get("DIRECT_UPGRADE_TO", ""):
    errors.append("Urban Planner must be terminal")

if g.get("Privateer", {}).get("DIRECT_UPGRADE_TO") != "Submarine":
    errors.append("Privateer must upgrade to Submarine")

if g.get("Paratrooper", {}).get("DIRECT_UPGRADE_TO") != "XCOM Squad":
    errors.append("Paratrooper must upgrade to XCOM Squad")

if g.get("Marine", {}).get("DIRECT_UPGRADE_TO", ""):
    errors.append("Marine must remain terminal specialist")

if g.get("Giant Death Robot", {}).get("UPGRADE_MODE") != "NO_UNIT_UPGRADE":
    errors.append("Giant Death Robot must use module upgrades rather than successor unit")

frigate = g.get("Frigate", {})
if frigate.get("UPGRADE_MODE") != "BRANCH_CHOICE":
    errors.append("Frigate must remain the explicit naval branch-choice row")
else:
    fs = {x.strip() for x in frigate["DIRECT_UPGRADE_TO"].split(";") if x.strip()}
    if fs != {"Ship of the Line", "Cruiser"}:
        errors.append("Frigate branch must be Ship of the Line / Cruiser")

expected_lines = {
    "Warrior": "Swordsman",
    "Swordsman": "Man-at-Arms",
    "Man-at-Arms": "Arquebusier",
    "Arquebusier": "Line Infantry",
    "Line Infantry": "Rifleman",
    "Rifleman": "Infantry",
    "Infantry": "Mechanized Infantry",
    "Spearman": "Pikeman",
    "Pikeman": "Pike and Shot",
    "Pike and Shot": "Anti-Tank Gun",
    "Anti-Tank Gun": "Modern AT",
    "Archer": "Composite Bowman",
    "Composite Bowman": "Crossbowman",
    "Crossbowman": "Skirmisher",
    "Skirmisher": "Gatling Gun",
    "Gatling Gun": "Machine Gun",
    "Catapult": "Trebuchet",
    "Trebuchet": "Bombard",
    "Bombard": "Field Gun",
    "Field Gun": "Artillery",
    "Artillery": "Rocket Artillery",
    "Scout": "Explorer",
    "Explorer": "Ranger",
    "Ranger": "Spec Ops",
    "Horseman": "Cavalry",
    "Cavalry": "Helicopter",
    "Chariot Archer": "Knight",
    "Knight": "Lancer",
    "Lancer": "Landship",
    "Landship": "Tank",
    "Tank": "Modern Armor",
    "Triplane": "Fighter",
    "Fighter": "Jet Fighter",
    "Great War Bomber": "Bomber",
    "Bomber": "Stealth Bomber",
    "Anti-Air Gun": "Mobile SAM",
    "Observation Balloon": "Drone",
    "Medic": "Supply Convoy",
}

for src, dst in expected_lines.items():
    if g.get(src, {}).get("DIRECT_UPGRADE_TO") != dst:
        errors.append(f"{src}: expected locked successor {dst}")

mode_counts = defaultdict(int)
for row in graph:
    mode_counts[row["UPGRADE_MODE"]] += 1

print(f"roster_units={len(units)}")
print(f"graph_rows={len(graph)}")
print(f"branch_rows={mode_counts['BRANCH_CHOICE']}")
print(f"production_replacements={mode_counts['PRODUCTION_REPLACEMENT']}")
print(f"no_upgrade_rows={mode_counts['NO_UPGRADE'] + mode_counts['NO_UNIT_UPGRADE']}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
