# Health and Plague Quantitative V1

Date: 2026-09-23
Status: QUANTITATIVE V1 LOCKED FOR PRE-AUTOPLAY

This file supersedes the numerical placeholder section of `HEALTH_AND_PLAGUE_QUALITATIVE_INTEGRATION_V1.md`.

The purpose of this pass is not to reproduce every hidden number from FramedArchitect's old Health & Plague mod. The public resource and forum material confirm the structure but the current CivFanatics download endpoint does not expose the full v19 `Plague.sql` in a directly recoverable form. Therefore exact source facts and project-adapted numbers are explicitly separated.

Primary public references:

- https://forums.civfanatics.com/resources/health-plague-for-bnw-v-19.21416/
- https://forums.civfanatics.com/threads/health-and-plague.499037/page-4
- https://steamcommunity.com/sharedfiles/filedetails/changelog/198143945

## 1. Source facts retained

The following are directly supported by the original mod description, change notes or author posts:

1. City Health depends on fresh water, local resources/features, population and buildings.
2. Empire Health modifies local City Health and is influenced by technologies/policies, Happiness, international trade and difficulty in the source mod.
3. Negative Health makes plague emergence/spread more likely.
4. Roads and sea routes accelerate plague propagation; international trade is especially important.
5. From v11 onward, resource Health is a worked-tile yield: multiple worked copies stack. The author explicitly gives cattle as a positive example and coal, iron and oil as additive negative examples. Merely traded copies do not grant city Health.
6. Aqueduct Health is equivalent to the fresh-water Health bonus in the later source design.
7. v18 changed plague population damage into a Health penalty whose magnitude is tied to plague duration.
8. v19 gives a plague a 10% chance to be virulent; virulent plague lasts 50% longer.
9. Plagues peak around the Medieval period and become less severe/frequent in later eras.

## 2. Project city Health equation

For city `c`:

`H_city = H_water + H_buildings + H_worked_resources + H_worked_features + H_empire - Population - H_pollution + H_active_plague`

where:

- `Population` contributes exactly `-1 Health` per citizen.
- `H_water = 2` if the city has natural fresh water OR an Aqueduct; otherwise 0.
- Natural fresh water and Aqueduct do not stack. The Aqueduct acts as a water-Health floor, not a second +2 on river cities.
- Building values come from `HEALTH_BUILDING_VALUES_V1.csv`.
- Worked resource and feature values come from `HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`.
- Pollution penalty is `-floor(city_pollution / 10)`, capped at `-5`.
- Active plague subtracts Health equal to the final plague duration after medical-building reductions.

This keeps the source's population pressure strong enough to matter while preventing automatic runaway Health from late-game building stacking.

## 3. Health to Food conversion

Health remains an economic yield rather than only a disease meter.

Normal city:

`Food_from_Health = clamp(H_city, -5, +5)`

Additional rules:

- positive Health adds Food only if the city already has positive non-Health food surplus;
- a stagnant/starving city cannot resume growth solely because of positive Health;
- negative Health can reduce Food and therefore can eventually cause ordinary Civ-style starvation/population loss;
- during an active plague, positive Health-to-Food conversion is disabled, while negative Health still applies.

The +/-5 cap is a project balance adaptation. It preserves the source concept but prevents a late Hospital/Sewer/Medical Lab stack from becoming an unlimited Food engine.

## 4. Building Health values

Locked direct values:

- Granary +1
- Aqueduct: water Health floor +2, not an additive +2 when natural fresh water already exists
- Apothecary +2
- Cold Storage +2
- Food Market +1
- Hospital +4
- Sewer +4
- Medical Lab +5
- Recycling Center +2

Special medical/sanitation behavior:

- Apothecary: plague duration -1 turn
- Hospital: plague duration -1 turn
- Medical Lab: plague duration -2 turns
- minimum plague duration after reductions: 3 turns
- Sewer: spontaneous plague emergence chance x0.75

Smokehouse and Water Mill receive no direct Health. Their food role is already substantial.

Factory and fossil power buildings receive no hard-coded negative Health. Their Health cost is mediated through Pollution, so the Power and Health systems remain separable and auditable.

## 5. Empire Health

The source mod used Empire Health. The project retains a deliberately small version so it cannot overwhelm local sanitation.

### Happiness contribution

- global Happiness >= 20: +1
- 0 to 19: 0
- -1 to -9: -1
- <= -10: -2

### Technology/civic contribution

- Sanitation: +1
- Penicillin: +1
- Modern Public Health: +1
- Advanced Assistive Medicine: +1

### International trade malus

Only active international trade routes count.

- every 4 international routes: -1 Empire Health
- trade malus cap: -2

Final Empire Health applied to every city is clamped to `[-3, +3]`.

Difficulty is intentionally excluded from Health V1. The project already has a separate VP-derived AI difficulty system; adding hidden disease difficulty bonuses would double-scale AI/human asymmetry.

## 6. Worked resources and features

The source rule that each worked copy counts independently is retained.

Positive Health resources currently locked at +1 per worked copy:

- Cattle
- Sheep
- Bison
- Deer
- Fish
- Wheat
- Rice
- Maize
- Bananas
- Citrus
- Olives

Negative Health resources at -1 per worked copy:

- Coal
- Iron
- Oil

Negative features at -1 per worked tile:

- Flood Plains
- Marsh
- Jungle/Rainforest

There is no diversity bonus and no Health from merely traded or owned-but-unworked copies. This is important for compatibility with the contact-based dynamic resource system: discovery/trade grants visibility and access, not automatic Health.

## 7. Spontaneous plague emergence

A city with `H_city >= 0` has no spontaneous plague roll.

Base per-turn risk before era and building modifiers:

- Health -1: 0.5%
- Health -2: 1.0%
- Health -3: 2.0%
- Health -4: 4.0%
- Health -5: 7.0%
- Health <= -6: 10.0%

Era multiplier:

- Ancient 0.50
- Classical 0.75
- Late Antiquity 1.00
- Early Medieval 1.25
- High Medieval 1.50
- Renaissance 1.25
- Exploration 1.00
- Enlightenment 0.80
- Industrial 0.65
- Modern 0.50
- Atomic 0.35
- Information 0.25
- Future 0.20

Then apply Sewer x0.75 if present.

This deliberately makes High Medieval the peak while still allowing serious outbreaks in badly managed earlier or later cities.

## 8. Plague duration and virulence

Standard-speed base duration: 6 turns.

Apply medical building reductions:

- Apothecary -1
- Hospital -1
- Medical Lab -2

Minimum final duration: 3 turns.

After that, roll virulence:

- 10% chance
- virulent duration x1.5, rounded to nearest whole turn

The active plague Health penalty equals the resulting duration. Thus a normal unmitigated six-turn plague applies `-6 Health`; a medically advanced city can reduce both duration and the corresponding Health shock.

## 9. Network spread

For each valid infected-city -> recipient-city link per turn:

`P_spread = 0.05 * EraMultiplier * NetworkMultiplier * RecipientHealthMultiplier`

Hard cap per link: 50%.

Network multipliers:

- ordinary nearby/adjacent link: 1.00
- road or rail connection: 1.50
- connected sea route: 1.50
- active international trade route: 2.00
- cross-border contact without trade: 0.50

Recipient Health multiplier:

- Health >= +3: 0.40
- +1 to +2: 0.70
- 0: 1.00
- -1: 1.25
- -2: 1.50
- <= -3: 2.00

This makes Health relevant both to outbreak generation and resistance to imported disease.

## 10. Static sanity scenarios

These are not runtime autoplay results. They are arithmetic checks of the locked equations.

### Ancient viable river city

Population 4, fresh water, Granary, one +1 Health worked resource:

`2 + 1 + 1 - 4 = 0 Health`

No spontaneous plague roll.

### Classical growing city

Population 7, Aqueduct, Granary, two +1 Health resources:

`2 + 1 + 2 - 7 = -2 Health`

Classical spontaneous risk:

`1.0% * 0.75 = 0.75% per turn`

### Late Antiquity medical transition

Population 8, water access, Granary, Apothecary, two positive resources:

`2 + 1 + 2 + 2 - 8 = -1 Health`

Base Late Antiquity risk: 0.5% per turn.

### High Medieval badly managed city

Health -4:

`4% * 1.5 = 6% per turn`

This is the intended high-risk historical window.

### Industrial sanitized city

Population 14 with water, Granary, Apothecary, Cold Storage, Food Market, Hospital, Sewer and two positive resources:

`2 + 1 + 2 + 2 + 1 + 4 + 4 + 2 - 14 = +4 Health`

No spontaneous plague roll before pollution or empire modifiers.

## 11. Files

Authoritative quantitative files for this pass:

- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`

## 12. Autoplay watches

Do not rebalance these before runtime evidence:

1. whether population -1 per citizen makes non-freshwater Ancient starts too punishing;
2. whether the +/-5 Food conversion cap is too strong or too weak;
3. whether the High Medieval 1.50 plague multiplier produces excessive chain outbreaks;
4. whether Sewer + Hospital + Medical Lab makes late-game plagues irrelevant too early;
5. whether worked food-resource Health creates a geographic advantage large enough to distort the dynamic resource/contact system;
6. whether Pollution thresholds duplicate penalties already produced elsewhere.

## Final verdict

**Health quantitative V1 is structurally locked for pre-autoplay integration.**

The system now has explicit city Health arithmetic, building/resource values, empire modifiers, Food conversion, plague emergence, virulence, duration and network spread. Further changes should be driven by runtime data rather than additional speculative tuning.