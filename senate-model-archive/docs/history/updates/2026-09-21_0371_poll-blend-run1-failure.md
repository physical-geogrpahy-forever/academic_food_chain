# Nested poll blend run 1 failure

## 날짜
2026-09-21

첫 실행은 성능 계산 전에 TypeError로 중단됐다. 재사용한 poll aggregate 함수의 세 번째 반환값은 poll 목록이 아니라 poll count 정수인데, 실험 코드가 다시 len()을 적용했다.

모델 성능 결과는 생성되지 않았으며 실패 run으로만 기록한다.

수정 후 동일한 direction-first nested OOS 실험을 재실행한다.
