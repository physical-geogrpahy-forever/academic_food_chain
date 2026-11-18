# ChatGPT Work 인계문 — 문명 계보 / 지도자 / 위대한 혁명가

> **2026-11-18 추가 감사 알림 (기존 내용 보존):** 이 문서는 2026-10-16 당시의 **2차 인계문**으로, 한국의 시대별 문명 계보가 누락되어 있고 중국·일본도 최종 잠금된 문명 로스터가 아니다. 사용자의 이전 대화 지적·수정사항을 재검색한 회수본은 [civilizations/EAST_ASIA_12ERA_RECOVERY_V1.md](../../civilizations/EAST_ASIA_12ERA_RECOVERY_V1.md), 구체적인 회수 근거와 한계는 [CONVERSATION_DECISIONS_PROVENANCE_20261118.md](../../civilizations/CONVERSATION_DECISIONS_PROVENANCE_20261118.md), 문명 1~5 후속 작업별 색인은 [PROJECT_CONVERSATION_WORKSTREAM_INDEX_20261118.md](../../civilizations/PROJECT_CONVERSATION_WORKSTREAM_INDEX_20261118.md)를 참조할 것. **한국 12시대 사용자 원본 표는 아직 전체 미복원**이므로 추정으로 확정하지 말 것. 현재 사용자 작업 지시는 **한·중·일 문명부터, 지도자 제외, 북미·중앙아메리카·카리브 후순위**다.

Date: 2026-10-16
Project: 문명
Repository: `physical-geogrpahy-forever/academic_food_chain`
Working branch: `civ-game-map-stage1b-etopo2022`
Branch HEAD before this handoff commit: `8a5be2c750ada100ecf34aac5768b1dc16333f59`

## 0. 이 문서를 먼저 읽을 것

현재 작업의 중심은 **문명 계보와 시대별 지도자를 먼저 확정한 뒤 Great Revolutionary / 위대한 혁명가 roster로 되돌아가는 것**이다.

Great Revolutionary 시스템의 정량 규칙은 이미 V2로 잠겨 있으나, 역사인물 최종 roster는 의도적으로 중단되어 있다. 이유는 George Washington, Oliver Cromwell, Vladimir Lenin처럼 **혁명가이면서 그 혁명 이후 국가의 지도자가 되는 인물**을 먼저 문명/지도자 체계와 연결해야 하기 때문이다.

따라서 다음 Work는 Great Revolutionary 후보를 계속 줄이거나 능력을 만드는 것이 아니라 **문명 목록과 역사적 계보를 먼저 정리**해야 한다.

---

# 1. 사용자 고정 시대 구분

사용자가 현재 문명 계보표에 사용하는 시대 열은 다음과 같다.

| 시대 | 세기 범위 |
|---|---|
| 고대 | 기원전 50세기~기원전 9세기 |
| 고전 | 기원전 8세기~서기 2세기 |
| 후기 고대 | 3~6세기 |
| 중세 초기 | 7~10세기 |
| 중세 성기 | 11~13세기 |
| 르네상스 | 14~15세기 |
| 탐험 | 16~17세기 |
| 계몽 | 18세기 |
| 산업 | 19세기 |
| 현대 | 20세기 초 |
| 원자력 | 20세기 중후반 |
| 정보화 | 21세기 |

문명 계보를 제시할 때 이 12열을 기본으로 사용한다.

사용자는 **긴 설명보다 먼저 한 표에서 전체 계보가 보이는 형식**을 선호한다.

---

# 2. 문명 선정 원칙 — 현재 대화에서 확립

## 2.1 원주민 / 부족국 처리

"원주민은 제외"라는 말은 **모든 유럽 도착 이전 아메리카 정치체를 제외한다는 뜻이 아니다.**

현재 원칙:

- 분산된 부족사회와 소규모 추장국은 Civilization 목록에서 생략 가능
- 중앙집권 국가, 제국, 큰 도시국가 체계, 장기간의 고도 문명권은 Civilization으로 포함 가능
- 민족성이나 유럽 여부가 아니라 **정치적 제도화와 규모**로 판정
- Aztec, Inca, Maya, Teotihuacan 등은 부족국으로 취급하지 않는다
- Taíno의 경우 복합 추장국이지만 현재 프로젝트의 "주요 국가/문명" 해상도에서는 Cuba, Santo Domingo, Jamaica의 식민 이전 Civilization 슬롯을 비워도 된다는 방향

## 2.2 계보 화살표의 의미

모든 화살표가 직접 왕조승계를 의미하지 않는다.

구분 필요:

- 직접 국가/식민정부의 후계
- 같은 지역의 역사적 문명 중심 이동
- 정복과 흡수
- 식민정부 형성
- 독립으로 신생국 형성
- 기존 국가의 체제혁명

특히 `Olmec -> Teotihuacan -> Toltec -> Aztec`는 직계 국가승계가 아니라 중앙멕시코의 장기 지역 계보를 게임적으로 압축한 것이다.

## 2.3 작은 국가를 모두 넣지 않는다

처음에는 "큼직큼직하게, 적어도 지역 강국 수준"을 원했으나, 중앙아메리카의 경우 사용자가 **중앙아메리카 연방이 붕괴하면 실제 구성국 5개가 각각 분화되는 것**을 명시적으로 요청했다.

따라서 규모 원칙은 절대적인 컷이 아니라 지역별 역사적 계보를 설명하는 데 필요한 정도로 적용한다.

---

# 3. Great Revolutionary와 지도자의 새 방향

기존의 "지도자로 쓸 인물은 Great Revolutionary에서 제외" 규칙은 폐기 방향이다.

현재 설계 방향:

```text
Great Revolutionary 등장
-> 혁명 / 독립 / 체제변동 성공
-> 새 Civilization 또는 successor state 생성
-> 연결된 인물이라면 같은 역사적 인물이 새 국가의 Leader로 전환
```

즉 역사인물은 동시에 두 인스턴스로 존재하는 것이 아니라:

```text
Great Revolutionary -> Civilization Leader
```

의 순차 역할을 가질 수 있다.

후속 설계에서 쓸 잠정 구분:

- `REVOLUTIONARY_ONLY`
- `REVOLUTIONARY_TO_LEADER`
- `LEADER_ONLY`

대표 예시:

- George Washington (조지 워싱턴): 북미 영국 식민정부에서 미국 독립 Revolutionary로 선택 -> 미국 형성 -> Washington이 미국 지도자로 전환
- Oliver Cromwell (올리버 크롬웰): 잉글랜드 체제혁명 Revolutionary -> Commonwealth/Protectorate 경로 -> 지도자 전환 가능
- Vladimir Lenin (블라디미르 레닌): 러시아 혁명 Revolutionary -> Soviet successor-state 경로 -> 지도자 전환 가능

이 예시는 방향을 설명하는 것이며 Civilization/Leader roster가 끝나기 전까지 최종 데이터 잠금은 하지 않는다.

---

# 4. 현재 Great Revolutionary 파일 위치

권위 작업상태:

- `city_system/great_revolutionaries/WORK_STATE.md`
  - Status: SYSTEM V2 QUANTITATIVE RULES LOCKED — HISTORICAL ROSTER PAUSED PENDING CIVILIZATION / LEADER SELECTION
  - 2026-09-25 업데이트에서 문명/지도자 선행 결정이 명시됨

정량 시스템:

- `city_system/great_revolutionaries/GREAT_REVOLUTIONARY_SYSTEM_V2.md`
- `city_system/great_revolutionaries/GREP_EVENT_VALUES_V1.csv`
- `city_system/great_revolutionaries/GREP_RECRUITMENT_THRESHOLDS_V1.csv`
- `city_system/FINAL_GREAT_PERSON_RECRUITMENT_SYSTEM_V2.md`

이전 초안:

- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`

후보 연구:

- `city_system/great_revolutionaries/GREAT_REVOLUTIONARY_ENLIGHTENMENT_BROAD_CANDIDATES_V1.md`
  - 계몽시대 broad candidate pool 46명
  - leader-conflict holding pool 3명
  - **최종 roster가 아님**
  - 기존 `LEADER_CONFLICT`는 이제 "제외"가 아니라 "문명/지도자 검토 필요"로 해석해야 함

탐험시대 후보는 대화에서 연구했으나 현재 위 파일들처럼 명확한 권위 roster 파일로 잠긴 상태가 아님. Work는 파일 유무를 다시 확인하고 없는 내용을 추정하지 말 것.

---

# 5. Great Revolutionary V2 중 잠긴 숫자

문명 작업 중에도 이 값은 유지한다.

- GReP는 도시 specialist가 아니라 정치단위가 보유
- 식민정부도 본국과 별도 GReP pool
- Movement Capacity + grievance가 있어야 반복 GReP 생성
- Standard speed 구조 압력 판정: 5턴마다
- grievance 1개: +4 GReP
- 2개: +6
- 3개 이상: +8
- 영입 threshold:
  - 첫 번째 100
  - 두 번째 120
  - 세 번째 140
  - 네 번째 160
  - 다섯 번째 이상 180
- pool cap = 현재 threshold x2
- overflow 유지
- 정치단위당 unresolved Revolutionary 1명
- Revolutionary 해결 후 15턴 recruitment cooldown
- 식민지가 독립해 successor state가 되어도 GReP pool, recruitment count, cooldown을 이어받음
- 전세계 역사인물 uniqueness 유지
- Great Philosopher가 GReP를 생성/보조할 수 있으나 직군은 별개

상세는 위 V2 파일 참조.

---

# 6. Great Philosopher 관련 상태

Great Revolutionary와 교차검토가 나중에 필요하므로 보존.

권위 작업상태:

- `city_system/great_philosophers/WORK_STATE.md`
- `city_system/great_philosophers/GREAT_PHILOSOPHER_SYSTEM_V1.md`

현재 active roster는 **220명**.

시대별:
- Ancient 5
- Classical 23
- Late Antiquity 12
- Early Medieval 11
- High Medieval 17
- Renaissance 10
- Exploration 26
- Enlightenment 25
- Industrial 19
- Modern 24
- Atomic 33
- Information 15

중요 경고:
- `city_system/great_philosophers/GREAT_PHILOSOPHER_CURRENT_SUMMARY.md`가 이전 227명 상태를 담고 있을 가능성이 있으므로 **220명 최신 기준으로 재생성해야 하는 stale summary**로 취급할 것
- Tagore는 Great Writer 우선
- Laozi는 HISTORICITY_REVIEW
- Philosopher와 Revolutionary 교차감사는 Civilization/Leader 작업 이후에 진행

---

# 7. 문명 작업 — 중국 / 일본은 탐색 단계

## 7.1 중국

다음과 같은 시대 매핑이 대화에서 검토되었으나 아직 최종 Civilization table로 파일화/잠금되지 않았다.

대략:
- 고대: 상/주
- 고전: 춘추전국 -> 진 -> 한
- 후기 고대: 위진남북조 -> 수
- 중세 초기: 당
- 중세 성기: 송/요/서하/금 -> 원
- 르네상스: 원 -> 명
- 탐험: 명 -> 청
- 계몽: 청
- 산업: 청
- 현대: 중화민국
- 원자력: 중화인민공화국 / 중화민국
- 정보화: 중화인민공화국 / 중화민국

주의:
- 이것은 아직 세부 Civilization identity를 몇 개로 나눌지 결정 전
- 요/금/서하/원/청을 중국 계보와 별도 민족/정복문명으로 어떻게 처리할지 추후 결정 필요

## 7.2 일본

대화에서 검토한 큰 흐름:

- 고전: 왜
- 후기 고대: 야마타이 -> 야마토
- 중세 초기: 율령 일본 -> 헤이안
- 중세 성기: 헤이안 -> 가마쿠라
- 르네상스: 무로마치
- 탐험: 센고쿠 -> 도쿠가와
- 계몽: 도쿠가와
- 산업: 도쿠가와 -> 메이지
- 현대: 일본 제국
- 원자력: 전후 일본
- 정보화: 현대 일본

주의:
- Yamatai -> Yamato는 직접 계승이 역사적으로 확정된 것으로 쓰지 말 것
- 이 역시 아직 최종 Civilization table 잠금 전

---

# 8. 북미 식민/국가 계보 — 현재 작업 방향

사용자는 식민지 국가가 쉬우므로 여기부터 실제 문명 작업을 하기로 했다.

## 8.1 미국

현재 큰 흐름:

```text
British America / 영국령 아메리카
-> Thirteen Colonies / 13개 식민지 정치상태
-> United States / 미국
```

13개 식민지를 각각 Civilization으로 만들지 않는 방향.

Great Revolutionary/Leader 예시:
- George Washington이 미국 독립과 연결되는 `REVOLUTIONARY_TO_LEADER` 대표 사례

## 8.2 캐나다

현재 큰 흐름:

```text
New France / 누벨프랑스
-> British Canada / 영국령 캐나다
-> Dominion / Canada
-> Canada / 캐나다
```

Upper Canada / Lower Canada는 별도 완전 Civilization보다 내부 정치단위/상태로 처리하는 방향이 제안됨.

캐나다는 미국처럼 단일 혁명 독립보다 자치와 연방, 점진적 주권 확대가 중요하므로 Great Revolutionary보다 다른 정치 메커니즘 비중이 클 수 있음.

## 8.3 멕시코

이 부분은 사용자 제시 표가 가장 중요하다.

### 중앙멕시코 주계보 — 사용자가 직접 제시한 형태

| 고대 | 고전 | 후기 고대 | 중세 초기 | 중세 성기 | 르네상스 | 탐험 | 계몽 | 산업 | 현대 | 원자력 | 정보화 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 올멕 | 테오티우아칸 | 테오티우아칸 | 톨텍 | 톨텍 | 아즈텍 | 누에바에스파냐 부왕령 | 누에바에스파냐 부왕령 | 멕시코 제1제국 -> 멕시코 공화국 | 멕시코 합중국 | 멕시코 합중국 | 멕시코 합중국 |

이 흐름을 기본 중앙멕시코 계보로 유지.

### 오악사카 병렬 계보 — 사용자 제시

| 고대 | 고전 | 후기 고대 | 중세 초기 | 중세 성기 | 르네상스 |
|---|---|---|---|---|---|
| 올멕 | 사포텍 | 사포텍 | 사포텍 | 사포텍/미스텍 | 사포텍/미스텍 |

탐험 이후에는 스페인 정복에 따라 누에바에스파냐 계통으로 합류하는 방향.

### 마야

사용자는 처음 멕시코 표에서:
`마야 | 마야 | 마야 | 마야 | 마야 | 마야`
까지 두었고 이후 마야가 중앙아메리카 북부까지 걸치는 점을 확인한 뒤 **중앙아메리카 계보로 연결하는 표**를 제시했다.

따라서 마야는 "멕시코 소속 단일 문명"으로 고정하지 말고 **멕시코 남동부 + 과테말라/벨리즈/온두라스 서부/엘살바도르 일부에 걸친 광역 문명권**으로 처리해야 한다.

현재 미해결:
- 탐험시대에 마야 계보를 New Spain 쪽과 Guatemala Captaincy General 쪽으로 어떻게 분기시킬지
- 한 Maya Civilization의 영토가 식민지 경계에 따라 둘 이상의 successor colonial polity로 분할 흡수되는 것을 데이터 모델에서 어떻게 표현할지

이 문제는 다음 Work가 해결해야 하는 핵심 중 하나.

---

# 9. 중앙아메리카 — 사용자 제시안

사용자가 다음 표가 괜찮은지 확인했고, 현재 방향상 채택 가능한 형태다.

| 고대 | 고전 | 후기 고대 | 중세 초기 | 중세 성기 | 르네상스 | 탐험 | 계몽 | 산업 | 현대 | 원자력 | 정보화 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 마야 | 마야 | 마야 | 마야 | 마야 | 마야 | 과테말라 총독령 | 과테말라 총독령 | 중앙아메리카 연방공화국 -> 과테말라/니카라과/엘살바도르/온두라스/코스타리카 | 과테말라/니카라과/엘살바도르/온두라스/코스타리카 | 과테말라/니카라과/엘살바도르/온두라스/코스타리카 | 과테말라/니카라과/엘살바도르/온두라스/코스타리카 |

중요 해석:
- "Maya 전체가 5개국의 직접 조상"이라는 뜻이 아님
- 중앙아메리카 북부 마야권 일부가 스페인 식민정치체인 과테말라 총독령에 흡수되고
- 그 식민정치체가 독립 후 중앙아메리카 연방으로 이어지고
- 연방이 5개국으로 분화한다는 **지역 정치계보**
- Nicaragua와 Costa Rica 자체가 마야 핵심영역이었다는 뜻은 아님

사용자 명시 결정:
- 중앙아메리카 연방이 붕괴하면 구성국을 실제 Civilization으로 분화시킬 것
  - Guatemala / 과테말라
  - Nicaragua / 니카라과
  - El Salvador / 엘살바도르
  - Honduras / 온두라스
  - Costa Rica / 코스타리카

Panama는 이 계보가 아니라 New Granada / Gran Colombia / Colombia 계보 쪽에서 다룰 가능성이 높음.

Belize는 중앙아메리카 연방 5개국 계보에 포함되지 않음. 포함 여부는 나중에 British Honduras -> Belize로 검토.

---

# 10. 카리브 — 현재 방향

사용자가 **Cuba, Dominican Republic, Jamaica를 포함**시키라고 명시했다. Haiti도 당연히 포함되는 방향.

식민 이전:
- Cuba, Santo Domingo/Hispaniola, Jamaica의 Taíno 및 관련 정치체는 복합 추장국 수준이지만 현재 "주요 국가/문명" 해상도에서는 별도 Civilization으로 넣지 않고 빈칸 처리 가능하다고 합의 방향이 잡힘
- "문명이 없었다"가 아니라 **Civilization 슬롯 기준 아래로 생략**하는 것

## 10.1 Cuba

큰 흐름:

```text
Spanish Cuba / 쿠바 식민정부
-> Cuba / 쿠바
```

1959 Cuban Revolution은 새 Civilization 생성이 아니라 기존 Cuba의 체제혁명/지도자 변경으로 처리하는 방향.

Fidel Castro는 향후 `REVOLUTIONARY_TO_LEADER` 후보가 될 수 있음.

## 10.2 Jamaica

큰 흐름:

```text
Spanish Jamaica
-> British Jamaica / 영국령 자메이카
-> Jamaica / 자메이카
```

West Indies Federation은 역사적으로 짧고 현재 해상도에서는 별도 정식 Civilization으로 잠그지 않았으며, 대체역사 통합경로로 활용 가능.

## 10.3 Haiti / Dominican Republic — 아직 최종 잠금 전

이 부분은 사용자가 "애매하다"고 지적했고 별도 정리가 필요하다.

현재 가장 깔끔하다고 제안된 working model:

```text
[서부]
Saint-Domingue / 생도맹그
-> Haitian Revolution
-> Haiti / 아이티

[동부]
Spanish Santo Domingo / 스페인령 산토도밍고
-> 1822 Haiti에 합병/정복 상태
-> 1844 Dominican Republic / 도미니카공화국 형성
```

중요 개념:
- Dominican Republic을 `Haiti -> Dominican Republic` 단순 후계로 두지 않는다
- historical parent는 Spanish Santo Domingo
- 1844년 secession parent / liberated-from은 Haiti
- 1822~1844는 Haiti가 동부를 통치하는 합병 상태
- 1821 짧은 독립정치체, 1861~65 스페인 재병합은 별도 Civilization으로 만들지 않는 방향

하지만 **사용자가 이 구조를 최종 확정했다고 보기는 이르므로 Work는 재검토 가능**.

---

# 11. 멕시코 지역에서 검토된 주요 고도 문명

사용자는 처음에 Aztec/Inca/Maya 이전에 국가급 문명이 있는지 질문했고, 다음 원칙을 확인했다.

주요 후보:
- Olmec / 올멕
- Teotihuacan / 테오티우아칸
- Toltec / 톨텍
- Zapotec / 사포텍
- Mixtec / 미스텍
- Maya / 마야
- Purépecha / 푸레페차
- Aztec / Mexica / 아즈텍/멕시카

그 외 Xochicalco, El Tajín, Tlaxcala, Totonac, Huastec, Paquimé 등도 역사적으로 중요하지만 현재 사용자는 **"주요 국가/문명만"** 원하므로 우선 핵심 계보에서 생략.

Purépecha는 Aztec의 하위/후계가 아니라 15~16세기에 병존한 별도 서부 강국으로 봐야 함.

사용자가 원하는 표시 방식은 **긴 문명 목록보다 병렬 계보를 한 표에 놓는 것**.

---

# 12. 남아메리카는 아직 본격 착수 전

다음 큰 작업 후보.

예상해야 할 주요 축:
- Inca 및 그 이전 안데스 국가들
- Viceroyalty of Peru
- Gran Colombia -> Colombia / Venezuela / Ecuador, 그리고 Panama 연결
- Río de la Plata -> Argentina / Uruguay / Paraguay
- Brazil 식민정부 -> Empire/Republic
- Peru / Bolivia
- Chile

그러나 이것들은 아직 이 대화에서 확정하지 않았으므로 **새 Work가 조사 및 사용자 확인을 거쳐 작성할 것**.

---

# 13. Great Revolutionary로 돌아가는 시점

문명 목록과 지도자를 충분히 확정한 뒤에만 복귀한다.

복귀 후 해야 할 것:

1. Great Revolutionary V2를 leader-transition-aware V3로 수정
2. 기존 `LEADER_CONFLICT`를 제거 또는 의미 변경
3. 각 후보에:
   - `REVOLUTIONARY_ONLY`
   - `REVOLUTIONARY_TO_LEADER`
   - `LEADER_ONLY`
   중 하나를 검토
4. predecessor/successor Civilization mapping 추가
5. 역사적 기본 혁명가가 존재하는 조건에서는 후보 풀에서 우선 노출되도록 설계
6. Washington, Cromwell, Lenin, Toussaint/Dessalines, Sun Yat-sen, Mao, Castro 등은 Civilization/Leader roster와 함께 재검토
7. Philosopher / General / Writer 경계 재감사
8. 개인별 능력 설계

Great Revolutionary roster를 지금 최종화하면 안 된다.

---

# 14. 다음 ChatGPT Work가 바로 해야 할 일

현재 사용자 흐름상 가장 자연스러운 다음 작업은 **아메리카 Civilization genealogy 계속 작성**이다.

권장 순서:

1. 현재 북미 + 중앙아메리카 + 카리브 표를 하나의 authority draft로 정리
2. Maya의 Mexico/Guatemala 식민지 분기 표현을 해결
3. Haiti/Dominican 계보를 최종 사용자 확인
4. South America major civilizations/states를 같은 12시대 표 형식으로 작성
5. 그 뒤 Europe/Africa/Asia로 확장
6. Civilization roster가 상당히 정리되면 시대별 leader roster 작성
7. 이후 Great Revolutionary V3로 복귀

사용자는 "일단 주요 국가/문명만", "계보를 한 번에 표로", "국문 이름 병기"를 선호한다.

---

# 15. GitHub 작업 시 주의

- Repository: `physical-geogrpahy-forever/academic_food_chain`
- Branch: `civ-game-map-stage1b-etopo2022`
- 기본 branch와 혼동하지 말 것
- Great Revolutionary 권위 파일은 이 branch에서 확인됨
- 문명 계보 결정은 이 handoff 작성 전까지 대화에만 존재했으므로, 다음 Work가 authority civilization 파일을 새로 만들 때 이 문서를 출발점으로 사용할 것
- 기존 파일의 수치나 roster count를 추정하지 말고 실제 branch 파일을 읽고 수정할 것
- 문명/지도자 작업이 끝나기 전 Great Revolutionary 후보의 `LEADER_CONFLICT`를 최종 탈락 사유로 사용하지 말 것

---

# 16. 핵심 한 줄

**현재는 Great Revolutionary 작업을 멈추고 Civilization genealogy를 확정하는 단계다. 문명을 확정하고 시대별 Leader를 배치한 뒤, Revolutionary가 신생국/후계국의 Leader로 전환되는 V3를 만든다.**
