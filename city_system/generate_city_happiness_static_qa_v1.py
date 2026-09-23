from __future__ import annotations

from pathlib import Path

from calculate_city_happiness_v1 import (
    DEFAULT_EXPECTATIONS,
    calculate_city_happiness,
    get_effective_expectations,
    load_expectations,
)

OUT = Path("city_system/CITY_HAPPINESS_STATIC_QA_V1.md")


def base_city(**overrides):
    data = dict(
        era="Ancient",
        population=4,
        gross_food_pre_health=6,
        production=2,
        gold=3,
        science=3,
        culture=2,
        city_health=0,
    )
    data.update(overrides)
    return data


def record(name: str, result: dict, notes: str = "") -> dict:
    return {
        "scenario": name,
        "population": result["population"],
        "needs_pre_cap": result["citizen_needs_pre_cap"],
        "needs_final": result["citizen_needs_unhappiness"],
        "health": result["health_unhappiness"],
        "local": result["local_happiness_positive"],
        "external": result["external_penalty_total"],
        "final": result["city_happiness"],
        "notes": notes,
        "status": "PASS",
    }


def fmt_number(value):
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.3f}".rstrip("0").rstrip(".")


def build_scenarios():
    scenarios = []

    # A. Balanced Ancient city.
    a = calculate_city_happiness(**base_city())
    assert (a["supported_basic"], a["supported_gold"], a["supported_science"], a["supported_culture"]) == (4, 4, 4, 5)
    assert a["citizen_needs_unhappiness"] == 0
    assert a["city_happiness"] == 0
    scenarios.append(record("A Balanced Ancient", a, "No Needs deficit"))

    # B. Severe underdevelopment must be population-capped.
    b = calculate_city_happiness(
        **base_city(gross_food_pre_health=4, production=2, gold=1, science=1, culture=0)
    )
    assert b["citizen_needs_pre_cap"] == 11
    assert b["citizen_needs_unhappiness"] == 4
    assert b["city_happiness"] == -4
    scenarios.append(record("B Underdeveloped Ancient", b, "Needs sum 11 capped to population 4"))

    # C. Flat building reduction applies exactly once.
    c = calculate_city_happiness(**base_city(science=1), illiteracy_reduction=1)
    assert c["illiteracy_raw"] == 3
    assert c["illiteracy"] == 2
    assert c["city_happiness"] == -2
    scenarios.append(record("C Illiteracy Reduction", c, "Illiteracy 3 -> 2"))

    # D. Health is a separate cause and does not change supported Basic population.
    d0 = calculate_city_happiness(**base_city(city_health=0))
    d = calculate_city_happiness(**base_city(city_health=-4))
    assert d["health_unhappiness"] == 2
    assert d["supported_basic"] == d0["supported_basic"]
    assert d["distress"] == d0["distress"]
    assert d["city_happiness"] == -2
    scenarios.append(record("D Health -4 Independent", d, "Health penalty 2; Distress unchanged"))

    # E. Religious minority formula.
    e = calculate_city_happiness(
        **base_city(population=6, gross_food_pre_health=10, production=2, gold=6, science=6, culture=4),
        minority_followers=5,
    )
    assert e["religious_unrest_raw"] == 2
    assert e["religious_unrest"] == 2
    assert e["city_happiness"] == -2
    scenarios.append(record("E Religious Minority", e, "5 minority followers -> unrest 2"))

    # F. Local Happiness cannot exceed city population.
    f = calculate_city_happiness(
        **base_city(population=3, gross_food_pre_health=4, production=2, gold=3, science=3, culture=2),
        local_happiness_sources=5,
    )
    assert f["local_happiness_positive"] == 3
    assert f["city_happiness"] == 3
    scenarios.append(record("F Local Happiness Cap", f, "Local sources 5 capped to population 3"))

    # G. Relative adjustment is clamped both high and low.
    expectations = load_expectations(DEFAULT_EXPECTATIONS)
    high_medians = {"basic": 3.0, "gold": 2.0, "science": 2.0, "culture": 1.0}
    low_medians = {"basic": 0.5, "gold": 0.1, "science": 0.1, "culture": 0.1}
    high = get_effective_expectations("Ancient", expectations, high_medians)
    low = get_effective_expectations("Ancient", expectations, low_medians)
    assert abs(high["basic"] - 2.2) < 1e-12
    assert abs(high["science"] - 0.825) < 1e-12
    assert abs(low["basic"] - 1.8) < 1e-12
    assert abs(low["culture"] - 0.36) < 1e-12
    g = calculate_city_happiness(**base_city(), global_medians=high_medians)
    scenarios.append(record("G Relative Clamp", g, "High=1.10x and low=0.90x verified"))

    # H. A named external penalty passes through exactly once.
    h = calculate_city_happiness(**base_city(), war_weariness_unhappiness=2)
    assert h["external_penalty_total"] == 2
    assert h["city_happiness"] == -2
    scenarios.append(record("H External Passthrough", h, "War Weariness 2 applied once"))

    # I. Population-zero transitional object has no local/Needs/Health terms.
    i = calculate_city_happiness(
        **base_city(population=0, gross_food_pre_health=0, production=0, gold=0, science=0, culture=0, city_health=-10),
        local_happiness_sources=10,
        war_weariness_unhappiness=1,
        occupation_unhappiness=1,
        colonial_unhappiness=1,
        policy_burden_unhappiness=1,
    )
    assert i["citizen_needs_unhappiness"] == 0
    assert i["health_unhappiness"] == 0
    assert i["local_happiness_positive"] == 0
    assert i["city_happiness"] == -4
    scenarios.append(record("I Zero Population", i, "Only explicit external penalties remain"))

    # J. Floating-point threshold must floor rather than round upward.
    j = calculate_city_happiness(
        **base_city(population=3, gross_food_pre_health=4, production=2, gold=3, science=(0.75 * 3) - 1e-9, culture=2)
    )
    assert j["supported_science"] == 2
    assert j["illiteracy_raw"] == 1
    assert j["city_happiness"] == -1
    scenarios.append(record("J Floor Boundary", j, "Science just below 3-person threshold supports 2"))

    # K. All four external penalty channels are independent and additive.
    k = calculate_city_happiness(
        **base_city(),
        war_weariness_unhappiness=2,
        occupation_unhappiness=1,
        colonial_unhappiness=3,
        policy_burden_unhappiness=1,
    )
    assert k["external_penalties"] == {
        "war_weariness": 2,
        "occupation": 1,
        "colonial": 3,
        "policy_burden": 1,
    }
    assert k["external_penalty_total"] == 7
    assert k["city_happiness"] == -7
    scenarios.append(record("K Four External Channels", k, "2+1+3+1 = 7 external penalty"))

    # L. Religion-disabled city ignores minority count for Religious Unrest.
    l = calculate_city_happiness(
        **base_city(population=6, gross_food_pre_health=10, production=2, gold=6, science=6, culture=4),
        minority_followers=5,
        religion_active=False,
    )
    assert l["religious_unrest_raw"] == 0
    assert l["religious_unrest"] == 0
    assert l["city_happiness"] == 0
    scenarios.append(record("L Religion Inactive", l, "Minority followers ignored before religion system is active"))

    assert len(scenarios) == 12
    return scenarios


def render_report(scenarios):
    lines = [
        "# City Happiness Static QA V1",
        "",
        "Date: 2026-09-23",
        "Status: PRE-RUNTIME STATIC ARITHMETIC QA",
        "",
        "This report is generated by `generate_city_happiness_static_qa_v1.py`. It is not gameplay telemetry and it is not autoplay evidence.",
        "",
        "| Scenario | Population | Needs pre-cap | Needs final | Health penalty | Local Happiness | External penalty | Final City Happiness | Status | Notes |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in scenarios:
        lines.append(
            "| {scenario} | {population} | {needs_pre_cap} | {needs_final} | {health} | {local} | {external} | {final} | {status} | {notes} |".format(
                scenario=row["scenario"],
                population=row["population"],
                needs_pre_cap=fmt_number(row["needs_pre_cap"]),
                needs_final=fmt_number(row["needs_final"]),
                health=fmt_number(row["health"]),
                local=fmt_number(row["local"]),
                external=fmt_number(row["external"]),
                final=fmt_number(row["final"]),
                status=row["status"],
                notes=row["notes"],
            )
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"**PASS: {len(scenarios)} / {len(scenarios)} static scenarios.**",
            "",
            "The checks cover population capping, flat Needs reductions, Health separation, religion, Local Happiness capping, relative-expectation bounds, external penalty interfaces, zero-population handling and floating-point floor behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    scenarios = build_scenarios()
    OUT.write_text(render_report(scenarios), encoding="utf-8")
    print(f"CITY_HAPPINESS_STATIC_QA: PASS scenarios={len(scenarios)}")


if __name__ == "__main__":
    main()
