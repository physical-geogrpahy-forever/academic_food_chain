# Final Generic Unit Roster V1 QA

Date: 2026-09-21  
Status: **PASS**

Authority:
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`
- `city_system/validate_final_generic_unit_roster_v1.py`
- workflow: `.github/workflows/civ-final-unit-roster-qa.yml`

## GitHub Actions result

- Workflow: **Civ Final Unit Roster QA**
- Run ID: **35527600918**
- Head SHA: `93798325946e29ffd699327bc93ba1c74c28e3ed`
- Event: push
- Status: completed
- Conclusion: **success**
- Validator step: **success**

Run:
https://github.com/physical-geogrpahy-forever/academic_food_chain/actions/runs/35527600918

## Validator output

```text
unit_count=85
technology_master_units=73
civic_only_units=7
baseline_system_units=5
duplicate_unit_names=0
forbidden_units_present=0
great_people_present=0
PASS
```

## Structural checks passed

- 85/85 expected units present
- duplicate UNIT_EN: 0
- duplicate UNIT_ID: 0
- unknown primary technology gates: 0
- unknown additional technology gates: 0
- unknown civic gates: 0
- missing domain/role family: 0
- non-locked status rows: 0
- Heavy Chariot present: 0
- Nuclear Missile present: 0
- Giant Death Robot present: 0
- Great People accidentally included: 0
- special-domain sanity checks: PASS

## Reconciliation corrections included in this PASS

- Mechanized Infantry restored to `Combined Arms`
- Missile Cruiser restored to `Guidance Systems + Warships`
- Work Boat domain = SEA
- Caravan domain = LAND
- Cargo Ship domain = SEA

## Interpretation

This PASS locks unit **existence and unlock ownership**. It does not yet lock numerical combat balance, exact direct upgrade edges, production cost, maintenance, promotions, movement, range, or per-unit strategic-resource quantities.
