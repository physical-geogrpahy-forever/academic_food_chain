# Generic Ballot parser debug

## 날짜
2026-09-21

## 직전 실패

Generic Ballot OOS 실험은 성능 계산 전에 `0 usable generic-ballot questions`로 중단됐다.

## 현재 판단

현재 FiveThirtyEight historical CSV 응답의 실제 schema 또는 응답 본문이 기존 parser 가정과 다를 가능성이 있다. 성능 결과로 간주하지 않는다.

## 수정

다음 Actions 실행에서 usable row가 100개 미만이면 실제 field names와 raw response 앞부분을 오류 로그에 출력한다. 이를 바탕으로 parser만 수정한 후 동일 OOS 실험을 재실행한다.
