# 99-row SameSeat performance experiment start

## 날짜
2026-09-21

## 이유

기존 후보블록 성능 실험은 exact six-year SameSeat가 없는 8개 headline race를 삭제해 91개만 평가했다. 보존된 Core V2 headline 표본은 99개이므로 이 실험은 최종 판정용으로 사용할 수 없다.

## 이번 실험

99개 headline race를 전부 유지하면서 다음 SameSeat 표현을 비교한다.

1. exact6 + missing indicator
2. last-prior + gap
3. exact6가 있으면 exact6, 없으면 last-prior를 쓰는 hybrid + fallback/gap indicator

각 outer test cycle에서 training-only inner rolling OOS로 SameSeat 표현, 후보변수 부분집합, candidate ridge 강도를 함께 선택한다. 빈 후보변수 집합도 허용한다.

## 채택 기준

99개 표본에서 실제 OOS RMSE가 더 낮은 구조만 유지한다. 후보변수 추가가 best structural-only보다 나쁘면 후보 augmentation은 폐기한다.
