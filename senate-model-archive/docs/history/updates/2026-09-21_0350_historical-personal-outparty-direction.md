# Historical PersonalVote + OutPartyIncumbent direction experiment

- Generated UTC: 2026-09-20T17:50:06.220867+00:00
- Baseline: fixed 45-day poll blend at 94/99.
- Candidate PersonalVote is reconstructed for historical Senate candidates from prior completed Senate races.
- Prior candidate overperformance = candidate-side residual from PVI after subtracting the same-cycle mean Senate residual.
- Only races before the target cycle enter each candidate personal history.
- Out-party penalty, personal protection, hostility interaction, shrinkage, and posterior threshold are selected using earlier cycles only.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 | 0 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected parameters

| test | gamma | personal delta | k | threshold | hostility slope | train accuracy | flips |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 1 | 0 | 0.5 | 999 | 0 | 84.4% | 1 |
| 2018 | 1 | 0.75 | 0.5 | 2 | 0 | 88.8% | 2 |
| 2022 | 2 | 0.75 | 8 | 999 | 0 | 89.4% | 3 |

## Correctness changes


## Decision

- Combined adjusted result: 94/99 = 94.9%.
- Adopt only if this exceeds 94/99 and the gain survives cycle-by-cycle inspection.

## Outputs

- experiments/historical_personal_outparty/results/historical_personal_summary.csv
- experiments/historical_personal_outparty/results/historical_personal_choices.csv
- experiments/historical_personal_outparty/results/historical_personal_predictions.csv
