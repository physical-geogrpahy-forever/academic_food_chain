# Direction-first nested poll blend optimization

- Generated UTC: 2026-09-20T18:01:03.485317+00:00
- Primary objective: winner-direction accuracy.
- The prior model is unchanged.
- For each outer cycle, poll window, half-life, w_max, and k are selected only from earlier cycles.
- Fixed comparison benchmark is window=30, half-life=14, w_max=0.75, k=0.5, which produced 94/99.

## Result

| scope | N | fixed correct | fixed acc | nested correct | nested acc | net |
|---|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 |

## Selected blend by outer cycle

| test | window | half-life | w_max | k | prior rows | train accuracy | train MAE |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 30 | 14 | 0.9 | 0.1 | 96 | 88.5% | 9.99 |
| 2018 | 14 | 7 | 0.9 | 0.25 | 161 | 90.1% | 8.79 |
| 2022 | 14 | 7 | 0.9 | 0.25 | 226 | 89.8% | 8.14 |

## Correctness changes


## Decision

Adopt only if nested poll blend exceeds 94/99 without using outer-cycle outcomes in parameter selection.

## Outputs

- experiments/poll_blend_direction/results/blend_summary.csv
- experiments/poll_blend_direction/results/blend_choices.csv
- experiments/poll_blend_direction/results/blend_predictions.csv
