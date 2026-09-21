# Final Unit Numeric Balance V1

Date: 2026-09-21  
Status: **MILITARY NUMERIC BASELINE LOCKED V1**

Authorities:
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`

## 1. Scope

This pass assigns the first canonical numerical baseline for the 89 generic non-Great-Person units.

Fields covered:
- Combat Strength
- Ranged Combat Strength
- attack/operational Range
- Movement
- Production Cost
- interception range
- paradrop range
- cargo capacity
- strategic-resource slot requirement
- strategic-resource per-turn upkeep
- Gold maintenance rule
- military supply rule
- source grade
- source/balance rationale

The table does **not** yet assign:
- promotion-tree bonuses
- anti-class percentage modifiers
- city-attack modifiers
- terrain modifiers
- healing aura magnitude
- interception probability
- evasion probability
- air sweep details
- nuclear-device delivery rules

Those belong to the next promotion/special-ability pass.

## 2. Primary scale

The project uses a **Civilization V BNW numerical scale** as the principal military/economic scale.

Where an adopted unit exists directly in Civ V BNW, its BNW strength, movement, range and production cost are retained whenever they still fit the project's role.

Examples:
- Warrior: 8 Strength, 2 Moves, 40 Production
- Swordsman: 14, 2, 75
- Rifleman: 34, 2, 225
- Cavalry: 34, 4, 225
- Tank: 70, 5, 375
- Modern Armor: 100, 5, 425
- Archer: 5 / 7 ranged, Range 2, 40 Production
- Crossbowman: 13 / 18, Range 2, 120
- Gatling Gun: 30 / 30, Range 1, 225
- Machine Gun: 60 / 60, Range 1, 350
- Artillery: 21 / 28, Range 3, 250
- Rocket Artillery: 45 / 60, Range 3, 425
- Frigate: 25 / 28, Range 2, 5 Moves, 185
- Battleship: 55 / 65, Range 3, 5 Moves, 375
- Missile Cruiser: 80 / 100, Range 3, 7 Moves, 425
- XCOM Squad: 100 Strength, Paradrop 40, 400 Production

## 3. Added and remapped units

A unit not present in the Civ V BNW generic roster is not assigned an arbitrary independent scale.

It is placed between known anchors in its locked upgrade family.

### Infantry chronology

Project:
`Warrior -> Swordsman -> Man-at-Arms -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry`

V1 values:
- Warrior 8
- Swordsman 14
- Man-at-Arms 21
- Arquebusier 24
- Line Infantry 28
- Rifleman 34
- Infantry 50
- Mechanized Infantry 70

Interpretation:
- Man-at-Arms uses the Civ V Longswordsman 21/120 anchor.
- Arquebusier uses the Civ V Musketman 24/150 anchor.
- Line Infantry is interpolated between Musketman and Rifleman.
- project Infantry occupies the Civ V Great War Infantry 50/320 stage.
- project Mechanized Infantry occupies the Civ V Infantry 70/375 stage because it unlocks at the project's earlier Combined Arms point.

This prevents the project from compressing both Civ V Great War Infantry and Infantry into one 70-strength Industrial unit and then immediately jumping to native Civ V Mechanized Infantry 90.

### Enlightenment Era / project intermediates

Examples:
- Skirmisher: 18 / 24, Range 2, cost 160
- Field Gun: 18 / 24, Range 2, cost 220
- Ship of the Line: 30 / 37, Range 2, cost 220
- Cruiser: 45 / 55, Range 2, 6 Moves, cost 300
- Explorer: 16 Strength, 3 Moves, cost 120

These are interpolation/adaptation rows and are explicitly identified as such in `SOURCE_GRADE`.

## 4. Source grades

### A_CIV5_BNW_EXACT
Direct Civ V BNW value retained.

### A_CIV5_BNW_XML
Direct Civ V BNW XML/database value retained where ordinary summary references are less convenient.

### A_CIV5_BNW_ANCHOR
Very close Civ V identity/value retained but the project's role classification differs.

### B_CIV5_STAGE_REMAP
A Civ V value is directly reused for a different project stage/name.

Examples:
- Man-at-Arms <- Longswordsman anchor
- Arquebusier <- Musketman anchor
- Infantry <- Great War Infantry anchor
- Mechanized Infantry <- Infantry anchor

### B_PROJECT_INTERPOLATED
Value interpolated between direct Civ V anchors in the same project upgrade family.

### B_EE_PROJECT_ADAPTED
Pouakai Enlightenment Era unit/function adopted, then placed on the Civ V numerical curve.

### B_CIV5_CIV6_HYBRID
Cross-game hybrid used only where neither game's value alone matches the adopted project implementation.

Current main example:
- Giant Death Robot: 150 Combat, 100 Ranged, Range 3, 5 Moves, 550 Production.

### C_CIV6_ADAPTED / C_CIV6_SCALED
Civilization VI / Gathering Storm unit adopted and converted to the lower Civ V combat/production scale.

### D_SYSTEM_DEFERRED
The unit exists, but its economic purchase/production value belongs to a different system.

Current deferred economic rows:
- Settler
- Pioneer
- Colonist
- Urban Planner
- Missionary
- Inquisitor
- Spy
- Naturalist
- Rock Band

These rows are **not missing data by accident**.

## 5. Founding units

The four founding units deliberately do not receive Production Cost in this military pass.

Reason:
- Pioneer, Colonist and Urban Planner provide increasingly large free-building packages;
- therefore their correct cost cannot be inferred from ordinary military production curves;
- assigning a military-style cost before pricing the value of the free infrastructure would systematically underprice them.

Their movement remains 2.

Their economic cost will be locked in the founding-economy pass.

## 6. Religious, cultural and off-map civilians

Missionary, Inquisitor, Naturalist and Rock Band use their own Faith/system acquisition models rather than ordinary military Production.

Spy is off-map and has no map movement or production value in this table.

Archaeologist remains a production-built Civ V-style civilian and therefore retains a production value.

## 7. Gold maintenance

V1 does **not invent a fixed per-unit Gold maintenance column**.

The project keeps the Civ V-style global unit-maintenance model:
`GLOBAL_CIV5_FORMULA`

This is intentional because Civ V unit maintenance is calculated at empire level from the paid-unit count and game progression rather than being a simple permanent value attached to each unit row.

Trade units use:
`GLOBAL_CIV5_FORMULA_TRADE_SUPPLY_EXEMPT`

Their trade/supply treatment remains distinct from ordinary military supply.

## 8. Military supply

Baseline:
- normal units: `ONE_SUPPLY`
- Caravan / Cargo Ship: `SUPPLY_EXEMPT`

This is a unit-cap / army-support rule, not Gold maintenance.

System-purchased civilians may be revisited when their own economies are finalized, but no new exception is invented in V1.

## 9. Strategic resources

The project keeps a **Civ V-style stock-slot reservation baseline** rather than silently converting the entire game to Gathering Storm's per-turn strategic-resource economy.

For resources already explicitly owned by the canonical unit roster:
- `RESOURCE_SLOT_COST = 1`
- `RESOURCE_UPKEEP_PER_TURN = 0`

Examples include:
- Horses
- Iron
- Niter
- Oil
- Aluminum
- Uranium

A blank strategic-resource field is not interpreted as permission to invent a new requirement during this numeric pass.

Even though Gathering Storm's GDR uses a per-turn Uranium system, the project GDR currently uses the project's existing Uranium slot model. A future whole-economy strategic-resource-flow redesign would have to change **all** relevant units together, not GDR alone.

## 10. Air-unit movement

Air units use:
- `MOVES = 0`
- `RANGE = operational strike/rebase combat range`

They are not ordinary tile-moving land units.

The fighter/bomber progression is:
- Triplane: 35 ranged, Range 5
- Fighter: 45, Range 8
- Jet Fighter: 75, Range 10
- Great War Bomber: 50, Range 6
- Bomber: 65, Range 10
- Stealth Bomber: 85, Range 20

## 11. Special ranges

Paradrop:
- Paratrooper: 9
- Spec Ops: 7
- XCOM Squad: 40

Interception coverage field:
- Triplane: 2
- Fighter: 2
- Jet Fighter: 2
- Anti-Air Gun: 2
- Mobile SAM: 2
- Missile Cruiser: 2

Cargo:
- Aircraft Carrier: 3
- Nuclear Submarine: 2
- Missile Cruiser: 3

Exact eligible cargo categories are handled separately from capacity.

## 12. Upgrade Gold formula

Authority:
`city_system/FINAL_UNIT_UPGRADE_COSTS_V1.csv`

The baseline follows the Civ V production-difference formula:

`base = 10 + max(0, 2 * (new production - old production))`

Then:

`upgrade gold = floor_to_5(base * (1 + 0.3 * equivalent era index))`

Project era -> compressed Civ V-equivalent era index:
- Ancient 0
- Classical 1
- Late Antiquity 2
- Early Medieval 2
- High Medieval 2
- Renaissance 3
- Exploration 3
- Enlightenment 4
- Industrial 4
- Modern 5
- Atomic 6
- Information 7
- Future 8

The multiplier is based on the **target unit's** project era.

The result is rounded down to the nearest 5 Gold.

Production replacements for founding units are not Gold upgrades and therefore do not receive an upgrade-cost row.

Air-unit upgrades require an appropriate city/air-basing context.

## 13. Current structural result

- unit numeric rows: 89
- generic roster rows: 89
- direct Gold upgrade-cost rows: 55
- founding production-replacement Gold rows: 0
- strategic-resource per-turn upkeep introduced: 0
- numeric source-grade metadata: complete

Status:
**MILITARY NUMERIC BASELINE LOCKED V1**
