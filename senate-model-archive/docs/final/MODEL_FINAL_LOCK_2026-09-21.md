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

The executable source that generates the canonical 98/99 production-retrospective path is authoritative.

Fundamentals prior actually used by that source:
- PVI
- SameSeat prior margin
- SameSeat year gap
- RelativeEconomicGrowth
- National environment
- IncumbencyDiff
- OutPartyIncumbent
- Incumbency era interaction
- OutPartyIncumbent era interaction

Not part of the canonical 98/99 production calculation:
- Senate / Governor / House experience
- PersonalVote
- FEC finance

Those candidate and finance fields may be retained as auxiliary diagnostics, but they must not be inserted into the locked 98/99 production calculation without defining and validating a new model version.

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

## Production model and validation status

There is **one locked production model**: **Core V2-R Direction Production 2026**.

Its historical retrospective production-rule result is:
- **98 / 99 correct**
- **98.99%**
- this is the performance record associated with the locked production rule
- it is retrospective, not OOS, because the production parameters were fit using historical information through 2022

Separately, the clean nested historical validation result is:
- **96 / 99 correct**
- **96.97%**
- this is the clean nested OOS validation benchmark only
- it is **not a second production model** and must not replace the 98/99 production-retrospective record when identifying the locked model

Recovery shorthand:
- **official locked model:** Core V2-R Direction Production 2026
- **production retrospective record:** 98/99
- **clean nested OOS validation:** 96/99

## Frozen production config
config/core_v2r_direction_2026_production.json

## Governance
No 2026 observed election outcome may be used to tune this locked model.
Any post-lock modification must:
- use a new version name
- receive its own chronological OOS validation
- preserve this locked config and documentation
- update CHANGELOG.md


## Canonical validation bundle

The authoritative reconstructed validation artifacts are frozen under:

- `final/validation/README.md`
- `final/validation/manifest.json`
- `final/validation/clean_nested_96of99_predictions.csv`
- `final/validation/production_98of99_predictions.csv`
- `final/validation/base_prior_99_predictions.csv`
- `final/validation/base_prior_coefficients_by_cycle.csv`
- `final/validation/base_prior_standardization_by_cycle.csv`
- `final/validation/production_selector_top_grid.csv`
- `final/validation/verification_report.json`

Recovery rule: read `final/validation/README.md` before using any experimental validation output.
