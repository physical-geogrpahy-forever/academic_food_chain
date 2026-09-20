# CIV resource history mask — 4000 BCE V3

Date: 2026-09-20  
Status: reviewed implementation baseline for the 18 dynamic biological resources

## Core rule

Stage10 keeps the modern resource-placement cells. V3 does not add, delete or move those cells.

For the 18 dynamic resources, each existing Stage10 cell is classified at game start as:

- `START_VISIBLE`: the resource or a directly usable source population existed by about 4000 BCE. Any civilization that reveals the tile can see the resource icon.
- `LATENT`: the cell represents a modern distribution location where the resource was not yet present at 4000 BCE. It is invisible to civilizations that have not acquired that resource.
- other resources remain static in this historical-mask pass.

The 4000 BCE envelopes are intentionally broad for gameplay. They represent a generous 4000 BCE starting world, not exact archaeological polygons.

## Dynamic V2 set

BANANAS, CATTLE, CITRUS, COCOA, COFFEE, COTTON, DYES, HORSES, MAIZE, OLIVES, RICE, SHEEP, SPICES, SUGAR, TEA, TOBACCO, WHEAT, WINE.

DYES and SPICES remain unified game resources. PERFUME is excluded from transfer. Geological/mineral resources do not move.

## Exact Stage10Y QA

Applied to the exact Stage10Y 12,500-cell placement artifact.

- dynamic-resource cells: 6,630
- START_VISIBLE: 1,950 (29.4%)
- LATENT: 4,680 (70.6%)

See `resource_history_4000bce_exact_summary_v3.csv`.

Critical checks all pass:
- Americas HORSES: 472 checked, 0 START_VISIBLE
- Americas CATTLE: 267 checked, 0 START_VISIBLE
- Americas SHEEP: 32 checked, 0 START_VISIBLE
- Korea RICE: 7 checked, 0 START_VISIBLE
- Mesoamerica MAIZE: 23 checked, 22 START_VISIBLE
- Upper Amazon COCOA: 24 checked, 24 START_VISIBLE
- Ethiopia/Boma COFFEE: 8 checked, 8 START_VISIBLE
- China RICE: 62 checked, 62 START_VISIBLE

## Korea QA

All dynamic-resource cells in the current Korea window are LATENT at 4000 BCE:
CATTLE 1, CITRUS 2, HORSES 6, MAIZE 1, RICE 7, TOBACCO 4, WINE 4.

This means Korea can acquire RICE through contact-enabled gameplay, for example by trading with a civilization that already has RICE. Once acquired, the existing Korean latent RICE cells can be shown to that civilization.

## SUGAR V3 correction

A New-Guinea-only mask produced zero visible Stage10 SUGAR cells because the current selected modern SUGAR cells do not fall in New Guinea itself.

V3 uses a broad New Guinea + ISEA/Southeast Asia source/dispersal belt, 95–130E and 10S–20N. The 20N cap keeps South China latent. Result: 39 START_VISIBLE and 191 LATENT SUGAR cells.

## Gameplay semantics

The historical mask is paired with `contact_dynamic_resource_system_v2.md`.

Important:
- seeing a START_VISIBLE source tile does not itself grant civilization-wide possession;
- settling the source region can grant possession;
- trade can transfer a possessed dynamic resource;
- conquest can transfer possessed dynamic resources;
- first contact alone does not automatically transfer resources;
- once a civilization possesses a resource, its explored LATENT Stage10 cells for that resource can be displayed/used according to the simple V2 rule;
- possession is persistent after acquisition;
- historical dates are not hard-coded unlock dates.

## Files

- `resource_start_visible_4000bce_mask_regions_v3.csv`
- `apply_resource_history_4000bce_v3.py`
- `resource_history_4000bce_exact_summary_v3.csv`
- `resource_history_4000bce_critical_checks_v3.csv`

V1 is superseded by this directory.
