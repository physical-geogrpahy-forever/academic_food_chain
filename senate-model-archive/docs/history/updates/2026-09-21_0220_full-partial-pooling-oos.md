# Full partial-pooling performance experiment

- Generated UTC: 2026-09-20T17:22:06.904273+00:00
- 99 preserved headline rows for 2014, 2018, 2022.
- Structural base: PVI + last-prior SameSeat + gap + signed relative income growth + 45-day generic ballot.
- Candidate groups: incumbency/out-party, prior elected-office experience, PersonalVote.
- All optional groups are selected only inside chronological inner OOS and use shared ridge shrinkage.

## Results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| base_nested | 99 | 9.7295 | 7.3701 | 88.9% |
| full_nested | 99 | 11.0542 | 8.7952 | 89.9% |

## Choices by outer cycle

| cycle | variant | groups | lambda N | lambda econ | lambda local | personal k | inner RMSE |
|---:|---|---|---:|---:|---:|---:|---:|
| 2014 | base_nested | NONE | 1024.0 | 16.0 | 64.0 | 16.0 | 30.1202 |
| 2014 | full_nested | inc;exp | 16.0 | 0.0 | 16.0 | 16.0 | 27.2563 |
| 2018 | base_nested | NONE | 16.0 | 16.0 | 64.0 | 16.0 | 22.5894 |
| 2018 | full_nested | inc | 16.0 | 0.0 | 16.0 | 16.0 | 20.6021 |
| 2022 | base_nested | NONE | 64.0 | 16.0 | 64.0 | 16.0 | 18.8162 |
| 2022 | full_nested | inc | 64.0 | 0.0 | 16.0 | 16.0 | 18.0148 |

## Decision

- Candidate/PersonalVote increment versus nested strong base: -1.3248 RMSE points.
- Decision: REJECT_FULL_LOCAL_BLOCK.
- Economic data remain revised-vintage diagnostic until historical release vintages are substituted.

## Outputs

- performance/results/full_partial_pooling_summary.csv
- performance/results/full_partial_pooling_choices.csv
- performance/results/full_partial_pooling_predictions.csv
