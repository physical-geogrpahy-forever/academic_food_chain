# 98/99 post-hoc direction candidate

## 날짜
2026-09-21

## 결합 규칙

Baseline은 기존 fixed 45-day poll blend 94/99다.

### Tier 1
out-party incumbent race이고 45-day poll의 절대 margin이 1.0%p 이하이면 state PVI 방향을 우선한다.

### Tier 2
Tier 1에 해당하지 않으면서:
- out-party incumbent race
- 45-day poll 절대 margin이 1.0%p 초과 2.0%p 이하
- FEC June-30 18-month total receipts share 방향이 state PVI 방향과 일치

이면 state PVI 방향을 우선한다.

그 외 race는 baseline을 유지한다.

## Headline 99-race 결과

- baseline: 94/99 = 94.9%
- Tier 1 only: 97/99 = 98.0%
- Tier 1 + Tier 2: **98/99 = 99.0%**

cycle별:
- 2014: 32/33
- 2018: **33/33**
- 2022: 33/33

교정된 race:
- 2018 NV: Tier 1
- 2018 MO: Tier 1
- 2018 IN: Tier 1
- 2018 FL: Tier 2

새로 틀린 headline race: 0

남은 오답:
- 2014 North Carolina

## 검증 상태

중요: 이 98/99는 현재 **post-hoc candidate**이며 clean nested OOS 채택 결과가 아니다.

Tier 1의 1.0%p 기준은 headline 결과를 본 뒤 확인했다.
Tier 2는 Florida 2018과 2022 Nevada의 차이를 설명하는 FEC pre-election 정보에서 도출했지만, 역시 headline 오류 분석 뒤 구성했다.

따라서 production baseline으로 올리기 전에 반드시 더 오래된 cycle에서 동일한 fixed rule을 검증한다.

## 다음 검증

- FEC June-30 Top-50 receipts 자료를 가능한 과거 cycle까지 확장
- historical rolling OOS Senate prior + 45-day polls에 동일한 Tier 1/Tier 2 rule 고정 적용
- cycle별 correct gain/loss 확인
- 특정 cycle에서만 작동하면 폐기 또는 uncertainty-only 신호로 강등

## 데이터 누출

두 tier 모두 선거 45일 전 또는 그 이전에 이용 가능한 정보만 사용한다.
- poll: election minus 45 days snapshot
- PVI: 이전 대통령선거 자료
- FEC receipts: election-year June 30 reporting window
