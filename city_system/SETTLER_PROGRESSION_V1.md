# Settler Progression V1

Date: 2026-09-21  
Status: **LOCKED V1**

Authority:
- `city_system/SETTLER_PROGRESSION_V1.csv`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`

## Final progression

`Settler -> Pioneer -> Colonist -> Urban Planner`

| Unit | Era | Gate | Starting population |
|---|---|---|---:|
| Settler | Ancient | game start | 1 |
| Pioneer | Exploration | Cartography + Exploration | 2 |
| Colonist | Industrial | Railroad + Colonialism | 3 |
| Urban Planner | Modern | Combustion + Urbanization | 4 |

## Territory rule

All four founding units use the **same base founding-territory rule**.

There is no larger free territorial claim for Pioneer, Colonist or Urban Planner. Later units are better because the founded city starts with more population and a stronger minimum infrastructure package, not because they seize more tiles.

## Founding infrastructure

The package now follows a **previous-era core infrastructure** rule. A late-founded city should not restart from the Ancient era.

The package never bypasses technology or civic progress: a building is granted only if the civilization has already unlocked it normally and all local city prerequisites are satisfied at founding.

- Settler: none
- Pioneer: core infrastructure through Renaissance
  - Monument, Granary, Library, Market, Aqueduct, Amphitheater, Workshop, University, Bank
- Colonist: Pioneer package + selected Exploration/Enlightenment core infrastructure
  - Opera House, Public School, Stock Exchange, Newspaper Office, Zoo
- Urban Planner: Colonist package + selected Industrial core infrastructure
  - **Factory, Hospital, Sewer, Food Market, Cinema, Shopping Mall, Power Plant**

Conditional local infrastructure:
- Water Mill if normally eligible
- Pioneer coastal city: Harbor + Lighthouse if eligible
- Colonist coastal city: + Seaport if eligible
- Urban Planner coastal city: + Shipyard if eligible

Important:
- Factory and Hospital are intentionally included in the Urban Planner package because they are major Industrial-era institutions.
- No building is granted if its normal technology/civic gate has not been met.
- A building that was ineligible at founding is not granted later for free when its prerequisite is researched.

Still excluded from the automatic core package:
- military-training chain
- city-defense chain
- religion-specialization chain
- one-per-civilization/government-choice buildings
- museum branch choices
- Research Lab, Medical Lab, Airport and Broadcast Center
- specialized Steelworks, Coal Power Plant and Drydock

Full authority:
`city_system/ADVANCED_SETTLER_FREE_BUILDING_PACKAGE_V1.md`

## Replacement behavior

Once a later founding unit is unlocked, newly produced founding units use the newer class:
- Pioneer replaces Settler
- Colonist replaces Pioneer
- Urban Planner replaces Colonist

Existing units already on the map are not automatically transformed.

The founding unit is consumed on city founding and does **not** create a free Worker afterward.

## Balance rationale

The starting-population sequence is intentionally restrained:

`1 -> 2 -> 3 -> 4`

A 7-population modern city was rejected as too large. Population growth and mature-city development must remain valuable even in the late game.

