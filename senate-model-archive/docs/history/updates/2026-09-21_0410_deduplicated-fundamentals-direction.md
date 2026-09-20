# De-duplicated fundamentals direction experiment

- Generated UTC: 2026-09-20T18:21:26.177494+00:00
- Primary objective: winner-direction accuracy after the fixed 45-day poll blend.
- This rebuild changes the fundamentals themselves rather than applying a post-hoc correction.

## De-duplication

1. SameSeat raw margin is replaced by a residual after removing the prior-cycle state PVI and the Senate cycle mean residual.
2. Senate candidate PersonalVote excludes the exact prior same-seat race used by SameSeat, preventing the same incumbent performance from entering twice.
3. Prior House candidate quality is measured as candidate-side district overperformance relative to the same district two years earlier after adjusting for the national House swing.
4. Prior governor candidate quality is measured as candidate-side gubernatorial residual from state PVI and the governor-cycle mean.
5. Incumbency and OutPartyIncumbent remain current-office effects rather than proxies for the prior election result.

## Result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 93 | 6 | 93.9% |
| 2014 | 33 | 31 | 2 | 93.9% |
| 2018 | 33 | 29 | 4 | 87.9% |
| 2022 | 33 | 33 | 0 | 100.0% |

## Selected model by outer cycle

| test | features | local ridge | context ridge | incumbent ridge | candidate ridge | inner accuracy | post MAE |
|---:|---|---:|---:|---:|---:|---:|---:|
| 2014 | raw_core | 16.0 | 64.0 | 256.0 | 4.0 | 89.6% | 10.36 |
| 2018 | resid_all_candidate | 16.0 | 1.0 | 256.0 | 256.0 | 90.7% | 9.06 |
| 2022 | raw_core | 16.0 | 64.0 | 256.0 | 4.0 | 91.2% | 8.07 |

## Remaining wrong races

- 2014 IA race 26: actual=-8.70, prior=7.03, poll=-0.7570233711596389, posterior=1.69, features=raw_core
- 2014 NC race 14: actual=-1.63, prior=5.45, poll=4.155797368429281, posterior=4.54, features=raw_core
- 2018 NV race 112: actual=5.25, prior=0.41, poll=-0.5256927411932983, posterior=-0.19, features=resid_all_candidate
- 2018 MO race 109: actual=-6.00, prior=10.10, poll=-0.566102263865442, posterior=3.30, features=resid_all_candidate
- 2018 FL race 100: actual=-0.12, prior=26.46, poll=1.651366682611031, posterior=9.01, features=resid_all_candidate
- 2018 IN race 102: actual=-6.16, prior=7.75, poll=0.6879242338141337, posterior=3.58, features=resid_all_candidate

## Five previously unresolved races

- 2014 NC: WRONG, actual=-1.63, prior=5.45, posterior=4.54, SameSeatResidual=8.09, SenatePV=0.00, HousePV=0.00, GovPV=0.00
- 2018 NV: WRONG, actual=5.25, prior=0.41, posterior=-0.19, SameSeatResidual=-14.44, SenatePV=0.00, HousePV=8.02, GovPV=0.00
- 2018 MO: WRONG, actual=-6.00, prior=10.10, posterior=3.30, SameSeatResidual=13.72, SenatePV=-2.27, HousePV=0.00, GovPV=0.00
- 2018 FL: WRONG, actual=-0.12, prior=26.46, posterior=9.01, SameSeatResidual=7.64, SenatePV=3.61, HousePV=24.55, GovPV=4.39
- 2018 IN: WRONG, actual=-6.16, prior=7.75, posterior=3.58, SameSeatResidual=6.82, SenatePV=0.00, HousePV=-0.08, GovPV=0.00

## Benchmark

- Current accepted direction benchmark: fixed-poll reconstruction 94/99 = 94.9%.
- Adopt this rebuilt fundamentals architecture only if it exceeds 94/99 under chronological nested OOS.

## Outputs

- experiments/deduplicated_fundamentals/results/deduplicated_summary.csv
- experiments/deduplicated_fundamentals/results/deduplicated_choices.csv
- experiments/deduplicated_fundamentals/results/deduplicated_predictions.csv
- experiments/deduplicated_fundamentals/results/deduplicated_feature_audit.csv
