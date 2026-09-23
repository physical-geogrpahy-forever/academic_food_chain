# VP 독점과 기업 시스템 적용안 V1

기준일: 2026-09-23

상위 문서: `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`

## 1. 목적

Vox Populi의 Monopoly, Corporation, Office, Franchise, 국제교역 연결 구조를 우리 게임의 역사적 기업, 자원 원산지, 자원 확산, Great Merchant/Great Engineer 시스템과 통합한다.

## 2. VP에서 확인된 핵심 구조

VP 기업 시스템은 특정 자원 독점을 기업 창설 조건으로 사용한다. 기업은 본사와 Office, Franchise를 통해 확장되고 국제교역로와 연결된다.

VP 공식 데이터에서는 기업별로 다음과 같은 요소가 존재한다.

- 필요한 자원 Monopoly
- 기본 Franchise 수
- 추가 Trade Route
- Franchise 확산
- 특정 건물 산출 보너스
- 특정 Specialist 산출 보너스
- 국제교역로 보너스
- Franchise 수에 따른 효과
- 자원 산출 보너스

즉 기업은 단순 `Gold +X` 건물이 아니라 자원, 도시, 전문가, 교역망을 묶는 후반 경제 시스템이다.

## 3. 우리 게임 기본 원칙

VP의 구조를 적극 채택하되 기업 이름과 창업 조건은 실제 역사 기반으로 재설계한다.

우리 게임 기업의 기본 구조:

```text
기술/사회조건
+
관련 자원 또는 산업기반
+
창업 가능한 Great Person
↓
기업 설립
↓
본사
↓
국내 지사
↓
해외 지사/Franchise
↓
상품, 서비스, 교역 효과
```

## 4. Monopoly

Monopoly는 한 문명이 특정 자원의 세계 생산 또는 실질 시장지배력을 충분히 확보한 상태다.

VP의 정확한 임계값을 그대로 쓰지 않는다.

우리 게임에서는 다음을 고려한다.

- 직접 소유 생산량
- 식민정부 생산량
- 종속국 공급권
- 장기 교역계약
- 기업이 확보한 공급망
- 세계 총생산량

### 자원 Monopoly의 의미

Monopoly는 단순 보너스가 아니라 다음 기능의 조건이 될 수 있다.

- 기업 창업
- 가격우위
- 특정 건물 보너스
- 외교적 영향력
- 전략자원 통제
- 세계의회 안건

## 5. 동적 자원 시스템과의 충돌 방지

우리 게임의 자원은 고정적으로 모든 문명이 처음부터 아는 것이 아니다.

따라서 Monopoly 계산은 `지도상 존재량`이 아니라 **현재 세계경제에서 발견되고 이용 가능한 공급량**을 기준으로 한다.

예:

```text
아메리카에 아직 알려지지 않은 자원
→ 유럽 문명 Monopoly 계산에서 제외

접촉 이후 교역망에 편입
→ 세계 공급량에 포함
```

이 규칙은 자원 발견과 확산 시스템을 훼손하지 않는다.

## 6. 기업 창업자

기업은 아무 도시에서 Production으로 바로 건설하지 않는다.

주요 창업 방식:

- Great Merchant
- Great Engineer
- 일부 특수 Great Person

창업 가능한 인물은 실제 역사적 기업 창업과 연결한다.

예:

- 상업/금융기업: Great Merchant 중심
- 제조/기술기업: Great Engineer도 가능

이미 확정한 위인 후보제와 동일하게 역사적 인물은 전세계에서 한 번만 영입된다.

## 7. 기업 본사

기업 설립 시 한 도시에 Headquarters가 생긴다.

본사의 역할:

- 기업의 기준 도시
- 기본 수익
- 지사 효과 집계
- 일부 Specialist 슬롯 또는 산출
- 기업별 고유능력

본사가 정복되었을 때 기업 소유권을 즉시 넘길지는 별도 규칙으로 둔다. 기본안은 `기업은 문명 소속, 본사는 재배치 가능`이다.

## 8. Office와 국내 지사

VP의 Office 개념을 채택한다.

Office가 있는 도시는:

- 기업 상품 생산
- 관련 Specialist 보너스
- 관련 건물 보너스
- 해외 Franchise와 연결되는 교역 보너스

을 받을 수 있다.

모든 도시에 무조건 Office를 짓는 구조는 피하고 기업별 제한 또는 유지비를 둔다.

## 9. Franchise와 해외 확장

VP의 Franchise 개념을 적극 채택한다.

Franchise는 외국 도시 또는 종속국 도시에 해당 기업의 경제적 존재가 생긴 상태다.

확산 수단:

- 국제 Trade Route
- 외교협정
- 투자
- 특정 Great Merchant 능력
- 기업 고유효과

Franchise는 도시 소유권을 바꾸지 않고 경제적 영향력을 확장한다.

## 10. 기업 상품과 서비스

우리 게임에서는 기업이 단순 산출량 보너스만 주지 않는다.

기업 유형에 따라 실제 기능을 둔다.

### 제조업

- Production
- 특정 자원 가공
- 유닛/건물 생산비
- 전략자원 효율

### 정유/에너지

- 석유제품
- Production
- Power
- 운송효율

### 식품/농업

- Food
- 농업생산성
- 식량 교역

### 금융

- Gold
- 국제교역
- 투자
- 기업 확산

### 문화/미디어

- Culture
- Tourism
- Broadcast/Cinema/Media 계열

### 기술기업

- Science
- Research Project
- 고급 제조

### 서비스기업

- 도시별 기능 보너스
- 관광
- 금융
- 물류

## 11. 자원과 기업 연결

VP처럼 기업마다 관련 자원군을 둔다.

다만 우리 게임에서는 자원군이 실제 산업과 맞아야 한다.

예:

```text
석유기업
Oil 접근 필요
→ Refinery와 연동
→ 석유제품 생산

섬유기업
Cotton 또는 Dyes 등 관련 공급망 필요
→ Factory/Shopping 계열 연동
```

기업 창업 조건에 반드시 세계 Monopoly만 요구할지는 기업별로 다르게 한다. 일부 기업은 충분한 공급망 확보만으로 가능하다.

## 12. 기업과 Specialist

VP처럼 기업이 Specialist 산출을 바꾸는 구조를 채택한다.

예:

- 기술기업 → Scientist/Engineer
- 금융기업 → Merchant
- 미디어기업 → Artist/Writer/Director
- 행정서비스기업 → Civil Servant가 존재한다면 연계 가능

기업이 해당 직종의 경제적 가치를 바꾸는 느낌을 준다.

## 13. 교역로

기업 확산의 핵심은 Trade Route다.

국제 Trade Route가 Franchise 도시를 연결하면:

- 본사 또는 Office 보너스
- Franchise 도시 보너스
- 상품/서비스 확산
- 일부 Culture/Tourism/Science 확산

이 가능하다.

우리 동적 자원 인지 시스템과도 연결해 기업 교역망이 새로운 자원 사용권을 확산할 수 있다.

## 14. 식민정부와 기업

식민정부의 자원은 본국 기업의 공급망에 포함될 수 있다.

그러나 식민정부 독립 시:

- 자원공급 계약 유지 여부
- 본국기업 Franchise 유지 여부
- 기업 국유화 가능성

등을 사건으로 처리할 수 있다.

## 15. 국가정책과 기업

정부와 정책은 기업 시스템에 영향을 줄 수 있다.

- 자유시장
- 보호무역
- 국유화
- 기업세
- 식민무역
- 반독점정책

후기 정부/이념 체계와 연결한다.

## 16. World Congress

기업은 국제정치의 대상이 된다.

가능한 결의:

- 특정 자원 금수
- 기업 제재
- 자유무역
- 환경규제
- 독점규제

## 17. AI

AI는 기업을 단순히 첫 가능 기업으로 설립하지 않는다.

판단 요소:

- 확보 자원
- 도시 전문화
- Trade Route 수
- 경쟁 기업
- 승리전략
- Great Person 기회비용

## 18. 그대로 복사하지 않는 것

- VP의 가상 기업 이름
- VP의 정확한 Franchise 수치
- VP의 자원군 구성
- VP의 기업별 고정 산출량
- Monopoly 임계값을 그대로 복사

## 19. 확정 상태

- Monopoly: 채택
- Headquarters: 채택
- Office: 채택
- Franchise: 채택
- Trade Route 기반 확산: 채택
- 실제 역사적 기업과 창업자: 우리 확장
- 기능성 상품/서비스: 우리 확장
- Great Merchant와 Great Engineer 창업: 확정 방향

## 20. VP 확인 자료

- `(2) Vox Populi/Database Changes/Corporations/CorporationChanges.sql`
- `(1) Community Patch/Database Changes/Corporations/NewCorporationTables.xml`
- `(2) Vox Populi/Core Files/New UI/CorporationsOverview.lua`

상태: **V1 구조 확정, 개별 기업 목록과 수치 미확정**
