from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "calculate_city_happiness_v1.py"
EXPECTATIONS = HERE / "HAPPINESS_ERA_EXPECTATIONS_V1.csv"


def load_module():
    if not MODULE_PATH.exists():
        raise AssertionError("calculate_city_happiness_v1.py does not exist yet")
    spec = importlib.util.spec_from_file_location("city_happiness", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assert_raises_value_error(fn, contains: str):
    try:
        fn()
    except ValueError as exc:
        assert contains in str(exc), (contains, str(exc))
    else:
        raise AssertionError(f"Expected ValueError containing {contains!r}")


def test_load_expectations_has_13_eras(module):
    data = module.load_expectations(EXPECTATIONS)
    assert len(data) == 13
    assert data["Ancient"]["basic"] == 2.0
    assert data["Ancient"]["culture"] == 0.4
    assert data["Future"]["science"] == 5.2


def test_relative_adjustment_clamps_to_ten_percent(module):
    data = module.load_expectations(EXPECTATIONS)
    hi = module.get_effective_expectations(
        "Ancient",
        data,
        {"basic": 3.0, "gold": 2.0, "science": 2.0, "culture": 1.0},
    )
    lo = module.get_effective_expectations(
        "Ancient",
        data,
        {"basic": 0.5, "gold": 0.1, "science": 0.1, "culture": 0.1},
    )
    assert abs(hi["basic"] - 2.2) < 1e-12
    assert abs(lo["basic"] - 1.8) < 1e-12
    assert abs(hi["science"] - 0.825) < 1e-12
    assert abs(lo["culture"] - 0.36) < 1e-12


def test_unknown_era_rejected(module):
    data = module.load_expectations(EXPECTATIONS)
    assert_raises_value_error(
        lambda: module.get_effective_expectations("Stone Age", data),
        "Unknown era",
    )


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


def test_balanced_ancient_city(module):
    result = module.calculate_city_happiness(**base_city())
    assert result["supported_basic"] == 4
    assert result["supported_gold"] == 4
    assert result["supported_science"] == 4
    assert result["supported_culture"] == 5
    assert result["citizen_needs_unhappiness"] == 0
    assert result["city_happiness"] == 0


def test_underdeveloped_city_population_caps_needs(module):
    result = module.calculate_city_happiness(
        **base_city(gross_food_pre_health=4, production=2, gold=1, science=1, culture=0)
    )
    assert result["citizen_needs_pre_cap"] > 4
    assert result["citizen_needs_unhappiness"] == 4


def test_building_reduction_never_goes_below_zero(module):
    baseline = module.calculate_city_happiness(
        **base_city(science=1, culture=2)
    )
    reduced = module.calculate_city_happiness(
        **base_city(science=1, culture=2), illiteracy_reduction=1
    )
    assert reduced["illiteracy"] == max(0, baseline["illiteracy"] - 1)

    over_reduced = module.calculate_city_happiness(
        **base_city(science=3), illiteracy_reduction=5
    )
    assert over_reduced["illiteracy"] == 0


def test_health_tier_is_independent_of_distress_food(module):
    healthy = module.calculate_city_happiness(**base_city(city_health=0))
    unhealthy = module.calculate_city_happiness(**base_city(city_health=-4))
    assert unhealthy["health_unhappiness"] == 2
    assert unhealthy["supported_basic"] == healthy["supported_basic"]
    assert unhealthy["distress"] == healthy["distress"]
    assert unhealthy["city_happiness"] == healthy["city_happiness"] - 2


def test_religious_minority_formula(module):
    result = module.calculate_city_happiness(
        **base_city(population=6, gross_food_pre_health=10, production=2, gold=6, science=6, culture=4),
        minority_followers=5,
    )
    assert result["religious_unrest_raw"] == 2
    assert result["religious_unrest"] == 2

    inactive = module.calculate_city_happiness(
        **base_city(population=6, gross_food_pre_health=10, production=2, gold=6, science=6, culture=4),
        minority_followers=5,
        religion_active=False,
    )
    assert inactive["religious_unrest_raw"] == 0


def test_local_happiness_capped_by_population(module):
    result = module.calculate_city_happiness(
        **base_city(population=3, gross_food_pre_health=4, production=2, gold=3, science=3, culture=2),
        local_happiness_sources=5,
    )
    assert result["local_happiness_positive"] == 3


def test_relative_adjustment_visible_in_breakdown(module):
    result = module.calculate_city_happiness(
        **base_city(),
        global_medians={"basic": 3.0, "gold": 2.0, "science": 2.0, "culture": 1.0},
    )
    assert abs(result["effective_expectations"]["science"] - 0.825) < 1e-12
    assert abs(result["effective_expectations"]["basic"] - 2.2) < 1e-12


def test_external_penalties_pass_through_once(module):
    result = module.calculate_city_happiness(
        **base_city(),
        war_weariness_unhappiness=2,
        occupation_unhappiness=1,
        colonial_unhappiness=3,
        policy_burden_unhappiness=1,
    )
    assert result["external_penalties"] == {
        "war_weariness": 2,
        "occupation": 1,
        "colonial": 3,
        "policy_burden": 1,
    }
    assert result["external_penalty_total"] == 7
    assert result["city_happiness"] == -7


def test_zero_population_only_passes_external_penalties(module):
    result = module.calculate_city_happiness(
        **base_city(
            population=0,
            gross_food_pre_health=0,
            production=0,
            gold=0,
            science=0,
            culture=0,
            city_health=-10,
        ),
        minority_followers=0,
        local_happiness_sources=10,
        war_weariness_unhappiness=1,
        occupation_unhappiness=1,
        colonial_unhappiness=1,
        policy_burden_unhappiness=1,
    )
    assert result["citizen_needs_unhappiness"] == 0
    assert result["health_unhappiness"] == 0
    assert result["local_happiness_positive"] == 0
    assert result["city_happiness"] == -4


def test_invalid_inputs_rejected(module):
    assert_raises_value_error(
        lambda: module.calculate_city_happiness(**base_city(population=-1)),
        "population",
    )
    for key in ("gross_food_pre_health", "production", "gold", "science", "culture"):
        kwargs = {key: -0.1}
        assert_raises_value_error(
            lambda kwargs=kwargs: module.calculate_city_happiness(**base_city(**kwargs)),
            key,
        )
    for key in (
        "distress_reduction",
        "poverty_reduction",
        "illiteracy_reduction",
        "boredom_reduction",
        "religious_unrest_reduction",
    ):
        assert_raises_value_error(
            lambda key=key: module.calculate_city_happiness(**base_city(), **{key: -1}),
            key,
        )
    assert_raises_value_error(
        lambda: module.calculate_city_happiness(**base_city(), minority_followers=5),
        "minority_followers",
    )

    invalid_medians = [
        {"basic": 2, "gold": 1, "science": 1},
        {"basic": 2, "gold": 1, "science": 1, "culture": 0},
        {"basic": 2, "gold": 1, "science": -1, "culture": 1},
        {"basic": 2, "gold": 1, "science": "bad", "culture": 1},
    ]
    for medians in invalid_medians:
        assert_raises_value_error(
            lambda medians=medians: module.calculate_city_happiness(
                **base_city(), global_medians=medians
            ),
            "global",
        )


def test_floor_boundary_does_not_round_up(module):
    result = module.calculate_city_happiness(
        **base_city(population=3, science=(0.75 * 3) - 1e-9)
    )
    assert result["supported_science"] == 2
    assert result["illiteracy_raw"] == 1


def run_task1_tests(module):
    test_load_expectations_has_13_eras(module)
    test_relative_adjustment_clamps_to_ten_percent(module)
    test_unknown_era_rejected(module)


def run_task2_tests(module):
    test_balanced_ancient_city(module)
    test_underdeveloped_city_population_caps_needs(module)
    test_building_reduction_never_goes_below_zero(module)
    test_health_tier_is_independent_of_distress_food(module)
    test_religious_minority_formula(module)
    test_local_happiness_capped_by_population(module)
    test_relative_adjustment_visible_in_breakdown(module)
    test_external_penalties_pass_through_once(module)
    test_zero_population_only_passes_external_penalties(module)
    test_invalid_inputs_rejected(module)
    test_floor_boundary_does_not_round_up(module)


def main():
    module = load_module()
    run_task1_tests(module)
    run_task2_tests(module)
    print("CITY_HAPPINESS_CALCULATOR_TEST: PASS")


if __name__ == "__main__":
    main()
