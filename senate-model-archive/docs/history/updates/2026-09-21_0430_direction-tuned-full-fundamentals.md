# Direction-tuned full fundamentals

- Generated UTC: 2026-09-20T18:32:54.143270+00:00
- This corrects the objective mismatch in the previous 94/99 baseline: the prior model hyperparameters had been selected by RMSE even after winner-direction became the primary goal.
- All structure/ridge choices here are selected by chronological inner OOS winner count AFTER the fixed 45-day poll blend.
- SameSeat is optional; the selector may drop it entirely.
- Ties use Brier score, then posterior MAE, then model simplicity and stronger shrinkage.

## Result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 93 | 6 | 93.9% |
| 2014 | 33 | 31 | 2 | 93.9% |
| 2018 | 33 | 29 | 4 | 87.9% |
| 2022 | 33 | 33 | 0 | 100.0% |

## Selected model by outer cycle

| test | features | PVI ridge | local ridge | context ridge | incumbent ridge | era ridge | inner accuracy | Brier | posterior MAE |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | pvi_same_context_incera | 16.0 | 64.0 | 64.0 | 256.0 | 1024.0 | 91.7% | 0.098 | 10.60 |
| 2018 | pvi_same_context_incera | 16.0 | 64.0 | 64.0 | 256.0 | 1024.0 | 91.9% | 0.082 | 9.41 |
| 2022 | pvi_same_context_allera | 16.0 | 16.0 | 16.0 | 256.0 | 1024.0 | 92.0% | 0.079 | 8.30 |

## Remaining wrong races

- 2014 IA race 26: actual=-8.70, prior=5.06, poll=-0.7570233711596389, posterior=1.07, model=pvi_same_context_incera
- 2014 NC race 14: actual=-1.63, prior=7.53, poll=4.155797368429281, posterior=5.16, model=pvi_same_context_incera
- 2018 NV race 112: actual=5.25, prior=-0.39, poll=-0.5256927411932983, posterior=-0.48, model=pvi_same_context_incera
- 2018 MO race 109: actual=-6.00, prior=11.80, poll=-0.566102263865442, posterior=3.91, model=pvi_same_context_incera
- 2018 FL race 100: actual=-0.12, prior=21.38, poll=1.651366682611031, posterior=7.51, model=pvi_same_context_incera
- 2018 IN race 102: actual=-6.16, prior=8.68, poll=0.6879242338141337, posterior=3.96, model=pvi_same_context_incera

## Previously unresolved five

- 2014 NC: WRONG, actual=-1.63, prior=7.53, posterior=5.16, PVI=-6.33, SameSeat=8.75, OutParty=1.0
- 2018 NV: WRONG, actual=5.25, prior=-0.39, posterior=-0.48, PVI=1.20, SameSeat=-1.28, OutParty=-1.0
- 2018 MO: WRONG, actual=-6.00, prior=11.80, posterior=3.91, PVI=-19.10, SameSeat=16.72, OutParty=1.0
- 2018 FL: WRONG, actual=-0.12, prior=21.38, posterior=7.51, PVI=-3.32, SameSeat=13.35, OutParty=1.0
- 2018 IN: WRONG, actual=-6.16, prior=8.68, posterior=3.96, PVI=-19.77, SameSeat=6.11, OutParty=1.0

## Benchmark

- Current accepted fixed-poll baseline: 94/99 = 94.9%.
- Adopt this model only if it exceeds 94/99 under the same 99-race OOS universe.

## Outputs

- experiments/direction_tuned_fundamentals/results/direction_tuned_summary.csv
- experiments/direction_tuned_fundamentals/results/direction_tuned_choices.csv
- experiments/direction_tuned_fundamentals/results/direction_tuned_predictions.csv
