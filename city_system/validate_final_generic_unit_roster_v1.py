#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "city_system" / "FINAL_GENERIC_UNIT_ROSTER_V1.csv"
TECH = ROOT / "tech_reference" / "MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv"
CIVIC = ROOT / "civics_reference" / "MASTER_CIVIC_UNLOCKS_72_V2.csv"

CIVIC_ONLY = {
    "Spy": ("", "", "Diplomatic Service"),
    "Explorer": ("Cartography", "", "Exploration"),
    "Galleon": ("Astronomy", "", "Exploration"),
    "Privateer": ("Warships", "", "Mercantilism"),
    "Archaeologist": ("", "", "Natural History"),
    "Naturalist": ("", "", "Conservation"),
    "Rock Band": ("", "", "Cold War"),
}
ADVANCED_SETTLERS = {
    "Pioneer": ("Cartography", "", "Exploration"),
    "Colonist": ("Railroad", "", "Colonialism"),
    "Urban Planner": ("Combustion", "", "Urbanization"),
}
BASELINE = {
    "Settler": "GAME_START",
    "Warrior": "GAME_START",
    "Scout": "GAME_START",
    "Missionary": "MAJORITY_RELIGION",
    "Inquisitor": "ENHANCED_RELIGION",
}
FORBIDDEN = {"Heavy Chariot", "Nuclear Missile"}
GREAT_PEOPLE = {
    "Great Artist", "Great Engineer", "Great General", "Great Merchant",
    "Great Scientist", "Great Admiral", "Great Prophet", "Great Musician",
    "Great Writer", "Great Director",
}

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

tech_rows = read_csv(TECH)
civic_rows = read_csv(CIVIC)
unit_rows = read_csv(ROSTER)

tech_names = {r["TECH_EN"] for r in tech_rows}
civic_names = {r["CIVIC_EN"] for r in civic_rows}

errors = []

# Build exact expected unit/gate map from the authoritative technology master.
expected = {}
for row in tech_rows:
    for item in [x.strip() for x in row["UNITS"].split(";") if x.strip()]:
        name = item
        addtech = ""
        civic = ""
        if " with " in item:
            name, suffix = item.rsplit(" with ", 1)
            name = name.strip()
            suffix = suffix.strip()
            if suffix in tech_names:
                addtech = suffix
            elif suffix in civic_names:
                civic = suffix
            else:
                errors.append(f"Unknown suffix gate in technology master: {item}")
        if name in expected:
            errors.append(f"Duplicate technology-master unit: {name}")
        expected[name] = (row["TECH_EN"], addtech, civic)

for name, gates in CIVIC_ONLY.items():
    if name in expected:
        errors.append(f"Civic-only unit duplicates technology-master unit: {name}")
    expected[name] = gates

for name, gates in ADVANCED_SETTLERS.items():
    if name in expected:
        errors.append(f"Advanced settler duplicates another source: {name}")
    expected[name] = gates

for name in BASELINE:
    if name in expected:
        errors.append(f"Baseline unit duplicates another source: {name}")
    expected[name] = ("", "", "")

actual_by_name = {}
actual_ids = set()
for row in unit_rows:
    name = row["UNIT_EN"]
    uid = row["UNIT_ID"]
    if name in actual_by_name:
        errors.append(f"Duplicate UNIT_EN: {name}")
    actual_by_name[name] = row
    if uid in actual_ids:
        errors.append(f"Duplicate UNIT_ID: {uid}")
    actual_ids.add(uid)

if set(actual_by_name) != set(expected):
    missing = sorted(set(expected) - set(actual_by_name))
    extra = sorted(set(actual_by_name) - set(expected))
    if missing:
        errors.append("Missing units: " + ", ".join(missing))
    if extra:
        errors.append("Extra units: " + ", ".join(extra))

for name, gates in expected.items():
    if name not in actual_by_name:
        continue
    row = actual_by_name[name]
    tech, addtech, civic = gates
    if name in BASELINE:
        if row["SYSTEM_GATE"] != BASELINE[name]:
            errors.append(f"{name}: expected SYSTEM_GATE={BASELINE[name]}, got {row['SYSTEM_GATE']}")
    else:
        if row["TECH_GATE"] != tech:
            errors.append(f"{name}: TECH_GATE expected {tech!r}, got {row['TECH_GATE']!r}")
        if row["ADDITIONAL_TECH_GATE"] != addtech:
            errors.append(f"{name}: ADDITIONAL_TECH_GATE expected {addtech!r}, got {row['ADDITIONAL_TECH_GATE']!r}")
        if row["CIVIC_GATE"] != civic:
            errors.append(f"{name}: CIVIC_GATE expected {civic!r}, got {row['CIVIC_GATE']!r}")
    if row["TECH_GATE"] and row["TECH_GATE"] not in tech_names:
        errors.append(f"{name}: unknown TECH_GATE {row['TECH_GATE']}")
    if row["ADDITIONAL_TECH_GATE"] and row["ADDITIONAL_TECH_GATE"] not in tech_names:
        errors.append(f"{name}: unknown ADDITIONAL_TECH_GATE {row['ADDITIONAL_TECH_GATE']}")
    if row["CIVIC_GATE"] and row["CIVIC_GATE"] not in civic_names:
        errors.append(f"{name}: unknown CIVIC_GATE {row['CIVIC_GATE']}")
    if not row["DOMAIN"] or not row["ROLE_FAMILY"]:
        errors.append(f"{name}: missing DOMAIN or ROLE_FAMILY")
    if row["STATUS"] != "LOCKED_ROSTER_V1":
        errors.append(f"{name}: unexpected STATUS {row['STATUS']}")

present = set(actual_by_name)
bad_forbidden = sorted(present & FORBIDDEN)
if bad_forbidden:
    errors.append("Forbidden baseline units returned: " + ", ".join(bad_forbidden))
bad_gp = sorted(present & GREAT_PEOPLE)
if bad_gp:
    errors.append("Great People incorrectly included in generic roster: " + ", ".join(bad_gp))

if len(unit_rows) != 89:
    errors.append(f"Expected 89 units, got {len(unit_rows)}")

# Domain sanity for special civilian/trade units.
expected_domains = {
    "Work Boat": "SEA",
    "Caravan": "LAND",
    "Cargo Ship": "SEA",
    "Spy": "OFFMAP",
    "Guided Missile": "MISSILE",
}
for name, domain in expected_domains.items():
    if name in actual_by_name and actual_by_name[name]["DOMAIN"] != domain:
        errors.append(f"{name}: DOMAIN expected {domain}, got {actual_by_name[name]['DOMAIN']}")

print(f"unit_count={len(unit_rows)}")
print(f"technology_master_units={sum(1 for r in unit_rows if r['SOURCE_FILE'].endswith('MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv'))}")
print(f"civic_only_units={sum(1 for r in unit_rows if r['SOURCE_FILE'].endswith('MASTER_CIVIC_UNLOCKS_72_V2.csv'))}")
print(f"baseline_system_units={sum(1 for r in unit_rows if r['SOURCE_RECORD']=='BASELINE_RECOVERY')}")
print(f"advanced_settler_units={sum(1 for r in unit_rows if r['SOURCE_RECORD']=='SETTLER_PROGRESSION_V1')}")
print(f"duplicate_unit_names={len(unit_rows)-len(actual_by_name)}")
print(f"forbidden_units_present={len(bad_forbidden)}")
print(f"great_people_present={len(bad_gp)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
