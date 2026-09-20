# Candidate-block performance decision correction

## 날짜
2026-09-21

## 첫 실제 OOS 결과

2014, 2018, 2022 결합 진단에서:

- structural_only: RMSE 11.1097
- candidate_fixed: RMSE 12.0664
- candidate_ridge_nested: RMSE 11.9132

Nested ridge는 무규제 후보블록보다 0.1533%p 개선됐지만 structural-only보다 0.8035%p 나빴다.

## 정정

자동 생성 MD의 기존 `KEEP_FOR_CORE_V2R_NEXT_STAGE` 판정은 비교 기준을 candidate_fixed로만 잡은 논리 오류였다. 성능 향상 목적에서는 structural-only보다 좋아져야 채택할 수 있다.

따라서 현재의 전체 candidate block ridge는 **REJECT**한다.

## 다음 성능 실험

후보 변수를 전부 강제로 넣지 않는다. `IncumbencyDiff`, `OutPartyIncumbent`, `SenateExperienceDiff`, `GovernorExperienceDiff`, `HouseExperienceDiff`의 모든 부분집합과 candidate ridge 강도를 training-only nested rolling OOS에서 선택한다. 빈 부분집합도 후보에 포함해, 후보효과가 도움이 되지 않으면 구조모형으로 자동 복귀하게 한다.
