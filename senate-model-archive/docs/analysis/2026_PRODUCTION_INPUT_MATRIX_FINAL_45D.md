# 2026 PRODUCTION INPUT MATRIX — FINAL 45-DAY SNAPSHOT

## Status

Frozen input matrix for the locked **Core V2-R Direction Production 2026** model.

Snapshot cutoff:
- U.S. calendar date: **2026-09-19**
- 2026 general election: 2026-11-03
- no information first published on 2026-09-20 or later is included

## Model-status distinction

- locked production model retrospective diagnostic: **98/99**
- clean nested OOS validation: **96/99**
- these are not interchangeable metrics

## Canonical 98/99 production inputs

Used by the locked production calculation:
- PVI
- SameSeat prior margin
- SameSeat year gap
- IncumbencyDiff
- OutPartyIncumbent
- RelativeEconomicGrowth
- National environment bridge
- era interaction terms derived from incumbency / out-party status
- 45-day poll layer
- production close-poll/PVI selector
- third-party / multi-candidate uncertainty flag only

Retained in this snapshot for diagnostics but **not used by the canonical 98/99 calculation**:
- SenateExperience
- GovernorExperience
- HouseExperience
- PersonalVote
- FEC finance

## PersonalVote diagnostic

PersonalVote was rebuilt through the 2024 election cycle from prior Senate and Governor general elections only. It is retained for audit and future experiments, but it is not a canonical 98/99 production term.

| State | D PersonalVote | R PersonalVote | D-R difference |
|---|---:|---:|---:|
| AK | NA | -10.777594893499712 | 10.777594893499712 |
| GA | 1.940880627023354 | NA | 1.940880627023354 |
| IA | NA | NA | NA |
| ME | NA | 37.9820694352427 | -37.9820694352427 |
| MI | NA | -2.2447700600703864 | 2.2447700600703864 |
| NH | NA | 7.44200737155826 | -7.44200737155826 |
| NC | 13.663702239598738 | NA | 13.663702239598738 |
| OH | 2.2667655244118703 | NA | 2.2667655244118703 |
| TX | NA | NA | NA |

A missing candidate-side value means there is no usable prior Senate/Governor general-election evidence. It does not mean the candidate has zero quality.

## Poll layer

The poll rows are frozen at the U.S. 2026-09-19 cutoff. The current RCP row extract does not expose usable sample-size metadata for every row, so the included value is a 14-day recency-weighted equal-sample-size diagnostic proxy.

This diagnostic proxy must not be confused with a reconstructed exact historical FiveThirtyEight-style n_eff poll aggregate.

## Third-party handling

No directional third-party point correction is used.

Alaska is explicitly flagged as a multi-candidate / ranked-choice uncertainty case.

## Frozen file

- data/snapshots/2026_PRODUCTION_INPUT_MATRIX_FINAL_45D.csv
