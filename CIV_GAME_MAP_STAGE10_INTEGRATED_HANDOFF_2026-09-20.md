# CIV GAME MAP STAGE 10 통합 인계본

Date: 2026-09-20  
Repository: `physical-geogrpahy-forever/academic_food_chain`  
Branch: `civ-game-map-stage1b-etopo2022`

## 1. 이 문서의 역할

이 문서는 2026-09-20 현재 Stage 10 자원 작업의 통합 인계본이다.

중요한 수정:
- 이전 인계 문서에서는 `resource_fix_v1`의 대형 12,500행 통합 CSV를 로컬 작업 산출물로만 두고 GitHub에는 compact patch를 주 인계 수단으로 두었다.
- 사용자 지시에 따라 이 정책을 폐기한다.
- 이제 GitHub에 **전체 12,500행 fixed placement CSV 통합본을 직접 저장**한다.
- compact patch와 reconstruction 파일은 보조 재현 자료로만 유지한다.

## 2. 현재 지도 기준

- CRS: EPSG:8857
- Parent grid: 335 x 781 = 261,635 hexes
- LAND: 68,048
- LAKE: 882
- COAST: 8,781
- OCEAN: 156,201
- VOID: 27,723
- Stage1A 1-degree 자료는 최종 산출물에 사용하지 않는다.
- Stage2B terrain/biome은 현재 지형 및 바이옴 기준이다.

## 3. 자원 목록

총 47종.

### Strategic 7
HORSES, IRON, NITER, COAL, OIL, ALUMINUM, URANIUM

### Bonus 10
BANANAS, BISON, CATTLE, DEER, FISH, SHEEP, STONE, WHEAT, MAIZE, RICE

### Luxury 30
CITRUS, COCOA, COPPER, COTTON, CRAB, DYES, FURS, GEMS, GOLD, INCENSE, IVORY, MARBLE, PEARLS, SALT, SILK, SILVER, SPICES, SUGAR, TRUFFLES, WHALES, WINE, COFFEE, TEA, TOBACCO, OLIVES, PERFUME, AMBER, JADE, LAPIS_LAZULI, CORAL

표시상 COCOA는 초콜릿 아이콘을 사용하고 PERFUME은 향수로 표시한다. 내부 데이터 ID는 기존 ID를 유지한다.

## 4. Stage10Y 기본 배치

기존 Stage10Y V2 기준:
- total 12,500
- strategic 2,500
- bonus 5,000
- luxury 5,000
- one resource per hex PASS
- LAND 10,896
- COAST 639
- OCEAN 965
- LAKE 0
- VOID 0

지역별 밀도 차이는 그 자체로 보정 대상이 아니다. 실제 지리적 집중은 유지한다. 단, 소스 오류, 처리 오류, 강도 plateau, surface 위반은 수정한다.

## 5. source-GPKG 감사

기존 이미지 좌표 변환 방식의 world/regional TIF는 자원 위치 검토에 신뢰할 수 없는 것으로 판정했다.

따라서 감사는 Stage10Y source GPKG geometry 자체에서 수행했다.

검증 결과:
- selected cells 12,500
- unique selected cell IDs 12,500
- duplicate 0
- LAND 10,896
- COAST 639
- OCEAN 965
- LAKE/VOID 0
- 기본 surface rule PASS
- 선택된 zero 또는 negative evidence 없음

한반도 LAND 감사 창:
- 124-131E
- 33-39.8N
- resource-bearing LAND cells 28
- RICE 7
- HORSES 6
- TOBACCO 4
- WINE 4
- CITRUS 2
- COAL 1
- IRON 1
- CATTLE 1
- JADE 1
- MAIZE 1

따라서 이전 TIF에서 한반도 육지 자원이 거의 안 보인 것은 source placement가 빈 것이 아니라 rendering alignment 실패였다.

## 6. biological plateau 감사와 resource_fix_v1

문제가 확인된 자원:
- BISON: top-tie 10,738 / selected 390
- IVORY: 15,552 / 248
- WHALES: 3,695 / 350

기존 이상:
- BISON desert biome 21
- IVORY desert biome 44
- IVORY temperate biome 8
- WHALES south/north 336/14

resource_fix_v1 review build:
- BISON desert biome 21 -> 0
- IVORY desert biome 44 -> 0
- IVORY temperate biome 8 -> 0
- WHALES south/north 336/14 -> 176/174
- WHALES tropical/subtropical 11 -> 35

review quota pools:
- BISON: North America 176, Europe 70, Central/South Asia 100, East Asia 44
- IVORY: Africa 198, South+Southeast Asia 50
- WHALES: North temperate/subpolar 123, South temperate/subpolar 158, North tropical/subtropical 17, South tropical/subtropical 18, high-latitude fringe 34

이 세 자원의 수정 배치는 아직 review build이며 canonical final로 승격하지 않는다.

## 7. GitHub의 통합본

### 전체 12,500행 fixed placement

`civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv`

이 파일은 더 이상 로컬 전용 산출물이 아니다. GitHub branch에 직접 저장된 현재 통합 배치표다.

업로드 commit:
- `1a822065b259f5f169ad40ba487aa7c3b805f7e4`

### 세 자원 전체 replacement selection

`civ_map_stage10_resources/resource_fix_v1/replacement_selections_v1.csv`

업로드 commit:
- `68f476b89697142c5262611dafd19378415c77c3`

### 보조 재현 자료

`civ_map_stage10_resources/resource_fix_v1/`
- README.md
- RECONSTRUCT_FIXED_PLACEMENT.md
- replacement_ids_v1.json
- plateau_comparison_v1.csv
- replacement_comparison_summary_v1.csv
- replacement_pool_counts_v1.csv
- replacement_region_comparison_v1.csv

compact patch는 통합 CSV의 대체물이 아니라 검산 및 재현 보조 자료다.

## 8. 감사 자료

`civ_map_stage10_resources/audit_2026-09-20/`

핵심 파일:
- RESOURCE_AUDIT_SUMMARY.md
- RESOURCE_FIX_PLAN_V1.md
- heuristic_fix_smoke_test_v1.csv
- korea_land_resource_audit.csv
- problem_resource_summary_v1.csv
- resource_audit_status.csv
- resource_fix_plan_v1.csv
- resource_tie_plateau_audit.csv
- world_land_resource_density_by_region.csv
- world_resource_surface_summary.csv
- world_resource_technical_audit.csv
- world_resource_technical_checks.json

## 9. Resource icon V4

`civ_map_stage10_resources/icons_v4/`

현재 V4에는 47개 자원 전체가 포함된다.

주요 수정:
- HORSES side profile
- BISON face
- URANIUM trefoil
- visible MAIZE kernels
- recognizable TEA leaves
- PERFUME bottle and display name 향수
- COCOA display as chocolate
- CRAB leg correction
- FURS internal pattern
- GOLD and SILVER bar form
- MARBLE bust/statue direction
- SILK fabric form
- SPICES, SUGAR, TRUFFLES redesign
- WHALES profile redesign

기본 배지:
- strategic: hexagon
- bonus: circle
- luxury: rounded diamond

## 10. 접촉 기반 동적 자원 시스템

상세 설계:
`civ_map_stage10_resources/contact_dynamic_resource_system_v1.md`

47개 분류표:
`civ_map_stage10_resources/resource_transfer_classes_v1.csv`

핵심 원칙:
- 역사적 전래 연도는 실제 역사 기본 시나리오를 재현하기 위한 prior다.
- 게임의 alternate history에서 전래를 일으키는 것은 연도 자체가 아니라 **접촉 사건**이다.

구분 상태:
1. native/source potential
2. civilization knowledge
3. introduced presence
4. exploitable/active state

전래를 일으킬 수 있는 사건:
- civilization contact
- trade
- exploration/discovery
- settlement/colonization
- conquest/occupation

예시:
- 한국 문명이 1000년에 남미에 도달하고 정착한다면, 한국이 이미 보유하고 운송 가능한 말, 소 등의 자원은 환경적으로 적합한 남미 셀에 도입될 수 있다.
- 시스템은 실제 역사상의 1492년을 기다리지 않는다.

지질자원은 고정:
- 접촉은 광상의 위치를 옮기지 않는다.
- 접촉은 지식, 발견, 채굴 기술, 이용 가능성을 바꾼다.

## 11. 앞으로 47개 자원별로 필요한 역사 자료

각 자원별로 다음 필드를 구축한다.

- native/source geography
- domestication 또는 original exploitation zone
- environmental suitability
- historical/default transfer pathways
- civilization knowledge requirements
- transportability
- establishment requirements
- trade transfer possibility
- settlement transfer possibility
- conquest transfer possibility
- exploration/discovery behavior
- exploitation technology
- historical timeline validation points

예를 들어:
- pre-Columbian America의 HORSES/CATTLE/SHEEP는 역사 기본 시나리오에서 비활성
- MAIZE/TOBACCO/COCOA는 아메리카 기원
- COTTON은 구세계와 신세계의 독립적인 재배 계통을 구분해야 함
- 한국 COTTON은 고려 후기 전래를 역사 기본 경로의 validation point로 사용할 수 있으나, alternate-history 게임에서는 실제 접촉 네트워크에 따라 더 이르거나 늦을 수 있음

## 12. 현재 canonical 상태

현재 기준:
- Stage10Y V2 original = preview
- resource_fix_v1 full integrated placement = review build
- canonical final placement = 아직 아님

canonical 승격 전 필요한 작업:
1. 47개 자원 contact/native/transfer evidence 조사
2. BISON/IVORY/WHALES fixed review 재감사
3. one-resource-per-hex 재검사
4. surface rule 재검사
5. plateau 재검사
6. default historical timeline 검증
7. source GPKG geometry 기반 직접 렌더링 재구축
8. 지역별 시각 QA

## 13. 다음 채팅에서 우선할 일

첫 번째 우선순위는 **47개 자원별 접촉 기반 역사 전래 데이터셋 작성**이다.

단순한 "몇 년에 해금" 표를 만들지 않는다.

최소 구현 규칙:
`known by source civilization + transferable class + valid contact/trade/settlement/conquest/expedition event + suitable destination -> introduction queue -> local activation/spread`

이 문서와 GitHub의 전체 fixed placement CSV를 다음 채팅의 기준점으로 사용한다.
