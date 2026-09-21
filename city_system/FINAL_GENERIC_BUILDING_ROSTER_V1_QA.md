# Final Generic Building Roster V1 QA

Date: 2026-09-21
Status: **PASS**

- Final building rows: **102**
- Duplicate building names: **0**
- Missing technology/civic gate excluding Palace/Monument start buildings: **0**
- Invalid scope values: **0**
- Missing source metadata: **0**
- Broken simple prerequisite references: **0**

## Scope
- CAPITAL_ONLY: 1
- PER_CITY: 83
- ONE_PER_CIV: 9
- ONE_PER_CIV_CHOICE: 9

## Mutually exclusive groups
- GOV_TIER1: Ancestral Hall / Audience Chamber / Warlord's Throne
- GOV_TIER2: Foreign Ministry / Grand Master's Chapel / Intelligence Agency
- GOV_TIER3: National History Museum / Royal Society / War Department
- MUSEUM_BRANCH: Art Museum / Archaeological Museum
- ENTERTAINMENT_BRANCH: Arena / Ferris Wheel
- POWER_SOURCE: Coal Power Plant / Nuclear Power Plant / Solar Plant

## Major reconciliations
- duplicate audit rows removed
- Consulate and Constabulary promoted from moved-source records to canonical buildings
- Museum -> Art Museum / Archaeological Museum
- Gallery -> Art Museum
- Menagerie -> Zoo
- Bastion -> Star Fort
- Broadcast Tower -> Broadcast Center
- Hydro Plant -> Hydroelectric Dam infrastructure upgrade
- Spaceship Factory -> Space Launch Center
- Government Plaza district -> one-per-civilization city/national building
- Water Park district -> coastal building chain Ferris Wheel -> Aquarium -> Aquatics Center

## Authority
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.md`


## Gathering Storm late-era validation

The Future Era realignment moved late environmental/energy buildings with their latest required civic/technology:

Information:
- Flood Barrier
- Recycling Center
- Solar Plant

Future:
- Grid Battery Storage

Additional pre-existing metadata cleanup:
- Coal Power Plant: removed invalid `CIVIC_GATE=Industrialization`
- Steelworks: removed invalid `CIVIC_GATE=Industrialization`
- both inherit Industrialization through the Factory / Power Plant prerequisite chain

Current cross-system validation:
- building rows: 102
- unknown normal civic gates: 0
- content earlier than latest technology/civic gate: 0
- broken simple prerequisite references: 0
- **PASS**
