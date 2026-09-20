# Performance experiment: full-cycle National + economic group-ridge OOS

- Generated UTC: 2026-09-20T17:23:44.955746+00:00
- Total modeling rows: 199
- Training uses all available Senate cycles from 2006 through 2022, including presidential-election years.
- Outer headline validation remains exactly the preserved 99 races in 2014, 2018, 2022.

## Results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| fullcycle_nested_group_ridge | 99 | 9.0712 | 6.9215 | 90.9% |
| fullcycle_fixed_N64 | 99 | 9.5017 | 6.9987 | 89.9% |

## Nested choices

| test cycle | lambda local | lambda econ | lambda national | inner RMSE |
|---:|---:|---:|---:|---:|
| 2014 | 0.0 | 0.0 | 0.0 | 1000000000.0000 |
| 2018 | 0.0 | 0.0 | 0.0 | 10.6796 |
| 2022 | 0.0 | 0.0 | 4.0 | 9.5393 |

## Comparison target

- Previous best 99-row reconstruction diagnostic: RMSE 8.9084 from midterm-only structural + economic + national with national ridge 64.
- This experiment is retained only if the full-cycle chronological training lowers that OOS RMSE.

## Leakage guard

- 45-day generic-ballot values use only dates on or before the snapshot.
- Headline outcomes are never used in hyperparameter selection for their own outer fold.
- Economic values are still current revised SQINC1 Q1 values, so this remains a signal/performance experiment rather than final vintage-clean Core V2 reproduction.

## Outputs

- performance/results/fullcycle_national_econ_summary.csv
- performance/results/fullcycle_national_econ_choices.csv
- performance/results/fullcycle_national_econ_predictions.csv
