# Nested poll-blend run fix

## 날짜
2026-09-21

## 오류

`poll_stack.run.aggregate()`는 `(poll_margin, n_eff, poll_count)`를 반환하지만 `poll_blend_direction/run.py`에서 세 번째 값을 poll list로 잘못 해석하고 `len()`을 호출했다.

따라서 첫 nested poll-blend run은 모델 평가 전에 `TypeError: object of type 'int' has no len()`으로 중단됐다.

## 수정

세 번째 반환값을 정수 `poll_count`로 직접 사용하도록 수정했다.

## 성능 판정

첫 run은 예측 결과를 만들지 못했으므로 성능 결과로 간주하지 않는다. 동일한 nested direction-accuracy 실험을 수정본으로 재실행한다.
