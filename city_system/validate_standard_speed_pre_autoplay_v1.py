#!/usr/bin/env python3
"""Static pre-autoplay validation for project Science/Culture cost curves.

This script does not run the Civilization game engine. It verifies the two
provisional Standard-speed cost curves and reproduces the era-level QA table.
"""
from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TECH = ROOT / "tech_reference" / "VP_SCIENCE_COST_CURVE_ADAPTATION_V1.csv"
CIVIC = ROOT / "civics_reference" / "VP_CULTURE_COST_CURVE_ADAPTATION_V1.csv"
OUT = Path(__file__).with_name("STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.csv")

ERA_ORDER = [
    "Ancient", "Classical", "Late Antiquity", "Early Medieval",
    "High Medieval", "Renaissance", "Exploration", "Enlightenment",
    "Industrial", "Modern", "Atomic", "Information", "Future",
]


def read_grouped(path: Path, era_col: str, cost_col: str) -> OrderedDict[str, list[int]]:
    grouped = OrderedDict((era, []) for era in ERA_ORDER)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            era = row[era_col]
            if era not in grouped:
                raise ValueError(f"Unexpected era {era!r} in {path}")
            grouped[era].append(int(row[cost_col]))
    return grouped


def r3(value: float | None) -> str:
    return "" if value is None else f"{value:.3f}".rstrip("0").rstrip(".")


def r1(value: float) -> str:
    return f"{value:.1f}"


def main() -> None:
    tech = read_grouped(TECH, "PROJECT_ERA", "SCIENCE_COST_PROVISIONAL")
    civic = read_grouped(CIVIC, "PROJECT_ERA", "CULTURE_COST_PROVISIONAL")

    assert sum(map(len, tech.values())) == 109, "Expected 109 technologies"
    assert sum(map(len, civic.values())) == 72, "Expected 72 civics"

    fields = [
        "ERA", "TECH_N", "TECH_SUM", "TECH_MEAN", "TECH_MIN", "TECH_MAX",
        "TECH_BOUNDARY_RATIO", "TECH_SUM_RATIO_PREV",
        "CIVIC_N", "CIVIC_SUM", "CIVIC_MEAN", "CIVIC_MIN", "CIVIC_MAX",
        "CIVIC_BOUNDARY_RATIO", "CIVIC_SUM_RATIO_PREV",
        "TECH_TO_CIVIC_MEAN_RATIO", "QA_FLAGS",
    ]

    rows = []
    for i, era in enumerate(ERA_ORDER):
        tv, cv = tech[era], civic[era]
        if not tv or not cv:
            raise ValueError(f"Missing Technology or Civic nodes for {era}")
        if tv != sorted(tv):
            raise ValueError(f"Non-monotonic Technology costs inside {era}")
        if cv != sorted(cv):
            raise ValueError(f"Non-monotonic Civic costs inside {era}")

        t_sum, c_sum = sum(tv), sum(cv)
        t_mean, c_mean = t_sum / len(tv), c_sum / len(cv)
        t_boundary = c_boundary = t_sum_ratio = c_sum_ratio = None
        if i:
            prev = ERA_ORDER[i - 1]
            t_boundary = min(tv) / max(tech[prev])
            c_boundary = min(cv) / max(civic[prev])
            t_sum_ratio = t_sum / sum(tech[prev])
            c_sum_ratio = c_sum / sum(civic[prev])
            if min(tv) <= max(tech[prev]):
                raise ValueError(f"Technology era boundary is not increasing: {prev} -> {era}")
            if min(cv) <= max(civic[prev]):
                raise ValueError(f"Civic era boundary is not increasing: {prev} -> {era}")

        flags = []
        if t_boundary is not None and t_boundary >= 1.5:
            flags.append("SCIENCE_BOUNDARY_JUMP")
        if c_boundary is not None and c_boundary >= 1.5:
            flags.append("CULTURE_BOUNDARY_JUMP")
        if t_sum_ratio is not None and t_sum_ratio >= 2.5:
            flags.append("SCIENCE_ERA_BULK")
        if c_sum_ratio is not None and c_sum_ratio >= 2.5:
            flags.append("CULTURE_ERA_BULK")
        if t_mean / c_mean >= 1.6:
            flags.append("SCIENCE_CULTURE_RATIO_WATCH")

        rows.append({
            "ERA": era,
            "TECH_N": len(tv), "TECH_SUM": t_sum, "TECH_MEAN": r1(t_mean),
            "TECH_MIN": min(tv), "TECH_MAX": max(tv),
            "TECH_BOUNDARY_RATIO": r3(t_boundary),
            "TECH_SUM_RATIO_PREV": r3(t_sum_ratio),
            "CIVIC_N": len(cv), "CIVIC_SUM": c_sum, "CIVIC_MEAN": r1(c_mean),
            "CIVIC_MIN": min(cv), "CIVIC_MAX": max(cv),
            "CIVIC_BOUNDARY_RATIO": r3(c_boundary),
            "CIVIC_SUM_RATIO_PREV": r3(c_sum_ratio),
            "TECH_TO_CIVIC_MEAN_RATIO": r3(t_mean / c_mean),
            "QA_FLAGS": ";".join(flags) if flags else "PASS_STATIC",
        })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    flagged = [r for r in rows if r["QA_FLAGS"] != "PASS_STATIC"]
    print(f"PASS: 109 technologies, 72 civics, {len(ERA_ORDER)} eras")
    print(f"Runtime-watch eras: {', '.join(r['ERA'] for r in flagged)}")
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    main()
