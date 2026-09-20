# Historical PersonalVote out-party decision

## 날짜
2026-09-21

## 결과

2006 이후 Senate 후보의 과거 초과성과를 복구해 OutPartyIncumbent penalty와 결합했지만 combined direction accuracy는 변하지 않았다.

- baseline: 94/99 = 94.9%
- historical PersonalVote + out-party adjustment: 94/99 = 94.9%

따라서 현재 primary model에는 추가하지 않는다.

## 다음

남은 오답의 poll error가 주 당파환경에 따라 체계적으로 달라지는지 시험한다. test cycle 이전 poll만으로 race-level poll error를 PVI, out-party incumbency, poll-fundamentals gap에 회귀하고, 그 predicted bias만 poll margin에서 제거한 뒤 기존 fixed Core V2 blend를 적용한다.
