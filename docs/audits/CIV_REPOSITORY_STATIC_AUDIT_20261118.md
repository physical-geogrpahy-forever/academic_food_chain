# 문명 프로젝트 GitHub 전수 정적 감사 — 2026-11-18

**판정: 최종 정적 감사 PASS / 게임 엔진·대형 지도 재계산 미검증 / 한국 사용자 원본 문명표 미복원**

## 1. 실제 실행 근거

| 항목 | GitHub Actions 실행 |
|---|---|
| 1차 검사 (오류 검출) | [Run 44250090964](https://github.com/physical-geogrpahy-forever/academic_food_chain/actions/runs/44250090964): **FAIL**, 파일 형식 오류 8개 파일, 오류 행 총 29개 |
| 2차 검사 (형식 수정 후) | [Run 44250696080](https://github.com/physical-geogrpahy-forever/academic_food_chain/actions/runs/44250696080): **PASS**, errors=0, warnings=3, validators=23 |
| 2차 대상 HEAD | `f0a0f4476842f9571b7e0c7d7ef250bd82dd221f` |
| 감사 코드 | [tools/audit_civ_repository_v1.py](../../tools/audit_civ_repository_v1.py) |
| 자동 실행 설정 | [.github/workflows/civ-full-repository-static-audit.yml](../../.github/workflows/civ-full-repository-static-audit.yml) |
| 실행 결과 파일 | 위 성공 Run의 `civ-full-repository-audit` artifact (JSON 및 Markdown) |

2차 실행에서 `git ls-files`로 확인된 **618개 파일** 중 **텍스트 615개**를 UTF-8 디코딩하고 종류별로 검사했다. 나머지 3개는 `.pyc` 이진 파일로 구조 파싱 대상이 아니다. Python 구문 컴파일, CSV 행/헤더 열 수 검사, JSON·YAML·SVG 파싱, 주요 권위 CSV 참조 관계 검사, 기존 Python 검증·테스트 **23개 재실행**을 포함한다.

**주의:** 모든 파일을 파싱했다는 것은 각 파일의 **역사적 사실·수치·외부 출처·과거 사용자 합의**까지 모두 검증했다는 뜻이 아니다. 대형 지도 원천 래스터의 실제 다운로드·지형/바이옴 재계산 및 문명 게임 엔진 통합실행은 이 정적 감사에 **포함되지 않는다**.

## 2. 주요 정적검사 통과 항목

| 계통 | 자료·실검증 항목 | 결과 |
|---|---|---|
| 기술 | `technology_roster_locked_v2.csv` ↔ `technology_tree_historical_v2.csv` ↔ `MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv` | 109개 일치, ID 중복/선행기술 누락/역행·순환 0 |
| 사회제도 | `civic_roster_locked_v1.csv`의 시대별 COUNT(합계 72) ↔ `civic_tree_historical_v3.csv` ↔ `MASTER_CIVIC_UNLOCKS_72_V3.csv` | 72개 일치, 선행제도 누락/순환 0 |
| 정책카드 | `FINAL_POLICY_CARD_ROSTER_V1.csv` | 127개, 존재하지 않는 CIVIC 참조 0 |
| 유닛 | `FINAL_GENERIC_UNIT_ROSTER_V1.csv` | 89개, 기술·사회제도 게이트 참조 누락 0 |
| 건물 | `FINAL_GENERIC_BUILDING_ROSTER_V1.csv` 102개 + V3 ADD 2개 ↔ `FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv` | 104개 일치, 중복 0 |
| 건물 정부 게이트 | Tier-2/3 government adoption | 일반 CIVIC이 아닌 **기존 정식 정부 채택 게이트**로 인식 |
| 지도시설 | `FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv` | 39개, 게이트 참조 누락 0 |
| 기업 | `signature_corporate_founder_roster_v1.csv` ↔ `CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.csv` | 98명/32개 업종, 중복 및 업종·기술·사회제도 참조 누락 0 |
| 자원 | `resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv` | 12,500행, 고유 셀 12,500, 47개 자원, 음수·비수치 수량 0 |
| 위대한 과학자 | 12개 시대별 인물 MD ↔ `GREAT_SCIENTIST_CURRENT_SUMMARY.md` | 319명, 인명 중복 0, 양쪽 명단 동일 |
| 위대한 철학자 | 12개 시대별 인물 MD | 220명, 인명 중복 0 |
| 기존 검증 스크립트 | 23개 `test_*.py` 및 활성 `validate_*.py` | 재실행 전부 PASS |

검증의 무게중심은 최종 권위 자료의 **구문·키·ID·정규화·선행관계·중복**이다. **게임플레이 시뮬레이션 결과가 검증됐다는 뜻은 아니다.**

## 3. 실제 오류 발견 및 수정

1차 검사는 **8개 CSV 파일에서 총 29개 행**의 헤더 열 개수 불일치를 발견했다.

| 파일 | 형식 오류 행 수 | 조치 |
|---|---:|---|
| `tech_reference/atomic_tech_civic_unlock_audit_v1_part_a.csv` | 6 | 누락된 빈 열 보충 |
| `tech_reference/atomic_tech_civic_unlock_audit_v1_part_b.csv` | 2 | 누락된 빈 열 보충 |
| `tech_reference/industrial_tech_civic_unlock_audit_v1_part_a.csv` | 1 | 누락된 빈 열 보충 |
| `tech_reference/industrial_tech_civic_unlock_audit_v1_part_b.csv` | 9 | 누락된 빈 열 보충 |
| `tech_reference/modern_tech_civic_unlock_audit_v1_part_a.csv` | 4 | 누락된 빈 열 보충 |
| `tech_reference/modern_tech_civic_unlock_audit_v1_part_b.csv` | 4 | 누락된 빈 열 보충 |
| `tech_reference/technology_unlock_audit_v1.csv` | 2 | `FINAL_TECH` 누락 빈 칸을 복구해 `REASON`을 올바른 열로 이동 |
| `tech_reference/technology_unlock_summary_ancient_v1.csv` | 1 | 불필요한 끝부분 빈 열 제거 |
| **합계** | **29** | 원래 해금 선택값·수치의 의미 유지 |

형식만 교정했으며, 새 문명·기술·해금 효과는 추가하지 않았다. 2차 감사에서는 이 8개 CSV를 포함한 전체 텍스트 파일의 구조 검사에 **오류 0**.

## 4. 주의사항 3개 (오류와 분리)

1. **항공우주 기업 업종 창업가 집계:** 업종표는 2명(`Ozires Silva`, `William Boeing`), 플레이용 98명 명단에는 William Boeing 1명. Ozires Silva는 별도 조사에서 **REFERENCE_ONLY**. 업종표에 미플레이 인물을 포함한 집계로 남아 있음. [업종 설명 MD](../../corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.md)에 차이 명시.
2. **과학자 오래된 작업상태:** `city_system/great_scientists/WORK_STATE.md`에는 구형 332명이 남아 있고 활성 로스터는 **319명**. 원본 삭제 없이 파일 상단에 구형 상태 경고를 추가함.
3. **철학자 오래된 요약:** `city_system/great_philosophers/GREAT_PHILOSOPHER_CURRENT_SUMMARY.md` 구형 227명과 활성 **220명**의 차이를 파일 상단에 표시함.

## 5. 한국 원래 문명표의 회수 상태

이번 감사에서 관련 과거 대화 검색으로 **2026-06-19 초기 AI 한국표**, **2026-09-17 AI 한국 시대표**, 그리고 사용자가 **14~15세기를 르네상스로 교정한 발언**을 회수했다. 그러나 **사용자가 최종 승인한 한국 12시대의 완전한 표는 확인되지 않았다**.

기존 기록 중 **2026-09-25 중국 표를 사용자가 직접 작성했다고 귀속한 것은 잘못**이었으며, 사용자는 기존 12시대를 기준으로 중국 역사를 정리하도록 요청하고 AI가 실제 표를 제시한 것으로 정정했다. 이 교정은 `civilizations/`의 기존 회수 문서 5개에 반영했다.

- [한국 계보 복원 추적 원본·한계](../../civilizations/KOREA_CHRONOLOGY_SOURCE_TRACE_20261118.md)
- [6월 초기표](../../civilizations/EARLY_JUNE_2026_11ERA_HISTORICAL_SNAPSHOT.md)
- [9월 검토안·발언자별 출처](../../civilizations/EAST_ASIA_CONVERSATION_SOURCE_RECONSTRUCTION_V2.md)

**이는 사용자 원본 최종 로스터를 재현했다고 주장할 수 있는 상태가 아니다.**

## 6. 범위 밖 / 잔여 검증

- 현재 Git 추적 파일에 `.gpkg`, `.tif`, `.tiff`, `.shp`, `.nc`, `.parquet` 실제 지리 데이터는 없음. 지도 빌드 소스와 일부 자원 CSV는 있으나 **세계지도 래스터·최종 육각셀 지오메트리 재계산을 실행하지 않음**.
- 기존 게임 엔진의 실제 통합 장기 플레이, 종교/기업/건물/유닛 시스템의 런타임 결합 시험은 수행하지 않음.
- 모든 문헌·모드 원본 수치와 게임 수치 간 **역사적·출처별 의미 일치**는 미검증(정적 수치 구조만 검증됨).
- 전체 과거 ChatGPT 대화 메시지를 전수 다운로드한 것은 아님. 이전 대화에서 검색 가능한 회수 내용을 출처별 기록.
- 독립 `civilization-game` GitHub 원격 저장소는 미생성. 이 결과는 `academic_food_chain`의 `civ-game-map-stage1b-etopo2022` 브랜치에 실제 커밋으로 저장됨.

**이 문서를 '게임 전체 검증 완료' 또는 '모든 사용자 합의 복원 완료'로 인용하지 말 것.**
