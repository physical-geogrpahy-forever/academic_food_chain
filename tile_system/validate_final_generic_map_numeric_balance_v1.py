#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "tile_system" / "FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv"
NUMERIC = ROOT / "tile_system" / "FINAL_GENERIC_MAP_NUMERIC_BALANCE_V1.csv"
UPGRADES = ROOT / "tile_system" / "FINAL_MAP_YIELD_UPGRADE_RULES_V1.csv"
COMPAT = ROOT / "tile_system" / "FINAL_RESOURCE_IMPROVEMENT_COMPATIBILITY_V1.csv"
MORELUX = ROOT / "tile_system" / "FINAL_MORE_LUXURIES_RESOURCE_RULES_V1.csv"
RESOURCE_CATALOG = ROOT / "civ_map_stage10_resources" / "resource_catalog_v1.yaml"

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def iv(row, field):
    return int(float(row[field]))

roster = read(ROSTER)
numeric = read(NUMERIC)
upgrades = read(UPGRADES)
compat = read(COMPAT)
morelux = read(MORELUX)

rmap = {r["ITEM_EN"]: r for r in roster}
nmap = {r["ITEM_EN"]: r for r in numeric}
cmap = {r["RESOURCE_ID"]: r for r in compat}
mlmap = {r["RESOURCE_ID"]: r for r in morelux}
errors = []

# Canonical 39 map records.
if len(roster) != 39:
    errors.append(f"map roster expected 39, got {len(roster)}")
if len(numeric) != 39:
    errors.append(f"map numeric expected 39, got {len(numeric)}")
if len(rmap) != len(roster):
    errors.append("duplicate ITEM_EN in map roster")
if len(nmap) != len(numeric):
    errors.append("duplicate ITEM_EN in map numeric")
if set(rmap) != set(nmap):
    errors.append("map numeric item set differs from canonical roster")

for name, r in rmap.items():
    n = nmap.get(name)
    if not n:
        continue
    if n["MAP_ITEM_ID"] != r["MAP_ITEM_ID"]:
        errors.append(f"{name}: MAP_ITEM_ID mismatch")
    if n["PROJECT_ERA"] != r["PROJECT_ERA"]:
        errors.append(f"{name}: era mismatch")
    if n["RECORD_KIND"] != r["RECORD_KIND"]:
        errors.append(f"{name}: record-kind mismatch")
    if n["NUMERIC_STATUS"] != "LOCKED_MAP_NUMERIC_V1":
        errors.append(f"{name}: numeric status not locked")

# Parse only the canonical resources block from YAML; support block and inline mapping forms.
catalog_text = RESOURCE_CATALOG.read_text(encoding="utf-8")
resource_block = catalog_text.split("\nresources:", 1)[1].split("\nexcluded:", 1)[0]
catalog_ids = set(
    re.findall(
        r"^\s*-\s*(?:id:\s*|\{id:\s*)([A-Z0-9_]+)",
        resource_block,
        flags=re.M,
    )
)
if len(catalog_ids) != 47:
    errors.append(f"resource catalog expected 47 IDs, got {len(catalog_ids)}")
if len(compat) != 47 or len(cmap) != 47:
    errors.append(f"resource compatibility expected 47 unique rows, got rows={len(compat)} unique={len(cmap)}")
if set(cmap) != catalog_ids:
    missing = sorted(catalog_ids - set(cmap))
    extra = sorted(set(cmap) - catalog_ids)
    errors.append(f"resource compatibility mismatch missing={missing} extra={extra}")

class_counts = {}
for r in compat:
    class_counts[r["RESOURCE_CLASS"]] = class_counts.get(r["RESOURCE_CLASS"], 0) + 1
if class_counts != {"strategic":7, "bonus":10, "luxury":30}:
    errors.append(f"resource class counts mismatch {class_counts}")

# Compatibility improvements must resolve to canonical map objects/rules.
for r in compat:
    names = [x.strip() for x in r["PRIMARY_IMPROVEMENT"].split("/") if x.strip()]
    for name in names:
        if name not in nmap:
            errors.append(f"{r['RESOURCE_ID']}: unknown primary improvement {name}")

# More Luxuries exact adopted mapping and resource yields.
EXPECTED_ML = {
    "COFFEE": ("Plantation",0,0,2),
    "TEA": ("Plantation",0,0,2),
    "TOBACCO": ("Plantation",0,0,2),
    "OLIVES": ("Plantation",1,0,1),
    "PERFUME": ("Plantation",0,0,2),
    "AMBER": ("Mine",0,0,2),
    "JADE": ("Mine",0,0,2),
    "LAPIS_LAZULI": ("Mine",0,0,2),
    "CORAL": ("Fishing Boats",0,0,2),
}
if len(morelux) != 9 or set(mlmap) != set(EXPECTED_ML):
    errors.append("More Luxuries rule set must contain exactly the 9 adopted resources")
for rid, (imp, food, prod, gold) in EXPECTED_ML.items():
    r = mlmap.get(rid)
    if not r:
        continue
    if r["PRIMARY_IMPROVEMENT"] != imp:
        errors.append(f"{rid}: More Luxuries improvement expected {imp}")
    if iv(r,"BASE_FOOD") != food or iv(r,"BASE_PRODUCTION") != prod or iv(r,"BASE_GOLD") != gold:
        errors.append(f"{rid}: More Luxuries base yield mismatch")
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"{rid}: More Luxuries rule not locked")
    if cmap[rid]["PRIMARY_IMPROVEMENT"] != imp:
        errors.append(f"{rid}: compatibility table conflicts with More Luxuries rule")

# Project-added staple/strategic mappings.
for rid, imp in {"MAIZE":"Farm","RICE":"Farm","NITER":"Mine"}.items():
    if cmap.get(rid,{}).get("PRIMARY_IMPROVEMENT") != imp:
        errors.append(f"{rid}: expected project improvement {imp}")

# Representative base map numeric locks.
CHECKS = {
    "Farm": {"BASE_FOOD":1,"BUILD_WORK":700},
    "Mine": {"BASE_PRODUCTION":1,"BUILD_WORK":700},
    "Quarry": {"BASE_PRODUCTION":1,"BUILD_WORK":800},
    "Lumber Mill": {"BASE_PRODUCTION":1,"BUILD_WORK":700},
    "Fort": {"DEFENSE_MODIFIER_PERCENT":50},
    "Road": {"ROUTE_MAINTENANCE_GOLD_PER_TILE":1,"BUILD_WORK":400},
    "Academy": {"BASE_SCIENCE":2,"PER_CITY_CAP":1},
    "Holy Site": {"BASE_FAITH":2,"PER_CITY_CAP":1},
    "Landmark": {"BASE_CULTURE":2,"PER_CITY_CAP":1},
    "Customs House": {"BASE_GOLD":2,"PER_CITY_CAP":1},
    "Manufactory": {"BASE_PRODUCTION":2,"PER_CITY_CAP":1},
    "Oil Well": {"BASE_PRODUCTION":3},
    "Offshore Oil Rig": {"BASE_PRODUCTION":3},
    "Airstrip": {"AIRCRAFT_SLOTS":3},
    "Wind Farm": {"BASE_PRODUCTION":1,"BASE_GOLD":1,"POWER_OUTPUT":2},
    "Solar Farm": {"BASE_PRODUCTION":1,"BASE_GOLD":1,"POWER_OUTPUT":2},
    "Geothermal Plant": {"BASE_PRODUCTION":2,"BASE_SCIENCE":1,"POWER_OUTPUT":4},
    "Offshore Wind Farm": {"BASE_PRODUCTION":1,"BASE_GOLD":1,"POWER_OUTPUT":2},
    "Seastead": {"BASE_FOOD":2},
}
for name, fields in CHECKS.items():
    n = nmap.get(name)
    if not n:
        errors.append(f"missing numeric map item {name}")
        continue
    for field, expected in fields.items():
        if iv(n,field) != expected:
            errors.append(f"{name}: {field} expected {expected}, got {n[field]}")

if nmap["Road"]["ROUTE_MP_COST"] != "0.5":
    errors.append("Road movement cost must be 0.5")
if nmap["Improved Road Movement"]["ROUTE_MP_COST"] != "0.333333":
    errors.append("Improved Road Movement must be approximately 1/3")
if nmap["Railroad"]["ROUTE_MP_COST"] != "0.1":
    errors.append("Railroad movement cost must be 0.1")
if iv(nmap["Railroad"],"ROUTE_MAINTENANCE_GOLD_PER_TILE") != 2:
    errors.append("Railroad maintenance must be 2 Gold/tile")
if "CAPITAL_CONNECTION_CITY_PRODUCTION_PERCENT=+25" not in nmap["Railroad"]["SPECIAL_EFFECTS"]:
    errors.append("Railroad capital connection +25% Production missing")

if iv(nmap["Fishing Boats"],"CONSUMES_BUILD_UNIT") != 1:
    errors.append("Fishing Boats must consume Work Boat in current system")

# GS effect-layer checks.
for name in ["Wind Farm","Solar Farm","Geothermal Plant","Offshore Wind Farm"]:
    if nmap[name]["SOURCE_GRADE"] != "CIV6_GS_EFFECT_EXACT_PROJECT_BUILD_WORK":
        errors.append(f"{name}: source-layer label must distinguish exact GS effect from project build work")

# Yield-upgrade rules.
if len(upgrades) != 23:
    errors.append(f"yield upgrade rows expected 23, got {len(upgrades)}")
for r in upgrades:
    if r["ITEM_EN"] not in nmap:
        errors.append(f"yield upgrade references unknown item {r['ITEM_EN']}")
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"yield upgrade not locked: {r['ITEM_EN']} / {r['UNLOCK']}")

required_upgrade_keys = {
    ("Farm","Irrigation","FOOD",1),
    ("Farm","Calendar","FOOD",1),
    ("Farm","Horse Collar","PRODUCTION",1),
    ("Farm","Fertilizer","FOOD",1),
    ("Pasture","Fertilizer","FOOD",1),
    ("Pasture","Replaceable Parts","PRODUCTION",1),
    ("Mine","Apprenticeship","PRODUCTION",1),
    ("Mine","Chemistry","PRODUCTION",1),
    ("Mine","Industrialization","PRODUCTION",1),
    ("Mine","Smart Materials","PRODUCTION",1),
    ("Fishing Boats","Compass","GOLD",1),
    ("Plantation","Fertilizer","FOOD",1),
    ("Quarry","Chemistry","PRODUCTION",1),
    ("Camp","Economics","GOLD",1),
    ("Lumber Mill","Machinery","PRODUCTION",1),
    ("Lumber Mill","Scientific Theory","PRODUCTION",1),
    ("Lumber Mill","Steam Power","PRODUCTION",1),
}
actual_upgrade_keys = {(r["ITEM_EN"],r["UNLOCK"],r["YIELD"],int(r["CHANGE"])) for r in upgrades}
for key in required_upgrade_keys:
    if key not in actual_upgrade_keys:
        errors.append(f"missing required yield upgrade {key}")

# Saltworks remains deliberately outside the canonical 39.
if "Saltworks" in nmap:
    errors.append("Saltworks must not silently enter V1 without a roster/gate decision")
if cmap.get("SALT",{}).get("PRIMARY_IMPROVEMENT") != "Mine":
    errors.append("Natural Salt must use Mine in V1")

print(f"map_roster_rows={len(roster)}")
print(f"map_numeric_rows={len(numeric)}")
print(f"resource_catalog_ids={len(catalog_ids)}")
print(f"resource_compat_rows={len(compat)}")
print(f"more_luxuries_rows={len(morelux)}")
print(f"yield_upgrade_rows={len(upgrades)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
