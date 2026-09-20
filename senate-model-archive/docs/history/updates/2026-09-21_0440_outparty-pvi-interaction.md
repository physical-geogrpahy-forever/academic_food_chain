# OutPartyIncumbent x PVI interaction experiment

- Generated UTC: 2026-09-20T18:40:39.220454+00:00
- Primary objective: winner-direction accuracy after the fixed 45-day poll blend.
- New structural term: OutPartyIncumbent × |PVI|. A quadratic version and interactions with incumbency/SameSeat are also tested.
- Feature family and ridge strengths are selected only by chronological inner OOS winner count.

## Result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 94 | 5 | 94.9% |
| 2014 | 33 | 31 | 2 | 93.9% |
| 2018 | 33 | 30 | 3 | 90.9% |
| 2022 | 33 | 33 | 0 | 100.0% |

## Selected model

| test | feature set | base ridge | incumbent ridge | interaction ridge | era ridge | inner accuracy | post MAE |
|---:|---|---:|---:|---:|---:|---:|---:|
| 2014 | outparty_pvi_inc | 16.0 | 256.0 | 1024.0 | 1024.0 | 91.7% | 10.15 |
| 2018 | outparty_pvi_inc | 16.0 | 256.0 | 1024.0 | 1024.0 | 91.9% | 9.06 |
| 2022 | outparty_pvi_inc | 16.0 | 256.0 | 1024.0 | 1024.0 | 92.0% | 8.22 |

## Remaining wrong races

- 2014 IA: actual=-8.70, prior=5.14, poll=-0.7570233711596389, posterior=1.10, model=outparty_pvi_inc
- 2014 NC: actual=-1.63, prior=4.77, poll=4.155797368429281, posterior=4.34, model=outparty_pvi_inc
- 2018 MO: actual=-6.00, prior=16.78, poll=-0.566102263865442, posterior=5.71, model=outparty_pvi_inc
- 2018 FL: actual=-0.12, prior=22.90, poll=1.651366682611031, posterior=7.96, model=outparty_pvi_inc
- 2018 IN: actual=-6.16, prior=13.08, poll=0.6879242338141337, posterior=5.76, model=outparty_pvi_inc

## Benchmark

- Current accepted benchmark: 94/99 = 94.9%.
- Adopt only if this interaction model exceeds 94/99 under the same outer OOS universe.

## Outputs

- experiments/outparty_pvi_interaction/results/interaction_summary.csv
- experiments/outparty_pvi_interaction/results/interaction_choices.csv
- experiments/outparty_pvi_interaction/results/interaction_predictions.csv
