# Resource Fix Plan V1

## Scope
This note covers the three resources that failed the Stage10Y technical audit because their top-score candidate plateaus are too large: **BISON, IVORY, WHALES**.

## Why these three fail
- **BISON**: 10,738 top-tie candidates for 390 selected cells. 21 current placements fall in desert biome.
- **IVORY**: 15,552 top-tie candidates for 248 selected cells. 44 current placements fall in desert biome and 8 in temperate biomes.
- **WHALES**: 3,695 top-tie candidates for 350 selected cells. Current output is 336 south vs 14 north, with no tropical placements.

## Recommended repair logic

### 1. BISON
**Hard filters**
- LAND only
- Absolute latitude 25 to 72
- Exclude tropical biomes and Deserts & Xeric Shrublands
- Keep only these main biomes:
  - Temperate Grasslands, Savannas & Shrublands
  - Boreal Forests/Taiga
  - Temperate Broadleaf & Mixed Forests
  - Temperate Conifer Forests
  - Tundra
  - Montane Grasslands & Shrublands

**Scoring**
- Base = `BISON_PHYLACINE_MEAN_RICHNESS`
- Multiply by biome weights
- Multiply by terrain weights: PLAINS > GRASSLAND > TUNDRA
- Multiply by feature weights: NONE > FOREST
- Multiply by a slope penalty so flatter cells outrank rugged cells

**Allocation**
- Start with **45% North America / 55% Eurasia**

### 2. IVORY
**Hard filters**
- LAND only
- Absolute latitude <= 35
- Exclude Deserts & Xeric Shrublands
- Exclude Temperate biomes and Mediterranean biomes
- Keep these main biomes:
  - Tropical & Subtropical Grasslands, Savannas & Shrublands
  - Tropical & Subtropical Moist Broadleaf Forests
  - Tropical & Subtropical Dry Broadleaf Forests
  - Flooded Grasslands & Savannas
- Secondary low-weight biome:
  - Tropical & Subtropical Coniferous Forests

**Scoring**
- Base = `IVORY_PHYLACINE_MEAN_RICHNESS`
- Savanna highest, moist forest second
- PLAINS and GRASSLAND preferred
- NONE and JUNGLE preferred over desert or temperate artifacts
- Add slope penalty

**Allocation**
- Start with **80% Africa / 20% South + Southeast Asia**

### 3. WHALES
**Hard filters**
- OCEAN or COAST only
- Main pool can require absolute latitude >= 15
- Optional tropical sub-pool reserved separately so the resource does not disappear from lower latitudes

**Scoring**
- Base = weighted combination of `WHALES_PHYLACINE_MEAN_RICHNESS` and `WHALES_PHYLACINE_MAX_RICHNESS`
- Multiply by a latitude preference peaking in temperate/subpolar waters
- Small coast bonus allowed
- If still too concentrated, add mild penalty for very high southern concentration

**Allocation**
Two workable options:
1. **Latitude-belt quotas**
   - 35% North temperate/subpolar
   - 45% South temperate/subpolar
   - 10% tropical
   - 10% high-latitude fringe
2. **Ocean-basin quotas**
   - Pacific 38%
   - Atlantic 27%
   - Indian 20%
   - Southern 10%
   - Arctic/North fringe 5%

## Implementation order
1. Rewrite the candidate filters for BISON, IVORY, WHALES
2. Recompute scores with the new weighted formulae
3. Re-run spacing and placement
4. Re-run the same audit tables
5. Only after the audit passes, rebuild regional/world maps
