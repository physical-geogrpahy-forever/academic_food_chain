# 2026 Core PersonalVote reconstruction

- Generated UTC: 2026-09-21T01:40:44.896502+00:00
- Uses prior statewide Senate and Governor general elections only.
- PVI is reconstructed from the two previous presidential state leans with 0.67/0.33 weights.
- Candidate overperformance is adjusted by leave-one-out office-cycle residual, matching the archived sufficient-statistics procedure.
- House and state-office races are not converted into PersonalVote.

| State | D PV | R PV | D-R PV diff | D prior N | R prior N |
|---|---:|---:|---:|---:|---:|
| AK | NA | -10.78 | 10.78 | 0 | 2 |
| GA | 1.94 | NA | 1.94 | 1 | 0 |
| IA | NA | NA | NA | 0 | 0 |
| ME | NA | 37.98 | -37.98 | 0 | 3 |
| MI | NA | -2.24 | 2.24 | 0 | 1 |
| NC | 13.66 | NA | 13.66 | 2 | 0 |
| NH | NA | 7.44 | -7.44 | 0 | 1 |
| OH | 2.27 | NA | 2.27 | 4 | 0 |
| TX | NA | NA | NA | 0 | 0 |

## Notes

- A missing candidate-side PersonalVote means no prior Senate/Governor general-election evidence was found; it is not evidence of zero candidate quality.
- The race-level difference uses zero only as a neutral placeholder when the opposite candidate has an observed PersonalVote. Both-missing races remain flagged separately.
- This file is an input reconstruction and does not change the locked historical model.

## Files

- data/snapshots/2026_personal_vote_core.csv
- data/snapshots/2026_personal_vote_prior_history.csv
