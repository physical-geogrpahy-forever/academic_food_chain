# VP Resource-Building Gap Resolution V2

Date: 2026-09-23
Status: SECOND-PASS RESOURCE/BUILDING RESOLUTION

The first resource-building interaction pass left two unresolved VP building classes: Smokehouse and Forge. Because the project has now adopted Vox Populi as the default gameplay baseline, these functions should not be silently mapped onto unrelated late buildings.

## 1. Smokehouse

Decision: **ADD AS A GENERIC BUILDING IN THE NEXT BUILDING-ROSTER REVISION**

Reason:
- Current VP explicitly has a Smokehouse building class.
- VP describes it as a growth/production building that boosts Camps and camp resources and gives Food when borders expand.
- The current project has no early building with the same role.
- Mapping Bison/Deer to Industrial Cold Storage would place the interaction far too late.

Resource interactions to preserve:

- Bison: Smokehouse -> Food +1
- Deer: Smokehouse -> Food +1

Provisional project placement:

- Gate: Trapping
- Chain: `FOOD_HEALTH` or a rural-production subchain
- Exact Production cost and all non-resource yields: pending building V3 numeric pass

## 2. Forge

Decision: **ADD AS AN EARLY GENERIC BUILDING IN THE NEXT BUILDING-ROSTER REVISION**

Reason:
- The old project rejected a generic Forge only because it was being considered at the much later Renaissance `Metal Casting` node.
- VP instead places Forge at Bronze Working, which removes that chronology problem.
- VP uses Forge as an early Engineer/production building and ties it to mined-resource development.
- Mapping its Iron/Copper effects to Exploration Gunsmith or Industrial Steelworks would delay the resource economy by several eras.

Verified VP role elements to carry forward:

- Gate: Bronze Working
- Engineer specialist slot: 1
- Science: +1
- Mine Production: +1

Resource interactions to preserve:

- Iron: Production +1, Gold +1
- Copper: Gold +2

Exact Production cost and final chain placement are deferred to the building V3 pass.

## 3. Why not reuse current buildings

Rejected mappings:

- Smokehouse -> Cold Storage: too late and industrial refrigeration is a different process.
- Smokehouse -> Granary: would overload the already broad grain-storage building and erase the camp-specialization role.
- Forge -> Gunsmith: too late and firearm manufacture is narrower than early metalworking.
- Forge -> Steelworks: too late and steel mass production is a different industrial stage.
- Forge -> Stone Works: wrong material/production identity.

## 4. Consequence for authoritative data

Until `FINAL_GENERIC_BUILDING_ROSTER_V2/V3` is regenerated:

- `PENDING_SMOKEHOUSE_EQUIVALENT` should be interpreted as **future generic Smokehouse**.
- `PENDING_FORGE_EQUIVALENT` should be interpreted as **future generic Forge at Bronze Working**.

No current building should receive those bonuses as a temporary substitute.
