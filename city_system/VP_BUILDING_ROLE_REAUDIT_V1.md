# VP 기준 건물 역할 재감사 V1

기준일: 2026-09-23

대상:
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv`
- `city_system/VP_CITY_BUILDING_SPECIALIST_TRADE_V1.md`
- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`

## 1. 목적

기존 건물 roster는 유지하되 Vox Populi의 설계 원칙인 `건물이 도시의 구체적 문제를 해결한다`는 구조를 적용한다.

이번 감사의 목적은 건물을 추가 삭제하는 것이 아니라, 각 건물 chain이 어떤 도시기능을 담당해야 하는지 확정하는 것이다.

## 2. 현재 roster의 장점

현재 건물표는 이미 기능별 chain이 나뉘어 있다.

주요 chain:

- CAPITAL_ADMIN
- CITY_DEFENSE
- COMMERCE_TRADE
- CULTURE_MEDIA
- ENTERTAINMENT
- FOOD_HEALTH
- GOVERNMENT_DIPLOMACY
- INDUSTRY_POWER
- MARITIME
- MILITARY_TRAINING
- RELIGION_NATURE
- SCIENCE_EDUCATION
- AIR_SPACE
- ENVIRONMENT_INFRA

이 구조는 VP식 도시 Needs와 직접 연결하기 좋다.

## 3. chain별 기본 역할

| Chain | 1차 역할 | 2차 역할 | Happiness/정치 연결 |
|---|---|---|---|
| CAPITAL_ADMIN | 수도 행정 | 정부/외교 | Stability |
| CITY_DEFENSE | 도시 방어 | 점령/주둔 | Stability 보조 |
| COMMERCE_TRADE | Gold와 Trade | 기업/자원 유통 | Poverty 완화 |
| CULTURE_MEDIA | Culture | Great Works/Tourism | Boredom 완화 |
| ENTERTAINMENT | Happiness | Tourism | 직접 Happiness |
| FOOD_HEALTH | Food와 성장 | Health | Distress/Health 완화 |
| GOVERNMENT_DIPLOMACY | 정부/행정 | 외교/첩보 | Stability |
| INDUSTRY_POWER | Production | Power | 경제/Power 안정 |
| MARITIME | 해상 Trade | 해군 Supply | 식민 연결 |
| MILITARY_TRAINING | 군사 생산 | Supply/XP | War 대응 |
| RELIGION_NATURE | Faith | 자연/종교 | Religious Unrest 완화 |
| SCIENCE_EDUCATION | Science | Specialist | Illiteracy 완화 |
| AIR_SPACE | 항공/우주 | 프로젝트 | 후기 전략 |
| ENVIRONMENT_INFRA | 환경/재난대응 | Health | 후기 도시안정 |

## 4. VP Needs 대응

VP의 대표 도시 문제를 다음 chain에 우선 연결한다.

### Distress

우선 해결:
- FOOD_HEALTH
- 일부 INDUSTRY_POWER
- 일부 ENTERTAINMENT

대표 건물:
- Granary
- Water Mill
- Aqueduct
- 이후 위생/생활 인프라

### Poverty

우선 해결:
- COMMERCE_TRADE
- MARITIME

대표 건물:
- Market
- Bank
- Stock Exchange
- Customs Office
- Harbor/Seaport 일부

### Illiteracy

우선 해결:
- SCIENCE_EDUCATION

대표 건물:
- Library
- Paper Workshop
- University
- Chemical Laboratory
- Public School
- Research Lab

### Boredom

우선 해결:
- CULTURE_MEDIA
- ENTERTAINMENT

대표 건물:
- Amphitheater
- Opera House
- Museum
- Newspaper Office
- Cinema/Broadcast 계열
- Arena/Zoo 등

### Religious Unrest

우선 해결:
- RELIGION_NATURE

대표 건물:
- Shrine
- Temple
- Sanctuary 계열

정책에 따라 종교다양성 자체가 불행을 만들지 않을 수도 있으므로 건물 효과는 정부/정책과 함께 계산한다.

## 5. 우리 게임 추가 문제 대응

### Health

관련 chain:
- FOOD_HEALTH
- ENVIRONMENT_INFRA
- 일부 SCIENCE_EDUCATION

Hospital, Medical Lab, Sewer 등은 단순 Food/Happiness보다 Health를 직접 다룬다.

### Power

관련 chain:
- INDUSTRY_POWER

Power Plant 계열은 Production 보너스보다 우선적으로 도시 Power 공급원이다.

Nuclear Power Plant, Solar Plant 등은 `POWER_SOURCE` 상호배타 구조를 유지한다.

### Stability

관련 chain:
- GOVERNMENT_DIPLOMACY
- CAPITAL_ADMIN
- CITY_DEFENSE 일부

Courthouse, Government Plaza, Court, Consulate, Police/Intelligence 계열은 Stability와 행정비용에 영향을 준다.

### Military Supply

관련 chain:
- MILITARY_TRAINING
- CITY_DEFENSE 일부
- MARITIME 일부

Barracks, Armory, Military Academy 등은 XP뿐 아니라 Military Supply에 기여해야 한다.

### Colonial Connection

관련 chain:
- MARITIME
- COMMERCE_TRADE
- GOVERNMENT_DIPLOMACY 일부

Harbor, Seaport, Customs Office 등은 본국-식민정부 연결과 해외 Supply를 보조한다.

## 6. 주요 건물 1차 판정

### Palace

기존 역할: 수도 건물.

VP식 확장:
- 수도 행정
- 기본 Stability
- 정부기관의 기준점

### Walls / Castle / Star Fort 계열

기존 역할: 방어.

추가:
- 지역 군사 Supply 일부
- 점령/반란 방어 보정은 제한적으로 가능

단순 Happiness 건물로 만들지 않는다.

### Monument

기존 Culture 역할 유지.

초기 Boredom 감소를 직접 크게 주기보다는 Culture 생산을 통해 간접적으로 해결하도록 한다.

### Granary

Food + Health chain을 대표한다.

- Food 저장/성장
- 초기 Distress 완화
- Health는 약한 보조

### Water Mill

- Food/Production
- 초기 생활기반

Health 효과는 물 공급 인프라 의미에서 제한적으로 가능하다.

### Courthouse

정복도시/행정도시용.

- 점령 페널티 감소
- Stability 개선
- 행정비용 감소

일반 모든 도시에 필수건물로 만들지 않는다.

### Government Plaza

정부 시스템의 핵심 기관.

- 국가 Stability
- 정부 관련 Specialist/정책
- 하위 정부건물 분기

### Barracks

VP Military Supply 철학을 직접 적용한다.

- 군사경험
- 군사 생산
- 고정 Supply 증가

### Grove

자연/종교 계열.

- 자연타일 상호작용
- Faith 또는 Culture
- 직접 Religious Unrest 해결은 약하게

### Shrine / Temple

- Faith
- 종교 Specialist/위인 연계
- 종교적 불만 완화

### Library

- Science
- 교육 부족 완화
- Scientist 계열 진입점

### Caravansary

- 육상 Trade Route
- Trade range 또는 수익
- 식민정부보다 육상 교역권에 집중

### Market / Bank / Stock Exchange

- Gold
- Merchant
- Poverty 완화
- 기업/금융 연계

각 단계가 단순 Gold 숫자만 증가시키지 않도록 역할을 분화한다.

### Harbor / Lighthouse / Seaport

- 해상 Trade
- 해군 Supply
- 해외 연결
- 식민정부 연결

Food만 주는 해안 건물로 축소하지 않는다.

### Amphitheater / Opera House / Museum

- Culture
- Great Work
- Boredom 완화
- Tourism

문화 chain의 각 단계가 Great Work 슬롯과 매체 차이로 구분되게 한다.

### Arena / Circus / Zoo / Aquarium 계열

- 직접 Happiness
- Boredom 완화
- 일부 Tourism

문화건물과 달리 오락/여가가 중심이다.

### Public School

- Science
- Illiteracy 완화
- 후기 교육기반

Great Philosopher 능력의 임의적 범용 조건으로 남발하지 않는다.

### Nuclear Power Plant / Solar Plant

- Power 공급이 핵심
- 발전원별 Production/환경/자원 trade-off

Power가 충분한 도시에서 단순 Production 스택만 늘리는 구조를 피한다.

### Recycling Center / Flood Barrier

후기 환경인프라.

- 재난/환경 부담
- Health
- 자원 효율

기존 Civ 효과를 문자 그대로 복제하지 않는다.

## 7. 모든 건물에 적용할 감사 필드

향후 CSV에 다음 필드를 추가하는 것을 권고한다.

- `PRIMARY_FUNCTION`
- `NEED_RELIEF`
- `HEALTH_EFFECT`
- `POWER_EFFECT`
- `STABILITY_EFFECT`
- `SUPPLY_EFFECT`
- `TRADE_EFFECT`
- `SPECIALIST_ROLE`
- `VP_ADAPTATION_STATUS`

## 8. 금지할 설계

- 이유 없이 Happiness +1을 여러 건물에 분산
- 이유 없이 모든 건물에 Gold/Science/Culture를 조금씩 추가
- 후속 건물이 전 단계의 단순 상위호환
- Health를 Food와 완전히 동일시
- Power 건물을 단순 Production 건물로 처리
- 정부건물을 Culture 생산 건물로만 처리

## 9. 다음 작업

다음 단계는 `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv`를 건물별로 읽어 실제 수치까지 감사한다.

각 건물에 대해:

```text
현재 효과
→ VP 역할 기준
→ 중복 여부
→ Needs/Health/Power/Stability 연결
→ 유지/수정 판정
```

을 기록한다.

## 10. 상태

**건물 chain별 역할 재감사 V1 완료.**

다음: 건물별 실제 수치 전수 감사.
