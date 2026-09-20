# Pollster house-effect direction experiment

- Generated UTC: 2026-09-20T17:42:12.574405+00:00
- Primary metric: winner-direction accuracy.
- Pollster house effects use only Senate poll errors from cycles before each test cycle.
- Pollster errors are first averaged within pollster-race to avoid overweighting repeated polls.
- Shrinkage strength is selected from earlier-cycle poll direction accuracy only.

## Result

| scope | N | correct | wrong | accuracy | poll-covered |
|---|---:|---:|---:|---:|---:|
| combined | 99 | 92 | 7 | 92.9% | 64 |
| 2014 | 33 | 30 | 3 | 90.9% | 20 |
| 2018 | 33 | 29 | 4 | 87.9% | 23 |
| 2022 | 33 | 33 | 0 | 100.0% | 21 |

## Selected adjustment by outer cycle

| test | mode | k | inner poll accuracy | inner poll MAE | prior poll races |
|---:|---|---:|---:|---:|---:|
| 2014 | pollster | 50.0 | 98.7% | 6.39 | 76 |
| 2018 | pollster | 1.0 | 91.3% | 6.27 | 115 |
| 2022 | pollster | 1.0 | 91.0% | 5.81 | 156 |

## Remaining wrong races

- 2014 CO 23: posterior=0.24, actual=-2.06
- 2014 IA 26: posterior=0.53, actual=-8.70
- 2014 NC 14: posterior=6.44, actual=-1.63
- 2018 NV 112: posterior=-1.90, actual=5.25
- 2018 MO 109: posterior=4.20, actual=-6.00
- 2018 FL 100: posterior=8.69, actual=-0.12
- 2018 IN 102: posterior=3.67, actual=-6.16

## Benchmark

- Fixed unadjusted poll blend benchmark: 94/99 = 94.9%.
- Keep pollster adjustment only if it exceeds 94/99 without outer-cycle tuning.

## Outputs

- experiments/poll_house_effect/results/house_effect_summary.csv
- experiments/poll_house_effect/results/house_effect_choices.csv
- experiments/poll_house_effect/results/house_effect_predictions.csv
