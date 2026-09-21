# Final Generic Map Numeric Source Audit V1

Date: 2026-09-21

## Source hierarchy

Authority:
`city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md`

### Civ V BNW
Used primarily for:
- Farm / Pasture / Mine / Fishing Boats / Plantation / Quarry / Road / Camp / Lumber Mill / Fort
- route movement/maintenance baseline
- Oil Well / Offshore Oil Rig baseline
- standard technology yield upgrades where the project did not override them

Reference:
https://civilization.fandom.com/wiki/List_of_improvements_in_Civ5

### Barathor More Luxuries
Used for the nine adopted extra luxuries.

Reference:
https://civilization-v-customisation.fandom.com/wiki/Barathor%27s_More_Luxuries
https://steamcommunity.com/sharedfiles/filedetails/?id=167389120

Locked source mapping:
- Coffee -> Plantation, +2 Gold
- Tea -> Plantation, +2 Gold
- Tobacco -> Plantation, +2 Gold
- Olives -> Plantation, +1 Food +1 Gold
- Perfume -> Plantation, +2 Gold
- Amber -> Mine, +2 Gold
- Jade -> Mine, +2 Gold
- Lapis Lazuli -> Mine, +2 Gold
- Coral -> Fishing Boats, +2 Gold

Do not replace this with Vox Populi or Resource Compendium remaps.

### Project resource expansion
Project-added:
- Maize -> Farm
- Rice -> Farm
- Niter -> Mine

These follow explicit project resource and technology decisions.

### Civ VI / Gathering Storm
Used for:
- Dam
- Canal
- National Park
- Airstrip
- Seaside Resort
- Ski Resort
- Wind Farm
- Solar Farm
- Geothermal Plant
- Offshore Wind Farm
- Seastead
- Hydroelectric Dam upgrade

District/Builder-charge logic is translated into the project's Civ V-style Worker/infrastructure framework.

### Project former-Great-Person conversion
Used for:
- Academy
- Manufactory
- Customs House
- Holy Site
- Landmark

Their worker-buildable nerfed values are project decisions, not original Civ V Great Person improvement values.

## Key anti-regression rules

- The resource compatibility table must contain exactly the project's 47 resources.
- More Luxuries' nine resources must not be reassigned to vanilla-only improvements.
- Amber/Jade/Lapis use Mine in the adopted original More Luxuries mapping.
- Coral uses Fishing Boats.
- Maize/Rice use Farm.
- Oil uses Oil Well on land and Offshore Oil Rig at sea.
- Salt remains Mine until Saltworks is explicitly added to the canonical map roster.
- Civ VI/GS effects can be exact while Worker build work remains project-scaled.
