from __future__ import annotations

import csv
from pathlib import Path

MASTER = Path("city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv")
OUT = Path("city_system/FINAL_BUILDING_REMAINING_PROVISIONAL_AUDIT_V1.md")


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def nonzero(value: str) -> bool:
    text = str(value or "").strip()
    if text == "":
        return False
    try:
        return float(text) != 0
    except ValueError:
        return True


def main():
    rows = read_csv(MASTER)
    if not rows:
        raise ValueError("final building master is empty")

    provisional_fields = [
        field for field in rows[0].keys() if field.upper().endswith("_PROVISIONAL")
    ]

    sections = []
    unresolved_count = 0

    for field in provisional_fields:
        hits = [r for r in rows if nonzero(r.get(field, ""))]
        if field == "HEALTH_POINTS_PROVISIONAL":
            status = "SUPERSEDED_PROVENANCE"
            authority = "HEALTH_POINTS_FINAL / Health V1"
        elif field == "STABILITY_POINTS_PROVISIONAL":
            status = "SUPERSEDED_PROVENANCE"
            authority = "STABILITY_POINTS_FINAL / Building Stability Support V1"
        else:
            status = "UNRESOLVED_REVIEW"
            authority = "No explicit superseding authority registered"
            unresolved_count += len(hits)

        sections.append((field, status, authority, hits))

    lines = [
        "# Final Building Remaining Provisional Audit V1",
        "",
        "Generated from `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`.",
        "",
        f"- Building rows: {len(rows)}",
        f"- Provisional columns found: {len(provisional_fields)}",
        f"- Unresolved nonzero provisional entries: {unresolved_count}",
        "",
    ]

    for field, status, authority, hits in sections:
        lines.extend([
            f"## {field}",
            "",
            f"- Status: `{status}`",
            f"- Current authority: {authority}",
            f"- Nonzero rows: {len(hits)}",
            "",
        ])
        if hits:
            lines.append("| Building | Era | Chain | Value |")
            lines.append("|---|---|---|---:|")
            for row in hits:
                lines.append(
                    f"| {row['BUILDING_EN']} | {row.get('PROJECT_ERA','')} | "
                    f"{row.get('CHAIN','')} | {row.get(field,'')} |"
                )
            lines.append("")
        else:
            lines.extend(["No nonzero entries.", ""])

    lines.extend([
        "## Decision",
        "",
        "`HEALTH_POINTS_PROVISIONAL` is retained only as provenance and does not control gameplay because Health V1 supplies `HEALTH_POINTS_FINAL`.",
        "",
        "`STABILITY_POINTS_PROVISIONAL` is also retained only as provenance. Building gameplay authority is `STABILITY_POINTS_FINAL` under `STABILITY_BUILDING_SUPPORT_V1.md`.",
        "",
        "The building support values are not direct additions to country-level State Stability. The later State Stability quantitative pass will aggregate them with Happiness, War Weariness, government transition, occupation and colonial burdens.",
        "",
    ])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(
        "BUILDING_PROVISIONAL_AUDIT: PASS "
        f"rows={len(rows)} fields={len(provisional_fields)} unresolved_entries={unresolved_count}"
    )


if __name__ == "__main__":
    main()
