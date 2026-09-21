# Production validation lock: 96/99 clean OOS and 98/99 retrospective

## Permanent distinction

- Clean nested OOS: **96/99 = 97.0%**.
- Production retrospective diagnostic: **98/99 = 99.0%**.
- The 98/99 result is NOT OOS because the production selector is fit using history through 2022.

## 98/99 exact race table

- Canonical file: final/validation/production_98of99_predictions.csv
- Rows: 99.
- Fixed-poll baseline correct: 94.
- Production-selector correct: 98.
- Only wrong race: **2014 North Carolina**.
- Corrected relative to the 94/99 baseline: **2018 Nevada, Missouri, Florida, Indiana**.

## Base prior reproduction

- Canonical base-prior predictions: final/validation/base_prior_99_predictions.csv
- Exact fitted coefficients by outer cycle: final/validation/base_prior_coefficients_by_cycle.csv
- Standardization means and standard deviations: final/validation/base_prior_standardization_by_cycle.csv
- Maximum absolute reconstruction error over all 99 base-prior predictions: **8.527e-14**.

## Selector reproduction

- Production config: final/validation/core_v2r_direction_2026_production.json
- Full selector grid: final/validation/production_selector_top_grid.csv
- Clean nested 96/99 race table and choices are frozen alongside the retrospective files.

## Integrity

- manifest.json stores SHA-256 checksums of source and canonical files.
- Future experiments must not overwrite this directory.
- Any changed production model must use a new versioned directory.
