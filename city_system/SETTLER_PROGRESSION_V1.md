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

The package is deliberately conservative. It prevents a late-founded city from restarting from the Ancient era without turning a new city into an instant mature core city.

- Settler: none
- Pioneer: Monument, Granary
- Colonist: Pioneer package + Library, Market, Aqueduct
- Urban Planner: Colonist package + Workshop, University, Sewer

Not granted for free:
- Barracks/Armory/Military Base
- Factory/Power Plant/Steelworks
- Hospital/Medical Lab
- Research Lab
- Stock Exchange
- Airport
- Broadcast Center
- terrain-conditional maritime buildings

This prevents founding units from becoming a shortcut to military, industrial, scientific or financial specialization.

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

