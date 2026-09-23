# VP 시스템 구현 인덱스 V5

기준일: 2026-09-23
상태: HEALTH QUANTITATIVE V1 / POWER-POLLUTION BRIDGE V1 / CROSS-SYSTEM STATIC QA READY

상위 기록:

- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V4.md`
- `city_system/STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.md`
- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

## 1. 기술 및 사회제도

권위본:

- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
- `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`

Building V3 추가 gate:

- Trapping -> Smokehouse
- Bronze Working -> Forge

Science/Culture 비용곡선 정적 QA는 `STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.*`를 따른다.

Runtime 감시:

- Ancient -> Classical 비용 경계
- Industrial 16 tech / 9 civic 밀도
- Atomic Science/Culture 상대 비용

정적 QA만으로 Science/Culture 공통 multiplier를 변경하지 않는다.

## 2. 유닛

권위 수치표:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`

업그레이드 Gold:

- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP_QA.md`

VP Production 차이 기반 Gold 공식을 사용한다.

Runtime 감시 최소비용 경로:

- Trebuchet -> Bombard: 10 Gold
- Rifleman -> Infantry: 10 Gold
- Landship -> Tank: 10 Gold

## 3. 타일개선 및 자원

권위본:

- `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
- `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
- `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`
- `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
- CONTACT_DYNAMIC_V2 biological-resource visibility rules

Worker-built former GPTI:

- Academy
- Manufactory
- Landmark
- Holy Site
- Customs House

Citadel은 제외한다.

자원 발견은 단순 기술 자동 발견보다 기존 접촉 기반 동적 자원 시스템을 우선한다.

## 4. Building V3/V4

구성:

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- numeric override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
- Power override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
- QA: `city_system/FINAL_GENERIC_BUILDING_V3_QA.md`

Smokehouse와 Forge는 일반 건물로 유지한다.

Worker-built Academy/Manufactory 반복 건설 때문에 다음 project nerf를 유지한다.

- Factory Manufactory Production bonus: +1
- Research Lab Academy Science bonus: +1

## 5. Power V1

권위본:

- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/VP_TILE_IMPROVEMENT_POWER_OVERRIDE_V3.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
- `city_system/POWER_POLLUTION_BRIDGE_V1.csv`

주요 발전량:

- Solar Farm: 2 Power
- Wind Farm: 2 Power
- Offshore Wind Farm: 2 Power
- Geothermal Plant: 4 Power
- Hydroelectric Dam: 6 Power
- Coal/Oil: 4 Power per reserved strategic-resource capacity
- Uranium: 16 Power per reserved strategic-resource capacity

Power와 일반 Production bonus를 동일 변수로 처리하지 않는다.

### Power -> Pollution -> Health bridge

Gathering Storm 계수를 글로벌 배출 측에 유지한다.

- Coal: 820 per generated Power
- Oil: 490 per generated Power
- Nuclear: 48 per generated Power
- renewables: 0

프로젝트 로컬 Pollution:

`local_pollution = round(actual_power_generated * GS_CO2_per_power / 300)`

Health penalty:

`-floor(local_pollution / 10)`, minimum -5

4 Power 예시:

- Coal: Pollution 11 -> Health -1
- Oil: Pollution 7 -> Health 0
- Nuclear: Pollution 1 -> Health 0

글로벌 CO2와 로컬 Pollution은 별도 변수다.

## 6. Health and Plague V1

정성 설계:

- `health_system/HEALTH_AND_PLAGUE_QUALITATIVE_INTEGRATION_V1.md`

정량 권위본:

- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

핵심식:

`City Health = water + buildings + worked resources + worked features + empire health - population - pollution penalty + active plague penalty`

확정 핵심:

- Population: -1 Health per citizen
- natural fresh water or Aqueduct: water Health floor +2, non-stacking
- Health-to-Food conversion cap: -5 to +5
- Granary +1
- Apothecary +2, plague duration -1
- Cold Storage +2
- Food Market +1
- Hospital +4, plague duration -1
- Sewer +4, spontaneous plague risk x0.75
- Medical Lab +5, plague duration -2
- Recycling Center +2
- Standard-speed plague duration 6 turns, minimum 3
- virulent plague chance 10%, duration x1.5
- High Medieval plague era multiplier 1.50 peak

Building V2의 `HEALTH_POINTS_PROVISIONAL`과 충돌하면 Health V1이 우선한다.

Factory나 fossil power building에 별도 direct -Health를 중복 적용하지 않는다. Harbor/Airport도 direct -Health가 아니라 전파 네트워크로 작동한다.

Runtime watch:

- Hospital +5 Food + Health +4
- Food Market +4 Food + powered +2 Food + Health +1
- 국제무역 Empire Health malus + 감염 시 x2 transmission
- worked Coal/Oil -1 Health + 소비단계 Pollution
- Sewer/Hospital/Medical Lab 이후 후기 plague 억제 강도

## 7. Pre-autoplay static QA

비용곡선:

- `city_system/STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.csv`
- `city_system/STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.md`
- `city_system/validate_standard_speed_pre_autoplay_v1.py`

Cross-system:

- `city_system/validate_cross_system_v1.py`
- `city_system/test_validate_cross_system_v1.py`
- `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`

Cross-system validator 범위:

- Power/resource capacity와 emission ordering
- renewable zero-emission consistency
- Health building 수치
- industry/transport direct Health 중복 방지
- plague 핵심 수치
- 55 upgrade edges
- 세 개 equal-cost 10 Gold watch edges

validator 로직은 matching fixture에서 `CROSS_SYSTEM_STATIC_QA: PASS`를 확인했다. GitHub 원본 행도 재검토하여 asserted anchor와 일치함을 확인했다.

이는 게임 엔진 autoplay가 실행되었다는 뜻이 아니다.

## 8. 현재 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V5.md`
2. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
3. `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`
4. `city_system/POWER_POLLUTION_BRIDGE_V1.csv`
5. `health_system/HEALTH_BUILDING_VALUES_V1.csv`
6. `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
7. `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
8. `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`
9. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
10. `city_system/POWER_SOURCE_BALANCE_V1.csv`
11. `city_system/POWER_DEMAND_BUILDING_V1.csv`
12. `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
13. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
14. `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`
15. `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_V3.csv`
16. `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
17. `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
18. `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
19. `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
20. `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
21. `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
22. locked historical/dynamic-resource rules
23. earlier V4/V3/V2/V1 audit and master files

## 9. 다음 작업

Power-Pollution-Health 숫자 연결까지 pre-autoplay 구조는 닫혔다.

다음 순서:

1. 실제 runtime autoplay harness 또는 게임 엔진 연결 경로 확정
2. Standard-speed autoplay
3. Ancient -> Classical, Industrial, Atomic pacing 감시
4. Health/plague outbreak와 후기 억제 감시
5. three equal-cost 10 Gold upgrade edges 감시
6. 실제 turn data가 있을 때만 Science/Culture/Production global multiplier 조정
7. 최종 완전 병합 master regeneration

## 10. 현재 판정

**Technology/Civic -> Unit -> Tile/Resource -> Building -> Power -> Pollution -> Health의 pre-autoplay 구조 통합 완료.**

남은 핵심은 실제 runtime autoplay이며, 아직 실행되었다고 간주하지 않는다.