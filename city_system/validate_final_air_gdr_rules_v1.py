#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMERIC = ROOT / "city_system" / "FINAL_UNIT_NUMERIC_BALANCE_V1.csv"
ASSIGN = ROOT / "city_system" / "FINAL_UNIT_PROMOTION_PROFILE_ASSIGNMENT_V1.csv"
INNATE = ROOT / "city_system" / "FINAL_UNIT_INNATE_ABILITIES_V1.csv"
GDR = ROOT / "city_system" / "FINAL_GDR_MODULE_BALANCE_V1.csv"
AIR_UNITS = ROOT / "city_system" / "FINAL_AIR_INTERCEPTION_UNIT_RULES_V1.csv"
AIR_GLOBAL = ROOT / "city_system" / "FINAL_AIR_COMBAT_GLOBAL_RULES_V1.csv"

def read(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

numeric = read(NUMERIC)
assign = read(ASSIGN)
innate = read(INNATE)
gdr = read(GDR)
air_units = read(AIR_UNITS)
air_global = read(AIR_GLOBAL)

nmap = {r["UNIT_EN"]: r for r in numeric}
amap = {r["UNIT_EN"]: r for r in assign}
imap = {r["RULE_ID"]: r for r in innate}
air = {r["UNIT_EN"]: r for r in air_units}
gmods = {(r["TECH_GATE"], r["MODULE_EN"], r["EFFECT_TYPE"]): r for r in gdr}
grules = {r["RULE_ID"]: r for r in air_global}
errors = []

# GDR base numeric identity.
g = nmap.get("Giant Death Robot")
if not g:
    errors.append("Giant Death Robot missing from numeric table")
else:
    expected = {
        "COMBAT": "150",
        "RANGED_COMBAT": "100",
        "RANGE": "3",
        "MOVES": "5",
        "PRODUCTION_COST": "550",
        "STRATEGIC_RESOURCE": "Uranium",
        "RESOURCE_SLOT_COST": "1",
        "RESOURCE_UPKEEP_PER_TURN": "0",
    }
    for k, v in expected.items():
        if g.get(k) != v:
            errors.append(f"GDR {k}: expected {v}, got {g.get(k)}")

# GDR gets no ordinary promotions.
if amap.get("Giant Death Robot", {}).get("PROMOTION_PROFILE") != "NONE":
    errors.append("GDR must have promotion profile NONE")

for rid in ["INNATE_GDR_NO_XP", "INNATE_GDR_AMPHIBIOUS", "INNATE_GDR_FRIENDLY_HEAL"]:
    if rid not in imap:
        errors.append(f"missing GDR innate rule {rid}")

# Exact Future modules.
checks = {
    ("Advanced AI","Drone Air Defense","ANTI_AIR_DEFENSE_STRENGTH"): ("", "130"),
    ("Advanced Power Cells","Particle Beam Siege Cannon","CITY_RANGED_STRENGTH_BONUS"): ("100","130"),
    ("Advanced Power Cells","Particle Beam Siege Cannon","CITY_DEFENSE_EFFECTIVENESS_PERCENT"): ("","100"),
    ("Cybernetics","Enhanced Mobility","MOVES_CHANGE"): ("5","8"),
    ("Cybernetics","Enhanced Mobility","MOUNTAIN_JUMP"): ("","1"),
    ("Smart Materials","Reinforced Armor Plating","DEFENSE_STRENGTH_VS_LAND_NAVAL"): ("","10"),
}
for key, (base, final) in checks.items():
    r = gmods.get(key)
    if not r:
        errors.append(f"missing GDR module row {key}")
        continue
    if r["BASE_VALUE"] != base or r["FINAL_VALUE"] != final or r["STATUS"] != "LOCKED_V1":
        errors.append(f"bad GDR module values {key}")

# Air interception unit rules.
expected_air = {
    "Triplane": (50,2,1,150,1,6,0,-50,"LOCKED_V1"),
    "Fighter": (100,2,1,150,1,6,0,-50,"LOCKED_V1"),
    "Jet Fighter": (100,2,1,150,1,6,0,-50,"LOCKED_V1"),
    "Anti-Air Gun": (100,2,1,150,0,0,0,0,"LOCKED_V1"),
    "Mobile SAM": (100,2,1,150,0,0,0,0,"LOCKED_V1"),
    "Destroyer": (40,2,1,0,0,0,0,0,"LOCKED_V1"),
    "Missile Cruiser": (100,2,1,0,0,0,0,0,"LOCKED_V1"),
    "Stealth Bomber": (0,0,0,0,0,6,100,0,"LOCKED_V1"),
    "Guided Missile": (0,0,0,0,0,0,100,0,"LOCKED_V1"),
    "Giant Death Robot": (100,2,1,0,0,0,0,0,"CONDITIONAL_MODULE"),
}
for name, vals in expected_air.items():
    r = air.get(name)
    if not r:
        errors.append(f"missing air rule {name}")
        continue
    fields = [
        "INTERCEPTION_CHANCE_PERCENT","INTERCEPTION_RADIUS","BASE_INTERCEPTIONS_PER_TURN",
        "ANTI_AIR_BONUS_PERCENT","AIR_SWEEP_CAPABLE","AIR_RECON_RADIUS",
        "BASE_EVASION_PERCENT","NORMAL_AIR_STRIKE_MODIFIER_PERCENT"
    ]
    for field, value in zip(fields, vals[:-1]):
        if int(r[field]) != value:
            errors.append(f"{name} {field}: expected {value}, got {r[field]}")
    if r["STATUS"] != vals[-1]:
        errors.append(f"{name} status mismatch")

# Global air resolution must remain present.
required_global = {
    "AIR_INTERCEPT_ORDER",
    "AIR_SINGLE_INTERCEPTOR",
    "AIR_BASE_INTERCEPT_LIMIT",
    "AIR_INTERCEPTION_EXTRA_ACTION",
    "AIR_SWEEP_PURPOSE",
    "AIR_SWEEP_FIGHTER",
    "AIR_SWEEP_SURFACE",
    "AIR_EVASION_PROMOTION",
    "AIR_STEALTH_EVASION",
    "AIR_GUIDED_EVASION",
    "AIR_FIGHTER_WEAK_STRIKE",
    "AIR_FIGHTER_ANTI_AIR",
    "AIR_GROUND_AA_SPECIALTY",
    "AIR_RECON",
    "AIR_GDR_DRONE_DEFENSE",
}
missing = sorted(required_global - set(grules))
if missing:
    errors.append("missing global air rules: " + ", ".join(missing))

if grules.get("AIR_EVASION_PROMOTION", {}).get("VALUE") != "-50":
    errors.append("earned Evasion promotion must reduce interception damage by 50%")
if grules.get("AIR_STEALTH_EVASION", {}).get("VALUE") != "100":
    errors.append("Stealth Bomber base evasion must be 100")
if grules.get("AIR_GUIDED_EVASION", {}).get("VALUE") != "100":
    errors.append("Guided Missile base evasion must be 100")
if grules.get("AIR_GDR_DRONE_DEFENSE", {}).get("VALUE") != "130":
    errors.append("GDR Drone Air Defense strength must be 130")

print(f"gdr_module_rows={len(gdr)}")
print(f"air_unit_rule_rows={len(air_units)}")
print(f"air_global_rule_rows={len(air_global)}")
print(f"errors={len(errors)}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("PASS")
