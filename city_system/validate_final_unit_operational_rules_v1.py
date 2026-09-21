#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMERIC = ROOT / "city_system" / "FINAL_UNIT_NUMERIC_BALANCE_V1.csv"
CARGO = ROOT / "city_system" / "FINAL_UNIT_CARGO_BASING_RULES_V1.csv"
PRIZE = ROOT / "city_system" / "FINAL_PRIVATEER_PRIZE_SHIPS_V1.csv"
SUPPORT = ROOT / "city_system" / "FINAL_SUPPORT_UNIT_OPERATION_RULES_V1.csv"
XP = ROOT / "city_system" / "FINAL_UNIT_XP_PROGRESSION_V1.csv"

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

numeric = {r["UNIT_EN"]: r for r in read(NUMERIC)}
cargo = read(CARGO)
prize = read(PRIZE)
support = read(SUPPORT)
xp = read(XP)
errors = []

# Cargo values must agree with numeric table.
if numeric["Aircraft Carrier"]["CARGO_CAPACITY"] != "2":
    errors.append("Aircraft Carrier numeric cargo must be 2")
if numeric["Nuclear Submarine"]["CARGO_CAPACITY"] != "2":
    errors.append("Nuclear Submarine numeric cargo must be 2")
if numeric["Missile Cruiser"]["CARGO_CAPACITY"] != "3":
    errors.append("Missile Cruiser numeric cargo must be 3")

cmap = {(r["BASE_TYPE"], r["BASE_EN"]): r for r in cargo}
required_cargo = {
    ("CITY","City Air Base"): "6",
    ("UNIT","Aircraft Carrier"): "2",
    ("UNIT","Nuclear Submarine"): "2",
    ("UNIT","Missile Cruiser"): "3",
}
for key, cap in required_cargo.items():
    r = cmap.get(key)
    if not r:
        errors.append(f"missing cargo row {key}")
        continue
    if r["BASE_CAPACITY"] != cap or r["STATUS"] != "LOCKED_V1":
        errors.append(f"bad cargo capacity/status {key}")

carrier = cmap[("UNIT","Aircraft Carrier")]
eligible = {x.strip() for x in carrier["ELIGIBLE_CARGO"].split(";") if x.strip()}
excluded = {x.strip() for x in carrier["EXCLUDED_CARGO"].split(";") if x.strip()}
expected_eligible = {"Triplane","Fighter","Jet Fighter","Great War Bomber","Bomber"}
if eligible != expected_eligible:
    errors.append(f"carrier eligible cargo mismatch {sorted(eligible)}")
if {"Stealth Bomber","Guided Missile"} - excluded:
    errors.append("carrier must exclude Stealth Bomber and Guided Missile")

for base in ["Nuclear Submarine","Missile Cruiser"]:
    r = cmap[("UNIT",base)]
    if {x.strip() for x in r["ELIGIBLE_CARGO"].split(";") if x.strip()} != {"Guided Missile"}:
        errors.append(f"{base} must carry Guided Missile only in current unit roster")

# Prize Ships exact formula constants.
if len(prize) != 1:
    errors.append(f"Prize Ships rows expected 1, got {len(prize)}")
else:
    r = prize[0]
    if r["SOURCE_UNIT"] != "Privateer":
        errors.append("Prize Ships source unit must be Privateer")
    if r["MIN_CHANCE_PERCENT"] != "10":
        errors.append("Prize Ships minimum chance must be 10")
    if r["MAX_CHANCE_PERCENT"] != "80":
        errors.append("Prize Ships maximum chance must be 80")
    if r["RATIO_MULTIPLIER"] != "40":
        errors.append("Prize Ships ratio multiplier must be 40")
    if r["CAPTURED_HP"] != "50":
        errors.append("Prize Ships captured HP must be 50")
    if r["CAPTURED_PROMOTIONS"] != "NONE":
        errors.append("Prize Ships captured promotions must be NONE")

# Support rules.
required_support = {
    ("Medic","HEAL_AURA"): ("20","1","TAKE_HIGHEST_ONLY"),
    ("Supply Convoy","HEAL_AURA"): ("20","1","TAKE_HIGHEST_ONLY"),
    ("Supply Convoy","MOVEMENT_AURA"): ("1","1","TAKE_HIGHEST_ONLY"),
    ("Observation Balloon","SIEGE_RANGE_AURA"): ("1","1","TAKE_HIGHEST_ONLY"),
    ("Drone","SIEGE_RANGE_AURA"): ("1","1","TAKE_HIGHEST_ONLY"),
    ("Drone","SIEGE_STRENGTH_AURA"): ("5","1","TAKE_HIGHEST_ONLY"),
}
smap = {(r["SUPPORT_UNIT"], r["AURA_CATEGORY"]): r for r in support}
for key, (value, radius, stacking) in required_support.items():
    r = smap.get(key)
    if not r:
        errors.append(f"missing support rule {key}")
        continue
    if r["AURA_VALUE"] != value or r["RADIUS"] != radius or r["STACKING_RULE"] != stacking:
        errors.append(f"bad support rule {key}")

# All aura support units use one support slot rule.
for r in support:
    if r["FORMATION_CLASS"] != "SUPPORT":
        errors.append(f"{r['SUPPORT_UNIT']}: formation class must be SUPPORT")
    if r["STATUS"] != "LOCKED_V1":
        errors.append(f"{r['SUPPORT_UNIT']}: support rule not locked")

# XP thresholds and gains.
xmap = {r["RULE_ID"]: r for r in xp}
thresholds = {
    "XP_LEVEL_2":"10","XP_LEVEL_3":"30","XP_LEVEL_4":"60","XP_LEVEL_5":"100",
    "XP_LEVEL_6":"150","XP_LEVEL_7":"210","XP_LEVEL_8":"280","XP_LEVEL_9":"360","XP_LEVEL_10":"450",
}
for rid, value in thresholds.items():
    if xmap.get(rid, {}).get("VALUE") != value:
        errors.append(f"{rid} expected {value}")

gains = {
    "XP_MELEE_ATTACK":"5","XP_MELEE_DEFEND":"4","XP_RANGED_ATTACK":"2","XP_RANGED_DEFEND":"2",
    "XP_AIR_ATTACK":"4","XP_AIR_DEFEND":"2","XP_AIR_SWEEP_ATTACK":"5",
    "XP_AIR_SWEEP_DEFEND_AIR":"5","XP_AIR_SWEEP_DEFEND_GROUND":"2",
    "XP_CITY_MELEE_ATTACK":"5","XP_CITY_RANGED_ATTACK":"3","XP_CITY_AIR_ATTACK":"4",
}
for rid, value in gains.items():
    if xmap.get(rid, {}).get("VALUE") != value:
        errors.append(f"{rid} expected {value}")

if xmap.get("XP_BARBARIAN_CAP", {}).get("VALUE") != "30":
    errors.append("Barbarian XP cap must be 30")
if xmap.get("XP_LEVEL_REWARD", {}).get("VALUE") != "PROMOTION_OR_HEAL_50_HP":
    errors.append("level reward must be promotion or heal 50 HP")

print(f"cargo_rows={len(cargo)}")
print(f"prize_rows={len(prize)}")
print(f"support_rows={len(support)}")
print(f"xp_rows={len(xp)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
