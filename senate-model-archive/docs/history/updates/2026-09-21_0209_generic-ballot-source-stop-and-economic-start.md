# Generic Ballot source stop and economic performance start

## 날짜
2026-09-21

## Generic Ballot 중단 이유

- 과거 FiveThirtyEight projects URL은 현재 ABC News HTML을 반환한다.
- `simonw/fivethirtyeight-polls` 미러의 현재 `generic_ballot_polls.csv`는 2020과 2022 cycle만 포함한다.
- 구 FiveThirtyEight GitHub의 historical trendline은 2016까지만 확인된다.

따라서 짧은 탐색 범위 안에서 2006, 2010, 2014, 2018, 2022를 동일 정의로 연결할 raw generic-ballot source를 확보하지 못했다. 사용자 목표가 성능 향상이므로 이 데이터 소스 추적은 여기서 중단한다.

## 다음 성능 실험

Core V2의 기존 필수항인 `RelativeEconomicGrowth`를 99-row `PVI + last-prior SameSeat + gap` baseline에 추가한다.

1차 신호 진단은 BEA current revised `SQINC1`에서 Q1 전년동기 개인소득 성장률을 계산한다. 미국 대비, 주 median 대비, 대통령당 방향을 곱한 형태를 training-only nested OOS에서 비교한다.

현재 revised 값을 쓰므로 이 단계는 signal test다. RMSE 개선이 확인될 때만 historical release-vintage 검증으로 넘어간다.
