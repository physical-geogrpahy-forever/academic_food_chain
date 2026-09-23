# VP 시스템 구현 인덱스 V6

기준일: 2026-09-23
상태: BUILDING MASTER FLATTEN PIPELINE READY / RUNTIME AUTOPLAY DEFERRED UNTIL GAME ENGINE EXISTS

상위 기록:

- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V5.md`
- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

## 0. V5 정정

V5의 다음 작업에서 `runtime autoplay harness 또는 게임 엔진 연결 경로 확정`을 즉시 수행하도록 적은 것은 현재 개발 단계와 맞지 않는다.

현재 저장소는 게임 규칙, 데이터, 지도, 수치 체계를 설계하고 정적 검증하는 단계이며 완성된 Civilization 실행 엔진 자체가 아직 없다. 따라서 실제 runtime autoplay는 현재 단계의 선행 조건이나 다음 작업이 아니다.

정적 계산기나 fixture 테스트를 `실제 autoplay`라고 부르지 않는다.

실제 runtime autoplay는 향후 게임 엔진이 구현된 뒤 수행한다.

## 1. 현재 시스템 권위본

### 기술 및 사회제도

- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
- `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`

### 유닛

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP_QA.md`

### 타일 및 자원

- `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
- `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
- `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`
- `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
- CONTACT_DYNAMIC_V2 biological-resource visibility rules

### Building

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- V3 numeric override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
- V4 Power override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`

### Power and Pollution

- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/VP_TILE_IMPROVEMENT_POWER_OVERRIDE_V3.csv`
- `city_system/POWER_POLLUTION_BRIDGE_V1.csv`

### Health and Plague

- `health_system/HEALTH_AND_PLAGUE_QUALITATIVE_INTEGRATION_V1.md`
- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

## 2. Building 최종 수치 master flatten 규칙

새 생성기:

- `city_system/build_final_building_master_v1.py`
- `city_system/test_build_final_building_master_v1.py`

목표 출력:

- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`

병합 순서:

1. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
2. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
3. `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
4. `HEALTH_BUILDING_VALUES_V1.csv`

이 순서는 단순 문서 우선순위가 아니라 실제 flatten 순서다.

### V3 처리

- `ADD`: Smokehouse, Forge 같은 신규 일반 건물을 base master에 추가한다.
- `OVERRIDE_SPECIAL_EFFECT`: Factory, Research Lab 등 기존 행의 V3 수치/특수효과를 덮어쓴다.
- Factory의 Worker-built Manufactory bonus +1과 Research Lab의 Worker-built Academy bonus +1을 유지한다.

### Power 처리

최종 master에 다음 필드를 추가한다.

- `POWER_LOAD`
- `POWERED_BONUS`
- `POWER_SOURCE_RULE`

Aquatics Center의 `Local Happiness 2 -> 1` 같은 명시적인 base correction도 flatten 시 실제 base 수치에 적용한다.

Power 발전량과 일반 Production bonus는 같은 필드로 합치지 않는다.

### Health 처리

최종 master에 다음 필드를 추가한다.

- `HEALTH_EFFECT_TYPE`
- `HEALTH_POINTS_FINAL`
- `SPONTANEOUS_PLAGUE_RISK_MULT`
- `PLAGUE_DURATION_MOD_TURNS`
- `HEALTH_OTHER_EFFECT`

기존 V2의 `HEALTH_POINTS_PROVISIONAL`은 provenance용으로 남길 수 있으나 실제 게임 수치 권위는 `HEALTH_POINTS_FINAL`이다.

Aqueduct는 일반 FLAT +2가 아니라 `WATER_HEALTH_FLOOR=2`다. 자연 담수 +2와 중복 합산하지 않는다.

Factory, Coal Power Plant, Power Plant에는 direct negative Health를 넣지 않는다. Pollution bridge를 통해 Health에 영향을 준다.

Harbor와 Airport도 direct negative Health를 넣지 않고 plague network exposure에서 처리한다.

## 3. merge generator QA

fixture 테스트가 확인하는 최소 조건:

- Smokehouse ADD가 실제 신규 행을 만든다.
- Factory V3 특수효과가 `PROJECT_MANUFACTORY_PRODUCTION=+1`로 반영된다.
- Factory Power load가 결합된다.
- Food Market의 powered Food bonus와 Health +1이 한 행에 공존한다.
- Aquatics Center base Local Happiness가 1로 보정된다.
- Coal Power Plant의 발전 규칙이 결합된다.
- Aqueduct가 `WATER_HEALTH_FLOOR`, Health 2로 병합된다.
- 병합 후 `BUILDING_EN` 중복을 허용하지 않는다.

fixture 기준 `BUILDING_MASTER_MERGE_TEST: PASS`를 확인했다.

## 4. 현재 pre-runtime 검증 상태

완료된 정적 검증:

- Science/Culture Standard-speed 비용 곡선 QA
- Unit upgrade Gold V2 QA
- Power source/demand 구조
- Power -> Pollution -> Health bridge
- Health/Plague 정량 규칙
- cross-system validator
- Building master flatten merge fixture

이 결과는 게임 플레이 결과나 실제 Civilization autoplay 결과가 아니다.

## 5. 현재 다음 작업

게임 엔진이 없는 현재 단계에서 다음 순서로 진행한다.

1. 최종 Building numeric master flatten 파일 생성 및 행 단위 QA
2. 기존 provisional Health/Power pending 문자열이 최종 master에서 실제 권위 필드와 충돌하지 않는지 검사
3. Building roster/unlock master와 numeric master의 건물명 전수 일치 검사
4. Technology/Civic unlock에 존재하는 건물이 roster/numeric master에 빠지지 않았는지 검사
5. Great People, Corporation, 정책/이념 등 아직 설계 중인 상위 시스템을 계속 확정
6. 게임 엔진 구현 단계가 시작된 뒤에야 runtime telemetry 및 autoplay를 추가

## 6. 현재 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V6.md`
2. 향후 생성될 `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
3. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
4. `health_system/HEALTH_BUILDING_VALUES_V1.csv`
5. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
6. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
7. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
8. Power, Health, Tech, Civic, Unit, Tile, Resource 각 세부 권위본
9. 이전 V5/V4/V3/V2/V1 인덱스 및 감사 파일

## 7. 현재 판정

**현재 병목은 runtime이 아니다.**

현재 해야 할 일은 이미 확정한 정적 규칙을 실제 단일 master 파일로 flatten하고, unlock/roster/numeric 간 누락과 충돌을 제거한 뒤 나머지 게임 시스템 설계를 계속 진행하는 것이다.
