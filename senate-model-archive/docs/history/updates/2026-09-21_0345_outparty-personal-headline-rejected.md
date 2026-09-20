# OutPartyIncumbent + headline PersonalVote decision

## 날짜
2026-09-21

## 결과

fixed poll posterior에 out-party incumbent penalty와 headline PersonalVote 보호효과를 추가했으나 combined direction accuracy가 악화됐다.

- baseline: 94/99 = 94.9%
- adjusted: 93/99 = 93.9%

2018에서는 29/33 -> 30/33으로 1개 개선했지만, 2022에서 33/33 -> 31/33으로 2개를 잃었다.

2018에서 Nevada, Missouri, Indiana를 고쳤지만 Montana와 West Virginia를 새로 틀렸다.

## 해석

문제는 out-party penalty 자체보다 PersonalVote 학습자료 부족이다. 2018 계수는 2014 headline 한 cycle만으로 선택됐기 때문에 strong personal-brand incumbent를 보호하는 구조를 충분히 학습하지 못했다.

## 다음

PersonalVote history를 headline 2014/2018/2022에 한정하지 않고 역사 Senate 후보별로 재구축한다. 각 후보의 이전 Senate race overperformance를 cycle-adjusted residual로 계산하고, 이 역사 PersonalVote를 이용해 out-party penalty와 personal protection을 이전 cycle 전체에서 학습한다.
