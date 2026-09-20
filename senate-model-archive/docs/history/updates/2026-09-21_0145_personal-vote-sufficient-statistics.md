# GitHub Actions run: PersonalVote sufficient statistics v1

- Generated UTC: 2026-09-20T17:06:30.725375+00:00
- Headline candidate-side rows: 198
- Candidate-side rows with at least one prior statewide Senate/Governor election: 82
- Candidate-side rows with cycle-adjusted prior overperformance available: 80
- Long prior-statewide history rows: 122

## Status

This is not a finalized PersonalVoteDiff. The exact Core V2 shrinkage formula, statewide-vs-district information weights, and hyperparameters were not recovered. The pipeline therefore preserves sufficient statistics first and does not tune a shrinkage constant against 2014/2018/2022 headline outcomes.

## Prior-race diagnostic

For a completed prior statewide race:

1. PVI-only residual = actual D-R two-party margin - reconstructed state PVI.
2. A leave-one-out office-cycle residual mean is computed from other Senate races or other gubernatorial races in that same cycle.
3. Cycle-adjusted candidate overperformance = actual margin - PVI - leave-one-out office-cycle residual.
4. Republican candidate values are sign-flipped so positive always means the candidate outperformed their own party-side baseline.

The leave-one-out office-cycle adjustment is a reconstruction diagnostic for prior personal performance. It is not claimed to be the recovered Core V2 National_t.

## Leakage rule

Only prior races with prior_cycle < target_cycle are attached. Same-cycle races are conservatively excluded because the exact election date ordering is not reconstructed here.

## House elections

House performance is not converted into PersonalVote using state PVI because House races are district-level. House experience remains available separately, and district-level personal-vote evidence can be added later only with a district partisan baseline.

## No final shrinkage yet

The output intentionally keeps count, statewide office type, raw mean, and cycle-adjusted mean separately. A final PersonalVoteDiff must choose pooling/shrinkage only inside rolling nested OOS, never from headline test outcomes.

## Outputs

- data/processed/core_v2r_personal_vote_prior_statewide_history.csv
- data/processed/core_v2r_personal_vote_sufficient_statistics.csv

## Next

Join these sufficient statistics to the headline design matrix as audit-only columns, reconstruct National_t and RelativeEconomicGrowth, then define candidate-personal shrinkage inside the rolling OOS training loop.
