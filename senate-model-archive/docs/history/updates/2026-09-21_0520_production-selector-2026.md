# 2026 production direction selector

- Generated UTC: 2026-09-20T19:07:32.063325+00:00
- Purpose: fit the production rule for 2026 using all historical information available through 2022.
- This is distinct from clean rolling OOS validation.

## Accepted clean validation

- Clean nested headline benchmark: **96/99 = 97.0%**.
- This remains the reported historical OOS performance.

## 2026 fitted selector

- poll-PVI disagree threshold: 2.0%p
- poll-PVI agree threshold: 0.75%p
- minimum |PVI| when poll and PVI agree: 15%p
- full-history training correct under selector objective: 237/259
- Brier: 0.0711
- log loss: 0.2523
- MAE: 7.93

## Retrospective headline diagnostic

- fixed baseline: 94/99
- 2026 fitted rule applied retrospectively: 98/99
- This number is NOT labeled OOS because 2014/2018/2022 participated in production parameter fitting.

## Retrospective remaining wrong

- 2014 NC: actual=-1.63, adjusted=5.44, reason=none

## Third-party policy

- No directional point correction is applied from third-party share.
- Historical multi-candidate audit recovered only one ordinary minor-third 3-15% race-cycle with usable explicit support: NC 2014.
- Therefore third-party support is an uncertainty flag only until a broader historical source is assembled.
- Major independent/party-replacement races are handled as a separate multi-candidate problem rather than ordinary D/R Senate races.

## Files

- config/core_v2r_direction_2026_production.json
- experiments/production_selector_2026/results/production_selector_diagnostic.csv
- experiments/production_selector_2026/results/production_selector_top_grid.csv
