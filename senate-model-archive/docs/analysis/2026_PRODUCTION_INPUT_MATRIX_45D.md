# 2026 production input matrix at the exact 45-day cutoff

- Cutoff: 2026-09-19 U.S. calendar date.
- This matrix joins the frozen structural layer, Core candidate experience, PersonalVote history, poll diagnostic rows, and FEC June-30 Top-50 finance fields.
- No 2026-09-20 or later information is used.

## PersonalVote

PersonalVote follows the Core historical definition:
- prior Senate and Governor general elections only
- candidate-side two-party margin residual versus cycle-specific PVI
- subtract the same-office same-cycle mean residual
- House and state-legislative performance are not inserted into PersonalVote
- 2024 Senate races are added from MEDSL 2024 official results collection

| State | D candidate | D prior statewide | D PV | R candidate | R prior statewide | R PV | PV diff D-R |
|---|---|---:|---:|---|---:|---:|---:|
| AK | Mary Peltola | 0 | NA | Dan Sullivan | 2 | -10.45 | 10.45 |
| GA | Jon Ossoff | 1 | 1.88 | Mike Collins | 0 | NA | 1.88 |
| IA | Josh Turek | 0 | NA | Ashley Hinson | 0 | NA | 0.00 |
| ME | Troy Jackson | 0 | NA | Susan Collins | 3 | 36.88 | -36.88 |
| MI | Abdul El-Sayed | 0 | NA | Mike Rogers | 1 | -2.18 | 2.18 |
| NH | Chris Pappas | 0 | NA | John Sununu | 1 | 7.35 | -7.35 |
| NC | Roy Cooper | 2 | 12.45 | Michael Whatley | 0 | NA | 12.45 |
| OH | Sherrod Brown | 4 | 3.46 | Jon Husted | 0 | NA | 3.46 |
| TX | James Talarico | 0 | NA | Ken Paxton | 0 | NA | 0.00 |

## FEC June-30 block

- Source family: FEC 2025-2026 candidate-summary bulk file (weball26.zip), filtered to Coverage_End_Date exactly 06/30/2026.
- Metrics: total receipts, contributions from individuals, cash on hand.
- A D-R share is computed only when both candidates have an exact 06/30/2026 candidate-summary record.
- Candidates whose latest bulk-summary coverage does not equal 06/30/2026 remain missing; later reporting periods are never back-filled or treated as June-30 data.

| State | receipts share | individual share | cash share |
|---|---:|---:|---:|
| AK | NA | NA | NA |
| GA | NA | NA | NA |
| IA | NA | NA | NA |
| ME | NA | NA | NA |
| MI | NA | NA | NA |
| NH | NA | NA | NA |
| NC | NA | NA | NA |
| OH | NA | NA | NA |
| TX | NA | NA | NA |

## Output

- data/snapshots/2026_production_input_matrix_45d.csv
- data/snapshots/2026_personal_vote_core.csv
- data/snapshots/2026_fec_june30_top50.csv

## Interpretation boundary

This file is a model-input artifact. It does not itself constitute a winner forecast or election-outcome probability.
