# GitHub Actions run: historical PVI panel

- Generated UTC: 2026-09-20T16:06:23.996542+00:00
- Execution: GitHub Actions
- Presidential source repo: fivethirtyeight/election-results
- Source commit: d7a7cff101da28f4ff77114450a964874800ca54
- Source blob SHA: 0e4171053b71363a31669137cb9a86289e58d438

## Reconstruction rule

For each Senate election cycle, use the two most recent presidential general elections strictly earlier than that Senate election. This prevents using same-year presidential results that were not known at a 45-day forecast snapshot.

State lean = state Democratic-minus-Republican two-party presidential margin minus national Democratic-minus-Republican two-party presidential margin.

Reconstruction default PVI = 0.67 * recent lean + 0.33 * older lean.

The 0.67/0.33 weights are preserved handoff defaults, not claimed recovered exact fitted weights.

## Presidential state rows by cycle

| presidential cycle | state/DC rows | national D-R two-party margin |
|---:|---:|---:|
| 2000 | 56 | 0.1175 |
| 2004 | 53 | -2.4184 |
| 2008 | 56 | 7.2983 |
| 2012 | 56 | 3.8218 |
| 2016 | 56 | 2.0561 |
| 2020 | 56 | 4.4175 |
| 2024 | 57 | -1.2643 |

## Outputs

- data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv
- data/processed/source_snapshots/presidential_source_manifest.csv
- data/processed/presidential_state_lean.csv
- data/processed/historical_senate_pvi_default_067_033.csv
- data/processed/pvi_2026_default_067_033.csv

- Historical Senate race rows receiving PVI: 348
- 2026 state PVI rows: 55

## Next

Cross-check presidential state and national margins against FEC official election publications, then add SameSeat six-year lag using the canonical Senate target panel once partisan-alignment exceptions are locked.
