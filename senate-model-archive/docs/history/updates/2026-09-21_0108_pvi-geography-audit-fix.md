# PVI geography audit and correction

## 날짜
2026-09-21

## 발견한 문제

첫 PVI GitHub Actions 결과에서 대통령 일반선거의 주별 행 수가 다음처럼 나왔다.

```text
2000: 56
2004: 53
2008: 56
2012: 56
2016: 56
2020: 56
2024: 57
```

또한 2026 PVI 출력이 55행이었다.

이는 50개 주 외의 미국 영토가 `state_abbrev`를 갖고 포함되었기 때문이다.

## 왜 문제인가

Core V2의 Senate PVI는 미국 주 단위 predictor다.

전국 대통령 D-R margin도 50개 주와 DC의 대통령 일반선거 표를 기준으로 계산해야 하며, 영토를 합산하면 national baseline이 왜곡된다.

## 수정

`build_historical_pvi.py`를 다음처럼 수정했다.

- national presidential total: 50 states + DC만 사용
- Senate PVI output: 50 states만 사용
- territories: 전부 제외
- 각 대통령선거 cycle마다 state + DC가 정확히 51개인지 validation
- 각 state-cycle에 presidential general `race_id`가 정확히 하나인지 validation
- 2026 PVI가 정확히 50개 state row인지 validation

validation 실패 시 CSV를 만들지 않고 Action을 실패시킨다.

## 그대로 유지하는 것

- `Lean = State D-R two-party margin - National D-R two-party margin`
- 각 Senate cycle에서 그 선거보다 엄격히 이전인 최근 두 대통령선거만 사용
- 2026은 2024 + 2020
- 현재 재구축 기본 가중치 `0.67 recent + 0.33 older`

마지막 가중치는 handoff에서 보존된 기본형이며, 원 Core V2의 exact fitted weight라고 단정하지 않는다.

## 다음

GitHub Actions로 수정본을 재실행하고 대통령 national margin을 FEC 공식 결과와 교차검증한다.
