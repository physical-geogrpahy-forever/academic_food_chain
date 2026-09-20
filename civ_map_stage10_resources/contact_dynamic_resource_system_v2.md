# Contact-Based Dynamic Resource System V2 — simplified canonical design

Date: 2026-09-20  
Status: reviewed implementation baseline  
Supersedes: `contact_dynamic_resource_system_v1.md`

## 1. Design goal

Use the existing Stage10 modern resource cells without allowing impossible prehistoric discoveries.

The game must support alternate history:
- resources can move earlier than their historical dates if civilizations connect earlier;
- no global fixed-year switch such as "horses appear in the Americas in 1492";
- no arbitrary player placement of resources;
- no population stocks, city stocks, probabilistic diffusion, adjacency spread model, or multi-layer economic simulation in V2.

## 2. The 18 dynamic resources

BANANAS, CATTLE, CITRUS, COCOA, COFFEE, COTTON, DYES, HORSES, MAIZE,
OLIVES, RICE, SHEEP, SPICES, SUGAR, TEA, TOBACCO, WHEAT, WINE.

DYES and SPICES remain unified resources.

PERFUME is explicitly excluded from dynamic transfer.

## 3. Map-cell states

Every existing Stage10 cell of a dynamic resource has a historical base state:

### START_VISIBLE
The resource or a directly usable source population existed there by about 4000 BCE.

If a civilization has explored the tile, the icon is visible even if that civilization does not yet possess the resource.

### LATENT
The modern Stage10 cell is a location where the resource can exist in the modern distribution, but it was not present there at 4000 BCE.

A civilization that does not possess the resource does not see a LATENT icon.

### ACTIVE_INTRODUCED
A LATENT cell has become physically introduced through gameplay, normally because a civilization that already possesses the resource settled a city whose territory contains that latent cell.

ACTIVE_INTRODUCED is globally real: any civilization that later explores the tile can see the icon.

No new cell is created. Introduction only activates an already-selected Stage10 LATENT cell.

## 4. Civilization state

Only one persistent civilization-level flag is required:

`has_resource[civ][resource] = true / false`

Once true, it stays true in V2.

No separate probability, stock quantity, city inventory, or regional inventory is required.

## 5. Visibility rule

Fog of war is unchanged.

For an explored tile:

```
if cell == START_VISIBLE:
    show resource
elif cell == ACTIVE_INTRODUCED:
    show resource
elif cell == LATENT and has_resource[civ][resource]:
    show resource
else:
    hide resource
```

Meaning:
- a source exists independently of civilizations;
- a latent modern location is invisible to a civilization that has never acquired the resource;
- a civilization that has acquired the resource can see its explored modern potential cells;
- an actually introduced cell can be seen by anybody who explores it.

## 6. Acquisition events

### 6.1 Exploration
Entering or revealing a START_VISIBLE cell reveals the icon.

Exploration alone does **not** set `has_resource=true`.

### 6.2 Settlement of a source
If a civilization founds a city or expands city territory to include a START_VISIBLE resource cell, it acquires that resource civilization-wide.

`has_resource[civ][resource] = true`

This prevents a source resource from becoming permanently unavailable merely because an original local civilization disappeared.

### 6.3 Trade
Trade with a civilization that already possesses a dynamic resource can transfer it.

Example:
America MAIZE -> Spain by trade -> Korea by trade with Spain.

Korea does not need direct American contact.

### 6.4 Conquest
Capturing a city from a civilization that possesses a dynamic resource is a valid acquisition route in the simple V2 system.

Example:
Spain possesses HORSES and CATTLE and founds an American colony.
A Native American civilization captures that colony.
The captor acquires HORSES and CATTLE.
Its explored American HORSES/CATTLE LATENT cells now become visible to it.

### 6.5 First contact
First contact alone does not automatically transfer a resource.

It may enable diplomacy/trade, but acquisition requires one of the explicit routes above.

## 7. Settlement and introduction

If a civilization that possesses resource R settles or controls territory containing LATENT R cells:

- those cells are visible to that civilization;
- cells inside the settlement/city territory may be marked ACTIVE_INTRODUCED;
- they then become physically present and visible to any later explorer.

This is the simple representation of crops or livestock being brought with settlers.

There is no random spread to neighboring cells in V2.

## 8. Canonical examples

### Spain introduces horses to the Americas

Before European arrival:
- American HORSES cells are LATENT.
- Native American civilizations cannot see them.

Spain already has HORSES.
Spain explores and settles America:
- Spain can see explored American HORSES latent cells.
- HORSES cells inside the colony territory can become ACTIVE_INTRODUCED.
- Native civilizations still cannot see the other latent horse cells.

A Native civilization captures the Spanish colony:
- it acquires HORSES;
- all of its explored American HORSES latent cells become visible;
- it can then transfer HORSES to another civilization through trade.

### Korean rice alternate history

At 4000 BCE:
- Korean RICE cells are LATENT.
- Yangtze-region RICE source cells are START_VISIBLE.

If Korea trades with a civilization that possesses RICE:
- Korea acquires RICE;
- its explored Korean RICE latent cells become visible immediately;
- no fixed historical Korean rice-introduction date is required.

### Original source civilization disappears

A local maize civilization can be destroyed.
A START_VISIBLE MAIZE source cell remains a real source.
A later explorer can still see it and acquire MAIZE by settling the source region.

## 9. 4000 BCE initial mask

Canonical reviewed mask:
`civ_map_stage10_resources/history_4000bce_v3/`

Exact Stage10Y QA:
- 6,630 dynamic-resource cells
- 1,950 START_VISIBLE
- 4,680 LATENT

Critical locked checks:
- Americas HORSES/CATTLE/SHEEP: all LATENT at start
- Korea RICE: all LATENT at start
- China early RICE: visible
- Mesoamerica MAIZE: visible
- Upper Amazon COCOA: visible
- Ethiopia/Boma COFFEE: visible

## 10. Non-dynamic exceptions

### Geological/mineral resources
Fixed to their map deposits. They do not move through trade or colonization.

### NITER
Natural NITER cells remain fixed.
A separate production facility/technology may manufacture saltpetre later.

### SALT
Natural SALT cells remain fixed.
Coastal salt production is represented by a separate tile improvement/facility such as SALTWORKS, not a city building and not by moving the SALT resource.

### Wild biological resources
BISON, DEER, FURS, IVORY, FISH, CRAB, PEARLS, WHALES, CORAL and TRUFFLES do not use this crop/livestock transfer system in V2.

### PERFUME
Keep as a source/raw luxury representation but exclude it from dynamic transfer in V2.

### SILK and INCENSE
Not included in the reviewed 18-resource V2 dynamic set. Leave unchanged pending a later explicit decision.

## 11. Minimal implementation data

Per dynamic resource cell:
```
hex_id
resource_id
history_state_4000  # START_VISIBLE or LATENT
active_introduced   # false initially unless later gameplay activates it
```

Per civilization:
```
civ_id
resource_id
has_resource
```

That is sufficient for V2.
