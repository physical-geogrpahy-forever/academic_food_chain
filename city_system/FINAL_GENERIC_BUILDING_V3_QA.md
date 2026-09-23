# Generic Building V3 QA

Date: 2026-09-23
Status: PASS - ROSTER GAP RESOLVED / WORKER-GPTI ADAPTATION APPLIED

## Authoritative composition

Building V3 is currently represented as the previous complete roster/numeric table plus a compact authoritative override layer:

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster V3 override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric table: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- numeric V3 override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`

The override files supersede base rows where names match and add new rows where `ACTION=ADD`.

## 1. Smokehouse added

Final placement:

- Era: Ancient
- Gate: Trapping
- Chain: FOOD_HEALTH
- Scope: per city
- Production: 75
- Maintenance: 1

Final functions:

- Camp Production +1
- Food +10 when city border grows
- worked Bison Food +1
- worked Deer Food +1

Why 75 Production:

The project Ancient specialized-building band already places comparable buildings such as Stone Works, Barracks and Library near 75 Production. The current VP gameplay role is adopted, while the project's own era/economy scale controls the cost anchor.

No provisional Health point was added merely because the building is in the FOOD_HEALTH chain. Health remains a separate quantified system.

## 2. Forge added

Final placement:

- Era: Ancient
- Gate: Bronze Working
- Chain: INDUSTRY_POWER
- Scope: per city
- Production: 75
- Maintenance: 1
- Engineer slots: 1
- Science: +1

Final functions:

- Mine Production +1
- Iron Production +1
- Iron Gold +1
- Copper Gold +2

No unsupported flat Production was added. The verified VP production-line role is expressed through Mine/resource enhancement and the Engineer slot.

## 3. Resource-building placeholders eliminated

The former placeholder interactions are now represented directly in:

- `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_V3.csv`

Resolved:

- Bison -> Smokehouse
- Deer -> Smokehouse
- Iron -> Forge
- Copper -> Forge

`PENDING_SMOKEHOUSE_EQUIVALENT` and `PENDING_FORGE_EQUIVALENT` are historical V1/V2 audit labels only and must not be used in implementation.

## 4. Technology gates connected

`tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv` adds:

- Trapping -> Smokehouse
- Bronze Working -> Forge

This V3 delta has precedence over the City Buildings field in `MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv` until a later fully regenerated technology master is emitted.

## 5. Worker-built GPTI adaptation

Project rule:

- Academy, Manufactory, Landmark, Holy Site and Customs House are ordinary Worker-built improvements.
- They do not consume Great People.
- They are `NoTwoAdjacent` and have deliberately reduced base/progression yields.

Therefore two direct VP building bonuses were too strong when copied literally.

### Factory

V2 copied:

- Manufactory Production +2

V3 project adaptation:

- Manufactory Production +1

Factory keeps:

- flat Production +10
- Production/pop +0.25
- Engineer slot 1
- existing project Production percent modifier

### Research Lab

V2 copied:

- Academy Science +4

V3 project adaptation:

- Academy Science +1

Research Lab keeps:

- flat Science +4
- Scientist slot 1
- Great Scientist rate +33%
- local Science +4 from Hospital/Medical Lab/Factory interaction
- Illiteracy reduction from the base V2 row

The reduced tile bonuses prevent a normal Worker from reproducing Great-Person-improvement scaling across a city's workable area.

## 6. Numeric status

Locked now:

- Smokehouse and Forge roster existence
- their technology gates and chains
- resource interactions
- verified VP functional roles
- Factory Manufactory +1 project override
- Research Lab Academy +1 project override

Still global-calibration work:

- a common building Production-cost multiplier, if autoplay requires it
- Health and Power quantitative systems
- whole-economy Science/Culture/Production pacing

Global calibration may scale common costs but must not silently restore the rejected Factory +2 / Research Lab +4 Worker-GPTI bonuses.

## Final verdict

**PASS.**

The previously unresolved VP resource-building gap is now implemented, and the two Worker-built GPTI over-scaling cases are resolved for Building V3.