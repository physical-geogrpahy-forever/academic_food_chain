# VP 도시, 건물, 전문가, 교역 적용안 V1

기준일: 2026-09-23

상위 문서:
- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`

## 1. 목적

Vox Populi의 핵심 설계 중 하나인 `도시의 실제 문제를 해결하는 건물`, `전문가의 장기적 가치`, `국내/국제 교역로의 전략적 차이`를 우리 게임의 Health, Power, 기업, 동적 자원 시스템에 통합한다.

## 2. 도시 운영 원칙

도시는 단순히 Food, Production, Gold를 최대화하는 생산기지가 아니다.

도시 운영에는 최소한 다음 축이 동시에 존재한다.

- 성장
- Production
- Gold
- Science
- Culture
- Faith
- Happiness
- Health
- Power
- 방어
- Specialist
- Trade

각 건물은 이 가운데 하나 이상의 도시 문제를 해결하도록 설계한다.

## 3. 건물 역할

VP식 원칙을 기본 채택한다.

`건물 = 산출량 + 기능` 구조를 우선한다.

예:

| 건물군 | 주요 기능 |
|---|---|
| Granary/Aqueduct | 성장과 Food 안정성 |
| Market/Bank | 경제, Poverty 완화, Trade |
| Library/University | Science, 교육 부족 완화 |
| Theater/Opera/Cinema | Culture, 문화적 불만 완화 |
| Shrine/Temple | Faith, 종교 불만 완화 |
| Hospital/Medical Lab | Health |
| Sewer | Health와 도시환경 |
| Barracks/Arsenal | 군사 생산과 Supply |
| Police/Constabulary | 치안, Stability, Espionage |
| Power Plant | Power와 Production |
| Harbor/Seaport | 해상 Trade, Supply, 해외 연결 |

## 4. 기존 건물표 재감사

`FINAL_GENERIC_BUILDING_ROSTER_V1.csv`와 수치표를 VP 역할 분화 기준으로 다시 감사한다.

감사 질문:

1. 이 건물은 왜 짓는가?
2. 단순 산출량 복제 건물인가?
3. 도시의 특정 문제를 해결하는가?
4. 같은 계열 건물과 기능이 중복되는가?
5. Health/Power/Happiness와 연결해야 하는가?
6. Specialist 슬롯이 역사적으로 자연스러운가?

기존 확정 건물을 삭제하기보다는 기능을 명확히 하는 방향을 우선한다.

## 5. Specialist

VP처럼 Specialist가 후반까지 가치가 유지되게 한다.

우리 게임의 Specialist는 위인 포인트 생성뿐 아니라 도시 기능에 직접 기여한다.

예:

- Scientist: Science, Great Scientist Point
- Engineer: Production, Great Engineer Point
- Merchant: Gold, Trade, Great Merchant Point
- Writer/Artist/Musician/Director 계열: Culture/Tourism과 각 위인 포인트
- 행정 Specialist를 둘 경우: Stability, 외교, Espionage 계열

Specialist가 많아질수록 Food 또는 도시 생활비를 소비하므로 항상 최적은 아니다.

## 6. Urbanization 계열 비용

VP처럼 Specialist 사용에는 도시적 비용이 발생할 수 있다.

우리 게임에서는 별도 Urbanization 게이지를 만들지 않고 다음에 반영한다.

- Food 소비
- Housing/생활 수요가 존재할 경우 증가
- Happiness 부담
- Health 부담 가능

산업화 이후 대도시에서 Specialist가 폭증할 때 도시 서비스 건물의 가치가 생기게 한다.

## 7. 국내 Trade Route

국내 교역로는 단순 Gold보다 국가 내부의 생산과 공급망에 초점을 둔다.

가능 효과:

- Food 이전
- Production 지원
- 자원 운송
- Power/연료 공급망 보조
- 식민정부 연결
- 군사 Supply 보조

도시가 완전히 자급자족하지 않아도 교역망을 통해 전문화할 수 있다.

## 8. 국제 Trade Route

국제 교역로는 다음을 제공한다.

- Gold
- 외교 관계
- Science 교류
- Culture/Tourism 교류
- Religion 전파
- 기업 Franchise 확산
- 자원 인지와 사용권 확대

우리 게임의 동적 자원 시스템과 직접 연결한다.

## 9. 동적 자원과 교역

교역로가 새로운 생물자원과 상품을 인지하고 확산시키는 주요 수단이 된다.

예:

```text
문명 A가 Coffee를 알고 있음
+
문명 B와 지속적 국제교역
↓
문명 B가 Coffee 인지/사용권 획득 가능
```

실제 재배 가능 여부는 기후, 기술, 역사적 확산 규칙에 따라 별도로 판정한다.

## 10. Trade Route와 질병

교역로는 이익만 주지 않는다.

Health 시스템과 연결해 전염병 확산 경로가 될 수 있다.

단, 매 교역로를 복잡한 감염 네트워크로 직접 시뮬레이션하지 않고 질병 발생 시 연결도에 따른 확산확률 보정으로 처리한다.

## 11. 기업과 교역

VP Corporation 구조처럼 국제교역은 Franchise 확산의 핵심 수단이다.

Office가 있는 도시와 Franchise 도시를 연결하면 기업별 효과를 얻는다.

기업은 Trade Route 추가, 특정 산출량 강화, 상품 확산 등에 영향을 줄 수 있다.

## 12. 식민정부와 교역

식민정부는 본국과 자동으로 모든 산출량을 공유하지 않는다.

본국-식민정부 Trade Route 또는 해상 연결이 중요하다.

연결이 끊기면:

- 본국 수입 감소
- 식민정부의 자율성 증가
- 군사 Supply 악화

등이 가능하다.

## 13. 도시 전문화

VP의 도시별 차별화를 강화한다.

도시가 모든 건물을 동일하게 짓는 것을 피하고 다음 전문화가 가능해야 한다.

- 과학도시
- 산업도시
- 금융/상업도시
- 문화도시
- 군사도시
- 항구/교역도시
- 행정도시

Happiness/Health/Power 문제 때문에 무한 전문화는 제한된다.

## 14. Process

VP처럼 Production을 다른 산출로 전환하는 도시 Process를 유지할 수 있다.

가능 예:

- Research
- Wealth
- Culture
- Food 지원
- 공공 Health 대응
- 국제 프로젝트

Process는 건물 건설이 필요 없는 시기에도 Production을 활용하게 한다.

## 15. AI

AI는 건물의 단순 산출량 합이 아니라 도시의 실제 부족요인을 본다.

우선순위 예:

```text
Health 위기 → Hospital/Sewer 우선
Power 부족 → 발전시설 우선
Poverty → Market/Bank 우선
군사 Supply 부족 → Barracks/Arsenal 우선
```

Trade Route도 가장 높은 Gold만 보고 선택하지 않는다.

- 전략자원
- 기업
- 외교
- 식민지
- 국내 Food/Production 필요

를 함께 평가한다.

## 16. 그대로 복사하지 않는 것

- VP 건물별 정확한 산출량 수치
- VP Specialist 숫자
- Civ V용 Trade Route 최대거리와 수치
- VP의 Urbanization 계산식

## 17. 확정 상태

- 문제 해결형 건물: 채택
- Specialist 강화: 채택
- 국내/국제 Trade Route 역할 분화: 채택
- Trade와 동적 자원 연결: 채택
- Trade와 기업 연결: 채택
- Trade와 질병 연결: 확장 채택
- 기존 건물 roster는 유지하며 역할 재감사

상태: **V1 구조 확정, 건물별 수치 감사 필요**
