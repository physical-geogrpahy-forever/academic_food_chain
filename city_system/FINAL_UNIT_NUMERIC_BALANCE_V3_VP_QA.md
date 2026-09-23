# FINAL_UNIT_NUMERIC_BALANCE_V3_VP QA

Date: 2026-09-23
Status: PASS - STRUCTURAL AND RELATIVE NUMERIC LOCK

## Scope

Authoritative file:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`

The table contains 89 project units plus one header row.

Verified line count:

- header: 1
- units: 89
- total lines: 90

## 1. Stat adoption rule

V3 applies the V2 VP audit as follows.

- `VP_DIRECT_ADOPT`: adopt VP combat/ranged/range/moves.
- `VP_ANALOGUE_ADOPT`: adopt the closest VP analogue where the project unit occupies the same battlefield niche.
- `PROJECT_UNIT_RETAIN`: retain project-specific combat statistics where no clean VP analogue exists.
- four explicit role conflicts use `VP_UNIT_ROLE_CONFLICT_RESOLUTION_V2.csv`.

Resolved role conflicts:

- Cavalry -> `MOUNTED_SKIRMISHER`, 40/31, Range 1, Moves 5.
- Anti-Tank Gun -> dedicated `ANTI_ARMOR`, Combat 50, Moves 2.
- Helicopter -> `MOUNTED_SKIRMISHER`, 70/70, Range 1, Moves 6.
- Aircraft Carrier -> `NAVAL_CARRIER`, Combat 70, no organic ranged attack, base cargo 2.

## 2. Production-cost rule

Cost precedence:

1. direct VP unit/class Production cost where available;
2. VP naval or air class-specific anchor;
3. project technology Science cost -> nearest VP TechCost tier -> basic/advanced land cost;
4. project-only naval class interpolation inside the naval family;
5. separate acquisition systems for settlers, religion, conservation, culture and espionage.

Basic land family:

- melee infantry
- gunpowder infantry
- ranged infantry
- recon
- anti-cavalry
- dedicated anti-armor/anti-air guns

Advanced land family:

- mounted units
- mounted skirmishers
- armor
- siege
- super-heavy mobile combat units

## 3. Important cost interpretation

V3 Production costs are now authoritative **relative VP anchors** for unit-to-unit balance.

The following are locked now:

- which units are cheaper or more expensive relative to one another;
- direct VP naval/air cost relationships;
- basic vs advanced land cost family;
- role-conflict assignments;
- strategic-resource requirements already present in the project roster.

The following remains global-calibration work:

- one common Production multiplier, if autoplay shows the entire unit economy is too fast or too slow;
- upgrade-Gold curve after the new Production costs are propagated;
- strategic-resource upkeep magnitude where later supply testing requires it.

Therefore autoplay may multiply the whole cost curve, but should not silently revert individual units to old Civ V BNW costs.

## 4. Separate-system units

No artificial Production cost was inserted for units whose acquisition is intentionally governed elsewhere.

- Settler
- Pioneer
- Colonist
- Urban Planner
- Spy
- Naturalist
- Rock Band

Religious VP Faith anchors are retained:

- Missionary: 200 Faith
- Inquisitor: 300 Faith

Archaeologist retains the VP anchor:

- 450 Production
- 450 Faith

## 5. Project-only naval interpolation

Two project-only hulls require interpolation rather than a direct VP unit copy.

- Galleon: 250 Production, between Caravel and later armored naval progression.
- Ship of the Line: 550 Production, between Frigate and Cruiser-class progression.

These values are relative anchors and remain subject only to the future common global Production multiplier.

## 6. Late-game examples

- Aircraft Carrier: 1800
- Destroyer: 1300
- Bomber: 1500
- Fighter: 1400
- Modern Armor: 2500
- Nuclear Submarine: 2500
- Missile Cruiser: 2500
- Giant Death Robot: 3000
- XCOM Squad: 3000

This eliminates the previous compressed late-game project costs such as 375-550 Production that were inherited from the old Civ V-scale table.

## Final verdict

**PASS.**

`FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv` supersedes `FINAL_UNIT_NUMERIC_BALANCE_V1.csv` and the numeric-decision layer of `FINAL_UNIT_NUMERIC_BALANCE_V2_VP_AUDIT.csv`.

V2 remains the audit trail; V3 is the implementation table.
