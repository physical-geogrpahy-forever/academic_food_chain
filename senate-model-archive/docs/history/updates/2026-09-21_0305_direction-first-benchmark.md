# Direction-first benchmark decision

## 날짜
2026-09-21

## 목표함수 변경

이 프로젝트의 1차 성능 목표는 margin RMSE가 아니라 **승패 방향 적중률**이다.

앞으로 모델 채택 순서는 다음과 같다.

1. rolling OOS direction accuracy
2. 동률이면 Brier score / log loss
3. 그 다음 MAE / RMSE
4. 특정 cycle 하나의 우연한 개선인지 확인
5. future leakage가 없는지 확인

RMSE가 낮아져도 방향 적중률이 낮아지면 채택하지 않는다.

## 현재 방향 기준선

Preserved Core V2:
- fundamentals: 90/99 = 90.9%
- + 45-day poll: documented 91.9%

Current reconstructed direction-first baseline:
- fullcycle incumbency-era prior: 90/99 = 90.9%
- + reconstructed 45-day poll layer, fixed Core V2 blend w_max=0.75, k=0.5: **94/99 = 94.9%**

## poll layer가 고친 4개

- 2014 Colorado: prior D, actual R -> poll posterior R
- 2014 Iowa: prior D, actual R -> poll posterior R
- 2018 West Virginia: prior R, actual D -> poll posterior D
- 2022 Pennsylvania: prior R, actual D -> poll posterior D

이번 고정 poll layer는 prior가 맞았던 선거를 새로 틀리게 만든 사례가 없었다.

## 현재 남은 5개 오답

- 2014 North Carolina
- 2018 Nevada
- 2018 Missouri
- 2018 Florida
- 2018 Indiana

## 다음 성능 목표

현재 94/99를 새 primary benchmark로 사용한다.

다음 실험은 RMSE 개선을 목표로 하지 않는다. 남은 5개 오답을 줄이되 기존 94개 정답을 훼손하지 않는 구조만 채택한다.

특히 2018 Missouri, Florida, Indiana는 fundamentals가 실제 결과와 반대 방향으로 크게 치우친 상태에서 45-day poll도 충분히 이를 교정하지 못했다. 따라서 candidate/local structure와 poll-fundamentals disagreement 처리의 direction accuracy를 별도로 검증한다.

## 파일

- experiments/poll_direction/results/poll_fixed_summary.csv
- experiments/poll_direction/results/poll_fixed_predictions.csv
- experiments/poll_direction/results/poll_snapshot_45d_reconstructed.csv
- experiments/direction_accuracy/results/direction_summary.csv
