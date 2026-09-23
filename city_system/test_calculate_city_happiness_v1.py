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


def run_task1_tests(module):
    test_load_expectations_has_13_eras(module)
    test_relative_adjustment_clamps_to_ten_percent(module)
    test_unknown_era_rejected(module)


def main():
    module = load_module()
    run_task1_tests(module)
    print("CITY_HAPPINESS_CALCULATOR_TEST: PASS task1")


if __name__ == "__main__":
    main()
