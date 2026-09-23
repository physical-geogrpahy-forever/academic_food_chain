# City Happiness Quantitative V1

Date: 2026-09-23
Status: QUANTITATIVE V1 LOCKED FOR PRE-RUNTIME STATIC INTEGRATION

This document is the numerical authority for the City Happiness core. It implements the structure approved in `docs/superpowers/specs/2026-09-23-city-happiness-quantitative-v1-design.md` and keeps City Happiness separate from State Stability, Health, Power and later War Weariness or colonial systems.

## 1. Design lineage

The project keeps the useful Vox Populi idea that urban unhappiness should have visible causes rather than one opaque population penalty.

The retained structural categories are:

- Distress: Food plus Production deficiency
- Poverty: Gold deficiency
- Illiteracy: Science deficiency
- Boredom: Culture deficiency
- Religious Unrest: religious minority pressure
- flat building reductions for the individual Needs
- a population cap on total Citizen Needs unhappiness

The project does not copy unrestricted Vox Populi world-median thresholds. Our thirteen-era game uses a project-native era expectation table, with only a small relative adjustment around that baseline.

The numerical values in `HAPPINESS_ERA_EXPECTATIONS_V1.csv` are therefore project balance values. They are not presented as exact Vox Populi values.

## 2. Era expectations

Authoritative table:

- `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`

Each row defines four expected per-capita outputs:

- `BASIC_NEED`: gross Food before Health conversion plus Production
- `GOLD_NEED`: Gold
- `SCIENCE_NEED`: Science
- `CULTURE_NEED`: Culture

The values increase across Ancient through Future so that later large cities must maintain correspondingly stronger urban economies and institutions.

## 3. Relative expectation adjustment

World conditions may modify the era baseline, but only weakly.

For each category `x`:

```text
relative_factor_x = clamp(global_median_per_capita_x / era_expectation_x, 0.90, 1.10)

effective_expectation_x = era_expectation_x * relative_factor_x
```

The upstream empire/world aggregator should compute the median only from eligible non-occupied cities with population at least 2. If fewer than four eligible cities exist, it should omit the relative layer and the calculator uses factor 1.00.

`calculate_city_happiness_v1.py` accepts either:

- no `global_medians`, which means factor 1.00 for all four categories, or
- all four positive medians: `basic`, `gold`, `science`, `culture`.

Supplying an incomplete, zero, negative or non-numeric relative layer is an error rather than a silent fallback.

## 4. Supported population

For city population `P`:

```text
supported_basic
= floor((gross_food_pre_health + production) / effective_basic_need)

supported_gold
= floor(gold / effective_gold_need)

supported_science
= floor(science / effective_science_need)

supported_culture
= floor(culture / effective_culture_need)
```

The use of `floor` is deliberate. A city just below the next full support threshold does not receive that extra supported citizen through floating-point rounding.

## 5. Four yield-based Needs

```text
distress_raw
= max(0, P - supported_basic)

poverty_raw
= max(0, P - supported_gold)

illiteracy_raw
= max(0, P - supported_science)

boredom_raw
= max(0, P - supported_culture)
```

Then apply final Building-master and future global reductions independently:

```text
distress
= max(0, distress_raw - distress_reduction)

poverty
= max(0, poverty_raw - poverty_reduction)

illiteracy
= max(0, illiteracy_raw - illiteracy_reduction)

boredom
= max(0, boredom_raw - boredom_reduction)
```

Current Building-master columns are:

- `VP_DISTRESS_REDUCTION`
- `VP_POVERTY_REDUCTION`
- `VP_ILLITERACY_REDUCTION`
- `VP_BOREDOM_REDUCTION`

The calculator accepts the final aggregate reductions as explicit named inputs so later policies or global modifiers can be added without changing the Needs arithmetic.

## 6. Religious Unrest

When the religion system is active in the city:

```text
religious_unrest_raw
= floor(minority_followers / 2)

religious_unrest
= max(0, religious_unrest_raw - religious_unrest_reduction)
```

`minority_followers` means followers of religions other than the city's majority religion.

When religion is not active for that city, Religious Unrest is zero even if a transitional data object contains a minority-follower count. Pantheon-only population is not treated as a hostile religious minority in V1.

Current Building-master reduction field:

- `VP_RELIGIOUS_UNREST_REDUCTION`

## 7. Citizen Needs population cap

The post-reduction components remain visible individually for UI and AI explanation, but their combined citizen penalty is bounded:

```text
citizen_needs_pre_cap
= distress
+ poverty
+ illiteracy
+ boredom
+ religious_unrest

citizen_needs_unhappiness
= min(P, citizen_needs_pre_cap)
```

This prevents a population 4 city from receiving, for example, eleven points of Citizen Needs unhappiness merely because it is simultaneously weak in several categories.

The uncapped breakdown is still retained so the player can see every underlying problem.

## 8. Health double-count protection

Health remains a separate system.

The Basic Need formula uses:

```text
gross_food_pre_health
```

not Food after `Food_from_Health` from `HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`.

Therefore negative Health cannot reduce Food, create extra Distress from that reduction, and then also apply a Health Happiness penalty. The Happiness layer reads final `H_city` only through the dedicated Health Unhappiness tier.

## 9. Health Unhappiness

Final city Health from the Health system maps to Happiness as follows:

| Final H_city | Health Unhappiness |
|---|---:|
| 0 or higher | 0 |
| -1 to -2 | 1 |
| -3 to -4 | 2 |
| -5 or lower | 3 |

This term is deliberately small because negative Health already affects Food and plague risk in its own system.

For a population-zero transitional city object, Health Unhappiness is forced to zero.

## 10. Local Happiness

Positive city-local Happiness is:

```text
local_happiness_positive
= min(P, max(0, sum_local_happiness_sources))
```

`LOCAL_HAPPINESS` from `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv` is a direct input source.

Local positive Happiness cannot exceed city population.

Empire-wide luxury/resource Happiness is not silently divided among cities and does not enter this field. It remains an empire-level quantity for later integration with Empire Health and State Stability.

## 11. Full City Happiness equation

```text
City_Happiness
=
  local_happiness_positive
- citizen_needs_unhappiness
- health_unhappiness
- war_weariness_unhappiness
- occupation_unhappiness
- colonial_unhappiness
- policy_burden_unhappiness
```

The four trailing penalties are explicit interface inputs. In City Happiness V1 they default to zero because their own systems have not yet been quantitatively locked.

They must not be replaced with guessed placeholder values.

No final clamp is applied to total City Happiness. Citizen Needs are population-capped, but future war, occupation and colonial shocks may legitimately drive a city's final Happiness below negative population.

## 12. Current Building-master integration

Validator:

- `city_system/validate_happiness_building_links_v1.py`

Fixture:

- `city_system/test_validate_happiness_building_links_v1.py`

Current 104-building master validation result:

- Distress reduction sources: 5
- Poverty reduction sources: 4
- Illiteracy reduction sources: 8
- Boredom reduction sources: 10
- Religious Unrest reduction sources: 2
- Local Happiness sources: 6

The validator requires all 104 rows to contain numeric, nonnegative values for Local Happiness and all five Needs reduction fields.

It also requires `HEALTH_POINTS_FINAL` and `STABILITY_POINTS_FINAL` to exist and remain numeric as cross-system guards, but those two fields are never counted as Happiness sources.

During integration this validator exposed blank Happiness fields on V3-added buildings such as Smokehouse. The Building merge generator was corrected to initialize all newly added buildings with zero Local Happiness and zero Needs reductions unless an explicit override provides otherwise.

## 13. Calculator interface

Implementation:

- `city_system/calculate_city_happiness_v1.py`

Required city inputs:

- era
- population
- gross Food before Health conversion
- Production
- Gold
- Science
- Culture
- final City Health

Optional explicit inputs include:

- minority followers
- whether religion is active
- Local Happiness sources
- five Needs reductions
- four global relative medians
- War Weariness penalty
- Occupation penalty
- Colonial penalty
- Policy Burden penalty

The result is a structured breakdown containing effective expectations, supported population by category, raw Needs, post-reduction Needs, pre-cap and final Citizen Needs, Health penalty, Local Happiness, each external penalty and final City Happiness.

This breakdown is intended to be consumed directly by future UI and AI rather than recomputing hidden variants of the formula elsewhere.

## 14. Static QA

Generator:

- `city_system/generate_city_happiness_static_qa_v1.py`

Generated report:

- `city_system/CITY_HAPPINESS_STATIC_QA_V1.md`

The V1 static suite contains 12 scenarios:

1. balanced Ancient city
2. severely underdeveloped Ancient city
3. Illiteracy building reduction
4. Health -4 independent penalty
5. five minority followers
6. Local Happiness cap
7. high and low relative-expectation clamp
8. single external-penalty passthrough
9. population-zero transitional object
10. floating-point floor boundary
11. all four external penalty channels simultaneously
12. religion-inactive minority case

Current result:

```text
CITY_HAPPINESS_STATIC_QA: PASS scenarios=12
```

This is arithmetic/static QA only. It is not runtime telemetry and it is not a Civilization autoplay result.

## 15. Error handling

The calculator rejects:

- unknown era names
- negative or non-integer population
- negative Food, Production, Gold, Science or Culture input
- negative Needs reductions
- negative minority count
- minority count above population
- incomplete or malformed global median dictionaries
- zero or negative supplied global medians
- negative external penalties

Population zero is valid for transitional/test objects and returns zero Needs, zero Local Happiness and zero Health penalty while preserving explicitly supplied external penalties.

## 16. Deferred inputs

This V1 does not assign numerical values to:

- War Weariness
- Occupation
- Colonial burden
- Policy burden
- State Stability
- empire-wide luxury Happiness allocation

These are not missing fields inside the calculator. They are named system boundaries intentionally left for their own quantitative passes.

The next political numerical pass after City Happiness is War Weariness.

## 17. Authority order

For City Happiness conflicts, use:

1. `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`
2. `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`
3. `city_system/calculate_city_happiness_v1.py`
4. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv` for Building-local source values
5. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md` for final Health input
6. `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md` and older structural planning documents

## Final verdict

City Happiness V1 now has a single explicit arithmetic core while retaining cause-by-cause diagnosis.

Yield deficiencies create Citizen Needs, Citizen Needs are population-capped, Health is separated to prevent double counting, Local Happiness is city-local and population-capped, and future political penalties enter through named external interfaces rather than speculative numbers.

Further numerical changes to the V1 core should be driven by later gameplay/runtime evidence after a game engine exists, not by relabeling static QA as autoplay.
