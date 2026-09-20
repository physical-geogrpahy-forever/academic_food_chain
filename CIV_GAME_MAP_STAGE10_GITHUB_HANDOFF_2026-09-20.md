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

## 7. GitHub file inventory added in this update

### Resource audit
`civ_map_stage10_resources/audit_2026-09-20/`

- `RESOURCE_AUDIT_SUMMARY.md`
- `RESOURCE_FIX_PLAN_V1.md`
- `heuristic_fix_smoke_test_v1.csv`
- `problem_resource_summary_v1.csv`
- `resource_audit_status.csv`
- `resource_fix_plan_v1.csv`
- `resource_tie_plateau_audit.csv`
- `world_resource_technical_audit.csv`
- `world_resource_technical_checks.json`
- `korea_land_resource_audit.csv`

### Resource fix
`civ_map_stage10_resources/resource_fix_v1/`

- `README.md`
- `replacement_comparison_summary_v1.csv`
- `replacement_pool_counts_v1.csv`
- `replacement_region_comparison_v1.csv`
- `plateau_comparison_v1.csv`
- package archive with the full fixed placement CSV and replacement selections

### Icons
`civ_map_stage10_resources/icons_v4/`

- `README.md`
- `resource_manifest_v4.csv`
- `resource_manifest_v4.json`
- `resource_atlas_v4.svg`
- V4 package ZIP containing the individual SVG icons

### Dynamic resource system
- `civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`

## 8. Immediate next work

1. Verify the new BISON/IVORY/WHALES placement against source evidence and broad geography.
2. Replace the three old selections in the Stage10Y review board.
3. Re-run the one-resource-per-hex and surface audits.
4. Build regional maps directly from source GPKG/placement coordinates rather than cropping a misaligned whole-world raster.
5. Build the first data table for contact-based transfer classes across all 47 resources.
6. Research native/source areas and historical transfer pathways for crops/livestock so the default historical path can be reconstructed without blocking alternate-history contact.

## 9. Canonical status warning

Stage10Y remains a preview/review placement.
Do not promote it to canonical final until:
- the three repaired biological resources pass review,
- direct-coordinate map rendering is fixed,
- the contact-based transfer model is integrated for movable resources.
