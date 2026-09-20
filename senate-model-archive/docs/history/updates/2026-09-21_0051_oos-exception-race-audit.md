# GitHub Actions run: 2006-2022 Senate exception-race audit

- Generated UTC: 2026-09-20T16:12:34.075707+00:00
- Execution: GitHub Actions
- Scope: all general-election records with cycle 2006 through 2022, including odd-year special cycles

## Why this audit was added

The first mechanical D/R audit can misclassify races where a non-major-party candidate wins even though both DEM and REP candidates are present. Ranked-choice records also require final-round handling rather than naive summation across rounds.

## Exception counts

- FINAL_ROUND_RULE_REQUIRED: 3
- MANUAL_PARTY_ALIGNMENT_REQUIRED: 6
- MANUAL_RACE_RULE_REQUIRED: 10
- SAFE_IF_AGGREGATE_SAME_CANDIDATE: 13
- SPECIAL_ELECTION_POLICY_REQUIRED: 16

- Total exception/review races: 48
- Headline-cycle exceptions (2014, 2018, 2022): 18

## Headline-cycle exception races

| cycle | state | seat | class | reasons | winner |
|---:|---|---|---|---|---|
| 2014 | AL | Class II | MANUAL_RACE_RULE_REQUIRED | non_unique_or_missing_D_R | Jeff Sessions [REP] 795606 |
| 2014 | HI | Class III | SPECIAL_ELECTION_POLICY_REQUIRED | special | Brian Schatz [DEM] 246827 |
| 2014 | KS | Class II | MANUAL_RACE_RULE_REQUIRED | non_unique_or_missing_D_R | Pat Roberts [REP] 460350 |
| 2014 | OK | Class III | SPECIAL_ELECTION_POLICY_REQUIRED | special | James Lankford [REP] 557002 |
| 2014 | SC | Class II | SAFE_IF_AGGREGATE_SAME_CANDIDATE | fusion_or_multiline | Lindsey Graham [REP] 672941 |
| 2014 | SC | Class III | SPECIAL_ELECTION_POLICY_REQUIRED | special | Tim Scott [REP] 727215 |
| 2018 | CA | Class I | MANUAL_RACE_RULE_REQUIRED | non_unique_or_missing_D_R | Dianne Feinstein [DEM] 6019422 |
| 2018 | CT | Class I | SAFE_IF_AGGREGATE_SAME_CANDIDATE | fusion_or_multiline | Christopher S. Murphy [DEM/WFP] 825579 |
| 2018 | ME | Class I | FINAL_ROUND_RULE_REQUIRED | winner_not_major_party;ranked_choice | Angus S. King Jr. [IND] 344575 |
| 2018 | MN | Class II | SPECIAL_ELECTION_POLICY_REQUIRED | special | Tina Smith [DEM] 1370540 |
| 2018 | NY | Class I | SAFE_IF_AGGREGATE_SAME_CANDIDATE | fusion_or_multiline | Kirsten E. Gillibrand [DEM/IDP/OTH/WFP] 4056931 |
| 2018 | VT | Class I | MANUAL_PARTY_ALIGNMENT_REQUIRED | non_unique_or_missing_D_R;winner_not_major_party | Bernie Sanders [IND] 183649 |
| 2022 | AK | Class III | FINAL_ROUND_RULE_REQUIRED | non_unique_or_missing_D_R;ranked_choice;fusion_or_multiline | Lisa Murkowski [REP] 366207 |
| 2022 | CA | Class III | SPECIAL_ELECTION_POLICY_REQUIRED | special | Alex Padilla [DEM] 6559303 |
| 2022 | CT | Class III | SAFE_IF_AGGREGATE_SAME_CANDIDATE | fusion_or_multiline | Richard Blumenthal [DEM/WFP] 723864 |
| 2022 | NY | Class III | SAFE_IF_AGGREGATE_SAME_CANDIDATE | fusion_or_multiline | Charles E. Schumer [DEM/WFP] 3320561 |
| 2022 | OK | Class II | SPECIAL_ELECTION_POLICY_REQUIRED | special | Markwayne Mullin [REP] 710643 |
| 2022 | UT | Class III | MANUAL_RACE_RULE_REQUIRED | non_unique_or_missing_D_R | Mike Lee [REP] 571974 |

## Provisional handling rules

1. Fusion or multi-line only: aggregate ballot lines belonging to the same candidate; do not treat them as separate candidates.
2. Ranked choice: do not sum across rounds; use the final certified round/result.
3. Winner not major party: require explicit partisan alignment or a documented exclusion rule before constructing D-minus-R margin.
4. Special election: keep separate until the original Core V2 inclusion policy is recovered or reproduced by OOS comparison.
5. Missing D/R or missing votes: manual rule required; never silently coerce to zero.

## Output

- data/processed/historical_senate_oos_exception_races.csv

## Next

Resolve the headline-cycle exceptions first, then compare inclusion-rule variants by historical OOS without using 2026 outcomes.
