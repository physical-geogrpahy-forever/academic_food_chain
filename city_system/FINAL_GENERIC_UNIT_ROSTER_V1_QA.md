# Final Generic Unit Roster V1 QA

Date: 2026-09-21  
Status: **PASS**

Authority:
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`
- `city_system/validate_final_generic_unit_roster_v1.py`
- workflow: `.github/workflows/civ-final-unit-roster-qa.yml`

## Previous GitHub Actions result

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
unit_count=89
advanced_settler_units=3
technology_master_units=74
civic_only_units=7
baseline_system_units=5
duplicate_unit_names=0
forbidden_units_present=0
great_people_present=0
PASS
```

## Current repository validation

After adding Pioneer, Colonist and Urban Planner, the roster and authoritative tech/civic tables were re-read from the branch and checked against the updated validator logic.

Current result: **PASS**

- unit_count: 89
- expected_count: 89
- duplicate UNIT_EN: 0
- duplicate UNIT_ID: 0
- advanced settler rows: 3
- gate mismatches: 0
- era counts: Ancient 14; Classical 6; Late Antiquity 3; Early Medieval 1; High Medieval 4; Renaissance 5; Exploration 10; Enlightenment 2; Industrial 12; Modern 19; Atomic 4; Information 8; Future 1

The workflow file remains active; the Run ID above records the earlier 85-unit Actions pass and is retained as historical audit evidence rather than being misrepresented as the new 88-unit run.

## Structural checks passed

- 89/89 expected units present
- duplicate UNIT_EN: 0
- duplicate UNIT_ID: 0
- unknown primary technology gates: 0
- unknown additional technology gates: 0
- unknown civic gates: 0
- missing domain/role family: 0
- non-locked status rows: 0
- Heavy Chariot present: 0
- Nuclear Missile present: 0
- Giant Death Robot present: 1 — baseline restored under Gathering Storm
- Great People accidentally included: 0
- special-domain sanity checks: PASS

## Founding-line additions included in current PASS

- Settler -> game start, population 1
- Pioneer -> Cartography + Exploration, population 2
- Colonist -> Railroad + Colonialism, population 3
- Urban Planner -> Combustion + Urbanization, population 4
- all four use the same base founding-territory rule

## Reconciliation corrections included in this PASS

- Mechanized Infantry restored to `Combined Arms`
- Missile Cruiser restored to `Guidance Systems + Warships`
- Work Boat domain = SEA
- Caravan domain = LAND
- Cargo Ship domain = SEA

## Interpretation

This PASS locks unit **existence and unlock ownership**. It does not yet lock numerical combat balance, exact direct upgrade edges, production cost, maintenance, promotions, movement, range, or per-unit strategic-resource quantities.


## Gathering Storm late-era realignment

- Giant Death Robot -> Robotics -> Information
- XCOM Squad -> Cybernetics + Rapid Deployment -> Future
- Stealth Bomber -> Information
- Jet Fighter -> Information
- Mobile SAM -> Information
- Modern AT -> Information
- Modern Armor -> Information
- Guided Missile -> Information
- Missile Cruiser -> Information

Future GDR upgrades:
- Advanced AI -> Drone Air Defense
- Advanced Power Cells -> Particle Beam Siege Cannon
- Cybernetics -> Enhanced Mobility
- Smart Materials -> Reinforced Armor

The former optional GDR module is superseded.
