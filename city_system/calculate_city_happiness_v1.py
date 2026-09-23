from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_EXPECTATIONS = HERE / "HAPPINESS_ERA_EXPECTATIONS_V1.csv"

NEED_KEYS = {
    "BASIC_NEED": "basic",
    "GOLD_NEED": "gold",
    "SCIENCE_NEED": "science",
    "CULTURE_NEED": "culture",
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _positive_float(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if number <= 0:
        raise ValueError(f"{label} must be > 0")
    return number


def load_expectations(path: Path = DEFAULT_EXPECTATIONS) -> dict[str, dict[str, float]]:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = ["ERA", *NEED_KEYS.keys()]
        if reader.fieldnames is None or any(field not in reader.fieldnames for field in required):
            raise ValueError(f"Expectation table missing required columns: {required}")

        result: dict[str, dict[str, float]] = {}
        for row in reader:
            era = str(row.get("ERA", "")).strip()
            if not era:
                raise ValueError("Expectation table contains blank ERA")
            if era in result:
                raise ValueError(f"Duplicate era in expectation table: {era}")
            result[era] = {
                target: _positive_float(row[source], f"{era} {source}")
                for source, target in NEED_KEYS.items()
            }

    if not result:
        raise ValueError("Expectation table is empty")
    return result


def get_effective_expectations(
    era: str,
    expectations: dict[str, dict[str, float]],
    global_medians: dict[str, float] | None = None,
) -> dict[str, float]:
    if era not in expectations:
        raise ValueError(f"Unknown era: {era}")

    base = expectations[era]
    if global_medians is None:
        return dict(base)

    required = {"basic", "gold", "science", "culture"}
    missing = required - set(global_medians)
    extra = set(global_medians) - required
    if missing or extra:
        raise ValueError(
            "global_medians must contain exactly basic, gold, science, culture; "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )

    effective: dict[str, float] = {}
    for key in ("basic", "gold", "science", "culture"):
        median = _positive_float(global_medians[key], f"global median {key}")
        factor = clamp(median / base[key], 0.90, 1.10)
        effective[key] = base[key] * factor
    return effective


if __name__ == "__main__":
    data = load_expectations(DEFAULT_EXPECTATIONS)
    print(f"HAPPINESS_EXPECTATIONS: PASS eras={len(data)}")
