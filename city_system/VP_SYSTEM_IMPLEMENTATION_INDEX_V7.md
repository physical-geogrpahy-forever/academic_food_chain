# VP 시스템 구현 인덱스 V7

기준일: 2026-09-23
상태: FINAL BUILDING MASTER PASS / HEALTH POWER STABILITY BUILDING LAYERS FLATTENED / RUNTIME AUTOPLAY DEFERRED UNTIL GAME ENGINE EXISTS

상위 기록:

- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V6.md`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5_QA.md`
- `city_system/STABILITY_BUILDING_SUPPORT_V1.md`
- `city_system/FINAL_BUILDING_REMAINING_PROVISIONAL_AUDIT_V1.md`

## 1. 현재 핵심 권위본

### 기술 및 사회제도

- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
- `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`

### Building

최종 gameplay numeric authority:

- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`

생성 및 검증:

- `city_system/build_final_building_master_v1.py`
- `city_system/test_build_final_building_master_v1.py`
- `city_system/validate_final_building_master_v1.py`
- `city_system/test_validate_final_building_master_v1.py`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5_QA.md`

입력 권위:

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- V3 numeric override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
- V4 Power override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
- Health building values: `health_system/HEALTH_BUILDING_VALUES_V1.csv`

### Power and Pollution

- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/VP_TILE_IMPROVEMENT_POWER_OVERRIDE_V3.csv`
- `city_system/POWER_POLLUTION_BRIDGE_V1.csv`

### Health and Plague

- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

### Happiness and Stability

구조 권위:

- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `city_system/GOVERNMENT_POLICY_SWITCHING_COST_V1.md`
- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`
- `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`

Building Stability 값 권위:

- `city_system/STABILITY_BUILDING_SUPPORT_V1.md`
- final field: `STABILITY_POINTS_FINAL`

## 2. Building master 최종 병합 순서

1. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
2. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
3. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
4. `HEALTH_BUILDING_VALUES_V1.csv`
5. 기존 `STABILITY_POINTS_PROVISIONAL`을 검증된 Building Stability support 값으로 `STABILITY_POINTS_FINAL`에 승격
6. stale Health/Power pending marker 정리

최종 master는 신규 V3 ADD 건물에도 Power, Health, Stability 기본값 0을 명시적으로 부여한다.

## 3. Stability Building layer 확정

`STABILITY_POINTS_FINAL`은 국가 `State Stability`에 즉시 더하는 직접 보너스가 아니다.

의미:

```text
행정 및 정치 제도가 국가질서를 유지하는 데 제공하는 건물 기반 지원점수
```

기존 17개 nonzero provisional 값을 수치 변경 없이 final로 승격했다.

- Palace, Courthouse, Government Plaza: 2
- National History Museum: 2
- Ancestral Hall, Audience Chamber, Consulate, Warlord's Throne: 1
- Court: 1
- Foreign Ministry, Grand Master's Chapel, Intelligence Agency: 1
- Telegraph Office: 1
- Royal Society, War Department: 1
- Chancery, Constabulary: 1

국가 Stability 전체식은 아직 별도 정량화 대상이다. 대형 제국이 반복 행정건물로 Stability를 무한히 쌓지 않도록 도시 수, 인구, 점령지와 식민정부의 행정 수요에 대해 정규화한다.

## 4. provisional 필드 상태

`FINAL_BUILDING_REMAINING_PROVISIONAL_AUDIT_V1.md` 기준:

- Building rows: 104
- provisional columns: 2
- unresolved nonzero provisional entries: 0

`HEALTH_POINTS_PROVISIONAL`:

- 9개 nonzero 행
- `HEALTH_POINTS_FINAL`로 대체된 provenance

`STABILITY_POINTS_PROVISIONAL`:

- 17개 nonzero 행
- `STABILITY_POINTS_FINAL`로 대체된 provenance

따라서 두 provisional 열은 gameplay authority가 아니다.

## 5. Building master QA 상태

현재 전체 검증 기준:

- merged roster: 104
- numeric master: 104
- duplicate building: 없음
- roster/master 누락: 없음
- Tech/Civic gate 누락: 없음
- Health final blank: 없음
- Power load blank: 없음
- Stability final blank: 없음
- nonzero Stability provisional/final mismatch: 없음
- validation warnings: 0

의도적으로 남긴 deferred special effects는 2개뿐이다.

1. Cold Storage
   - `FOOD_STORAGE_TRADE_LOSS_REDUCTION=PENDING_LOGISTICS_SYSTEM`
2. Grid Battery Storage
   - `POWER_SYSTEM_CAPACITY=PENDING`

이 둘은 Building row 미완성이 아니라 각각 Logistics와 전력 저장용량 시스템의 후속 결정이다.

## 6. CI

`.github/workflows/build-final-building-master.yml`은 다음을 순서대로 실행한다.

1. merge fixture test
2. validator fixture test
3. Building cross-gate repair
4. merged master 생성
5. 전체 validator
6. provisional audit
7. generated master와 QA 자동 커밋

fixture는 Stability 승격과 provisional/final mismatch 검출도 포함한다.

## 7. 다음 정량화 순서

Building master 자체의 정적 flatten은 완료 상태로 두고 다음 정치 시스템을 순서대로 수치화한다.

1. City Happiness 정량식
2. War Weariness 정량식
3. 정부교체 Culture 비용, 과도기, Stability 충격
4. 점령지와 식민정부의 Stability 부담
5. `STABILITY_POINTS_FINAL`을 포함한 State Stability 전체식

그 후 Logistics와 Grid Battery 저장용량 규칙을 처리하면 Building master의 의도적 deferred 2건도 제거할 수 있다.

## 8. runtime 원칙

현재 저장소에는 완성된 게임 엔진이 없다.

따라서:

- 정적 fixture와 validator를 실제 autoplay라고 부르지 않는다.
- Science/Culture, upgrade Gold, Health, Power, Building master의 현재 QA는 pre-runtime 정적 검증이다.
- 실제 turn telemetry와 autoplay는 게임 엔진 구현 뒤 수행한다.

## 9. 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V7.md`
2. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
3. `city_system/STABILITY_BUILDING_SUPPORT_V1.md`
4. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
5. Power, Health, Happiness/Stability 세부 권위본
6. Building V4/V3/V2 입력 파일
7. Tech/Civic/Unit/Tile/Resource 각 세부 권위본
8. 이전 V6/V5/V4/V3/V2/V1 인덱스 및 감사 파일

## 10. 현재 판정

최종 Building numeric master는 104개 건물 전체를 단일 authoritative table로 flatten했다.

Health, Power와 Building Stability support는 각각 독립 final field로 유지한다. Food, Production, Health, Power, Stability를 서로 같은 수치로 취급하지 않는다.

다음 정치 정량화 시작점은 `City Happiness`다.
