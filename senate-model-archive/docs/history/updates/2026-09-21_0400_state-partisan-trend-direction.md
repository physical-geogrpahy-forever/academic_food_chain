# State partisan trend direction experiment

- Generated UTC: 2026-09-20T18:18:27.755370+00:00
- Baseline: fixed 45-day poll blend, 94/99.
- State trend = most recent completed presidential state lean minus the preceding presidential state lean.
- This adds information that the 0.67/0.33 PVI average can damp when a state is moving quickly.
- Gamma, posterior threshold, and minimum trend magnitude are selected only from cycles earlier than each outer test cycle.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 93 | 93.9% | -1 | 1 |
| 2014 | 33 | 32 | 97.0% | 31 | 93.9% | -1 | 1 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected trend rule

| test | gamma | posterior threshold | minimum | train accuracy | train flips |
|---:|---:|---:|---:|---:|---:|
| 2014 | 1.5 | 3 | 0 | 87.5% | 6 |
| 2018 | 0.5 | 2 | 0 | 90.1% | 4 |
| 2022 | 0.5 | 2 | 0 | 90.3% | 5 |

## Correctness changes

- 2014 AK 12: baseline correct -> trend wrong, trend=10.96, post -2.65->13.79

## Decision

Adopt only if historical winner-direction accuracy exceeds 94/99 under chronological OOS.

## Outputs

- experiments/state_trend_direction/results/state_trend_summary.csv
- experiments/state_trend_direction/results/state_trend_choices.csv
- experiments/state_trend_direction/results/state_trend_predictions.csv
