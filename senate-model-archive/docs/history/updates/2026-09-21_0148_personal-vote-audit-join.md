# GitHub Actions run: PersonalVote audit-only design-matrix join

- Generated UTC: 2026-09-20T17:01:37.436976+00:00
- Headline rows: 99
- Rows where both sides have cycle-adjusted prior statewide history: 5

## Important

PersonalVoteDiff_raw_unshrunk_audit is not the Core V2 model term. It is emitted only when both D and R candidates have prior statewide cycle-adjusted performance. Missing candidate history is not silently treated as zero in this diagnostic difference.

The final PersonalVoteDiff still requires partial pooling, era interaction, candidate-history-count shrinkage, and any statewide-vs-district information weighting to be selected inside rolling nested OOS.

## Output

- data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv

## Next

Audit reconstructable historical sources for National_t and RelativeEconomicGrowth before any regression fitting.
