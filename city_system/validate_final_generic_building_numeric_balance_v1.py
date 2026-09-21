#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "city_system" / "FINAL_GENERIC_BUILDING_ROSTER_V1.csv"
NUMERIC = ROOT / "city_system" / "FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv"

ERA = {
    "Ancient": 1,
    "Classical": 2,
    "Late Antiquity": 3,
    "Early Medieval": 4,
    "High Medieval": 5,
    "High Medieval/Exploration": 5.5,
    "Renaissance": 6,
    "Exploration": 7,
    "Enlightenment": 8,
    "Industrial": 9,
    "Modern": 10,
    "Atomic": 11,
    "Information": 12,
    "Future": 13,
}

VALID_GRADES = {
    "A_CIV5_BNW_EXACT",
    "B_CIV5_FUNCTIONAL_REMAP",
    "B_CIV6_ADAPTED",
    "B_EE_ADAPTED",
    "B_PROJECT_INTERPOLATED",
}

VALID_GW_TYPES = {"", "ANY", "Writing", "Art", "Artifact", "Music", "Film"}

NUMERIC_FIELDS = [
    "PRODUCTION_COST","GOLD_MAINTENANCE",
    "FOOD_FLAT","PRODUCTION_FLAT","GOLD_FLAT","SCIENCE_FLAT","CULTURE_FLAT","FAITH_FLAT",
    "LOCAL_HAPPINESS","CITY_DEFENSE_STRENGTH","CITY_HP","FOOD_CARRYOVER_PERCENT",
    "PRODUCTION_PERCENT","BUILDING_PRODUCTION_PERCENT","GOLD_PERCENT","SCIENCE_PERCENT","CULTURE_PERCENT",
    "UNIT_XP_BONUS","SPECIALIST_SLOTS","FLAT_GPP","GREAT_WORK_SLOTS","AIR_CAPACITY_CHANGE",
]

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def iv(row, field):
    return int(float(row[field]))

roster = read(ROSTER)
numeric = read(NUMERIC)
rmap = {r["BUILDING_EN"]: r for r in roster}
nmap = {r["BUILDING_EN"]: r for r in numeric}
errors = []

if len(roster) != 102:
    errors.append(f"roster rows expected 102, got {len(roster)}")
if len(numeric) != 102:
    errors.append(f"numeric rows expected 102, got {len(numeric)}")
if len(rmap) != len(roster):
    errors.append("duplicate building name in roster")
if len(nmap) != len(numeric):
    errors.append("duplicate building name in numeric table")
if set(rmap) != set(nmap):
    errors.append("numeric building set differs from canonical roster")

for name, r in rmap.items():
    n = nmap.get(name)
    if not n:
        continue
    if n["PROJECT_ERA"] != r["PROJECT_ERA"]:
        errors.append(f"{name}: era mismatch")
    if n["CHAIN"] != r["CHAIN"]:
        errors.append(f"{name}: chain mismatch")
    if n["NUMERIC_STATUS"] not in {"LOCKED_BUILDING_V1", "MOD_SOURCE_REAUDIT_REQUIRED"}:
        errors.append(f"{name}: invalid numeric status {n['NUMERIC_STATUS']}")
    if n["SOURCE_GRADE"] not in VALID_GRADES:
        errors.append(f"{name}: invalid source grade {n['SOURCE_GRADE']}")
    for field in NUMERIC_FIELDS:
        try:
            v = iv(n, field)
        except Exception:
            errors.append(f"{name}: nonnumeric {field}={n[field]}")
            continue
        if field != "AIR_CAPACITY_CHANGE" and v < 0:
            errors.append(f"{name}: negative {field}")

    if name == "Palace":
        if iv(n, "PRODUCTION_COST") != 0:
            errors.append("Palace cost must be 0/automatic")
    elif iv(n, "PRODUCTION_COST") <= 0:
        errors.append(f"{name}: production cost must be positive")

    if n["GREAT_WORK_TYPE"] not in VALID_GW_TYPES:
        errors.append(f"{name}: invalid Great Work type {n['GREAT_WORK_TYPE']}")
    if iv(n, "GREAT_WORK_SLOTS") > 0 and not n["GREAT_WORK_TYPE"]:
        errors.append(f"{name}: Great Work slots without type")
    if iv(n, "GREAT_WORK_SLOTS") == 0 and n["GREAT_WORK_TYPE"]:
        errors.append(f"{name}: Great Work type without slots")

    if iv(n, "SPECIALIST_SLOTS") > 0 and not n["SPECIALIST_TYPE"]:
        errors.append(f"{name}: specialist slots without type")
    if iv(n, "SPECIALIST_SLOTS") == 0 and n["SPECIALIST_TYPE"]:
        errors.append(f"{name}: specialist type without slots")
    if iv(n, "FLAT_GPP") > 0 and not n["GPP_TYPE"]:
        errors.append(f"{name}: flat GPP without GPP type")
    if iv(n, "FLAT_GPP") == 0 and n["GPP_TYPE"]:
        errors.append(f"{name}: GPP type without flat GPP")

# Building prerequisite chronology.
for name, r in rmap.items():
    prereq = r["PREREQUISITE"].strip()
    if not prereq or prereq not in rmap:
        continue
    if ERA[rmap[prereq]["PROJECT_ERA"]] > ERA[r["PROJECT_ERA"]]:
        errors.append(
            f"prerequisite era regression: {name}({r['PROJECT_ERA']}) <- "
            f"{prereq}({rmap[prereq]['PROJECT_ERA']})"
        )

# Hard-lock representative Civ V anchors.
ANCHORS = {
    "Palace": {"PRODUCTION_COST":0,"PRODUCTION_FLAT":3,"GOLD_FLAT":3,"SCIENCE_FLAT":3,"CULTURE_FLAT":1,"CITY_DEFENSE_STRENGTH":2,"GREAT_WORK_SLOTS":1},
    "Walls": {"PRODUCTION_COST":75,"CITY_DEFENSE_STRENGTH":5,"CITY_HP":50},
    "Monument": {"PRODUCTION_COST":40,"GOLD_MAINTENANCE":1,"CULTURE_FLAT":2},
    "Granary": {"PRODUCTION_COST":60,"GOLD_MAINTENANCE":1,"FOOD_FLAT":2},
    "Water Mill": {"PRODUCTION_COST":75,"GOLD_MAINTENANCE":2,"FOOD_FLAT":2,"PRODUCTION_FLAT":1},
    "Barracks": {"PRODUCTION_COST":75,"GOLD_MAINTENANCE":1,"UNIT_XP_BONUS":15},
    "Shrine": {"PRODUCTION_COST":40,"GOLD_MAINTENANCE":1,"FAITH_FLAT":1},
    "Library": {"PRODUCTION_COST":75,"GOLD_MAINTENANCE":1},
    "Market": {"PRODUCTION_COST":100,"GOLD_MAINTENANCE":0,"GOLD_FLAT":1,"GOLD_PERCENT":25,"SPECIALIST_SLOTS":1},
    "Amphitheater": {"PRODUCTION_COST":100,"GOLD_MAINTENANCE":2,"CULTURE_FLAT":1,"GREAT_WORK_SLOTS":1},
    "Aqueduct": {"PRODUCTION_COST":100,"GOLD_MAINTENANCE":1,"FOOD_CARRYOVER_PERCENT":40},
    "Armory": {"PRODUCTION_COST":160,"GOLD_MAINTENANCE":1,"UNIT_XP_BONUS":15},
    "Castle": {"PRODUCTION_COST":160,"CITY_DEFENSE_STRENGTH":7,"CITY_HP":25},
    "Workshop": {"PRODUCTION_COST":120,"GOLD_MAINTENANCE":2,"PRODUCTION_FLAT":2,"PRODUCTION_PERCENT":10,"SPECIALIST_SLOTS":1},
    "University": {"PRODUCTION_COST":160,"GOLD_MAINTENANCE":2,"SCIENCE_PERCENT":33,"SPECIALIST_SLOTS":2},
    "Bank": {"PRODUCTION_COST":200,"GOLD_FLAT":2,"GOLD_PERCENT":25,"SPECIALIST_SLOTS":1},
    "Windmill": {"PRODUCTION_COST":250,"GOLD_MAINTENANCE":2,"PRODUCTION_FLAT":2,"BUILDING_PRODUCTION_PERCENT":10,"SPECIALIST_SLOTS":1},
    "Constabulary": {"PRODUCTION_COST":160,"GOLD_MAINTENANCE":1},
    "Arsenal": {"PRODUCTION_COST":300,"CITY_DEFENSE_STRENGTH":9,"CITY_HP":25},
    "Opera House": {"PRODUCTION_COST":200,"GOLD_MAINTENANCE":1,"CULTURE_FLAT":1,"GREAT_WORK_SLOTS":1},
    "Seaport": {"PRODUCTION_COST":250,"GOLD_MAINTENANCE":2},
    "Observatory": {"PRODUCTION_COST":200,"GOLD_MAINTENANCE":0,"SCIENCE_PERCENT":50},
    "Stock Exchange": {"PRODUCTION_COST":300,"GOLD_FLAT":3,"GOLD_PERCENT":25,"SPECIALIST_SLOTS":2},
    "Zoo": {"PRODUCTION_COST":200,"GOLD_MAINTENANCE":2,"LOCAL_HAPPINESS":2},
    "Military Academy": {"PRODUCTION_COST":300,"GOLD_MAINTENANCE":1,"UNIT_XP_BONUS":15},
    "Public School": {"PRODUCTION_COST":300,"GOLD_MAINTENANCE":3,"SCIENCE_FLAT":3,"SPECIALIST_SLOTS":1},
    "Factory": {"PRODUCTION_COST":360,"GOLD_MAINTENANCE":3,"PRODUCTION_FLAT":4,"PRODUCTION_PERCENT":10,"SPECIALIST_SLOTS":2},
    "Hospital": {"PRODUCTION_COST":360,"GOLD_MAINTENANCE":2,"FOOD_FLAT":5},
    "Military Base": {"PRODUCTION_COST":500,"CITY_DEFENSE_STRENGTH":12,"CITY_HP":25},
    "Airport": {"PRODUCTION_COST":400,"GOLD_MAINTENANCE":5},
    "Stadium": {"PRODUCTION_COST":500,"GOLD_MAINTENANCE":2,"LOCAL_HAPPINESS":2},
    "Medical Lab": {"PRODUCTION_COST":500,"GOLD_MAINTENANCE":3,"FOOD_CARRYOVER_PERCENT":25},
    "Research Lab": {"PRODUCTION_COST":500,"GOLD_MAINTENANCE":3,"SCIENCE_FLAT":4,"SCIENCE_PERCENT":50,"SPECIALIST_SLOTS":1},
    "Solar Plant": {"PRODUCTION_COST":500,"GOLD_MAINTENANCE":3,"PRODUCTION_FLAT":5,"PRODUCTION_PERCENT":15},
}
for name, fields in ANCHORS.items():
    n = nmap.get(name)
    if not n:
        errors.append(f"missing anchor building {name}")
        continue
    for field, expected in fields.items():
        actual = iv(n, field)
        if actual != expected:
            errors.append(f"{name}: anchor {field} expected {expected}, got {actual}")

# Guild progression.
for name, stype, slots, gtype, gpp in [
    ("Writers' Guild","Writer",2,"Great Writer",1),
    ("Artists' Guild","Artist",2,"Great Artist",2),
    ("Musicians' Guild","Musician",2,"Great Musician",3),
    ("Director's Guild","Director",2,"Great Director",3),
]:
    n=nmap[name]
    if (n["SPECIALIST_TYPE"],iv(n,"SPECIALIST_SLOTS"),n["GPP_TYPE"],iv(n,"FLAT_GPP")) != (stype,slots,gtype,gpp):
        errors.append(f"{name}: guild specialist/GPP mismatch")

# Government building adaptation locks.
checks = {
    "Ancestral Hall": ["FOUNDING_UNIT_PRODUCTION_PERCENT=+50", "NO_FREE_WORKER=1"],
    "Audience Chamber": ["GOVERNOR_EFFECT_REMOVED=1"],
    "Foreign Ministry": ["CITY_STATE_LEVY_GOLD_COST_PERCENT=-50", "LEVIED_CITY_STATE_UNIT_COMBAT=+4"],
    "Grand Master's Chapel": ["BUY_LAND_MILITARY_UNITS_WITH_FAITH=1"],
    "Intelligence Agency": ["SPY_CAPACITY=+1"],
    "Royal Society": ["WORKER_CHARGE_CONSUMPTION_REMOVED=1"],
    "War Department": ["ON_KILL_HEAL_HP=20"],
}
for name, tokens in checks.items():
    effect=nmap[name]["SPECIAL_EFFECTS"]
    for token in tokens:
        if token not in effect:
            errors.append(f"{name}: missing locked adaptation {token}")

if "FREE_WORKER" in nmap["Ancestral Hall"]["SPECIAL_EFFECTS"] and "NO_FREE_WORKER=1" not in nmap["Ancestral Hall"]["SPECIAL_EFFECTS"]:
    errors.append("Ancestral Hall illegally reintroduces free Worker")
if iv(nmap["Grand Master's Chapel"],"FAITH_FLAT") != 0:
    errors.append("Grand Master's Chapel must not invent flat Faith")
if iv(nmap["National History Museum"],"GREAT_WORK_SLOTS") != 4 or nmap["National History Museum"]["GREAT_WORK_TYPE"] != "ANY":
    errors.append("National History Museum must have 4 ANY Great Work slots")

# Power replacement semantics.
for name in ["Coal Power Plant","Nuclear Power Plant","Solar Plant"]:
    if "REPLACES_POWER_PLANT_OUTPUT=1" not in nmap[name]["SPECIAL_EFFECTS"]:
        errors.append(f"{name}: missing power-plant replacement semantics")

# Adopted Enlightenment Era effects must not regress to generic interpolation.
cloth=nmap["Cloth Mill"]
if iv(cloth,"PRODUCTION_FLAT") != 1 or iv(cloth,"PRODUCTION_PERCENT") != 10 or "WORKED_COTTON_SHEEP_SILK_GOLD=+2" not in cloth["SPECIAL_EFFECTS"]:
    errors.append("Cloth Mill must retain Pouakai Enlightenment Era effect")
gunsmith=nmap["Gunsmith"]
if iv(gunsmith,"PRODUCTION_FLAT") != 0 or "GUNPOWDER_INFANTRY_PRODUCTION_PERCENT=+25" not in gunsmith["SPECIAL_EFFECTS"]:
    errors.append("Gunsmith must retain Pouakai Enlightenment Era effect")
drydock=nmap["Drydock"]
if "NAVAL_UNIT_TRAINED_COMBAT_STRENGTH_PERCENT=+15" not in drydock["SPECIAL_EFFECTS"]:
    errors.append("Drydock must retain Pouakai Enlightenment Era effect")

# Exact Art Museum chronology correction.
if rmap["Art Museum"]["PROJECT_ERA"] != "Exploration":
    errors.append("Art Museum must be Exploration after prerequisite correction")
if rmap["Art Museum"]["PREREQUISITE"] != "Opera House":
    errors.append("Art Museum prerequisite must remain Opera House")

grade_counts={}
for n in numeric:
    grade_counts[n["SOURCE_GRADE"]]=grade_counts.get(n["SOURCE_GRADE"],0)+1

print(f"roster_rows={len(roster)}")
print(f"numeric_rows={len(numeric)}")
print(f"locked_rows={sum(r['NUMERIC_STATUS']=='LOCKED_BUILDING_V1' for r in numeric)}")
print(f"mod_reaudit_rows={sum(r['NUMERIC_STATUS']=='MOD_SOURCE_REAUDIT_REQUIRED' for r in numeric)}")
print("source_grades="+str(grade_counts))
print(f"errors={len(errors)}")
if errors:
    print("FAIL")
    for e in errors:
        print(" -",e)
    raise SystemExit(1)
print("PASS")
