# Selective poll override direction experiment

- Generated UTC: 2026-09-20T17:44:23.907836+00:00
- Baseline is the fixed Core V2 poll blend at 94/99.
- Only races where baseline posterior direction and poll direction disagree are eligible for an override.
- The override rule for each outer cycle is selected only from earlier cycles.
- Primary selection criterion is number of correct winners. Ties prefer fewer overrides, then simpler rules.

## Result

| scope | N | baseline correct | baseline acc | override correct | override acc | net | overrides |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 | 0 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected rules

| test | rule | prior rows | prior accuracy | train flips |
|---:|---|---:|---:|---:|
| 2014 | abspoll_ge_1 | 96 | 89.6% | 8 |
| 2018 | abspoll_ge_3 | 161 | 90.1% | 4 |
| 2022 | abspoll_ge_3 | 226 | 89.8% | 4 |

## Changed correctness


## Decision

Adopt only if the selective override exceeds 94/99 without using the outer test outcome in rule selection.

## Outputs

- experiments/selective_poll_override/results/override_summary.csv
- experiments/selective_poll_override/results/override_choices.csv
- experiments/selective_poll_override/results/override_predictions.csv
