# FEC candidate name-order match fix

## 날짜
2026-09-21

candidate-level Form 3 Q2 API 조회는 정상 작동했지만 finance coverage가 0으로 남았다.

후보 매칭 감사를 확인한 결과 FEC candidate master는 일반적으로 `LAST, FIRST MIDDLE` 형식이고, headline 데이터는 `First Middle Last` 형식이다. 기존 matcher는 쉼표를 삭제하기만 해 `udall mark e`와 `mark udall`을 비교했고 대부분의 정상 후보를 낮은 유사도로 탈락시켰다.

수정:

- FEC 이름에 쉼표가 있으면 `LAST, FIRST MIDDLE`을 `FIRST MIDDLE LAST`로 재배열한다.
- 문자열 유사도 외에 surname exact match, first-name/initial match, token overlap, party consistency를 함께 사용한다.
- 후보/보고서 매칭이 불확실하면 계속 baseline을 유지한다.

앞선 0-coverage 결과는 성능 결과로 채택하지 않는다.
