# GitHub Actions run: presidential national-margin audit

- Generated UTC: 2026-09-20T16:31:55.778784+00:00
- Execution: GitHub Actions
- Purpose: compare 50-state+DC aggregation against explicit national general-election rows in the same pinned source.

| cycle | state-sum D-R two-party margin | explicit national margin | difference | status |
|---:|---:|---:|---:|---|
| 2000 | 0.5322 | 0.5322 | 0.0000 | OK |
| 2004 | -2.4880 | -2.4880 | 0.0000 | OK |
| 2008 | 7.3777 | 7.3777 | 0.0000 | OK |
| 2012 | 3.9166 | 3.9166 | 0.0000 | OK |
| 2016 | 2.2267 | 2.2267 | -0.0000 | OK |
| 2020 | 4.5360 | 4.5360 | 0.0000 | OK |
| 2024 | -1.5001 | NA | NA | NO_NATIONAL_ROW |

## Interpretation

A mismatch means the state-level source cannot be assumed to reproduce the official national popular-vote total for that cycle. Such a cycle requires official FEC cross-check or correction before its national baseline is locked.

- Mismatch cycles: none

## Output

- data/processed/presidential_national_margin_audit.csv

## Next

For mismatch or missing-national-row cycles, compare against the FEC official Federal Elections publication and store an explicit official national-margin table.
