import csv
import importlib.util
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "build_final_building_master_v1.py"
spec = importlib.util.spec_from_file_location("building_merge", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_merge_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        base = root / "base.csv"
        v3 = root / "v3.csv"
        power = root / "power.csv"
        health = root / "health.csv"
        out = root / "out.csv"

        base_fields = [
            "BUILDING_EN", "PROJECT_ERA", "CHAIN", "PRODUCTION_COST",
            "GOLD_MAINTENANCE", "FOOD_FLAT", "PRODUCTION_FLAT", "GOLD_FLAT",
            "SCIENCE_FLAT", "CULTURE_FLAT", "FAITH_FLAT", "LOCAL_HAPPINESS",
            "SPECIALIST_TYPE", "SPECIALIST_SLOTS", "SPECIAL_EFFECTS", "SOURCE_GRADE",
            "NUMERIC_STATUS", "NUMERIC_BASIS", "VP_DISTRESS_REDUCTION",
            "VP_POVERTY_REDUCTION", "VP_ILLITERACY_REDUCTION", "VP_BOREDOM_REDUCTION",
            "VP_RELIGIOUS_UNREST_REDUCTION", "HEALTH_POINTS_PROVISIONAL",
            "STABILITY_POINTS_PROVISIONAL", "VP_AUDIT_STATUS", "VP_AUDIT_REASON",
        ]

        def base_row(
            name,
            era="Industrial",
            local_happiness="0",
            effects="OLD",
            health="0",
            stability="0",
        ):
            row = {k: "" for k in base_fields}
            row.update(
                BUILDING_EN=name,
                PROJECT_ERA=era,
                CHAIN="X",
                PRODUCTION_COST="100",
                GOLD_MAINTENANCE="1",
                FOOD_FLAT="0",
                PRODUCTION_FLAT="0",
                GOLD_FLAT="0",
                SCIENCE_FLAT="0",
                CULTURE_FLAT="0",
                FAITH_FLAT="0",
                LOCAL_HAPPINESS=local_happiness,
                SPECIALIST_SLOTS="0",
                SPECIAL_EFFECTS=effects,
                VP_DISTRESS_REDUCTION="0",
                VP_POVERTY_REDUCTION="0",
                VP_ILLITERACY_REDUCTION="0",
                VP_BOREDOM_REDUCTION="0",
                VP_RELIGIOUS_UNREST_REDUCTION="0",
                HEALTH_POINTS_PROVISIONAL=health,
                STABILITY_POINTS_PROVISIONAL=stability,
            )
            return row

        write_csv(
            base,
            base_fields,
            [
                base_row("Factory"),
                base_row("Research Lab", "Modern"),
                base_row("Food Market"),
                base_row("Aquatics Center", "Modern", "2"),
                base_row("Coal Power Plant"),
                base_row("Aqueduct", "Classical", health="2"),
                base_row("Courthouse", "Ancient", stability="2"),
            ],
        )

        v3_fields = [
            "BUILDING_EN", "ACTION", "PROJECT_ERA", "CHAIN", "PRODUCTION_COST",
            "GOLD_MAINTENANCE", "FOOD_FLAT", "PRODUCTION_FLAT", "GOLD_FLAT",
            "SCIENCE_FLAT", "CULTURE_FLAT", "FAITH_FLAT", "SPECIALIST_TYPE",
            "SPECIALIST_SLOTS", "SPECIAL_EFFECTS", "NUMERIC_STATUS", "VP_AUDIT_STATUS",
            "RATIONALE",
        ]
        write_csv(
            v3,
            v3_fields,
            [
                {
                    "BUILDING_EN": "Smokehouse", "ACTION": "ADD", "PROJECT_ERA": "Ancient",
                    "CHAIN": "FOOD_HEALTH", "PRODUCTION_COST": "75", "GOLD_MAINTENANCE": "1",
                    "FOOD_FLAT": "0", "PRODUCTION_FLAT": "0", "GOLD_FLAT": "0",
                    "SCIENCE_FLAT": "0", "CULTURE_FLAT": "0", "FAITH_FLAT": "0",
                    "SPECIALIST_TYPE": "", "SPECIALIST_SLOTS": "0",
                    "SPECIAL_EFFECTS": "CAMP_PRODUCTION=+1", "NUMERIC_STATUS": "V3",
                    "VP_AUDIT_STATUS": "ADOPT", "RATIONALE": "fixture",
                },
                {
                    "BUILDING_EN": "Factory", "ACTION": "OVERRIDE_SPECIAL_EFFECT",
                    "PROJECT_ERA": "Industrial", "CHAIN": "INDUSTRY_POWER",
                    "PRODUCTION_COST": "360", "GOLD_MAINTENANCE": "3", "FOOD_FLAT": "0",
                    "PRODUCTION_FLAT": "10", "GOLD_FLAT": "0", "SCIENCE_FLAT": "0",
                    "CULTURE_FLAT": "0", "FAITH_FLAT": "0", "SPECIALIST_TYPE": "Engineer",
                    "SPECIALIST_SLOTS": "1", "SPECIAL_EFFECTS": "PROJECT_MANUFACTORY_PRODUCTION=+1",
                    "NUMERIC_STATUS": "V3", "VP_AUDIT_STATUS": "ADOPT", "RATIONALE": "fixture",
                },
            ],
        )

        power_fields = [
            "BUILDING_EN", "ACTION", "POWER_LOAD", "POWERED_BONUS",
            "BASE_NUMERIC_CHANGE", "POWER_SOURCE_RULE", "STATUS", "RATIONALE",
        ]
        write_csv(
            power,
            power_fields,
            [
                {"BUILDING_EN": "Factory", "ACTION": "ADD_POWER_LAYER", "POWER_LOAD": "2", "POWERED_BONUS": "Production+3", "BASE_NUMERIC_CHANGE": "", "POWER_SOURCE_RULE": "", "STATUS": "x", "RATIONALE": "x"},
                {"BUILDING_EN": "Food Market", "ACTION": "ADD_POWER_LAYER", "POWER_LOAD": "1", "POWERED_BONUS": "Food+2", "BASE_NUMERIC_CHANGE": "", "POWER_SOURCE_RULE": "", "STATUS": "x", "RATIONALE": "x"},
                {"BUILDING_EN": "Aquatics Center", "ACTION": "ADD_POWER_LAYER", "POWER_LOAD": "2", "POWERED_BONUS": "Local Happiness+2", "BASE_NUMERIC_CHANGE": "Local Happiness 2 -> 1", "POWER_SOURCE_RULE": "", "STATUS": "x", "RATIONALE": "x"},
                {"BUILDING_EN": "Coal Power Plant", "ACTION": "RESOLVE_POWER_SOURCE", "POWER_LOAD": "0", "POWERED_BONUS": "", "BASE_NUMERIC_CHANGE": "", "POWER_SOURCE_RULE": "Coal capacity 1 -> 4 Power", "STATUS": "x", "RATIONALE": "x"},
            ],
        )

        health_fields = [
            "BUILDING", "PROJECT_ERA", "HEALTH_EFFECT_TYPE", "HEALTH_VALUE",
            "SPONTANEOUS_PLAGUE_RISK_MULT", "PLAGUE_DURATION_MOD_TURNS", "OTHER_EFFECT",
            "STATUS", "BASIS",
        ]
        write_csv(
            health,
            health_fields,
            [
                {"BUILDING": "Food Market", "PROJECT_ERA": "Industrial", "HEALTH_EFFECT_TYPE": "FLAT", "HEALTH_VALUE": "1", "SPONTANEOUS_PLAGUE_RISK_MULT": "1.00", "PLAGUE_DURATION_MOD_TURNS": "0", "OTHER_EFFECT": "", "STATUS": "x", "BASIS": "x"},
                {"BUILDING": "Aqueduct", "PROJECT_ERA": "Classical", "HEALTH_EFFECT_TYPE": "WATER_HEALTH_FLOOR", "HEALTH_VALUE": "2", "SPONTANEOUS_PLAGUE_RISK_MULT": "1.00", "PLAGUE_DURATION_MOD_TURNS": "0", "OTHER_EFFECT": "nonstack", "STATUS": "x", "BASIS": "x"},
                {"BUILDING": "Factory", "PROJECT_ERA": "Industrial", "HEALTH_EFFECT_TYPE": "NONE", "HEALTH_VALUE": "0", "SPONTANEOUS_PLAGUE_RISK_MULT": "1.00", "PLAGUE_DURATION_MOD_TURNS": "0", "OTHER_EFFECT": "pollution", "STATUS": "x", "BASIS": "x"},
            ],
        )

        rows = module.build(base, v3, power, health, out)
        by_name = {r["BUILDING_EN"]: r for r in rows}

        assert by_name["Smokehouse"]["PRODUCTION_COST"] == "75"
        assert by_name["Smokehouse"]["LOCAL_HAPPINESS"] == "0"
        for field in (
            "VP_DISTRESS_REDUCTION",
            "VP_POVERTY_REDUCTION",
            "VP_ILLITERACY_REDUCTION",
            "VP_BOREDOM_REDUCTION",
            "VP_RELIGIOUS_UNREST_REDUCTION",
        ):
            assert by_name["Smokehouse"][field] == "0", (field, by_name["Smokehouse"][field])
        assert by_name["Factory"]["SPECIAL_EFFECTS"] == "PROJECT_MANUFACTORY_PRODUCTION=+1"
        assert by_name["Factory"]["POWER_LOAD"] == "2"
        assert by_name["Food Market"]["POWERED_BONUS"] == "Food+2"
        assert by_name["Food Market"]["HEALTH_POINTS_FINAL"] == "1"
        assert by_name["Aquatics Center"]["LOCAL_HAPPINESS"] == "1"
        assert by_name["Coal Power Plant"]["POWER_SOURCE_RULE"].startswith("Coal capacity")
        assert by_name["Aqueduct"]["HEALTH_EFFECT_TYPE"] == "WATER_HEALTH_FLOOR"
        assert by_name["Aqueduct"]["HEALTH_POINTS_FINAL"] == "2"
        assert by_name["Courthouse"]["STABILITY_POINTS_FINAL"] == "2"
        assert by_name["Smokehouse"]["STABILITY_POINTS_FINAL"] == "0"
        assert len({r["BUILDING_EN"] for r in rows}) == len(rows)


if __name__ == "__main__":
    test_merge_fixture()
    print("BUILDING_MASTER_MERGE_TEST: PASS")
