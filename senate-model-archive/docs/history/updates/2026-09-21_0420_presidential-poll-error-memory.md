# Previous-presidential state polling-error memory

- Generated UTC: 2026-09-20T18:27:27.967146+00:00
- Primary metric: Senate winner-direction accuracy.
- 2010 Senate races use 2008 presidential state polling error, 2014 uses 2012, and 2018 uses 2016.
- For each target midterm, gamma and raw-vs-centered state error are selected only from earlier eligible midterms.
- 2022 is deliberately left unchanged in this first-stage test because the 2020 polling-average archive is not part of the pinned 1968-2016 file.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 93 | 93.9% | -1 | 1 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 28 | 84.8% | -1 | 1 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected memory rule

| test | mode | gamma | inner N | inner accuracy | inner MAE |
|---:|---|---:|---:|---:|---:|
| 2014 | centered | -0.5 | 35 | 82.9% | 12.90 |
| 2018 | centered | -0.5 | 68 | 89.7% | 9.81 |
| 2022 | none | 0.0 | 0 | NA | NA |

## Correctness changes

- 2018 TN 120: baseline correct -> adjusted wrong, memory=-13.938142672941172, correction=6.97, posterior -4.28->0.43

## Previously unresolved five

- 2014 NC: WRONG, actual=-1.63, baseline=5.44, memory=-0.6123339500000029, correction=0.31, adjusted=5.65
- 2018 NV: WRONG, actual=5.25, baseline=-0.62, memory=6.0378622570588245, correction=-3.02, adjusted=-2.55
- 2018 MO: WRONG, actual=-6.00, baseline=4.72, memory=-3.3951085729411767, correction=1.70, adjusted=5.80
- 2018 FL: WRONG, actual=-0.12, baseline=9.21, memory=1.973412467058826, correction=-0.99, adjusted=8.52
- 2018 IN: WRONG, actual=-6.16, baseline=5.41, memory=-3.172365632941177, correction=1.59, adjusted=6.35

## Decision

- Current accepted benchmark: 94/99.
- This signal is worth continuing only if it increases correct winners without test-cycle parameter tuning. If it improves 2018, the next step is to add the archived 2020 presidential polling average and validate 2022 under the same rule.

## Outputs

- experiments/pres_poll_error_memory/results/pres_error_summary.csv
- experiments/pres_poll_error_memory/results/pres_error_choices.csv
- experiments/pres_poll_error_memory/results/pres_error_predictions.csv
- experiments/pres_poll_error_memory/results/pres_error_audit.csv
