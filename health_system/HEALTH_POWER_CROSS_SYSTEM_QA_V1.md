# Health-Power Cross-System QA V1

Date: 2026-09-23
Status: STATIC CROSS-SYSTEM QA COMPLETE / POWER-POLLUTION BRIDGE RESOLVED

Inputs:

- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/POWER_POLLUTION_BRIDGE_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
- `city_system/validate_cross_system_v1.py`

## 1. Direct Health versus Pollution

PASS.

Factory, Coal Power Plant and generic Oil-role Power Plant do not receive an additional hard-coded direct negative Health value.

Their route is:

`industrial/power source -> local Pollution -> city Health penalty`

Health V1 uses:

`Health pollution penalty = -floor(city_pollution / 10)`, capped at -5.

This prevents duplicate direct industrial `-Health` plus Pollution-derived `-Health`.

## 2. Power emission -> local Pollution bridge

RESOLVED V1.

Authority:

- `city_system/POWER_POLLUTION_BRIDGE_V1.csv`

Gathering Storm fuel coefficients retained for the global-emission side:

- Coal: 820 per generated Power
- Oil: 490 per generated Power
- Nuclear: 48 per generated Power
- adopted renewables: 0

Project local-Pollution conversion:

`local_pollution = round(actual_power_generated * GS_CO2_per_power / 300)`

The `/300` term is a project normalization, not a claim that Gathering Storm itself uses local Pollution points.

Examples at 4 generated Power:

- Coal: local Pollution 11 -> Health -1
- Oil: local Pollution 7 -> Health 0
- Nuclear: local Pollution 1 -> Health 0

At 8 Power, Oil reaches about 13 local Pollution and therefore Health -1. This preserves the intended ordering `Coal > Oil > Nuclear > renewables` without making one fossil plant automatically trigger the -5 Health cap.

Global CO2 and local Pollution remain separate variables.

## 3. Power demand versus Health buildings

PASS.

Hospital, Sewer, Apothecary and Medical Lab do not receive invented Power loads merely because they are medical buildings.

Food Market has Power load 1 because it comes from the adopted Gathering Storm Power structure.

## 4. Food Market overlap

RUNTIME WATCH, not a structural error.

Food Market has:

- base Food +4
- Health +1
- Power load 1
- powered Food +2

Direct Food and Health-derived Food are distinct systems. Do not remove either before runtime evidence.

## 5. Hospital overlap

RUNTIME WATCH.

Hospital retains base Food +5 while Health V1 adds Health +4 and plague-duration -1.

Monitor Industrial city growth and whether Population -1 Health per citizen naturally absorbs the temporary Health surplus.

## 6. Aqueduct duplicate counting

PASS.

Natural fresh water and Aqueduct each provide a water-Health floor of +2, but do not stack. River cities therefore do not receive an accidental +4 water bonus.

## 7. International trade double-effect

PASS structurally, RUNTIME WATCH quantitatively.

International trade has two distinct effects:

1. every four active international routes impose -1 Empire Health, capped at -2;
2. an infected international trade link uses plague transmission multiplier x2.0.

The first is persistent connectivity pressure; the second exists only when an infected source city is present.

## 8. Dynamic resource compatibility

PASS.

Health from resources requires the local resource copy to be worked. Visibility, contact, or import alone does not create city Health.

## 9. Strategic-resource Health tradeoff

RUNTIME WATCH.

Worked Coal/Oil can carry extraction-site Health maluses while power consumption creates citywide Pollution. These are different mechanisms but can compound, so autoplay must test whether the combined burden is excessive.

## 10. Late disease suppression

RUNTIME WATCH.

The late stack can include Sewer +4, Hospital +4, Medical Lab +5, Recycling Center +2 and Pollution -25%. No static nerf is applied before outbreak-frequency data exists.

## 11. Validator

`city_system/validate_cross_system_v1.py` checks:

- Coal/Oil/Nuclear Power-resource ratios and emission ordering;
- zero-emission renewable consistency;
- Health building positive values;
- absence of duplicate direct Health penalties on industry/transport buildings;
- locked plague anchors;
- 55 unit-upgrade edges and the three equal-cost 10 Gold watch edges.

The validator logic was executed against a matching fixture and returned `CROSS_SYSTEM_STATIC_QA: PASS`. Repository-source rows were then reread through GitHub and matched the asserted anchors. Full game-engine runtime autoplay remains separate.

## Final verdict

Health-Power structural integration is now closed for pre-autoplay V1.

No known numeric bridge remains between Power emissions and Health.

Remaining issues are runtime balance questions rather than missing structural links.