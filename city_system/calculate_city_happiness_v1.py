from __future__ import annotations

import csv
import math
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


def _number(value, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc


def _positive_float(value, label: str) -> float:
    number = _number(value, label)
    if number <= 0:
        raise ValueError(f"{label} must be > 0")
    return number


def _nonnegative_number(value, label: str) -> float:
    number = _number(value, label)
    if number < 0:
        raise ValueError(f"{label} must be >= 0")
    return number


def _nonnegative_int(value, label: str) -> int:
    number = _number(value, label)
    if number < 0 or not number.is_integer():
        raise ValueError(f"{label} must be a nonnegative integer")
    return int(number)


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
    if not isinstance(global_medians, dict):
        raise ValueError("global_medians must be a dictionary")
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


def health_unhappiness(health: int | float) -> int:
    health_value = _number(health, "city_health")
    if health_value >= 0:
        return 0
    if health_value >= -2:
        return 1
    if health_value >= -4:
        return 2
    return 3


def calculate_city_happiness(
    *,
    era,
    population,
    gross_food_pre_health,
    production,
    gold,
    science,
    culture,
    city_health,
    minority_followers=0,
    religion_active=True,
    local_happiness_sources=0,
    distress_reduction=0,
    poverty_reduction=0,
    illiteracy_reduction=0,
    boredom_reduction=0,
    religious_unrest_reduction=0,
    global_medians=None,
    war_weariness_unhappiness=0,
    occupation_unhappiness=0,
    colonial_unhappiness=0,
    policy_burden_unhappiness=0,
    expectations_path=DEFAULT_EXPECTATIONS,
):
    population = _nonnegative_int(population, "population")
    minority_followers = _nonnegative_int(minority_followers, "minority_followers")
    if minority_followers > population:
        raise ValueError("minority_followers cannot exceed population")

    yields = {
        "gross_food_pre_health": _nonnegative_number(
            gross_food_pre_health, "gross_food_pre_health"
        ),
        "production": _nonnegative_number(production, "production"),
        "gold": _nonnegative_number(gold, "gold"),
        "science": _nonnegative_number(science, "science"),
        "culture": _nonnegative_number(culture, "culture"),
    }

    reductions = {
        "distress": _nonnegative_number(distress_reduction, "distress_reduction"),
        "poverty": _nonnegative_number(poverty_reduction, "poverty_reduction"),
        "illiteracy": _nonnegative_number(
            illiteracy_reduction, "illiteracy_reduction"
        ),
        "boredom": _nonnegative_number(boredom_reduction, "boredom_reduction"),
        "religious_unrest": _nonnegative_number(
            religious_unrest_reduction, "religious_unrest_reduction"
        ),
    }

    local_sources = _number(local_happiness_sources, "local_happiness_sources")
    external_penalties = {
        "war_weariness": _nonnegative_number(
            war_weariness_unhappiness, "war_weariness_unhappiness"
        ),
        "occupation": _nonnegative_number(
            occupation_unhappiness, "occupation_unhappiness"
        ),
        "colonial": _nonnegative_number(
            colonial_unhappiness, "colonial_unhappiness"
        ),
        "policy_burden": _nonnegative_number(
            policy_burden_unhappiness, "policy_burden_unhappiness"
        ),
    }

    expectations = load_expectations(Path(expectations_path))
    effective = get_effective_expectations(era, expectations, global_medians)
    health_value = _number(city_health, "city_health")

    supported_basic = math.floor(
        (yields["gross_food_pre_health"] + yields["production"])
        / effective["basic"]
    )
    supported_gold = math.floor(yields["gold"] / effective["gold"])
    supported_science = math.floor(yields["science"] / effective["science"])
    supported_culture = math.floor(yields["culture"] / effective["culture"])

    if population == 0:
        distress_raw = poverty_raw = illiteracy_raw = boredom_raw = 0
        religious_unrest_raw = 0
        distress = poverty = illiteracy = boredom = religious_unrest = 0
        pre_cap = 0
        citizen_needs = 0
        health_penalty = 0
        local_positive = 0
    else:
        distress_raw = max(0, population - supported_basic)
        poverty_raw = max(0, population - supported_gold)
        illiteracy_raw = max(0, population - supported_science)
        boredom_raw = max(0, population - supported_culture)

        if religion_active:
            religious_unrest_raw = minority_followers // 2
        else:
            religious_unrest_raw = 0

        distress = max(0.0, distress_raw - reductions["distress"])
        poverty = max(0.0, poverty_raw - reductions["poverty"])
        illiteracy = max(0.0, illiteracy_raw - reductions["illiteracy"])
        boredom = max(0.0, boredom_raw - reductions["boredom"])
        religious_unrest = max(
            0.0,
            religious_unrest_raw - reductions["religious_unrest"],
        )

        pre_cap = distress + poverty + illiteracy + boredom + religious_unrest
        citizen_needs = min(float(population), pre_cap)
        health_penalty = health_unhappiness(health_value)
        local_positive = min(float(population), max(0.0, local_sources))

    external_total = sum(external_penalties.values())
    city_happiness = (
        local_positive - citizen_needs - health_penalty - external_total
    )

    return {
        "era": era,
        "population": population,
        "effective_expectations": effective,
        "supported_basic": supported_basic,
        "supported_gold": supported_gold,
        "supported_science": supported_science,
        "supported_culture": supported_culture,
        "distress_raw": distress_raw,
        "poverty_raw": poverty_raw,
        "illiteracy_raw": illiteracy_raw,
        "boredom_raw": boredom_raw,
        "religious_unrest_raw": religious_unrest_raw,
        "distress": distress,
        "poverty": poverty,
        "illiteracy": illiteracy,
        "boredom": boredom,
        "religious_unrest": religious_unrest,
        "citizen_needs_pre_cap": pre_cap,
        "citizen_needs_unhappiness": citizen_needs,
        "health_unhappiness": health_penalty,
        "local_happiness_positive": local_positive,
        "external_penalties": external_penalties,
        "external_penalty_total": external_total,
        "city_happiness": city_happiness,
    }


if __name__ == "__main__":
    data = load_expectations(DEFAULT_EXPECTATIONS)
    print(f"HAPPINESS_EXPECTATIONS: PASS eras={len(data)}")
