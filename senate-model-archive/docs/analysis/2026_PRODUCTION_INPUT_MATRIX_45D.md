# 2026 production input matrix at exact 45-day cutoff

- Cutoff: 2026-09-19 US date.
- PersonalVote uses prior Senate and Governor general elections only.
- Candidate-side overperformance = D/R-side residual from state PVI after subtracting the same-cycle mean residual.
- PersonalVote is shrunk with k=2 for the audit column.
- FEC finance uses official 2026 18-month Top-50 tables through June 30. Missing Top-50 membership is not converted to zero.
- FEC remains an auxiliary diagnostic because it was not adopted as a production direction modifier in historical OOS.
- Poll recency values are cutoff diagnostics with equal-sample assumption because RCP feed does not provide sample sizes.

## Candidate PersonalVote

| State | D PV | n | R PV | n | D-R shrunk PV |
|---|---:|---:|---:|---:|---:|
| AK | 0.00 | 0 | -10.45 | 2 | 5.23 |
| GA | 1.88 | 1 | 0.00 | 0 | 0.63 |
| IA | 0.00 | 0 | 0.00 | 0 | 0.00 |
| ME | 0.00 | 0 | 36.88 | 3 | -22.13 |
| MI | 0.00 | 0 | -2.18 | 1 | 0.73 |
| NH | 0.00 | 0 | 7.35 | 1 | -2.45 |
| NC | 12.45 | 2 | 0.00 | 0 | 6.22 |
| OH | 3.46 | 4 | 0.00 | 0 | 2.30 |
| TX | 0.00 | 0 | 0.00 | 0 | 0.00 |

## Complete input rows

The full machine-readable matrix is data/snapshots/2026_production_input_matrix_45d.csv.

## Important separation

- Locked model inputs: PVI, SameSeat, incumbency, OutPartyIncumbent, experience, PersonalVote, RelativeEconomicGrowth, National, 45-day poll layer.
- Auxiliary diagnostics only: FEC finance shares and third-party uncertainty flag.
- No 2026 election outcome is used anywhere in these inputs.
