# Full-cycle incumbency era-interaction OOS

- Generated UTC: 2026-09-20T17:27:52.539946+00:00
- Modeling rows: 290
- Outer validation: preserved 99 races in 2014, 2018, 2022.
- 2000, 2002, 2004 are used only as SameSeat lag sources.
- Headline incumbency/out-party flags use the corrected audited features; historical training flags use prior same-seat winner identity.

## Result

- RMSE: 9.7457
- MAE: 7.8082
- Direction: 90.9%

## Nested choices

| cycle | architecture | local | econ | national | inc | era | inner RMSE |
|---:|---|---:|---:|---:|---:|---:|---:|
| 2014 | inc_era | 256.0 | 256.0 | 0.0 | 256.0 | 256.0 | 15.5286 |
| 2018 | inc_era | 256.0 | 256.0 | 0.0 | 256.0 | 256.0 | 13.8441 |
| 2022 | inc_era | 256.0 | 256.0 | 0.0 | 256.0 | 1024.0 | 12.8296 |

## Comparison

- Current leakage-safe full-cycle National+economic benchmark before this experiment: RMSE 8.8467.
- Keep this architecture only if its 99-row RMSE is below 8.8467.

## Outputs
- performance/results/fullcycle_inc_era_summary.csv
- performance/results/fullcycle_inc_era_choices.csv
- performance/results/fullcycle_inc_era_predictions.csv
