# Incumbency architecture headroom diagnostic

## 날짜
2026-09-21

## 방향 정확도 비교

동일한 45-day fixed poll layer를 사용해 두 fundamentals architecture를 비교했다.

- incumbency-era prior + poll: 94/99
- no-incumbency full-cycle prior + poll: 92/99

cycle별:
- 2014: incumbency-era 32/33, no-inc 30/33
- 2018: incumbency-era 29/33, no-inc 30/33
- 2022: incumbency-era 33/33, no-inc 32/33

따라서 현직항을 전부 제거하는 것은 폐기한다.

## 중요한 headroom

cycle별로 더 좋은 architecture를 oracle로 고르면:
- 2014: incumbency-era 32/33
- 2018: no-inc 30/33
- 2022: incumbency-era 33/33

합계는 95/99다.

이 값은 outer 결과를 보고 고른 oracle이므로 채택할 수 없다. 하지만 기존 변수만으로 94/99를 넘을 구조적 headroom이 있음을 보여준다.

## 다음

각 outer cycle 이전 선거에서 두 architecture의 poll-combined winner accuracy를 rolling OOS로 계산하고, test cycle 결과를 보지 않은 상태에서 누적 historical accuracy가 더 높은 architecture를 선택하는 meta-selector를 검증한다.
