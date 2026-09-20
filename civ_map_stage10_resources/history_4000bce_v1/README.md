# CIV resource history mask — 4000 BCE V1

## Status
Broad game-design mask for the 18 dynamic biological resources discussed in chat.

This mask does not add or move resource cells. It only classifies already-selected modern Stage10 resource cells as `START_VISIBLE` or `LATENT`; all non-dynamic resources are `STATIC`.

## Runtime meaning
- `START_VISIBLE`: physically present at game start; any civilization revealing the tile can see it.
- `LATENT`: reserved modern Stage10 cell; not physically present at 4000 BCE and invisible to a civ that has not acquired the resource.
- `STATIC`: outside this dynamic transfer system.

## Agreed acquisition model
A civilization can acquire a dynamic resource by:
1. discovering a real source tile and later settling that source region;
2. trading with a civilization that already has the resource;
3. capturing a city of a civilization that already has the resource.

After acquisition, that civilization can see/use its relevant latent modern distribution and can become a secondary transfer source for other civilizations.

## Important implementation note
The CSV uses intentionally broad rectangular envelopes. These are game masks, not archaeological claims that real boundaries were rectangular. They only intersect the existing Stage10 resource cells, so they never create resources in a new cell.

## Dynamic resources
MAIZE, WHEAT, RICE, BANANAS, CITRUS, COCOA, COTTON, SUGAR, COFFEE, TEA, TOBACCO, OLIVES, WINE, DYES, SPICES, HORSES, CATTLE, SHEEP.

## QA targets
1. American HORSES/CATTLE/SHEEP must be LATENT.
2. Korean RICE must be LATENT.
3. Yangtze RICE must be START_VISIBLE.
4. Mesoamerican MAIZE must be START_VISIBLE; Eurasian MAIZE must be LATENT.
5. Upper-Amazon COCOA must be START_VISIBLE; African cacao must be LATENT.
6. Ethiopian/South-Sudan COFFEE must be START_VISIBLE; Yemen/Brazil coffee must be LATENT.
