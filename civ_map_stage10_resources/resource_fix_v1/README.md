# resource_fix_v1

Status: REVIEW BUILD, not canonical final placement.

This folder stores the reproducible patch for the three repaired resources:
- BISON
- IVORY
- WHALES

## Repository contents

- `replacement_ids_v1.json`: complete replacement cell IDs for BISON, IVORY, WHALES
- `RECONSTRUCT_FIXED_PLACEMENT.md`: exact reconstruction procedure for the full fixed Stage10Y placement table
- `replacement_comparison_summary_v1.csv`: before/after anomaly counts
- `replacement_pool_counts_v1.csv`: achieved selections by quota pool
- `replacement_region_comparison_v1.csv`: broad regional distribution comparison
- `plateau_comparison_v1.csv`: top-tie plateau comparison

## Full-table reconstruction

The full local review table created in the chat was:
`CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`

To reconstruct it from the repository:
1. Load the original Stage10Y V2 placement table.
2. Remove BISON, IVORY and WHALES rows.
3. Rebuild those rows from `replacement_ids_v1.json` and the source Stage10Y GPKG attributes.
4. Append them back and re-run one-resource-per-hex and surface audits.

The repository intentionally stores the compact replacement patch rather than claiming that the large full CSV or gzip archive is present when it is not.
