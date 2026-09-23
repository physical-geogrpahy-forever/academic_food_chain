import csv
import importlib.util
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "validate_final_building_master_v1.py"
spec = importlib.util.spec_from_file_location("building_validator", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_fixture(root, stability_final="2"):
    roster = root / "roster.csv"
    roster_v3 = root / "roster_v3.csv"
    master = root / "master.csv"
    tech = root / "tech.csv"
    civic = root / "civic.csv"

    roster_fields = ["BUILDING_EN", "TECH_GATE", "CIVIC_GATE"]
    write_csv(
        roster,
        roster_fields,
        [
            {"BUILDING_EN": "Aqueduct", "TECH_GATE": "Engineering", "CIVIC_GATE": ""},
            {"BUILDING_EN": "Courthouse", "TECH_GATE": "Writing", "CIVIC_GATE": "Code of Laws"},
            {"BUILDING_EN": "Coal Power Plant", "TECH_GATE": "Electricity", "CIVIC_GATE": ""},
        ],
    )

    write_csv(
        roster_v3,
        ["BUILDING_EN", "ACTION", "TECH_GATE", "CIVIC_GATE"],
        [
            {"BUILDING_EN": "Smokehouse", "ACTION": "ADD", "TECH_GATE": "Trapping", "CIVIC_GATE": ""},
        ],
    )

    master_fields = [
        "BUILDING_EN", "SPECIAL_EFFECTS", "HEALTH_EFFECT_TYPE", "HEALTH_POINTS_FINAL",
        "HEALTH_POINTS_PROVISIONAL", "STABILITY_POINTS_PROVISIONAL", "STABILITY_POINTS_FINAL",
        "POWER_LOAD", "POWER_SOURCE_RULE", "POWERED_BONUS",
    ]
    write_csv(
        master,
        master_fields,
        [
            {"BUILDING_EN": "Aqueduct", "SPECIAL_EFFECTS": "HEALTH_SYSTEM_EFFECT=HEALTH_V1", "HEALTH_EFFECT_TYPE": "WATER_HEALTH_FLOOR", "HEALTH_POINTS_FINAL": "2", "HEALTH_POINTS_PROVISIONAL": "2", "STABILITY_POINTS_PROVISIONAL": "0", "STABILITY_POINTS_FINAL": "0", "POWER_LOAD": "0", "POWER_SOURCE_RULE": "", "POWERED_BONUS": ""},
            {"BUILDING_EN": "Courthouse", "SPECIAL_EFFECTS": "", "HEALTH_EFFECT_TYPE": "NONE", "HEALTH_POINTS_FINAL": "0", "HEALTH_POINTS_PROVISIONAL": "0", "STABILITY_POINTS_PROVISIONAL": "2", "STABILITY_POINTS_FINAL": stability_final, "POWER_LOAD": "0", "POWER_SOURCE_RULE": "", "POWERED_BONUS": ""},
            {"BUILDING_EN": "Coal Power Plant", "SPECIAL_EFFECTS": "POWER_SYSTEM_OUTPUT=POWER_V4", "HEALTH_EFFECT_TYPE": "NONE", "HEALTH_POINTS_FINAL": "0", "HEALTH_POINTS_PROVISIONAL": "0", "STABILITY_POINTS_PROVISIONAL": "0", "STABILITY_POINTS_FINAL": "0", "POWER_LOAD": "0", "POWER_SOURCE_RULE": "Coal capacity 1 -> 4 Power", "POWERED_BONUS": ""},
            {"BUILDING_EN": "Smokehouse", "SPECIAL_EFFECTS": "", "HEALTH_EFFECT_TYPE": "NONE", "HEALTH_POINTS_FINAL": "0", "HEALTH_POINTS_PROVISIONAL": "", "STABILITY_POINTS_PROVISIONAL": "", "STABILITY_POINTS_FINAL": "0", "POWER_LOAD": "0", "POWER_SOURCE_RULE": "", "POWERED_BONUS": ""},
        ],
    )

    write_csv(
        tech,
        ["TECH_EN", "CITY_BUILDINGS", "SYSTEMS_NOTES"],
        [
            {"TECH_EN": "Engineering", "CITY_BUILDINGS": "Aqueduct", "SYSTEMS_NOTES": ""},
            {"TECH_EN": "Writing", "CITY_BUILDINGS": "Library", "SYSTEMS_NOTES": "Courthouse additionally requires Code of Laws"},
            {"TECH_EN": "Electricity", "CITY_BUILDINGS": "Coal Power Plant", "SYSTEMS_NOTES": ""},
            {"TECH_EN": "Trapping", "CITY_BUILDINGS": "Smokehouse", "SYSTEMS_NOTES": ""},
        ],
    )

    write_csv(
        civic,
        ["CIVIC_EN", "FINAL_UNLOCKS_SYSTEMS"],
        [
            {"CIVIC_EN": "Code of Laws", "FINAL_UNLOCKS_SYSTEMS": "Courthouse with Writing"},
        ],
    )

    return roster, roster_v3, master, tech, civic


def test_validator_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        paths = make_fixture(Path(tmp))
        result = module.validate(*paths)
        assert result["roster_rows"] == 4
        assert result["master_rows"] == 4


def test_validator_rejects_stability_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        paths = make_fixture(Path(tmp), stability_final="1")
        try:
            module.validate(*paths)
        except AssertionError as exc:
            assert "Stability" in str(exc)
        else:
            raise AssertionError("validator accepted mismatched provisional/final Stability")


if __name__ == "__main__":
    test_validator_fixture()
    test_validator_rejects_stability_mismatch()
    print("FINAL_BUILDING_MASTER_QA_TEST: PASS")
