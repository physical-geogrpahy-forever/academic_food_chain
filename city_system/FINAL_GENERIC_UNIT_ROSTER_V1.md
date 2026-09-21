# Final Generic Unit Roster V1

Date: 2026-09-21  
Status: **LOCKED / QA TARGET**

Authority:
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`
- `city_system/validate_final_generic_unit_roster_v1.py`

## 1. Scope

This file consolidates the project's **generic non-Great-Person unit roster** after the 109-technology and 72-civic unlock passes.

Current total: **89 units**

Source split:
- 74 units from `MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv`
- 7 civic-only or civic-owned units from `MASTER_CIVIC_UNLOCKS_72_V2.csv`
- 5 baseline/system units recovered outside the unlock tables
- 3 project-designed advanced founding units from `SETTLER_PROGRESSION_V1`

Great People are intentionally excluded from this roster. Great Generals, Great Admirals, Great Prophets, Great Merchants, Great Engineers, Great Scientists, Great Writers, Great Artists, Great Musicians and the project Great Director remain in their own Great Person systems.

## 2. Baseline/system recovery

The technology and civic tables only record unlocks. Therefore five generic units had to be restored explicitly:

- Settler -> game start
- Warrior -> game start
- Scout -> game start
- Missionary -> majority-religion system gate
- Inquisitor -> enhanced-religion system gate

This follows the adopted Civ V-style baseline. Civ V's unit roster separately lists Settler, Worker and Work Boat as civilian units, Missionary and Inquisitor as religious units, and Caravan and Cargo Ship as trade units. Its BNW unit-class data also contains Settler, Worker, Warrior, Scout and the other base classes.

External reference:
- https://civilization.fandom.com/wiki/List_of_units_in_Civ5
- https://civilization.fandom.com/wiki/Module:Data/Civ5/BNW/UnitClasses

## 3. Recovered audit/master mismatches

Two real inconsistencies were found while consolidating the roster.

### Mechanized Infantry

The Modern and Atomic audit records had already remapped Mechanized Infantry away from late satellite/electronics placement to **Combined Arms**, but the final 109-tech master accidentally omitted it from the UNITS field.

Final V1:
- Mechanized Infantry -> Combined Arms
- role family -> GUNPOWDER_INFANTRY
- era -> Modern

The technology summary and 109-tech master have now been synchronized.

### Missile Cruiser

The Atomic audit and the Lasers note explicitly said that Missile Cruiser moves to **Guidance Systems + Warships**, but the Guidance Systems UNITS field did not contain it.

Final V1:
- Missile Cruiser -> Guidance Systems + Warships
- role family -> NAVAL_RANGED
- era -> Atomic

The Atomic summary and 109-tech master have now been synchronized.

## 4. Gate model

The roster uses separate fields rather than embedding every dependency in the unit name:

- `TECH_GATE`
- `ADDITIONAL_TECH_GATE`
- `CIVIC_GATE`
- `SYSTEM_GATE`
- `GATE_MODE`

Examples:

| Unit | Technology | Additional technology | Civic/system |
|---|---|---|---|
| Caravan | Animal Husbandry | - | Foreign Trade |
| Military Engineer | Military Engineering | - | Military Training |
| Explorer | Cartography | - | Exploration |
| Battleship | Armor Plating | Warships | - |
| Infantry | Replaceable Parts | - | Nationalism |
| Spec Ops | Radar | - | Rapid Deployment |
| Missile Cruiser | Guidance Systems | Warships | - |
| Jet Fighter | Lasers | Advanced Flight | - |

This prevents technology names such as Warships or Advanced Flight from being misread as civic prerequisites.

## 5. Major role families

These remain role/progression families in this roster file. Exact direct one-step upgrade edges are now separately locked in `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`.

- Recon: Scout -> Explorer -> Ranger -> Spec Ops
- Ranged infantry: Archer -> Composite Bowman -> Crossbowman -> Skirmisher -> Gatling Gun -> Machine Gun
- Siege: Catapult -> Trebuchet -> Bombard -> Field Gun -> Artillery -> Rocket Artillery
- Gunpowder/front-line infantry: Fire Lance -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry
- Armored: Landship -> Tank -> Modern Armor
- Anti-armor: Anti-Tank Gun -> Modern AT
- Submarine: Submarine -> Nuclear Submarine
- Fighter aircraft: Triplane -> Fighter -> Jet Fighter
- Bomber aircraft: Great War Bomber -> Bomber -> Stealth Bomber
- Late airborne assault: Paratrooper / Marine -> XCOM Squad
- Founding: Settler -> Pioneer -> Colonist -> Urban Planner

Exact combat strength, cost, movement, promotions and strict upgrade edges belong to the later numerical combat-balance pass.

## 6. Civic-only unit layer

The following are not owned by a single technology row alone:

- Spy -> Diplomatic Service
- Explorer -> Cartography + Exploration
- Galleon -> Astronomy + Exploration
- Privateer -> Warships + Mercantilism
- Archaeologist -> Natural History
- Naturalist -> Conservation
- Rock Band -> Cold War

Cross-gated units already present in the technology master, such as Infantry, Paratrooper, Supply Convoy, Nuclear Submarine and Spec Ops, are not duplicated.

## 7. Founding-unit progression

The generic founding line is now:

**Settler -> Pioneer -> Colonist -> Urban Planner**

| Unit | Era | Gate | Starting population | Territory |
|---|---|---|---:|---|
| Settler | Ancient | game start | 1 | same base rule |
| Pioneer | Exploration | Cartography + Exploration | 2 | same base rule |
| Colonist | Industrial | Railroad + Colonialism | 3 | same base rule |
| Urban Planner | Modern | Combustion + Urbanization | 4 | same base rule |

Later founding units do **not** claim more free tiles. Their advantage comes from the restrained population progression `1 -> 2 -> 3 -> 4` and a progressively stronger minimum founding-infrastructure package.

Authority: `city_system/SETTLER_PROGRESSION_V1.md`.

## 8. Explicit exclusions

### Heavy Chariot
Excluded as a separate generic unit. The project retains the Civ V-style Chariot Archer + Horseman ancient mounted structure.

### Nuclear Missile
Excluded as a standalone generic unit. Nuclear weapons use the adopted strategic-device model:
- Nuclear Device
- Thermonuclear Device
- Missile Silo and eligible delivery platforms

### Giant Death Robot
Restored to the baseline roster under the Gathering Storm Future Era realignment.
- Robotics -> Giant Death Robot
- Advanced AI -> Drone Air Defense
- Advanced Power Cells -> Particle Beam Siege Cannon
- Cybernetics -> Enhanced Mobility
- Smart Materials -> Reinforced Armor

The former optional module is superseded and retained only as design provenance.

### Great People
Excluded from this generic roster and managed separately.

## 9. Resource-requirement field

`RESOURCE_REQUIREMENT` only records strategic-material requirements that were already explicitly locked or stated in the audit trail.

A blank field **does not mean the unit is permanently resource-free**. It means that no strategic-material requirement is being newly invented during this consolidation pass. Final quantity and consumption rules remain part of military/economic numerical balance.

## 10. Era counts

| Era | Units |
|---|---:|
| Ancient | 14 |
| Classical | 6 |
| Late Antiquity | 3 |
| Early Medieval | 1 |
| High Medieval | 4 |
| Renaissance | 5 |
| Exploration | 10 |
| Enlightenment | 2 |
| Industrial | 12 |
| Modern | 18 |
| Atomic | 5 |
| Information | 8 |
| Future | 1 |
| **Total** | **89** |

The Gathering Storm realignment separates late military content across Atomic, Information and Future. Giant Death Robot is now a baseline Information-era super-unit, while XCOM Squad is a Future-era unit.

## 11. Next military pass

This V1 locks **which generic units exist and what unlocks them**.

The direct upgrade graph is now complete and locked in:
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.md`
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1_QA.md`

The next military-specific pass should determine:
- combat/ranged strength
- movement and range
- production and maintenance cost
- strategic-resource quantity/consumption
- promotions and unit-class interactions
- upgrade Gold costs
- naval transport/cargo rules
- air basing and interception rules

Those numerical rules should not modify the 89-unit existence/gate roster unless a concrete progression gap is demonstrated.


## 12. Direct upgrade graph — LOCKED V1

The 89-unit graph is structurally complete.

Important lines:
- Warrior -> Swordsman -> Man-at-Arms -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry
- Spearman -> Pikeman -> Pike and Shot -> Anti-Tank Gun -> Modern AT
- Archer -> Composite Bowman -> Crossbowman -> Skirmisher -> Gatling Gun -> Machine Gun
- Catapult -> Trebuchet -> Bombard -> Field Gun -> Artillery -> Rocket Artillery
- Scout -> Explorer -> Ranger -> Spec Ops
- Horseman -> Cavalry -> Helicopter
- Chariot Archer -> Knight -> Lancer -> Landship -> Tank -> Modern Armor
- Trireme -> Caravel -> Ironclad -> Destroyer
- Privateer -> Submarine -> Nuclear Submarine
- Paratrooper -> XCOM Squad
- Observation Balloon -> Drone
- Battering Ram -> Siege Tower -> Medic -> Supply Convoy

Naval ranged contains the sole explicit branch:
- Frigate -> Ship of the Line -> Battleship -> Missile Cruiser
- Frigate -> Cruiser -> Missile Cruiser

Founding units are production replacements, not direct upgrades.

QA:
- 89/89 rows
- unknown successors 0
- era regressions 0
- cycles 0
- PASS
