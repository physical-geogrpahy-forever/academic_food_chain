# 2022 external forecast expression prefix fix

## 날짜
2026-09-21

## 문제

2022 archived Senate topline의 `expression` 값은 `classic`/`deluxe`가 아니라 `_classic`/`_deluxe` 형태다. 기존 parser가 앞의 `_`를 제거하지 않아 usable row가 0건이 되었다.

## 수정

`expression`을 소문자화한 뒤 `lstrip('_')`로 접두 밑줄을 제거한다.

## 성능 판정

이전 세 번의 external-candidate-signal run은 모두 성능 계산 전에 source/parser 단계에서 실패했으므로 성능 결과로 간주하지 않는다. 동일한 45-day external adjustment 실험을 수정본으로 다시 실행한다.
