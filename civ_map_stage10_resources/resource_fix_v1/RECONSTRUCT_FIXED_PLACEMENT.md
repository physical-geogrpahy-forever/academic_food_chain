# Reconstruct Stage10Y fixed placement V1

The full 12,500-row fixed table is large, so the repository stores the replacement patch for the three repaired resources as three compact CSV files.

Base table: Stage10Y V2 placement preview.

Procedure:
1. Load the original Stage10Y V2 placement table.
2. Remove rows where `RESOURCE_ID` is one of `BISON`, `IVORY`, `WHALES`.
3. Append:
   - `replacement_patch_bison_v1.csv`
   - `replacement_patch_ivory_v1.csv`
   - `replacement_patch_whales_v1.csv`
4. Sort by class/resource/id if desired.
5. Re-run one-resource-per-hex and surface audits.

The local full table created in this chat is `CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`; the three patch files contain all rows needed to reproduce its changed portion.
