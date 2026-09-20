# CIV GAME MAP STAGE 10 - GITHUB HANDOFF

Date: 2026-09-20
Repository: `physical-geogrpahy-forever/academic_food_chain`
Branch: `civ-game-map-stage1b-etopo2022`

## 1. Current locked map/resource baseline

- Parent grid: 335 x 781 = 261,635 hexes
- CRS: EPSG:8857
- LAND: 68,048
- LAKE: 882
- COAST: 8,781
- OCEAN: 156,201
- VOID: 27,723
- Resource roster: 47 total
  - Strategic: 7
  - Bonus: 10
  - Luxury: 30
- Stage 10Y preview target: 12,500 selected resource hexes
  - Strategic 2,500
  - Bonus 5,000
  - Luxury 5,000
- One resource type per hex remains locked.
- Regional density differences are not to be normalized away merely for balance.

## 2. Resource placement audit performed in this chat

The rendered world/regional maps were found unreliable for positional QA because the image-coordinate overlay was not aligned reliably with the source GPKG.

The audit was therefore repeated directly from the source Stage10Y GPKG.

Technical findings:
- selected resource cells: 12,500
- unique selected cell IDs: 12,500
- duplicate selected cells: 0
- LAND resource cells: 10,896
- COAST resource cells: 639
- OCEAN resource cells: 965
- LAKE/VOID resource cells: 0
- no basic surface-rule violations were found

Korea land audit:
- tight window used for audit: 124-131E, 33-39.8N
- resource-bearing LAND cells in the audit window: 28
- resources included RICE, HORSES, TOBACCO, WINE, CITRUS, COAL, IRON, CATTLE, JADE, MAIZE

Important conclusion:
- The apparent lack of Korean land resources in the earlier rendered TIF/PNG was a rendering/alignment failure, not evidence that the source placement table was empty.
- Earlier composite TIF regional crops should not be used for positional validation.

## 3. Three resources requiring placement repair

The source-strength audit found severe top-score plateaus for:
- BISON
- IVORY
- WHALES

Original plateau diagnostics:
- BISON: 10,738 top-tie candidates for 390 selected
- IVORY: 15,552 top-tie candidates for 248 selected
- WHALES: 3,695 top-tie candidates for 350 selected

Additional anomalies:
- BISON had 21 desert-biome selections
- IVORY had 44 desert-biome selections and 8 temperate-biome selections
- WHALES was overwhelmingly southern-hemisphere biased

## 4. resource_fix_v1

A replacement placement set was produced for BISON, IVORY, and WHALES while retaining the other Stage10Y selections.

Main changes:
- BISON
  - desert-biome selections reduced to 0
  - quota pools used for North America, Europe, Central/South Asia, East Asia
- IVORY
  - desert-biome selections reduced to 0
  - temperate-biome selections reduced to 0
  - Africa and South/Southeast Asia pools used
- WHALES
  - north/south distribution rebalanced
  - tropical/subtropical pool restored
  - temperate/subpolar and high-latitude pools separated

The replacement is still a review build and is not yet the canonical final resource map.

## 5. Resource icon V4

The lightweight procedural SVG icon system is now at V4.

Locked UI rules:
- Strategic badge: hexagon
- Bonus badge: circle
- Luxury badge: rounded diamond
- SVG vector only
- no raster texture/shadow/filter dependency
- central symbol must remain inside the badge

V4 corrections include:
- horse redrawn in side-profile direction
- bison face revised
- uranium trefoil corrected
- maize kernels added
- tea redrawn as recognizable leaves
- perfume label/icon changed to perfume bottle
- cocoa display changed to chocolate icon
- crab legs corrected
- fur pattern added
- gold and silver redrawn as bars
- marble changed toward statue/bust representation
- silk redrawn as fabric
- spices, sugar, truffles redrawn
- whale redrawn toward a recognizable whale profile

## 6. Contact-based dynamic resource system

Historical introduction dates are default historical priors, not absolute global locks.

Alternate-history transfer must be possible through:
- civilization contact
- trade
- exploration/discovery
- settlement/colonization
- conquest/occupation

Locked example:
- If Korea reaches South America in 1000 CE and establishes a settlement, resources already known and carried by Korea, such as horses or cattle, may be introduced there if the destination is suitable.
- The system must not wait for 1492 merely because that was the historical path.

State separation:
- native presence
- civilization knowledge
- introduced presence
- exploitable/active state

Detailed design:
`civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`

## 7. GitHub file inventory synced in this update

### Resource audit
`civ_map_stage10_resources/audit_2026-09-20/`

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

### Resource fix
`civ_map_stage10_resources/resource_fix_v1/`

- `README.md`
- `plateau_comparison_v1.csv`
- `replacement_comparison_summary_v1.csv`
- `replacement_pool_counts_v1.csv`
- `replacement_region_comparison_v1.csv`
- `RECONSTRUCT_FIXED_PLACEMENT.md`
- `replacement_ids_v1.json`
- `replacement_selections_v1.csv`
- `CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv` — full 12,500-row integrated review-build table

The repository stores both the compact reproducible patch and the **full integrated 12,500-row fixed placement table**. The authoritative review-build table is `civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`. The compact `replacement_ids_v1.json` and reconstruction instructions are retained only as reproducibility aids, not as substitutes for the integrated table.

### Icons
`civ_map_stage10_resources/icons_v4/`

- `README.md`
- `resource_manifest_v4.csv`
- `resource_icons_v4_sprite_1.svg`
- `resource_icons_v4_sprite_2.svg`
- `resource_icons_v4_sprite_3.svg`
- `resource_icons_v4_sprite_4.svg`
- `resource_icons_v4_sprite_5.svg`

The five sprite sheets contain all 47 V4 resource symbols exactly once.

### Dynamic resource system

- `civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`
- `civ_map_stage10_resources/resource_transfer_classes_v1.csv`

The transfer-class table covers all 47 resources and separates geological fixed resources, transferable domesticated plants, transferable domesticated animals, wild biological resources, processed/composite display resources, and technology-sensitive niter.

## 8. Immediate next work

1. Research all 47 resources for native/source geography, domestication or original exploitation zone, historical transfer pathways, and resource-specific transferability.
2. Treat historical dates as validation/default-path priors, not global hard locks.
3. Implement contact-driven transfer events:
   - civilization contact
   - trade
   - exploration/discovery
   - settlement/colonization
   - conquest/occupation
4. Add environmental-suitability checks before introduced biological resources can establish.
5. Keep geological resources spatially fixed while letting knowledge and extraction technology spread.
6. Reconstruct and re-audit the Stage10Y fixed placement after the dynamic-resource data model is ready.
7. Only then rebuild regional/world maps directly from source GPKG geometry. Do not return to the old image-coordinate overlay.

## 9. Canonical status warning

Stage10Y remains a preview/review placement.

Do not promote it to canonical final until:
- the repaired BISON/IVORY/WHALES placement passes final review,
- direct-coordinate map rendering is fixed,
- the contact-based transfer model has resource-specific data for all transferable resources,
- the default historical path can be reconstructed without preventing alternate-history contacts.


## 10. GitHub inventory verification

Verified directly against branch `civ-game-map-stage1b-etopo2022` on 2026-09-20.

Confirmed present:
- `CIV_GAME_MAP_STAGE10_INTEGRATED_HANDOFF_2026-09-20.md`
- full integrated 12,500-row fixed placement CSV
- full BISON/IVORY/WHALES replacement selection CSV
- Stage10 status MD
- this handoff MD
- source-GPKG audit tables
- Korea LAND-only audit
- BISON/IVORY/WHALES plateau diagnostics and repair plan
- `resource_fix_v1` compact patch and reconstruction instructions
- Resource icon V4 manifests and five SVG sprite files
- contact-based dynamic resource system design

Latest inventory correction commit before this handoff update:
- `0e2d1a41580a9dfe0bb57c01414fd3de56298af0`
- message: `Fix resource_fix_v1 inventory documentation`

The branch must be treated as the authoritative handoff location for the next chat.


## 11. Integrated full-table sync correction

User decision: the GitHub handoff must include the actual integrated placement table, not only a compact patch.

Now committed on this branch:
- `civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`
  - 12,500 selected rows plus header
  - commit: `1a822065b259f5f169ad40ba487aa7c3b805f7e4`
- `civ_map_stage10_resources/resource_fix_v1/replacement_selections_v1.csv`
  - complete 988-row BISON/IVORY/WHALES replacement set plus header
  - commit: `68f476b89697142c5262611dafd19378415c77c3`
- `CIV_GAME_MAP_STAGE10_INTEGRATED_HANDOFF_2026-09-20.md`
  - unified current-state handoff
  - commit: `700c1fbf127e0c6284749ed5b14c6a02a91d6d7e`

The integrated CSV is the primary handoff artifact for the current resource_fix_v1 review build. Compact patches remain secondary reproducibility tools.
