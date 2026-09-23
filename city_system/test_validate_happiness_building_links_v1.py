from __future__ import annotations

import csv
import importlib.util
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "validate_happiness_building_links_v1.py"

REQUIRED = [
    "BUILDING_EN",
    "LOCAL_HAPPINESS",
    "VP_DISTRESS_REDUCTION",
    "VP_POVERTY_REDUCTION",
    "VP_ILLITERACY_REDUCTION",
    "VP_BOREDOM_REDUCTION",
    "VP_RELIGIOUS_UNREST_REDUCTION",
    "HEALTH_POINTS_FINAL",
    "STABILITY_POINTS_FINAL",
]


def load_module():
    if not MODULE_PATH.exists():
        raise AssertionError("validate_happiness_building_links_v1.py does not exist yet")
    spec = importlib.util.spec_from_file_location("happiness_building_validator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def row(name: str, **overrides):
    data = {field: "0" for field in REQUIRED}
    data["BUILDING_EN"] = name
    data.update({k: str(v) for k, v in overrides.items()})
    return data


def valid_rows():
    return [
        row("Distress Hall", VP_DISTRESS_REDUCTION=1),
        row("Poverty Hall", VP_POVERTY_REDUCTION=1),
        row("School", VP_ILLITERACY_REDUCTION=1),
        row("Theater", VP_BOREDOM_REDUCTION=1),
        row("Temple", VP_RELIGIOUS_UNREST_REDUCTION=1, HEALTH_POINTS_FINAL=2, STABILITY_POINTS_FINAL=1),
    ]


def assert_fails(fn, contains: str):
    try:
        fn()
    except (AssertionError, ValueError) as exc:
        assert contains.lower() in str(exc).lower(), (contains, str(exc))
    else:
        raise AssertionError(f"Expected failure containing {contains!r}")


def test_valid_fixture(module, root: Path):
    master = root / "valid.csv"
    write_csv(master, REQUIRED, valid_rows())
    result = module.validate_building_links(master)
    assert result["rows"] == 5
    assert result["distress_sources"] == 1
    assert result["poverty_sources"] == 1
    assert result["illiteracy_sources"] == 1
    assert result["boredom_sources"] == 1
    assert result["religious_sources"] == 1


def test_missing_distress_column_fails(module, root: Path):
    path = root / "missing_distress.csv"
    fields = [f for f in REQUIRED if f != "VP_DISTRESS_REDUCTION"]
    rows = [{k: v for k, v in r.items() if k in fields} for r in valid_rows()]
    write_csv(path, fields, rows)
    assert_fails(lambda: module.validate_building_links(path), "VP_DISTRESS_REDUCTION")


def test_negative_local_happiness_fails(module, root: Path):
    path = root / "negative_local.csv"
    rows = valid_rows()
    rows[0]["LOCAL_HAPPINESS"] = "-1"
    write_csv(path, REQUIRED, rows)
    assert_fails(lambda: module.validate_building_links(path), "LOCAL_HAPPINESS")


def test_nonnumeric_need_fails(module, root: Path):
    path = root / "nonnumeric_need.csv"
    rows = valid_rows()
    rows[2]["VP_ILLITERACY_REDUCTION"] = "not-a-number"
    write_csv(path, REQUIRED, rows)
    assert_fails(lambda: module.validate_building_links(path), "VP_ILLITERACY_REDUCTION")


def test_cross_system_guard_columns_required(module, root: Path):
    for missing in ("HEALTH_POINTS_FINAL", "STABILITY_POINTS_FINAL"):
        path = root / f"missing_{missing}.csv"
        fields = [f for f in REQUIRED if f != missing]
        rows = [{k: v for k, v in r.items() if k in fields} for r in valid_rows()]
        write_csv(path, fields, rows)
        assert_fails(lambda path=path: module.validate_building_links(path), missing)


def main():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        test_valid_fixture(module, root)
        test_missing_distress_column_fails(module, root)
        test_negative_local_happiness_fails(module, root)
        test_nonnumeric_need_fails(module, root)
        test_cross_system_guard_columns_required(module, root)
    print("HAPPINESS_BUILDING_LINK_TEST: PASS")


if __name__ == "__main__":
    main()
