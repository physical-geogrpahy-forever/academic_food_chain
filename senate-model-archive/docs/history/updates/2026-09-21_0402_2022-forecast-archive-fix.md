# 2022 forecast archive source fix

## 날짜
2026-09-21

## 문제

FiveThirtyEight의 2022 live `senate_state_toplines_2022.csv` URL도 현재 CSV 대신 HTML을 반환한다.

## 대체 원자료

`stephensond/election-night-2022` 저장소에 해당 CSV가 실제 파일로 보존되어 있다.

- pinned commit: `83f2c9867f319b921fa10ad04bc256d8106bc8f4`
- path: `input/senate_state_toplines_2022.csv`
- blob SHA: `dc1842d6661b550b2cdfe08bfd2349a9983a292d`

전체 일별 forecast series에서 election day 45일 전 이하의 가장 최근 `forecastdate`만 사용한다. 따라서 archive 자체가 선거 후 생성됐더라도 선택되는 feature 값은 45일 snapshot 이후 정보를 사용하지 않는다.
