# Core V2-R reconstruction start

## 날짜
2026-09-21

## 이번 업데이트

Core V2의 exact 구현 산출물이 현재 복구되지 않은 상태에서, 보존된 handoff와 audit를 기준으로 `Core V2-R` 재구축을 시작한다.

## 확정된 원칙

- 기준 모델명: `Core V2`
- 재구축 모델명: `Core V2-R`
- 원 Core V2 headline benchmark:
  - RMSE 7.85%p
  - MAE 5.79%p
  - 방향 91.9%
- 재구축 모델이 유사한 수치를 내더라도 exact 원본과 동일하다고 단정하지 않는다.
- 모든 역사 검증은 rolling OOS로 한다.
- 45-day snapshot은 선거일 기준 정확히 45일 전 정보만 사용한다.
- `RelativeEconomicGrowth`는 Core 필수항으로 유지한다.
- 새 변수는 Core V2-R 재현 뒤에만 증분 시험한다.

## 재구축 순서

1. historical Senate election panel
2. presidential lean/PVI panel
3. same-seat lag
4. candidate experience panel
5. incumbency/out-party incumbent
6. personal vote panel
7. BEA historical economic snapshot
8. historical 45-day poll snapshot
9. rolling OOS estimator
10. headline benchmark reproduction audit

## 다음 작업

역사 Senate election panel의 최소 스키마와 공식 데이터 소스를 고정한다.
