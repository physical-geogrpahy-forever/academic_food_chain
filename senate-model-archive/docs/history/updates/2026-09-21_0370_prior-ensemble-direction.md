# Rolling prior-ensemble direction experiment

- Generated UTC: 2026-09-20T18:01:10.463875+00:00
- Candidate priors: current fullcycle incumbency-era prior and nested PVI/SameSeat prior.
- Same fixed 45-day poll layer is applied after prior ensembling.
- Ensemble weight for each outer cycle is selected only from earlier cycles.
- Primary selection criterion is winner-direction correct count; MAE is only the first tie-breaker.

## Result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 92 | 7 | 92.9% |
| 2014 | 33 | 31 | 2 | 93.9% |
| 2018 | 33 | 29 | 4 | 87.9% |
| 2022 | 33 | 32 | 1 | 97.0% |

## Selected ensemble weights

| test | inc prior weight | seat prior weight | training rows | training accuracy | training MAE |
|---:|---:|---:|---:|---:|---:|
| 2014 | 0.50 | 0.50 | 68 | 85.3% | 10.30 |
| 2018 | 0.90 | 0.10 | 133 | 89.5% | 8.65 |
| 2022 | 0.00 | 1.00 | 198 | 90.4% | 7.84 |

## Remaining wrong races

- 2014 IA 26: posterior=0.02, actual=-8.70
- 2014 NC 14: posterior=3.21, actual=-1.63
- 2018 NV 112: posterior=-0.10, actual=5.25
- 2018 MO 109: posterior=4.24, actual=-6.00
- 2018 FL 100: posterior=8.83, actual=-0.12
- 2018 IN 102: posterior=4.82, actual=-6.16
- 2022 NV 8937: posterior=-1.09, actual=0.80

## Benchmarks

- Current validated fixed-blend benchmark: 94/99 = 94.9%.
- Descriptive 75% inc-era + 25% seat-prior blend: 95/99, but that weight was discovered on the outer sample and is not adopted unless rolling selection reproduces the gain.

## Decision

- Rolling-selected ensemble result: 92/99 = 92.9%.
- Adopt only if it exceeds 94/99.

## Outputs

- experiments/prior_ensemble/results/ensemble_summary.csv
- experiments/prior_ensemble/results/ensemble_choices.csv
- experiments/prior_ensemble/results/ensemble_predictions.csv
