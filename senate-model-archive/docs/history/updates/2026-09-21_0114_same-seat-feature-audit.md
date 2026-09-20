# GitHub Actions run: SameSeat feature audit

- Generated UTC: 2026-09-20T16:39:00.954783+00:00
- Execution: GitHub Actions
- Headline target input: Core V2-R Hypothesis A, 99 races

## Handoff rule

The preserved handoff explicitly defines SameSeat as the result from the same Senate Class exactly six years earlier: SameSeat_{i,t-6}. The reconstruction therefore does not silently replace it with the most recent prior election.

## Coverage

- headline rows: 99
- exact 6-year same-class available: 91
- exact 6-year missing: 8
- last-prior-same-class available: 99

Both total-vote and D/R two-party margin versions are preserved until the original target denominator is recovered through OOS reproduction.

## Missing exact-6-year rows

| cycle | state | seat | special | last prior cycle | gap |
|---:|---|---|---|---:|---:|
| 2014 | AR | Class II | false | 2002 | 12 |
| 2014 | HI | Class III | true | 2010 | 4 |
| 2014 | OK | Class III | true | 2010 | 4 |
| 2014 | SC | Class III | true | 2010 | 4 |
| 2018 | MN | Class II | true | 2014 | 4 |
| 2022 | CA | Class III | true | 2010 | 12 |
| 2022 | CA | Class III | false | 2010 | 12 |
| 2022 | OK | Class II | true | 2020 | 2 |

## Rule status

- Core candidate feature: exact-6-year same-class margin.
- Audit-only comparator: last prior same-class margin and year gap.
- Missing exact-6-year values are not silently filled from last-prior values.
- How the original Core V2 encoded missing SameSeat values remains unresolved and must be tested without leakage.

## Output

- data/processed/core_v2r_headline_same_seat_features.csv

## Next

Join PVI to the 99-race target panel, then reconstruct incumbency and candidate-experience variables before attempting any regression.
