# Out-party favored-posterior rule decision

## 날짜
2026-09-21

## 결과

out-party incumbent이면서 fixed-poll posterior가 해당 현직을 가리키는 경우에만 state-partisan penalty를 주고, PersonalVote로 보호하는 규칙을 이전 cycle에서 선택했다.

- fixed poll baseline: 94/99 = 94.9%
- adjusted rule: 93/99 = 93.9%

2018은 29/33 -> 31/33으로 개선했지만 2022가 33/33 -> 30/33으로 악화됐다.

따라서 이 규칙은 폐기한다.

현재 primary benchmark는 계속 94/99다.

다음에는 hand-built post-poll rule을 추가하지 않고, prior/poll/structural/candidate 정보를 함께 사용한 regularized winner classifier를 chronological nested OOS로 평가한다.
