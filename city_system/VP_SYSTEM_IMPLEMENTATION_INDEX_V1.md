# VP 시스템 구현 인덱스 V1

기준일: 2026-09-23

상위 기준: `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`

## 1. 목적

Vox Populi의 핵심 시스템을 우리 게임에 거의 전면 도입하기로 한 뒤, 실제 구현 규칙으로 분해한 하위 문서의 현황을 추적한다.

## 2. 작성 완료 문서

| 문서 | 상태 | 핵심 내용 |
|---|---|---|
| `VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md` | 상위 기준 | VP 거의 전면 채택 원칙 |
| `VP_HAPPINESS_STABILITY_ADAPTATION_V1.md` | V1 구조 확정 | Needs, Happiness, Stability |
| `VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md` | V1 구조 확정 | War Weariness, Supply, 점령저항 |
| `VP_DIPLOMACY_VASSAL_CITYSTATE_V1.md` | V1 구조 확정 | Vassalage, 보호국, 자치령, 도시국가 |
| `VP_MONOPOLY_CORPORATION_ADAPTATION_V1.md` | V1 구조 확정 | Monopoly, Corporation, Franchise |
| `VP_PIONEER_COLONIST_COLONIAL_GOVERNMENT_V1.md` | V1 구조 확정 | Settler/Pioneer/Colonist, 식민정부 |
| `GREAT_REVOLUTIONARY_SYSTEM_V1.md` | V1 구조 확정 | GReP, 혁명가 유형, 독립/체제혁명 |
| `GOVERNMENT_POLICY_SWITCHING_COST_V1.md` | V1 구조 확정 | 정책교체 비용, 정부교체 비용, 과도기 |
| `VP_CITY_BUILDING_SPECIALIST_TRADE_V1.md` | V1 구조 확정 | 도시, 건물, Specialist, Trade |
| `VP_RELIGION_ESPIONAGE_CULTURE_WORLD_CONGRESS_V1.md` | V1 구조 확정 | 종교, 첩보, 문화, 관광, 세계의회 |
| `VP_AI_DIFFICULTY_IMPLEMENTATION_V1.md` | V1 원칙 확정 | AI 계층과 난이도 철학 |

## 3. 현재 잠긴 핵심 규칙

### 도시와 정치

- 도시 Happiness는 원인별로 추적한다.
- 국가 단위 Stability를 추가한다.
- 별도 Independence Pressure 게이지는 만들지 않는다.
- 독립과 반란은 Happiness, Stability, 정치상태, 사건으로 판정한다.

### 군사

- War Weariness 채택
- Military Supply Cap 채택
- 해외전쟁에 추가 보급비용
- 점령지 Partisan/저항 구조 도입

### 외교

- Vassalage 채택
- 자발/강제 종속 구분
- 보호국과 자치령 추가
- City-State Diplomacy 대폭 확장

### 경제

- Monopoly 채택
- Corporation/Office/Franchise 채택
- 기업은 역사적 창업자와 실제 산업기능으로 재설계
- 기업 창업에 Great Merchant와 Great Engineer 사용 가능

### 개척과 식민지

- Settler → Pioneer → Colonist 계보 채택
- 후기 개척자는 더 높은 초기개발 수준 보유
- 해외도시는 조건에 따라 식민정부에 귀속
- 식민정부는 반자동 운영
- 본국은 식민정부 산출 전체가 아니라 일부를 받음

### 혁명과 독립

- Great Revolutionary 직군 추가
- GReP는 일반 Specialist 중심이 아니라 사건/제도/사상에서 발생
- 식민정부는 본국과 별도 GReP 풀 사용
- Great Revolutionary가 식민정부에 등장하면 독립 가능
- Great Revolutionary 등장만으로 자동독립하지 않음
- 역사적 신생 문명 등장시기와 연동

### 정부와 정책

- 사회제도 완료 시 무료 정책 전면 재편
- 평상시 정책교체는 Culture 비용
- 정부교체는 Culture + Stability 손실 + 과도기
- 정부 전환은 개혁/체제전환/혁명적 전환의 3단계
- Great Revolutionary가 전환비용과 과도기에 개입

### 문화와 국제정치

- Historic Event 채택
- Great Work, Tourism, Archaeology 유지
- Great Philosopher에는 Great Work of Philosophy를 만들지 않음
- Great Prophet은 Faith 직접 구매 유지
- World Congress 확대

### AI

- AI가 시스템을 이해한 뒤 난이도 보너스를 보조적으로 받는 구조
- 도시 문제 해결형 생산 AI
- Supply/War Weariness를 고려한 전쟁 AI
- 식민정부와 독립 AI
- 기업과 Great Person 사용 AI

## 4. 다음 세부 작업

### A. 건물 재감사

기존 건물표를 VP 역할분화 기준으로 다시 본다.

- Happiness 원인 완화
- Health
- Power
- Specialist
- Supply
- Espionage
- Trade

### B. 정부 목록과 전환행렬

기존 정부 후보를 확정한 뒤 각 정부쌍을:

- 개혁
- 체제전환
- 혁명적 전환

으로 분류한다.

### C. Great Revolutionary 후보군

- 시대별 후보 수집
- Great General/Philosopher와 중복 감사
- 독립형/체제형/사회혁명형/확산형 분류
- 개별 능력 설계

### D. 후기 개척자 수치

- Pioneer 해금
- Colonist 해금
- 초기 인구
- 무료 건물
- 식민정부 생성 조건

### E. VP 유닛계보 대조

기존 우리 유닛표와 VP 유닛계보를 대조해 시대별 공백을 확인한다.

### F. 종교/첩보 세부수치

- Belief 목록
- Spy Point 도입 여부
- 첩보임무 목록

### G. AI 평가함수

각 시스템의 가중치와 시나리오 테스트를 작성한다.

## 5. VP 공식 확인 경로

기준 저장소:

`LoneGazebo/Community-Patch-DLL`

주요 확인 파일:

- `(2) Vox Populi/Database Changes/Text/en_US/Concepts/NewConceptText.xml`
- `(2) Vox Populi/Database Changes/Units/NewUnits.xml`
- `(2) Vox Populi/Database Changes/Units/UnitChanges2.sql`
- `(2) Vox Populi/Core Files/New UI/VassalageOverview.lua`
- `(2) Vox Populi/Database Changes/Corporations/CorporationChanges.sql`
- `CvGameCoreDLL_Expansion2/CvPlayerAI.cpp`
- `CvGameCoreDLL_Expansion2/CvCityStrategyAI.cpp`

## 6. 현재 상태

**VP의 주요 시스템을 우리 게임의 구조로 옮기는 1차 설계 분해 완료.**

다음 단계부터는 `도입 여부`를 다시 논의하기보다, 각 시스템의 **구체적 데이터와 수치**를 확정하는 단계로 진행한다.
