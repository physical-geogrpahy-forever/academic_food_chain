from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROSTER = Path("city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv")
ROSTER_V3 = Path("city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv")
MASTER = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv")
TECH = Path("tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv")
CIVIC = Path("civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv")

SYNTHETIC_CIVIC_GATES = {
    "Tier-2 government adoption",
    "Tier-3 government adoption",
}

ALLOWED_PENDING_SPECIAL_EFFECT_TOKENS = {
    "FOOD_STORAGE_TRADE_LOSS_REDUCTION=PENDING_LOGISTICS_SYSTEM",
    "POWER_SYSTEM_CAPACITY=PENDING",
}


def read(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def row_contains(row, needle):
    return needle.lower() in " | ".join(str(v) for v in row.values()).lower()


def merged_roster(base_rows, overrides):
    rows = [dict(r) for r in base_rows]
    by_name = {r["BUILDING_EN"]: r for r in rows}
    for ov in overrides:
        name = ov["BUILDING_EN"]
        action = ov["ACTION"]
        if action == "ADD":
            if name in by_name:
                raise AssertionError(f"Roster ADD duplicates existing building: {name}")
            row = {k: "" for k in rows[0].keys()}
            for key, value in ov.items():
                if key != "ACTION" and key in row:
                    row[key] = value
            rows.append(row)
            by_name[name] = row
        elif action == "OVERRIDE":
            if name not in by_name:
                raise AssertionError(f"Roster override target missing: {name}")
            for key, value in ov.items():
                if key != "ACTION" and key in by_name[name] and value != "":
                    by_name[name][key] = value
        else:
            raise AssertionError(f"Unsupported roster action: {action} for {name}")
    return rows


def validate(roster_path, roster_v3_path, master_path, tech_path, civic_path):
    roster = merged_roster(read(roster_path), read(roster_v3_path))
    master = read(master_path)
    tech = read(tech_path)
    civic = read(civic_path)

    roster_names = [r["BUILDING_EN"] for r in roster]
    master_names = [r["BUILDING_EN"] for r in master]
    errors = []
    warnings = []
    deferred = []

    if len(roster_names) != len(set(roster_names)):
        errors.append("duplicate BUILDING_EN in merged roster")
    if len(master_names) != len(set(master_names)):
        errors.append("duplicate BUILDING_EN in numeric master")

    roster_set = set(roster_names)
    master_set = set(master_names)
    for name in sorted(roster_set - master_set):
        errors.append(f"roster building missing numeric master: {name}")
    for name in sorted(master_set - roster_set):
        errors.append(f"numeric master building missing roster: {name}")

    tech_by = {r["TECH_EN"]: r for r in tech}
    civic_by = {r["CIVIC_EN"]: r for r in civic}

    for row in roster:
        name = row["BUILDING_EN"]
        tech_gate = row.get("TECH_GATE", "").strip()
        civic_gate = row.get("CIVIC_GATE", "").strip()

        if tech_gate:
            if tech_gate not in tech_by:
                errors.append(f"{name}: TECH_GATE not found: {tech_gate}")
            elif not row_contains(tech_by[tech_gate], name):
                errors.append(f"{name}: tech row {tech_gate} does not mention building")

        if civic_gate and civic_gate not in SYNTHETIC_CIVIC_GATES:
            if civic_gate not in civic_by:
                errors.append(f"{name}: CIVIC_GATE not found: {civic_gate}")
            elif not row_contains(civic_by[civic_gate], name):
                errors.append(f"{name}: civic row {civic_gate} does not mention building")

    for row in master:
        name = row["BUILDING_EN"]
        special = row.get("SPECIAL_EFFECTS", "")
        health_type = row.get("HEALTH_EFFECT_TYPE", "NONE")

        pending_tokens = [
            token.strip()
            for token in special.split(";")
            if "PENDING" in token.upper()
        ]
        for token in pending_tokens:
            if token in ALLOWED_PENDING_SPECIAL_EFFECT_TOKENS:
                deferred.append(f"{name}: {token}")
            else:
                errors.append(f"{name}: unexpected unresolved pending marker: {token}")

        if row.get("HEALTH_POINTS_FINAL", "") == "":
            errors.append(f"{name}: HEALTH_POINTS_FINAL blank")
        if row.get("POWER_LOAD", "") == "":
            errors.append(f"{name}: POWER_LOAD blank")

        provisional = row.get("HEALTH_POINTS_PROVISIONAL", "")
        final_health = row.get("HEALTH_POINTS_FINAL", "")
        if provisional not in ("", final_health) and health_type != "NONE":
            warnings.append(
                f"{name}: provisional Health retained for provenance; "
                f"final={final_health}, provisional={provisional}"
            )

    if errors:
        raise AssertionError("\n".join(errors))

    return {
        "roster_rows": len(roster),
        "master_rows": len(master),
        "warnings": warnings,
        "deferred": deferred,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=ROSTER)
    parser.add_argument("--roster-v3", type=Path, default=ROSTER_V3)
    parser.add_argument("--master", type=Path, default=MASTER)
    parser.add_argument("--tech", type=Path, default=TECH)
    parser.add_argument("--civic", type=Path, default=CIVIC)
    args = parser.parse_args()

    result = validate(args.roster, args.roster_v3, args.master, args.tech, args.civic)
    print(
        "FINAL_BUILDING_MASTER_QA: PASS "
        f"roster={result['roster_rows']} master={result['master_rows']} "
        f"warnings={len(result['warnings'])} deferred={len(result['deferred'])}"
    )
    for warning in result["warnings"]:
        print("WARN:", warning)
    for item in result["deferred"]:
        print("DEFERRED:", item)


if __name__ == "__main__":
    main()
