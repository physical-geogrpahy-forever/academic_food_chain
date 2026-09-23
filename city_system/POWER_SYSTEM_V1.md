# Power System V1

Date: 2026-09-23
Status: STRUCTURE AND CORE NUMERICS LOCKED

## 1. Source precedence

The project explicitly adopted the Civilization VI: Gathering Storm Power/climate/renewable-energy mechanic. Therefore Power-specific fields use Gathering Storm as the primary source under `PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md`.

Project adaptations are required because this project uses:

- Civ V-style direct city buildings rather than districts;
- persistent Workers rather than Builder charges;
- strategic-resource capacity rather than the Gathering Storm stockpile/depletion model;
- mixed VP/Civ V/Civ VI building roles.

Authoritative numeric tables:

- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`

## 2. City Power state

Power is evaluated once per turn for each city.

Let:

`PowerDemand(city) = sum(PowerLoad of all completed power-consuming buildings)`

and

`PowerSupply(city) = local renewable supply + allocated network supply`.

A city is:

- `POWERED` if `PowerSupply >= PowerDemand`
- `UNPOWERED` otherwise

There is no partial powered state in V1.

If a city is UNPOWERED:

- all ordinary base project building yields/effects remain;
- none of the `POWERED_BONUS` effects in `POWER_DEMAND_BUILDING_V1.csv` apply.

If a city is POWERED:

- all listed powered bonuses apply simultaneously.

This preserves the Gathering Storm all-or-nothing city status and avoids building-priority micromanagement.

## 3. Power demand

Power-consuming project buildings:

- Factory: 2
- Stock Exchange: 3
- Research Lab: 3
- Broadcast Center: 3
- Film Studio: 3
- Food Market: 1
- Shopping Mall: 1
- Airport: 1
- Stadium: 2
- Aquatics Center: 2

The project does not invent Power loads for buildings that do not have a Gathering Storm Power requirement merely because they are modern.

## 4. Powered bonuses

Gathering Storm incremental powered effects are treated as a separate field layered over the project's existing building role.

- Factory: +3 Production
- Stock Exchange: +7 Gold
- Research Lab: +5 Science
- Broadcast Center: +4 Culture
- Film Studio: +4 Culture
- Food Market: +2 Food
- Shopping Mall: +2 Gold and +1 Local Happiness
- Airport: +2 Production
- Stadium: +2 Local Happiness
- Aquatics Center: +2 Local Happiness

This does not replace VP/project baseline effects. It is the reward for satisfying the Power mechanic.

Aquatics Center base Local Happiness is corrected from 2 to 1 so the GS-derived base/powered split is 1 + 2 rather than 2 + 2.

## 5. Renewable sources

### Hydroelectric Dam

- +6 Power
- own city
- no emissions
- requires the project Dam infrastructure and Electricity

### Solar Farm

- +1 Production
- +1 Gold
- +2 Power
- own city
- flat land; no Snow under the GS terrain rule unless a later project terrain adaptation explicitly changes this
- project gate: Ecology + Environmentalism

### Wind Farm

- +1 Production
- +2 Gold
- +2 Power
- own city
- Hills
- project gate: Composites + Environmentalism

### Geothermal Plant

- +2 Production
- +1 Science
- +4 Power
- own city
- requires a Geothermal Fissure or a separately implemented project geothermal-potential tile layer
- project gate: Ecology + Environmentalism

### Offshore Wind Farm

- +2 Production
- +2 Power
- own city
- Coast or Lake
- project gate: Predictive Systems + Environmentalism

No Gold is added in V1 because the current Gathering Storm Civilopedia data used for this pass lists +2 Production and +2 Power for Offshore Wind Farm.

## 6. Fuel-based city power plants

The project does not use Gathering Storm's accumulating strategic-resource stockpile. Instead, fuel plants reserve available strategic-resource capacity while they are supplying electricity.

### Coal Power Plant

- network radius: city centers within 6 hexes
- 1 uncommitted Coal capacity supports 4 Power
- heavy emissions

### Power Plant = Oil role

The existing generic project `Power Plant` is assigned the Gathering Storm Oil Power Plant fuel behavior rather than adding a duplicate new roster building.

- network radius: 6 hexes
- 1 uncommitted Oil capacity supports 4 Power
- moderate emissions

Its existing project Production effects remain the building baseline.

### Nuclear Power Plant

- network radius: 6 hexes
- 1 uncommitted Uranium capacity supports 16 Power
- minuscule emissions relative to fossil fuels
- reactor age/accident risk remains a separate later module

## 7. Strategic-resource capacity accounting

Power uses only currently uncommitted resource capacity after permanent unit/resource commitments are reserved.

For each fuel type:

`AvailableForPower = TotalResourceCapacity - UnitAndOtherCommittedCapacity`

Maximum fuel Power is:

- Coal: `4 * AvailableCoalForPower`
- Oil: `4 * AvailableOilForPower`
- Uranium: `16 * AvailableUraniumForPower`

Fuel is not permanently depleted in V1. Capacity is reserved and released turn by turn according to electricity demand.

This is a project adaptation required by the existing Civ V-style strategic-resource economy.

## 8. Allocation priority

Default automatic supply order:

1. own-city renewable improvements and Hydroelectric Dam
2. networked Solar Plant building supply
3. Nuclear Power Plant
4. Oil-role Power Plant
5. Coal Power Plant

Within the same tier, use the nearest eligible network source first; ties may use stable city ID/order for deterministic simulation.

Rationale:

- zero-emission energy is used before fuel capacity;
- nuclear is four times as resource-efficient as fossil fuel in the adopted GS ratio;
- Oil is preferred to Coal when both have the same 4 Power/resource efficiency because its emission class is lower.

## 9. Solar Plant city building

The project already contains a Civ V-derived Solar Plant city building, while Gathering Storm supplies solar electricity through tile improvements instead.

Project adaptation:

- fixed +6 Power
- 6-hex city network
- zero emissions
- existing building Production effects retained

+6 is intentionally equivalent to:

- one GS Hydroelectric Dam, or
- three Solar Farms.

It provides a late compact urban renewable option without making Solar Farms irrelevant.

## 10. Grid Battery Storage

Grid Battery Storage generates 0 Power.

Its exact storage/discharge capacity is not invented in this pass because Gathering Storm has no direct generic building counterpart and the base V1 electricity sources are deterministic rather than weather-variable.

Status remains:

`DEFERRED_STORAGE_RULE`

The building remains in the roster for a later renewable-network/reliability module.

## 11. Pollution link

Power V1 records emission classes only:

- ZERO
- MINUSCULE
- MODERATE
- HEAVY

Exact CO2/pollution points are not invented here. The later climate/pollution pass must map these classes to project global-warming quantities.

## 12. Implementation notes

Power-specific values supersede earlier `POWER_SYSTEM_OUTPUT=PENDING`, `POWERED_BONUS_HANDLED_BY_POWER_SYSTEM_PENDING`, and equivalent placeholders.

Building base yields and VP Needs/Health effects continue to follow their own source layers.

## Final verdict

Core Power supply, demand, powered bonuses, network range and strategic-resource translation are **LOCKED V1**.

Remaining Power-adjacent work:

- geothermal placement layer if the map does not already expose a geothermal feature;
- Grid Battery Storage capacity;
- numeric pollution/CO2 conversion;
- autoplay balance for late-game Power availability.