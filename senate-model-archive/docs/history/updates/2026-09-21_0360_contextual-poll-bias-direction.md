# Contextual Senate poll-bias direction experiment

- Generated UTC: 2026-09-20T17:53:17.523545+00:00
- Baseline: fixed 45-day Core V2 poll blend, 94/99.
- Poll bias models are trained only on poll-covered races in cycles before each test cycle.
- Candidate predictors: PVI, absolute PVI, out-party-incumbent status, and fundamentals-poll gap.
- Model family and ridge strength are selected by chronological inner OOS winner-direction accuracy; poll MAE is only the first tie-breaker.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 90 | 90.9% | -4 | 4 |
| 2014 | 33 | 32 | 97.0% | 29 | 87.9% | -3 | 3 |
| 2018 | 33 | 29 | 87.9% | 28 | 84.8% | -1 | 1 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected bias model

| test | features | lambda | inner accuracy | inner poll MAE | train poll rows |
|---:|---|---:|---:|---:|---:|
| 2014 | full | 0.0 | 87.9% | 5.77 | 71 |
| 2018 | pvi_gap | 0.0 | 90.8% | 7.24 | 110 |
| 2022 | pvi | 0.0 | 91.4% | 6.53 | 151 |

## Correctness changes

- 2014 CO 23: baseline correct -> adjusted wrong, bias=-1.58
- 2014 IA 26: baseline correct -> adjusted wrong, bias=-2.13
- 2014 AK 12: baseline correct -> adjusted wrong, bias=-6.28
- 2018 WV 126: baseline correct -> adjusted wrong, bias=8.47

## Decision

- Combined adjusted result: 90/99 = 90.9%.
- Adopt only if this exceeds 94/99 without outer-cycle tuning.

## Outputs

- experiments/contextual_poll_bias/results/contextual_bias_summary.csv
- experiments/contextual_poll_bias/results/contextual_bias_choices.csv
- experiments/contextual_poll_bias/results/contextual_bias_predictions.csv
