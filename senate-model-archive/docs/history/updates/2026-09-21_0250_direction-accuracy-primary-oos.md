# Primary-objective experiment: Senate direction accuracy OOS

- Generated UTC: 2026-09-20T17:30:46.069304+00:00
- Primary objective is win/loss direction accuracy, not margin RMSE.
- Hyperparameters and model family are selected using chronological inner OOS direction accuracy.
- Tie-breakers are lower log loss, lower Brier score, then simpler architecture.

## Combined result

| N | correct | wrong | direction accuracy | Brier | log loss |
|---:|---:|---:|---:|---:|---:|
| 99 | 87 | 12 | 87.9% | 0.0986 | 0.3401 |

## By cycle

| cycle | N | correct | wrong | accuracy |
|---:|---:|---:|---:|---:|
| 2014 | 33 | 28 | 5 | 84.8% |
| 2018 | 33 | 28 | 5 | 84.8% |
| 2022 | 33 | 31 | 2 | 93.9% |

## Outer-fold selected models

| test | model | architecture | lambda | inner accuracy | inner log loss |
|---:|---|---|---:|---:|---:|
| 2014 | margin | pvi_local_national | 16.0 | 82.4% | 0.4973 |
| 2018 | margin | pvi_local_national | 16.0 | 84.4% | 0.4487 |
| 2022 | margin | pvi_local_national | 1.0 | 85.8% | 0.4126 |

## Benchmarks

- Preserved Core V2 fundamentals direction accuracy: 90.9%.
- Preserved Core V2 + poll direction accuracy: 91.9%.
- New model is considered better on the primary task only if it exceeds those comparable direction benchmarks without test-fold tuning.

## Misclassified historical races

- 2014 CO 23: actual R, predicted D, P(D)=0.515
- 2014 IA 26: actual R, predicted D, P(D)=0.595
- 2014 MT 5: actual R, predicted D, P(D)=0.548
- 2014 NH 8: actual D, predicted R, P(D)=0.496
- 2014 MN 6: actual D, predicted R, P(D)=0.477
- 2018 MO 109: actual R, predicted D, P(D)=0.606
- 2018 MT 110: actual D, predicted R, P(D)=0.499
- 2018 WV 126: actual D, predicted R, P(D)=0.413
- 2018 FL 100: actual R, predicted D, P(D)=0.738
- 2018 IN 102: actual R, predicted D, P(D)=0.539
- 2022 PA 8945: actual D, predicted R, P(D)=0.458
- 2022 GA 8925: actual D, predicted R, P(D)=0.354

## Outputs

- experiments/direction_accuracy/results/direction_summary.csv
- experiments/direction_accuracy/results/direction_choices.csv
- experiments/direction_accuracy/results/direction_predictions.csv
