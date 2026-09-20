# First >94/99 direction candidate: fixed 1.0pp out-party close-poll rule

## 날짜
2026-09-21

## 결과

현재 accepted baseline:
- fixed 45-day poll blend: 94/99 = 94.9%

진단 후보:
- out-party incumbent race에서 45-day poll의 절대 margin이 1.0%p 이하일 때만 state PVI 방향을 우선
- 그 외 모든 race는 baseline 유지

결과:
- combined: **97/99 = 98.0%**
- 2014: 32/33 -> 32/33
- 2018: 29/33 -> **32/33**
- 2022: 33/33 -> 33/33
- 새로 틀린 race: 0

교정된 race:
- 2018 Nevada: poll R+0.53, PVI D+1.20, actual D -> PVI 방향으로 교정
- 2018 Missouri: poll R+0.57, PVI R+19.10, actual R -> PVI 방향으로 교정
- 2018 Indiana: poll D+0.69, PVI R+19.77, actual R -> PVI 방향으로 교정

남은 headline 오답:
- 2014 North Carolina
- 2018 Florida

## 매우 중요한 검증 상태

이 97/99는 **post-hoc candidate**다.

이유:
- strict nested selector는 2018 이전 전체 training에서 threshold=none과 threshold=1.0이 winner count에서 동률이었다.
- 기존 selector는 tie-break로 fewer overrides를 사용해 none을 선택했다.
- 1.0%p를 headline 결과를 본 뒤 다시 확인했으므로 이를 곧바로 clean OOS improvement라고 부르면 안 된다.

다만 다음 사실은 중요하다.
- 2018 이전 training에서 threshold=1.0은 baseline보다 winner count가 나쁘지 않았다.
- headline 2014에서 변화 없음.
- headline 2022에서도 변화 없음.
- 2018에서 정확히 세 오류를 교정하고 새 오류를 만들지 않았다.

따라서 이 규칙은 폐기 대상이 아니라 **independent validation이 필요한 production candidate**로 승격한다.

## 다음 검증

1. 2006-2022 all-midterm historical cycle별로 fixed 1.0pp rule의 변화 확인
2. modern-era only robustness 확인
3. threshold 0.75/1.0/1.25에 대한 민감도
4. Florida 2018은 1.65%p라 별도 challenger-strength evidence가 필요한지 확인
5. North Carolina 2014는 poll D+4.16이라 이 규칙과 별개의 candidate-quality 문제로 분리

## 관련 파일

- experiments/outparty_closepoll_pvi/results/closepoll_predictions.csv
- experiments/outparty_closepoll_pvi/results/closepoll_choices.csv
- docs/history/updates/2026-09-21_0450_outparty-closepoll-pvi-rule.md
