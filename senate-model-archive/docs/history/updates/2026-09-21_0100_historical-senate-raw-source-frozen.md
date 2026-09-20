# Historical Senate raw source frozen

## 날짜
2026-09-21

## 작업

FiveThirtyEight 공개 `election-results` 저장소의 `election_results_senate.csv`를 현재 GitHub 아카이브에 frozen raw copy로 보존했다.

## 원본

- repository: `fivethirtyeight/election-results`
- path: `election_results_senate.csv`
- ref: `main`
- source blob SHA: `85ce75b587257b06208db6c9f1e3d0031aa16eae`
- frozen archive path:
  `data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv`

## 이 자료를 사용하는 이유

- Senate election result를 후보 단위로 표준화한다.
- cycle, stage, special, office seat/class, party, candidate, votes, percent, winner, source를 함께 가진다.
- 각 결과의 원 출처 URL이 포함되어 있어 주정부/FEC 공식 결과와 교차검증할 수 있다.
- 장기 시계열의 상당 부분은 MIT Election Lab 자료를 포함해 표준화되어 있다.

## 검증 전략

작업용 canonical raw source는 frozen 538 CSV로 두되, Core V2-R headline에 직접 쓰이는 2006, 2010, 2014, 2018, 2022 Senate general results는 FEC Federal Elections 공식 편찬물과 cycle별로 교차검증한다.

## 아직 하지 않은 것

- regular election과 special election 포함 여부 최종 확정
- fusion voting / multi-ballot-party 중복표 처리
- independent 후보를 D/R alignment에 어떻게 연결할지 확정
- unopposed race 처리
- runoff 및 ranked-choice 최종 round 처리
- Core V2 원 구현과 동일한 race inclusion rule 복구

따라서 raw copy를 저장했다고 해서 곧바로 모델 입력 패널로 사용하지 않는다.

## 다음 작업

`race_id` 단위로 2006~2024 general-election 구조를 감사하고, D/R margin을 만들 때 필요한 예외 케이스를 목록화한다.
