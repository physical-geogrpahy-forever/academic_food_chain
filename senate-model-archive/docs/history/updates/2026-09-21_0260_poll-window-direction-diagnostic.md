# Poll-window direction diagnostic

## 날짜
2026-09-21

## 목표 수정

평가의 1차 기준은 RMSE가 아니라 historical OOS winner/direction correctness다.

## 사용한 prior

- extended-history fundamentals reconstruction
- headline validation 99 races: 2014, 2018, 2022
- prior direction: 90/99 = 90.9%

## Poll source

Diagnostic source:
Jack-Whitcomb/All-US-Senate-polls-2006-2024

이 자료는 RealClearPolling에 공개된 Senate general-election polls를 정리한 보조 자료다.
같은 state-year에 regular/special election이 겹치는 경우를 완전히 구분하지 못한다는 저장소 자체의 경고가 있으므로,
`overlapping_special_election` 표시가 있는 poll은 이번 진단에서 사용하지 않았다.

## Snapshot rule

- snapshot date = election day - 45 days
- snapshot 뒤 poll은 사용하지 않음
- poll margin = mean(Dem - Rep)
- preserved Core V2 poll weight:
  `w = 0.75 * n / (n + 0.5)`
- no-poll state는 fundamentals prior 유지

## Descriptive result

| Poll lookback before 45d snapshot | Correct | Accuracy | Poll-covered races | Good flips | Bad flips |
|---|---:|---:|---:|---:|---:|
| 14 days | 92/99 | 92.9% | 42 | 3 | 1 |
| 30 days | 90/99 | 90.9% | 55 | 3 | 3 |
| 45 days | 91/99 | 91.9% | 55 | 3 | 2 |
| 60 days | 91/99 | 91.9% | 55 | 3 | 2 |

## Important leakage warning

14, 30, 45, 60 day windows were compared on the same 99 headline outcomes.
Therefore 14-day = 92/99 is **not yet a valid new benchmark**.
It is only a candidate architecture discovered descriptively.

A legitimate adoption requires chronological nested selection:
- 2014 window/weight chosen from pre-2014 cycles only
- 2018 chosen from pre-2018 cycles only
- 2022 chosen from pre-2022 cycles only

## Persistent fundamentals misses and poll signal

Among the nine races missed by all three recent fundamentals reconstructions:

- poll direction correct at 45d snapshot: 2014 MN, 2018 MO, 2018 MT, 2022 PA
- poll direction wrong: 2014 IA, 2018 FL, 2022 GA
- no usable unambiguous poll in the 30-day diagnostic: 2014 NH, 2018 WV

This supports keeping a capped observation layer rather than replacing fundamentals with polls.

## Decision

Do not claim 92/99 yet.
Proceed to nested historical poll-window/weight validation with direction correctness as the primary objective.
