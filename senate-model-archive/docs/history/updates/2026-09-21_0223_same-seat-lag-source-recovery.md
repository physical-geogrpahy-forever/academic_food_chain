# SameSeat lag-source recovery for full-cycle OOS

## 날짜
2026-09-21

## 문제

full-cycle 실험은 2006~2022를 학습 대상으로 선언했지만, `races` 구성 단계에서 2006 이후 선거만 남겼다. 따라서 2006, 2008, 2010의 SameSeat를 만들기 위해 필요한 2000, 2002, 2004 동일 의석 선거가 seat history에 존재하지 않았다.

그 결과 초기 세 cycle이 modeling panel에서 탈락했고, 2014 outer fold의 inner OOS validation이 사실상 성립하지 않아 `inner_rmse = 1e9`가 발생했다.

## 수정

- 2000, 2002, 2004 Senate 일반선거를 `LAG_SOURCE_CYCLES`로 추가한다.
- 이 세 cycle은 SameSeat history를 만들기 위한 lag source로만 사용한다.
- 실제 회귀 modeling rows는 기존처럼 2006~2022에 한정한다.
- 따라서 2006 PVI는 기존 2004/2000 presidential lean으로 계산된 값을 그대로 사용하며, 2000~2004 자체에 새로운 PVI를 만들 필요가 없다.

## 성능 의미

이 수정은 새 변수를 추가하는 것이 아니라 2006, 2008, 2010의 기존 Core V2 `SameSeat` 입력을 복구해 초기 학습표본을 되살리는 것이다. 수정 후 2014 outer fold도 training-only inner OOS로 ridge를 선택할 수 있어야 한다.
