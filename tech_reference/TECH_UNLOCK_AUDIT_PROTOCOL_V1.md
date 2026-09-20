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

## 2. Source priority

For every technology and every unlock candidate, audit in this order:

1. **Civilization V: Brave New World**
   - primary structural source for city buildings, units, routes and tile improvements;
   - use BNW-era behavior where expansion rules differ from vanilla/Gods & Kings.

2. **Civilization VI: Gathering Storm**
   - secondary content source;
   - keep useful buildings, units, infrastructure and systems;
   - convert district-dependent content into Civ V-style city buildings/infrastructure where possible;
   - never import a district simply because the source game uses one.

3. **Civilization V Enlightenment Era / already adopted project references**
   - gap filling only.

4. **Historical addition**
   - only when the locked 109-tech tree has a real implementation gap that the source games do not cover.

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

## 4. Great Person tile-improvement rule

Great-Person-consumed tile improvements are removed from the normal project baseline.

Default removal:
- Academy — Great Scientist
- Manufactory — Great Engineer
- Customs House — Great Merchant
- Citadel — Great General
- Holy Site — Great Prophet

Reason:
- the project does not want Great People to be primarily consumed as permanent yield tiles;
- Great People already have stronger active/system roles;
- corporations, Great Works, research bursts, engineering actions, trade actions and military command are cleaner than one-off super-tiles.

Important BNW distinction:
- Landmark is **not automatically removed** merely because older Civ V versions associated it with Great Artists.
- In Brave New World, Landmark belongs to the archaeology layer and must be audited separately with Archaeology/Antiquity Site mechanics.

Thus:
**remove Great-Person tile placement, not every historically related improvement name.**

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
- collect relevant Civ VI GS additions;
- classify;
- remap;
- remove district/GP-improvement/Wonder content;
- run duplicate and empty-tech QA.

Do not research all 109 technologies in one giant pass.
