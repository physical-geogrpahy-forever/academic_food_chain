# GitHub Actions run: 2000 presidential duplicate-row audit

- Generated UTC: 2026-09-20T17:03:58.604154+00:00
- Execution: GitHub Actions
- Reason: 2000 state-summed national D-R margin differs from the source national row and FEC official aggregate.

- States/DC with exact duplicate signatures: 1
- Total duplicate lines: 8

| state | raw lines | duplicates | raw D | raw R | dedup D | dedup R | raw margin | dedup margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AL | 16 | 8 | 1385222 | 1882346 | 692611 | 941173 | -15.2139 | -15.2139 |

## Alabama diagnostic

AL raw D/R = 1385222/1882346, deduplicated = 692611/941173

FEC official 2000 Alabama values are Bush 941,173 and Gore 692,611. Exact-duplicate removal is accepted only if it recovers the official state result; otherwise a broader source correction is required.

## Outputs

- data/processed/presidential_2000_duplicate_audit.csv
- data/processed/presidential_2000_duplicate_rows.csv

## Next

If exact duplicates explain Alabama and the national mismatch, apply deterministic exact-row deduplication before candidate aggregation and re-run all PVI validation gates. Otherwise freeze FEC official state data for 2000.
