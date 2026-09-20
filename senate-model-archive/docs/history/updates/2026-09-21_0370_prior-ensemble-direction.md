# Rolling prior-ensemble direction experiment

- Generated UTC: 2026-09-20T18:02:56.943016+00:00
- Primary prior: fullcycle incumbency-era rolling OOS prior.
- Secondary prior architecture is frozen from the 2014 fold pre-2014 inner selection: recent presidential lean only, raw SameSeat, ridge PVI=4/local=64/econ=4096/national=0.
- Same fixed 45-day poll layer is applied after prior ensembling.
- Ensemble weight for each outer cycle is selected only from earlier cycles; correct-winner count is primary and MAE is tie-breaker.

## Result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 93 | 6 | 93.9% |
| 2014 | 33 | 31 | 2 | 93.9% |
| 2018 | 33 | 30 | 3 | 90.9% |
| 2022 | 33 | 32 | 1 | 97.0% |

## Selected weights

| test | inc weight | seat/PVI weight | train N | train accuracy | train MAE |
|---:|---:|---:|---:|---:|---:|
| 2014 | 0.25 | 0.75 | 96 | 87.5% | 10.02 |
| 2018 | 0.25 | 0.75 | 161 | 88.8% | 8.91 |
| 2022 | 0.25 | 0.75 | 226 | 89.4% | 7.95 |

## Wrong races

- 2014 IA 26: posterior=0.30, actual=-8.70
- 2014 NC 14: posterior=2.15, actual=-1.63
- 2018 MO 109: posterior=1.15, actual=-6.00
- 2018 FL 100: posterior=6.39, actual=-0.12
- 2018 IN 102: posterior=0.96, actual=-6.16
- 2022 NV 8937: posterior=-0.19, actual=0.80

## Benchmark

- Validated fixed-blend benchmark: 94/99 = 94.9%.
- Descriptive 75/25 blend was 95/99 but is not accepted unless rolling historical weight selection reproduces the gain.

## Decision
- Rolling-selected ensemble: 93/99 = 93.9%.
- Adopt only if it exceeds 94/99.
