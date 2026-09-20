# External 538 direction headroom diagnostic

- Generated UTC: 2026-09-20T18:18:18.203933+00:00
- Diagnostic only. No external forecast is adopted here.
- Uses only 45-day-or-earlier archived 2018 and 2022 model outputs.
- Purpose: determine whether external lite/classic/deluxe direction contains information capable of correcting the current 94/99 baseline errors.

- 2018 snapshot: 2018-09-22
- 2022 snapshot: 2022-09-24

## Accuracy by external model

| cycle | model | N | correct | accuracy |
|---:|---|---:|---:|---:|
| 2018 | baseline | 33 | 29 | 87.9% |
| 2018 | lite | 32 | 27 | 84.4% |
| 2018 | classic | 32 | 27 | 84.4% |
| 2018 | deluxe | 32 | 27 | 84.4% |
| 2022 | baseline | 33 | 33 | 100.0% |
| 2022 | lite | 33 | 30 | 90.9% |
| 2022 | classic | 33 | 32 | 97.0% |
| 2022 | deluxe | 33 | 33 | 100.0% |

## Current baseline errors and external direction

| cycle | state | actual | baseline | lite | classic | deluxe |
|---:|---|---:|---:|---:|---:|---:|
| 2018 | NV | 5.25 | -0.62 | 0.88 | 0.72 | 1.10 |
| 2018 | MO | -6.00 | 4.72 | 0.92 | 2.23 | 2.09 |
| 2018 | FL | -0.12 | 9.21 | 0.28 | 1.34 | 1.50 |
| 2018 | IN | -6.16 | 5.41 | 2.71 | 5.37 | 4.19 |

## Interpretation

If external directions fail on the same races, this source family has no useful directional headroom. If they correctly distinguish some current errors, a leakage-free ensemble gate can be tested separately.

## Outputs

- experiments/external_538_direction/results/external_direction_summary.csv
- experiments/external_538_direction/results/external_direction_races.csv
- experiments/external_538_direction/results/baseline_wrong_external_signals.csv
