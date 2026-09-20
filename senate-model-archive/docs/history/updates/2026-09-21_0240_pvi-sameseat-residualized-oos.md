# Performance experiment: nested PVI weighting + residualized SameSeat

- Generated UTC: 2026-09-20T17:29:59.507647+00:00
- Model rows: 297
- Outer validation: preserved 99 races in 2014, 2018, 2022.
- PVI recent-election weight candidates: 0.50, 0.67, 0.80, 1.00.
- SameSeat modes: raw margin, prior-PVI residual, age-decayed residual, two-observation exponentially weighted residual.
- All architecture choices and ridge strengths are selected inside chronological inner OOS only.

## Result

| N | RMSE | MAE | direction |
|---:|---:|---:|---:|
| 99 | 8.6566 | 6.8217 | 88.9% |

## Outer-fold choices

| test | PVI recent weight | SameSeat mode | PVI ridge | local ridge | econ ridge | National ridge | inner RMSE |
|---:|---:|---|---:|---:|---:|---:|---:|
| 2014 | 1.0 | raw | 4.0 | 64.0 | 4096.0 | 0.0 | 16.4051 |
| 2018 | 1.0 | raw | 4.0 | 64.0 | 4096.0 | 0.0 | 15.0009 |
| 2022 | 1.0 | raw | 4.0 | 64.0 | 4096.0 | 0.0 | 13.3891 |

## Benchmarks

- Current best strict nested OOS: 8.8189 RMSE.
- Best descriptive fixed-grid diagnostic: 8.9084 RMSE.
- Preserved original Core V2 fundamentals: 7.99 RMSE.

## Decision

Keep the selected PVI/SameSeat architecture only if RMSE is below 8.8189. Otherwise retain the extended-history baseline unchanged.

## Outputs

- experiments/seat_pvi_tuning/results/seat_pvi_summary.csv
- experiments/seat_pvi_tuning/results/seat_pvi_choices.csv
- experiments/seat_pvi_tuning/results/seat_pvi_predictions.csv
