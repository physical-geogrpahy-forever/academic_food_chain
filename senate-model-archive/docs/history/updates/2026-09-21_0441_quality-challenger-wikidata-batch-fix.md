# QualityChallenger Wikidata batch fix

## 날짜
2026-09-21

## 첫 실행 실패 원인

후보별 `wbsearchentities` 요청을 반복하면서 GitHub Actions 공용 IP가 Wikidata HTTP 429 rate limit에 걸렸다. 모델 적합 단계에는 도달하지 못했다.

## 수정

전체 후보 이름과 이름 변형을 하나의 Wikidata SPARQL `VALUES` 질의로 묶고, 후보 P39 position held와 시작일/종료일을 한 번에 회수하도록 변경했다.

후보별 반복 네트워크 호출은 제거했다.

## 누출 방지

선거일 이전에 시작했거나 선거일 이전에 종료된 P39 claim만 자동 quality coding에 사용한다. 시작일과 종료일이 모두 없는 eligible office claim은 review로 남기고 자동 점수에는 넣지 않는다.

## 성능 판정

첫 실행은 성능 결과가 없으므로 무효다. 동일한 99-race QualityChallenger OOS 실험을 수정본으로 재실행한다.
