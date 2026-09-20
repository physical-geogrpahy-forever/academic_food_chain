# FEC finance source switch after OpenFEC rate limit

## 날짜
2026-09-21

후보 이름 정규화 문제를 수정한 뒤 candidate master에서 PCC를 확보하고 OpenFEC Form 3 Q2를 조회하는 단계까지 진행했으나, 공유 `DEMO_KEY`가 HTTP 429 rate limit에 걸려 재현 가능한 대량 실험을 완료할 수 없었다.

API 호출을 반복하지 않는다.

대체 자료원은 FEC가 선거연도 6월 30일까지의 Form 3 자료로 직접 생성한 18-month Top 50 Senate campaign tables다.

- 6a: receipts
- 6b: contributions from individuals
- 6f: cash on hand

각 metric에서 D/R 양 후보가 모두 Top 50에 있을 때만 race-level finance share를 계산한다. 한 후보가 표에 없으면 0으로 간주하지 않고 해당 metric을 missing으로 유지한다. Finance signal이 없는 race는 94/99 fixed-poll baseline을 그대로 유지한다.
