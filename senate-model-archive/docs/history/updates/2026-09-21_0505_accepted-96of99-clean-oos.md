# Accepted direction benchmark: 96/99 clean nested OOS

## 날짜
2026-09-21

## 변경

기존 fixed-poll baseline 94/99보다 높은 clean nested OOS 결과를 확인했다.

outparty_closepoll_calibrated selector는 각 outer cycle 이전 자료만 사용하여 threshold를 선택한다.

평가 순서:
1. winner-direction accuracy
2. Brier score / log loss
3. MAE
4. complexity

## 결과

- combined: **96/99 = 97.0%**
- 2014: 32/33
- 2018: 32/33
- 2022: 32/33

따라서 현재 accepted primary benchmark를 94/99에서 **96/99**로 갱신한다.

남은 오답:
- 2014 North Carolina
- 2018 Montana
- 2022 Nevada

## 제3후보 audit

NC 2014는 Sean Haugh를 포함한 다자구도였다. 45-day 직전 historical multi-candidate poll average에서 explicit third-party support는 약 5.6%, actual non-D/R share는 약 3.78%였다.

다만 2006-2022 archived daily table coverage를 확장해도 ordinary minor-third-party 3-15% context로 복원된 race-cycle은 NC 2014 한 건뿐이었다. 따라서 directional point correction을 학습하기에는 표본이 부족하다.

현재 제3후보 정보는 uncertainty/calibration 후보로 취급하고, NC를 억지로 방향 보정하지 않는다.

## 다음

MT 2018과 NV 2022는 동일 close-poll override의 과잉적용이다.
poll-PVI agreement 상태별 threshold와 minimum |PVI|를 prior-cycle data에서만 선택하는 selector를 시험한다.