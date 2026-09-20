# Out-party incumbent survival model

- Generated UTC: 2026-09-20T18:05:46.864868+00:00
- The 94/99 fixed-poll baseline is left unchanged for every non-out-party-incumbent race.
- A separate survival classifier is trained only on historical out-party incumbents.
- Features are oriented to the incumbent: fixed-poll posterior, PVI disadvantage, prior same-seat performance, poll signal, national/economic context, and related interactions.
- An override occurs only when the survival classifier disagrees with the baseline and exceeds a confidence threshold selected on earlier-cycle OOS.

## Historical out-party incumbent counts

- 2008: 6
- 2010: 2
- 2012: 6
- 2014: 5
- 2016: 5
- 2018: 10
- 2020: 3
- 2022: 3

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 92 | 92.9% | -2 | 2 |
| 2014 | 33 | 32 | 97.0% | 30 | 90.9% | -2 | 2 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected survival models

| test | feature set | lambda | confidence | train outparty N | inner accuracy | inner overrides |
|---:|---|---:|---:|---:|---:|---:|
| 2014 | core | 128 | 0.65 | 14 | 100.0% | 0 |
| 2018 | core | 128 | 0.75 | 24 | 81.2% | 0 |
| 2022 | core | 128 | 0.75 | 37 | 72.4% | 0 |

## Correctness changes

- 2014 AK 12: baseline correct -> survival wrong
- 2014 AR 32: baseline correct -> survival wrong

## Decision

Adopt only if adjusted accuracy exceeds 94/99 while non-out-party races remain untouched.

## Outputs

- experiments/outparty_survival/results/survival_summary.csv
- experiments/outparty_survival/results/survival_choices.csv
- experiments/outparty_survival/results/survival_predictions.csv
