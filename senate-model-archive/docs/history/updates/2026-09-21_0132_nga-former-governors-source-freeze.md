# GitHub Actions run: NGA former-governors source freeze

- Generated UTC: 2026-09-20T16:37:09.956747+00:00
- Source: National Governors Association former-governors search page
- URL: https://www.nga.org/former-governors/search/
- HTML sha256: `30e7e956fcc40862407c407a4301c1a5df47b5d19549893441768232bab05eea`
- Parsed governor-term rows: 2625

## Use

This source is used only to audit whether a Senate candidate had gubernatorial service before the Senate election. The election-history flag remains the fallback when name matching is not accepted.

## Leakage guard

A governor term counts only when its start year is no later than the Senate election year and the term is chronologically relevant to that election. Later gubernatorial service in the current NGA snapshot does not create prior experience.

## Outputs

- data/processed/source_snapshots/nga_former_governors_snapshot.csv
- data/processed/source_snapshots/nga_former_governors_manifest.csv
