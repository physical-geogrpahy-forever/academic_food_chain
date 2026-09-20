# 2018 forecast archive source fix

## 날짜
2026-09-21

## 문제

FiveThirtyEight의 원래 2018 `senate_seat_forecast.csv` live URL은 현재 CSV가 아니라 HTML을 반환한다.

## 대체 원자료

Rdatasets GitHub archive에 당시 FiveThirtyEight seat forecast 데이터가 정적 CSV로 보존되어 있다.

- repository: `vincentarelbundock/Rdatasets`
- pinned commit: `1dcc2bf5f955cc1224a3e1307256e1fe86b68dae`
- path: `csv/fivethirtyeight/senate_seat_forecast.csv`
- file blob SHA 확인값: `8fb6184752d3e7f925f05476f8e2922d903fd044`

## 구조 수정

2018 데이터는 race-level margin 한 행이 아니라 후보별 행이다. 따라서 45일 snapshot에서 state + Senate class + model별로 D 후보 voteshare와 R 후보 voteshare를 묶어 `D - R` margin을 계산한다. 그 뒤 `deluxe margin - classic margin`만 외부 adjustment signal로 사용한다.

2022는 `senate_state_toplines_2022.csv`의 `mean_netpartymargin`에서 같은 차이를 계산한다.

## 누출 방지

각 cycle에서 election day 45일 전 날짜 이하의 가장 최근 forecastdate만 사용한다.
