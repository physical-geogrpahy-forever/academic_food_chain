# Unit Upgrade Source Audit V1

Date: 2026-09-21

This file records the external game/mod references used to resolve the ambiguous direct-upgrade graph.

## Civilization V

Chariot Archer:
- upgrades to Knight
- source: Civilization Wiki, Chariot Archer (Civ5)
- https://civilization.fandom.com/wiki/Chariot_Archer_(Civ5)

Caravel:
- Trireme -> Caravel -> Ironclad continuity
- source: Civilization Wiki, Caravel (Civ5)
- https://civilization.fandom.com/wiki/Caravel_(Civ5)

Tank:
- upgrades from Landship and to Modern Armor
- source: Civilization Wiki, Tank (Civ5)
- https://civilization.fandom.com/wiki/Tank_(Civ5)

Civ V upgrade semantics:
- upgrades cannot normally skip required intermediate stages
- promotions are retained through upgrades
- source: Civilization Wiki, Unit (Civ5)
- https://civilization.fandom.com/wiki/Unit_(Civ5)

## Civilization VI / Gathering Storm

Base upgrade table:
- Warrior -> Swordsman -> Man-at-Arms -> Musketman -> Line Infantry -> Infantry
- Spearman -> Pikeman -> later anti-cavalry
- source: Civilization Wiki data module
- https://civilization.fandom.com/wiki/Module:Data/Civ6/Base/UnitUpgrades

Pike and Shot:
- upgrades from Pikeman
- source: https://civilization.fandom.com/wiki/Pike_and_Shot_(Civ6)

Modern AT:
- upgrades from AT Crew
- source: https://civilization.fandom.com/wiki/Modern_AT_(Civ6)

Privateer / Submarine:
- Privateer -> Submarine -> Nuclear Submarine
- sources:
  - https://civilization.fandom.com/wiki/Privateer_(Civ6)
  - https://civilization.fandom.com/wiki/Submarine_(Civ6)

Support:
- Gathering Storm Battering Ram -> Siege Tower
- Medic -> Supply Convoy
- Observation Balloon -> Drone
- sources:
  - https://civilization.fandom.com/wiki/Battering_Ram_(Civ6)
  - https://civilization.fandom.com/wiki/Medic_(Civ6)
  - https://civilization.fandom.com/wiki/Supply_Convoy_(Civ6)
  - https://civilization.fandom.com/wiki/Observation_Balloon_(Civ6)
  - https://civilization.fandom.com/wiki/Drone_(Civ6)

Recon:
- Ranger -> Spec Ops
- source: https://civilization.fandom.com/wiki/Spec_Ops_(Civ6)

Naval ranged:
- Quadrireme -> Frigate -> Battleship -> Missile Cruiser is the Civ VI skeleton.
- project inserts adopted Galleass / Ship of the Line / Cruiser stages.
- sources:
  - https://civilization.fandom.com/wiki/Quadrireme_(Civ6)
  - https://civilization.fandom.com/wiki/Frigate_(Civ6)
  - https://civilization.fandom.com/wiki/Missile_Cruiser_(Civ6)

## Pouakai Enlightenment Era

Reference:
- https://civ5customization-archive.fandom.com/wiki/Pouakai%27s_Enlightenment_Era

Explicit changes relevant to this project:
- Scout -> Explorer
- Crossbowman -> Skirmisher
- Cannon -> Field Gun
- Frigate -> Cruiser
- Trireme -> Carrack in the source mod

The project does not contain Carrack, so its naval melee tree instead uses the already adopted Caravel.

## Project-only reconciliation

The following edges are project syntheses rather than claims about an original source game:
- Fire Lance -> Arquebusier
- Man-at-Arms -> Arquebusier
- Knight -> Lancer
- Lancer -> Landship
- Galleon -> Ironclad
- Frigate -> Ship of the Line branch
- Ship of the Line -> Battleship
- Pike and Shot -> Anti-Tank Gun
- Paratrooper -> XCOM Squad

These are used only where necessary to preserve role continuity across the project's merged 89-unit roster.
