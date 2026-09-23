from __future__ import annotations

import argparse
import csv
from pathlib import Path

MASTER = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv")

NEED_FIELDS = {
    "distress": "VP_DISTRESS_REDUCTION",
    "poverty": "VP_POVERTY_REDUCTION",
    "illiteracy": "VP_ILLITERACY_REDUCTION",
    "boredom": "VP_BOREDOM_REDUCTION",
    "religious": "VP_RELIGIOUS_UNREST_REDUCTION",
}

REQUIRED = [
    "BUILDING_EN",
    "LOCAL_HAPPINESS",
    *NEED_FIELDS.values(),
    "HEALTH_POINTS_FINAL",
    "STABILITY_POINTS_FINAL",
]


def read_csv(path: Path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise AssertionError("Building master has no header")
        rows = list(reader)
        return reader.fieldnames, rows


def parse_numeric(value, *, building: str, field: str, nonnegative: bool) -> float:
    text = str(value if value is not None else "").strip()
    if text == "":
        raise AssertionError(f"{building}: {field} is blank")
    try:
        number = float(text)
    except ValueError as exc:
        raise AssertionError(f"{building}: {field} is non-numeric: {text!r}") from exc
    if nonnegative and number < 0:
        raise AssertionError(f"{building}: {field} must be >= 0, got {number}")
    return number


def validate_building_links(path: Path = MASTER) -> dict[str, object]:
    fieldnames, rows = read_csv(path)
    missing = [field for field in REQUIRED if field not in fieldnames]
    if missing:
        raise AssertionError(f"Building master missing required fields: {', '.join(missing)}")
    if not rows:
        raise AssertionError("Building master has no rows")

    counts = {key: 0 for key in NEED_FIELDS}
    local_happiness_sources = 0
    seen = set()

    for row in rows:
        name = str(row.get("BUILDING_EN", "")).strip()
        if not name:
            raise AssertionError("Building master contains blank BUILDING_EN")
        if name in seen:
            raise AssertionError(f"Duplicate BUILDING_EN: {name}")
        seen.add(name)

        local = parse_numeric(
            row.get("LOCAL_HAPPINESS"),
            building=name,
            field="LOCAL_HAPPINESS",
            nonnegative=True,
        )
        if local > 0:
            local_happiness_sources += 1

        for key, field in NEED_FIELDS.items():
            value = parse_numeric(
                row.get(field),
                building=name,
                field=field,
                nonnegative=True,
            )
            if value > 0:
                counts[key] += 1

        # Cross-system guard columns must exist and remain numeric, but they are
        # deliberately excluded from Happiness source counts.
        parse_numeric(
            row.get("HEALTH_POINTS_FINAL"),
            building=name,
            field="HEALTH_POINTS_FINAL",
            nonnegative=False,
        )
        parse_numeric(
            row.get("STABILITY_POINTS_FINAL"),
            building=name,
            field="STABILITY_POINTS_FINAL",
            nonnegative=False,
        )

    for required_source in ("distress", "poverty", "illiteracy", "boredom"):
        if counts[required_source] == 0:
            raise AssertionError(
                f"No positive building source for {NEED_FIELDS[required_source]}"
            )

    return {
        "rows": len(rows),
        "distress_sources": counts["distress"],
        "poverty_sources": counts["poverty"],
        "illiteracy_sources": counts["illiteracy"],
        "boredom_sources": counts["boredom"],
        "religious_sources": counts["religious"],
        "local_happiness_sources": local_happiness_sources,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, default=MASTER)
    args = parser.parse_args()
    result = validate_building_links(args.master)
    print(
        "HAPPINESS_BUILDING_LINK_QA: PASS "
        f"rows={result['rows']} "
        f"distress_sources={result['distress_sources']} "
        f"poverty_sources={result['poverty_sources']} "
        f"illiteracy_sources={result['illiteracy_sources']} "
        f"boredom_sources={result['boredom_sources']} "
        f"religious_sources={result['religious_sources']} "
        f"local_happiness_sources={result['local_happiness_sources']}"
    )


if __name__ == "__main__":
    main()
