# VP 시스템 구현 인덱스 V8

기준일: 2026-09-23
상태: CITY HAPPINESS QUANTITATIVE V1 LOCKED / BUILDING HAPPINESS LINKS VALIDATED / RUNTIME AUTOPLAY DEFERRED UNTIL GAME ENGINE EXISTS

역사적 선행본:

- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V7.md`

V7은 Building master, Health, Power, Building Stability layer까지 정리한 역사적 선행본으로 유지한다. V8부터 City Happiness 정량 규칙과 해당 QA를 현행 권위 체계에 포함한다.

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

Happiness 연결 검증:

- `city_system/validate_happiness_building_links_v1.py`
- `city_system/test_validate_happiness_building_links_v1.py`

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

### City Happiness

수치 권위:

- `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`
- `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`

실행식 및 검증:

- `city_system/calculate_city_happiness_v1.py`
- `city_system/test_calculate_city_happiness_v1.py`
- `city_system/generate_city_happiness_static_qa_v1.py`
- `city_system/CITY_HAPPINESS_STATIC_QA_V1.md`

구조 선행본:

- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`

### Stability and political switching

- `city_system/STABILITY_BUILDING_SUPPORT_V1.md`
- final Building field: `STABILITY_POINTS_FINAL`
- `city_system/GOVERNMENT_POLICY_SWITCHING_COST_V1.md`
- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`
- `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`

## 2. City Happiness 정량식 V1

시대별 기대치는 `HAPPINESS_ERA_EXPECTATIONS_V1.csv`의 13개 시대 행을 사용한다.

네 기본 Needs:

```text
supported_basic   = floor((gross_food_pre_health + production) / effective_basic)
supported_gold    = floor(gold / effective_gold)
supported_science = floor(science / effective_science)
supported_culture = floor(culture / effective_culture)

Distress    = max(0, population - supported_basic - distress_reduction)
Poverty     = max(0, population - supported_gold - poverty_reduction)
Illiteracy  = max(0, population - supported_science - illiteracy_reduction)
Boredom     = max(0, population - supported_culture - boredom_reduction)
```

Religious Unrest:

```text
religious_unrest_raw = minority_followers // 2
religious_unrest = max(0, religious_unrest_raw - religious_unrest_reduction)
```

종교 시스템이 비활성 상태이면 Religious Unrest는 0이다.

Citizen Needs 최종값은 인구를 넘을 수 없다.

```text
citizen_needs_unhappiness = min(population, sum of five post-reduction Needs)
```

Health는 Distress에 섞지 않고 별도 Unhappiness 축으로 유지한다.

```text
Health >= 0      -> 0
Health -1 to -2  -> 1
Health -3 to -4  -> 2
Health <= -5     -> 3
```

Local Happiness는 도시 인구를 초과하지 못한다.

```text
local_happiness_positive = min(population, max(0, local_happiness_sources))
```

최종 도시 Happiness:

```text
City Happiness
= Local Happiness
- Citizen Needs Unhappiness
- Health Unhappiness
- War Weariness Unhappiness
- Occupation Unhappiness
- Colonial Unhappiness
- Policy Burden Unhappiness
```

현재 마지막 네 항은 명시적 외부 입력 인터페이스다. 아직 해당 하위 시스템을 이 계산기 내부에서 임의 추정하지 않는다.

## 3. 상대 기대치 조정

같은 시대라도 전세계 실질 산출 수준이 표의 기준값과 다를 수 있으므로 선택적으로 global median을 넣을 수 있다.

각 Needs 기대치 보정계수는 기준 기대치 대비 전세계 median 비율을 사용하되 `0.90`에서 `1.10` 사이로 제한한다.

따라서 상대 보정은 시대표를 대체하지 않으며 한 번에 기대치를 10% 넘게 흔들지 못한다.

## 4. Building Happiness 연결 검증

104개 최종 Building master 전체를 strict validator로 검사한다.

필수 필드:

- `LOCAL_HAPPINESS`
- `VP_DISTRESS_REDUCTION`
- `VP_POVERTY_REDUCTION`
- `VP_ILLITERACY_REDUCTION`
- `VP_BOREDOM_REDUCTION`
- `VP_RELIGIOUS_UNREST_REDUCTION`
- `HEALTH_POINTS_FINAL`
- `STABILITY_POINTS_FINAL`

Health와 Stability는 schema guard와 숫자 파싱만 확인하며 Happiness source count에 합산하지 않는다.

현재 검증된 positive source 수:

- Distress: 5
- Poverty: 4
- Illiteracy: 8
- Boredom: 10
- Religious Unrest: 2
- Local Happiness: 6

V3 `ADD` 건물인 Smokehouse와 Forge를 포함한 신규행에는 Happiness와 Needs 필드를 빈칸이 아니라 명시적 `0`으로 초기화한다. 이 규칙은 `build_final_building_master_v1.py`와 fixture test에 고정했다.

## 5. Health와 Stability 독립성

세 시스템은 서로 다른 의미를 가진다.

- `Happiness`: 시민의 Needs 충족, 종교불안, 도시 행복원, 외부 정치적 불행을 계산
- `Health`: 위생, 질병, 자원, 지형, Pollution으로 결정되는 도시 보건 상태
- `Stability`: 국가와 행정체계의 질서 유지 및 정치적 안정성

따라서:

- `HEALTH_POINTS_FINAL`을 Local Happiness로 직접 더하지 않는다.
- `STABILITY_POINTS_FINAL`을 Local Happiness로 직접 더하지 않는다.
- 부정적 Health가 주는 Happiness 효과만 `Health Unhappiness` 계층을 통해 연결한다.
- Stability 전체식은 별도 정량화한다.

## 6. Empire luxury Happiness 처리

제국 사치자원 Happiness를 각 도시 `LOCAL_HAPPINESS`에 조용히 분배하지 않는다.

사치자원과 제국 단위 Happiness가 City Happiness에 미치는 방식은 별도 empire aggregation 계층에서 명시적으로 처리한다. 현재 도시 계산기에는 숨은 luxury 분배가 없다.

이는 접촉 기반 동적 자원 시스템과도 일치한다. 자원을 발견하거나 교역했다고 해서 모든 도시의 Local Happiness 행에 자동 복제하지 않는다.

## 7. 정적 QA

`CITY_HAPPINESS_STATIC_QA_V1.md`는 `generate_city_happiness_static_qa_v1.py`가 재생성한다.

고정 시나리오 12개를 검증한다.

- 기본 균형 도시
- 낮은 산출 도시
- Needs reduction 적용
- Health 독립 페널티
- Religious Unrest
- Local Happiness 인구 상한
- 외부 페널티
- 상대 기대치 상향 clamp
- 상대 기대치 하향 clamp
- 인구 0 passthrough
- 부동소수점 threshold floor
- 네 외부 페널티 동시 적용 및 중복 적용 방지

CI는 generator를 실행한 뒤 checked-in Markdown과 `git diff --exit-code`로 비교하여 보고서가 계산기와 어긋나면 실패한다.

이 결과는 **pre-runtime 정적 balance QA**이며 실제 gameplay autoplay나 turn telemetry가 아니다.

## 8. Building master QA 및 CI

현재 Building master:

- rows: 104
- duplicate building: 없음
- roster/master 누락: 없음
- Tech/Civic gate 누락: 없음
- Health final blank: 없음
- Power load blank: 없음
- Stability final blank: 없음
- Happiness 필수 numeric field blank: 없음

`.github/workflows/build-final-building-master.yml`은 master 재생성 직후 Happiness-link validator까지 실행한다.

따라서 Building source를 수정해 master를 다시 만들 때 Happiness schema 누락이 생기면 같은 build workflow에서 차단된다.

`.github/workflows/city-happiness-qa.yml`은 다음을 순서대로 실행한다.

1. City Happiness calculator test
2. Building Happiness-link fixture test
3. 실제 104-row Building master Happiness validator
4. 12-scenario static QA generator
5. checked-in static QA report drift check

## 9. 현재 deferred 정치 입력

City Happiness 계산기는 다음 외부 입력을 받을 준비가 되어 있으나 해당 발생식 자체는 아직 후속 정량화 대상이다.

- War Weariness Unhappiness
- Occupation Unhappiness
- Colonial Unhappiness
- Policy Burden Unhappiness

이 중 다음 정량화 우선순위는 `War Weariness`다.

## 10. 다음 정량화 순서

1. War Weariness 정량식
2. 정부교체 Culture 비용, 과도기, Stability 충격
3. 점령지와 식민정부의 Stability 부담
4. `STABILITY_POINTS_FINAL`을 포함한 State Stability 전체식
5. Logistics
6. Grid Battery 저장용량 규칙

City Happiness V1은 위 후속 시스템이 완성되기 전에도 외부 페널티를 명시적으로 주입하여 독립 검증할 수 있다.

## 11. runtime 원칙

현재 저장소에는 완성된 게임 엔진이 없다.

따라서:

- fixture와 static QA를 실제 autoplay라고 부르지 않는다.
- `CITY_HAPPINESS_STATIC_QA_V1.md`는 사전 수치 검증이다.
- 실제 turn telemetry, AI 행동 검증, 장기 autoplay는 게임 엔진 구현 뒤 수행한다.

## 12. 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V8.md`
2. `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`
3. `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`
4. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
5. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
6. `city_system/STABILITY_BUILDING_SUPPORT_V1.md`
7. Power, Health, Happiness/Stability 세부 권위본
8. Building V4/V3/V2 입력 파일
9. Tech/Civic/Unit/Tile/Resource 각 세부 권위본
10. 이전 V7/V6/V5/V4/V3/V2/V1 인덱스 및 감사 파일

## 13. 현재 판정

City Happiness는 이제 구조 구상 단계가 아니라 **정량 V1 단계**다.

13시대 기대치, 네 기본 Needs, Religious Unrest, citizen cap, Health Unhappiness, Local Happiness cap, 외부 정치 페널티 인터페이스, 104개 Building 연결, 12개 정적 QA 시나리오가 하나의 재현 가능한 체계로 고정되었다.

Building, Health, Power, Happiness, Stability는 서로 독립 필드를 유지하며 필요한 지점에서만 명시적 bridge를 통해 연결한다.

다음 정치 정량화 시작점은 `War Weariness`다.
