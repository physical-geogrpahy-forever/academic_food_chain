# Rich direction classifier OOS

- Generated UTC: 2026-09-20T17:56:37.203464+00:00
- Primary objective: winner-direction accuracy.
- Candidate model families combine the fixed-poll posterior with poll information, PVI, SameSeat, economy, national environment, incumbency, and OutPartyIncumbent.
- Feature set and ridge strength are selected only by chronological inner OOS before each outer cycle.

## Result

| scope | N | baseline correct | baseline acc | classifier correct | classifier acc | net |
|---|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 89 | 89.9% | -5 |
| 2014 | 33 | 32 | 97.0% | 28 | 84.8% | -4 |
| 2018 | 33 | 29 | 87.9% | 28 | 84.8% | -1 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 |

## Selected models

| test | feature set | lambda | inner accuracy | inner log loss | train N |
|---:|---|---:|---:|---:|---:|
| 2014 | candidate_interactions | 4 | 87.9% | 0.404 | 96 |
| 2018 | candidate | 64 | 88.8% | 0.435 | 161 |
| 2022 | candidate_interactions | 16 | 89.6% | 0.312 | 226 |

## Changed correctness

- 2014 CO 23: baseline correct -> classifier wrong
- 2014 IA 26: baseline correct -> classifier wrong
- 2014 AK 12: baseline correct -> classifier wrong
- 2014 AR 32: baseline correct -> classifier wrong
- 2018 ND 116: baseline correct -> classifier wrong

## Decision

Adopt only if classifier accuracy exceeds 94/99 under the same outer OOS universe.

## Outputs

- experiments/rich_direction_classifier/results/rich_classifier_summary.csv
- experiments/rich_direction_classifier/results/rich_classifier_choices.csv
- experiments/rich_direction_classifier/results/rich_classifier_predictions.csv
