# GitHub Actions run: Congress experience overrides v1

- Generated UTC: 2026-09-20T17:06:26.709001+00:00
- Candidate-side override rows: 12
- Unique cycle-candidate overrides: 11
- SenateExperience corrections: 6
- HouseExperience corrections: 6
- Incumbency corrections: 6

## Rule

An override is created only when the candidate has an ACCEPTED match to unitedstates/congress-legislators and the actual term-date flag differs from the election-history proxy. Ambiguous or unmatched names never overwrite the election-history value.

## Overrides

| cycle | state | side | candidate | changed fields | Senate auto->term | House auto->term | Inc auto->term |
|---:|---|---|---|---|---|---|---|
| 2014 | HI | D | Brian Schatz | SenateExperience;Incumbency | 0->1 | 0->0 | 0->1 |
| 2014 | IL | D | Richard J. Durbin | HouseExperience | 1->1 | 0->1 | 1->1 |
| 2014 | OK | R | James M. Inhofe | HouseExperience | 1->1 | 0->1 | 1->1 |
| 2014 | RI | D | Jack Reed | HouseExperience | 1->1 | 0->1 | 1->1 |
| 2014 | SC | R | Tim Scott | SenateExperience;Incumbency | 0->1 | 1->1 | 0->1 |
| 2018 | DE | D | Thomas R. Carper | HouseExperience | 1->1 | 0->1 | 1->1 |
| 2018 | MN | D | Tina Smith | SenateExperience;Incumbency | 0->1 | 0->0 | 0->1 |
| 2018 | WA | D | Maria Cantwell | HouseExperience | 1->1 | 0->1 | 1->1 |
| 2022 | CA | D | Alex Padilla | SenateExperience;Incumbency | 0->1 | 0->0 | 0->1 |
| 2022 | CA | D | Alex Padilla | SenateExperience;Incumbency | 0->1 | 0->0 | 0->1 |
| 2022 | GA | D | Raphael Warnock | SenateExperience;Incumbency | 0->1 | 0->0 | 0->1 |
| 2022 | ID | R | Mike Crapo | HouseExperience | 1->1 | 0->1 | 1->1 |

## Interpretation

The important Senate/incumbency corrections are appointments or mid-cycle accessions that a prior-general-election-win proxy cannot see. House corrections capture candidates who had House service even when the election-history winner query missed it.

## Outputs

- config/congress_experience_overrides_v1.csv
- data/processed/core_v2r_headline_candidate_experience_hybrid.csv
- data/processed/core_v2r_headline_design_matrix_with_congress_experience.csv

## Not yet final

GovernorExperience remains election-history based and still needs a separate term-history audit. OutPartyIncumbent and PersonalVote are not yet joined.

## Next

Audit GovernorExperience for succession/non-election entry, then join GovernorExperienceDiff and construct the final incumbency variables.
