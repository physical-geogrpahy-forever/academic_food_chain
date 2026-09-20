# OutPartyIncumbent + PersonalVote post-poll direction experiment

- Generated UTC: 2026-09-20T17:46:44.763356+00:00
- Baseline: fixed Core V2 poll blend, 94/99 = 94.9%.
- Adjustment is applied only to out-party incumbents and optionally only when posterior margin is within a learned threshold.
- Out-party penalty moves toward the state-favored party.
- Incumbent PersonalVote protects candidates with demonstrated prior overperformance.
- 2018 parameters are learned from 2014 only; 2022 parameters are learned from 2014+2018; 2014 receives no learned adjustment.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 93 | 93.9% | -1 | 7 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 30 | 90.9% | +1 | 5 |
| 2022 | 33 | 33 | 100.0% | 31 | 93.9% | -2 | 2 |

## Selected parameters

| test | gamma out-party | delta personal | personal k | posterior threshold | train accuracy | train flips |
|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 0 | 0 | 1 | 999 | NA | 0 |
| 2018 | 6 | 0 | 0.5 | 999 | 100.0% | 1 |
| 2022 | 6 | 0.1 | 0.5 | 999 | 98.5% | 4 |

## Correctness changes

- 2018 NV 112: baseline wrong -> adjusted correct, posterior -0.62 -> 5.38
- 2018 MO 109: baseline wrong -> adjusted correct, posterior 4.72 -> -1.28
- 2018 MT 110: baseline correct -> adjusted wrong, posterior 5.59 -> -0.41
- 2018 WV 126: baseline correct -> adjusted wrong, posterior 4.74 -> -1.26
- 2018 IN 102: baseline wrong -> adjusted correct, posterior 5.41 -> -0.59
- 2022 NV 8937: baseline correct -> adjusted wrong, posterior 2.39 -> -3.49
- 2022 GA 8925: baseline correct -> adjusted wrong, posterior 3.81 -> -2.19

## Decision

Adopt only if combined adjusted direction accuracy exceeds 94/99 and the gain comes from parameters selected on earlier cycles only.

## Outputs

- experiments/outparty_personal/results/outparty_personal_summary.csv
- experiments/outparty_personal/results/outparty_personal_choices.csv
- experiments/outparty_personal/results/outparty_personal_predictions.csv
