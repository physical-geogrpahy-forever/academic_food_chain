# GitHub Actions run: historical PVI panel v3 — geography + exact-duplicate fix

- Generated UTC: 2026-09-20T16:22:16.849620+00:00
- Execution: GitHub Actions
- Fix 1: exclude presidential congressional-district rows such as M1/M2/N1/N2/N3 from state and national presidential margins
- Fix 2: remove exact duplicate source result lines before candidate aggregation
- Presidential source repo: fivethirtyeight/election-results
- Source commit: d7a7cff101da28f4ff77114450a964874800ca54
- Source blob SHA: 0e4171053b71363a31669137cb9a86289e58d438

## Geography correction

Only the 50 states plus DC are used to construct the national presidential two-party margin. U.S. territories are excluded. Senate PVI output contains the 50 states only.
- Excluded non-state/DC abbreviations observed in source: M1, M2, N1, N2, N3, PR

## Correction from v1

The presidential source includes non-state congressional-district result rows used for electoral-vote allocation in Maine and Nebraska. The first reconstruction treated those rows as if they were additional states, producing 55 2026 PVI rows and slightly contaminating national presidential margins. v2 filters to the 50 states plus DC before calculating national margin and state lean.

The v1 worklog is retained as an audit trail; its generated PVI files are superseded by this run.

## Exact duplicate correction

- Exact duplicate source rows removed: 8
- Duplicate state-cycles: 2000-AL:8
- 2000 Alabama de-duplication is separately audited against FEC certified results.

## Reconstruction rule

For each Senate election cycle, use the two most recent presidential general elections strictly earlier than that Senate election. This prevents same-year presidential final results from leaking into a pre-election Senate forecast.

State lean = state Democratic-minus-Republican two-party presidential margin minus national Democratic-minus-Republican two-party presidential margin.

Reconstruction default PVI = 0.67 * recent lean + 0.33 * older lean.

The 0.67/0.33 weights are preserved handoff defaults, not claimed recovered exact fitted weights.

## Presidential state rows by cycle

| presidential cycle | state + DC rows | national D-R two-party margin |
|---:|---:|---:|
| 2000 | 51 | 0.5322 |
| 2004 | 51 | -2.4880 |
| 2008 | 51 | 7.3777 |
| 2012 | 51 | 3.9166 |
| 2016 | 51 | 2.2267 |
| 2020 | 51 | 4.5360 |
| 2024 | 51 | -1.5001 |

## Outputs

- data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv
- data/processed/source_snapshots/presidential_source_manifest.csv
- data/processed/presidential_state_lean.csv
- data/processed/historical_senate_pvi_default_067_033.csv
- data/processed/pvi_2026_default_067_033.csv

- Historical Senate race rows receiving PVI: 348
- 2026 state PVI rows: 50 (expected 50)

## Validation gates

- Every presidential cycle must have exactly 51 state/DC rows.
- Every state-cycle must have exactly one presidential general race_id.
- 2026 PVI must have exactly 50 state rows.

## Next

Cross-check national presidential margins against FEC official results, then proceed to SameSeat construction after target-race alignment rules are locked.
