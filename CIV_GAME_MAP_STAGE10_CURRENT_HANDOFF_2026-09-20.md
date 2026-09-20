# CIV GAME MAP STAGE 10 — CURRENT HANDOFF / GITHUB INVENTORY

Date: 2026-09-20  
Repository: `physical-geogrpahy-forever/academic_food_chain`  
Branch: `civ-game-map-stage1b-etopo2022`

## 1. Purpose

This is the current handoff file for the Civilization-style world map resource work.

It records:
- the locked map/resource baseline,
- the Stage10Y preview and audit,
- the `resource_fix_v1` review build,
- Resource Icon V4,
- the contact-based dynamic resource system,
- the exact GitHub paths that should be treated as the handoff inventory.

## 2. Locked map baseline

- CRS: EPSG:8857
- Parent grid: 335 x 781 = 261,635 hexes
- LAND: 68,048
- LAKE: 882
- COAST: 8,781
- OCEAN: 156,201
- VOID: 27,723
- Stage1A 1-degree data is abandoned and must not be used.
- Stage1B relief uses NOAA ETOPO 2022 v1 60 arc-second.
- Stage2B terrain/biome is the current terrain/biome baseline.

## 3. Locked resource roster

47 map resources total.

Strategic 7:
HORSES, IRON, NITER, COAL, OIL, ALUMINUM, URANIUM

Bonus 10:
BANANAS, BISON, CATTLE, DEER, FISH, SHEEP, STONE, WHEAT, MAIZE, RICE

Luxury 30:
CITRUS, COCOA, COPPER, COTTON, CRAB, DYES, FURS, GEMS, GOLD, INCENSE, IVORY, MARBLE, PEARLS, SALT, SILK, SILVER, SPICES, SUGAR, TRUFFLES, WHALES, WINE, COFFEE, TEA, TOBACCO, OLIVES, PERFUME, AMBER, JADE, LAPIS_LAZULI, CORAL

Display decisions:
- COCOA is displayed with a chocolate icon.
- PERFUME is displayed in Korean as 향수.
- Internal IDs remain COCOA and PERFUME.

## 4. Stage10Y original preview

Stage10Y V2 remains a preview, not canonical final.

Targets and actual:
- strategic 2,500
- bonus 5,000
- luxury 5,000
- total 12,500
- one-resource-per-hex PASS

Surface counts:
- LAND 10,896
- COAST 639
- OCEAN 965
- LAKE 0
- VOID 0

Regional density differences are not a balancing defect by themselves. Do not smooth or equalize real geographic concentration unless a source or processing error is demonstrated.

## 5. Source-GPKG audit

The previous world/regional TIFF renderings were judged unreliable for positional QA because resources had been overlaid using an image-coordinate transform rather than rendered directly from source GPKG geometry.

The Stage10Y source GPKG was therefore audited directly.

Audit results:
- selected resource cells: 12,500
- unique selected IDs: 12,500
- duplicate selected cells: 0
- LAND resources: 10,896
- COAST resources: 639
- OCEAN resources: 965
- LAKE/VOID resources: 0
- basic surface rules: PASS
- selected zero/negative evidence: none

Korea LAND-only audit window:
- 124–131E
- 33–39.8N
- resource-bearing LAND cells: 28
- RICE 7
- HORSES 6
- TOBACCO 4
- WINE 4
- CITRUS 2
- COAL 1
- IRON 1
- CATTLE 1
- JADE 1
- MAIZE 1

Therefore the apparent absence of Korean land resources in the old TIF/PNG was a rendering/alignment failure, not an empty placement table.

Do not use the old image-coordinate overlay for future positional validation.

## 6. Biological plateau audit

Three resources failed the plateau audit:

- BISON: 10,738 top-tie candidates for 390 selected
- IVORY: 15,552 top-tie candidates for 248 selected
- WHALES: 3,695 top-tie candidates for 350 selected

Old anomalies:
- BISON desert-biome selections: 21
- IVORY desert-biome selections: 44
- IVORY temperate-biome selections: 8
- WHALES south/north: 336/14

## 7. resource_fix_v1 review build

A replacement set was built for only BISON, IVORY and WHALES. The other Stage10Y selections are retained.

Before/after:
- BISON desert-biome: 21 -> 0
- IVORY desert-biome: 44 -> 0
- IVORY temperate-biome: 8 -> 0
- WHALES south/north: 336/14 -> 176/174
- WHALES tropical/subtropical: 11 -> 35

Review quota pools:
- BISON: North America 176, Europe 70, Central/South Asia 100, East Asia 44
- IVORY: Africa 198, South+Southeast Asia 50
- WHALES: North temperate/subpolar 123, South temperate/subpolar 158, North tropical/subtropical 17, South tropical/subtropical 18, high-latitude fringe 34

Status:
- review build only
- not canonical final

Authoritative integrated review-build table:
`civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`

This is the full 12,500-row placement table and is the primary handoff artifact.

## 8. Resource Icon V4

GitHub directory:
`civ_map_stage10_resources/icons_v4/`

Rules:
- strategic badge: hexagon
- bonus badge: circle
- luxury badge: rounded diamond
- SVG/vector geometry
- no raster textures, filters or shadows
- central symbol stays inside badge

Important V4 corrections:
- HORSES side profile
- BISON face revision
- URANIUM trefoil
- MAIZE visible kernels
- TEA recognizable leaves
- PERFUME bottle, Korean label 향수
- COCOA shown as chocolate
- CRAB legs corrected
- FURS inner pattern
- GOLD/SILVER bar forms
- MARBLE bust/statue direction
- SILK fabric direction
- SPICES/SUGAR/TRUFFLES redesign
- WHALES profile redesign

The five sprite files collectively contain all 47 resources exactly once.

## 9. Contact-based dynamic resource system

Core design file:
`civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`

47-resource transfer-class table:
`civ_map_stage10_resources/resource_transfer_classes_v1.csv`

Core principle:
Historical introduction dates are historical/default-path priors, not global hard locks.

The game must distinguish:
1. native/source presence
2. civilization knowledge
3. introduced presence
4. exploitable/active state

Transfer events can include:
- civilization contact
- trade
- exploration/discovery
- settlement/colonization
- conquest/occupation

Locked alternate-history example:
If Korea reaches South America in 1000 CE and establishes a settlement, transferable resources already known and carried by Korea, such as horses or cattle, may be introduced to environmentally suitable cells. The game must not wait for the historical year 1492.

Geological resources do not move with contact:
- contact can reveal them,
- knowledge can spread,
- extraction technology can activate them,
- deposit geography remains fixed.

## 10. Resource transfer classes

Current broad classes:

A. Geological fixed resources  
Examples: IRON, COAL, OIL, ALUMINUM, URANIUM, COPPER, GOLD, SILVER, MARBLE, SALT, GEMS, JADE, LAPIS_LAZULI, AMBER, STONE

B. Transferable domesticated plants  
Examples: WHEAT, RICE, MAIZE, BANANAS, CITRUS, COTTON, SUGAR, COFFEE, TEA, TOBACCO, OLIVES, WINE/grape basis, transportable SPICES components

C. Transferable domesticated animals  
HORSES, CATTLE, SHEEP

D. Wild biological resources  
BISON, DEER, FURS, IVORY, FISH, CRAB, PEARLS, WHALES, CORAL, TRUFFLES

E. Processed/composite display resources  
COCOA/Chocolate, PERFUME/향수, plus other resources that need ingredient-specific interpretation such as DYES or INCENSE

F. Technology-sensitive natural/manufactured resource  
NITER

## 11. GitHub inventory

### Root handoff/status

- `CIV_GAME_MAP_RESOURCE_STAGE10_STATUS_2026-09-20.md`
- `CIV_GAME_MAP_STAGE10_GITHUB_HANDOFF_2026-09-20.md`
- `CIV_GAME_MAP_STAGE10_INTEGRATED_HANDOFF_2026-09-20.md`
- `CIV_GAME_MAP_STAGE10_CURRENT_HANDOFF_2026-09-20.md` (this file)

### Stage10 audit

Directory:
`civ_map_stage10_resources/audit_2026-09-20/`

Files:
- `RESOURCE_AUDIT_SUMMARY.md`
- `RESOURCE_FIX_PLAN_V1.md`
- `heuristic_fix_smoke_test_v1.csv`
- `korea_land_resource_audit.csv`
- `problem_resource_summary_v1.csv`
- `resource_audit_status.csv`
- `resource_fix_plan_v1.csv`
- `resource_tie_plateau_audit.csv`
- `world_land_resource_density_by_region.csv`
- `world_resource_surface_summary.csv`
- `world_resource_technical_audit.csv`
- `world_resource_technical_checks.json`

### resource_fix_v1

Directory:
`civ_map_stage10_resources/resource_fix_v1/`

Files:
- `CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`
- `replacement_selections_v1.csv`
- `replacement_comparison_summary_v1.csv`
- `replacement_pool_counts_v1.csv`
- `replacement_region_comparison_v1.csv`
- `plateau_comparison_v1.csv`
- `replacement_ids_v1.json`
- `RECONSTRUCT_FIXED_PLACEMENT.md`
- `README.md`

### Icon V4

Directory:
`civ_map_stage10_resources/icons_v4/`

Files:
- `README.md`
- `resource_manifest_v4.csv`
- `resource_icons_v4_sprite_1.svg`
- `resource_icons_v4_sprite_2.svg`
- `resource_icons_v4_sprite_3.svg`
- `resource_icons_v4_sprite_4.svg`
- `resource_icons_v4_sprite_5.svg`

### Dynamic resource system

- `civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`
- `civ_map_stage10_resources/resource_transfer_classes_v1.csv`

## 12. Current progress

Completed:
- 47-resource roster locked
- current real-world evidence layers assembled
- Stage10X evidence audit completed
- Stage10Y 12,500-cell preview completed
- one-resource-per-hex check completed
- source-GPKG surface and Korea audit completed
- BISON/IVORY/WHALES plateau diagnosis completed
- resource_fix_v1 integrated 12,500-row review table committed
- Resource Icon V4 committed
- contact-based dynamic resource-system baseline committed
- 47-resource transfer-class table committed

Not yet complete:
- resource-by-resource historical/native/contact-transfer research for all 47 resources
- resource-specific environmental establishment rules for transferable biological resources
- default historical path validation
- final re-audit of resource_fix_v1 under the dynamic model
- direct GPKG-coordinate world/regional rendering
- final regional visual QA
- canonical final Stage10 placement

## 13. Next work

Highest priority:
Build the 47-resource historical/contact dataset.

For each resource record:
- native/source geography
- domestication or original exploitation zone
- wild vs domesticated distinction
- environmental suitability
- historical/default transfer paths
- transportability
- knowledge-transfer behavior
- trade transfer
- settlement transfer
- conquest transfer
- expedition/discovery behavior
- establishment conditions
- extraction/cultivation technology
- historical validation points

Do not implement a simple fixed-year unlock table.

Minimum gameplay rule:
`known by source civilization + transferable class + valid contact/trade/settlement/conquest/expedition event + suitable destination -> introduction queue -> local activation/spread`

## 14. Canonical warning

Current state:
- Stage10Y V2 original = preview
- resource_fix_v1 integrated placement = review build
- canonical final placement = not yet established

Do not promote to canonical until:
1. all 47 resource contact/native/transfer records are researched,
2. fixed BISON/IVORY/WHALES selection is re-audited,
3. one-resource-per-hex and surface rules are rechecked,
4. direct source-GPKG rendering is used,
5. regional visual QA passes.

This branch is the authoritative handoff location for continuing work.
