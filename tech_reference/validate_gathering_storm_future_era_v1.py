#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TECH_TREE = ROOT / "tech_reference" / "technology_tree_historical_v2.csv"
CIVIC_TREE = ROOT / "civics_reference" / "civic_tree_historical_v3.csv"
CROSSLINK = ROOT / "civics_reference" / "civic_tech_crosslinks_v1.csv"
UNITS = ROOT / "city_system" / "FINAL_GENERIC_UNIT_ROSTER_V1.csv"
POLICIES = ROOT / "civics_reference" / "FINAL_POLICY_CARD_ROSTER_V1.csv"
MAPS = ROOT / "tile_system" / "FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv"
BUILDINGS = ROOT / "city_system" / "FINAL_GENERIC_BUILDING_ROSTER_V1.csv"

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

EXPECTED_TECH = {
    "Atomic": {"Computers","Nuclear Fission","Synthetic Materials","Ecology","Particle Physics"},
    "Information": {"Telecommunications","Satellites","Guidance Systems","Lasers","Composites","Stealth Technology","Robotics","Nuclear Fusion","Nanotechnology"},
    "Future": {"Advanced AI","Advanced Power Cells","Cybernetics","Smart Materials","Predictive Systems","Seasteads","Offworld Mission","Future Tech"},
}

EXPECTED_CIVIC = {
    "Atomic": {"Nuclear Program","Cultural Heritage","Cold War","Rapid Deployment","Space Race"},
    "Information": {"Globalization","Social Media","Near Future Governance","Venture Politics","Distributed Sovereignty","Optimization Imperative","Environmentalism"},
    "Future": {"Information Warfare","Global Warming Mitigation","Cultural Hegemony","Smart Power Doctrine","Exodus Imperative","Future Civic"},
}

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

tech = read(TECH_TREE)
civic = read(CIVIC_TREE)
cross = read(CROSSLINK)
units = read(UNITS)
policies = read(POLICIES)
maps = read(MAPS)
buildings = read(BUILDINGS)

tm = {r["TECH"]: r for r in tech}
cm = {r["CIVIC_EN"]: r for r in civic}
errors = []

if len(tech) != 109:
    errors.append(f"technology count expected 109, got {len(tech)}")
if len(civic) != 72:
    errors.append(f"civic count expected 72, got {len(civic)}")
if len(units) != 89:
    errors.append(f"unit count expected 89, got {len(units)}")
if len(policies) != 127:
    errors.append(f"policy count expected 127, got {len(policies)}")
if len(maps) != 39:
    errors.append(f"map count expected 39, got {len(maps)}")
if len(buildings) != 102:
    errors.append(f"building count expected 102, got {len(buildings)}")

for era, expected in EXPECTED_TECH.items():
    actual = {r["TECH"] for r in tech if r["PROJECT_ERA"] == era}
    if actual != expected:
        errors.append(f"{era} technologies mismatch: expected={sorted(expected)} actual={sorted(actual)}")

for era, expected in EXPECTED_CIVIC.items():
    actual = {r["CIVIC_EN"] for r in civic if r["PROJECT_ERA"] == era}
    if actual != expected:
        errors.append(f"{era} civics mismatch: expected={sorted(expected)} actual={sorted(actual)}")

for r in tech:
    if int(r["ERA_INDEX"]) != ERA[r["PROJECT_ERA"]]:
        errors.append(f"{r['TECH']}: bad era index")
    for p in [x.strip() for x in r["PREREQUISITES_AND"].split(";") if x.strip()]:
        if p not in tm:
            errors.append(f"{r['TECH']}: missing prerequisite {p}")
        elif int(tm[p]["ERA_INDEX"]) > int(r["ERA_INDEX"]):
            errors.append(f"backward tech edge {p} -> {r['TECH']}")

for r in civic:
    if int(r["ERA_INDEX"]) != ERA[r["PROJECT_ERA"]]:
        errors.append(f"{r['CIVIC_EN']}: bad era index")
    for p in [x.strip() for x in r["SOCIAL_PREREQUISITES_AND"].split(";") if x.strip()]:
        if p not in cm:
            errors.append(f"{r['CIVIC_EN']}: missing prerequisite {p}")
        elif int(cm[p]["ERA_INDEX"]) > int(r["ERA_INDEX"]):
            errors.append(f"backward civic edge {p} -> {r['CIVIC_EN']}")

for r in cross:
    t = r["DIRECT_TECH"].strip()
    if not t:
        continue
    if t not in tm:
        errors.append(f"{r['CIVIC_EN']}: missing crosslink tech {t}")
        continue
    c = cm[r["CIVIC_EN"]]
    if ERA[tm[t]["PROJECT_ERA"]] > ERA[c["PROJECT_ERA"]]:
        errors.append(f"later-tech crosslink {r['CIVIC_EN']} <- {t}")

def latest_gate_era(tech_gate="", additional_tech="", civic_gate=""):
    n = 0
    for t in (tech_gate, additional_tech):
        if t and t in tm:
            n = max(n, ERA[tm[t]["PROJECT_ERA"]])
    if civic_gate and civic_gate in cm:
        n = max(n, ERA[cm[civic_gate]["PROJECT_ERA"]])
    return n

for r in units:
    n = latest_gate_era(r["TECH_GATE"], r["ADDITIONAL_TECH_GATE"], r["CIVIC_GATE"])
    if n and ERA[r["PROJECT_ERA"]] < n:
        errors.append(f"unit earlier than gate: {r['UNIT_EN']}")

for r in policies:
    owner = cm.get(r["CIVIC_EN"])
    if not owner:
        errors.append(f"policy missing owner civic: {r['POLICY_EN']}")
    elif r["PROJECT_ERA"] != owner["PROJECT_ERA"]:
        errors.append(f"policy era mismatch: {r['POLICY_EN']}")

for r in maps:
    n = latest_gate_era(r["TECH_GATE"], r["ADDITIONAL_TECH_GATE"], r["CIVIC_GATE"])
    if n and ERA[r["PROJECT_ERA"]] < n:
        errors.append(f"map item earlier than gate: {r['ITEM_EN']}")

for r in buildings:
    cg = r["CIVIC_GATE"].strip()
    if cg and cg not in cm and not cg.startswith("Tier-"):
        errors.append(f"building unknown civic gate: {r['BUILDING_EN']} -> {cg}")
    n = latest_gate_era(r["TECH_GATE"], "", cg if cg in cm else "")
    if n and r["PROJECT_ERA"] in ERA and ERA[r["PROJECT_ERA"]] < n:
        errors.append(f"building earlier than gate: {r['BUILDING_EN']}")

u = {r["UNIT_EN"]: r for r in units}
if "Giant Death Robot" not in u:
    errors.append("Giant Death Robot missing")
else:
    if u["Giant Death Robot"]["TECH_GATE"] != "Robotics" or u["Giant Death Robot"]["PROJECT_ERA"] != "Information":
        errors.append("Giant Death Robot gate/era mismatch")

if "XCOM Squad" not in u:
    errors.append("XCOM Squad missing")
else:
    x = u["XCOM Squad"]
    if (x["TECH_GATE"], x["CIVIC_GATE"], x["PROJECT_ERA"]) != ("Cybernetics","Rapid Deployment","Future"):
        errors.append("XCOM Squad gate/era mismatch")

pmap = {r["POLICY_EN"]: r for r in policies}
ial = pmap.get("Integrated Attack Logistics")
if not ial or "50% Production toward Giant Death Robots" not in ial["FINAL_EFFECT"]:
    errors.append("Integrated Attack Logistics GDR production clause missing")

print("future_era_index=13")
print(f"technology_count={len(tech)}")
print(f"civic_count={len(civic)}")
print(f"unit_count={len(units)}")
print(f"policy_count={len(policies)}")
print(f"map_count={len(maps)}")
print(f"building_count={len(buildings)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
