# City Happiness Quantitative V1 Design

Date: 2026-09-23
Branch: `civ-game-map-stage1b-etopo2022`
Status: DESIGN APPROVED IN CHAT, IMPLEMENTATION NOT YET STARTED

## 1. Purpose

Quantify the already-adopted City Happiness system without copying Vox Populi's full dynamic median formula and without duplicating Health, War Weariness, occupation, colonial, or policy penalties.

The player sees one city-level `City Happiness` value. Internal causes remain decomposed so AI and UI can explain why a city is unhappy.

This design implements the numeric core for:

- Distress
- Poverty
- Illiteracy
- Boredom
- Religious Unrest
- Health Unhappiness
- Local Happiness offset

War Weariness, Occupation, Colonial and Policy Burden remain explicit external input slots. They are not assigned speculative numbers in this pass.

## 2. Existing authorities preserved

This design extends, and does not replace, the following project authorities:

- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`
- `city_system/STABILITY_BUILDING_SUPPORT_V1.md`

Vox Populi source behavior retained conceptually:

- Distress is tied to Food plus Production.
- Poverty is tied to Gold.
- Illiteracy is tied to Science.
- Boredom is tied to Culture.
- Buildings can provide flat reduction to individual Needs.
- Citizen Needs unhappiness is population-bounded.
- Religious Unrest is tied to religious minority population.

Project adaptation:

- Era expectations replace VP's unrestricted world-median thresholds as the primary baseline.
- A small global relative adjustment may move each expectation by at most plus or minus 10 percent.
- Health is a separate cause and is not folded into Distress.

## 3. Era expectation table

All values are per citizen. `BASIC_NEED` is applied to pre-Health-conversion gross Food plus Production.

| Era | BASIC_NEED | GOLD_NEED | SCIENCE_NEED | CULTURE_NEED |
|---|---:|---:|---:|---:|
| Ancient | 2.00 | 0.75 | 0.75 | 0.40 |
| Classical | 2.20 | 1.00 | 1.00 | 0.50 |
| Late Antiquity | 2.40 | 1.10 | 1.20 | 0.60 |
| Early Medieval | 2.60 | 1.25 | 1.40 | 0.70 |
| High Medieval | 2.80 | 1.40 | 1.60 | 0.80 |
| Renaissance | 3.00 | 1.60 | 1.90 | 1.00 |
| Exploration | 3.20 | 1.80 | 2.20 | 1.20 |
| Enlightenment | 3.40 | 2.00 | 2.60 | 1.40 |
| Industrial | 3.60 | 2.30 | 3.00 | 1.60 |
| Modern | 3.80 | 2.60 | 3.50 | 1.90 |
| Atomic | 4.00 | 3.00 | 4.00 | 2.20 |
| Information | 4.20 | 3.40 | 4.60 | 2.60 |
| Future | 4.40 | 3.80 | 5.20 | 3.00 |

These are project-native V1 balance values, not claims about exact Vox Populi numbers.

## 4. Small relative adjustment

For each of the four output categories, compute a global median per-capita yield among non-occupied cities with population at least 2.

For category `x`:

```text
relative_factor_x = clamp(global_median_per_capita_x / era_expectation_x, 0.90, 1.10)

effective_expectation_x = era_expectation_x * relative_factor_x
```

If fewer than 4 eligible cities exist globally, use `relative_factor_x = 1.00`.

This preserves the existing project rule that world conditions may provide an auxiliary relative-expectation effect while preventing VP-style global medians from dominating the system.

## 5. Needs calculation

For a city with population `P`:

```text
supported_basic = floor((gross_food_pre_health + production) / effective_basic_need)
supported_gold = floor(gold / effective_gold_need)
supported_science = floor(science / effective_science_need)
supported_culture = floor(culture / effective_culture_need)
```

Raw deficits:

```text
distress_raw = max(0, P - supported_basic)
poverty_raw = max(0, P - supported_gold)
illiteracy_raw = max(0, P - supported_science)
boredom_raw = max(0, P - supported_culture)
```

Apply flat reductions from the final Building master and future policy/global modifiers:

```text
distress = max(0, distress_raw - VP_DISTRESS_REDUCTION - other_distress_reduction)
poverty = max(0, poverty_raw - VP_POVERTY_REDUCTION - other_poverty_reduction)
illiteracy = max(0, illiteracy_raw - VP_ILLITERACY_REDUCTION - other_illiteracy_reduction)
boredom = max(0, boredom_raw - VP_BOREDOM_REDUCTION - other_boredom_reduction)
```

No Need may become negative.

### Health double-count protection

`gross_food_pre_health` explicitly excludes `Food_from_Health` from `HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`.

Therefore negative Health does not first reduce Food and then create a second Distress penalty. Health affects Happiness only through the dedicated Health Unhappiness term defined below.

## 6. Religious Unrest

Religious Unrest is inactive when the religion system is not active in the city or when the city has no meaningful religious majority/minority structure.

Otherwise:

```text
minority_followers = population following religions other than the city majority religion
religious_unrest_raw = floor(minority_followers / 2)
religious_unrest = max(0, religious_unrest_raw - VP_RELIGIOUS_UNREST_REDUCTION - other_religious_reduction)
```

Pantheon-only population does not count as a hostile minority for this V1 calculation.

## 7. Citizen Needs cap

```text
citizen_needs_unhappiness = min(
    P,
    distress + poverty + illiteracy + boredom + religious_unrest
)
```

This is the main runaway-prevention rule. Multiple simultaneous deficits can explain the problem in the tooltip, but their combined Citizen Needs penalty cannot exceed city population.

For tooltip reporting, show each uncapped post-reduction component and also show the final population cap when it binds.

## 8. Health Unhappiness

Use final `H_city` from `HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`.

| H_city | Health Unhappiness |
|---|---:|
| 0 or higher | 0 |
| -1 to -2 | 1 |
| -3 to -4 | 2 |
| -5 or lower | 3 |

Health Unhappiness is not included inside the Citizen Needs population cap because Health already has its own bounded scale and plague logic. It is also deliberately capped at 3 in V1.

## 9. Local Happiness

Local positive Happiness comes from city-local buildings, local policies, local events and similar effects.

```text
local_happiness_positive = min(P, max(0, sum_local_happiness_sources))
```

The existing `LOCAL_HAPPINESS` field in `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv` contributes here.

Empire-wide luxury/resource Happiness does not enter this city-local positive term. It remains an empire-level quantity and can later affect State Stability and Empire Health through their own interfaces.

## 10. City Happiness interface

The full interface is:

```text
City_Happiness =
    local_happiness_positive
    - citizen_needs_unhappiness
    - health_unhappiness
    - war_weariness_unhappiness
    - occupation_unhappiness
    - colonial_unhappiness
    - policy_burden_unhappiness
```

For City Happiness V1 implementation:

- `war_weariness_unhappiness` is an external input with default 0 until War Weariness V1 is quantified.
- `occupation_unhappiness` is an external input with default 0 until Occupation V1 is quantified.
- `colonial_unhappiness` is an external input with default 0 until Colonial Government burden is quantified.
- `policy_burden_unhappiness` is an external input with default 0 until policy burden is quantified.

The calculator must expose these as named inputs rather than silently omitting them.

No final total clamp is applied in V1. Citizen Needs are population-capped, while war, occupation and colonial shocks may push total City Happiness below negative population if later subsystem rules justify it.

## 11. Required implementation artifacts

Implementation should create:

- `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`
- `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`
- `city_system/calculate_city_happiness_v1.py`
- `city_system/test_calculate_city_happiness_v1.py`
- `city_system/validate_happiness_building_links_v1.py`
- `city_system/CITY_HAPPINESS_STATIC_QA_V1.md`

The existing final Building master is an input authority and must not be rewritten merely to implement Happiness.

## 12. Calculator contract

The calculator must accept at minimum:

- era
- population
- gross Food before Health conversion
- Production
- Gold
- Science
- Culture
- final City Health
- minority followers
- local Happiness sources
- five flat Needs reductions
- optional global median per-capita values for the four output categories
- optional external War Weariness, Occupation, Colonial and Policy Burden inputs

The calculator must return a structured breakdown containing:

- four effective era expectations
- four supported-population values
- five raw Needs
- five post-reduction Needs
- Citizen Needs pre-cap sum
- Citizen Needs final capped value
- Health Unhappiness
- Local Happiness positive value
- each external penalty
- final City Happiness

## 13. Static QA scenarios

At minimum the tests must cover these cases.

### A. Ancient balanced city

Population 4, Food 6, Production 2, Gold 3, Science 3, Culture 2, Health 0, no minority followers, no reductions.

With no relative adjustment:

- supported Basic = 4
- supported Gold = 4
- supported Science = 4
- supported Culture = 5
- Citizen Needs = 0
- final City Happiness = 0 before local/external effects

### B. Ancient severely underdeveloped city

Population 4, Food 4, Production 2, Gold 1, Science 1, Culture 0.

Raw deficits exceed population in total, but final Citizen Needs must equal 4 because of the population cap.

### C. Building reduction works

An otherwise identical city with `VP_ILLITERACY_REDUCTION=1` must reduce Illiteracy by exactly 1 and never below 0.

### D. Health tier works independently

Health -4 produces exactly 2 Health Unhappiness and does not alter Distress input Food.

### E. Religious minority

A city with 5 minority followers produces `floor(5/2)=2` Religious Unrest before reductions.

### F. Local Happiness cap

Population 3 with 5 points of local Happiness sources receives exactly +3 local positive Happiness.

### G. Relative adjustment clamp

A global median that is 50 percent above the era expectation may increase the effective expectation by only 10 percent. A median 50 percent below may reduce it by only 10 percent.

### H. External penalty passthrough

The four external penalty inputs must be added exactly once and reported separately.

## 14. Building-link validation

The validator must scan `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv` and confirm:

- every Needs reduction field is numeric and nonnegative;
- every `LOCAL_HAPPINESS` value is numeric and nonnegative;
- every building row has all five VP Needs reduction columns;
- no Health final value is accidentally read as a Happiness reduction;
- no Stability final value is accidentally read as a Happiness reduction;
- at least one building exists for each of Distress, Poverty, Illiteracy and Boredom reduction in the final master;
- Religious Unrest reduction may validly have fewer or zero building sources if religion-specific relief is primarily supplied by beliefs/policies.

## 15. Error handling

The calculator must reject:

- unknown era names;
- negative population;
- negative gross yield inputs;
- negative flat reductions;
- negative minority follower count;
- minority followers greater than population;
- malformed relative-median inputs.

Population 0 is allowed for test or transitional city objects and returns zero Needs, zero local positive Happiness and only explicitly supplied external penalties.

## 16. Scope boundaries

This pass does not quantify:

- War Weariness
- occupation
- colonial burden
- policy burden
- State Stability
- empire-wide luxury Happiness allocation
- AI decision weights

It only defines the City Happiness numeric core and the interfaces those later systems will use.

## 17. Acceptance criteria

The implementation is acceptable only if:

1. all eight static QA scenarios pass;
2. Building master link validation passes for all 104 current buildings;
3. Health and Stability final fields remain independent and are not reused as Happiness fields;
4. Citizen Needs are population-capped;
5. relative adjustment never exceeds plus or minus 10 percent;
6. the calculator returns a cause-by-cause breakdown suitable for UI and AI use;
7. no runtime/autoplay claim is made because the game engine does not yet exist.
