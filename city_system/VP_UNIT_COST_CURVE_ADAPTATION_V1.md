# VP Unit Cost Curve Adaptation V1

Date: 2026-09-23
Status: PROVISIONAL NUMERIC INTEGRATION

## 1. VP rule being adopted

VP does not use one generic era cost for all military units.

It separates:

- basic land classes: melee, gunpowder infantry, ranged infantry, recon
- advanced land classes: mounted, armor, siege and mounted units
- class-specific naval costs
- class-specific air costs
- special civilian/system costs

The project adopts this structure.

## 2. Land cost mapping

Authoritative anchor table:

`city_system/VP_UNIT_COST_CURVE_ADAPTATION_V1.csv`

For every project unit with a technology gate:

1. read the prerequisite technology's provisional project Science cost;
2. find the nearest VP TechCost anchor;
3. use `LAND_BASIC_COST` or `LAND_ADVANCED_COST` according to role family;
4. only interpolate when two adjacent VP anchors are materially closer than a simple nearest-tier assignment;
5. round to a practical production number after full economy testing.

### Basic family

- melee infantry
- gunpowder infantry
- ranged infantry
- recon
- dedicated anti-armor guns unless explicitly treated as advanced mechanized equipment

### Advanced family

- mounted melee
- mounted skirmisher
- armored
- siege
- comparable high-complexity mobile combat units

This means the newly resolved Cavalry and Helicopter use the advanced family.

## 3. Direct VP naval anchors

Where the project has the same class, retain VP class-specific cost before global speed calibration.

| Class | VP cost |
|---|---:|
| Trireme | 120 |
| Caravel | 160 |
| Privateer | 350 |
| Ironclad | 900 |
| Destroyer | 1300 |
| advanced destroyer | 1800 |
| endgame combat ship | 2500 |
| Galleass | 175 |
| Frigate | 375 |
| cruiser-class | 900 |
| dreadnought-class | 1300 |
| Battleship | 1800 |
| Missile Cruiser | 2500 |
| Submarine | 1300 |
| attack submarine | 1800 |
| Nuclear Submarine | 2500 |
| Aircraft Carrier | 1800 |
| supercarrier | 4000 |

Project-only naval classes are interpolated inside the appropriate naval family rather than using the land table.

## 4. Direct VP air anchors

| Class | VP cost |
|---|---:|
| Triplane | 800 |
| Fighter | 1400 |
| Jet Fighter | 2100 |
| early bomber | 850 |
| Bomber | 1500 |
| Stealth Bomber | 2200 |

Aircraft operational range and payload are audited separately from Production cost.

## 5. Civilian and system units

VP anchors:

- Worker: 80 Production
- Work Boat: 40 Production
- Siege Tower: 100 Production / 200 Faith
- Archaeologist: 450 Production / 450 Faith
- Caravan: 90 + 75 per era
- Cargo Ship: 140 + 75 per era
- diplomatic units: 100 + 150 per era
- Missionary: 200 Faith
- Inquisitor: 300 Faith

Project exceptions:

- Settler, Pioneer and Colonist remain governed by the project founding-package system.
- Naturalist, Rock Band, Great People and special support units retain their own acquisition systems.
- Nuclear weapons remain strategic devices rather than a generic Nuclear Missile unit.

## 6. Important integration warning

These VP costs are not yet final project costs.

The project currently has more technologies and more eras than VP, and the current building Production curve has not yet been fully converted to VP's BuildingCost sweep. Therefore direct VP Production numbers are treated as **relative anchors** until:

- building costs are re-swept,
- average city Production by era is measured,
- Standard-speed autoplay is run.

The role hierarchy and cost ratios are adopted now. The global multiplier remains provisional.

## 7. Next V3 unit table

`FINAL_GENERIC_UNIT_NUMERIC_BALANCE_V3` should apply:

- the 56 direct VP combat/stat mappings from V2,
- the 4 role-conflict decisions from `VP_UNIT_ROLE_CONFLICT_RESOLUTION_V2`,
- the cost mapping in this document,
- project-specific interpolation for the remaining units,
- Military Supply and strategic-resource requirements.
