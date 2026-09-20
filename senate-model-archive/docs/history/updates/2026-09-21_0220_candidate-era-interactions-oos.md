# Performance experiment: candidate/local era interactions OOS

- Generated UTC: 2026-09-20T17:24:01.991679+00:00
- BEA member: SQINC1__ALL_AREAS_1948_2026.csv
- Baseline includes PVI, last-prior SameSeat, SameSeat gap, signed RelativeEconomicGrowth, and 45-day Generic Ballot National.
- Era index is (cycle-2006)/4, so candidate/local coefficients can change linearly across midterm cycles.

## Combined 99-row modern OOS

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| base_national64 | 99 | 8.9084 | 6.6580 | 89.9% |
| seat_era | 99 | 8.7967 | 6.5682 | 89.9% |
| inc_era | 99 | 8.5042 | 6.8893 | 87.9% |
| candidate_era | 99 | 10.6688 | 7.8960 | 88.9% |
| full_local_era | 99 | 10.5396 | 7.7790 | 88.9% |
| nested_training_only | 99 | 9.8862 | 7.4947 | 88.9% |

## Nested choices

| test cycle | architecture | National ridge | level ridge | era ridge | inner RMSE |
|---:|---|---:|---:|---:|---:|
| 2014 | full_local_era | 0.0 | 4.0 | 1024.0 | 26.6886 |
| 2018 | inc_era | 64.0 | 4.0 | 64.0 | 20.0247 |
| 2022 | inc_era | 64.0 | 4.0 | 64.0 | 16.9131 |

## Decision

- Fixed National64 no-local baseline RMSE: 8.9084.
- Leakage-safe nested candidate/local era RMSE: 9.8862.
- Nested improvement: -0.9778 RMSE points.
- Candidate/local era structure is retained only if the nested training-only result improves on the comparable baseline.

## Outputs

- performance/results/candidate_era_oos_summary.csv
- performance/results/candidate_era_oos_choices.csv
- performance/results/candidate_era_oos_predictions.csv
