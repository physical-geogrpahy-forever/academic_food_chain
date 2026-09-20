# Pollster house-effect decision

## 날짜
2026-09-21

## 결과

historical Senate poll errors로 pollster house effect를 추정하고 test cycle 이전 자료만으로 shrinkage를 선택했으나 fixed blend보다 악화됐다.

- fixed unadjusted poll blend: 94/99 = 94.9%
- pollster house-effect adjusted: 92/99 = 92.9%

따라서 pollster house-effect 보정은 현재 모델에서 폐기한다.

현재 primary benchmark는 계속 94/99다.

## 다음

전역 poll 보정은 중단한다. fixed blend의 posterior direction을 기본으로 유지하고, posterior와 poll sign이 충돌하는 경우에만 이전 cycle에서 학습된 단순 selective override rule이 flip을 허용하는 보수적 구조를 시험한다.
