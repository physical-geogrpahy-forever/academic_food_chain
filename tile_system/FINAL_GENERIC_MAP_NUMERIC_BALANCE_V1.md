# Final Generic Map Numeric Balance V1

Date: 2026-09-21
Status: **LOCKED V1**

Authorities:
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv`
- `tile_system/FINAL_GENERIC_MAP_NUMERIC_BALANCE_V1.csv`
- `tile_system/FINAL_MAP_YIELD_UPGRADE_RULES_V1.csv`
- `tile_system/FINAL_RESOURCE_IMPROVEMENT_COMPATIBILITY_V1.csv`
- `tile_system/FINAL_MORE_LUXURIES_RESOURCE_RULES_V1.csv`

## 1. Source precedence

This layer follows:
`city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md`

Priority:
1. explicit project lock
2. adopted source/mod that supplied the mechanic
3. another adopted source used for reconciliation
4. Civ V BNW fallback
5. project interpolation only when needed

Therefore the map layer does **not** assume the vanilla Civ V resource list.

## 2. Canonical resource coverage

The project has exactly **47 resources**:
- 7 strategic
- 10 bonus
- 30 luxury

Every resource has a primary improvement rule in:
`FINAL_RESOURCE_IMPROVEMENT_COMPATIBILITY_V1.csv`

Important project-added / mod-added mappings:

### More Luxuries
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

Exact More Luxuries base resource yields are preserved separately:
- Coffee +2 Gold
- Tea +2 Gold
- Tobacco +2 Gold
- Perfume +2 Gold
- Amber +2 Gold
- Jade +2 Gold
- Lapis Lazuli +2 Gold
- Coral +2 Gold
- Olives +1 Food +1 Gold

These are **resource yields**, not invented city-building bonuses.

## 3. Core Ancient/Classical improvements

### Farm
Base:
- +1 Food
- build work 700

Project upgrade chain:
- Irrigation: fresh-water Farm +1 Food
- Calendar: improved Wheat/Rice/Maize +1 Food
- Horse Collar: Farm +1 Production
- Fertilizer: non-fresh-water Farm +1 Food
- Civil Engineering: allows eligible Hill Farms

Compatible staple resources:
- Wheat
- Maize
- Rice

### Pasture
Compatible:
- Horses
- Cattle
- Sheep

Base resource-improvement effects:
- Horses/Cattle: +1 Production
- Sheep: +1 Food

Later:
- Fertilizer +1 Food
- Replaceable Parts +1 Production

### Mine
Base:
- +1 Production
- build work 700

Compatible project resources:
- Iron
- Niter
- Coal
- Aluminum
- Uranium
- Copper
- Gems
- Gold
- Salt
- Silver
- Amber
- Jade
- Lapis Lazuli

Later:
- Apprenticeship +1 Production
- Chemistry +1
- Industrialization +1
- Smart Materials +1

### Fishing Boats
Base:
- +1 Food
- Work Boat is consumed
- no ordinary Worker build time

Compatible:
- Fish
- Crab
- Pearls
- Whales
- Coral

Compass:
- +1 Gold

### Plantation
Generic base:
- +1 Gold
- build work 600

Compatible:
- Bananas
- Citrus
- Cocoa
- Cotton
- Dyes
- Incense
- Silk
- Spices
- Sugar
- Wine
- Coffee
- Tea
- Tobacco
- Olives
- Perfume

Bananas retain their resource-specific Food treatment instead of generic Plantation Gold.

Fertilizer:
- +1 Food

### Quarry
Base:
- +1 Production
- build work 800

Compatible:
- Stone
- Marble

Chemistry:
- +1 Production

### Camp
Compatible:
- Bison
- Deer
- Furs
- Ivory
- Truffles

Resource-specific base improvement effect:
- Bison/Deer +1 Production
- Furs/Ivory/Truffles +1 Gold

Economics:
- +1 Gold

The Civ VI Mercantilism Camp bonus remains deliberately excluded.

### Lumber Mill
Base:
- +1 Production
- preserves Forest

Upgrades:
- Machinery +1 Production
- Scientific Theory +1
- Steam Power +1

## 4. Routes

Road:
- movement cost 0.5 per tile
- maintenance 1 Gold/tile
- city connection enabled

Improved Road Movement:
- movement cost 1/3 per tile

Road Bridge Capability:
- roads cross rivers without the normal river movement penalty

Railroad:
- movement cost 0.1 per tile
- maintenance 2 Gold/tile
- city connection
- Capital connection gives city +25% Production

Military Road Construction is a Military Engineer capability rather than a second route type.

## 5. Fortification

Fort:
- +50% defensive modifier

Bastion Fort Upgrade:
- total +75%

Advanced Fortification Upgrade:
- total +100%

The latter two are upgrade rules, not separate buildable improvement objects.

## 6. Former Great Person improvements

Worker-built and nerfed:

Academy:
- +2 Science
- per-city cap 1
- Scientific Theory +1 Science
- Atomic Theory +1

Manufactory:
- +2 Production
- per-city cap 1
- Chemistry +1 Production

Customs House:
- +2 Gold
- per-city cap 1

Holy Site:
- +2 Faith
- per-city cap 1
- working city must have an established religion

Landmark:
- +2 Culture
- per-city cap 1
- Flight +2 Tourism

No Great Person is consumed.

Historic Landmark remains a separate Archaeologist-created antiquity-site improvement.

## 7. Industrial infrastructure

Dam:
- flood damage immunity
- drought Food-loss prevention
- +1 local Happiness
- one per river
- Housing field is retained only if/when the project Housing system is enabled

Hydroelectric Dam Upgrade:
- renewable Power 6

Canal:
- naval / embarked passage through eligible land
- maritime trade-route shortcut

Oil Well:
- +3 Production
- land Oil only

Offshore Oil Rig:
- +3 Production
- sea Oil only

Future extraction upgrade:
- Predictive Systems + Optimization Imperative -> +1 Production to Oil Well / Offshore Oil Rig

Reforestation:
- Worker action that plants Woods
- not a permanent improvement type

National Park:
- Naturalist-created protected area
- ordinary Worker cannot build it
- Tourism derives from the project's scenic/appeal value

## 8. Modern/Future infrastructure

Airstrip:
- 3 aircraft slots

Seaside Resort:
- Gold = scenic/appeal value
- Tourism = scenic/appeal value

Ski Resort:
- +1 local Happiness
- Tourism = scenic/appeal value
- mountain tile may remain unworkable

Wind Farm:
- +1 Production
- +1 Gold
- Power 2

Solar Farm:
- +1 Production
- +1 Gold
- Power 2

Geothermal Plant:
- +2 Production
- +1 Science
- Power 4

Offshore Wind Farm:
- +1 Production
- +1 Gold
- Power 2

Seastead:
- +2 Food
- adjacent Fishing Boat interactions
- adjacent Reef +1 Culture and +1 Tourism
- Housing applies only if the project enables Housing accounting

Power values are supply values for the separate Power-grid system. They do not imply that the entire Power accounting layer is already implemented.

## 9. Saltworks

The project resource-transfer file mentions a possible coastal `SALTWORKS` production facility.

Current canonical map roster:
- does **not** contain Saltworks
- therefore this numeric pass does **not** silently add a 40th map record

Natural Salt currently uses:
- Mine

Saltworks remains an explicit future design candidate and must receive a technology gate and roster decision before implementation.

## 10. Build work

Civ V-style improvements retain Civ V-scale build work where available.

Civ VI/GS improvements use project-scaled Worker build work while retaining their adopted gameplay effects.

Therefore a row labeled:
`CIV6_GS_EFFECT_EXACT_PROJECT_BUILD_WORK`
means:
- effect/yields from Gathering Storm
- Worker construction work adapted to this Civ V-style project

## 11. Status

Current locked layers:
- map records: 39
- resource/improvement compatibility: 47
- More Luxuries exact resource rules: 9
- yield-upgrade rules: 23

The validator ensures the 47-resource table matches the actual project resource catalog rather than the vanilla Civ V resource set.
