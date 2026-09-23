from __future__ import annotations

import argparse
import csv
from pathlib import Path

BASE = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv")
V3 = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv")
POWER = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv")
HEALTH = Path("health_system/HEALTH_BUILDING_VALUES_V1.csv")
OUT = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv")

EXTRA_FIELDS = [
    "POWER_LOAD",
    "POWERED_BONUS",
    "POWER_SOURCE_RULE",
    "HEALTH_EFFECT_TYPE",
    "HEALTH_POINTS_FINAL",
    "SPONTANEOUS_PLAGUE_RISK_MULT",
    "PLAGUE_DURATION_MOD_TURNS",
    "HEALTH_OTHER_EFFECT",
    "STABILITY_POINTS_FINAL",
    "FINAL_MERGE_STATUS",
    "FINAL_MERGE_SOURCES",
]

HAPPINESS_ZERO_DEFAULT_FIELDS = [
    "LOCAL_HAPPINESS",
    "VP_DISTRESS_REDUCTION",
    "VP_POVERTY_REDUCTION",
    "VP_ILLITERACY_REDUCTION",
    "VP_BOREDOM_REDUCTION",
    "VP_RELIGIOUS_UNREST_REDUCTION",
]

V3_TO_BASE = {
    "PROJECT_ERA": "PROJECT_ERA",
    "CHAIN": "CHAIN",
    "PRODUCTION_COST": "PRODUCTION_COST",
    "GOLD_MAINTENANCE": "GOLD_MAINTENANCE",
    "FOOD_FLAT": "FOOD_FLAT",
    "PRODUCTION_FLAT": "PRODUCTION_FLAT",
    "GOLD_FLAT": "GOLD_FLAT",
    "SCIENCE_FLAT": "SCIENCE_FLAT",
    "CULTURE_FLAT": "CULTURE_FLAT",
    "FAITH_FLAT": "FAITH_FLAT",
    "SPECIALIST_TYPE": "SPECIALIST_TYPE",
    "SPECIALIST_SLOTS": "SPECIALIST_SLOTS",
    "SPECIAL_EFFECTS": "SPECIAL_EFFECTS",
    "NUMERIC_STATUS": "NUMERIC_STATUS",
    "VP_AUDIT_STATUS": "VP_AUDIT_STATUS",
    "RATIONALE": "VP_AUDIT_REASON",
}

STALE_MARKER_REPLACEMENTS = {
    "HEALTH_SYSTEM_EFFECT=PENDING": "HEALTH_SYSTEM_EFFECT=HEALTH_V1",
    "POWER_SYSTEM_OUTPUT=PENDING": "POWER_SYSTEM_OUTPUT=POWER_V4",
    "POWERED_BONUS_HANDLED_BY_POWER_SYSTEM_PENDING": "POWERED_BONUS_HANDLED_BY_POWER_SYSTEM=POWER_V4",
    "POLLUTION_SYSTEM_EFFECT=PENDING": "POLLUTION_SYSTEM_EFFECT=POWER_POLLUTION_BRIDGE_V1",
}


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def as_int_text(value):
    s = str(value).strip()
    if not s:
        return ""
    return str(int(float(s)))


def blank_row(fieldnames):
    return {k: "" for k in fieldnames}


def init_system_defaults(row):
    row["POWER_LOAD"] = "0"
    row["HEALTH_EFFECT_TYPE"] = "NONE"
    row["HEALTH_POINTS_FINAL"] = "0"
    row["SPONTANEOUS_PLAGUE_RISK_MULT"] = "1.00"
    row["PLAGUE_DURATION_MOD_TURNS"] = "0"
    row["STABILITY_POINTS_FINAL"] = "0"
    for field in HAPPINESS_ZERO_DEFAULT_FIELDS:
        if field in row:
            row[field] = "0"
    row["FINAL_MERGE_STATUS"] = "MERGED_V5"
    return row


def apply_v3(rows, fieldnames, v3_rows):
    by_name = {r["BUILDING_EN"]: r for r in rows}
    for ov in v3_rows:
        name = ov["BUILDING_EN"]
        action = ov["ACTION"]
        if action == "ADD":
            if name in by_name:
                raise ValueError(f"V3 ADD duplicates existing building: {name}")
            row = init_system_defaults(blank_row(fieldnames))
            row["BUILDING_EN"] = name
            for src, dst in V3_TO_BASE.items():
                if src in ov and ov[src] != "":
                    row[dst] = ov[src]
            row["SOURCE_GRADE"] = "PROJECT_V3_OVERRIDE"
            row["NUMERIC_BASIS"] = "Building V3 additive override"
            rows.append(row)
            by_name[name] = row
        elif action in {"OVERRIDE_SPECIAL_EFFECT", "OVERRIDE"}:
            if name not in by_name:
                raise ValueError(f"V3 override target missing: {name}")
            row = by_name[name]
            for src, dst in V3_TO_BASE.items():
                if src in ov and ov[src] != "":
                    row[dst] = ov[src]
        else:
            raise ValueError(f"Unsupported V3 action {action} for {name}")

        row = by_name[name]
        row["FINAL_MERGE_SOURCES"] = ";".join(
            filter(None, [row.get("FINAL_MERGE_SOURCES", ""), "V3"])
        )
    return rows


def apply_base_numeric_change(row, change):
    change = (change or "").strip()
    if not change:
        return
    if change == "Local Happiness 2 -> 1":
        row["LOCAL_HAPPINESS"] = "1"
        return
    raise ValueError(f"Unsupported POWER BASE_NUMERIC_CHANGE: {change}")


def apply_power(rows, power_rows):
    by_name = {r["BUILDING_EN"]: r for r in rows}
    for ov in power_rows:
        name = ov["BUILDING_EN"]
        if name not in by_name:
            raise ValueError(f"Power target missing: {name}")
        row = by_name[name]
        row["POWER_LOAD"] = as_int_text(ov.get("POWER_LOAD", "")) or "0"
        row["POWERED_BONUS"] = ov.get("POWERED_BONUS", "").strip()
        row["POWER_SOURCE_RULE"] = ov.get("POWER_SOURCE_RULE", "").strip()
        apply_base_numeric_change(row, ov.get("BASE_NUMERIC_CHANGE", ""))
        row["FINAL_MERGE_SOURCES"] = ";".join(
            filter(None, [row.get("FINAL_MERGE_SOURCES", ""), "POWER_V4"])
        )
    return rows


def apply_health(rows, health_rows):
    by_name = {r["BUILDING_EN"]: r for r in rows}
    for ov in health_rows:
        name = ov["BUILDING"]
        if name not in by_name:
            raise ValueError(f"Health target missing: {name}")
        row = by_name[name]
        row["HEALTH_EFFECT_TYPE"] = ov["HEALTH_EFFECT_TYPE"]
        row["HEALTH_POINTS_FINAL"] = as_int_text(ov["HEALTH_VALUE"]) or "0"
        row["SPONTANEOUS_PLAGUE_RISK_MULT"] = ov[
            "SPONTANEOUS_PLAGUE_RISK_MULT"
        ]
        row["PLAGUE_DURATION_MOD_TURNS"] = (
            as_int_text(ov["PLAGUE_DURATION_MOD_TURNS"]) or "0"
        )
        row["HEALTH_OTHER_EFFECT"] = ov["OTHER_EFFECT"]
        row["FINAL_MERGE_SOURCES"] = ";".join(
            filter(None, [row.get("FINAL_MERGE_SOURCES", ""), "HEALTH_V1"])
        )
    return rows


def apply_stability(rows):
    for row in rows:
        final_value = as_int_text(row.get("STABILITY_POINTS_PROVISIONAL", "")) or "0"
        row["STABILITY_POINTS_FINAL"] = final_value
        if final_value != "0":
            row["FINAL_MERGE_SOURCES"] = ";".join(
                filter(None, [row.get("FINAL_MERGE_SOURCES", ""), "STABILITY_BUILDING_V1"])
            )
    return rows


def resolve_stale_markers(rows):
    for row in rows:
        special = row.get("SPECIAL_EFFECTS", "")

        if row.get("HEALTH_EFFECT_TYPE", "NONE") != "NONE":
            special = special.replace(
                "HEALTH_SYSTEM_EFFECT=PENDING",
                STALE_MARKER_REPLACEMENTS["HEALTH_SYSTEM_EFFECT=PENDING"],
            )

        if row.get("POWER_SOURCE_RULE", ""):
            special = special.replace(
                "POWER_SYSTEM_OUTPUT=PENDING",
                STALE_MARKER_REPLACEMENTS["POWER_SYSTEM_OUTPUT=PENDING"],
            )
            special = special.replace(
                "POLLUTION_SYSTEM_EFFECT=PENDING",
                STALE_MARKER_REPLACEMENTS["POLLUTION_SYSTEM_EFFECT=PENDING"],
            )

        if row.get("POWERED_BONUS", ""):
            special = special.replace(
                "POWERED_BONUS_HANDLED_BY_POWER_SYSTEM_PENDING",
                STALE_MARKER_REPLACEMENTS[
                    "POWERED_BONUS_HANDLED_BY_POWER_SYSTEM_PENDING"
                ],
            )

        row["SPECIAL_EFFECTS"] = special
    return rows


def build(base, v3, power, health, out):
    base_rows = read_csv(base)
    if not base_rows:
        raise ValueError("Base building table is empty")

    base_fields = list(base_rows[0].keys())
    fieldnames = base_fields + [f for f in EXTRA_FIELDS if f not in base_fields]

    rows = []
    for src in base_rows:
        row = init_system_defaults(blank_row(fieldnames))
        row.update(src)
        row["FINAL_MERGE_SOURCES"] = "BASE_V2"
        rows.append(row)

    apply_v3(rows, fieldnames, read_csv(v3))
    apply_power(rows, read_csv(power))
    apply_health(rows, read_csv(health))
    apply_stability(rows)
    resolve_stale_markers(rows)

    names = [r["BUILDING_EN"] for r in rows]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate BUILDING_EN after merge")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--v3", type=Path, default=V3)
    parser.add_argument("--power", type=Path, default=POWER)
    parser.add_argument("--health", type=Path, default=HEALTH)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    rows = build(args.base, args.v3, args.power, args.health, args.out)
    print(f"BUILDING_MASTER_MERGE: PASS rows={len(rows)} out={args.out}")


if __name__ == "__main__":
    main()
