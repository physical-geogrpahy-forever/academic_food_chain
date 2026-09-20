# Poll stack decision

## 날짜
2026-09-21

## 결과

기존 94/99 fixed poll blend 위에 과거 cycle로 학습한 stacked logistic classifier를 추가했으나 성능이 악화됐다.

- baseline fixed poll blend: 94/99 = 94.9%
- stacked classifier: 91/99 = 91.9%
- net: -3 correct races

cycle별:
- 2014: 32/33 -> 29/33
- 2018: 29/33 -> 30/33
- 2022: 33/33 -> 32/33

stack은 2018 Nevada를 고쳤지만 2014 Iowa, Alaska, Arkansas와 2022 Nevada를 새로 틀렸다.

## 판정

전역 stacked classifier는 폐기한다.

현재 primary benchmark는 계속 94/99 = 94.9%다.

## 다음

전역 winner classifier 대신 pollster별 historical house effect를 test cycle 이전 선거에서만 추정해 poll margin 자체를 보정한다. 보정 shrinkage는 이전 cycle의 poll-direction accuracy로만 선택하고, outer 2014/2018/2022 결과는 선택에 사용하지 않는다.
