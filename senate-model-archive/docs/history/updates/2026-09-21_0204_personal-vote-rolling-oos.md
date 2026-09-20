# Performance experiment: PersonalVote rolling OOS

- Generated UTC: 2026-09-20T17:05:34.312841+00:00
- Same 91-race modern validation universe as the candidate-block diagnostic.
- 2006/2010 rows have no reconstructed headline PersonalVote sufficient-statistics file and therefore receive the zero prior, not a fabricated score.

## Combined results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| structural_only | 91 | 11.1097 | 8.4058 | 85.7% |
| personal_offset_nested | 91 | 11.2938 | 8.7094 | 83.5% |
| personal_regression_nested | 91 | 11.1702 | 8.6111 | 84.6% |

## Decision

- Personal offset improvement vs structural: -0.1842 RMSE points.
- Personal regression improvement vs structural: -0.0605 RMSE points.
- Best PersonalVote architecture: personal_regression_nested.
- Decision: REJECT_PERSONAL_VOTE_ARCHITECTURE

## Interpretation guard

This experiment tests only whether pre-election candidate overperformance contains transferable OOS signal after count shrinkage. It is still not the complete Core V2 because National_t, RelativeEconomicGrowth, and poll update are absent.

## Outputs

- performance/results/personal_vote_oos_predictions.csv
- performance/results/personal_vote_oos_summary.csv
- performance/results/personal_vote_oos_hyperparams.csv
