# Out-party incumbent favored-posterior rule

- Generated UTC: 2026-09-20T17:52:24.721256+00:00
- Baseline: fixed Core V2 poll blend, 94/99.
- Rule is eligible only when an out-party incumbent exists AND the fixed-poll posterior still favors that incumbent.
- Strong incumbent PersonalVote can protect the incumbent from the state-partisan penalty.
- Parameters for each outer cycle are selected only from earlier cycles by number of correctly classified winners.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 93 | 93.9% | -1 | 5 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 31 | 93.9% | +2 | 2 |
| 2022 | 33 | 33 | 100.0% | 30 | 90.9% | -3 | 3 |

## Selected parameters

| test | PersonalVote threshold | shrink k | gamma | train accuracy | train flips |
|---:|---:|---:|---:|---:|---:|
| 2014 | 0 | 1 | 1 | NA | 0 |
| 2018 | 3 | 2 | 6 | 100.0% | 1 |
| 2022 | 5 | 2 | 10 | 98.5% | 6 |

## Correctness changes

- 2018 MO 109: baseline wrong -> adjusted correct, posterior 4.72 -> -1.28, shrunk PV 1.78
- 2018 IN 102: baseline wrong -> adjusted correct, posterior 5.41 -> -0.59, shrunk PV 2.34
- 2022 AZ 8919: baseline correct -> adjusted wrong, posterior 7.10 -> -2.90, shrunk PV 1.88
- 2022 NV 8937: baseline correct -> adjusted wrong, posterior 2.39 -> -7.61, shrunk PV 0.60
- 2022 GA 8925: baseline correct -> adjusted wrong, posterior 3.81 -> -6.19, shrunk PV 0.00

## Decision

Adopt only if combined adjusted direction accuracy exceeds 94/99 with parameters selected strictly from earlier cycles.

## Outputs

- experiments/outparty_favored/results/favored_summary.csv
- experiments/outparty_favored/results/favored_choices.csv
- experiments/outparty_favored/results/favored_predictions.csv
