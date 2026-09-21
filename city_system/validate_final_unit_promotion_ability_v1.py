#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "city_system" / "FINAL_GENERIC_UNIT_ROSTER_V1.csv"
GRAPH = ROOT / "city_system" / "FINAL_UNIT_UPGRADE_GRAPH_V1.csv"
PROMOS = ROOT / "city_system" / "FINAL_UNIT_PROMOTION_SYSTEM_V1.csv"
ASSIGN = ROOT / "city_system" / "FINAL_UNIT_PROMOTION_PROFILE_ASSIGNMENT_V1.csv"
INNATE = ROOT / "city_system" / "FINAL_UNIT_INNATE_ABILITIES_V1.csv"
INHERIT = ROOT / "city_system" / "FINAL_UNIT_PROMOTION_INHERITANCE_V1.csv"

PROFILES = {
    "LAND_MELEE", "LAND_RANGED", "RECON", "NAVAL_MELEE",
    "NAVAL_RANGED", "NAVAL_RAIDER", "CARRIER",
    "AIR_FIGHTER", "AIR_BOMBER", "NONE"
}

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

roster = read(ROSTER)
graph = read(GRAPH)
promos = read(PROMOS)
assign = read(ASSIGN)
innate = read(INNATE)
inherit = read(INHERIT)

units = {r["UNIT_EN"]: r for r in roster}
edges = {
    (r["UNIT_EN"], dst.strip())
    for r in graph
    for dst in r["DIRECT_UPGRADE_TO"].split(";")
    if dst.strip()
}
errors = []

if len(roster) != 89:
    errors.append(f"expected 89 units, got {len(roster)}")
if len(assign) != 89:
    errors.append(f"expected 89 profile assignments, got {len(assign)}")
if len({r["UNIT_EN"] for r in assign}) != len(assign):
    errors.append("duplicate unit in profile assignment")
if {r["UNIT_EN"] for r in assign} != set(units):
    errors.append("profile assignment unit set differs from canonical roster")

for r in assign:
    if r["PROMOTION_PROFILE"] not in PROFILES:
        errors.append(f"{r['UNIT_EN']}: unknown profile {r['PROMOTION_PROFILE']}")
    if r["ROLE_FAMILY"] != units[r["UNIT_EN"]]["ROLE_FAMILY"]:
        errors.append(f"{r['UNIT_EN']}: role mismatch")
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"{r['UNIT_EN']}: assignment not locked")

# Intentional profile decisions.
amap = {r["UNIT_EN"]: r["PROMOTION_PROFILE"] for r in assign}
expected_profiles = {
    "Privateer": "NAVAL_MELEE",
    "Submarine": "NAVAL_RAIDER",
    "Nuclear Submarine": "NAVAL_RAIDER",
    "Aircraft Carrier": "CARRIER",
    "Triplane": "AIR_FIGHTER",
    "Fighter": "AIR_FIGHTER",
    "Jet Fighter": "AIR_FIGHTER",
    "Great War Bomber": "AIR_BOMBER",
    "Bomber": "AIR_BOMBER",
    "Stealth Bomber": "AIR_BOMBER",
    "Scout": "RECON",
    "Explorer": "RECON",
    "Ranger": "RECON",
    "Spec Ops": "RECON",
    "Guided Missile": "NONE",
}
for name, profile in expected_profiles.items():
    if amap.get(name) != profile:
        errors.append(f"{name}: expected profile {profile}, got {amap.get(name)}")

# Promotion definitions.
promo_ids = [r["PROMOTION_ID"] for r in promos]
if len(set(promo_ids)) != len(promo_ids):
    errors.append("duplicate PROMOTION_ID")
if not promos:
    errors.append("promotion table empty")
for r in promos:
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"{r['PROMOTION_ID']}: promotion not locked")
    if not r["PROMOTION_EN"] or not r["PROFILE"] or not r["EFFECT_TYPE"]:
        errors.append(f"{r['PROMOTION_ID']}: incomplete promotion definition")

required_promotions = {
    "PROMO_SHOCK_1", "PROMO_SHOCK_2", "PROMO_SHOCK_3",
    "PROMO_DRILL_1", "PROMO_DRILL_2", "PROMO_DRILL_3",
    "PROMO_ACCURACY_1", "PROMO_ACCURACY_2", "PROMO_ACCURACY_3",
    "PROMO_BARRAGE_1", "PROMO_BARRAGE_2", "PROMO_BARRAGE_3",
    "PROMO_SCOUTING_1", "PROMO_SURVIVALISM_1",
    "PROMO_COASTAL_RAIDER_1", "PROMO_BOARDING_1",
    "PROMO_TARGETING_1", "PROMO_BOMBARDMENT_1",
    "PROMO_WOLFPACK_1", "PROMO_FLIGHT_DECK_1",
    "PROMO_INTERCEPTION_1", "PROMO_DOGFIGHTING_1",
    "PROMO_AIR_SIEGE_1", "PROMO_AIR_BOMBARD_1",
    "PROMO_LOGISTICS_LAND", "PROMO_RANGE_LAND",
}
missing_promos = sorted(required_promotions - set(promo_ids))
if missing_promos:
    errors.append("missing required promotions: " + ", ".join(missing_promos))

# Innate target validation.
role_names = {r["ROLE_FAMILY"] for r in roster}
innate_ids = [r["RULE_ID"] for r in innate]
if len(set(innate_ids)) != len(innate_ids):
    errors.append("duplicate innate RULE_ID")
for r in innate:
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"{r['RULE_ID']}: innate rule not locked")
    if r["TARGET_TYPE"] == "UNIT":
        if r["TARGET"] not in units:
            errors.append(f"{r['RULE_ID']}: unknown target unit {r['TARGET']}")
    elif r["TARGET_TYPE"] == "UNIT_LIST":
        for x in [x.strip() for x in r["TARGET"].split(";") if x.strip()]:
            if x not in units:
                errors.append(f"{r['RULE_ID']}: unknown target unit {x}")
    elif r["TARGET_TYPE"] == "ROLE":
        if r["TARGET"] not in role_names:
            errors.append(f"{r['RULE_ID']}: unknown target role {r['TARGET']}")
    elif r["TARGET_TYPE"] == "ROLE_LIST":
        for x in [x.strip() for x in r["TARGET"].split(";") if x.strip()]:
            if x not in role_names:
                errors.append(f"{r['RULE_ID']}: unknown target role {x}")
    else:
        errors.append(f"{r['RULE_ID']}: invalid TARGET_TYPE {r['TARGET_TYPE']}")

required_innate = {
    "INNATE_ANTI_CAV_50",
    "INNATE_ANTI_ARMOR_100",
    "INNATE_SIEGE_CITY",
    "INNATE_SIEGE_SETUP",
    "INNATE_ARTILLERY_INDIRECT",
    "INNATE_ROCKET_NO_SETUP",
    "INNATE_PRIVATEER_PRIZE",
    "INNATE_SUB_STEALTH",
    "INNATE_ASW_DETECT",
    "INNATE_MEDIC_HEAL",
    "INNATE_SUPPLY_HEAL",
    "INNATE_SUPPLY_MOVE",
    "INNATE_BALLOON_RANGE",
    "INNATE_DRONE_RANGE",
    "INNATE_DRONE_STRENGTH",
    "INNATE_GDR_MODULE_AI",
    "INNATE_GDR_MODULE_POWER",
    "INNATE_GDR_MODULE_CYBER",
    "INNATE_GDR_MODULE_MATERIAL",
}
missing_innate = sorted(required_innate - set(innate_ids))
if missing_innate:
    errors.append("missing required innate rules: " + ", ".join(missing_innate))

# Promotion inheritance references must point to real upgrade edges, except DEFAULT.
for r in inherit:
    if r["STATUS"] != "LOCKED_V1":
        errors.append("inheritance rule not locked")
    if r["FROM_UNIT"] == "DEFAULT":
        continue
    pair = (r["FROM_UNIT"], r["TO_UNIT"])
    if pair not in edges:
        errors.append(f"inheritance rule references non-upgrade edge {pair[0]} -> {pair[1]}")

# Locked conversion checks.
def has_rule(src, dst, rule, source_promo=None, target_promo=None):
    for r in inherit:
        if r["FROM_UNIT"] == src and r["TO_UNIT"] == dst and r["INHERITANCE_RULE"] == rule:
            if source_promo is not None and r["SOURCE_PROMOTION"] != source_promo:
                continue
            if target_promo is not None and r["TARGET_PROMOTION"] != target_promo:
                continue
            return True
    return False

for a, b in [
    ("Accuracy I","Shock I"),("Accuracy II","Shock II"),("Accuracy III","Shock III"),
    ("Barrage I","Drill I"),("Barrage II","Drill II"),("Barrage III","Drill III"),
    ("Logistics","Blitz"),("Range","Mobility")
]:
    if not has_rule("Chariot Archer","Knight","CONVERT",a,b):
        errors.append(f"missing Chariot Archer conversion {a} -> {b}")

if not has_rule("Privateer","Submarine","CONVERT_HIGHEST_RANK"):
    errors.append("missing Privateer -> Submarine rank conversion")
if not has_rule("Privateer","Submarine","DROP_INNATE","Prize Ships",""):
    errors.append("Prize Ships must be dropped on Privateer -> Submarine")

print(f"roster_units={len(roster)}")
print(f"profile_assignments={len(assign)}")
print(f"promotion_definitions={len(promos)}")
print(f"innate_rules={len(innate)}")
print(f"inheritance_rules={len(inherit)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
