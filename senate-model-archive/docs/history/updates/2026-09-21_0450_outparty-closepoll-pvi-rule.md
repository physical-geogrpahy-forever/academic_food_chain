# Out-party incumbent close-poll PVI override

- Generated UTC: 2026-09-20T18:44:44.266125+00:00
- Baseline: fixed 45-day poll blend, 94/99.
- Rule applies only to races with an out-party incumbent and a 45-day poll margin whose absolute value is below a threshold.
- If eligible, direction is set to the state PVI direction rather than the incumbency-heavy posterior.
- The threshold, including a no-rule option, is selected only from cycles before each outer test cycle by winner count.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 | 0 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected threshold

| test | threshold | train N | train correct | train accuracy | train flips |
|---:|---:|---:|---:|---:|---:|
| 2014 | -1 | 96 | 80 | 83.3% | 0 |
| 2018 | -1 | 161 | 141 | 87.6% | 0 |
| 2022 | 0.75 | 226 | 202 | 89.4% | 3 |

## Correctness changes


## Decision

- Adopt only if combined adjusted accuracy exceeds 94/99 under this strict forward-selection protocol.
- This rule is intentionally narrow: it does not alter non-out-party races or out-party races whose 45-day polls show a clear lead.

## Outputs

- experiments/outparty_closepoll_pvi/results/closepoll_summary.csv
- experiments/outparty_closepoll_pvi/results/closepoll_choices.csv
- experiments/outparty_closepoll_pvi/results/closepoll_predictions.csv
