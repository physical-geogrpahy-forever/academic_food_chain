# FEC Table 2 aggregate experiment rejection

## 날짜
2026-09-21

기존 `fec18m_direction` 첫 구현은 FEC의 Congressional Candidate Table 2를 후보별 표로 잘못 가정했다. 실제 2014 workbook을 검사한 결과 Table 2는 Senate 전체 및 정당별 연도 집계표이며 개별 후보 행이 아니다.

따라서 해당 workbook으로 후보별 모금 우위를 계산하는 접근은 폐기한다. 이 실패 run은 성능 결과로 간주하지 않는다.

대체 구현은 FEC candidate master의 candidate ID/PCC를 이용해 후보를 식별하고, OpenFEC House/Senate Form 3 financial reports에서 선거연도 6월 30일 종료 보고서의 누적 재정항목을 직접 읽는다.

후보 매칭 또는 Q2 보고서가 불확실한 경우 해당 선거의 기존 94/99 baseline 예측을 그대로 유지한다.
