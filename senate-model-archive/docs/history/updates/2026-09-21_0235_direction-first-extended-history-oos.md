# Performance experiment: extended-history National + economic nested OOS

- Generated UTC: 2026-09-20T17:31:00.622795+00:00
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
| 99 | 8.9576 | 7.2484 | 89.9% |

## Nested choices

| test | train N | inner folds | inner correct | inner direction | inner MAE | inner RMSE | PVI ridge | local ridge | econ ridge | National ridge |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 134 | 3 | 86/102 | 84.3% | 13.3766 | 17.6351 | 4.0 | 16.0 | 1024.0 | 0.0 |
| 2018 | 199 | 5 | 144/167 | 86.2% | 11.3976 | 15.2808 | 0.0 | 64.0 | 256.0 | 0.0 |
| 2022 | 264 | 7 | 202/232 | 87.1% | 10.2580 | 14.1211 | 4.0 | 16.0 | 1024.0 | 0.0 |

## Benchmarks

- Previous leakage-safe midterm-only National nested RMSE: 9.1890.
- Previous full-cycle attempt RMSE: 9.0712, but its 2014 inner tuning had no valid fold.
- Best descriptive fixed-grid diagnostic: 8.9084.
- Preserved original Core V2 fundamentals benchmark: 7.99.

## Objective correction

PRIMARY: maximize strictly chronological inner-OOS winner/direction correctness. Ties are broken by lower MAE, then lower RMSE.

The outer 99-race result is judged first by correct winner count / direction percentage, not by RMSE.

## Decision rule

Keep this architecture only if its strictly chronological outer OOS direction correctness exceeds the preserved benchmark; use MAE/RMSE only as tie-breakers.

## Data limitation

The BEA economic series is still the current revised SQINC1 history rather than release-vintage snapshots, so this remains a performance experiment, not final vintage-clean replication.

## Outputs

- experiments/history_extension/direction_results/direction_first_summary.csv
- experiments/history_extension/direction_results/direction_first_choices.csv
- experiments/history_extension/direction_results/direction_first_predictions.csv
