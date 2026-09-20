# Performance experiment: extended-history National + economic nested OOS

- Generated UTC: 2026-09-20T17:26:32.820889+00:00
- Model rows: 297
- Earliest modeled cycle: 2006
- PVI is rebuilt directly from the two most recent completed presidential-election state leans before each Senate cycle.
- SameSeat uses the most recent prior same-seat result plus year gap.
- National uses 45-day Generic Ballot D-R.
- Economic signal uses president-party-signed state Q1 YoY personal-income growth relative to U.S.

## Cycle coverage

- 2006: 32 races
- 2008: 33 races
- 2010: 36 races
- 2012: 33 races
- 2014: 33 races
- 2016: 32 races
- 2018: 33 races
- 2020: 32 races
- 2022: 33 races

## OOS result

| N | RMSE | MAE | direction |
|---:|---:|---:|---:|
| 99 | 8.8189 | 6.9723 | 90.9% |

## Nested choices

| test | train N | inner folds | PVI ridge | local ridge | econ ridge | National ridge | inner RMSE |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 134 | 3 | 4.0 | 64.0 | 1024.0 | 0.0 | 16.6791 |
| 2018 | 199 | 5 | 1.0 | 64.0 | 1024.0 | 0.0 | 15.2093 |
| 2022 | 264 | 7 | 4.0 | 64.0 | 1024.0 | 0.0 | 13.6011 |

## Benchmarks

- Previous leakage-safe midterm-only National nested RMSE: 9.1890.
- Previous full-cycle attempt RMSE: 9.0712, but its 2014 inner tuning had no valid fold.
- Best descriptive fixed-grid diagnostic: 8.9084.
- Preserved original Core V2 fundamentals benchmark: 7.99.

## Decision rule

Keep this architecture only if its strictly chronological outer OOS RMSE is lower than the prior leakage-safe benchmarks.

## Data limitation

The BEA economic series is still the current revised SQINC1 history rather than release-vintage snapshots, so this remains a performance experiment, not final vintage-clean replication.

## Outputs

- experiments/history_extension/results/extended_history_summary.csv
- experiments/history_extension/results/extended_history_choices.csv
- experiments/history_extension/results/extended_history_predictions.csv
