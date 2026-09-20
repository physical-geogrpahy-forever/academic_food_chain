# GitHub Actions run: GovernorExperience audit

- Generated UTC: 2026-09-20T16:37:09.990160+00:00
- Candidate-side rows: 198
- Accepted NGA name matches: 13/198
- Election-history governor positives: 12
- Final governor positives after NGA cross-check: 15
- New supported overrides: 3

## Rule

The election-history governor flag is never reduced by an NGA name-match failure. NGA can add a missing prior-governor flag only when the candidate-to-governor name match is accepted and the NGA term starts before the Senate election year.

## Supported additions

| cycle | state | side | candidate | auto | NGA | matched governor | terms |
|---:|---|---|---|---:|---:|---|---|
| 2014 | ID | R | James E. Risch | 0 | 1 | James E. Risch | Idaho:2006-2007 |
| 2014 | TN | R | Lamar Alexander | 0 | 1 | Lamar Alexander | Tennessee:1979-1987 |
| 2018 | PA | D | Robert P. Casey Jr. | 0 | 1 | Robert P. Casey | Pennsylvania:1987-1995 |

## Outputs

- data/processed/core_v2r_headline_governor_experience_crosscheck.csv
- config/governor_experience_overrides_v1.csv
- data/processed/core_v2r_headline_design_matrix_with_candidate_experience.csv

## Next

Add OutPartyIncumbent and PersonalVote, then reconstruct National_t and Era interactions before any coefficient fitting.
