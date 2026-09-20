# GovernorExperience parent-child identity fix

## 날짜
2026-09-21

## 발견

NGA 교차검증 첫 결과에서 2018 Pennsylvania Democratic candidate `Robert P. Casey Jr.`가 전 Pennsylvania governor `Robert P. Casey`와 같은 인물로 처리되어 GovernorExperience가 0에서 1로 잘못 보정되었다.

## 외부 검증

- U.S. Senate의 Pennsylvania senator history는 해당 후보를 `Robert P. Casey, Jr.`로 기록한다.
- Senate 기록에서 Casey Jr. 본인이 전 Pennsylvania governor Robert P. Casey를 자신의 아버지라고 명시한다.

따라서 두 인물은 동일인이 아니다.

## 수정 규칙

- 느슨한 이름 정규화는 후보 탐색에만 사용한다.
- NGA를 이용해 기존 0을 1로 새로 올리는 경우에는 generational suffix(`Jr.`, `Sr.`, `II`, `III`, `IV`)가 서로 충돌하지 않아야 한다.
- suffix mismatch가 있으면 NGA match가 높더라도 신규 GovernorExperience override를 만들지 않는다.
- 기존 election-history positive는 NGA 매칭 실패나 suffix mismatch 때문에 0으로 내리지 않는다.

## 기대 결과

재실행 후 신규 NGA 기반 GovernorExperience 보정은 Robert P. Casey Jr.를 제외하고 실제 같은 인물로 확인되는 사례만 남아야 한다.
