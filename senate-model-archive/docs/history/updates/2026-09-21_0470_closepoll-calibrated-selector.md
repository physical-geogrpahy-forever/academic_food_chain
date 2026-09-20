# Calibrated selector for out-party close-poll PVI rule

- Generated UTC: 2026-09-20T18:51:13.995118+00:00
- Fixes a methodological inconsistency in the previous selector.
- Project decision order is direction accuracy first, then Brier/log loss, then MAE.
- Previous close-poll selector incorrectly used fewer overrides as the first tie-break.
- For an override, the posterior magnitude is preserved and only its sign is set to the PVI direction, enabling consistent Brier/log-loss/MAE comparison.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 96 | 97.0% | +2 | 6 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 32 | 97.0% | +3 | 5 |
| 2022 | 33 | 33 | 100.0% | 32 | 97.0% | -1 | 1 |

## Strictly prior-cycle selected threshold

| test | threshold | train correct | train accuracy | Brier | log loss | MAE | flips |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | -1 | 80 | 83.3% | 0.1161 | 0.4023 | 10.69 | 0 |
| 2018 | 5.0 | 141 | 87.6% | 0.0890 | 0.3092 | 9.21 | 6 |
| 2022 | 2.0 | 202 | 89.4% | 0.0779 | 0.2715 | 8.34 | 9 |

## Correctness changes

- 2018 NV 112: baseline wrong -> adjusted correct, poll=-0.5256927411932983, PVI=1.20, threshold=5.0
- 2018 MO 109: baseline wrong -> adjusted correct, poll=-0.566102263865442, PVI=-19.10, threshold=5.0
- 2018 MT 110: baseline correct -> adjusted wrong, poll=3.4041817614524206, PVI=-22.31, threshold=5.0
- 2018 FL 100: baseline wrong -> adjusted correct, poll=1.651366682611031, PVI=-3.32, threshold=5.0
- 2018 IN 102: baseline wrong -> adjusted correct, poll=0.6879242338141337, PVI=-19.77, threshold=5.0
- 2022 NV 8937: baseline correct -> adjusted wrong, poll=-1.5004737646641886, PVI=-1.28, threshold=2.0

## Decision

- If this prior-cycle selector chooses a nonzero threshold and exceeds 94/99, it qualifies as a clean nested improvement under the declared metric hierarchy.
- Otherwise the fixed 1.0pp 97/99 result remains post-hoc only.

## Outputs

- experiments/outparty_closepoll_calibrated/results/calibrated_summary.csv
- experiments/outparty_closepoll_calibrated/results/calibrated_choices.csv
- experiments/outparty_closepoll_calibrated/results/calibrated_predictions.csv
