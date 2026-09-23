# VP 시스템 구현 인덱스 V2

기준일: 2026-09-23
상태: SECOND-PASS INTEGRATION

상위 기준:
- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V1.md`

이 문서는 V1 이후 진행된 기술/사회제도, 유닛, 타일개선, 자원 교차감사의 최신 상태를 기록한다.

## 1. 기술 및 사회제도

완료:

- 109개 기술 roster 유지
- 72개 civic roster 유지
- `tech_reference/VP_SCIENCE_COST_CURVE_ADAPTATION_V1.csv`
- `civics_reference/VP_CULTURE_COST_CURVE_ADAPTATION_V1.csv`
- `civics_reference/civic_tree_locked_v2.csv`
- `tech_reference/VP_TECH_CIVIC_SYSTEM_REAUDIT_V1.md`

후기 시대 분류는 V2 tree가 권위본이다.

- Environmentalism: Information
- Information Warfare: Future
- Global Warming Mitigation: Future
- Cultural Hegemony: Future
- Smart Power Doctrine: Future
- Exodus Imperative: Future
- Future Civic: Future

비용곡선은 아직 provisional이며 전체 autoplay 뒤 최종 보정한다.

## 2. 기술-타일-자원 override

새 권위 델타:

- `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
  - commit `76eca36591b623f91ab84f43b8ddd478f2cf2d8b`
- `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`
  - commit `f2122d5154fe54c2ba84201ffe102cbb6fb21779`

핵심 수정:

- Animal Husbandry는 Horses를 자동 reveal하지 않는다. 동적 자원 CONTACT 시스템이 visibility를 지배한다.
- Calendar의 기존 Wheat/Rice/Maize 직접 +1 Food 메모 제거.
- Farm 업그레이드는 Mathematics, Civil Service, Fertilizer, Robotics로 통일.
- Mine 업그레이드는 Steel, Steam Power, Combustion, Robotics로 통일.
- Quarry 업그레이드는 Machinery, Steam Power, Dynamite로 통일.
- Pasture 업그레이드는 Civil Service, Fertilizer, Robotics로 통일.
- Fishing Boats 업그레이드는 Compass, Navigation, Refrigeration으로 통일.
- Lumber Mill 업그레이드는 Metallurgy, Combustion으로 통일.
- Camp 업그레이드는 Guilds, Gunpowder, Rifling, Refrigeration으로 통일.

## 3. 유닛

1차 감사:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V2_VP_AUDIT.csv`
- 89개 감사
- VP 직접대응 56
- VP analogue 9
- role conflict 4
- project-specific 20

2차 role conflict 해결:

- `city_system/VP_UNIT_ROLE_CONFLICT_RESOLUTION_V2.csv`
  - commit `83879691a8bd07cbb56868f419f3a87a5d6cd78b`
- `city_system/VP_UNIT_ROLE_CONFLICT_RESOLUTION_V2.md`
  - commit `158da43ce243224391b445596363cf686020cf28`

최종 role 결정:

### Cavalry
- `LIGHT_CAVALRY` -> `MOUNTED_SKIRMISHER`
- provisional 40/31, Range 1, Moves 5
- VP role 채택

### Anti-Tank Gun
- `ANTI_ARMOR` 유지
- provisional Combat 50, Moves 2
- VP의 skirmisher 재분류는 거부

### Helicopter
- `LIGHT_CAVALRY` -> `MOUNTED_SKIRMISHER`
- provisional 70/70, Range 1, Moves 6
- VP gunship role 채택

### Aircraft Carrier
- `NAVAL_CARRIER` platform role 유지
- VP-era defensive Combat 70 채택
- 독립 ranged attack은 부여하지 않음
- base cargo 2 유지

Production cost와 upgrade Gold는 전체 unit-cost curve 보정 뒤 확정한다.

## 4. 타일개선

권위본:

- `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
  - commit `3f44a045a1c0d8d638bac3b4590fb0e4f6d263ba`

V2 핵심 수정:

### Customs House

V1 오류:
- Banking: Gold +2
- Architecture: Food +2

삭제 이유:
- 프로젝트 Customs House는 Economics + Mercantilism에서 해금되어 Banking보다 늦다.
- 프로젝트 109기술에는 Architecture가 없다.

V2 최종 업그레이드:
- Railroad: Food +2, Culture +1
- Refrigeration: Gold +2

GP 계열 Worker improvement 원칙은 유지:
- Academy
- Manufactory
- Landmark
- Holy Site
- Customs House

이들은 위인을 소비하지 않으므로 full VP GPTI 수치보다 낮게 유지한다.

Citadel은 계속 제외한다.

## 5. 자원

1차 감사:

- `civ_map_stage10_resources/VP_RESOURCE_YIELD_ADOPTION_V1.csv`
- 47개 자원 전부 VP yield/monopoly 대응

2차 override:

- `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
  - commit `5d71758ba088b674f64bdf8f371ae7f16ad9d1ff`

### Niter monopoly 확정

VP에는 Niter가 없으므로 프로젝트 독자 효과:

- **화약 및 공성 유닛 Production +10%**

선정 이유:
- Horses Attack +10%, Iron Defense +10%, Oil XP, Aluminum healing, Uranium Science/Attack과 역할이 겹치지 않는다.
- 안정적인 질산염/화약 공급망이라는 역사적 기능을 Production 보너스로 표현한다.

### Horses visibility 재확인

- CONTACT_DYNAMIC_V2가 권위 규칙
- Animal Husbandry는 Pasture/exploitation gate
- LATENT/ACTIVE_INTRODUCED Horses를 기술 하나로 전세계 reveal하지 않음

## 6. 자원-건물 공백 해결

- `tile_system/VP_RESOURCE_BUILDING_GAP_RESOLUTION_V2.md`
  - commit `e306646865f289dba3232e3754a962d756d22148`
- `tile_system/VP_RESOURCE_BUILDING_INTERACTIONS_OVERRIDE_V2.csv`
  - commit `2b56a6d23ced5bdade92897532b240812b4b0f0c`

### Smokehouse

다음 건물 roster에서 신규 일반건물로 추가한다.

- provisional gate: Trapping
- Bison: Food +1
- Deer: Food +1
- 정확한 비용/일반 효과는 building V3에서 확정

Cold Storage 또는 Granary에 억지로 흡수하지 않는다.

### Forge

다음 건물 roster에서 신규 일반건물로 추가한다.

- gate: Bronze Working
- Engineer slot 1
- Science +1
- Mine Production +1
- Iron: Production +1, Gold +1
- Copper: Gold +2

기존에 generic Forge가 거부된 이유는 Renaissance Metal Casting에 놓으면 너무 늦었기 때문이다. VP처럼 Bronze Working에 배치하면 이 문제가 사라진다.

Gunsmith, Steelworks, Stone Works에 임시 흡수하지 않는다.

## 7. 현재 권위 우선순위

충돌 시:

1. 이 V2 인덱스에 명시된 2차 결정
2. `VP_*_V2` override/adoption 파일
3. 프로젝트의 locked historical/dynamic-resource rules
4. VP master 데이터
5. 이전 V1 master/unlock note

즉 기존 `MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv` 안의 타일 yield 메모가 V2 override와 충돌하면 V2 override가 우선한다.

## 8. 다음 작업

이 세 영역에서 남은 것은 구조가 아니라 최종 수치 통합이다.

1. `FINAL_GENERIC_UNIT_NUMERIC_BALANCE_V3` 생성
   - V2 role resolution 적용
   - VP unit cost sweep을 13시대 기술비용에 맞춰 재스케일
   - upgrade Gold, resource requirement, supply 검증
2. `MASTER_TECHNOLOGY_UNLOCKS_109_V2` 생성
   - tile/resource override를 old master에 병합
3. `MASTER_CIVIC_UNLOCKS_72_V3` 생성
   - civic tile override와 Future-era labels 병합
4. Building roster V3
   - Smokehouse, Forge 실제 추가
   - Research Lab -> Academy +4, Factory -> Manufactory +2 보너스는 Worker-built GPTI 때문에 재검토
5. Power 개선시설 수치 확정
6. Standard-speed autoplay 후 Science/Culture/Production 최종 보정

## 9. 상태

**기술 및 사회제도 -> 유닛 -> 타일개선/자원의 VP 2차 구조 통합 완료.**

현재 남은 핵심은 master 파일 병합과 전체 비용곡선 수치 보정이다.
