# VP AI와 난이도 적용안 V1

기준일: 2026-09-23

상위 문서: `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`

## 1. 목적

Vox Populi의 핵심 가치 가운데 하나인 `AI가 실제 규칙을 이해하고 사용하는 방향`을 우리 게임 전체 시스템에 적용한다.

난이도는 AI가 시스템을 못 쓰기 때문에 생산량 보너스를 과도하게 받는 구조보다, AI가 전략을 이해한 뒤 필요한 범위에서 보정을 받는 구조를 목표로 한다.

## 2. AI 계층

AI를 최소 다음 층으로 나눈다.

- Grand Strategy
- Diplomacy
- Military Strategy
- Tactical Combat
- City Strategy
- Production
- Technology
- Civics/Policy
- Religion
- Espionage
- Trade
- Great Person
- Colonial Government
- Corporation

각 시스템의 AI는 공통 평가함수를 공유하되 독립된 우선순위를 가진다.

## 3. Grand Strategy

AI는 현재 국가의 장기 목표를 판단한다.

예:

- 군사 팽창
- 과학
- 문화/관광
- 외교
- 경제/기업
- 종교
- 식민제국

Grand Strategy는 영구 고정값이 아니라 시대와 상황에 따라 조정된다.

## 4. 도시 AI

도시는 단순 `가장 높은 산출량 건물`을 짓지 않는다.

도시의 부족요인을 먼저 평가한다.

```text
Health 위기
→ 의료/위생 건물 가중치 상승

Power 부족
→ 발전시설 가중치 상승

Poverty 심각
→ Market/Bank 가중치 상승

War Weariness 높음
→ Happiness 관련 건물과 평화 전략 가중치 상승
```

전문화된 도시는 해당 역할의 가중치를 추가로 받는다.

## 5. 군사 전략 AI

AI는 전쟁 전 다음을 평가한다.

- 상대 전력
- 국경과 지형
- War Weariness
- Military Supply
- 해외보급
- 목표 도시 가치
- 동맹관계
- 전쟁 목표

장거리 식민전쟁은 본토 인접전쟁보다 비용을 높게 평가한다.

## 6. Tactical AI

VP식 전술 개선을 목표로 한다.

필수 판단:

- 전선 유지
- 집중공격
- 후퇴
- 공성유닛 보호
- 원거리유닛 보호
- 기병 우회
- 해군과 상륙작전
- 항공지원
- 보급선 고려

각 유닛은 자신의 역할에 맞는 목표함수를 가져야 한다.

## 7. 외교 AI

외교는 단일 호감도 숫자로만 결정하지 않는다.

평가요소:

- 군사위협
- 국경경쟁
- 장기 동맹
- 배신
- 종속국 관계
- 도시국가 경쟁
- 종교
- Trade
- 기업
- 세계의회
- 독립/식민문제

장기 기억과 최근 사건을 구분한다.

## 8. 정책과 정부 AI

새 정부가 해금되었다고 즉시 교체하지 않는다.

AI는 다음을 계산한다.

```text
새 정부 기대효과
-
Culture 전환비용
-
Stability 손실
-
과도기 비용
```

Great Revolutionary가 있으면 전환비용 평가를 다시 계산한다.

정책카드도 현재 전쟁, 경제, 건설 계획 등에 따라 바꾸되 교체비용을 고려한다.

## 9. 식민정부 AI

식민정부는 별도 하위 AI를 가진다.

평가:

- 지역 성장
- 방어
- 본국 관계
- 세금/부담
- Happiness
- GReP
- 자치도
- 독립 가능성

Great Revolutionary가 등장한 뒤에도 무조건 독립하지 않는다.

자치령 유지와 독립전쟁의 기대효용을 비교한다.

## 10. 종주국 AI

종주국은 식민지에 대해 다음 선택을 비교한다.

- 직접통제 강화
- 자치 확대
- 세금 인하
- 군사 진압
- 자치령 전환

식민지 유지비와 얻는 자원을 함께 평가한다.

## 11. 기업 AI

AI는 가능한 첫 기업을 무조건 창업하지 않는다.

평가요소:

- 자원 공급망
- Monopoly
- Great Person 기회비용
- Trade Route 수
- 국내 도시 전문화
- 해외 Franchise 가능성
- 경쟁기업

Great Merchant와 Great Engineer의 다른 사용처와 비교한다.

## 12. Great Person AI

위인마다 고유능력이 다르므로 단일 사용규칙을 쓰지 않는다.

AI 데이터에 다음을 기록한다.

- 즉시 사용 기대값
- 특정 도시 사용
- 전쟁 중 가치
- 정부교체 연계
- 기업 창업 연계
- 독립 연계

후보 영입 단계에서도 현재 전략과 인물의 능력을 평가한다.

## 13. 종교 AI

종교 AI는 다음을 판단한다.

- Pantheon/Belief 시너지
- 현재 도시구조
- 확산경로
- 외교비용
- 종교건물
- Faith의 다른 사용처

Great Prophet이 Faith 직접 구매 방식이므로 Prophet 구매와 다른 Faith 소비의 기회비용을 비교한다.

## 14. Espionage AI

Spy 임무는 목표별 기대효용을 계산한다.

- 기술격차가 크면 기술절도
- 전쟁 전 군사정보
- 위험한 적에게 방첩
- 도시국가 경쟁
- 기업정보

Great Revolutionary와 역할을 혼동하지 않는다.

## 15. Trade AI

Trade Route는 최대 Gold만으로 결정하지 않는다.

가중요소:

- Food/Production 국내지원
- Gold
- Science/Culture 교류
- 자원 인지
- 기업 Franchise
- 종교
- 외교
- 식민정부 연결
- 질병 위험

## 16. 난이도 설계

난이도는 두 층으로 나눈다.

### AI 의사결정 품질

난이도와 무관하게 가능한 한 높은 수준을 유지한다.

### 수치 보정

난이도가 높을수록 제한적으로:

- Production
- Gold
- Science
- Culture
- 유닛 유지
- Happiness/Needs

등을 보정할 수 있다.

그러나 AI의 잘못된 행동을 수치로 덮는 것을 피한다.

## 17. 숨은 보너스 최소화

가능하면 플레이어가 AI의 난이도 보정을 이해할 수 있게 한다.

난이도 화면에 주요 보너스 범주를 명시한다.

## 18. VP 코드 참고 범위

VP 공식 저장소에는 `CvPlayerAI.cpp`, `CvCityStrategyAI.cpp` 등 핵심 AI 코드와 각종 시스템별 AI 로직이 포함되어 있다.

우리 게임은 엔진이 다르므로 코드를 그대로 이식하는 것이 아니라 판단구조와 평가항목을 참고한다.

## 19. AI 테스트

최소 다음 시나리오를 자동 테스트한다.

- 평시 100턴 경제
- 인접국 전쟁
- 장거리 해외전쟁
- 식민정부 성장
- 식민정부 독립위기
- 기업 창업과 해외확장
- 정부교체
- War Weariness 위기
- 도시 Health/Power 위기

각 시나리오에서 AI의 선택 로그를 저장한다.

## 20. 확정 상태

- VP식 AI 강화 철학: 채택
- 도시 문제 해결형 AI: 채택
- 전쟁비용과 Supply 판단: 채택
- 식민정부 AI: 우리 확장
- 기업 AI: 우리 확장
- 정부교체 비용 판단: 우리 확장
- 난이도 수치보너스는 보조수단: 확정

## 21. VP 확인 자료

- `CvGameCoreDLL_Expansion2/CvPlayerAI.cpp`
- `CvGameCoreDLL_Expansion2/CvCityStrategyAI.cpp`
- VP 공식 저장소의 전술, 외교, 경제 AI 코드

상태: **V1 원칙 확정, 실제 평가함수와 가중치 미구현**
