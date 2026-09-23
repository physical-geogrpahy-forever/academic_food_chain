#!/usr/bin/env python3
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CITY = ROOT / "city_system"
HEALTH = ROOT / "health_system"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def as_float(value):
    return float(str(value).strip())


def fail(errors, message):
    errors.append(message)


def main():
    errors = []

    power_sources = read_csv(CITY / "POWER_SOURCE_BALANCE_V1.csv")
    bridge = read_csv(CITY / "POWER_POLLUTION_BRIDGE_V1.csv")
    health_rules = read_csv(HEALTH / "HEALTH_PLAGUE_NUMERIC_RULES_V1.csv")
    health_buildings = read_csv(HEALTH / "HEALTH_BUILDING_VALUES_V1.csv")
    upgrades = read_csv(CITY / "FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv")

    power_by_name = {r["SOURCE_NAME"]: r for r in power_sources}
    bridge_by_name = {r["POWER_SOURCE"]: r for r in bridge}
    rule_by_key = {r["KEY"]: r for r in health_rules}
    health_by_building = {r["BUILDING"]: r for r in health_buildings}

    # 1. Fuel-source bridge must preserve Power/resource ratios and emission ordering.
    aliases = {
        "Coal Power Plant": ("Coal Power Plant", "HEAVY"),
        "Oil-role Power Plant": ("Power Plant", "MODERATE"),
        "Nuclear Power Plant": ("Nuclear Power Plant", "MINUSCULE"),
    }
    co2 = {}
    divisor = as_float(rule_by_key["POLLUTION_HEALTH_PENALTY_DIVISOR"]["VALUE"])
    cap = as_float(rule_by_key["POLLUTION_HEALTH_PENALTY_CAP"]["VALUE"])

    for bridge_name, (source_name, expected_class) in aliases.items():
        if bridge_name not in bridge_by_name:
            fail(errors, f"missing pollution bridge row: {bridge_name}")
            continue
        if source_name not in power_by_name:
            fail(errors, f"missing power source row: {source_name}")
            continue
        b = bridge_by_name[bridge_name]
        p = power_by_name[source_name]
        if as_float(b["POWER_PER_RESOURCE_CAPACITY"]) != as_float(p["POWER_PER_SOURCE_OR_RESOURCE"]):
            fail(errors, f"power/resource mismatch: {bridge_name}")
        if p["EMISSION_CLASS"] != expected_class:
            fail(errors, f"emission class mismatch: {source_name}")
        co2[bridge_name] = as_float(b["GS_CO2_PER_POWER"])
        local = as_float(b["EXAMPLE_AT_4_POWER"])
        expected_health = max(cap, -math.floor(local / divisor))
        if as_float(b["HEALTH_EFFECT_AT_EXAMPLE"]) != expected_health:
            fail(errors, f"Health example mismatch: {bridge_name}")

    if not (co2.get("Coal Power Plant", 0) > co2.get("Oil-role Power Plant", 0) > co2.get("Nuclear Power Plant", 0) >= 0):
        fail(errors, "CO2 coefficients do not preserve Coal > Oil > Nuclear ordering")

    # 2. Zero-emission sources must remain zero in both Power and pollution bridge tables.
    zero_names = ["Solar Plant", "Solar Farm", "Wind Farm", "Offshore Wind Farm", "Geothermal Plant", "Hydroelectric Dam"]
    for name in zero_names:
        if name not in bridge_by_name or name not in power_by_name:
            fail(errors, f"missing zero-emission source: {name}")
            continue
        if as_float(bridge_by_name[name]["GS_CO2_PER_POWER"]) != 0 or as_float(bridge_by_name[name]["EXAMPLE_AT_4_POWER"]) != 0:
            fail(errors, f"nonzero pollution on renewable: {name}")
        if power_by_name[name]["EMISSION_CLASS"] != "ZERO":
            fail(errors, f"Power table emission class is not ZERO: {name}")

    # 3. Health building values: no duplicate direct industrial/transport penalties.
    expected_positive = {
        "Granary": 1,
        "Aqueduct": 2,
        "Apothecary": 2,
        "Cold Storage": 2,
        "Food Market": 1,
        "Hospital": 4,
        "Sewer": 4,
        "Medical Lab": 5,
        "Recycling Center": 2,
    }
    for name, value in expected_positive.items():
        row = health_by_building.get(name)
        if row is None:
            fail(errors, f"missing Health building row: {name}")
        elif as_float(row["HEALTH_VALUE"]) != value:
            fail(errors, f"Health value mismatch: {name}")

    expected_none = ["Factory", "Coal Power Plant", "Power Plant", "Airport", "Harbor", "Smokehouse", "Water Mill"]
    for name in expected_none:
        row = health_by_building.get(name)
        if row is None:
            fail(errors, f"missing non-direct Health row: {name}")
            continue
        if row["HEALTH_EFFECT_TYPE"] != "NONE" or as_float(row["HEALTH_VALUE"]) != 0:
            fail(errors, f"unexpected direct Health effect: {name}")

    # 4. Locked plague anchors.
    expected_rules = {
        "BASE_DURATION_STANDARD": 6,
        "MIN_DURATION": 3,
        "VIRULENT_CHANCE": 0.10,
        "VIRULENT_DURATION_MULT": 1.50,
        "POLLUTION_HEALTH_PENALTY_DIVISOR": 10,
        "POLLUTION_HEALTH_PENALTY_CAP": -5,
        "NETWORK_INTERNATIONAL_TRADE": 2.00,
    }
    for key, value in expected_rules.items():
        row = rule_by_key.get(key)
        if row is None:
            fail(errors, f"missing Health/Plague rule: {key}")
        elif as_float(row["VALUE"]) != value:
            fail(errors, f"Health/Plague rule mismatch: {key}")

    # 5. Upgrade graph/cost anchors.
    if len(upgrades) != 55:
        fail(errors, f"upgrade edge count is {len(upgrades)}, expected 55")
    equal_cost_expected = {
        ("Trebuchet", "Bombard"),
        ("Rifleman", "Infantry"),
        ("Landship", "Tank"),
    }
    equal_cost_actual = {
        (r["FROM_UNIT"], r["TO_UNIT"])
        for r in upgrades
        if as_float(r["PRODUCTION_DIFF"]) == 0 and as_float(r["FINAL_GOLD_COST"]) == 10
    }
    if equal_cost_actual != equal_cost_expected:
        fail(errors, f"equal-cost 10 Gold watch set mismatch: {sorted(equal_cost_actual)}")

    if errors:
        print("CROSS_SYSTEM_STATIC_QA: FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("CROSS_SYSTEM_STATIC_QA: PASS")
    print(f"power_sources={len(power_sources)} pollution_bridge={len(bridge)} health_buildings={len(health_buildings)} upgrade_edges={len(upgrades)}")
    print("watch=runtime_autoplay_required; static pass is not engine autoplay")
    return 0


if __name__ == "__main__":
    sys.exit(main())
