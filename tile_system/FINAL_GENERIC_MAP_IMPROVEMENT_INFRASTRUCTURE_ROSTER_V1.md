# Final Generic Map Improvement / Infrastructure Roster V1

Date: 2026-09-21  
Status: **LOCKED / QA TARGET**

Authorities:
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv`
- `tile_system/validate_final_generic_map_roster_v1.py`

## 1. Scope

This roster consolidates the generic map-side construction layer that was previously split across the 109-technology master, 72-civic master and former-Great-Person improvement decision.

Total: **39 records**

Composition:
- 32 technology-master tile/route/infrastructure entries
- 7 civic-only or special archaeology entries
- 28 directly buildable map objects
- 11 capability, upgrade, placement, action or special-area records

The roster deliberately keeps rule unlocks such as Road bridges and Hill Farm placement separate from buildable objects. This prevents a capability from accidentally becoming a second tile type.

## 2. Core buildable improvements and infrastructure

Ancient foundation:
- Farm
- Pasture
- Mine
- Fishing Boats
- Plantation
- Quarry
- Road
- Camp

Classical and medieval:
- Lumber Mill
- Fort
- Dam
- Academy
- Holy Site

Renaissance and Enlightenment:
- Landmark
- Historic Landmark
- Customs House
- Manufactory

Industrial onward:
- Canal
- National Park
- Oil Well
- Railroad
- Airstrip
- Seaside Resort
- Ski Resort
- Offshore Oil Rig
- Wind Farm
- Solar Farm
- Geothermal Plant
- Offshore Wind Farm
- Seastead

## 3. Rule and upgrade records

These are intentionally **not separate ordinary tile objects**:

- Road Bridge Capability -> Engineering
- Fort Construction Specialization -> Military Engineering
- Military Road Construction -> Military Engineering
- Improved Road Movement -> Machinery
- Bastion Fort Upgrade -> Siege Tactics
- Advanced Fortification Upgrade -> Fortification
- Hill Farm Placement -> Civil Engineering
- Reforestation -> Conservation
- Hydroelectric Dam Upgrade -> Electricity

National Park is a `SPECIAL_AREA` created through Naturalist/Conservation rather than an ordinary Worker improvement.

Historic Landmark is a `SPECIAL_IMPROVEMENT` produced by an Archaeologist preserving an Antiquity Site. It remains distinct from the Worker-built Humanism Landmark.

## 4. Former Great Person improvements

The previously locked five-item restoration is incorporated directly:

- Academy -> Education
- Manufactory -> Manufacturing
- Customs House -> Economics + Mercantilism
- Holy Site -> Theology
- Landmark -> Humanism

All five remain nerfed ordinary Worker-buildable improvements and consume no Great Person.

Citadel remains excluded. Military map defense follows:
Fort -> Bastion Fort Upgrade -> Advanced Fortification Upgrade.

## 5. Environmental cross-gates

The renewable-energy layer is now explicit:

- Wind Farm -> Composites + Environmentalism
- Solar Farm -> Ecology + Environmentalism
- Geothermal Plant -> Ecology + Environmentalism
- Offshore Wind Farm -> Predictive Systems + Environmentalism

During consolidation, the Ecology technology text was synchronized from the ambiguous
`Solar Farm; Geothermal Plant with Environmentalism`
to:
`Solar Farm with Environmentalism; Geothermal Plant with Environmentalism`

This matches the already-locked Environmentalism civic, which treats Solar, Wind and Geothermal infrastructure as cross-gated content.

### Gathering Storm era split

- Wind Farm -> Information (Composites + Environmentalism)
- Offshore Wind Farm -> Future (Predictive Systems + Environmentalism)
- Seastead -> Future (Seasteads)

The unlock gates are unchanged; only the project-era classification is realigned.

## 6. Water infrastructure

- Dam -> Buttress
- Hydroelectric Dam Upgrade -> Electricity
- Canal -> Steam Power + Civil Engineering

These are map/infrastructure objects. The project does not restore Civilization VI district placement.

The former Hydro Plant duplicate remains merged into the Hydroelectric Dam upgrade.

## 7. Roads and transport

- Road -> Wheel
- Road Bridge Capability -> Engineering
- Military Road Construction -> Military Engineering
- Improved Road Movement -> Machinery
- Railroad -> Railroad technology

Only Road and Railroad are route objects. Bridge, military construction and movement improvement are route capabilities/upgrades.

## 8. Explicit nonbaseline items

### Citadel
Excluded by the former-Great-Person improvement decision.

### Trading Post
Excluded in the High Medieval and Enlightenment audits. The project uses the BNW-style trade-route structure and does not reintroduce generic Trading Post spam.

### Aerodrome
Not a map district. Airstrip remains the map infrastructure object and Airport is handled in the city-building/infrastructure system.

### Hydro Plant
Not a separate building/improvement. It is merged into Hydroelectric Dam infrastructure.

## 9. Implementation status

This V1 locks:
- map item existence
- map class
- record kind
- technology/civic ownership
- parent object for upgrade/rule records
- broad execution mode

It does **not** yet lock:
- tile yields
- adjacency
- build time
- terrain constraints
- resource consumption
- per-city/per-empire caps
- exact improvement upgrade magnitudes

Those belong to the later map-economy numerical-balance pass.
