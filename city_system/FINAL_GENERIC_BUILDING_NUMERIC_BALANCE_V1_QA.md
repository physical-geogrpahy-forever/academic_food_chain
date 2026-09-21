# Final Generic Building Numeric Balance V1 QA

Date: 2026-09-21  
Status: **STRUCTURAL PASS / SOURCE-FINALITY PARTIAL**

Authorities:
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.md`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_SOURCE_AUDIT_V1.md`
- `city_system/validate_final_generic_building_numeric_balance_v1.py`

## Current result

- canonical building rows: **102**
- numeric building rows: **102**
- duplicate building names: **0**
- missing numeric rows: **0**
- era mismatches between roster/numeric table: **0**
- chain mismatches: **0**
- invalid source grades: **0**
- locked rows: **83**
- mod-source re-audit rows: **19**
- Great Work type/slot mismatches: **0**
- specialist type/slot mismatches: **0**
- flat GPP without a GPP type: **0**
- building-prerequisite era regressions: **0**
- representative Civ V anchor mismatches: **0**
- government-building adaptation-rule mismatches: **0**
- source-specific power plants missing replacement semantics: **0**
- result: **PASS**

## Source-grade distribution

- A_CIV5_BNW_EXACT: **45**
- B_CIV5_FUNCTIONAL_REMAP: **4**
- B_CIV6_ADAPTED: **31**
- B_EE_ADAPTED: **4**
- B_PROJECT_INTERPOLATED: **18**

Total: **102**

## Era distribution after prerequisite correction

- Ancient: 12
- Classical: 16
- Late Antiquity: 4
- Early Medieval: 4
- High Medieval: 4
- High Medieval/Exploration: 3
- Renaissance: **6**
- Exploration: **8**
- Enlightenment: 11
- Industrial: 16
- Modern: 12
- Atomic: 2
- Information: 3
- Future: 1

Art Museum moved from Renaissance to Exploration because it requires Opera House, which is an Exploration building.

## Important protected decisions

### Advanced founding units
Ancestral Hall:
- founding-unit Production +50%
- **NO FREE WORKER**

This validator protects the project-wide rule that settlement never creates a free Worker.

### Government buildings
- Governor titles removed
- Governor-only effects translated or omitted
- Grand Master's Chapel has no invented flat Faith
- National History Museum = 4 ANY Great Work slots
- Royal Society does not consume persistent Workers

### Power
Coal / Nuclear / Solar Plant:
- all use `REPLACES_POWER_PLANT_OUTPUT=1`
- their outputs therefore replace rather than double-stack the generic source layer

### Conditional technology/civic bonuses
Conditional bonuses from `NUMERIC_BALANCE_DECISIONS_V1.csv` are referenced through special-effect tags rather than being silently double-counted in base yields.

## System placeholders

Health, electric Power accounting and pollution still contain explicit `PENDING` tags where the **external system** is not finalized.

These do not invalidate the building row:
- cost is locked
- maintenance is locked
- normal yields are locked
- only the external-system accounting remains separate

## GitHub Actions

Workflow:
`.github/workflows/civ-final-building-numeric-balance-qa.yml`

Do not claim a completed Actions run until one is retrieved.
The PASS above comes from re-reading the current authoritative branch and reproducing the structural/anchor checks directly.


## Mod-aware source re-audit

The previous QA incorrectly treated all 102 numeric rows as equally final.

Current authoritative distinction:
- 83 rows remain `LOCKED_BUILDING_V1`
- 19 rows are `MOD_SOURCE_REAUDIT_REQUIRED`

Re-audit manifest:
`city_system/BUILDING_MOD_SOURCE_REAUDIT_V2.csv`

Source-precedence authority:
`city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md`

The structural validator may still PASS while these 19 rows remain under source audit.  
Therefore **STRUCTURAL PASS is not the same as SOURCE-FINALITY PASS**.

Known corrected Enlightenment Era effects:
- Cloth Mill source effect restored
- Gunsmith source effect restored
- Drydock source effect restored
