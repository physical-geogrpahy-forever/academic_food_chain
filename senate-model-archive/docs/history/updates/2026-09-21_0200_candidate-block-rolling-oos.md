# Performance experiment: candidate-block rolling OOS

- Generated UTC: 2026-09-20T17:00:47.988164+00:00
- Training is strictly chronological: 2014<-2006/2010; 2018<-earlier cycles; 2022<-earlier cycles.
- Historical panel rows after required PVI + same-seat coverage: 153
- Modern validation rows retained: 91
- Dropped rows for missing PVI/same-seat: 15

## Combined modern OOS results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| structural_only | 91 | 11.1097 | 8.4058 | 85.7% |
| candidate_fixed | 91 | 12.0664 | 9.1801 | 87.9% |
| candidate_ridge_nested | 91 | 11.9132 | 8.9331 | 87.9% |
| candidate_subset_nested | 91 | 12.9710 | 9.6580 | 87.9% |

## Decision

- Nested candidate ridge improvement vs unregularized candidate block: +0.1533 RMSE points.
- Nested candidate ridge improvement vs structural-only diagnostic: -0.8035 RMSE points.
- Decision: REJECT_RIDGE_CANDIDATE_BLOCK
- Nested subset-selection improvement vs structural-only diagnostic: -1.8613 RMSE points.
- Subset decision: REJECT_SUBSET_ARCHITECTURE

## Important limitation

This is a focused candidate-block performance experiment, not the complete preserved Core V2 reconstruction. National_t, RelativeEconomicGrowth, poll updating, and final PersonalVoteDiff are intentionally absent. Therefore its absolute RMSE must not be compared as if it were the preserved Core V2 7.99%p fundamentals benchmark. The valid comparison here is fixed candidate coefficients versus nested OOS candidate-block shrinkage under an identical structural base.

## Next performance step

If candidate-block ridge improves OOS, carry that shrinkage architecture into the full Core V2-R model and add PersonalVote with nested count-based shrinkage. If it does not, discard it rather than preserving it for methodological elegance.

## Outputs

- performance/results/candidate_block_oos_panel.csv
- performance/results/candidate_block_oos_predictions.csv
- performance/results/candidate_block_oos_summary.csv
- performance/results/candidate_block_oos_hyperparams.csv

## Dropped rows

- 2010 DE race 1513: missing_same_seat
- 2010 NY race 1531: missing_same_seat
- 2010 LA race 1524: missing_same_seat
- 2010 WV race 1543: missing_same_seat
- 2010 ID race 1517: missing_same_seat
- 2010 MA race 1526: missing_same_seat
- 2006 AZ race 1581: missing_same_seat
- 2014 AR race 32: missing_same_seat
- 2014 HI race 34: missing_same_seat
- 2014 OK race 35: missing_same_seat
- 2014 SC race 36: missing_same_seat
- 2018 MN race 129: missing_same_seat
- 2022 CA race 9480: missing_same_seat
- 2022 CA race 8921: missing_same_seat
- 2022 OK race 9482: missing_same_seat
