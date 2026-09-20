# Performance experiment: National generic-ballot signal OOS

- Generated UTC: 2026-09-20T17:21:33.575589+00:00
- Historical source bytes: 754089
- 2018+ average source bytes: 266194
- BEA member: SQINC1__ALL_AREAS_1948_2026.csv

## 45-day national values

| cycle | election | target | source date | D-R generic margin | source |
|---:|---|---|---|---:|---|
| 2006 | 2006-11-07 | 2006-09-23 | 2006-09-23 | 9.2022 | historical_topline |
| 2010 | 2010-11-02 | 2010-09-18 | 2010-09-18 | -3.6178 | historical_topline |
| 2014 | 2014-11-04 | 2014-09-20 | 2014-09-20 | -1.8046 | historical_topline |
| 2018 | 2018-11-06 | 2018-09-22 | 2018-09-22 | 8.8349 | generic_ballot_averages |
| 2022 | 2022-11-08 | 2022-09-24 | 2022-09-24 | 1.8033 | generic_ballot_averages |

## Combined 99-row modern OOS

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| structural | 99 | 10.6055 | 7.8754 | 87.9% |
| structural_econ | 99 | 10.4571 | 7.8451 | 86.9% |
| structural_national | 99 | 9.6223 | 7.9034 | 86.9% |
| structural_econ_national | 99 | 9.6740 | 7.8822 | 87.9% |
| structural_econ_national_ridge1 | 99 | 9.6289 | 7.8318 | 87.9% |
| structural_econ_national_ridge4 | 99 | 9.5074 | 7.6936 | 87.9% |
| structural_econ_national_ridge16 | 99 | 9.1774 | 7.2766 | 86.9% |
| structural_econ_national_ridge64 | 99 | 8.9084 | 6.6580 | 89.9% |
| nested_training_only | 99 | 9.1890 | 7.3299 | 87.9% |

## Decision

- Structural baseline RMSE: 10.6055.
- Structural + fixed economic signal RMSE: 10.4571.
- Lowest fixed diagnostic architecture: structural_econ_national_ridge64 with RMSE 8.9084; fixed-grid test comparison is descriptive only.
- Leakage-safe nested training-only RMSE: 9.1890.
- Improvement vs structural: +1.6971.
- Improvement vs structural+econ: +1.5487.
- This is still a reconstruction diagnostic, not the preserved 7.99 headline Core V2, because candidate and PersonalVote architecture are not yet fully restored.

## Outputs

- performance/results/national_oos_summary.csv
- performance/results/national_oos_predictions.csv
- performance/results/national_oos_nested_choices.csv
- performance/results/national_45d_values.csv
