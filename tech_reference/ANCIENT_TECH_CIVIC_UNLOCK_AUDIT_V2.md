# Ancient Technology + Civic Unlock Audit V2

Date: 2026-09-21
Status: **ANCIENT RESTART COMPLETE — 14 technologies + 7 civics**

## Core rule

Use Civ V BNW first for city/tile form and baseline content.

When sources overlap or conflict:
1. historical and functional fit;
2. project 109-tech + 72-civic coherence;
3. avoid duplicate unlocks;
4. gameplay progression;
5. source-game placement.

Civilization VI **technologies and civics** are both audited.

## Gate modes

- TECH: material/scientific capability
- CIVIC: institution, law, doctrine, organization or culture
- TECH+CIVIC: both are genuinely required

## Ancient final technology summary

| Technology | Main result |
|---|---|
| Agriculture | Farm; Worker framework |
| Pottery | Granary |
| Animal Husbandry | Pasture; Horses reveal; Caravan only with Foreign Trade |
| Mining | Mine; forest clearing |
| Sailing | Work Boat; Trireme; Fishing Boats; Cargo Ship only with Foreign Trade |
| Astrology | participates in Great Prophet/religion access with Mysticism |
| Irrigation | Plantation; marsh clearing; fresh-water Farm +1 Food |
| Archery | Archer |
| Writing | Library; Courthouse only with Code of Laws |
| Masonry | Quarry; Walls; Stone Works; Battering Ram |
| Bronze Working | Spearman; Iron reveal; rainforest clearing |
| Wheel | Road; Water Mill; Chariot Archer |
| Calendar | seasonal agriculture; improved Wheat/Rice/Maize +1 Food |
| Trapping | Camp and wild-resource exploitation |

## Ancient civic summary

| Civic | Main result |
|---|---|
| Code of Laws | Chiefdom; early policy system; Courthouse with Writing |
| Craftsmanship | labor/artisan policy layer |
| Foreign Trade | +1 trade capacity; enables trade when Animal Husbandry/Sailing provides transport |
| Military Tradition | Barracks; flanking/support doctrine |
| State Workforce | Government Plaza converted to one-per-civ national city building |
| Early Empire | enforced borders and Open Borders |
| Mysticism | Shrine; religion/Great Prophet system with Astrology |

## Major changes from Ancient V1

### Plantation
Final:
**Irrigation -> Plantation**

Civ V remains the structural baseline, but its Calendar placement is overridden by stronger functional fit.

### Shrine
Final:
**Mysticism -> Shrine**

Pottery and Astrology source placements are not retained as the final building gate. Astrology still matters through:
**Astrology + Mysticism -> Great Prophet / religion access**

### Barracks
Final:
**Military Tradition -> Barracks**

Civ V and Civ VI attach Barracks to Bronze Working, but permanent military training is organizational rather than metallurgical.

### Courthouse
Final:
**Writing + Code of Laws -> Courthouse**

Civ V Mathematics placement is rejected as functionally weak.

### Trade
Final:
- Animal Husbandry + Foreign Trade -> Caravan / land trade
- Sailing + Foreign Trade -> Cargo Ship / maritime trade

Civ VI Foreign Trade is explicitly used as the institutional trade gate.

### Government Plaza
Civ VI State Workforce unlocks Government Plaza.

The district placement is removed. It becomes:
**Government Plaza (National Building)**

- ordinary Civ V-style city object;
- one per civilization;
- tier government buildings are deferred until Political Philosophy because they depend on government choice.

### Open Borders
Civ VI places border enforcement and Open Borders at Early Empire.

Final:
**Early Empire -> border/Open Borders system**

Do not attach Open Borders to Writing merely because an older source associates early diplomatic functions with Writing.

## Civ VI civic content that remains non-generic

Civilization-specific infrastructure is recorded but not generalized:
- Sphinx
- Chemamull
- Qhapaq Ñan
- Pairidaeza

## District handling

Removed as districts:
- Holy Site
- Campus
- Encampment
- Preserve

Useful content is re-evaluated separately:
- Shrine -> Mysticism
- Library -> Writing
- Barracks -> Military Tradition
- Grove -> deferred for later nature/religion/Conservation fit

## Wonders

All Wonders remain DEFER_WONDER and are not decided here.

## Health integration

Granary and fresh-water/Irrigation effects remain tagged for the Health & Plague system pass.
No exact Health coefficients are invented yet.

## Authority files

- `tech_reference/ancient_tech_civic_unlock_audit_v2.csv`
- `tech_reference/technology_unlock_summary_ancient_v2.csv`
- `civics_reference/civic_unlock_summary_ancient_v1.csv`

This V2 supersedes Ancient V1 for final Ancient unlock decisions.
