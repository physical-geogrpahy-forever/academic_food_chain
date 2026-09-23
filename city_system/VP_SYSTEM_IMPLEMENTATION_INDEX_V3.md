# VP 시스템 구현 인덱스 V3

기준일: 2026-09-23
상태: MASTER MERGE + UNIT V3 COMPLETE

상위 감사 기록:

- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V2.md`
- `city_system/VP_TECH_UNIT_TILE_RESOURCE_SECOND_PASS_QA_V2.md`

이 문서는 V2에서 남겨둔 master 병합과 unit numeric V3 생성 결과를 반영한 최신 권위 인덱스다.

## 1. 기술 master

새 권위본:

- `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
- commit `a010f414077f68e3878c722e9ae3e782138449c9`

V2는 기존 109개 기술 roster를 유지하면서 `VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`를 master에 실제 병합했다.

추가 정리:

- Animal Husbandry의 세계 Horses 자동 reveal 제거
- Calendar의 작물 직접 +1 Food 제거
- Mathematics Farm +1 Food 반영
- Irrigation의 옛 fresh-water Farm +1 메모 제거
- Horse Collar의 옛 Farm +1 Production 메모 제거
- Smart Materials의 옛 Mine +1 Production 메모 제거
- VP형 Farm/Mine/Quarry/Pasture/Plantation/Camp/Fishing Boats/Lumber Mill/Fort progression 반영
- Worker-built Academy/Manufactory/Landmark/Holy Site 관련 기술 progression 반영

충돌 시 V1보다 V2가 우선한다.

## 2. 사회제도 master

새 권위본:

- `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
- commit `2135958b25d41060576738a3c9cf2f372d062dba`

V3는 기존 72 civic roster를 유지하면서 다음을 병합했다.

- `civic_tree_locked_v2.csv`의 후기 시대 분류
- `VP_CIVIC_TILE_OVERRIDE_V2.csv`의 worker-improvement gate와 yield progression
- Future Era civic 분리 유지

주요 gate:

- Civil Service -> Farm/Pasture progression
- Guilds -> Village/Camp progression
- Theology -> Worker-built Holy Site
- Mercantilism + Economics -> Worker-built Customs House
- Natural History -> Worker-built Landmark
- Civil Engineering + Steam Power -> Canal
- Environmentalism과 관련 기술 -> renewable power improvements

충돌 시 V2 master보다 V3가 우선한다.

## 3. 유닛 수치 V3

새 구현 권위본:

- `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
- commit `52f3cc73be23ab08b8348a384dd3bb1ae165bd24`
- QA: `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP_QA.md`
- QA commit `e3681a2e8f10e0e7d87a3482aa1f48d995854891`

검증:

- 89 units
- CSV total 90 lines including header
- 4 role conflicts resolved and applied
- direct VP combat/stat mapping applied
- project-specific units retained where no clean VP counterpart exists
- unit Production-cost hierarchy converted to VP-relative curve

최종 role conflict:

- Cavalry -> MOUNTED_SKIRMISHER 40/31 Range 1 Moves 5
- Anti-Tank Gun -> ANTI_ARMOR Combat 50 Moves 2
- Helicopter -> MOUNTED_SKIRMISHER 70/70 Range 1 Moves 6
- Aircraft Carrier -> NAVAL_CARRIER Combat 70, no organic ranged attack, cargo 2

Production cost는 이제 개별 유닛 간 상대관계가 권위값이다.

남은 global numeric work는 autoplay 뒤 **전체 curve에 공통 multiplier를 적용할지 여부**이지, 개별 유닛을 옛 BNW cost로 되돌리는 것이 아니다.

## 4. 타일개선

권위본 유지:

- `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
- `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
- `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`

주요 progression:

- Farm: Mathematics / Civil Service / Fertilizer / Robotics
- Village: Guilds / Railroad
- Mine: Steel / Steam Power / Combustion / Robotics
- Quarry: Machinery / Steam Power / Dynamite
- Pasture: Civil Service / Fertilizer / Robotics
- Plantation: Chemistry / Economics / Plastics
- Camp: Guilds / Gunpowder / Rifling / Refrigeration
- Fishing Boats: Compass / Navigation / Refrigeration
- Lumber Mill: Metallurgy / Combustion
- Fort: Chemistry / Military Science / Electronics / Stealth Technology

GP-derived improvements remain Worker-built and nerfed:

- Academy
- Manufactory
- Landmark
- Holy Site
- Customs House

Citadel은 제외한다.

## 5. 자원

권위본 유지:

- `civ_map_stage10_resources/VP_RESOURCE_YIELD_ADOPTION_V1.csv`
- `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
- CONTACT_DYNAMIC_V2 biological-resource visibility system

핵심:

- 47개 프로젝트 자원 유지
- Stage10 실제 배치 우선
- Horses/Cattle/Sheep 및 작물의 동적 발견/접촉 체계 우선
- Niter monopoly: gunpowder and siege unit Production +10%

## 6. 자원-건물 공백

확정된 다음 roster 변경:

### Smokehouse

- generic building 추가
- provisional tech gate: Trapping
- Bison: Food +1
- Deer: Food +1

### Forge

- generic building 추가
- tech gate: Bronze Working
- Engineer slot 1
- Science +1
- Mine Production +1
- Iron: Production +1, Gold +1
- Copper: Gold +2

이 둘은 Building roster V3에서 실제 행으로 추가해야 한다.

## 7. 현재 권위 우선순위

충돌 시 다음 순서를 사용한다.

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V3.md`
2. `tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv`
3. `civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv`
4. `city_system/FINAL_UNIT_NUMERIC_BALANCE_V3_VP.csv`
5. `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
6. `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
7. 프로젝트 locked historical/dynamic-resource rules
8. V2 audit/override files
9. 이전 V1 master files

V2 audit는 근거 기록으로 보존하지만 구현 수치는 V3가 우선한다.

## 8. 다음 작업

이제 다음 순서로 진행한다.

1. Building roster V3
   - Smokehouse 실제 추가
   - Forge 실제 추가
   - 모드/GS/VP 출처를 다시 구분
2. Building numeric V3
   - `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv` 기반
   - Worker-built Academy/Manufactory 반복건설 문제 때문에 Research Lab -> Academy +4, Factory -> Manufactory +2 재검토
3. Power 개선시설 수치
4. unit upgrade Gold를 V3 Production cost에 맞춰 재계산
5. Standard-speed autoplay
6. Science/Culture/Production common multiplier 최종 결정

## 9. 현재 판정

**기술 master, civic master, unit combat/stat/cost V3까지 구조 통합 완료.**

이제 가장 큰 미완성 영역은 Building roster/numeric V3이다.
