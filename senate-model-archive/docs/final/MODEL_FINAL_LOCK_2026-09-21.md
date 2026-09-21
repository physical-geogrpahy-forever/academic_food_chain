# MODEL FINAL LOCK — Core V2-R Direction Production 2026

## Lock date
2026-09-21

## Status
This model is frozen for 2026 production analysis.

Any later structural or coefficient change must be created under a separate experimental version and must not silently overwrite this configuration.

## Primary objective
Winner-direction accuracy is the primary historical validation objective.

Tie-break order:
1. winner-direction accuracy
2. Brier score / log loss
3. MAE
4. complexity / parsimony

## Base architecture
Fundamentals prior:
- PVI
- National environment
- SameSeat
- Incumbency
- OutPartyIncumbent
- Senate / Governor / House experience
- PersonalVote
- RelativeEconomicGrowth
- era interactions

Poll layer:
- exact benchmark lead time: election minus 45 days
- 30-day aggregation window
- 14-day recency half-life
- w_max = 0.75
- k = 0.5

Production direction selector:
- if poll and PVI disagree: threshold = 2.0 percentage points
- if poll and PVI agree: threshold = 0.75 percentage points
- in the agree case, |PVI| must be at least 15 percentage points
- when eligible, direction follows state PVI while posterior magnitude is preserved

Third-party handling:
- no directional point-margin correction
- third-party support is an uncertainty flag only
- ordinary minor-party flag threshold: 3% poll share
- major independent / party-replacement races are separate multi-candidate problems

## Validation
Accepted clean nested headline validation:
- 96 / 99 correct
- 96.97%

This is the official historical OOS direction benchmark.

Production parameters were then re-fit using historical information through 2022.
Retrospective application of the production rule to the 99 headline races gives 98 / 99, but this is explicitly NOT reported as OOS because those cycles participated in production parameter fitting.

## Frozen production config
config/core_v2r_direction_2026_production.json

## Governance
No 2026 observed election outcome may be used to tune this locked model.
Any post-lock modification must:
- use a new version name
- receive its own chronological OOS validation
- preserve this locked config and documentation
- update CHANGELOG.md
