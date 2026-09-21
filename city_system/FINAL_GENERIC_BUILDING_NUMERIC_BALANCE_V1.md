# Final Generic Building Numeric Balance V1

Date: 2026-09-21  
Status: **LOCKED V1**

Authorities:
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv`

## Scope

This table assigns a numerical baseline to all **102** generic/national buildings.

Locked numeric fields include:
- Production Cost
- Gold maintenance
- flat Food / Production / Gold / Science / Culture / Faith
- Local Happiness
- city-defense Strength and HP
- Food carryover
- city Production / building Production / Gold / Science / Culture modifiers
- generic military XP
- specialist slots
- flat Great Person points where the source building itself generates them
- Great Work type and capacity
- structured special effects

## Numerical philosophy

The project remains **Civ V-scale**.

Priority:
1. direct Civ V BNW value
2. Civ V functional remap
3. Civ VI building converted from district dependence into a direct city building
4. Pouakai Enlightenment Era adaptation
5. project/historical interpolation

Source grades in the CSV:
- `A_CIV5_BNW_EXACT`
- `B_CIV5_FUNCTIONAL_REMAP`
- `B_CIV6_ADAPTED`
- `B_EE_ADAPTED`
- `B_PROJECT_INTERPOLATED`

Current distribution:
- Civ V direct: 45
- Civ V functional remap: 4
- Civ VI adapted: 31
- Pouakai adapted: 4
- project/interpolated: 18

## Representative Civ V anchors

### Science
- Library: 75 Production, 1 maintenance, +1 Science per 2 Population
- University: 160 / 2, +33% Science, 2 Scientist slots, worked Jungle +2 Science
- Public School: 300 / 3, +3 Science, +1 Science per 2 Population, 1 Scientist slot
- Research Lab: 500 / 3, +4 Science, +50% Science, 1 Scientist slot
- Observatory: 200 / 0, +50% Science

### Production
- Workshop: 120 / 2, +2 Production, +10% Production, 1 Engineer slot
- Windmill: 250 / 2, +2 Production, +10% building Production, 1 Engineer slot
- Factory: 360 / 3, +4 Production, +10% Production, 2 Engineer slots
- Solar Plant: 500 / 3, +5 Production, +15% Production

### Gold
- Market: 100 / 0, +1 Gold, +25% Gold, 1 Merchant slot
- Bank: 200 / 0, +2 Gold, +25% Gold, 1 Merchant slot
- Stock Exchange: 300 / 0, +3 Gold, +25% Gold, 2 Merchant slots

### Growth
- Granary: 60 / 1, +2 Food, +1 Food from Wheat/Bananas/Deer
- Water Mill: 75 / 2, +2 Food, +1 Production
- Aqueduct: 100 / 1, 40% Food carryover
- Hospital: 360 / 2, +5 Food
- Medical Lab: 500 / 3, +25% Food carryover

### Defense
- Walls: 75, +5 Defense, +50 HP
- Castle: 160, +7 Defense, +25 HP
- Arsenal: 300, +9 Defense, +25 HP
- Military Base: 500, +12 Defense, +25 HP

### Culture
- Monument: 40 / 1, +2 Culture
- Amphitheater: 100 / 2, +1 Culture, 1 Writing slot
- Opera House: 200 / 1, +1 Culture, 1 Music slot
- Broadcast Center: 500 / 3, +1 Culture, +33% Culture, 1 Music slot

## Great Person buildings

Civ V guild progression:
- Writers' Guild: 100 / 1, 2 Writer slots, +1 flat Great Writer point
- Artists' Guild: 150 / 1, 2 Artist slots, +2 flat Great Artist points
- Musicians' Guild: 200 / 1, 2 Musician slots, +3 flat Great Musician points

Project film equivalent:
- Director's Guild: 300 / 1, 2 Director slots, +3 flat Great Director points

This does not replace specialist-generated Great Person points; it records the building's own flat component separately.

## Government buildings

The Civ VI Government Plaza district itself is **not** used as a map district. It is represented as a one-per-civilization city institution.

Tier costs retain the source scale where practical:
- Tier 1: 150 Production / 1 maintenance
- Tier 2: 290 / 2
- Tier 3: 440 / 3

Governor titles and Governor-only conditions are removed.

### Tier 1
Ancestral Hall:
- +50% Production toward founding units in its city
- source free Builder effect is explicitly **removed**
- this preserves the locked rule that founding a city never creates a free Worker

Audience Chamber:
- Governor dependency removed
- project tall-administration translation:
  - Capital and Courthouse cities +2 Local Happiness
  - +10% Growth

Warlord's Throne:
- after capturing an enemy city, all cities +20% Production for 5 turns

### Tier 2
Foreign Ministry:
- city-state levy Gold cost -50%
- levied/suzerain city-state units +4 Combat
- no invented Diplomatic Favor yield

Grand Master's Chapel:
- purchase land military units with Faith
- pillaging grants Faith
- no invented flat Faith yield

Intelligence Agency:
- +1 Spy capacity
- source "higher chance of success" retained as an espionage-system bonus, without inventing a false source number

### Tier 3
National History Museum:
- 4 slots for any Great Work
- no invented base Culture

Royal Society:
- Civ VI Builder-charge consumption cannot transfer because the project uses persistent Workers
- project translation: +20% city-project Production in the government-center city
- Workers are **not consumed**

War Department:
- units heal up to 20 HP after eliminating an enemy unit

## Direct-city conversion of Civ VI district buildings

District placement is removed.

Examples:
- Arena: +2 Local Happiness
- Ferris Wheel: +2 Local Happiness, +3 Culture, +2 Tourism
- Aquarium: +1 Local Happiness; coastal resources, Reefs and Shipwrecks +1 Science
- Aquatics Center: +2 Local Happiness; coastal/lake-adjacent Wonders provide Tourism
- Shopping Mall: +2 Gold, +1 Local Happiness, +4 Tourism
- Food Market: +4 Food under the Gathering Storm-era direct-city adaptation
- Art Museum: +2 Culture, 3 Art slots
- Archaeological Museum: +2 Culture, 3 Artifact slots
- National History Museum: 4 ANY Great Work slots

## Project culture/film chain

Project Film content uses:
- Cinema: 300 / 2, +2 Culture, 2 Film slots
- Director's Guild: 300 / 1, 2 Director slots, +3 Great Director points
- Film Studio: 450 / 3, +2 Culture, 2 Film slots, Film Tourism +50%

These are explicitly project values, not claims about Civ V.

## Conditional tech/civic effects are not double-counted

Existing locked conditional effects remain outside base building yields.

Examples:
- Paper Workshop +1 Science/+1 Culture from Papermaking + Recorded History
- Algebra scholarship bonuses to Library / Scriptorium / Paper Workshop
- Algebra administration bonuses to Courthouse / Market
- University +1 Great Scientist point from Education + Scholasticism
- University +10% Science from Scientific Revolution
- Woodblock Printing House bonus to Great Works of Writing
- Palace Great Work slot additions from Court Culture

The base table points to these with `SPECIAL_EFFECTS` rather than re-adding the same yield.

## Health and Power

This V1 locks **building cost, maintenance and ordinary yields** even where a larger system is unfinished.

The following tags deliberately remain system-level placeholders:
- `HEALTH_SYSTEM_EFFECT=PENDING`
- `POWER_SYSTEM_OUTPUT=PENDING`
- `POWER_SYSTEM_CAPACITY=PENDING`
- `POLLUTION_SYSTEM_EFFECT=PENDING`

Therefore:
- Hospital's +5 Food is locked even though later Health effects are not
- Apothecary and Sewer keep their baseline city-building values while Health is finalized later
- Power Plant / Coal / Nuclear / Solar / Grid Battery ordinary production values are locked, while exact electricity accounting remains later work

Source-specific plants use:
`REPLACES_POWER_PLANT_OUTPUT=1`

This prevents the generic Power Plant output from stacking twice with a selected source-specific plant.

## Recycling Center

The old Civ V effect that directly creates Aluminum is **not** copied.

Project V1:
- +2 Gold
- city pollution -25%
- maintenance 3
- old Aluminum-generation effect explicitly removed

## Art Museum era correction

The previous roster placed Art Museum in Renaissance while requiring Opera House from Exploration.

That impossible prerequisite order is corrected:
- Art Museum -> **Exploration**
- Opera House prerequisite remains

No other building prerequisite points backward in era after the correction.

## Status

All 102 rows:
`NUMERIC_STATUS=LOCKED_BUILDING_V1`

System-placeholder tags identify only the unfinished external system layer; they do not mean the building row itself is missing.
