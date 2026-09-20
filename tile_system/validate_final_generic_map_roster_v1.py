#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "tile_system" / "FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv"
TECH = ROOT / "tech_reference" / "MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv"
CIVIC = ROOT / "civics_reference" / "MASTER_CIVIC_UNLOCKS_72_V2.csv"

NORMALIZE = {
    "Road bridges": "Road Bridge Capability",
    "Fort construction specialization": "Fort Construction Specialization",
    "Military Road construction": "Military Road Construction",
    "Improved Road Movement": "Improved Road Movement",
    "Dam (river-linked infrastructure)": "Dam",
    "Bastion Fort upgrade": "Bastion Fort Upgrade",
    "Advanced Fortification upgrade": "Advanced Fortification Upgrade",
    "Hydroelectric Dam upgrade": "Hydroelectric Dam Upgrade",
    "Railroad route": "Railroad",
}

CIVIC_ONLY = {
    "Holy Site": ("", "", "Theology"),
    "Landmark": ("", "", "Humanism"),
    "Hill Farm Placement": ("", "", "Civil Engineering"),
    "Reforestation": ("", "", "Conservation"),
    "National Park": ("", "", "Conservation"),
    "Ski Resort": ("", "", "Professional Sports"),
    "Historic Landmark": ("", "", "Natural History"),
}

FORBIDDEN = {
    "Citadel",
    "Trading Post",
    "Hydro Plant",
    "Aerodrome",
    "Preserve",
}

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

tech_rows = read_csv(TECH)
civic_rows = read_csv(CIVIC)
map_rows = read_csv(ROSTER)

tech_names = {r["TECH_EN"] for r in tech_rows}
civic_names = {r["CIVIC_EN"] for r in civic_rows}
errors = []
expected = {}

for row in tech_rows:
    for column in ("TILE_IMPROVEMENTS", "ROUTES_INFRASTRUCTURE"):
        value = row[column]
        for item in [x.strip() for x in value.split(";") if x.strip()]:
            name = item
            civic = ""
            addtech = ""
            if " with " in item:
                name, suffix = item.rsplit(" with ", 1)
                name = name.strip()
                suffix = suffix.strip()
                if suffix in civic_names:
                    civic = suffix
                elif suffix in tech_names:
                    addtech = suffix
                else:
                    errors.append(f"Unknown suffix gate: {item}")
            name = NORMALIZE.get(name, name)
            if name in expected:
                errors.append(f"Duplicate normalized technology-map item: {name}")
            expected[name] = (row["TECH_EN"], addtech, civic)

for name, gates in CIVIC_ONLY.items():
    if name in expected:
        errors.append(f"Civic/special item duplicates technology item: {name}")
    expected[name] = gates

actual_by_name = {}
actual_ids = set()
for row in map_rows:
    name = row["ITEM_EN"]
    mid = row["MAP_ITEM_ID"]
    if name in actual_by_name:
        errors.append(f"Duplicate ITEM_EN: {name}")
    actual_by_name[name] = row
    if mid in actual_ids:
        errors.append(f"Duplicate MAP_ITEM_ID: {mid}")
    actual_ids.add(mid)

if set(actual_by_name) != set(expected):
    missing = sorted(set(expected) - set(actual_by_name))
    extra = sorted(set(actual_by_name) - set(expected))
    if missing:
        errors.append("Missing map items: " + ", ".join(missing))
    if extra:
        errors.append("Extra map items: " + ", ".join(extra))

for name, gates in expected.items():
    if name not in actual_by_name:
        continue
    row = actual_by_name[name]
    tech, addtech, civic = gates
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
    if not row["MAP_CLASS"] or not row["RECORD_KIND"]:
        errors.append(f"{name}: missing MAP_CLASS or RECORD_KIND")
    if row["STATUS"] != "LOCKED_ROSTER_V1":
        errors.append(f"{name}: unexpected STATUS {row['STATUS']}")

present = set(actual_by_name)
bad = sorted(present & FORBIDDEN)
if bad:
    errors.append("Forbidden/nonbaseline items returned: " + ", ".join(bad))

if len(map_rows) != 39:
    errors.append(f"Expected 39 roster rows, got {len(map_rows)}")

# Important semantic sanity checks.
checks = {
    "Fishing Boats": ("IMPROVEMENT", "BUILDABLE", "Sailing", "", ""),
    "Canal": ("WATER_INFRASTRUCTURE", "BUILDABLE", "Steam Power", "", "Civil Engineering"),
    "Customs House": ("IMPROVEMENT", "BUILDABLE", "Economics", "", "Mercantilism"),
    "Solar Farm": ("ENERGY", "BUILDABLE", "Ecology", "", "Environmentalism"),
    "Historic Landmark": ("ARCHAEOLOGY", "SPECIAL_IMPROVEMENT", "", "", "Natural History"),
    "National Park": ("PROTECTED_AREA", "SPECIAL_AREA", "", "", "Conservation"),
}
for name, vals in checks.items():
    if name not in actual_by_name:
        continue
    row = actual_by_name[name]
    got = (row["MAP_CLASS"], row["RECORD_KIND"], row["TECH_GATE"], row["ADDITIONAL_TECH_GATE"], row["CIVIC_GATE"])
    if got != vals:
        errors.append(f"{name}: semantic tuple expected {vals}, got {got}")

print(f"map_roster_count={len(map_rows)}")
print(f"technology_master_map_entries={32}")
print(f"civic_or_special_entries={7}")
print(f"duplicate_item_names={len(map_rows)-len(actual_by_name)}")
print(f"forbidden_items_present={len(bad)}")
print(f"buildable_rows={sum(1 for r in map_rows if r['RECORD_KIND']=='BUILDABLE')}")
print(f"rule_or_special_rows={sum(1 for r in map_rows if r['RECORD_KIND']!='BUILDABLE')}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
