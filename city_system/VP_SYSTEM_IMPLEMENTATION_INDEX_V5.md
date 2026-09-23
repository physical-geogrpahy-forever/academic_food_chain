# VP 시스템 구현 인덱스 V5

기준일: 2026-09-23
상태: HEALTH QUANTITATIVE V1 / PRE-AUTOPLAY STATIC QA COMPLETE / POWER-POLLUTION BRIDGE DEFERRED

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

Science/Culture 비용곡선의 정적 QA는 `STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.*`를 따른다.

Runtime 감시:

- Ancient -> Classical 비용 경계
- Industrial의 16 tech / 9 civic 밀도
- Atomic Science/Culture 상대 비용

정적 QA만으로 Science/Culture 공통 multiplier를 변경하지 않는다.

## 2. 유닛

권위 수치표:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`

89개 유닛의 역할, 전투수치, VP 상대 Production 비용 구조를 사용한다.

업그레이드 Gold:

- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
- `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP_QA.md`

VP식 Production 차이 기반 Gold 공식을 사용한다.

Runtime 감시 대상 최소비용 경로:

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

자원 발견은 `Animal Husbandry -> Horses 자동 발견` 방식이 아니라 기존 접촉 기반 동적 자원 시스템을 우선한다.

## 4. Building V3

구성:

- base roster: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv`
- roster override: `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
- base numeric: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`
- numeric override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
- Power override: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
- QA: `city_system/FINAL_GENERIC_BUILDING_V3_QA.md`

Smokehouse와 Forge는 실제 일반 건물로 추가된 상태를 유지한다.

Worker-built Academy/Manufactory 반복 건설 때문에 다음 nerf는 유지한다.

- Factory의 Manufactory Production bonus: project +1
- Research Lab의 Academy Science bonus: project +1

Autoplay가 시작되었다고 해서 자동으로 VP 원수치로 복구하지 않는다.

## 5. Power V1

권위본:

- `city_system/POWER_SOURCE_BALANCE_V1.csv`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/VP_TILE_IMPROVEMENT_POWER_OVERRIDE_V3.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`

주요 발전량:

- Solar Farm: 2 Power
- Wind Farm: 2 Power
- Offshore Wind Farm: 2 Power
- Geothermal Plant: 4 Power
- Hydroelectric: 6 Power
- Coal/Oil: 4 Power per reserved strategic-resource capacity
- Uranium: 16 Power per reserved strategic-resource capacity

Power와 일반 Production bonus를 동일 변수로 처리하지 않는다.

중요한 미완성 연결:

- Coal = HEAVY
- Oil = MODERATE
- Nuclear = MINUSCULE
- renewable = ZERO

까지는 확정되어 있으나, 이 emission class를 **numeric local Pollution points**로 변환하는 값은 아직 확정하지 않았다.

따라서 Health의 Pollution penalty 식은 존재하지만 발전소가 몇 Pollution point를 투입하는지는 아직 `DEFERRED_POWER_EMISSION_TO_LOCAL_POLLUTION_BRIDGE`이다.

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
- normal Standard-speed plague duration 6 turns, minimum 3 after medical reduction
- virulent plague chance 10%, duration x1.5
- High Medieval plague era multiplier 1.50 peak

`FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`의 `HEALTH_POINTS_PROVISIONAL` 값과 충돌할 경우 본 Health V1 파일들이 우선한다.

Power/industry의 Health 외부효과는 Pollution을 통해 연결한다. Factory나 Coal Power Plant에 별도 direct -Health를 중복 적용하지 않는다.

Harbor/Airport는 전파 네트워크를 통해 작용하고 direct -Health를 받지 않는다.

Cross-system runtime watch:

- Hospital +5 base Food와 Health +4의 간접 Food 전환
- Food Market +4 base Food + powered Food +2 + Health +1
- 국제무역의 소규모 Empire Health malus와 감염 시 x2 transmission
- worked Coal/Oil의 -1 Health와 향후 소비단계 Pollution의 결합
- Sewer/Hospital/Medical Lab 이후 후기 plague 억제가 지나치게 빠른지

## 7. Pre-autoplay static QA

권위본:

- `city_system/STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.csv`
- `city_system/STANDARD_SPEED_PRE_AUTOPLAY_CURVE_QA_V1.md`
- `city_system/validate_standard_speed_pre_autoplay_v1.py`

판정:

- STATIC PASS WITH RUNTIME WATCHES
- runtime autoplay가 실행되었다는 뜻은 아니다.
- Science/Culture/Production global common multiplier는 아직 변경하지 않는다.

## 8. 현재 권위 우선순위

충돌 시:

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V5.md`
2. `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
3. `health_system/HEALTH_POWER_CROSS_SYSTEM_QA_V1.md`
4. `health_system/HEALTH_BUILDING_VALUES_V1.csv`
5. `health_system/HEALTH_RESOURCE_FEATURE_VALUES_V1.csv`
6. `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
7. `health_system/HEALTH_PLAGUE_ERA_RISK_V1.csv`
8. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V4_POWER_OVERRIDE.csv`
9. `city_system/POWER_SOURCE_BALANCE_V1.csv`
10. `city_system/POWER_DEMAND_BUILDING_V1.csv`
11. `city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv`
12. `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V3_VP_OVERRIDE.csv`
13. `tech_reference/VP_TECH_BUILDING_ADDITIONS_V3.csv`
14. `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_V3.csv`
15. `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
16. `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
17. `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
18. `city_system/FINAL_UNIT_UPGRADE_COSTS_V2_VP.csv`
19. `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
20. `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
21. locked historical/dynamic-resource rules
22. earlier V4/V3/V2/V1 audit and master files

## 9. 다음 작업

다음 순서:

1. Power emission class -> numeric local Pollution bridge 확정
2. Health/Power/Upgrade까지 포함한 정적 cross-system validator 작성
3. runtime autoplay harness 또는 실제 게임 엔진 연결 경로 확정
4. Standard-speed autoplay
5. Ancient -> Classical, Industrial, Atomic, Health/plague, equal-cost upgrade 감시
6. 실제 turn data가 있을 때만 Science/Culture/Production global common multiplier 조정
7. 최종 완전 병합 master regeneration

## 10. 현재 판정

**Technology/Civic -> Unit -> Tile/Resource -> Building -> Power -> Health의 pre-autoplay 구조 및 Health 정량화는 완료.**

다만 **Power emission class -> numeric local Pollution** 연결은 runtime Health-Power 통합 전 필수 미완성 항목이다.

다음 단계는 이 Pollution bridge를 먼저 확정하는 것이다.