# Objective correction: winner accuracy first

## 날짜
2026-09-21

## 오류

최근 성능 탐색에서 RMSE를 1차 목표로 사용했다. 이 프로젝트의 실질 목표는 각 상원 선거의 승패 방향을 맞히는 것이므로 평가 우선순위가 잘못되었다.

## 즉시 수정

앞으로 모델 선택 기준은 다음 순서를 사용한다.

1. strictly chronological OOS에서 맞힌 승패 수
2. direction accuracy
3. 동률일 때 MAE
4. 그래도 동률이면 RMSE

RMSE가 낮아져도 승패 적중 수가 줄면 성능 향상으로 판정하지 않는다.

## 현재 재판정

- 보존 Core V2 fundamentals: direction 90.9%
- 보존 Core V2 + 45-day poll: direction 91.9%
- extended-history RMSE-first reconstruction: direction 90.9%

따라서 RMSE 8.8189는 방향 기준으로는 보존 Core V2 + poll을 이기지 못했고, 최종 성능 향상으로 채택할 수 없다.

## 다음 실험

extended-history의 하이퍼파라미터 선택 자체를 inner-OOS direction correct count 최대화로 바꾼다. 동률일 때만 MAE와 RMSE를 사용한다.
