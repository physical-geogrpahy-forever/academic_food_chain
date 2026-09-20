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

## 9. Contact-based dynamic resource system — reviewed V2

Canonical current design:
`civ_map_stage10_resources/contact_dynamic_resource_system_v2.md`

Transfer-class table:
`civ_map_stage10_resources/resource_transfer_classes_v2.csv`

The old V1 design is superseded and is explicitly marked DO NOT IMPLEMENT.

V2 intentionally removes the earlier probability, city-stock, regional-stock, diffusion and neighbor-spread machinery.

Minimal state:
- map cell: START_VISIBLE / LATENT, plus optional ACTIVE_INTRODUCED after gameplay introduction
- civilization: `has_resource[civ][resource]`

Visibility on an explored tile:
1. START_VISIBLE -> visible to everyone
2. ACTIVE_INTRODUCED -> visible to everyone
3. LATENT + civilization possesses resource -> visible to that civilization
4. otherwise hidden

Fog of war remains unchanged.

Acquisition routes:
- explore a START_VISIBLE source: icon becomes visible, but possession is not granted yet
- settle/claim a START_VISIBLE source region: civilization acquires resource
- trade with a civilization that possesses the resource: acquire resource
- capture a city from a civilization that possesses the resource: valid V2 acquisition route
- first contact alone: no automatic transfer

Once acquired, possession persists in V2.

Settlement never creates an arbitrary new resource cell. It can only activate already-selected Stage10 LATENT cells inside the settlement/city territory as ACTIVE_INTRODUCED.

Locked example:
- American HORSES cells start LATENT
- Spain with HORSES can see its explored American HORSES latent cells
- horse cells introduced within a Spanish colony can become ACTIVE_INTRODUCED and are then physically visible to other explorers
- a Native civilization capturing the Spanish colony acquires HORSES
- that Native civilization can then see its explored American HORSES latent cells and can transfer HORSES onward through trade

## 10. Reviewed dynamic resource set

V2 dynamic-transfer resources, 18 total:

Plants/composite plant resources:
- BANANAS
- CITRUS
- COCOA
- COFFEE
- COTTON
- DYES
- MAIZE
- OLIVES
- RICE
- SPICES
- SUGAR
- TEA
- TOBACCO
- WHEAT
- WINE

Domestic animals:
- HORSES
- CATTLE
- SHEEP

Important locks:
- DYES stays one unified resource.
- SPICES stays one unified resource.
- COCOA internal ID remains COCOA even though the icon/display may be chocolate.
- PERFUME is explicitly excluded from dynamic transfer.
- SILK and INCENSE are not in the reviewed 18-resource V2 dynamic set and remain deferred.
- wild biological resources are not moved by this system.
- geological/mineral resources remain fixed.

Special fixed-production exceptions:
- NITER natural cells remain fixed; separate technology/facility may manufacture saltpetre.
- SALT natural cells remain fixed; coastal salt production uses a separate tile improvement/facility such as SALTWORKS, not a city building.

## 11. 4000 BCE historical start mask — reviewed V3

Canonical current directory:
`civ_map_stage10_resources/history_4000bce_v3/`

Files:
- `README.md`
- `resource_start_visible_4000bce_mask_regions_v3.csv`
- `apply_resource_history_4000bce_v3.py`
- `resource_history_4000bce_exact_summary_v3.csv`
- `resource_history_4000bce_critical_checks_v3.csv`

The old `history_4000bce_v1` README is marked superseded.

Design principle:
- use about 4000 BCE as the single initial-history baseline
- intentionally use broad source/early-spread envelopes for gameplay
- only classify already-selected Stage10 cells; never create new resource locations
- direct wild source populations that could plausibly be discovered and exploited are allowed as START_VISIBLE
- modern distributions that did not yet physically exist are LATENT

## 12. Exact Stage10Y V3 mask result

The V3 mask was applied to the exact Stage10Y 12,500-cell placement artifact.

Dynamic-resource cells:
- total: 6,630
- START_VISIBLE: 1,950 (29.4%)
- LATENT: 4,680 (70.6%)

Per-resource result:

| Resource | START_VISIBLE | LATENT | Total | Visible % |
|---|---:|---:|---:|---:|
| BANANAS | 48 | 373 | 421 | 11.4 |
| CATTLE | 155 | 466 | 621 | 25.0 |
| CITRUS | 17 | 249 | 266 | 6.4 |
| COCOA | 24 | 146 | 170 | 14.1 |
| COFFEE | 8 | 192 | 200 | 4.0 |
| COTTON | 40 | 195 | 235 | 17.0 |
| DYES | 71 | 12 | 83 | 85.5 |
| HORSES | 293 | 830 | 1,123 | 26.1 |
| MAIZE | 22 | 491 | 513 | 4.3 |
| OLIVES | 152 | 79 | 231 | 65.8 |
| RICE | 62 | 387 | 449 | 13.8 |
| SHEEP | 357 | 256 | 613 | 58.2 |
| SPICES | 215 | 97 | 312 | 68.9 |
| SUGAR | 39 | 191 | 230 | 17.0 |
| TEA | 45 | 111 | 156 | 28.8 |
| TOBACCO | 34 | 199 | 233 | 14.6 |
| WHEAT | 195 | 287 | 482 | 40.5 |
| WINE | 173 | 119 | 292 | 59.2 |

Critical QA:
- Americas HORSES: 472 checked, 0 START_VISIBLE — PASS
- Americas CATTLE: 267 checked, 0 START_VISIBLE — PASS
- Americas SHEEP: 32 checked, 0 START_VISIBLE — PASS
- Korea RICE: 7 checked, 0 START_VISIBLE — PASS
- Mesoamerica MAIZE: 23 checked, 22 START_VISIBLE — PASS
- Upper Amazon COCOA: 24 checked, 24 START_VISIBLE — PASS
- Ethiopia/Boma COFFEE: 8 checked, 8 START_VISIBLE — PASS
- China RICE: 62 checked, 62 START_VISIBLE — PASS

Korea dynamic-resource cells under V3:
- CATTLE 1: LATENT
- CITRUS 2: LATENT
- HORSES 6: LATENT
- MAIZE 1: LATENT
- RICE 7: LATENT
- TOBACCO 4: LATENT
- WINE 4: LATENT

Thus the current Korea window has no START_VISIBLE cells among the reviewed 18 dynamic resources at 4000 BCE. This is not equivalent to Korea having no map resources overall; static minerals/wild resources are separate.

## 13. SUGAR V3 correction

A New-Guinea-only source mask produced zero START_VISIBLE SUGAR cells because the current Stage10 SUGAR placement contains no selected modern cells in New Guinea itself.

V3 therefore uses a broad game envelope:
- New Guinea origin
- Island Southeast Asia / Southeast Asian early Saccharum source-dispersal zone
- longitude 95–130E
- latitude 10S–20N

The 20N cap keeps South China LATENT.

Final V3 result:
- SUGAR START_VISIBLE 39
- SUGAR LATENT 191

## 14. GitHub inventory additions

### Current dynamic system
- `civ_map_stage10_resources/contact_dynamic_resource_system_v2.md`
- `civ_map_stage10_resources/resource_transfer_classes_v2.csv`

### 4000 BCE V3
Directory:
`civ_map_stage10_resources/history_4000bce_v3/`

Files:
- `README.md`
- `resource_start_visible_4000bce_mask_regions_v3.csv`
- `apply_resource_history_4000bce_v3.py`
- `resource_history_4000bce_exact_summary_v3.csv`
- `resource_history_4000bce_critical_checks_v3.csv`

Legacy files retained only for provenance:
- `contact_dynamic_resource_system_v1.md` — superseded warning added
- `history_4000bce_v1/README.md` — superseded warning added
- `resource_transfer_classes_v1.csv` — legacy; use V2

## 15. Current progress

Completed:
- 47-resource roster locked
- Stage10X evidence layers assembled
- Stage10Y exact 12,500-cell preview completed
- one-resource-per-hex audit completed
- source-GPKG/Korea audit completed
- BISON/IVORY/WHALES plateau diagnosis and resource_fix_v1 review build completed
- Resource Icon V4 committed
- simple contact-based dynamic system V2 reviewed and committed
- 18-resource dynamic set reviewed and committed
- 4000 BCE broad historical mask V3 reviewed and committed
- V3 applied to exact Stage10Y 12,500-cell artifact
- exact per-resource summary and critical QA committed

Still not canonical final placement:
- `resource_fix_v1` remains a review build
- direct source-GPKG regional visual QA of final combined historical display remains desirable
- final canonical Stage10 placement has not yet been promoted

## 16. Next work

Highest priority:
1. implement V2 runtime visibility/acquisition events in the actual game layer
2. generate direct-GPKG maps showing START_VISIBLE versus LATENT for regional visual QA
3. test alternate-history cases:
   - Spain -> American colony -> Native conquest -> Native trade
   - Yangtze RICE -> intermediary trade -> Korea
   - source civilization destroyed but source tile remains discoverable
4. re-audit resource_fix_v1 with the V3 historical display layer
5. only then decide whether to promote the integrated Stage10 placement to canonical final

Do not reintroduce the V1 probability/diffusion/stock model unless explicitly requested.

## 17. Canonical warning

Current authoritative design baseline:
- dynamic transfer: V2
- historical start mask: 4000 BCE V3
- Stage10 placement: resource_fix_v1 review build, not yet canonical final

The current branch remains the authoritative handoff location for continuing work.


## Civic system milestone — 2026-09-20

Civic design now has a locked 72-node roster and prerequisite DAG.

Authoritative files:
- `civics_reference/CIVIC_ROSTER_LOCKED_V1.md`
- `civics_reference/civic_roster_locked_v1.csv`
- `civics_reference/CIVIC_TREE_LOCKED_V1.md`
- `civics_reference/civic_tree_locked_v1.csv`
- `civics_reference/validate_civic_tree_v1.py`

QA baseline:
- 72/72 civics reachable from Code of Laws
- one root only: Code of Laws
- zero missing prerequisite references
- zero cycles
- zero backward-era prerequisite edges
- zero isolated civics
- maximum two direct prerequisites
- Future-like civics remain randomized through a fixed acyclic A-E template inspired by Gathering Storm

New civics beyond the imported Civ VI roster:
Written Culture; Court Culture; Scholasticism; Patronage; Print Culture; Scientific Revolution; Sovereignty; Constitutionalism; Public Sphere; Romanticism; Labor Movement.

Next civic task:
governments/policy cards/Inspirations/unlocks/culture costs. Do not add more civic nodes without a concrete implementation gap.


## Civic historical-flow revision V2 — 2026-09-20

The 72-node civic roster remains locked, but the old Civ-VI-heavy prerequisite graph is superseded for social-to-social prerequisite design by:

- `civics_reference/CIVIC_TREE_HISTORICAL_V2.md`
- `civics_reference/civic_tree_historical_v2.csv`
- `civics_reference/validate_civic_tree_historical_v2.py`

Purpose:
- remove historically implausible social causation while keeping the Civ VI-based roster;
- reserve material/technical necessities for later technology cross-gates.

QA:
- 72/72 reachable from Code of Laws
- one root
- zero missing references
- zero cycles
- zero backward-era edges
- maximum two direct social prerequisites

Important removed hard links include:
- Theology -> Written Culture
- Feudalism -> Court Culture
- Reformed Church -> Sovereignty
- Exploration -> Scientific Revolution
- Mass Media -> Capitalism
- Ideology -> Professional Sports
- Rapid Deployment -> Environmentalism
- Space Race -> Social Media

Next step after review:
classify every civic as social-only, hard-tech-gated, or tech-boosted.


## Civic historical-flow V3 — full audit

Historical V3 supersedes V2 for social-to-social prerequisite design.

Authoritative social-flow files:
- `civics_reference/CIVIC_TREE_HISTORICAL_V3.md`
- `civics_reference/civic_tree_historical_v3.csv`
- `civics_reference/validate_civic_tree_historical_v3.py`

V3 removes remaining game-shaped causal links including:
- Games and Recreation -> Military Training
- Drama and Poetry -> Recorded History
- Mercenaries -> Exploration
- Scorched Earth -> Mobilization
- Mobilization -> Ideology
- Ideology -> Nuclear Program
- Labor Movement -> Suffrage as a mandatory link
- Professional Sports -> Social Media
- Cultural Heritage -> Environmentalism as a mandatory link

QA:
- 72 nodes
- 72 reachable from Code of Laws
- one root
- zero cycles
- zero missing references
- zero backward-era edges
- max 2 direct social prerequisites

Next: technology cross-gate classification.


## Civic–technology crosslinks V1

Added provisional direct technology relations for all 72 civics.

Authoritative crosslink files:
- `civics_reference/CIVIC_TECH_CROSSLINKS_V1.md`
- `civics_reference/civic_tech_crosslinks_v1.csv`
- `civics_reference/validate_civic_tech_crosslinks_v1.py`

Classification:
- HARD: 11
- BOOST: 31
- NONE: 30

Principle:
- HARD only for near-material impossibility;
- BOOST for enabling/accelerating technologies;
- inherited hard gates are calculated through the social prerequisite DAG and not redundantly repeated.

Exact technology names remain provisional until the science tree is locked.


## Technology roster locked V1

Technology roster is now locked at **103 nodes**, sourced from:
- Civ VI Gathering Storm: 77
- non-duplicating Civ V BNW additions: 21
- technical Pouakai Enlightenment Era additions: 5

Authoritative files:
- `tech_reference/TECHNOLOGY_ROSTER_LOCKED_V1.md`
- `tech_reference/technology_roster_locked_v1.csv`
- `tech_reference/technology_merge_exclusions_v1.csv`

Era counts:
- Ancient: 14
- Classical: 9
- Late Antiquity: 2
- Early Medieval: 2
- High Medieval: 6
- Renaissance: 5
- Exploration: 9
- Enlightenment: 6
- Industrial: 16
- Modern: 12
- Atomic: 13
- Information: 9

Civ/social duplicates such as Theology, Civil Service, Mass Media, Globalization, Sovereignty, Humanism, Natural History and Romanticism are excluded from the science tree.

Next:
build and validate the 103-node technology prerequisite DAG, then reconcile civic HARD/BOOST technology crosslinks.


## Technology prerequisite DAG V1

The locked 103-technology roster now has a historical/technical prerequisite DAG.

Authoritative files:
- `tech_reference/TECHNOLOGY_TREE_HISTORICAL_V1.md`
- `tech_reference/technology_tree_historical_v1.csv`
- `tech_reference/validate_technology_tree_historical_v1.py`

QA:
- 103 technologies
- roots: Agriculture, Pottery, Animal Husbandry, Mining, Sailing, Archery
- 103/103 reachable from a root
- zero missing prerequisite references
- zero cycles
- zero backward-era prerequisite edges
- maximum 2 direct prerequisites

Next:
reconcile civic HARD/BOOST crosslinks against this exact technology tree.


## Civic-tech reconciliation V2

Civic-tech crosslinks were validated against the locked 103-node technology DAG.

Results:
- 72 civic crosslink rows checked
- HARD 11, BOOST 31, NONE 30
- zero unknown tech names
- zero hard/boost links to a later project era
- Mass Media boost corrected: Radio -> Telegraph
- Globalization social prerequisite corrected: Cold War + Capitalism -> Capitalism + Mass Media, avoiding unintended Nuclear Fission inheritance

Reference:
- `civics_reference/CIVIC_TECH_CROSSLINK_RECONCILIATION_V2.md`


## Technology roster/tree locked V2 — 109 nodes

The earlier 103-node technology baseline is superseded.

Authoritative technology files:
- `tech_reference/TECHNOLOGY_ROSTER_TREE_LOCKED_V2.md`
- `tech_reference/technology_roster_locked_v2.csv`
- `tech_reference/technology_tree_historical_v2.csv`
- `tech_reference/validate_technology_tree_historical_v2.py`

Final roster: **109 technologies**.

Historical additions:
Papermaking; Horse Collar; Alchemy; Block Printing; Algebra; Astrolabe.

Historical moves:
- Stirrups -> Late Antiquity
- Gunpowder -> Early Medieval
- Metallurgy -> Renaissance

QA:
- 109/109 reachable
- zero missing prerequisites
- zero cycles
- zero backward-era edges
- maximum two direct prerequisites

Civic crosslinks were revalidated against the 109-tech tree:
- zero missing referenced technologies
- zero later-era HARD/BOOST references
- reference: `civics_reference/CIVIC_TECH_CROSSLINK_RECONCILIATION_V3.md`


## Civ V-style city system and Great Directors

Locked design direction:
- city management follows Civ V rather than Civ VI district placement;
- normal buildings are constructed directly in cities;
- specialists remain a core city-management mechanic;
- Civ VI district unlocks must be translated into Civ V-style buildings/infrastructure.

Great Director system is included:
- Great Director
- Director specialist
- Director's Guild / film-production building line
- Cinema
- Great Works of Film with dedicated Film slots

Reference implementation:
JFD Great Works of Film; MoreTech integration.

World wonders such as Hollywood are NOT automatically imported and remain subject to separate wonder-quality audit.

Technology implication:
Cinematography is now a strong new technology candidate because the Great Director/Film mechanic creates a concrete technical prerequisite gap. Evaluate together with Photography before modifying the locked technology tree.

Reference:
- `city_system/CIV5_STYLE_CITY_AND_GREAT_DIRECTOR_BASELINE_V1.md`


## Corporation system baseline

Locked core direction:
- corporations are not Wonders;
- sectors are non-exclusive;
- named historical firms may be unique;
- both Great Merchants and Great Engineers may found corporations;
- Great Merchants favor commercial/service/consumer sectors;
- Great Engineers favor technical/industrial sectors;
- signature founders may create predetermined historical firms;
- outputs are split into Manufactured Luxuries, Functional Corporate Goods and Services;
- functional goods use quantity/supply rather than simple permanent empire-wide modifiers;
- services grant sector-specific effects, not universally Culture/Tourism.

Examples:
- Refined Petroleum Products -> Production/logistics
- Pharmaceuticals -> Growth/Health
- Finance -> Gold/investment
- Hotels/Film/Travel -> Culture/Tourism
- Telecommunications/Software -> Science/economic efficiency

Thomas Edison and Carl Benz are strong Great Engineer founder candidates.

Reference:
- `corporations/CORPORATION_FOUNDING_AND_OUTPUT_SYSTEM_V1.md`


## Corporate founder pool research V1

A broad founder research pool has been assembled across Great Merchants and Great Engineers.

Reference:
- `corporations/CORPORATE_FOUNDER_POOL_RESEARCH_V1.md`

Key design findings:
- functional goods use supplied quantities, not empire-wide permanent modifiers;
- services use branch/network coverage;
- Refined Petroleum Products -> Production/logistics;
- Finance -> Gold/investment;
- Hotels -> Tourism/Culture/Gold;
- Telecom -> Science/network efficiency;
- Logistics -> trade/branch reach;
- Automobiles and Consumer Electronics are hybrid manufactured-luxury + functional categories;
- multiple brands in the same product category do not stack full Amenity bonuses infinitely.

Founder pool now explicitly includes many Great Engineers as well as Great Merchants. Further pass should expand toward 80-100 audited candidates.
