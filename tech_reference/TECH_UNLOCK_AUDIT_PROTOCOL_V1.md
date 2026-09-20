# Technology Unlock Audit Protocol V1

Date: 2026-09-21
Status: LOCKED RESEARCH METHOD

## 1. Structural baseline

The project uses a **Civilization V-style city and tile structure**.

Therefore the technology audit must not copy Civilization VI district placement.

Use:
- city buildings constructed directly inside the city;
- ordinary tile improvements placed on workable map tiles;
- units;
- resource reveal/exploitation;
- corporation-sector unlocks;
- infrastructure/system unlocks.

Do not use map-placed Civ VI district puzzles as final gameplay objects.

**Structural baseline does not mean source-game unlock placement is binding.**

When Civ V, Civ VI, adopted mods and historical logic disagree, choose the final technology by:
1. historical and functional fit;
2. coherence with the locked 109-tech project tree;
3. avoidance of duplicate unlocks;
4. gameplay progression and era balance;
5. source-game placement only after the above.

Therefore Civ V defines the city/tile **form**, while the project may deliberately move an improvement, building, unit or system to a different technology when that is more coherent. Plantation -> Irrigation is an explicit example.

## 2. Source priority and adopted mod sources

For every technology and every unlock candidate, audit in this order:

1. **Civilization V: Brave New World**
   - primary structural source for city buildings, units, routes and tile improvements;
   - use BNW-era behavior where expansion rules differ from vanilla/Gods & Kings.

2. **Adopted Civilization V expansion/system mods**
   These are not optional afterthoughts. If the project already used a mod to build the technology/system design, its relevant unlock content must also be audited.

   ### Enlightenment Era
   - full content source for the Enlightenment and adjacent transition;
   - audit its technologies, units and buildings, not only the technology names;
   - Wonders remain DEFER_WONDER;
   - remap content to the locked project technologies where the mod's standalone nodes were merged or renamed.

   ### Health & Plague for BNW
   - system/content source for Health, sanitation, epidemic and disease mechanics;
   - especially audit against Sanitation, Biology and Penicillin, and earlier supporting buildings/resources where historically appropriate;
   - candidate mechanics include city Health, fresh-water/building/resource modifiers, plague spawning/spread and disease effects;
   - do not automatically copy its entire balance model: extract useful buildings, technology effects and systems, then adapt them to this project.

   ### Great Works of Film / MoreTech
   - selective adopted source only for Great Director, Cinema, Great Works of Film and directly related media infrastructure;
   - do not import MoreTech's entire technology/building tree.
   - project mapping remains Electricity -> Radio for film/media.

3. **Civilization VI: Gathering Storm**
   - secondary content source;
   - keep useful buildings, units, infrastructure and systems;
   - convert district-dependent content into Civ V-style city buildings/infrastructure where possible;
   - never import a district simply because the source game uses one.

4. **Other specifically approved Civ V mods**
   - may be added to the source registry when they solve a real content/system gap;
   - approval is source-specific: using one element from a mod does not automatically import the whole mod.

5. **Historical addition**
   - only when the locked 109-tech tree has a real implementation gap that the source games and adopted mods do not cover.

The source registry is:
`tech_reference/TECH_UNLOCK_SOURCE_REGISTRY_V1.csv`

Mod content is a **candidate source, not an automatic KEEP**. Every object still passes the same KEEP / ADAPT / REMAP / DROP audit.

## 2A. Parallel civic audit rule

Technology unlock research must audit the project's **72-civic tree in parallel**, with Civilization VI civics used as a major source for institutional content.

Every candidate unlock must be assigned to one of three gate modes:
- **TECH** — material/scientific capability is sufficient;
- **CIVIC** — institution, doctrine, law, culture or organization is the real prerequisite;
- **TECH+CIVIC** — both material capability and institutional organization are necessary.

Examples:
- Library -> Writing (TECH)
- Barracks -> Military Tradition (CIVIC; source-game Bronze Working placement may be overridden)
- Caravan -> Animal Husbandry + Foreign Trade (TECH+CIVIC)
- Great Prophet access -> Astrology + Mysticism (TECH+CIVIC)
- Courthouse -> Writing + Code of Laws (TECH+CIVIC)

Civilization VI civic unlocks to audit include:
- city/infrastructure candidates;
- governments;
- policy cards;
- diplomacy and border rules;
- trade permissions/capacity;
- combat doctrine;
- governor-style systems where relevant.

Civilization-specific unique improvements/buildings found on the Civ VI civic tree are **not** promoted into the generic roster. Record them as civilization-unique/deferred references.

Districts remain subject to the Civ V-style conversion rule: remove district placement, then separately assess any useful building or institution.

## 3. Audit unit

Do not make only one wide row per technology during research.

Use a **long-form unlock audit** where every candidate unlock is one row.

Required fields:

- TECH_EN
- PROJECT_ERA
- UNLOCK_TYPE
- CONTENT_EN
- SOURCE_GAME
- SOURCE_TECH
- SOURCE_FORM
- DECISION
- FINAL_FORM
- FINAL_TECH
- REASON
- NOTES

Allowed UNLOCK_TYPE values:
- UNIT
- CITY_BUILDING
- TILE_IMPROVEMENT
- ROUTE_INFRASTRUCTURE
- RESOURCE_REVEAL
- RESOURCE_EXPLOITATION
- CORPORATION_SECTOR
- SYSTEM
- PROJECT
- GREAT_PERSON_SYSTEM
- WONDER
- POLICY
- GOVERNMENT
- DIPLOMACY
- YIELD_UPGRADE
- DISTRICT

Allowed DECISION values:
- KEEP
- ADAPT_CITY
- ADAPT_TILE
- REMAP_TECH
- MERGE
- REMOVE_GP_IMPROVEMENT
- REMOVE_DISTRICT
- DEFER_WONDER
- DEFER
- DROP
- CROSS_GATE
- MOVE_TO_CIVIC
- MOVE_TO_TECH
- DEFER_CIV_UNIQUE
- DEFER_SYSTEM

## 4. Former Great Person tile-improvement rule

Former Civilization V Great Person tile improvements are **not deleted wholesale**.

The project converts them into **nerfed ordinary Worker-buildable tile improvements** that do not require or consume a Great Person.

Retained:
- Academy — former Great Scientist improvement
- Manufactory — former Great Engineer improvement
- Customs House — former Great Merchant improvement
- Holy Site — former Great Prophet improvement
- Landmark — former Great Artist improvement before Brave New World

Excluded:
- Citadel — former Great General improvement

Final qualitative gates:
- Education -> Academy
- Manufacturing -> Manufactory
- Economics + Mercantilism -> Customs House
- Theology -> Holy Site
- Humanism -> Landmark

Later source-game upgrades may remain:
- Scientific Theory -> Academy Science upgrade
- Atomic Theory -> Academy Science upgrade
- Chemistry -> Manufactory Production upgrade

Landmark distinction:
- Humanism unlocks the generic Worker-built cultural Landmark.
- Natural History may preserve an Antiquity Site as an archaeological Historic Landmark.
- These are related but distinct mechanics.

Citadel remains excluded because the project already has:
Fort -> Bastion Fort -> Advanced Fortification,
and Civ5 Citadel's territory seizure / adjacent damage is too specialized for an ordinary Worker improvement.

Great People retain active/system roles and are not consumed to construct these improvements.

Exact yields, build times, placement restrictions and caps are numerical balance items.

Authority:
`tile_system/FORMER_GREAT_PERSON_TILE_IMPROVEMENTS_V1.md`

## 5. Civilization VI district conversion rule

District itself:
- REMOVE_DISTRICT

District building:
- evaluate individually.

Examples:
- Campus -> remove district
- Library -> CITY_BUILDING
- University -> CITY_BUILDING
- Research Lab -> CITY_BUILDING

- Commercial Hub -> remove district
- Market -> CITY_BUILDING
- Bank -> CITY_BUILDING
- Stock Exchange -> CITY_BUILDING

- Industrial Zone -> remove district
- Workshop -> CITY_BUILDING
- Factory -> CITY_BUILDING
- Power Plant -> CITY_BUILDING

- Theater Square -> remove district
- Amphitheater -> CITY_BUILDING
- Museum -> CITY_BUILDING
- Broadcast building -> CITY_BUILDING

- Encampment -> remove district
- Barracks -> CITY_BUILDING
- Armory -> CITY_BUILDING
- Military Academy -> CITY_BUILDING

Aqueduct, Dam, Canal and Neighborhood must be audited as:
- city infrastructure;
- tile infrastructure;
- route/infrastructure system;
- or dropped.

Do not preserve their Civ VI district semantics automatically.

## 6. World Wonder rule

World Wonders are not assigned during the ordinary technology audit.

Every Wonder candidate gets:
- UNLOCK_TYPE = WONDER
- DECISION = DEFER_WONDER

The separate Wonder audit remains authoritative.

## 7. Technology remapping rule

The 109 technology nodes are already locked.

Source-game unlocks do **not** have to stay on the source game's technology if the merged project chronology would be wrong.

Use REMAP_TECH when:
- the source-game technology no longer exists;
- the source game's era placement conflicts with the project chronology;
- the content is better attached to one of the project's added historical nodes.

Examples:
- paper-related content can move to Papermaking;
- printing-related content can distinguish Block Printing from Printing;
- early gunpowder content can attach to Gunpowder rather than a later firearm node;
- film production is already locked to Electricity, with Radio as later media upgrade.

## 8. Resource rule

Audit resource interactions separately from buildings.

For each technology ask:
1. Does it reveal a map resource?
2. Does it permit extraction/improvement?
3. Does it unlock processing?
4. Does it unlock a corporation sector using that resource?

Example:
Oil can have distinct rows for:
- reveal;
- well/extraction;
- Refining;
- Petroleum corporation;
- Refined Petroleum Products.

Do not collapse these into one generic "Oil unlocked" event.

## 9. Corporation integration

Use:
`corporations/corporation_tech_unlock_map_v1.csv`

Corporation rows are already mapped to the 109-tech tree.

During the technology audit:
- import those rows;
- do not independently reinvent corporation gates.

## 10. Final technology summary

After the long-form audit is complete, generate one summary row for each of the 109 technologies with:

- Units
- City Buildings
- Tile Improvements
- Routes/Infrastructure
- Resource Reveal
- Resource Exploitation
- Corporation Unlocks
- Systems/Projects

The long-form file remains the audit authority.
The 109-row summary is the gameplay/design reference.

## 11. Recommended work order

Audit by era, not by content type:

1. Ancient
2. Classical
3. Late Antiquity
4. Early Medieval
5. High Medieval
6. Renaissance
7. Exploration
8. Enlightenment
9. Industrial
10. Modern
11. Atomic
12. Information

For each era:
- collect Civ V BNW unlocks;
- collect relevant adopted-mod unlocks (especially Enlightenment Era and any system-specific source such as Health & Plague);
- collect relevant Civ VI GS additions;
- classify;
- remap;
- remove district/GP-improvement/Wonder content;
- run duplicate and empty-tech QA.

Do not research all 109 technologies in one giant pass.


## Civ VI fallback rule

When a project technology or civic remains materially empty after:
1. checking Civilization V BNW,
2. checking already adopted Civilization V mods,
3. resolving source conflicts by historical and functional fit,

**actively use Civilization VI technology/civic content to fill the gap.**

Priority:
- preserve Civ V-style city and tile structure;
- convert Civ VI districts into direct city buildings, tile infrastructure, national buildings or systems;
- keep generic Civ VI units/buildings/policies when they fit;
- keep civilization-unique content unique;
- do not import Governor-only, Giant Death Robot-only, district-adjacency, or victory-only effects literally when they do not fit the project;
- adapt those effects into ordinary systems where possible before inventing brand-new content.

In short:
**Civ V first -> historical/functional reconciliation -> Civ VI fallback -> minimal historical invention.**
