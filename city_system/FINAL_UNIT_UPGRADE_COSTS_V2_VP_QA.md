# Unit Upgrade Gold V2 VP QA

Date: 2026-09-23
Status: PASS WITH THREE AUTOPLAY WATCH EDGES

## Authoritative table

- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`

Coverage:

- 55 upgrade edges from the locked upgrade graph
- V3 Production costs from `FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`

## 1. Why V1 formula was replaced

V1 used an era multiplier on top of the old compressed Civ V-style Production costs.

After unit V3, Production costs already follow the Vox Populi tech-tier cost curve. Reusing the V1 era multiplier would double-count late-era scaling and make several upgrades disproportionately expensive.

## 2. Current Vox Populi formula

Current VP code calculates base unit upgrade Gold from Production-cost difference:

`raw = BASE_UNIT_UPGRADE_COST + max(0, NewCost - OldCost) * UNIT_UPGRADE_COST_PER_PRODUCTION`

Current VP defines used in this pass:

- `BASE_UNIT_UPGRADE_COST = 10`
- `UNIT_UPGRADE_COST_PER_PRODUCTION = 1.25`
- `UNIT_UPGRADE_COST_MULTIPLIER_PER_ERA = 0.0`
- `UNIT_UPGRADE_COST_EXPONENT = 1.0`
- visible divisor = 5

Therefore project V2 uses:

`Gold = floor_to_5(10 + 1.25 * max(0, ToProduction - FromProduction))`

No extra era multiplier is applied.

## 3. Examples

- Warrior 40 -> Swordsman 100: 85 Gold
- Spearman 70 -> Pikeman 160: 120 Gold
- Crossbowman 300 -> Skirmisher 625: 415 Gold
- Caravel 160 -> Ironclad 900: 935 Gold
- Cavalry 800 -> Helicopter 2250: 1820 Gold
- Fighter 1400 -> Jet Fighter 2100: 885 Gold
- Paratrooper 1300 -> XCOM Squad 3000: 2135 Gold

This follows the same VP formula at every era and lets the already-adopted Production curve carry the late-game scaling.

## 4. Equal-cost watch edges

Three project upgrade pairs have the same V3 Production cost:

- Trebuchet 350 -> Bombard 350
- Rifleman 900 -> Infantry 900
- Landship 1800 -> Tank 1800

The source-exact VP formula therefore gives the minimum 10 Gold.

These are tagged:

`VP_SOURCE_EXACT_AUTOPLAY_WATCH_EQUAL_COST`

No arbitrary floor is introduced before testing because the adopted source explicitly defines the formula. If autoplay shows repeated exploitative mass upgrading, the preferred fix is to revisit the adjacent unit Production anchors first, rather than hiding a cost-curve problem behind a special Gold floor.

## 5. Air-unit context

The four air upgrade edges retain the existing project requirement `CITY_WITH_AIR_BASING`:

- Great War Bomber -> Bomber
- Bomber -> Stealth Bomber
- Triplane -> Fighter
- Fighter -> Jet Fighter

All other rows retain `FRIENDLY_TERRITORY_STANDARD` unless their operational rules already impose additional restrictions.

## 6. Branch upgrades

Frigate retains two explicit branch options:

- Frigate -> Ship of the Line
- Frigate -> Cruiser

Both use the same VP difference formula against their respective V3 target Production costs.

## 7. Strategic resources

This table calculates Gold only.

Target-unit strategic-resource requirements remain enforced separately. Paying the Gold upgrade cost does not bypass Horses, Iron, Oil, Aluminum, Uranium or other target-unit requirements defined by the unit roster/resource system.

## Final verdict

**PASS.**

`FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv` supersedes the Gold values in `FINAL_UNIT_UPGRADE_COSTS_V1.csv` while retaining the locked upgrade graph and operational contexts.
