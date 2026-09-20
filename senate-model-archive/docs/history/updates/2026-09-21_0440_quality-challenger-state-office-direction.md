# QualityChallenger with state-office audit

- Generated UTC: 2026-09-20T18:58:05.541082+00:00
- Primary objective: historical winner-direction accuracy.
- Candidate-quality coding is fixed before model scoring and applied uniformly to every headline candidate.
- Existing Senate, House, and Governor experience is merged with pre-election Wikidata P39 office history.
- New office tiers: statewide elected executive=3, state legislature=2, local elected office=1, existing federal or Governor experience=4.
- Undated Wikidata office claims are not automatically counted, preventing post-election office leakage.

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 | 0 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected rule by outer cycle

| test | gamma | hostility eta | personal tau | quality mode | cap | train accuracy | flips |
|---:|---:|---:|---:|---|---:|---:|---:|
| 2014 | 0 | 0 | 999 | binary | 999 | NA | 0 |
| 2018 | 0 | 0 | 999 | binary | 999 | 97.0% | 0 |
| 2022 | 2 | 0.3 | 8 | binary | 999 | 97.0% | 3 |

## Correctness changes


## Five unresolved races

- 2014 NC: WRONG, challenger=R tier=0, baseline=5.44, adjusted=5.44, hostility=6.33, incumbent personal=8.34
- 2018 NV: WRONG, challenger=D tier=4, baseline=-0.62, adjusted=-0.62, hostility=1.20, incumbent personal=14.89
- 2018 MO: WRONG, challenger=R tier=3, baseline=4.72, adjusted=4.72, hostility=19.10, incumbent personal=3.57
- 2018 FL: WRONG, challenger=R tier=4, baseline=9.21, adjusted=9.21, hostility=3.32, incumbent personal=9.53
- 2018 IN: WRONG, challenger=R tier=2, baseline=5.41, adjusted=5.41, hostility=19.77, incumbent personal=7.03

## Audit review load
- Candidate-side records requiring review or containing undated eligible office claims: 50 of 196.
- Full rows are preserved in quality_candidate_audit.csv; review-only offices are not used automatically.

## Decision
- Current accepted benchmark: 94/99.
- Adopt only if adjusted accuracy exceeds 94/99 with parameters selected from earlier cycles only.

## Outputs
- experiments/quality_challenger/results/quality_candidate_audit.csv
- experiments/quality_challenger/results/quality_race_features.csv
- experiments/quality_challenger/results/quality_summary.csv
- experiments/quality_challenger/results/quality_choices.csv
- experiments/quality_challenger/results/quality_predictions.csv
