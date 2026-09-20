# GitHub Actions run: candidate experience auto-audit

- Generated UTC: 2026-09-20T16:35:54.332806+00:00
- Execution: GitHub Actions
- Headline races: 99
- Candidate politician_id matched uniquely: 198/198
- Unresolved candidate-id cases: 0

## Automatic pre-election history flags

- prior Senate general-election winners: D-side 49, R-side 27
- prior Governor general-election winners: D-side 8, R-side 4
- prior House general-election winners: D-side 29, R-side 24
- same-seat prior-winner incumbency proxy: D-side 49, R-side 26

## Important limitation

These are reconstruction audit variables, not yet authoritative Core V2 variables. A prior election win can miss appointed officeholders, succession to a governorship, and service that did not originate in a general-election win. The incumbency field is explicitly a proxy based on the most recent prior winner of the same state/class, not a final incumbency coding.

No test-election outcome is used to create these flags; only election history strictly before each Senate cycle is queried.

## Outputs

- data/processed/source_snapshots/election_results_house_d7a7cff101da.csv
- data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv
- data/processed/source_snapshots/candidate_experience_source_manifest.csv
- data/processed/core_v2r_headline_candidate_experience_audit.csv

## Next

Identify false negatives caused by appointments/succession and compare automatic experience flags with official biographies before joining them to the Core V2-R design matrix.
