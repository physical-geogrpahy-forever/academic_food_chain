# CIV GAME PROJECT MASTER HANDOFF — 2026-09-20

Repository: `physical-geogrpahy-forever/academic_food_chain`  
Authoritative branch: `civ-game-map-stage1b-etopo2022`

Status: **MASTER HANDOFF / 다음 채팅 인계용**

이 문서는 현재 프로젝트 전체 상태를 한 번에 이어가기 위한 통합 인계문서다.  
기존의 지도/자원 handoff, 사회제도, 기술, 도시 시스템, 위대한 감독, 기업 시스템 문서를 하나의 작업 순서로 묶는다.

---

# 0. 가장 중요한 현재 위치

현재 프로젝트는 다음 순서까지 진행됐다.

1. 세계지도 기본 격자와 지형/바이옴 기반 확정
2. 47개 지도 자원 로스터 확정
3. Stage10Y 12,500개 자원 배치 프리뷰 생성
4. BISON / IVORY / WHALES 문제를 수정한 `resource_fix_v1` 검토본 생성
5. **4000 BCE 기준 자원 발견/전파 시스템 V2 + 역사 마스크 V3 확정**
6. 72개 사회제도 로스터 확정
7. 사회제도 간 역사 흐름 V3 확정
8. 109개 과학기술 로스터와 기술 DAG V2 확정
9. 사회제도-과학기술 HARD/BOOST 교차조건 검증
10. 도시 운영은 **Civilization V식 비지구형 도시 시스템**으로 확정
11. 위대한 감독 / 영화 명작 시스템 포함 확정
12. 기업은 Wonder형이 아니라 **위대한 상인/위대한 기술자가 설립하는 비독점 업종 시스템**으로 설계 중
13. 기업 창업가 1차 대규모 후보조사는 실제로 저장돼 있음
14. **기술별 유닛/건물/시설/자원 해금을 붙이려다가, 기업이 건물과 자원가공 구조에 직접 영향을 주므로 기업 시스템을 먼저 확정하기로 하고 중단한 상태**

따라서 다음 채팅에서는 **기업 시스템 확정 및 창업가 풀 확장**부터 이어가야 한다.

---

# 1. GitHub 기준

## Repository

`physical-geogrpahy-forever/academic_food_chain`

## Branch

`civ-game-map-stage1b-etopo2022`

이 branch를 현재 권위 있는 작업 branch로 사용한다.

## 기존 종합 handoff

`CIV_GAME_MAP_STAGE10_CURRENT_HANDOFF_2026-09-20.md`

이 파일은 지도/자원 작업에서 시작해 사회제도, 기술, 도시, 기업까지 계속 누적돼 있다.

## 이 문서

`CIV_GAME_PROJECT_MASTER_HANDOFF_2026-09-20.md`

앞으로 다음 채팅은 우선 이 문서를 읽고, 세부 수치나 구현이 필요할 때 아래 권위 파일을 읽는 방식으로 진행한다.

---

# 2. 세계지도 제작 기준

## 기본 격자

- CRS: EPSG:8857
- Parent grid: 335 x 781
- 전체 hex: 261,635

Surface:
- LAND: 68,048
- LAKE: 882
- COAST: 8,781
- OCEAN: 156,201
- VOID: 27,723

## 지형/고도 기준

- Stage1A의 1-degree 자료는 폐기됨
- Stage1B relief는 **NOAA ETOPO 2022 v1 60 arc-second**
- Stage2B terrain/biome이 현재 지형/바이옴 기준

## 중요한 위치 검증 원칙

과거 TIFF/PNG 프리뷰에서 자원 아이콘 위치가 틀어진 문제가 있었다.

원인:
- source GPKG geometry를 직접 렌더링하지 않고 image-coordinate 변환으로 overlay

따라서:
- 위치 검증은 반드시 **source GPKG geometry 기준**
- old image-coordinate overlay는 positional QA에 사용하지 않는다

한국 지역 검증에서 실제 LAND 자원이 존재했으므로, 옛 PNG에서 안 보이던 것은 배치 부재가 아니라 렌더링 오류였다.

---

# 3. 지도 자원 로스터 — 47개 확정

## Strategic 7

- HORSES
- IRON
- NITER
- COAL
- OIL
- ALUMINUM
- URANIUM

## Bonus 10

- BANANAS
- BISON
- CATTLE
- DEER
- FISH
- SHEEP
- STONE
- WHEAT
- MAIZE
- RICE

## Luxury 30

- CITRUS
- COCOA
- COPPER
- COTTON
- CRAB
- DYES
- FURS
- GEMS
- GOLD
- INCENSE
- IVORY
- MARBLE
- PEARLS
- SALT
- SILK
- SILVER
- SPICES
- SUGAR
- TRUFFLES
- WHALES
- WINE
- COFFEE
- TEA
- TOBACCO
- OLIVES
- PERFUME
- AMBER
- JADE
- LAPIS_LAZULI
- CORAL

Display:
- COCOA는 내부 ID 유지, 아이콘은 chocolate 형태
- PERFUME 한국어 표기는 향수
- internal ID는 바꾸지 않는다

---

# 4. Stage10Y 자원 배치 상태

## 목표 및 실제

총 12,500 cells.

- Strategic: 2,500
- Bonus: 5,000
- Luxury: 5,000

one-resource-per-hex: PASS

Surface:
- LAND: 10,896
- COAST: 639
- OCEAN: 965
- LAKE: 0
- VOID: 0

## 현재 상태

**아직 canonical final이 아니다.**

현재 핵심 검토본:
`civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`

이 파일은 12,500-row 통합 배치표다.

## resource_fix_v1

BISON, IVORY, WHALES만 교체했다.

기존 문제:
- BISON top plateau 후보가 너무 많아 desert 선택 발생
- IVORY도 plateau 때문에 desert/temperate 오류
- WHALES가 남반구에 지나치게 편중

수정:
- BISON desert: 21 -> 0
- IVORY desert: 44 -> 0
- IVORY temperate: 8 -> 0
- WHALES north/south: 14/336 -> 174/176 수준으로 균형 보정

Status:
- **review build**
- final canonical placement 아님

## 자원 아이콘

`civ_map_stage10_resources/icons_v4/`

V4가 현재 아이콘 기준.

---

# 5. 가장 중요한 시스템 — 자원 발견/전파 V2

권위 파일:
- `civ_map_stage10_resources/contact_dynamic_resource_system_v2.md`
- `civ_map_stage10_resources/resource_transfer_classes_v2.csv`

**V1 확률확산/stock 시스템은 폐기. 다시 도입하지 않는다.**

## 설계 철학

Stage10의 현대 잠재분포 셀은 그대로 유지한다.

그러나 4000 BCE에 역사적으로 존재하지 않았던 지역에서는 처음부터 보이지 않는다.

플레이어가 자원을 임의로 지도에 생성하거나 심는 시스템이 아니다.

## Cell state

### START_VISIBLE

4000 BCE 무렵 실제 자원 또는 직접 이용 가능한 source population이 존재.

- 탐험하면 누구나 아이콘 확인 가능
- 단순 발견만으로 civilization-wide possession은 얻지 않음

### LATENT

현대 잠재분포로는 존재하지만 4000 BCE에는 아직 해당 지역에 없던 cell.

- 해당 자원을 획득하지 않은 문명에게는 숨김

### ACTIVE_INTRODUCED

LATENT였지만 플레이 과정에서 실제로 도입된 cell.

- 물리적으로 현실화됨
- 이후 탐험하는 모든 문명에게 보임

## Civilization state

핵심:
`has_resource[civ][resource]`

V2는 단순화 시스템이므로 다음은 사용하지 않는다.

- city stock
- regional stock
- 확률 확산
- adjacency spread
- neighbor diffusion
- 복잡한 population diffusion

## 획득 방법

- START_VISIBLE source 지역을 정착/영유
- 이미 가진 문명과 무역
- 가진 문명의 도시 정복
- 첫 접촉만으로는 획득되지 않음

한 번 획득한 resource possession은 V2에서 지속된다.

## LATENT visibility

문명이 어떤 동적 자원을 획득하면:

**그 자원의 Stage10 현대 잠재분포 중 이미 탐험한 LATENT cell을 해당 문명이 볼 수 있다.**

핵심 해석:

> 자원 획득 = 그 자원의 현대 잠재분포를 해당 문명에게 해금

단:
- 자원을 새 좌표에 생성하는 것이 아니다
- Stage10에 이미 선택된 cell만 사용한다

## Settlement introduction

자원을 이미 가진 문명이 LATENT cell을 포함한 지역에 정착하면:
- 그 이미 존재하는 Stage10 LATENT cell을 ACTIVE_INTRODUCED로 전환 가능

이후 해당 cell은 세계적으로 실제 존재하는 자원으로 취급한다.

## 대표 예시 — 말

- 아메리카 HORSES modern-potential cell은 4000 BCE LATENT
- 스페인이 말을 보유하고 아메리카를 탐험하면 자기에게 latent horse potential이 보임
- 스페인이 그 영역에 정착하면 해당 Stage10 HORSES cell을 ACTIVE_INTRODUCED로 현실화 가능
- Native 문명이 식민도시를 점령하면 HORSES 획득 가능
- 이후 Native 문명도 자기 explored HORSES latent cell을 볼 수 있음
- 다시 다른 문명과 무역으로 전달 가능

역사 연도를 hard-code하지 않는다.

Alternate history에서 접촉이 빨라지면 자원 전파도 빨라질 수 있다.

---

# 6. 동적 전파 대상 18개

다음 18개만 현재 V2 dynamic set.

Plants/composite:
- BANANAS
- CITRUS
- COCOA
- COFFEE
- COTTON
- DYES
- MAIZE
- OLIVES
- RICE
- SPICES
- SUGAR
- TEA
- TOBACCO
- WHEAT
- WINE

Domestic animals:
- HORSES
- CATTLE
- SHEEP

Important:
- DYES 하나로 유지
- SPICES 하나로 유지
- PERFUME dynamic에서 제외
- SILK, INCENSE는 현재 18개 set에서 제외 및 deferred
- wild biological resources는 이동 시스템 대상 아님
- geological/mineral resources는 fixed

특수:
- NITER 자연 cell은 fixed. 별도 기술/시설로 saltpetre 제조 가능성
- SALT 자연 cell은 fixed. 해안 saltworks 같은 개선/시설로 생산 가능. 일반 city building으로 처리하지 않는 방향

---

# 7. 4000 BCE 역사 마스크 V3

권위 directory:
`civ_map_stage10_resources/history_4000bce_v3/`

Files:
- `README.md`
- `resource_start_visible_4000bce_mask_regions_v3.csv`
- `apply_resource_history_4000bce_v3.py`
- `resource_history_4000bce_exact_summary_v3.csv`
- `resource_history_4000bce_critical_checks_v3.csv`

V1은 superseded.

## Exact result

18 dynamic resource cells:
- total: 6,630
- START_VISIBLE: 1,950 = 29.4%
- LATENT: 4,680 = 70.6%

| Resource | START_VISIBLE | LATENT | Total |
|---|---:|---:|---:|
| BANANAS | 48 | 373 | 421 |
| CATTLE | 155 | 466 | 621 |
| CITRUS | 17 | 249 | 266 |
| COCOA | 24 | 146 | 170 |
| COFFEE | 8 | 192 | 200 |
| COTTON | 40 | 195 | 235 |
| DYES | 71 | 12 | 83 |
| HORSES | 293 | 830 | 1123 |
| MAIZE | 22 | 491 | 513 |
| OLIVES | 152 | 79 | 231 |
| RICE | 62 | 387 | 449 |
| SHEEP | 357 | 256 | 613 |
| SPICES | 215 | 97 | 312 |
| SUGAR | 39 | 191 | 230 |
| TEA | 45 | 111 | 156 |
| TOBACCO | 34 | 199 | 233 |
| WHEAT | 195 | 287 | 482 |
| WINE | 173 | 119 | 292 |

Critical PASS:
- Americas HORSES: 472 checked, START_VISIBLE 0
- Americas CATTLE: 267, 0
- Americas SHEEP: 32, 0
- Korea RICE: 7, 0
- Mesoamerica MAIZE: 23, 22 visible
- Upper Amazon COCOA: 24/24 visible
- Ethiopia/Boma COFFEE: 8/8 visible
- China RICE: 62/62 visible

## Korea

현재 Korea window의 dynamic cells는 전부 4000 BCE LATENT:
- CATTLE 1
- CITRUS 2
- HORSES 6
- MAIZE 1
- RICE 7
- TOBACCO 4
- WINE 4

이것은 한국에 자원이 없다는 뜻이 아니다.
static mineral/wild resource는 별도다.

예:
Yangtze 지역 RICE를 가진 문명과 접촉/무역하면 한국 문명도 RICE possession을 획득하고 자기 LATENT RICE를 확인할 수 있다.

## SUGAR special

New Guinea only mask는 현재 Stage10 selected SUGAR cell과 겹치지 않아 0 visible이 됐다.

V3는 broad gameplay envelope:
- 95–130E
- 10S–20N

결과:
- START_VISIBLE 39
- LATENT 191

---

# 8. 사회제도 — 72개 확정

권위 roster:
- `civics_reference/CIVIC_ROSTER_LOCKED_V1.md`
- `civics_reference/civic_roster_locked_v1.csv`

사회제도 기본 철학:
1. Civ VI Gathering Storm 우선
2. Civ V BNW에서 실제 gap만 보충
3. Civ V era-mod에서 gap 보충
4. 새로운 original civic은 최후 수단
5. Civ VI에 같은 이름/기능 또는 상위 개념이 있으면 Civ VI 우선

## Era counts

- Ancient: 7
- Classical: 5
- Late Antiquity: 4
- Early Medieval: 4
- High Medieval: 4
- Renaissance: 4
- Exploration: 6
- Enlightenment: 5
- Industrial: 9
- Modern: 6
- Atomic: 5
- Information: 7
- Future: 6

Total: **72**

## Civ VI 외 추가 11개

- Written Culture
- Court Culture
- Scholasticism
- Patronage
- Print Culture
- Scientific Revolution
- Sovereignty
- Constitutionalism
- Public Sphere
- Romanticism
- Labor Movement

## 시대별 핵심 추가

Early Medieval:
- Written Culture
- Court Culture

High Medieval:
- Scholasticism

Renaissance:
- Patronage
- Print Culture

Exploration:
- Scientific Revolution
- Sovereignty

Enlightenment:
- Constitutionalism
- Public Sphere

Industrial:
- Romanticism
- Labor Movement

---

# 9. 사회제도 역사 흐름 — V3가 권위

권위:
- `civics_reference/CIVIC_TREE_HISTORICAL_V3.md`
- `civics_reference/civic_tree_historical_v3.csv`
- `civics_reference/validate_civic_tree_historical_v3.py`

구형:
- CIVIC_TREE_LOCKED_V1: Civ VI 연결 보존형
- Historical V2: 1차 역사보정
- **Historical V3: 현재 기준**

## QA

- 72 nodes
- root = Code of Laws 하나
- 72/72 reachable
- missing refs 0
- cycle 0
- backward-era edges 0
- max direct social prerequisites 2

## 중요한 수정 철학

사회제도 선행조건은:
- 사회
- 제도
- 문화
- 사상
의 인과만 담당한다.

과학기술이 필요한 부분을 억지 사회제도로 연결하지 않는다.

예:
- Reformed Church -> Sovereignty 제거
- Exploration -> Scientific Revolution 제거
- Mass Media -> Capitalism 제거
- Ideology -> Professional Sports 제거
- Scorched Earth -> Mobilization 제거
- Ideology -> Nuclear Program 제거
- Professional Sports -> Social Media 제거

## 중요 흐름 예

### Early Medieval / High Medieval

Civil Service -> Written Culture  
Written Culture + Drama and Poetry -> Court Culture  
Theology + Written Culture -> Scholasticism  
Medieval Faires + Written Culture -> Guilds

### Renaissance

Scholasticism + Court Culture -> Humanism  
Court Culture -> Diplomatic Service  
Humanism + Guilds -> Patronage  
Humanism -> Print Culture

### Exploration

Naval Tradition + Medieval Faires -> Exploration  
Theology + Print Culture -> Reformed Church  
Print Culture -> Scientific Revolution  
Diplomatic Service + Humanism -> Sovereignty  
Exploration + Sovereignty -> Mercantilism  
Mercantilism -> Colonialism

### Enlightenment

Scientific Revolution + Sovereignty -> The Enlightenment  
Patronage -> Opera and Ballet  
Scientific Revolution + Exploration -> Natural History  
Print Culture + The Enlightenment -> Public Sphere  
Public Sphere + Sovereignty -> Constitutionalism

### Industrial

Mercantilism -> Capitalism  
Civil Service + Sovereignty -> Civil Engineering  
Sovereignty + Public Sphere -> Nationalism  
Opera and Ballet + The Enlightenment -> Romanticism  
Civil Engineering + Capitalism -> Urbanization  
Natural History + Romanticism -> Conservation  
Public Sphere + Urbanization -> Mass Media  
Capitalism + Urbanization -> Labor Movement

### Modern

Nationalism + Urbanization -> Mobilization  
Nationalism + Mass Media -> Ideology  
Constitutionalism -> Suffrage  
Ideology -> Totalitarianism  
Ideology + Labor Movement -> Class Struggle  
Games and Recreation + Urbanization -> Professional Sports

### Atomic / Information

Mobilization -> Nuclear Program  
Ideology + Nuclear Program -> Cold War  
Cold War -> Rapid Deployment  
Cold War -> Space Race  
Conservation + Mass Media -> Environmentalism

Capitalism + Mass Media -> Globalization  
Mass Media + Public Sphere -> Social Media

중요:
Globalization에서 Cold War hard prerequisite를 제거했다.
이유는 Cold War가 Nuclear Program을 통해 Nuclear Fission을 상속하여 세계화까지 핵분열을 강제하는 문제가 발생했기 때문.

---

# 10. 과학기술 — 109개 V2 확정

권위:
- `tech_reference/TECHNOLOGY_ROSTER_TREE_LOCKED_V2.md`
- `tech_reference/technology_roster_locked_v2.csv`
- `tech_reference/technology_tree_historical_v2.csv`
- `tech_reference/validate_technology_tree_historical_v2.py`

103-node V1은 superseded.

## 소스 우선순위

1. Civilization VI Gathering Storm
2. Civilization V Brave New World
3. Pouakai Civilization V Enlightenment Era
4. game-source merge가 명백한 역사 공백을 만들 때만 최소 historical addition

사회제도와 중복되는 Civ V 기술은 science tree에서 제외.

예:
- Theology
- Civil Service
- Mass Media
- Globalization
- Humanism
- Sovereignty
- Natural History
- Romanticism

## Total

**109 technologies**

## Era counts

- Ancient: 14
- Classical: 10
- Late Antiquity: 5
- Early Medieval: 5
- High Medieval: 6
- Renaissance: 5
- Exploration: 8
- Enlightenment: 6
- Industrial: 16
- Modern: 12
- Atomic: 5
- Information: 9
- Future: 8

## Historical additions 6

- Papermaking
- Horse Collar
- Alchemy
- Block Printing
- Algebra
- Astrolabe

## Historical moves

- Stirrups -> Late Antiquity
- Gunpowder -> Early Medieval
- Metallurgy -> Renaissance

## 중요 기술 흐름

Writing + Agriculture -> Papermaking  
Papermaking + Writing -> Block Printing  
Block Printing + Machinery -> Printing

Bronze Working + Astrology -> Alchemy  
Alchemy + Military Engineering -> Gunpowder  
Metal Casting + Alchemy -> Metallurgy  
Alchemy + Scientific Theory -> Chemistry

Mathematics + Writing -> Algebra  
Writing + Algebra -> Education  
Algebra + Engineering -> Physics

Celestial Navigation + Optics -> Astrolabe  
Astrolabe + Optics -> Astronomy

Animal Husbandry + Wheel -> Horse Collar  
Horseback Riding + Iron Working -> Stirrups

Manufacturing + Scientific Theory -> Steam Power  
Steam Power + Manufacturing -> Industrialization  
Replaceable Parts + Industrialization -> Mass Production

Electricity + Printing -> Telegraph  
Electricity + Radio -> Electronics  
Electronics + Mathematics -> Computers  
Electronics + Computers -> Telecommunications

Atomic Theory + Chemistry -> Nuclear Fission  
Rocketry + Electronics -> Satellites  
Computers + Electronics -> Robotics  
Nuclear Fission + Particle Physics -> Nuclear Fusion

## QA

- 109 nodes
- roots: Agriculture, Pottery, Animal Husbandry, Mining, Sailing, Archery
- 109/109 reachable
- missing prerequisites 0
- cycles 0
- backward-era edges 0
- max direct prerequisites 2

---

# 11. 중요 미해결 기술 예외 — Photography / Cinematography

위대한 감독 시스템을 채택한 뒤 다음 파일에서 문제를 명시했다.

`city_system/CIV5_STYLE_CITY_AND_GREAT_DIRECTOR_BASELINE_V1.md`

MoreTech 계열 참고에서는 Great Director / Film을 Cinematography에서 연다.

현재 109-tech V2에는:
- Photography 없음
- Cinematography 없음

따라서 둘 중 하나를 선택해야 한다.

A. 109-tech lock을 절대 유지
- 기존 기술에 Great Director/Film unlock을 매핑

B. 실제 구현 gap을 인정
- Photography
- Cinematography
를 추가하여 111-tech로 확장

현재는 **추가하지 않은 상태**다.

다음 채팅에서 임의로 추가하지 말고 먼저 결정해야 한다.

---

# 12. 사회제도-과학기술 병렬 시스템

권위:
- `civics_reference/civic_tech_crosslinks_v1.csv`
- `civics_reference/CIVIC_TECH_CROSSLINK_RECONCILIATION_V3.md`

두 트리는 병렬이지만 상호 연결한다.

## Direct relation 3종

### HARD

그 기술이 없으면 해당 사회제도 자체가 물질적으로 성립 불가능.

### BOOST

기술이 없어도 사회제도 연구 가능하지만 큰 가속/영감.

### NONE

별도 기술 조건 없음.

## 현재 분류

- HARD: 11
- BOOST: 31
- NONE: 30

## HARD 11

- Recorded History <- Writing
- Naval Tradition <- Sailing
- Print Culture <- Printing
- Exploration <- Cartography
- Civil Engineering <- Engineering
- Nuclear Program <- Nuclear Fission
- Rapid Deployment <- Flight
- Space Race <- Rocketry
- Social Media <- Telecommunications
- Optimization Imperative <- Robotics
- Exodus Imperative <- Satellites

## 대표 BOOST

- Scientific Revolution <- Astronomy
- Mass Media <- Telegraph
- Environmentalism <- Ecology

## 검증

109-tech V2 기준:
- civic crosslink 72 rows 검증
- missing technology refs 0
- later-era HARD/BOOST 0
- combined cycle 0

현재 technology tree에는 civic prerequisite가 없으므로 cross-tree cycle 없음.

---

# 13. 도시 운영 — Civilization V식으로 확정

권위:
`city_system/CIV5_STYLE_CITY_AND_GREAT_DIRECTOR_BASELINE_V1.md`

## 핵심

**Civilization VI식 district city puzzle은 사용하지 않는다.**

즉:
- Campus map district 없음
- Commercial Hub map district 없음
- Industrial Zone map district 없음
- Theater Square map district 없음
- Encampment map district 없음

건물은 Civ V처럼 도시 내부에 직접 건설.

시민:
- 주변 타일 작업
- specialist slot 작업

Tile improvement는 지도에 존재.

## Civ VI 콘텐츠 변환

Campus 제거:
- Library -> University -> Research Lab은 city building으로 유지

Commercial Hub 제거:
- Market -> Bank -> Stock Exchange

Industrial Zone 제거:
- Workshop -> Factory -> Power Plant

Theater Square 제거:
- Amphitheater -> Museum -> Broadcast 계열

Encampment 제거:
- Barracks -> Armory -> Military Academy

Aqueduct / Dam / Canal / Neighborhood 같은 Civ VI district/infrastructure는 그대로 복사하지 않고:
- city infrastructure
- tile improvement
- special project
등으로 재해석해야 한다.

---

# 14. 위대한 감독 / 영화 명작

위대한 감독 시스템 포함 확정.

기준:
JFD Great Works of Film + MoreTech 참고.

## 구성

- Great Director
- Director specialist
- Director's Guild / Film School / Studio 계열
- Cinema
- Great Works of Film
- Film slot

## 방향

Great Director:
- 주 행동: Great Work of Film 생성
- 2차 능력은 미확정

Director specialist:
- Culture/Tourism
- Great Director points

Film:
- Music과 별개 Great Work category
- 전용 slot
- Culture/Tourism
- 테마 보너스는 추후

## World Wonder

Hollywood를 자동 채택하지 않는다.

**모든 불가사의는 별도 엄격 심사.**

평가기준:
- 세계사적 위상
- 독창성
- 건축/문화적 식별성
- 실제로 World Wonder급인지
- 게임플레이 독자성

현재 기술/건물 해금 작업에서도 불가사의는 제외한다.

---

# 15. 기업 시스템 — 현재 가장 중요한 다음 작업

권위:
`corporations/CORPORATION_FOUNDING_AND_OUTPUT_SYSTEM_V1.md`

## 핵심 철학

기업은 World Wonder가 아니다.

- 업종은 비독점
- 어느 문명이든 조건 충족 시 같은 업종 기업 설립 가능
- 역사적 named firm은 unique 가능
- unique firm이 있어도 sector는 막히지 않음

예:
Ford, Toyota, Honda, Hyundai가 모두 자동차 sector에서 공존 가능.

## 기업 설립 위인

### Great Merchant

주력:
- finance
- trade
- retail
- food
- clothing/fashion
- cosmetics
- hospitality
- commercial services

### Great Engineer

주력:
- automotive
- machinery
- electrical
- chemicals
- electronics
- telecommunications
- precision engineering
- industrial energy
- advanced manufacturing

## Signature Founder

특정 위인은 고유 기업을 설립 가능.

예:
- Thomas Edison -> Edison/GE lineage
- Carl Benz -> Benz & Cie.
- Henry Ford -> Ford
- Robert Bosch -> Bosch
- Levi Strauss -> Levi Strauss & Co.
- Estée Lauder -> Estée Lauder
- Milton Hershey -> Hershey
- Fritz Hoffmann-La Roche -> Roche

위인을 기업 설립에 쓰지 않고 일반 Great Person 능력으로 쓰는 선택도 가능하게 할 방향.

---

# 16. 기업 산출물 3종

## A. Manufactured Luxury

소비재/브랜드 상품.

예:
- Jeans
- Cosmetics
- Chocolate
- Furniture
- Automobiles
- Consumer Electronics
- Watches
- Fashion Goods
- Soft Drinks

효과:
- Amenities/Happiness
- Gold
- export demand
- 일부 iconic product는 Culture/Tourism

중요:
같은 product category 여러 brand가 Amenities를 무한 중첩하지 않는다.

예:
Ford + Toyota + Honda + Hyundai 모두 Automobile 생산 가능.

하지만:
- 첫 Automobile category가 주 Amenity 제공
- 추가 brand는 Gold, Tourism, demand, market share, 기업 경쟁에 기여

## B. Functional Corporate Good

실제 공급량을 가진 기능성 상품.

예:

| Product | Main effect |
|---|---|
| Refined Petroleum Products | Production + logistics |
| Steel Products | Production + construction |
| Machine Tools | Production + factory efficiency |
| Fertilizer | Food + farm productivity |
| Pharmaceuticals | Growth/Health + healing |
| Electrical Equipment | Production + Science |
| Precision Components | Production + advanced units |
| Semiconductors | Science + Production |
| Construction Materials | infrastructure Production |
| Processed Food | Food + Growth |
| Industrial Chemicals | Production + advanced industry |
| Paper Products | Culture/education/admin |

### 정유 예

Oil
-> refinery corporation
-> Refined Petroleum Products
-> supplied city

효과:
- Production
- transport/logistics
- industrial infrastructure
- civilian fuel burden 감소 등

Raw Oil은 strategic resource 그대로.
Refined Petroleum Products가 value-added corporate output.

## C. Service

물리 resource stock이 아니라:
- branch
- network
- trade connection
- service coverage
로 제공.

예:

| Service | Main effect |
|---|---|
| Finance | Gold + investment |
| Retail | Gold + product distribution |
| Hospitality | Tourism + Culture + Gold |
| Film/Entertainment | Culture + Tourism + Great Director |
| Media | Culture + Tourism + civic spread |
| Telecommunications | Science + network/trade |
| Logistics | trade route + movement + Gold |
| Insurance | risk/loss reduction |
| Advertising | demand + Gold + Tourism |
| Software | Science + Production + Gold |
| Airlines/Travel | Tourism + connectivity |

**서비스를 전부 Culture/Tourism으로 만들지 않는다.**

---

# 17. 기업 공급과 지점

기능성 상품:
- 본사/공장이 quantity 생산
- 도시가 실제 공급을 받아야 bonus
- 국내/해외 수출 가능
- 공급 안 된 도시는 bonus 없음

서비스:
- branch/network coverage로 적용

기업 상태에 들어갈 것:
- founder
- HQ city
- sector
- required civic
- required technology
- inputs
- output class
- product/service
- branches
- production capacity
- domestic demand
- foreign demand
- profit
- branding
- foreign market presence

Foreign branch:
- trade access/open borders/경제 허가
- network/trade route
- demand
등을 고려

## 일반 unlock 방향

기업 시스템 일반 기반:
- civic: Capitalism
- + sector technology

예:
- apparel: Capitalism + Mass Production
- petroleum: Capitalism + Refining
- automotive: Capitalism + Combustion / Mass Production
- electrical: Capitalism + Electricity
- pharmaceuticals: Capitalism + Chemistry/Biology
- electronics: Capitalism + Electronics
- telecom: Capitalism + Telecommunications
- software: Capitalism + Computers

Corporations라는 별도 civic은 현재 추가하지 않는다.

---

# 18. 기업 창업가 조사 — 실제 진행됨

권위:
`corporations/CORPORATE_FOUNDER_POOL_RESEARCH_V1.md`

Status:
**RESEARCH POOL**
모든 후보가 final lock은 아니다.

## 현재 이미 수집된 주요 후보

### Europe / North America

- Levi Strauss
- Estée Lauder
- Milton Hershey
- Henri Nestlé
- Henry J. Heinz
- Gabrielle Chanel
- Ingvar Kamprad
- Conrad Hilton
- J. Willard Marriott
- Marcus Goldman
- J. Pierpont Morgan
- John D. Rockefeller
- Carl Benz
- Henry Ford
- Robert Bosch
- Werner von Siemens
- Gerard Philips
- Lars Magnus Ericsson
- John Deere
- Herbert H. Dow
- Johann Friedrich Weskott
- Friedrich Bayer
- Fritz Hoffmann-La Roche
- Charles Pfizer
- Adi Dassler
- Robert Noyce
- Gordon Moore
- Jensen Huang
- Larry Ellison

### East Asia

- Yataro Iwasaki
- Kiichiro Toyoda
- Soichiro Honda
- Namihei Odaira
- Konosuke Matsushita
- Masaru Ibuka
- Shojiro Ishibashi
- Torakusu Yamaha
- Koo In-hwoi
- Lee Byung-chul
- Pony Ma
- Jack Ma
- Liu Chuanzhi
- Terry Gou
- Stan Shih

### South Asia

- Jamsetji Tata
- J. C. Mahindra
- K. C. Mahindra
- Sunil Bharti Mittal
- Dilip Shanghvi

### Southeast Asia / Middle East

- Chia Ek Chor
- Chia Seow Hui
- Anthony Tan
- Tan Hooi Ling
- Mudassir Sheikha
- Magnus Olsson
- Fadi Ghandour

### Africa

- Aliko Dangote
- Strive Masiyiwa
- Mo Ibrahim

### Latin America

- Ozires Silva
- Lorenzo Servitje

## 재검증 필요 후보

다음은 유력하지만 founder/co-founder role을 더 확인해야 함.

- Apple: Steve Jobs / Steve Wozniak / Ronald Wayne
- Disney: Walt / Roy Disney
- Coca-Cola
- Microsoft: Bill Gates / Paul Allen
- TSMC: Morris Chang
- BYD: Wang Chuanfu
- Reliance: Dhirubhai Ambani
- Godrej
- Walmart: Sam Walton
- Nike
- FedEx
- Maersk
- Mercado Libre
- Nubank
- Gojek
- Jollibee
- Amorepacific
- Lotte
- Naver
- Kakao

## 다음 founder target

80-100 audited candidates까지 확대.

특히 부족한 영역:
- Latin America
- Africa
- Middle East
- Southeast Asia
- women founders
- shipping/logistics
- mining/materials
- insurance
- aviation
- pharmaceuticals
- software/digital

각 후보에 붙여야 할 것:
- project era
- Great Merchant / Great Engineer
- exact firm
- founder/co-founder wording
- sector
- input
- output class
- product/service
- civic gate
- technology gate
- signature ability
- HQ effect
- branch effect
- supply quantity rules

---

# 19. 왜 지금 기술별 건물/유닛 해금 작업을 멈췄는가

원래 다음 단계는 109개 기술 각각에:

- Unit
- City Building
- Tile Improvement
- Resource reveal/use
- System unlock

을 붙이는 것이었다.

그리고 불가사의는 별도 심사 때문에 제외하기로 했다.

하지만 도시 시스템을 Civ V식으로 확정했고 기업 시스템이 추가되면서 다음 문제가 생겼다.

## 기업이 기술 해금에 직접 영향을 줌

예:
- Refining -> refinery-related corporate production
- Mass Production -> apparel/automobile corporation
- Electricity -> electrical corporation
- Electronics -> electronics firms
- Telecommunications -> telecom corporation/network
- Computers -> software/digital services
- Film technology -> cinema/director/film corporation

기업을 먼저 정의하지 않고 기술 unlock table을 만들면:
- 기업 building
- branch
- factory
- service network
- functional product
를 나중에 전부 다시 뜯어고쳐야 한다.

따라서 현재 작업 순서는 의도적으로:

**기술 확정 -> 기업 시스템 확정 -> 기술별 실제 unlock 배치**

로 바뀌었다.

---

# 20. 기술별 해금 작업의 규칙

기업이 어느 정도 확정된 뒤 시작.

각 기술에 대해 다음만 우선 정리:

1. Units
2. City Buildings
3. Tile Improvements
4. Resource reveal / resource exploitation
5. Corporate sector/product unlock
6. Infrastructure/system unlock

World Wonders는 제외.

## 소스 우선

- Civ VI content를 쓸 때 district 자체는 제거
- 건물/유닛/시설/효과만 Civ V-style city system으로 변환
- Civ V BNW와 Enlightenment Era는 gap fill
- 중복이면 Civ VI 우선
- 실제 역사 흐름에 맞지 않으면 시대/선행관계를 이미 만든 V2 technology tree에 맞춤

---

# 21. 불가사의 정책

현재 **불가사의 목록은 확정하지 않는다.**

기업, 기술, 건물에 source game Wonder가 있다고 자동 추가하지 않는다.

별도 Wonder audit 예정.

평가:
- 세계사적 가치
- 실제 건축/문화적 독창성
- 특정 국가의 유명 랜드마크일 뿐인지
- World Wonder급인지
- 게임에서 고유 효과가 필요한지

Hollywood 같은 항목도 자동 채택 금지.

---

# 22. 현재 권위 파일 목록

## Map / resources

- `CIV_GAME_MAP_STAGE10_CURRENT_HANDOFF_2026-09-20.md`
- `civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`
- `civ_map_stage10_resources/icons_v4/`

## Dynamic resource discovery

- `civ_map_stage10_resources/contact_dynamic_resource_system_v2.md`
- `civ_map_stage10_resources/resource_transfer_classes_v2.csv`

## 4000 BCE history

- `civ_map_stage10_resources/history_4000bce_v3/README.md`
- `civ_map_stage10_resources/history_4000bce_v3/resource_start_visible_4000bce_mask_regions_v3.csv`
- `civ_map_stage10_resources/history_4000bce_v3/apply_resource_history_4000bce_v3.py`
- `civ_map_stage10_resources/history_4000bce_v3/resource_history_4000bce_exact_summary_v3.csv`
- `civ_map_stage10_resources/history_4000bce_v3/resource_history_4000bce_critical_checks_v3.csv`

## Civics

- `civics_reference/CIVIC_ROSTER_LOCKED_V1.md`
- `civics_reference/civic_roster_locked_v1.csv`
- `civics_reference/CIVIC_TREE_HISTORICAL_V3.md`
- `civics_reference/civic_tree_historical_v3.csv`
- `civics_reference/validate_civic_tree_historical_v3.py`

## Civic-tech

- `civics_reference/civic_tech_crosslinks_v1.csv`
- `civics_reference/CIVIC_TECH_CROSSLINK_RECONCILIATION_V3.md`

## Technologies

- `tech_reference/TECHNOLOGY_ROSTER_TREE_LOCKED_V2.md`
- `tech_reference/technology_roster_locked_v2.csv`
- `tech_reference/technology_tree_historical_v2.csv`
- `tech_reference/validate_technology_tree_historical_v2.py`

## City / Great Director

- `city_system/CIV5_STYLE_CITY_AND_GREAT_DIRECTOR_BASELINE_V1.md`

## Corporations

- `corporations/CORPORATION_FOUNDING_AND_OUTPUT_SYSTEM_V1.md`
- `corporations/CORPORATE_FOUNDER_POOL_RESEARCH_V1.md`

Superseded/reference only:
- `corporations/SIGNATURE_GREAT_MERCHANT_FOUNDERS_REVIEW_V1.md` — merchant-only framework superseded
- 103-tech V1 docs — superseded
- civic historical V2 — superseded by V3
- dynamic resource V1 — DO NOT IMPLEMENT
- history_4000bce_v1 — superseded

---

# 23. 다음 채팅에서 절대 잊으면 안 되는 결정

1. **자원 배치와 자원 발견은 별개다.**
   - Stage10 현대 잠재분포
   - 4000 BCE START_VISIBLE/LATENT
   - contact-based acquisition
   를 구분한다.

2. 자원 발견은 fixed-year unlock이 아니다.
   - alternate history 접촉과 교역이 전파 시기를 바꿀 수 있다.

3. dynamic resources는 현재 18개만.
   - geological/mineral은 fixed.

4. 사회제도는 72개.
   - historical V3가 선행관계 권위.

5. 과학기술은 109개 V2.
   - 103 V1 사용 금지.

6. 사회제도와 기술은 병렬.
   - HARD / BOOST crosslinks 사용.

7. 도시는 Civ V식.
   - Civ VI district 심시티 사용 안 함.

8. Great Director / Film 포함.
   - Photography/Cinematography 문제는 아직 별도 결정 필요.

9. 기업은 Wonder가 아니다.
   - sector 비독점
   - named firm만 unique 가능.

10. Great Merchant와 Great Engineer 모두 기업 설립 가능.

11. 기업 산출물은:
   - Manufactured Luxury
   - Functional Good
   - Service
   로 나눔.

12. 기능성 상품은 실제 공급량을 갖는 방향.
   - 정유제품은 Production/logistics 등

13. 서비스는 sector별 효과.
   - 호텔/영화는 Culture/Tourism
   - 금융은 Gold/investment
   - telecom은 Science/network
   - logistics는 trade/movement

14. 기업 창업가 조사는 이미 일부 진행됨.
   - V1 pool 존재
   - 다음 목표 80-100 candidates

15. **현재 즉시 다음 작업은 기업 시스템 확정이다.**
   - 기업이 확정되기 전에 109개 기술에 건물/유닛 unlock을 붙이지 않는다.

16. World Wonders는 지금 다루지 않는다.
   - 나중에 별도 엄격 심사.

---

# 24. 다음 작업 순서 — 권장

## Step A. 기업 founder pool 확대 및 확정

목표:
80-100명 수준의 Great Merchant / Great Engineer 후보.

각 founder:
- historical verification
- founder/co-founder
- region
- era
- GP class
- firm
- sector
- output
- technology gate
- civic gate
- HQ effect
- branch effect

## Step B. 기업 업종과 산출물 catalogue 확정

예:
- Petroleum
- Steel
- Chemicals
- Pharmaceuticals
- Automotive
- Electronics
- Telecom
- Apparel
- Cosmetics
- Food
- Furniture
- Finance
- Retail
- Hospitality
- Logistics
- Film/Media
- Software

각 sector에:
- inputs
- output class
- product/service
- supply model
- yield effects
- trade behavior

## Step C. 기업 unlock 조건을 109-tech + 72-civic tree에 연결

General:
Capitalism + sector technology

단, sector별 예외 검토.

## Step D. 기술별 실제 unlock table 작성

109 technologies x:
- units
- buildings
- improvements
- resource reveal/exploitation
- corporation unlock
- systems

Civ V city model 사용.

## Step E. 사회제도 unlock content

72 civics x:
- governments
- policy cards
- buildings/system unlocks
- specialists
- Inspirations

## Step F. resource runtime implementation

V2 dynamic resource state 실제 게임 레이어 구현.

## Step G. Stage10 placement finalization

- resource_fix_v1 + V3 history layer visual QA
- direct GPKG map
- alternate history runtime test
- 이후 canonical final promotion 여부 결정

## Step H. World Wonder audit

가장 마지막 별도 작업.

---

# 25. 다음 채팅 시작 문구 권장

다음 ChatGPT에게는 이 문서를 먼저 읽힌 뒤 다음처럼 지시:

> `CIV_GAME_PROJECT_MASTER_HANDOFF_2026-09-20.md`를 기준으로 이어가라. 현재 immediate task는 corporation founder pool을 80-100명 수준으로 확대하고, Great Merchant / Great Engineer, firm, sector, output class, product/service, technology gate, civic gate를 검증하는 것이다. 기업을 확정하기 전에는 technology unlock building table로 넘어가지 마라. 자원 발견 시스템 V2와 4000 BCE V3, 72 civic historical V3, 109-tech V2는 유지하라.



---

# 26. 기업 창업가 / 업종 V2 완료 상태 — 2026-09-20 추가

기존 immediate task였던 **80-100명 founder pool 확대**는 V2에서 완료했다.

## 새 권위 파일

- `corporations/CORPORATE_FOUNDER_POOL_AUDITED_V2.csv`
- `corporations/CORPORATE_FOUNDER_POOL_AUDITED_V2.md`
- `corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.csv`
- `corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.md`

기존:
- `corporations/CORPORATE_FOUNDER_POOL_RESEARCH_V1.md`

은 1차 출처감사 archive/reference로 유지한다.

## Founder V2 exact state

- 총 후보: **99**
- Great Merchant: **53**
- Great Engineer: **46**
- LOCK_CANDIDATE: **98**
- Liu Chuanzhi: `LOCK_CANDIDATE` — founding-team leader / co-founder
- Ozires Silva: `REFERENCE_ONLY_INSTITUTIONAL_CREATOR` — ordinary signature-founder roster에서 제외

지역:
- Europe/North America 44
- East Asia 23
- Southeast Asia 9
- South Asia 7
- Latin America 6
- Middle East 5
- Africa 4
- Oceania 1

## Canonical sector V2

- 총 sector: **32**
- 현재 founder가 있는 sector: **30**
- founder를 아직 잠그지 않은 future sector:
  - `MEDIA_FILM_ENTERTAINMENT`
  - `AIRLINES_TRAVEL`

모든 founder row는 `CANONICAL_SECTOR_ID`로 sector catalogue에 연결돼 있다.

## Gate QA

99 founder rows 전체에 대해:

- missing technology ref: **0**
- missing civic ref: **0**
- founder 시대보다 뒤의 technology gate: **0**
- missing sector ref: **0**
- sector/gate mismatch: **0**
- non-hybrid output-class mismatch: **0**
- duplicate founder: **0**
- missing source: **0**

일반 gate 원칙은 계속:

**Capitalism + sector technology**

이다.

역사적 단계가 긴 sector는 같은 sector 내에서 base -> mature technology progression을 허용한다.

예:
- Telecommunications: `Telegraph -> Telecommunications`
- Automotive: `Mass Production -> Combustion`
- Shipping/Logistics: `Steam Power -> Railroad -> Advanced Flight`
- Machinery/Components: `Replaceable Parts -> Combustion / Electronics`

## 중요 역사보정

- Carl Benz는 1880년대 창업을 Modern의 Combustion에 억지로 늦추지 않고 Industrial의 `Mass Production`을 초기 automotive gate로 사용.
- Robert Bosch는 1886년 창업에 맞춰 `Replaceable Parts`.
- Mahindra 형제는 창업 당시 steel-trading 성격을 반영해 `STEEL_HEAVY_MATERIALS`.
- Lee Byung-chul은 Samsung Electronics의 창업자로 소급하지 않고 founder-era `TRADING_HOUSES`.
- Jamsetji Tata도 후대 Tata Steel을 직접 창업한 것으로 소급하지 않고 founder-era `TRADING_HOUSES`.
- Thomas Edison은 modern GE의 단독 창업자가 아니라 Edison electric-company / GE lineage로 한정.
- Ozires Silva는 state-created Embraer의 key creator / first managing director로 별도 표시.

## Film sector 예외

`MEDIA_FILM_ENTERTAINMENT`의 기술 gate는 아직:

`PENDING_FILM_TECH_DECISION`

이다.

Photography / Cinematography를 109-tech에 추가할지 여부를 아직 결정하지 않았으므로 Radio 등에 임의로 덮어씌우지 않는다.

## 이제 immediate task

Founder 숫자를 더 무작정 늘리는 것이 우선이 아니다.

다음은 기업 시스템을 실제 플레이 가능한 수준으로 확정하는 작업이다:

1. 32 sector의 **정량적 생산량 / 소비량 / branch coverage / yield 효과** 확정
2. 기업 diversification 규칙 확정
3. Liu Chuanzhi / Ozires Silva 두 edge case 최종 wording 결정
4. signature founder 실제 게임 투입 subset 확정
5. Film/Cinematography 기술 결정
6. 그 뒤에만 109-tech의 unit/building/improvement/corporation unlock table로 이동

**기업의 정량적 supply/branch mechanics가 확정되기 전에는 기술별 건물/유닛 unlock table로 넘어가지 않는다.**


---

# 27. 기업 정량 supply / branch 모델 V1 — 2026-09-20 추가

권위 파일:
- `corporations/CORPORATION_QUANTITATIVE_SUPPLY_BRANCH_MODEL_V1.md`
- `corporations/corporation_sector_effects_v1.csv`

## 핵심

실물 기업상품은 empire-wide permanent modifier가 아니라 **Supply Unit (SU)**로 공급한다.

기본 도시 수요:
- Functional Good: `ceil(population / 5)` SU/turn
- Manufactured Luxury: `ceil(population / 8)` SU/turn
- Hybrid physical product: `ceil(population / 6)` SU/turn

기본 plant 생산:
- 일반: 4 SU/turn
- 대량 소비재/식품: 약 5 SU/turn
- 중공업/항공/석유 등: 약 3 SU/turn

공급률:
`coverage = min(1, allocated_SU / demand_SU)`

percentage bonus는 coverage에 비례한다.

Manufactured Luxury Amenity 기본:
- coverage < 0.75: Amenity 없음
- coverage >= 0.75: 해당 product category에서 +1 Amenity

동일 category의 여러 brand는 Amenity를 중복하지 않는다.
추가 brand는 Gold, market share, Tourism, export demand 등으로 경쟁한다.

## Service

Finance, Hospitality, Insurance, Software, Digital Platform 등은 stock resource를 만들지 않는다.

기본 service coverage:
- 없음: 0
- national network만 연결: 0.5
- local branch/network node: 1.0
- foreign city에서 명시적 branch/network access: 1.0

## Foreign trade

실물 corporate good의 foreign allocation 기본 throughput:
- active trade connection당 4 SU/turn
- Shipping/Logistics full service가 있으면 5 SU/turn

## Diversification

기업은 founder-era primary sector를 유지한다.

다른 sector 진입은 Diversification Project:
1. target sector tech 필요
2. HQ 외 branch/plant 3개 이상
3. target input/network 확보
4. HQ project 완료

기본 secondary sector 한도:
- 최대 2개

Samsung, Tata, Reliance 같은 conglomerate를 founder 시대에 후대 업종으로 소급하지 않고 게임 안에서 diversification으로 재현한다.

## QA

- canonical sector catalogue: 32
- quantitative sector effect rows: 32
- missing effect rows: 0
- orphan effect rows: 0
- duplicate effect rows: 0


## Founder edge-case finalization

- **Liu Chuanzhi**: `LOCK_CANDIDATE`. 게임 표기는 **Founding-team leader / co-founder**.
- **Ozires Silva**: `REFERENCE_ONLY_INSTITUTIONAL_CREATOR`. 99명 research pool에는 남지만 일반 signature-founder roster에서는 제외.
- 따라서 일반 signature-founder eligible pool은 **98명**이다.


---

# 28. Signature corporate founder roster V1 — 2026-09-20 추가

권위 파일:
- `corporations/signature_corporate_founder_roster_v1.csv`
- `corporations/SIGNATURE_CORPORATE_FOUNDER_ROSTER_V1.md`

## Exact state

연구 DB:
- `CORPORATE_FOUNDER_POOL_AUDITED_V2.csv`
- 총 99명

실제 게임 signature-founder roster:
- 총 **98명**
- Great Merchant **53**
- Great Engineer **45**

시대:
- Industrial 23
- Modern 20
- Atomic 42
- Information 13

Ozires Silva:
- 연구 DB에는 유지
- `REFERENCE_ONLY_INSTITUTIONAL_CREATOR`
- 일반 signature-founder roster에서는 제외

Liu Chuanzhi:
- 실제 roster 포함
- 표기: `Founding-team leader / co-founder`
- sole founder로 표기하지 않음

## Gameplay rule

Signature Great Person을 영입했다고 회사가 자동 설립되지는 않는다.

플레이어는:
- 일반 Great Person 능력을 사용하거나
- 해당 기업의 gate가 충족되었을 때 Great Person을 소비해 named firm을 설립

할 수 있다.

named historical firm:
- 세계적으로 unique

canonical sector:
- non-exclusive

generic corporation:
- 같은 sector에서 계속 설립 가능

기업의 founder-era primary sector는 고정하며,
후대의 업종 확장은 Diversification Project로 처리한다.

## 현재 기업 작업 완료 상태

완료:
1. founder research pool 확대: 99명
2. signature gameplay roster: 98명
3. canonical sector catalogue: 32
4. founder-sector 연결: 완료
5. technology/civic gate QA: 완료
6. quantitative SU / branch model: 완료
7. diversification baseline: 완료
8. Liu Chuanzhi / Ozires Silva edge case: 완료

남은 핵심 blocking item:
- **Film / Great Director 기술 gate 결정**

Photography / Cinematography를 추가하여 111-tech로 갈지,
109-tech를 유지하고 기존 기술에 매핑할지 결정한 뒤
109-tech unit/building/improvement/corporation unlock table로 넘어간다.


## Former Great Person tile improvements — 2026-09-21 update

Supersedes the previous blanket removal rule.

Five former Civ V Great Person improvements return as **nerfed Worker-buildable tile improvements** with no Great Person consumption:

- Academy -> Education
- Manufactory -> Manufacturing
- Customs House -> Economics + Mercantilism
- Holy Site -> Theology
- Landmark -> Humanism

The Great General Citadel remains excluded.

The city institution previously called Customs House is renamed **Customs Office** so that Customs House remains the tile-improvement name.

Natural History archaeology retains a separate archaeological Historic Landmark pathway.

Authority:
`tile_system/FORMER_GREAT_PERSON_TILE_IMPROVEMENTS_V1.md`


## Civic policy finalization — 2026-09-21

Qualitative policy ownership is complete.

Current authorities:
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V2.csv`
- `civics_reference/FINAL_POLICY_CARD_ROSTER_V1.csv`
- `civics_reference/FINAL_POLICY_CARD_ROSTER_V1.md`

Results:
- 72/72 civics present
- 127 final policy cards
- duplicate policy ownership 0
- Civ VI direct policy content is the main fallback source when Civ V/project content is sparse
- Governor-dependent policy content is removed/adapted because baseline Governors are not adopted
- district conditions are translated to Civ V-style city buildings/infrastructure
- exact percentages/yields/caps remain for numerical balance


## Unlock deferred queue closed — 2026-09-21

All tracked generic technology/civic unlock deferrals are resolved.

Current baseline:
- 109 technology master complete
- 72 civic master V2 complete
- 127 policy-card ownership entries, duplicate 0
- former Great Person improvements restored as nerfed Worker-built tiles except Citadel
- Governor system not adopted
- GDR restored to the baseline by the later Gathering Storm Future Era realignment
- tracked numeric/system deferrals resolved
- deferred generic queue remaining: 0

Authorities:
- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv`
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V2.csv`
- `civics_reference/FINAL_POLICY_CARD_ROSTER_V1.csv`
- `tech_reference/NUMERIC_BALANCE_DECISIONS_V1.csv`
- `tech_reference/DEFERRED_GENERIC_UNLOCK_QUEUE_V1.md`


## Policy effects fully locked — 2026-09-21

The civic-policy pass is complete.

- 72/72 civics present
- 127 final policy cards
- 127/127 have a locked policy slot
- 127/127 have a locked final effect
- 127/127 are `NUMERIC_STATUS=LOCKED_V1`
- duplicate policy names: 0

Slot distribution:
- Military: 35
- Economic: 46
- Wildcard: 26
- Diplomatic: 20

Current authorities:
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V2.csv`
- `civics_reference/FINAL_POLICY_CARD_ROSTER_V1.csv`
- `civics_reference/FINAL_POLICY_CARD_ROSTER_V1_QA.md`
- `civics_reference/policy_balance/*_POLICY_EFFECTS_V1.csv`

Civ VI is the main fallback source for policy content when Civ V/project content is sparse. District/Builder/Governor-dependent effects are translated to the project's Civ V-style structure; Gathering Storm GDR effects are retained where the baseline GDR now exists.


## Generic building roster locked — 2026-09-21

The generic/national building roster is now consolidated and QA-passed.

- final buildings: 102
- duplicate names: 0
- missing gates: 0
- broken prerequisites: 0

Authorities:
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.md`
- `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1_QA.md`

Important additions/recoveries:
Palace, Monument, Stone Works, Barracks, Shrine, Windmill, Artists' Guild, Director's Guild, Cinema, Consulate, Constabulary, Military Base, Ferris Wheel and Aquarium.

Important merges:
generic Museum -> Art/Archaeological Museum branch;
Gallery -> Art Museum;
Menagerie -> Zoo;
Bastion -> Star Fort;
Broadcast Tower -> Broadcast Center;
Hydro Plant -> Hydroelectric Dam infrastructure;
Spaceship Factory -> Space Launch Center.

Government building choices and Civ6 Water Park content are converted into Civ V-style city buildings without districts.


---

## Generic unit roster locked — 2026-09-21

The generic non-Great-Person unit roster is now consolidated and GitHub-Actions QA-passed.

Authorities:
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.md`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1_QA.md`
- `city_system/validate_final_generic_unit_roster_v1.py`
- `.github/workflows/civ-final-unit-roster-qa.yml`

Exact state:
- final generic units: **89**
- technology-master units: **74**
- civic-only/civic-owned units: **7**
- recovered game-start/religion-system units: **5**
- duplicate unit names: **0**
- forbidden baseline units returned: **0**
- Great People accidentally mixed into generic roster: **0**
- GitHub Actions QA: **PASS**
- workflow run: **35527600918**
- validated head: `93798325946e29ffd699327bc93ba1c74c28e3ed`

Baseline/system units recovered outside the unlock tables:
- Settler
- Warrior
- Scout
- Missionary
- Inquisitor

Important audit/master mismatch corrections:
- **Mechanized Infantry -> Combined Arms**
  - Modern/Atomic audit records already remapped it to Combined Arms, but it had been omitted from the final 109-tech UNITS field.
- **Missile Cruiser -> Guidance Systems + Warships**
  - Atomic audit plus the Lasers master note already moved it there, but it had been omitted from the Guidance Systems UNITS field.

Explicit exclusions remain:
- Heavy Chariot: no separate generic unit
- Nuclear Missile: no standalone generic unit; use Nuclear/Thermonuclear Device delivery system
- Giant Death Robot: baseline Information-era unit at Robotics; Future upgrades at Advanced AI / Advanced Power Cells / Cybernetics / Smart Materials
- Great People: separate Great Person systems

Major role families now represented:
- Recon: Scout -> Explorer -> Ranger -> Spec Ops
- Ranged infantry: Archer -> Composite Bowman -> Crossbowman -> Skirmisher -> Gatling Gun -> Machine Gun
- Siege: Catapult -> Trebuchet -> Bombard -> Field Gun -> Artillery -> Rocket Artillery
- Front-line firearm infantry: Fire Lance -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry
- Armored: Landship -> Tank -> Modern Armor
- Submarine: Submarine -> Nuclear Submarine
- Fighter: Triplane -> Fighter -> Jet Fighter
- Bomber: Great War Bomber -> Bomber -> Stealth Bomber

These are role/progression families. Exact one-click upgrade edges, combat strength, cost, movement, promotions and strategic-resource quantities remain for the later military numerical-balance pass.

### Current immediate content-design state

The following large generic content sets are now consolidated:
- 109 technologies
- 72 civics
- 127 policy cards
- 102 generic/national buildings
- 89 generic non-Great-Person units
- 5 restored former-Great-Person Worker-built improvements
- 32 corporation sectors / 98 signature founders

The next clean consolidation target is the **full generic tile-improvement / route / infrastructure roster**, because technology and civic masters contain these unlocks but there is not yet a building-style canonical roster for the complete set.


---

## Generic map improvement / infrastructure roster locked — 2026-09-21

The complete generic map-side improvement, route and infrastructure unlock layer is now consolidated and GitHub-Actions QA-passed.

Authorities:
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv`
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.md`
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1_QA.md`
- `tile_system/validate_final_generic_map_roster_v1.py`
- `.github/workflows/civ-final-map-roster-qa.yml`

Exact state:
- canonical records: **39**
- technology-master map entries: **32**
- civic/special entries: **7**
- directly buildable rows: **28**
- rule/capability/upgrade/special rows: **11**
- duplicate names: **0**
- forbidden/nonbaseline items present: **0**
- GitHub Actions QA: **PASS**
- workflow run: **35527902714**
- validated head: `efd057e0042e04dd7c832369f5154f5518983cbd`

Important consolidation rules:
- Road bridges, military-road construction and improved road movement are route capabilities/upgrades, not new route objects.
- Hill Farm is a Farm placement rule, not a second Farm improvement.
- Reforestation is a Worker action, not a permanent improvement type.
- National Park is a Naturalist-created special protected area.
- Historic Landmark is an Archaeologist-created special improvement and remains distinct from the Worker-built Humanism Landmark.
- Dam -> Hydroelectric Dam is infrastructure progression.
- Canal is Steam Power + Civil Engineering.
- Aerodrome/Preserve districts remain excluded from the Civ V-style map/city baseline.

Former Great Person improvements integrated:
- Academy
- Manufactory
- Customs House
- Holy Site
- Landmark

Citadel remains excluded.

Environmental cross-gates are explicit:
- Wind Farm -> Composites + Environmentalism
- Solar Farm -> Ecology + Environmentalism
- Geothermal Plant -> Ecology + Environmentalism
- Offshore Wind Farm -> Predictive Systems + Environmentalism

The Ecology technology master was synchronized so Solar Farm explicitly carries Environmentalism, matching the already-locked civic rule.

### Consolidated generic content state after this pass

- 109 technologies
- 72 civics
- 127 policy cards
- 102 generic/national buildings
- 89 generic non-Great-Person units
- 39 generic map improvement/route/infrastructure records
- 32 corporation sectors
- 98 signature corporate founders

The core generic **existence + unlock ownership** layer is therefore substantially consolidated. Remaining large design layers are now primarily numerical/gameplay layers rather than missing generic-content ownership:
- military stats and strict upgrade edges
- tile yields/build times/terrain constraints
- building numerical yields/costs
- Great Person and specialist numerical rules/rosters
- World Wonder audit
- civilization-specific unique content


---

## Advanced founding-unit progression locked — 2026-09-21

The generic unit roster is superseded from 85 to **88** units by adding three advanced founding units.

Authority:
- `city_system/SETTLER_PROGRESSION_V1.csv`
- `city_system/SETTLER_PROGRESSION_V1.md`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`

Final line:

`Settler -> Pioneer -> Colonist -> Urban Planner`

Final gates and starting population:
- Settler: game start, population 1
- Pioneer: Cartography + Exploration, population 2
- Colonist: Railroad + Colonialism, population 3
- Urban Planner: Combustion + Urbanization, population 4

**All four use the same base founding-territory rule.** Later founding units do not receive a larger initial tile claim.

Founding infrastructure V1 (expanded previous-era core rule):
- Settler: none
- Pioneer: 10 core buildings through Renaissance
  - Monument, Granary, Library, Market, Aqueduct, Amphitheater, Arena, Workshop, University, Bank
- Colonist: 15 core buildings through Enlightenment
  - Pioneer package + Opera House, Public School, Stock Exchange, Newspaper Office, Zoo
- Urban Planner: 24 core buildings through Industrial
  - Colonist package + Factory, Hospital, Sewer, Food Market, Cold Storage, Cinema, Shopping Mall, Telegraph Office, Power Plant
- conditional local infrastructure:
  - Water Mill where eligible
  - Pioneer coastal: Harbor + Lighthouse
  - Colonist coastal: + Seaport
  - Urban Planner coastal: + Shipyard

Critical rule:
- free building never bypasses its normal technology/civic/local prerequisites
- if not eligible at the founding moment, it is not granted later for free
- one-per-civ, government-choice, religion-specialization, military-training, city-defense and museum-choice buildings remain outside the automatic core package
- Factory and Hospital are explicitly part of the Urban Planner package as major Industrial-era infrastructure.

Authority:
- `city_system/ADVANCED_SETTLER_FREE_BUILDING_PACKAGE_V1.md`
- `city_system/validate_settler_progression_v1.py`
- `.github/workflows/civ-settler-progression-qa.yml`

Replacement behavior:
- newly produced founding units use the newest unlocked class
- existing units already on the map do not auto-upgrade
- founding consumes the unit
- no free Worker is created after founding

The previous 7-population Urban Planner concept is rejected. Final starting-population progression is deliberately restrained at **1 -> 2 -> 3 -> 4**.


## Great Person class scope locked — 2026-09-21

No additional Great Person classes will be added beyond the already adopted Great Director.

Final class scope:
- Great General
- Great Admiral
- Great Scientist
- Great Engineer
- Great Merchant
- Great Prophet
- Great Writer
- Great Artist
- Great Musician
- Great Director

Great Diplomat, Great Explorer, Great Doctor, Great Architect, Great Philosopher, Great Sculptor and other mod-added classes are not adopted as separate classes.

Authority:
- `city_system/CIV5_STYLE_CITY_AND_GREAT_DIRECTOR_BASELINE_V1.md`


---

## Gathering Storm Future Era realignment locked — 2026-09-21

Authoritative late-era document:
- `tech_reference/GATHERING_STORM_FUTURE_ERA_REALIGNMENT_V1.md`

The project now uses a distinct **Future Era (era index 13)**.

Technology distribution:
- Atomic 5
- Information 9
- Future 8
- total remains 109

Civic distribution:
- Atomic 5
- Information 7
- Future 6
- total remains 72

Critical decisions:
- Giant Death Robot is baseline again at Robotics.
- GDR upgrades: Advanced AI / Advanced Power Cells / Cybernetics / Smart Materials.
- XCOM Squad is Future and unlocks at Cybernetics + Rapid Deployment.
- Spec Ops is Atomic because Rapid Deployment is Atomic.
- generic unit roster total is **89**.
- Environmentalism is Information.
- Information/Future infrastructure follows the latest gate era.
- Future policies are separated from Information; total policy cards remains 127.
- old SS Engine / SS Stasis Chamber space-part abstractions are superseded.

Science-victory chain:
`Launch Earth Satellite -> Moon Landing -> Launch Mars Colony -> Exoplanet Expedition -> Terrestrial/Lagrange Laser Stations`

Cross-system validation:
- 109 technologies
- 72 civics
- 89 units
- 127 policies
- 39 map/infrastructure records
- 102 buildings
- missing references 0
- backward-era edges 0
- content-earlier-than-gate violations 0
- **PASS**


---

## Final direct unit upgrade graph locked — 2026-09-21

Authorities:
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.md`
- `city_system/FINAL_UNIT_UPGRADE_SOURCE_AUDIT_V1.md`
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1_QA.md`
- `city_system/validate_final_unit_upgrade_graph_v1.py`
- `.github/workflows/civ-final-unit-upgrade-graph-qa.yml`

Exact state:
- generic units covered: **89/89**
- direct graph rows: **89**
- unknown successors: **0**
- era-regressing edges: **0**
- directed cycles: **0**
- explicit branch-choice rows: **1**
- structural validation: **PASS**

Major lines:
- Warrior -> Swordsman -> Man-at-Arms -> Arquebusier -> Line Infantry -> Rifleman -> Infantry -> Mechanized Infantry
- Fire Lance -> Arquebusier
- Spearman -> Pikeman -> Pike and Shot -> Anti-Tank Gun -> Modern AT
- Archer -> Composite Bowman -> Crossbowman -> Skirmisher -> Gatling Gun -> Machine Gun
- Catapult -> Trebuchet -> Bombard -> Field Gun -> Artillery -> Rocket Artillery
- Scout -> Explorer -> Ranger -> Spec Ops
- Horseman -> Cavalry -> Helicopter
- Chariot Archer -> Knight -> Lancer -> Landship -> Tank -> Modern Armor
- Trireme -> Caravel -> Ironclad -> Destroyer
- Privateer -> Submarine -> Nuclear Submarine
- Paratrooper -> XCOM Squad
- Battering Ram -> Siege Tower -> Medic -> Supply Convoy
- Observation Balloon -> Drone

Naval ranged branch:
- Quadrireme -> Galleass -> Frigate
- Frigate -> Ship of the Line -> Battleship -> Missile Cruiser
- Frigate -> Cruiser -> Missile Cruiser

Special rules:
- Settler -> Pioneer -> Colonist -> Urban Planner is **production replacement only**, not direct unit upgrading.
- Marine remains terminal amphibious specialist rather than upgrading to XCOM.
- Giant Death Robot has no successor unit; Future technologies apply module upgrades to the same GDR.
- Guided Missile is consumable.

### Next military task

Direct upgrade ownership is finished.

Next:
1. Combat Strength / Ranged Strength
2. Movement / Range
3. production cost
4. Gold maintenance
5. strategic-resource requirement and per-turn consumption
6. upgrade Gold cost
7. promotion/class interactions

Use Civ V BNW values as primary anchors, with Civ VI / Gathering Storm and adopted era-mod units interpolated only where Civ V has no matching unit.


---

## Unit numeric balance V1 locked — 2026-09-21

Authorities:
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V1.csv`
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V1.md`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V1.csv`
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V1_QA.md`
- `city_system/validate_final_unit_numeric_balance_v1.py`
- `.github/workflows/civ-final-unit-numeric-balance-qa.yml`

Exact state:
- canonical units: **89**
- numeric rows: **89**
- locked military/support/trade numeric rows: **80**
- intentionally deferred system-economy rows: **9**
- direct Gold upgrade edges priced: **55**
- numeric validation: **PASS**

Primary numerical scale:
- Civilization V BNW exact stats where directly available;
- Civ V stage remapping/interpolation for project historical stages;
- Civ VI / Gathering Storm scaled into Civ V magnitude only where Civ V has no matching unit;
- Pouakai Enlightenment Era adopted units interpolated between Civ V anchors.

Important economic rules:
- no invented fixed per-unit Gold maintenance; retain Civ V-style global maintenance formula;
- explicit strategic-resource units reserve 1 slot;
- strategic-resource upkeep per turn remains 0 in V1;
- do not silently convert the project to Gathering Storm's per-turn strategic-resource economy.

System-economy costs deliberately deferred:
- Settler
- Pioneer
- Colonist
- Urban Planner
- Missionary
- Inquisitor
- Spy
- Naturalist
- Rock Band

Those require founding/Faith/espionage/conservation/culture-specific pricing.

Upgrade Gold:
- 55 direct edges
- production-cost-difference formula derived from Civ V
- project 13 eras compressed to Civ V-equivalent indices
- founding production-replacement edges receive no Gold-upgrade cost

Next military task:
1. promotion trees and retained promotions
2. anti-class / city / terrain combat modifiers
3. healing/support aura values
4. interception/evasion and air-sweep rules
5. cargo eligibility and missile/air basing rules


---

## Unit promotion / innate ability / air combat V1 locked — 2026-09-21

Authorities:
- `city_system/FINAL_UNIT_PROMOTION_SYSTEM_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_PROFILE_ASSIGNMENT_V1.csv`
- `city_system/FINAL_UNIT_INNATE_ABILITIES_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_INHERITANCE_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_AND_ABILITY_SYSTEM_V1.md`
- `city_system/FINAL_UNIT_PROMOTION_AND_ABILITY_SYSTEM_V1_QA.md`
- `city_system/FINAL_GDR_MODULE_BALANCE_V1.csv`
- `city_system/FINAL_AIR_INTERCEPTION_UNIT_RULES_V1.csv`
- `city_system/FINAL_AIR_COMBAT_GLOBAL_RULES_V1.csv`
- `city_system/FINAL_AIR_COMBAT_AND_GDR_RULES_V1.md`
- `city_system/FINAL_AIR_COMBAT_AND_GDR_RULES_V1_QA.md`

Current exact state:
- 89/89 units assigned a promotion profile
- 70 promotion definitions
- 60 innate ability rules
- 15 promotion-inheritance rules
- structural QA: PASS

Important promotion decisions:
- Civ V-style Shock/Drill, Accuracy/Barrage, naval Targeting/Bombardment, Coastal Raider/Boarding Party, Wolfpack, air Interception/Dogfighting retained
- Chariot Archer -> Knight converts ranged promotions to melee equivalents
- Privateer -> Submarine converts highest surface-raider rank into same Wolfpack rank
- GDR cannot gain ordinary XP/promotions; promotion profile NONE

GDR modules:
- Advanced AI -> AA Defense Strength 130
- Advanced Power Cells -> city ranged strength 130 / full defense effectiveness
- Cybernetics -> Moves 8 + Mountain Jump
- Smart Materials -> +10 defensive strength vs land/naval

Air interception:
- Triplane 50%
- Fighter / Jet Fighter / AA Gun / Mobile SAM / Missile Cruiser 100%
- Destroyer 40%
- one interceptor per attack
- base one interception per unit/turn
- Sortie gives fighter +1 interception
- evasion check occurs before interception chance
- Stealth Bomber and Guided Missile have innate 100% evasion
- learned Evasion promotion instead reduces interception damage by 50%

Next remaining military-system tasks:
1. exact naval/air/missile cargo eligibility
2. Prize Ships capture chance
3. support-aura stacking/formation interaction
4. XP thresholds / promotion acquisition cadence


---

## Generic unit operational rules V1 locked — 2026-09-21

Authorities:
- `city_system/FINAL_UNIT_CARGO_BASING_RULES_V1.csv`
- `city_system/FINAL_PRIVATEER_PRIZE_SHIPS_V1.csv`
- `city_system/FINAL_SUPPORT_UNIT_OPERATION_RULES_V1.csv`
- `city_system/FINAL_UNIT_XP_PROGRESSION_V1.csv`
- `city_system/FINAL_UNIT_OPERATIONAL_RULES_V1.md`
- `city_system/FINAL_UNIT_OPERATIONAL_RULES_V1_QA.md`
- `city_system/validate_final_unit_operational_rules_v1.py`
- `.github/workflows/civ-final-unit-operational-rules-qa.yml`

Exact locked state:

### Cargo / basing
- City air capacity: 6
- Aircraft Carrier base capacity: **2**, not 3
- Flight Deck I / II / III -> Carrier capacity 3 / 4 / 5
- Carrier may base Triplane, Fighter, Jet Fighter, Great War Bomber, Bomber
- Carrier may not base Stealth Bomber or Guided Missile
- Nuclear Submarine: 2 Guided Missiles
- Missile Cruiser: 3 Guided Missiles

### Prize Ships
Privateer capture chance:
`min(80, 10 + int((attacker_base_combat / defender_base_combat) * 40))`

- minimum 10%
- maximum 80%
- captured ship appears at 50 HP
- captured promotions do not transfer
- Prize Ships is lost on project Privateer -> Submarine transition

### Support formation
- one SUPPORT-class unit may share a tile with one friendly land combat unit
- only one SUPPORT-class unit occupies the support slot
- same aura category does not stack; strongest applies
- different categories may coexist

Values:
- Medic +20 stationary healing
- Supply Convoy +20 stationary healing and +1 Movement
- Observation Balloon +1 siege Range
- Drone +1 siege Range and +5 siege Ranged Strength

### XP
Civ V progression retained:
- cumulative promotion thresholds: 10, 30, 60, 100, 150, 210, 280, 360, 450
- formula: 5*(L-1)*L
- promotion opportunity may instead be spent to heal 50 HP
- Barbarian XP cap: 30
- GDR remains excluded from normal XP/promotion progression

Current operational QA: **PASS**

This closes the generic military-unit baseline for:
- roster
- unlocks
- direct upgrade graph
- numerical stats
- upgrade Gold
- promotions
- innate abilities
- GDR modules
- air combat
- cargo/basing
- support rules
- XP progression

Remaining military work is now mainly civilization-specific unique units and the separate nuclear-device delivery system.
