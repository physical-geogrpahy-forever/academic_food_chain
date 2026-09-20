# Poll layer diagnostic with fixed Core V2 blend weight

- Generated UTC: 2026-09-20T17:34:05.571787+00:00
- Poll source: https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv
- Parsed Senate poll questions: 1208
- Snapshot date: election day minus 45 days.
- Core V2 blend fixed at w_max=0.75, k=0.5.
- This stage does not tune blend weights on the 2014/2018/2022 test outcomes.

## Combined 99-race direction results

| aggregation | poll-covered | prior correct | prior acc | posterior correct | posterior acc | net correct |
|---|---:|---:|---:|---:|---:|---:|
| w30_h14_all | 64 | 90 | 90.9% | 94 | 94.9% | +4 |
| w45_h14_all | 64 | 90 | 90.9% | 94 | 94.9% | +4 |
| w60_h14_all | 64 | 90 | 90.9% | 94 | 94.9% | +4 |
| w45_equal_all | 64 | 90 | 90.9% | 94 | 94.9% | +4 |
| w45_h14_nonpartisan | 0 | 90 | 90.9% | 90 | 90.9% | +0 |

## Descriptive best fixed aggregation

- w30_h14_all: 94/99 = 94.9%, net +4 correct races versus the same prior.
- This best row is descriptive only. It is not adopted merely because it is best on the outer test set.

## Benchmarks

- Preserved Core V2 fundamentals: 90.9% direction.
- Preserved Core V2 + 45-day poll: 91.9% direction.
- The reconstruction should meet or exceed 91.9% before being considered an improvement on the primary task.

## Outputs

- experiments/poll_direction/results/poll_fixed_summary.csv
- experiments/poll_direction/results/poll_fixed_predictions.csv
- experiments/poll_direction/results/poll_snapshot_45d_reconstructed.csv
