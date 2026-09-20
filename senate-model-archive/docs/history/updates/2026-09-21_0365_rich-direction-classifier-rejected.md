# Rich direction classifier decision

## 날짜
2026-09-21

## 결과

fixed-poll posterior에 poll 정보, PVI, SameSeat, 경제, 전국환경, Incumbency, OutPartyIncumbent와 상호작용을 추가한 regularized logistic winner classifier를 chronological nested OOS로 평가했다.

- fixed poll baseline: 94/99 = 94.9%
- rich classifier: 89/99 = 89.9%

따라서 rich direction classifier는 폐기한다.

현재 primary benchmark는 계속 94/99다.

## 다음

모형 구조를 더 복잡하게 하지 않고, 아직 방향 정확도 기준으로 선택하지 않았던 poll blend 자체를 최적화한다. window, half-life, w_max, k를 이전 cycle의 winner accuracy로만 선택한다.
