# Performance experiment: SameSeat handling on full 99-row headline sample

- Generated UTC: 2026-09-20T17:16:38.843155+00:00
- Outer validation rows: 99 exactly (2014, 2018, 2022 preserved headline universe).

## Results

| variant | N | RMSE | MAE | direction |
|---|---:|---:|---:|---:|
| struct_exact6_zero_plus_missing | 99 | 11.2838 | 8.5447 | 85.9% |
| struct_last_prior_plus_gap | 99 | 10.6055 | 7.8754 | 87.9% |
| struct_hybrid_exact_else_last | 99 | 10.7314 | 8.0757 | 85.9% |
| nested_joint_sameSeat_plus_candidate | 99 | 12.5015 | 9.2497 | 87.9% |

## Nested choices by outer cycle

| test cycle | SameSeat encoding | candidate features | lambda | inner RMSE |
|---:|---|---|---:|---:|
| 2014 | hybrid_exact_else_last | outparty;gov_exp_diff;house_exp_diff | 0.0 | 26.3312 |
| 2018 | last_prior_plus_gap | outparty;house_exp_diff | 0.0 | 20.7237 |
| 2022 | last_prior_plus_gap | outparty;sen_exp_diff;house_exp_diff | 4.0 | 18.1927 |

## Decision

- Best structural SameSeat encoding: struct_last_prior_plus_gap with RMSE 10.6055.
- Joint nested selection RMSE: 12.5015.
- Joint improvement versus best no-candidate structural encoding: -1.8960 RMSE points.
- Keep candidate augmentation only if the improvement is positive. Otherwise use the best SameSeat structural encoding and move to National/economic/personal-vote terms.

## Why this supersedes the 91-row candidate experiment

The prior experiment dropped 8 headline races because it required an exact six-year SameSeat record. The preserved handoff benchmark uses 99 races. This experiment keeps all 99 and treats missing exact-six information explicitly rather than deleting the race.

## Outputs

- performance/results/same_seat_99row_summary.csv
- performance/results/same_seat_99row_choices.csv
- performance/results/same_seat_99row_predictions.csv
