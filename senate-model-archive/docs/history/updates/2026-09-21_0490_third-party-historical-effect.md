# Historical third-party Senate polling effect audit

- Generated UTC: 2026-09-20T18:56:58.403278+00:00
- Source: Electoral-vote.com archived daily Senate pages.
- Window: 14 calendar days ending at the election-minus-45-day snapshot.
- Purpose: test whether explicit third-candidate support is associated with larger D-R polling error or winner-direction misses.
- This is an audit, not yet a production correction.

## Source coverage

- Unique poll observations: 161
- Race-cycle aggregates: 71
- Race-cycles with explicit third-party poll share >=3%: 3

## Descriptive comparison

| group | N | direction accuracy | mean absolute D-R error |
|---|---:|---:|---:|
| third_poll_ge_3pct | 3 | 66.7% | 29.64 |
| third_poll_lt_3pct_or_none | 68 | 94.1% | 8.53 |

## North Carolina 2014

- 45-day-window average D=44.14, R=39.71, explicit third=5.60.
- Poll D-R margin=4.43.
- Actual two-party D-R margin=-1.63.
- Actual non-D/R share=3.78.
- D-R polling error actual-minus-poll=-6.06.

## Interpretation rule

- If third-party races show materially worse direction accuracy or error, add third-party share to uncertainty/calibration first.
- Only add a directional correction if historical OOS evidence shows a stable sign. Do not assign all minor-party votes to one major party.
- NC 2014 will only be corrected by a third-party model if the historical relationship supports such a directional adjustment; otherwise it remains a general polling miss.

## Outputs

- experiments/third_party_historical/results/daily_poll_rows.csv
- experiments/third_party_historical/results/race_third_party_audit.csv
- experiments/third_party_historical/results/third_party_group_summary.csv
- experiments/third_party_historical/results/source_days.csv
