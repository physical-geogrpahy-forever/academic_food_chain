# VP 시스템 구현 인덱스 V4

기준일: 2026-09-23
상태: BUILDING V3 PASS COMPLETE

상위 기록:

- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V3.md`
- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP_QA.md`
- `city_system/FINAL_GENERIC_BUILDING_V3_QA.md`

## 1. 기술 및 사회제도

권위본:

- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`

Building V3에서 신규 추가된 기술-건물 gate는 다음 V3 delta가 추가 우선권을 가진다.

- `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`
  - Trapping -> Smokehouse
  - Bronze Working -> Forge

## 2. 유닛

권위 구현표:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`

89개 유닛의 역할/전투수치/VP 상대 생산비 구조가 확정되어 있다.

전체 Production multiplier는 autoplay 뒤 공통 조정할 수 있으나 개별 유닛을 옛 BNW 비용으로 되돌리지 않는다.

## 3. 타일개선

권위본:

- `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
- `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
- `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`

Worker-built former GPTI:

- Academy
- Manufactory
- Landmark
- Holy Site
- Customs House

Citadel은 제외한다.

## 4. 자원

권위본:

- `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
- CONTACT_DYNAMIC_V2 biological-resource visibility rules

신규 자원-건물 직접 연결 권위본:

- `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_V3.csv`

확정:

- Bison -> Smokehouse Food +1
- Deer -> Smokehouse Food +1
- Iron -> Forge Production +1, Gold +1
- Copper -> Forge Gold +2

이제 `PENDING_SMOKEHOUSE_EQUIVALENT`와 `PENDING_FORGE_EQUIVALENT`는 구현용 값이 아니라 과거 감사 흔적이다.

## 5. Building V3

구현 구성:

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- numeric override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
- QA: `city_system/FINAL_GENERIC_BUILDING_V3_QA.md`

### Smokehouse

- Ancient
- Trapping
- FOOD_HEALTH
- Production 75
- Maintenance 1
- Camp Production +1
- border growth Food +10
- Bison Food +1
- Deer Food +1

### Forge

- Ancient
- Bronze Working
- INDUSTRY_POWER
- Production 75
- Maintenance 1
- Science +1
- Engineer slot 1
- Mine Production +1
- Iron Production +1, Gold +1
- Copper Gold +2

### Worker-built GPTI building interaction nerfs

Factory:

- VP Manufactory +2 Production -> project +1 Production

Research Lab:

- VP Academy +4 Science -> project +1 Science

이 두 감소는 일반 Worker가 Academy/Manufactory를 반복 건설할 수 있기 때문에 적용하며, autoplay에서 자동으로 원복하지 않는다.

## 6. 현재 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V4.md`
2. `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
3. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
4. `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`
5. `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_V3.csv`
6. `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
7. `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
8. `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
9. `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
10. `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
11. locked historical/dynamic-resource rules
12. earlier V2/V1 audit and master files

## 7. 다음 작업

구조적 공백은 대부분 닫혔다. 남은 작업은 다음 순서다.

1. Power 개선시설 수치 확정
   - Solar Farm
   - Geothermal Plant
   - Wind Farm
   - Offshore Wind Farm
   - city power buildings와 공급량 단위를 일치시킬 것
2. unit upgrade Gold를 V3 Production cost에 맞춰 재계산
3. Health 수치 최종 pass
4. Standard-speed autoplay
5. Science/Culture/Production global common multiplier 최종 보정
6. 완전 병합 master regeneration

## 8. 현재 판정

**Technology/Civic -> Unit -> Tile/Resource -> Building의 VP 구조 통합은 Building V3까지 완료.**

다음 핵심은 Power 수치와 upgrade Gold이며, 이후 autoplay가 전체 숫자곡선의 최종 검증 단계다.
