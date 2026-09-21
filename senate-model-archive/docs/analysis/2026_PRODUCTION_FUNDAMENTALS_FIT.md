# 2026 production fundamentals fit

## Status

- Fits the canonical Core V2-R fundamentals source on all eligible historical rows through 2022.
- The source SHA-256 is checked against final/validation/manifest.json before fitting.
- This step freezes coefficients and standardization only; it does not emit 2026 race directions.

## Canonical feature set

- pvi
- same_last
- same_gap
- econ
- national
- inc_diff
- outparty
- inc_era
- outparty_era

## Selected fit

- architecture: inc_era
- training rows: 290
- training cycles: 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022
- lambda_local: 256.0
- lambda_econ: 256.0
- lambda_national: 0.0
- lambda_inc: 256.0
- lambda_era: 1024.0
- chronological inner RMSE used for tuning: 12.202271

Training-set diagnostics below are descriptive fit checks only, not OOS validation:
- RMSE: 12.276501
- MAE: 8.716470
- direction accuracy: 90.000%

## Outputs

- data/snapshots/2026_production_fundamentals_coefficients.csv
- data/snapshots/2026_production_fundamentals_standardization.csv
- data/snapshots/2026_production_fundamentals_fit_meta.json
