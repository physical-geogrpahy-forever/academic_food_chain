# Performance experiment: presidential approval National proxy on 99 rows

- Generated UTC: 2026-09-20T17:20:43.044063+00:00
- Baseline: PVI + last-prior SameSeat + year gap.
- National inputs are fixed at 45 days before each federal general election.
- signed_net_approval = president-party sign in D-minus-R direction multiplied by net approval.

## Results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| baseline | 99 | 10.6055 | 7.8754 | 87.9% |
| approval_signed_fixed | 99 | 30.0112 | 22.6723 | 77.8% |
| approval_plus_party_fixed | 99 | 17.8834 | 13.4758 | 79.8% |
| approval_nested | 99 | 10.3101 | 7.8846 | 85.9% |

## Decision

- Best National architecture: approval_nested.
- Improvement versus 99-row baseline: +0.2954 RMSE points.
- Decision: KEEP_APPROVAL_NATIONAL.

## Next

If kept, use this National structure as the new structural baseline and test RelativeEconomicGrowth next. Candidate blocks remain excluded unless they improve the stronger baseline.

## Outputs

- performance/results/approval_national_99row_summary.csv
- performance/results/approval_national_99row_hyperparams.csv
- performance/results/approval_national_99row_predictions.csv
