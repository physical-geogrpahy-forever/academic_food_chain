# Generic Ballot OOS signal test start

## 날짜
2026-09-21

## 목적

후보효과와 PersonalVote 재구축은 현재 OOS에서 성능을 높이지 못했다. 다음으로 Core V2의 National 계열 중 직접 재구축 가능한 generic ballot 45-day signal을 시험한다.

## 단계

1. 기존 91-row diagnostic panel에서 generic ballot의 OOS 신호가 존재하는지 먼저 판정한다.
2. 개선이 있으면 99-row `last-prior + gap` SameSeat 구조에 이식한다.
3. 개선이 없으면 generic ballot 단독 National proxy는 폐기하고 다른 National 구조 또는 경제항으로 이동한다.

## 채택 기준

동일 구조 baseline 대비 combined modern OOS RMSE가 실제로 감소해야 한다.
