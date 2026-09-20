# Split close-poll selector: poll-PVI agreement aware

- Generated UTC: 2026-09-20T19:03:44.409529+00:00
- Primary objective: winner-direction accuracy.
- The override threshold is estimated separately when poll and PVI disagree versus agree.
- When poll and PVI agree, override additionally requires a minimum absolute PVI.
- All parameters for each outer cycle are selected only from earlier cycles.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 96 | 97.0% | +2 | 4 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 31 | 93.9% | +2 | 4 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected parameters

| test | disagree threshold | agree threshold | min abs PVI if agree | train accuracy | Brier | MAE | flips |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | -1 | -1 | 20 | 83.3% | 0.1160 | 10.69 | 0 |
| 2018 | 5.0 | -1 | 20 | 88.8% | 0.0869 | 9.17 | 4 |
| 2022 | 2.0 | 0.75 | 15 | 90.3% | 0.0764 | 8.31 | 7 |

## Correctness changes

- 2018 NV: baseline wrong -> adjusted correct, reason=disagree, poll=-0.5256927411932983, PVI=1.20
- 2018 MT: baseline correct -> adjusted wrong, reason=disagree, poll=3.4041817614524206, PVI=-22.31
- 2018 FL: baseline wrong -> adjusted correct, reason=disagree, poll=1.651366682611031, PVI=-3.32
- 2018 IN: baseline wrong -> adjusted correct, reason=disagree, poll=0.6879242338141337, PVI=-19.77

## Remaining wrong races

- 2014 NC: actual=-1.63, posterior=5.44, poll=4.155797368429281, PVI=-6.33
- 2018 MO: actual=-6.00, posterior=4.72, poll=-0.566102263865442, PVI=-19.10
- 2018 MT: actual=3.66, posterior=5.59, poll=3.4041817614524206, PVI=-22.31

## Benchmark

- Current accepted clean nested benchmark: 96/99 = 97.0%.
- Adopt this split selector only if it exceeds 96/99 under the same 99-race universe.

## Outputs

- experiments/outparty_closepoll_split/results/split_summary.csv
- experiments/outparty_closepoll_split/results/split_choices.csv
- experiments/outparty_closepoll_split/results/split_predictions.csv
