# FEC Top-50 June-30 fundraising direction experiment

- Generated UTC: 2026-09-20T18:14:03.738869+00:00
- Uses official FEC 18-month Top 50 Senate tables for receipts (6a), contributions from individuals (6b), and cash on hand (6f).
- All tables cover January 1 of the pre-election year through June 30 of the election year.
- A finance share is computed only when both major-party general-election candidates appear in the same Top-50 metric table.
- Missing Top-50 membership is never treated as zero; uncovered races retain the 94/99 baseline.
- Signal, coefficient and optional posterior threshold are selected from earlier cycles only.

## Result

| scope | N | any finance covered | baseline correct | baseline acc | finance correct | finance acc | net | flips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 36 | 94 | 94.9% | 94 | 94.9% | +0 | 0 |
| 2014 | 33 | 14 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 12 | 29 | 87.9% | 29 | 87.9% | +0 | 0 |
| 2022 | 33 | 10 | 33 | 100.0% | 33 | 100.0% | +0 | 0 |

## Selected finance rule

| test | signal | gamma | posterior threshold | train accuracy | train signal coverage | test signal coverage |
|---:|---|---:|---:|---:|---:|---:|
| 2014 | receipts_share | 0 | 999 | NA | 0 | 10 |
| 2018 | cash_share | 0 | 999 | 97.0% | 12 | 9 |
| 2022 | cash_share | 0 | 999 | 92.4% | 21 | 7 |

## Correctness changes


## Decision

Adopt only if combined winner-direction accuracy exceeds 94/99 without outer-cycle tuning.

## Outputs

- experiments/fec18m_direction/results/fec_top50_summary.csv
- experiments/fec18m_direction/results/fec_top50_choices.csv
- experiments/fec18m_direction/results/fec_top50_predictions.csv
- experiments/fec18m_direction/results/fec_top50_match_review.csv
- experiments/fec18m_direction/results/fec_top50_source_meta.csv
