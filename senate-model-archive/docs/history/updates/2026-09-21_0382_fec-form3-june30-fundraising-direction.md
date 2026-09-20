# Candidate-level FEC Form 3 June-30 fundraising direction experiment

- Generated UTC: 2026-09-20T18:10:16.270172+00:00
- The discarded FEC Table 2 aggregate workbook is not used.
- Senate candidates are matched to the FEC candidate master and principal campaign committee (PCC).
- Finance values come from the latest Form 3 report whose coverage_end_date is June 30 of the election year.
- Candidate matching/report gaps preserve the 94/99 baseline unchanged.
- Signal/gamma for each outer cycle is selected only from prior outer cycles with finance coverage.

## Coverage and result

| scope | N | finance-covered | baseline correct | baseline acc | finance correct | finance acc | net |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 0 | 94 | 94.9% | 94 | 94.9% | +0 |
| 2014 | 33 | 0 | 32 | 97.0% | 32 | 97.0% | +0 |
| 2018 | 33 | 0 | 29 | 87.9% | 29 | 87.9% | +0 |
| 2022 | 33 | 0 | 33 | 100.0% | 33 | 100.0% | +0 |

## Selected signal

| test | signal | gamma | train N | train accuracy | test finance coverage |
|---:|---|---:|---:|---:|---:|
| 2014 | individual_share | 0 | 0 | NA | 0 |
| 2018 | individual_share | 0 | 0 | NA | 0 |
| 2022 | individual_share | 0 | 0 | NA | 0 |

## Correctness changes


## API field audit

- OpenFEC report keys observed: 

## Decision

Adopt only if candidate-level June-30 fundraising exceeds 94/99 without outer-test tuning and finance coverage is adequate.

## Outputs

- experiments/fec18m_direction/results/fec_form3_summary.csv
- experiments/fec18m_direction/results/fec_form3_choices.csv
- experiments/fec18m_direction/results/fec_form3_predictions.csv
- experiments/fec18m_direction/results/fec_form3_candidate_matches.csv
- experiments/fec18m_direction/results/fec_form3_source_meta.csv
