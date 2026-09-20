# Reconstruct Stage10Y fixed placement V1

The repository stores the repaired BISON, IVORY and WHALES placement as a compact patch rather than the full 12,500-row fixed table.

## Required inputs

1. Original Stage10Y V2 placement table
2. Source Stage10Y GPKG with cell attributes
3. `replacement_ids_v1.json`

## Procedure

1. Load the original Stage10Y V2 placement table.
2. Remove every row whose `RESOURCE_ID` is `BISON`, `IVORY`, or `WHALES`.
3. Read the replacement cell IDs from `replacement_ids_v1.json`.
4. Join those IDs to the source Stage10Y GPKG to recover cell coordinates and attributes.
5. Assign:
   - BISON -> bonus, quantity 1
   - IVORY -> luxury, quantity 1
   - WHALES -> luxury, quantity 1
6. Append the repaired rows to the unchanged Stage10Y rows.
7. Re-run:
   - one-resource-per-hex audit
   - LAND/COAST/OCEAN surface-rule audit
   - resource-count audit
8. Keep the result as REVIEW BUILD until visual and gameplay QA are complete.

## Local artifact

The full local review table produced in the chat was:

`CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`

That large local CSV is not currently stored in this GitHub folder. Do not claim that a full CSV, gzip copy, or package archive is present unless it is uploaded later.
