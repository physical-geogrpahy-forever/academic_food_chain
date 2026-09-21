# Final Unit Numeric Balance V1 QA

Date: 2026-09-21  
Status: **PASS — current repository structural validation**

Authorities:
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V1.csv`
- `city_system/validate_final_unit_numeric_balance_v1.py`

## Current validation

- canonical unit rows: **89**
- numeric rows: **89**
- locked military/system numeric rows: **80**
- intentionally deferred system-economy rows: **9**
- direct Gold upgrade-cost rows: **55**
- duplicate numeric unit names: **0**
- missing canonical units: **0**
- role/era mismatches: **0**
- strategic-resource mismatches against canonical roster: **0**
- nonzero strategic-resource per-turn upkeep introduced: **0**
- direct-upgrade combat-power regressions: **0**
- upgrade-cost edge mismatches: **0**
- upgrade-cost formula mismatches: **0**
- founding-unit production replacements incorrectly priced as Gold upgrades: **0**
- result: **PASS**

## Deferred system-economy rows

Exactly nine:
- Settler
- Pioneer
- Colonist
- Urban Planner
- Missionary
- Inquisitor
- Spy
- Naturalist
- Rock Band

These are not accidental blanks. Their acquisition cost belongs to founding, Faith, espionage, conservation or cultural systems.

## Strategic-resource baseline

Current resource-required unit rows inherited from the canonical roster:

- Chariot Archer -> Horses
- Horseman -> Horses
- Swordsman -> Iron
- Fire Lance -> Niter
- Lancer -> Horses
- Bombard -> Niter
- Tank -> Oil
- Destroyer -> Oil
- Stealth Bomber -> Aluminum
- Jet Fighter -> Aluminum
- Giant Death Robot -> Uranium

For V1:
- each listed unit reserves 1 strategic-resource slot;
- per-turn strategic-resource upkeep = 0;
- no blank resource requirement was filled by invention during this pass.

## Upgrade Gold costs

The table contains 55 direct Gold-upgrade edges.

Founding progression is excluded:
- Settler -> Pioneer
- Pioneer -> Colonist
- Colonist -> Urban Planner

because those are production replacements, not direct unit upgrades.

The validator recalculates every Gold cost from production costs and the compressed Civ V era multiplier and requires rounding to the nearest lower 5 Gold.

## Anchor checks

The validator hard-locks representative values so they cannot drift silently, including:
- Warrior 8 / 40
- Swordsman 14 / 75
- Archer 5/7 / 40
- Crossbowman 13/18 / 120
- Cavalry 34 / 225
- Tank 70 / 375
- Modern Armor 100 / 425
- Artillery 21/28 / 250
- Rocket Artillery 45/60 / 425
- Frigate 25/28 / 185
- Battleship 55/65 / 375
- Missile Cruiser 80/100 / 425
- XCOM Squad 100 / 400
- Giant Death Robot 150/100 / 550 project hybrid

## GitHub Actions

Workflow:
`.github/workflows/civ-final-unit-numeric-balance-qa.yml`

A current completed Actions run ID has **not** been retrieved through the connected GitHub endpoint, so none is claimed here.

The PASS above is from re-reading the current branch files and reproducing the validator checks directly.


## Aircraft Carrier cargo correction

A later source audit corrected Carrier base cargo from 3 to the Civ V BNW value of **2**.

- base capacity: 2
- Flight Deck I: 3
- Flight Deck II: 4
- Flight Deck III: 5

This correction is validated by `validate_final_unit_operational_rules_v1.py`.
