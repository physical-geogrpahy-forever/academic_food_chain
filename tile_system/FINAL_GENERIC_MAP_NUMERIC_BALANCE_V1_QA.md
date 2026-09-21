# Final Generic Map Numeric Balance V1 QA

Date: 2026-09-21
Status: **PASS — current repository structural/resource validation**

Authorities:
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv`
- `tile_system/FINAL_GENERIC_MAP_NUMERIC_BALANCE_V1.csv`
- `tile_system/FINAL_MAP_YIELD_UPGRADE_RULES_V1.csv`
- `tile_system/FINAL_RESOURCE_IMPROVEMENT_COMPATIBILITY_V1.csv`
- `tile_system/FINAL_MORE_LUXURIES_RESOURCE_RULES_V1.csv`
- `tile_system/validate_final_generic_map_numeric_balance_v1.py`

Current result:
- canonical map records: **39**
- numeric map rows: **39**
- canonical resource IDs from actual project catalog: **47**
- resource/improvement compatibility rows: **47**
- strategic resources: **7**
- bonus resources: **10**
- luxury resources: **30**
- More Luxuries exact-resource rows: **9**
- technology/civic yield-upgrade rows: **23**
- unknown resource IDs: **0**
- missing project resources: **0**
- More Luxuries mapping mismatches: **0**
- route movement mismatches: **0**
- Power-output mismatches: **0**
- result: **PASS**

## More Luxuries protected mappings

Plantation:
- Coffee
- Tea
- Tobacco
- Olives
- Perfume

Mine:
- Amber
- Jade
- Lapis Lazuli

Fishing Boats:
- Coral

Base resource yields:
- Coffee +2 Gold
- Tea +2 Gold
- Tobacco +2 Gold
- Perfume +2 Gold
- Amber +2 Gold
- Jade +2 Gold
- Lapis Lazuli +2 Gold
- Coral +2 Gold
- Olives +1 Food +1 Gold

## Project resource extensions

- Maize -> Farm
- Rice -> Farm
- Niter -> Mine

## Routes

- Road movement cost: 0.5
- improved Road: 0.333333
- Railroad: 0.1
- Road maintenance: 1 Gold/tile
- Railroad maintenance: 2 Gold/tile
- Railroad capital connection: +25% city Production

## Environmental / Future infrastructure

- Wind Farm: +1 Production, +1 Gold, Power 2
- Solar Farm: +1 Production, +1 Gold, Power 2
- Geothermal Plant: +2 Production, +1 Science, Power 4
- Offshore Wind Farm: +1 Production, +1 Gold, Power 2
- Seastead: +2 Food plus adjacency rules

Power values are supply values for the separate Power system.

## Saltworks

Natural Salt remains Mine-based.

The existing resource-transfer design mentions a possible coastal Saltworks, but it is not in the canonical 39-record map roster and therefore was **not silently added**.

A later Saltworks adoption requires:
- explicit roster addition
- technology/civic gate
- numeric rule
- validator update

## Validator parser note

The project resource catalog mixes block-style and inline YAML mappings and also contains an `excluded:` section.

The validator now reads only the `resources:` block and supports both YAML styles, so excluded Nutmeg/Cloves/Pepper/etc. are not mistaken for active project resources.

No GitHub Actions run is claimed here unless a completed run is separately retrieved.
