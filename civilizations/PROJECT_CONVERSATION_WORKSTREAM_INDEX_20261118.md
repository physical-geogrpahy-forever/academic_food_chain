# 문명 1~5 및 후속 대화 — 작업별 결정사항·GitHub 권위 파일 색인

작성: 2026-11-18  
범위: 현재 검색·열람 가능한 **문명 프로젝트의 관련 과거 대화 요약**과 연결 GitHub 원본. **전체 이전 채팅 메시지 본문을 전수 다운로드했다는 뜻이 아님.**  
원칙: 사용자 요구/교정, 게임 설계 확정, 후속 GitHub 파일 상태, 미확정 사항을 구분한다.

| 작업 대화·시기 | 사용자 핵심 요구·교정 | 현재 권위 파일 또는 상태 | 주의 |
|---|---|---|---|
| 9월 17일 문명 기획·한국사 및 일본 논의 | 고대~정보화 12시대, 르네상스 **14~15세기** 교정, 한국 국가 후보 시대표, 일본 야마타이·야마토 등 국가 단위·계승 추측 금지 | [한·중·일 회수본](EAST_ASIA_12ERA_RECOVERY_V1.md), [대화 증거 장부](CONVERSATION_DECISIONS_PROVENANCE_20261118.md) | 한국 사용자 원본 전체 칸 미복원. AI 표를 원안으로 위장 금지 |
| 문명 1·문명 2, 9월 19일 지도 제작 | 지도는 **게임**이며 실제 지형/바이옴 완성본을 먼저 확인해야 함; 자원 선택 합의 전 자원 배치로 넘어간 것을 사용자 지적 | [Stage10 통합 인계](../CIV_GAME_MAP_STAGE10_INTEGRATED_HANDOFF_2026-09-20.md), [프로젝트 마스터 인계](../CIV_GAME_PROJECT_MASTER_HANDOFF_2026-09-20.md), `civ_map_stage1b`~`civ_map_stage9_review` | 지도 최종 미리보기·원천 대형 래스터가 항상 repo에 있는 것은 아님 |
| 문명 3, 자원 선정·접촉 기반 시스템 | 아메리카 말·소, 아시아 담배·옥수수 등 지리적 원산과 실제 **접촉/탐험/정착/무역**을 통해 자원 등장, 1492년 자동 전환 금지, 간단한 이식 가능 구조 | [동적 자원 V2](../civ_map_stage10_resources/contact_dynamic_resource_system_v2.md), [resource_fix_v1 README](../civ_map_stage10_resources/resource_fix_v1/README.md), [placement CSV](../civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv) | 확정된 47종 자원과 18종 접촉형 동적 자원. `resource_fix_v1`은 REVIEW BUILD이지 최종 맵 승인 아님 |
| 문명 4, 기술·사회제도/기업 | **기술과 사회제도 확정 후 건물 전에 기업 결정**, 기업 창업가 사전 로스터 연구, 기능성 제품은 생산력·서비스는 문화/관광 등, 위대한 **상인과 기술자** 모두 창업 가능 | [기술 109종](../tech_reference/technology_roster_locked_v2.csv), [사회제도 72종](../civics_reference/civic_roster_locked_v1.csv), [기업 창립 시스템](../corporations/CORPORATION_FOUNDING_AND_OUTPUT_SYSTEM_V1.md), [기업 정량 공급](../corporations/CORPORATION_QUANTITATIVE_SUPPLY_BRANCH_MODEL_V1.md) | 업종 독점 아님, 제품/서비스의 Supply Unit 기반 공급 모형을 유지 |
| 문명 5, 건물·위인 | Health와 Power 구분, Civ V BNW만 무조건 복제 금지; **More Luxuries·Health & Plague·Enlightenment Era·VP·Civ VI/GS** 채택 원문 우선; 전문가 GPP+문명6식 실존인물 영입, 선지자는 신앙 구매·장군/제독은 전투 포인트 | [소스별 우선순위](../city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md), [건물 수치 V5](../city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv), [건물 QA](../city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5_QA.md), [위인 V2](../city_system/FINAL_GREAT_PERSON_RECRUITMENT_SYSTEM_V2.md) | 수치/효과는 **효과별 출처 우선순위**. 104개 건물 마스터 QA 통과, 선지자·장군 생성 방식 보존 |
| 9월 22~25일 위대한 철학자·과학자·혁명가 | 위대한 철학자는 별도 직군, 혁명가와 지도자의 인물 중복은 배제 아닌 **혁명가→지도자** 전환 검토, 문명/지도자부터 확정 | [철학자 현 상태](../city_system/great_philosophers/WORK_STATE.md), [과학자 현 상태](../city_system/great_scientists/WORK_STATE.md), [혁명가 현 상태](../city_system/great_revolutionaries/WORK_STATE.md) | 과학자 319·철학자 220은 후속 정정 기준. 혁명가 역사 로스터는 **일시 중단** |
| 9월 25~27일 문명 국가 계보 | 중국 시대별 검토안, 일본 국가 단위, 미주에서 주요 국가/문명만 계보로·식민정부·독립/후계 국가를 표현 | [기존 10월 16일 인계문](../docs/handoffs/CHATGPT_WORK_HANDOFF_CIVILIZATIONS_REVOLUTIONARIES_20261016_KO.md), [한·중·일 회수본](EAST_ASIA_12ERA_RECOVERY_V1.md) | 10월 인계는 **2차 요약**. 사용자 현재 지시로 북미·중앙아메리카·카리브는 보류 |
| 11월 18일 저장소 분리 요청 | 기존 `academic_food_chain`에서 문명 프로젝트를 독립 repo로 분리 | 원격 `physical-geogrpahy-forever/civilization-game`은 2026-11-18 조회에서 **존재 확인 불가(404)** | 새 repo 생성이 완료되었다고 주장하지 말 것. 이 파일은 **현재 쓸 수 있는 기존 문명 브랜치**에 실저장됨 |
| 11월 18일 문명 회수·정리 | 한·중·일부터, 지도자 제외하고 **문명만**, 원안 임의 재구성 금지, 대화 검증 후 GitHub 실저장 | `civilizations/` 신규 데이터·증거 장부 | 국가 후보와 시대별 확인 칸, AI 검토안과 사용자 잠금 구분 |

## 현재 사용해야 하는 정보의 위계

1. 사용자가 기존 대화에서 직접 확정하거나 수정한 사항 (증거가 회수된 범위에서)
2. GitHub 파일에 실제 `AUTHORITATIVE` / `LOCKED` 선언된 구체적 설계
3. 검토안·후보 목록·이전 어시스턴트의 제안 (`DRAFT` / `NOT_LOCKED`)
4. 복원 불가 내용은 `UNRECOVERED`로 유지. 새 역사 서술로 사용자 원본을 대체하지 않는다.

기존 [PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md](../city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md)에 따른 게임 콘텐츠 효과의 소스 우선순위와는 **적용 범위가 다름**. 이 문서는 대화·계보 **출처 신뢰도**를 관리한다.

## 작업 상태와 남은 결손

- 한국·중국·일본 **완성된 플레이 가능 Civilization 최종 roster는 없음**.
- 한·중·일 12시대 회수표는 저장됨. 한국 원본의 정확한 12개 셀은 아직 미복원.
- 중국의 복수 왕조·정복 왕조 처리, 일본의 막부·왕권 분리 여부는 미확정.
- 지도자 개인별 선택 및 Great Revolutionary V3의 역사인물 roster는 문명 결정 뒤에 진행.
- 이 파일의 기록은 **검색 가능한 이전 대화 조각을 사용한 작업 색인**으로, '이전 모든 채팅 원문 전체 열람 완료'라는 표현은 허용하지 않음.
