# Performance experiment: RelativeEconomicGrowth OOS

 - Generated UTC: 2026-09-20T17:20:05.099396+00:00
- BEA source: https://apps.bea.gov/regional/zip/SQINC.zip
- ZIP bytes: 18134176
- CSV member: SQINC1__ALL_AREAS_1948_2026.csv
- Economic diagnostic uses Q1 year-over-year personal-income growth from current revised SQINC1 values. This is a signal test, not yet a historical-vintage-valid headline model.

## Combined 99-row modern OOS results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| structural | 99 | 10.6055 | 7.8754 | 87.9% |
| econ_rel_us | 99 | 11.1554 | 8.2261 | 86.9% |
| econ_rel_median | 99 | 10.7621 | 7.9506 | 86.9% |
| econ_rel_us_signed | 99 | 10.4571 | 7.8451 | 86.9% |
| econ_rel_median_signed | 99 | 10.5979 | 7.8425 | 87.9% |
| econ_nested_selection | 99 | 10.9070 | 7.9525 | 84.8% |

## Nested choices

| test cycle | selected economic coding | lambda | inner RMSE |
|---:|---|---:|---:|
| 2014 | econ_rel_us | 16.0 | 30.1048 |
| 2018 | econ_rel_us_signed | 16.0 | 23.0469 |
| 2022 | econ_rel_us_signed | 4.0 | 19.6221 |

## Decision

- Structural baseline RMSE: 10.6055.
- Best observed architecture: econ_rel_us_signed, RMSE 10.4571.
- Improvement: +0.1484 RMSE points.
- Retain the economic architecture for full Core V2-R only if improvement is positive. Before claiming headline comparability, rerun with release-vintage-consistent BEA data.

## Outputs

- performance/results/economic_growth_oos_summary.csv
- performance/results/economic_growth_oos_choices.csv
- performance/results/economic_growth_oos_predictions.csv
