# Final Building Remaining Provisional Audit V1

Generated from `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`.

- Building rows: 104
- Provisional columns found: 2
- Unresolved nonzero provisional entries: 0

## HEALTH_POINTS_PROVISIONAL

- Status: `SUPERSEDED_PROVENANCE`
- Current authority: HEALTH_POINTS_FINAL / Health V1
- Nonzero rows: 9

| Building | Era | Chain | Value |
|---|---|---|---:|
| Granary | Ancient | FOOD_HEALTH | 1 |
| Recycling Center | Information | INDUSTRY_POWER | 2 |
| Aqueduct | Classical | FOOD_HEALTH | 2 |
| Cold Storage | Industrial | FOOD_HEALTH | 2 |
| Food Market | Industrial | FOOD_HEALTH | 1 |
| Hospital | Industrial | FOOD_HEALTH | 4 |
| Sewer | Industrial | FOOD_HEALTH | 4 |
| Apothecary | Late Antiquity | FOOD_HEALTH | 2 |
| Medical Lab | Modern | FOOD_HEALTH | 5 |

## STABILITY_POINTS_PROVISIONAL

- Status: `SUPERSEDED_PROVENANCE`
- Current authority: STABILITY_POINTS_FINAL / Building Stability Support V1
- Nonzero rows: 17

| Building | Era | Chain | Value |
|---|---|---|---:|
| Palace | Ancient | CAPITAL_ADMIN | 2 |
| Courthouse | Ancient | GOVERNMENT_DIPLOMACY | 2 |
| Government Plaza | Ancient | GOVERNMENT_DIPLOMACY | 2 |
| Ancestral Hall | Classical | GOVERNMENT_DIPLOMACY | 1 |
| Audience Chamber | Classical | GOVERNMENT_DIPLOMACY | 1 |
| Consulate | Classical | GOVERNMENT_DIPLOMACY | 1 |
| Warlord's Throne | Classical | GOVERNMENT_DIPLOMACY | 1 |
| Court | Early Medieval | GOVERNMENT_DIPLOMACY | 1 |
| Foreign Ministry | High Medieval/Exploration | GOVERNMENT_DIPLOMACY | 1 |
| Grand Master's Chapel | High Medieval/Exploration | GOVERNMENT_DIPLOMACY | 1 |
| Intelligence Agency | High Medieval/Exploration | GOVERNMENT_DIPLOMACY | 1 |
| Telegraph Office | Industrial | GOVERNMENT_DIPLOMACY | 1 |
| National History Museum | Modern | GOVERNMENT_DIPLOMACY | 2 |
| Royal Society | Modern | GOVERNMENT_DIPLOMACY | 1 |
| War Department | Modern | GOVERNMENT_DIPLOMACY | 1 |
| Chancery | Renaissance | GOVERNMENT_DIPLOMACY | 1 |
| Constabulary | Renaissance | GOVERNMENT_DIPLOMACY | 1 |

## Decision

`HEALTH_POINTS_PROVISIONAL` is retained only as provenance and does not control gameplay because Health V1 supplies `HEALTH_POINTS_FINAL`.

`STABILITY_POINTS_PROVISIONAL` is also retained only as provenance. Building gameplay authority is `STABILITY_POINTS_FINAL` under `STABILITY_BUILDING_SUPPORT_V1.md`.

The building support values are not direct additions to country-level State Stability. The later State Stability quantitative pass will aggregate them with Happiness, War Weariness, government transition, occupation and colonial burdens.
