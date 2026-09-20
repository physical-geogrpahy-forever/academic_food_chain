# CIV GAME MAP — RESOURCE STAGE 10 STATUS
Date: 2026-09-20
Branch: `civ-game-map-stage1b-etopo2022`

## 1. Locked resource roster

47 map resources total.

- Strategic 7: HORSES, IRON, NITER, COAL, OIL, ALUMINUM, URANIUM
- Bonus 10: BANANAS, BISON, CATTLE, DEER, FISH, SHEEP, STONE, WHEAT, MAIZE, RICE
- Luxury 30: CITRUS, COCOA, COPPER, COTTON, CRAB, DYES, FURS, GEMS, GOLD,
  INCENSE, IVORY, MARBLE, PEARLS, SALT, SILK, SILVER, SPICES, SUGAR,
  TRUFFLES, WHALES, WINE, COFFEE, TEA, TOBACCO, OLIVES, PERFUME,
  AMBER, JADE, LAPIS_LAZULI, CORAL

Design decisions:
- Nutmeg, cloves, pepper are merged into generic SPICES.
- Jewelry and porcelain are removed as processed goods.
- More Luxuries is adopted except Glass.
- Goldsmith/Jewelers/More Luxuries is not adopted.
- From Civ VI, NITER, MAIZE, RICE are added; other Civ VI-only additions are excluded.
- PERFUME means raw fragrance-material source regions, not finished perfume manufacturing.
- One final map hex may contain at most one resource type.

## 2. Canonical map inherited from earlier stages

- CRS EPSG:8857
- 335 x 781 = 261,635 parent hexes
- LAND 68,048
- LAKE 882
- COAST 8,781
- OCEAN 156,201
- VOID 27,723
- Stage1A 1-degree data remains forbidden in final products.

## 3. Strategic evidence

Current strategic candidate evidence:
- HORSES: 54,658 candidate hexes, GLW 2015 horse density
- IRON: 2,913, USGS MRDS
- NITER: 314, documented natural nitrate + historical saltpetre source regions
- COAL: 1,380, GEM Global Coal Mine Tracker public map 2026-08
- OIL: 2,152, GEM GOGET public map 2026-03 plus field-register fallback
- ALUMINUM: 1,031, MRDS bauxite/aluminium evidence
- URANIUM: 2,390, IAEA UThDEPO public-map payload, replacing MRDS as primary source

UThDEPO was captured from the public Blazor map WebSocket. The payload contains
deposit IDs, names, countries, Resource Range, Grade Range, latitude and longitude.

## 4. Strategic quantity policy

Strategic resources carry an integer quantity per selected hex.

Candidate ranges:
- HORSES 2–4
- IRON 2–6
- NITER 2–6
- COAL 2–7
- OIL 2–7
- ALUMINUM 3–8
- URANIUM 1–4

Physical magnitudes are NEVER compared between different strategic resource types.
Evidence is normalized within each resource only.

Important correction on 2026-09-20:
The first Stage 10Y preview selected the strongest strategic candidates first,
which unintentionally made HORSES all quantity 4 and URANIUM all quantity 4.
That preview is superseded.

The corrected Stage 10Y selector preserves the candidate quantity-stratum
proportions while thinning spatially. Current selected strategic distribution:

- HORSES 1,123 hexes:
  - qty 2: 374
  - qty 3: 374
  - qty 4: 375
  - total units 3,370
- IRON 296:
  - qty 2: 55
  - qty 3: 102
  - qty 4: 22
  - qty 5: 57
  - qty 6: 60
  - total units 1,149
- NITER 131:
  - qty 2: 19
  - qty 3: 34
  - qty 4: 26
  - qty 5: 26
  - qty 6: 26
  - total units 530
- COAL 219:
  - qty 2: 36
  - qty 3: 36
  - qty 4: 34
  - qty 5: 30
  - qty 6: 33
  - qty 7: 50
  - total units 1,014
- OIL 262:
  - qty 2: 21
  - qty 3: 69
  - qty 4: 43
  - qty 5: 43
  - qty 6: 43
  - qty 7: 43
  - total units 1,195
- ALUMINUM 196:
  - qty 3: 33
  - qty 4: 9
  - qty 5: 93
  - qty 7: 31
  - qty 8: 30
  - total units 1,057
- URANIUM 273:
  - qty 1: 67
  - qty 2: 71
  - qty 3: 62
  - qty 4: 73
  - total units 687

The absence of aluminum qty 6 is inherited from tied/discrete source evidence;
equal evidence was not arbitrarily split simply to force every integer bin.

## 5. Non-strategic evidence stages completed

Crop/livestock/mineral/marine evidence includes:
- MAPSPAM 2020: wheat, rice, maize, sugar, cotton, coffee, cocoa, tea, tobacco,
  bananas, citrus
- EarthStat/Monfreda: olives, wine/grape, generic spices
- GLW 2015: cattle, sheep
- PHYLACINE v1.2.1 Present_natural: bison, deer, ivory/elephants, furs,
  historically hunted large whales
- USGS MRDS: stone, copper, gold, silver, salt, marble, gems
- dedicated documented source regions: amber, jade, lapis lazuli
- UNEP-WCMC coral reef data: coral
- OBIS precision-4 occurrence grids: fish, crab, pearl oysters
- documented source regions: dyes, incense, silk, truffles, perfume raw materials

Latest documented evidence examples:
- CORAL evidence hexes: 3,476
- BISON: 11,885
- DEER: 41,109
- IVORY: 16,388
- FURS: 50,320
- FISH: 70,457
- CRAB: 18,561
- PEARLS: 1,638
- DYES: 709
- INCENSE: 657
- SILK: 575
- TRUFFLES: 556
- PERFUME: 968

## 6. Crop-branch correction

A downstream branch had inherited an older Stage 10N/O artifact, causing newer
MAPSPAM crop columns such as BANANAS_SPAM_HA to be absent downstream.

Stage 10X0 corrected this by merging the latest N/O crop evidence into the
latest downstream W board by canonical `id`.

Latest crop examples after correction:
- WHEAT 26,069 evidence hexes
- RICE 20,361
- MAIZE 32,093
- BANANAS 15,997

Stage 10X0 artifact:
- ID 10586057118
- name `CIV_GAME_MAP_STAGE10X0_CONSOLIDATED_EVIDENCE`

## 7. Stage 10X all-resource audit

Corrected Stage 10X run:
- run 35478885525
- artifact ID 10594977300
- artifact `CIV_GAME_MAP_STAGE10X_ALL_RESOURCE_STRENGTH`
- 47/47 resources have positive evidence
- class counts: strategic 7, bonus 10, luxury 30
- nonstrategic evidence strength = within-resource empirical percentile only
- tied top values use rank(method=max), so a tied top class reaches 1.0
- no final thinning at X
- no one-resource-per-hex enforcement at X

## 8. Stage 10Y placement PREVIEW

Current corrected run:
- run 35479205126
- artifact ID 10595363416
- artifact `CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW`

This is NOT canonical final placement yet.

Preview class targets:
- strategic: 2,500 hexes
- bonus: 5,000
- luxury: 5,000
- actual: exactly 2,500 / 5,000 / 5,000
- total selected: 12,500 hexes
- fraction of all parent hexes: 4.7776%
- one-resource-per-hex audit: PASS

Allocation:
- resource target within class is proportional to sqrt(positive evidence hex count)
- class-specific min/max caps prevent common resources from dominating
- no random numbers
- within class, scarcer resources are allocated before widespread resources
- conflict priority: strategic > luxury > bonus
- deterministic evidence ranking
- same-resource spatial spacing with controlled adaptive relaxation
- strategic resources preserve quantity strata during thinning

Examples of current targets:
- HORSES 1,123
- IRON 296
- NITER 131
- COAL 219
- OIL 262
- ALUMINUM 196
- URANIUM 273
- LAPIS_LAZULI 54
- AMBER 54
- JADE 65
- PEARLS 105
- CORAL 136
- FISH 667

The Stage 10Y class totals and min/max caps are explicit preview parameters in:
`civ_map_stage10_resources/resource_placement_preview_v1.yaml`

They must be reviewed for gameplay density before promotion to canonical final.

## 9. Immediate next work

1. Visual QA of corrected Stage 10Y distribution, especially:
   - strategic resource geography and quantity mixtures
   - resource density in Europe, India, eastern China, eastern North America
   - sparse regions such as central Australia, Sahara, Amazon interior and high latitudes
   - maritime-resource density around island arcs and southern oceans
2. Compare preview resource density against Civ V placement philosophy:
   - frequency by eligible plots
   - same-resource impact radius
   - major/minor strategic deposits
   - sparse/abundant multipliers
3. Adjust preview class totals/spacing only if QA shows over- or under-density.
4. Do NOT call Stage 10Y canonical final until density and distribution are visually approved.


## 10. Density QA policy locked 2026-09-20

User decision:
- Regional resource over-density or under-density is NOT a balancing defect by itself.
- Geographic concentration and scarcity are intended consequences of real-world spatial evidence.
- Do not smooth, equalize, normalize, or compensate resource density by world region.
- Density QA should check only overall/class/surface density and technical artifacts.
- Regional inspection is allowed only for detecting clear data/processing errors, not for enforcing geographic balance.

Stage 10Y V2 density:
- all selected resource hexes: 12,500
- LAND: 10,896 / 68,048 = 16.012%
- COAST: 639 / 8,781 = 7.277%
- OCEAN: 965 / 156,201 = 0.618%
- LAND+COAST: 11,535 / 76,829 = 15.014%
- all playable non-VOID surfaces including lakes: 12,500 / 233,912 = 5.344%
- LAND class density:
  - strategic 2,416 / 68,048 = 3.550%
  - bonus 4,333 / 68,048 = 6.368%
  - luxury 4,147 / 68,048 = 6.094%
- 83.988% of LAND hexes remain resource-free.

No regional-density correction should be applied unless a technical source/processing error is demonstrated.


## 11. Source-GPKG resource audit and rendering correction

The earlier whole-world/resource TIFF and regional crops are not reliable for positional QA because the resource overlay was aligned through an image-coordinate transformation rather than rendered directly from the source GPKG geometry.

The Stage10Y GPKG was therefore audited directly.

Global technical checks:
- selected cells: 12,500
- unique selected cell IDs: 12,500
- duplicate selected cells: 0
- LAND resource cells: 10,896
- COAST: 639
- OCEAN: 965
- LAKE/VOID resource cells: 0
- all selected surface rules: PASS
- no selected zero/negative strength or evidence values

Korea LAND-only audit:
- audit window: 124-131E, 33-39.8N
- resource-bearing LAND cells: 28
- resource counts: RICE 7, HORSES 6, TOBACCO 4, WINE 4, CITRUS 2, COAL 1, IRON 1, CATTLE 1, JADE 1, MAIZE 1

Therefore the apparent lack of Korean land resources in the earlier rendered image was a rendering/alignment failure, not an empty source placement table.

## 12. Biological-resource plateau audit

Three resources require placement repair because the top-score candidate plateau is too large:

- BISON: 10,738 top-tie candidates / 390 selected
- IVORY: 15,552 / 248
- WHALES: 3,695 / 350

Additional old-selection anomalies:
- BISON desert-biome selections: 21
- IVORY desert-biome selections: 44
- IVORY temperate-biome selections: 8
- WHALES south/north distribution: 336 / 14

## 13. resource_fix_v1 review build

A replacement selection was generated for BISON, IVORY and WHALES while keeping the remaining Stage10Y resource selections unchanged.

Before/after diagnostics:
- BISON desert-biome selections: 21 -> 0
- IVORY desert-biome selections: 44 -> 0
- IVORY temperate-biome selections: 8 -> 0
- WHALES south/north distribution: 336/14 -> 176/174
- WHALES tropical/subtropical selections: 11 -> 35

Quota-pool review build:
- BISON: North America 176, Europe 70, Central/South Asia 100, East Asia 44
- IVORY: Africa 198, South+Southeast Asia 50
- WHALES: North temperate/subpolar 123, South temperate/subpolar 158, North tropical/subtropical 17, South tropical/subtropical 18, high-latitude fringe 34

This is still a review build. It is not canonical final placement.

## 14. Resource icon V4

The current procedural vector icon package is V4.

Important V4 revisions:
- horse side-profile redesign
- bison face revision
- uranium trefoil correction
- visible maize kernels
- recognizable tea leaves
- perfume bottle and Korean display name 향수
- cocoa display changed to chocolate icon
- crab leg correction
- fur pattern
- gold/silver bar forms
- marble bust/statue direction
- silk fabric form
- spices/sugar/truffle redesign
- whale profile redesign

## 15. Contact-based dynamic resource system

Historical dates are no longer to be implemented as absolute global switches for transferable crops and livestock.

The game must distinguish:
- native presence
- civilization knowledge
- introduced presence
- active/exploitable state

Transfer can occur through:
- contact
- trade
- exploration/discovery
- settlement/colonization
- conquest/occupation

Locked alternate-history example:
If Korea reaches South America in 1000 CE and establishes a settlement, resources already known and transported by Korea, such as horses or cattle, can be introduced in environmentally suitable cells. The system must not wait for the historical 1492 contact date.

Detailed design:
`civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`

## 16. GitHub handoff

The current Stage10 file inventory and next-work checklist are maintained in:
`CIV_GAME_MAP_STAGE10_GITHUB_HANDOFF_2026-09-20.md`
