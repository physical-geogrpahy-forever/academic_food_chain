# Performance experiment: RelativeEconomicGrowth OOS

 - Generated UTC: 2026-09-20T17:15:28.081065+00:00
- BEA source: https://apps.bea.gov/regional/zip/SQINC.zip
- ZIP bytes: 18134176
- CSV member: SQINC11__ALL_AREAS_1998_2026.csv
- Economic diagnostic uses Q1 year-over-year personal-income growth from current revised SQINC1 values. This is a signal test, not yet a historical-vintage-valid headline model.

## Combined 99-row modern OOS results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| structural | 99 | 10.6055 | 7.8754 | 87.9% |
| econ_rel_us | 99 | 15.1238 | 11.1385 | 83.8% |
| econ_rel_median | 99 | 10.6807 | 7.9742 | 87.9% |
| econ_rel_us_signed | 99 | 12.0231 | 9.4472 | 84.8% |
| econ_rel_median_signed | 99 | 10.6824 | 8.0045 | 86.9% |
| econ_nested_selection | 99 | 10.5828 | 7.8136 | 88.9% |

## Nested choices

| test cycle | selected economic coding | lambda | inner RMSE |
|---:|---|---:|---:|
| 2014 | econ_rel_median | 0.0 | 30.1551 |
| 2018 | econ_rel_us_signed | 256.0 | 22.8692 |
| 2022 | econ_rel_us_signed | 256.0 | 19.5011 |

## Decision

- Structural baseline RMSE: 10.6055.
- Best observed architecture: econ_nested_selection, RMSE 10.5828.
- Improvement: +0.0227 RMSE points.
- Retain the economic architecture for full Core V2-R only if improvement is positive. Before claiming headline comparability, rerun with release-vintage-consistent BEA data.

## Outputs

- performance/results/economic_growth_oos_summary.csv
- performance/results/economic_growth_oos_choices.csv
- performance/results/economic_growth_oos_predictions.csv
