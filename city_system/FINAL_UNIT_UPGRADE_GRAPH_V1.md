# Final Unit Upgrade Graph V1

Date: 2026-09-21  
Status: **LOCKED V1**

Authorities:
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`

## Core rule

This file locks **direct one-step unit upgrades and explicit non-upgrade behavior**.

It does not yet lock:
- combat strength
- ranged strength
- range
- movement
- production cost
- maintenance
- strategic-resource quantity
- promotion values
- upgrade Gold cost

Those belong to the next numerical military pass.

## Design rule

The project combines:
1. Civ V's preference for keeping veteran units useful through upgrades;
2. Civ VI's clearer role-family continuity;
3. Pouakai's Enlightenment Era where the project already adopted intermediate units;
4. minimal project bridges only where the merged roster would otherwise produce an obvious dead end.

Do not force every unit into a successor merely to make the graph visually complete.

## Locked major lines

### Front-line infantry

`Warrior -> Swordsman -> Man-at-Arms -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry`

The early gunpowder branch also converges:

`Fire Lance -> Arquebusier`

Rationale:
- Man-at-Arms remains the armored-foot successor of Swordsman.
- Fire Lance is not used as a replacement for the entire melee line.
- both converge once mature shoulder-fired gunpowder infantry appears.

### Anti-cavalry / anti-armor

`Spearman -> Pikeman -> Pike and Shot -> Anti-Tank Gun -> Modern AT`

This deliberately treats anti-tank infantry/artillery as the mechanized-era continuation of the battlefield counter-cavalry role.

### Ranged infantry

`Archer -> Composite Bowman -> Crossbowman -> Skirmisher -> Gatling Gun -> Machine Gun`

Pouakai Enlightenment Era is authoritative for the Crossbowman -> Skirmisher insertion.

### Siege

`Catapult -> Trebuchet -> Bombard -> Field Gun -> Artillery -> Rocket Artillery`

Field Gun is therefore locked as a **siege/artillery stage**, not ordinary ranged infantry.

### Recon

`Scout -> Explorer -> Ranger -> Spec Ops`

The project uses Pouakai's Explorer extension rather than treating the project's Skirmisher as a recon unit.

### Light cavalry

`Horseman -> Cavalry -> Helicopter`

This preserves the fast raiding/mobile role through the industrial and modern transition.

### Heavy cavalry / armor

`Chariot Archer -> Knight -> Lancer -> Landship -> Tank -> Modern Armor`

Important:
- Chariot Archer -> Knight follows Civ V even though this changes ranged mounted combat into melee mounted combat.
- Knight -> Lancer is the project's post-medieval heavy-mounted bridge.
- Lancer -> Landship is a deliberate cavalry-to-armor historical transition.
- the project does **not** copy Civ V's Lancer -> Anti-Tank Gun role reversal.

### Air fighters

`Triplane -> Fighter -> Jet Fighter`

### Strategic bombers

`Great War Bomber -> Bomber -> Stealth Bomber`

### Anti-air

`Anti-Air Gun -> Mobile SAM`

### Airborne

`Paratrooper -> XCOM Squad`

Marine remains a terminal amphibious specialist.

XCOM is not a direct Marine upgrade because its defining gameplay lineage is airborne deployment.

## Naval lines

### Naval melee

`Trireme -> Caravel -> Ironclad -> Destroyer`

Galleon also converges:

`Galleon -> Ironclad`

This avoids creating a dead-end sailing warship while preserving Caravel as the main exploration/melee lineage.

### Naval raider

`Privateer -> Submarine -> Nuclear Submarine`

The project follows Civ VI here rather than Civ V's Privateer -> Destroyer conversion, because the canonical project roster explicitly classifies Privateer as `NAVAL_RAIDER`.

### Naval ranged

Opening:

`Quadrireme -> Galleass -> Frigate`

At Frigate, one branch choice is allowed:

- `Frigate -> Ship of the Line -> Battleship -> Missile Cruiser`
- `Frigate -> Cruiser -> Missile Cruiser`

This is the only explicit multi-successor direct-upgrade row in V1.

Reason:
- the merged roster contains both Ship of the Line and Cruiser;
- forcing Cruiser -> Battleship would collapse historically distinct cruiser/capital-ship roles;
- forcing one of the two out of the upgrade graph would create an avoidable dead end.

Both late branches converge on Missile Cruiser for gameplay continuity.

### Carrier

Aircraft Carrier has no generic successor in the current roster.

## Support lines

Gathering Storm support progression:

`Battering Ram -> Siege Tower -> Medic -> Supply Convoy`

This is an intentional support-role shift inherited from Civ VI.

Siege observation:

`Observation Balloon -> Drone`

Military Engineer remains a persistent specialist support unit with no successor.

## Founding units are NOT direct upgrades

`Settler -> Pioneer -> Colonist -> Urban Planner`

This line is recorded as **PRODUCTION_REPLACEMENT**, not direct unit upgrade.

When the later class is unlocked:
- newly produced founding units use the later class;
- existing older founding units remain unchanged;
- there is no Gold-button upgrade from Settler to Pioneer, etc.

This preserves the already locked settler-progression behavior.

## Civilian/system units without direct upgrades

No direct upgrade:
- Work Boat
- Worker
- Missionary
- Inquisitor
- Caravan
- Cargo Ship
- Spy
- Archaeologist
- Naturalist
- Rock Band

These are governed by their own action, trade, religion, archaeology, conservation, espionage or culture systems.

Guided Missile is consumable rather than upgradeable.

## Giant Death Robot

Giant Death Robot has **no successor unit**.

Instead it remains the same unit and receives Future-era module upgrades:
- Advanced AI -> Drone Air Defense
- Advanced Power Cells -> Particle Beam Siege Cannon
- Cybernetics -> Enhanced Mobility
- Smart Materials -> Reinforced Armor

## Terminal conventional combat units

Terminal under V1 include:
- Mechanized Infantry
- Marine
- Aircraft Carrier
- Destroyer
- Machine Gun
- Spec Ops
- Rocket Artillery
- Supply Convoy
- Stealth Bomber
- Jet Fighter
- Mobile SAM
- Modern AT
- Modern Armor
- Helicopter
- Nuclear Submarine
- Missile Cruiser
- Drone
- XCOM Squad
- Giant Death Robot

A terminal designation means **no generic successor currently exists**. It does not prevent future civilization-specific unique replacements.

## Source basis

Major imported source behavior used in V1:
- Civilization V BNW: Chariot Archer -> Knight; Caravel -> Ironclad; Landship -> Tank; classic fighter/bomber continuity
- Civilization VI / Gathering Storm: anti-cavalry family, Privateer -> Submarine -> Nuclear Submarine, Caravel -> Ironclad -> Destroyer, Medic -> Supply Convoy, Observation Balloon -> Drone
- Pouakai Enlightenment Era: Scout -> Explorer, Crossbowman -> Skirmisher, Frigate -> Cruiser, Cannon/field-artillery insertion concept

Project-specific bridges are explicitly labeled `Project ... bridge` in the CSV and should not be mistaken for source-game claims.

## QA

Current structural validation:
- roster units: 89
- graph rows: 89
- missing unit rows: 0
- duplicate source-unit rows: 0
- unknown successors: 0
- upgrade-era regressions: 0
- directed cycles: 0
- explicit branch rows: 1
- status: **PASS**
