# 문명 선정·계보 작업장 (2026-11-18 회수본)

## 2026-11-19 유럽 116계보 게임 구현 분류 (최신)

- **[116계보 분류 마스터 V1](EUROPE_116_CIVILIZATION_PLAYABILITY_CLASSIFICATION_MASTER_V1.md):** A 핵심 독립 문명 **41**, B 시대·지역 특화 독립 문명 후보 **59**, C 문화권·보조 정치체 **16**. 각 행의 역사적 유형·중복 관계·주의사항·미확정 기준을 설명한다.
- **[116계보 분류 CSV](EUROPE_116_LINEAGES_PLAYABILITY_TRIAGE_V1.csv):** 원본 116행과 일대일 대응, 지역·정치체 유형·첫/마지막 등장 시대·긴급 검토·승인상태를 기록. **USER_APPROVAL_STATUS=PROPOSED_NOT_USER_LOCKED**.
- [분류 검증기](../tools/validate_europe_classification_v1.py): 원래 116행·13시대와 분류 CSV의 일치 여부, 중복·누락·승인상태·고증 우선순위를 검사한다.
- **사용자 원본 `문명.xlsx`와 동아시아 수정안은 그대로 보존**, 유럽 A/B/C는 새 설계 제안으로만 추가.

## 2026-11-18 유럽 계보 전수 후보 풀

- [유럽 문명·정치체 계보 전수 정리 V1](EUROPE_CIVILIZATION_GENEALOGY_MASTER_REVIEW_20261118.md): 고대 문명·부족·부족연맹·왕국·제국·근대국가·초국가 조직의 구분, 연대와 관계 주의사항, 참고자료.
- [유럽 전체 116계보 시대별 매트릭스](EUROPE_FULL_ERA_MATRIX_DRAFT_20261118.csv): 사용자 `문명.xlsx`의 13개 시대 열과 동일한 순서로 만든 116행 후보 CSV. **플레이 가능 문명 116개 확정이 아님.**
- [고대 문명·부족 확대 조사](EUROPE_ANCIENT_CIVILIZATIONS_AND_TRIBAL_POLITIES_DRAFT_20261118.md): 미노스·미케네·키클라데스, 골족·삼니움·이베리아·일리리아·트라키아 등 상세 후보.
- [유럽 범위 초안](EUROPE_CIVILIZATION_SCOPE_DRAFT_20261118.md): 최초 21개 국가 중심 범위 제안. 최신 전수 후보 풀은 위 master review를 우선 참조.
- 원본 `문명.xlsx`와 한중일 수정안은 이번 유럽 후보 작성 과정에서 변경하지 않았다.

> **2026-11-18 사용자 원본 엑셀 발견:** `문명.xlsx`의 `Sheet1!A1:N25`를 직접 확인했다. **[원본 셀 값 보존 CSV](USER_UPLOADED_CIVILIZATION_SHEET1_20261118.csv)**와 **[원본 출처·SHA-256·우선순위 기록](USER_UPLOADED_XLSX_SOURCE_AUTHORITY_20261118.md)**을 우선한다. 기존의 '한국 원본 미복원' 및 AI 시대별 추정표는 **엑셀 첨부 이전의 복구 상태**에 해당하며, 현재 사용자 제공 원본을 대체하지 않는다. **원본의 일본 고대~중세 성기 빈칸과 중국 후기 고대 '수'도 임의 수정 금지.**

**현재 단계: 동아시아 사용자 엑셀 원본을 보존한 상태에서 유럽 문명 후보 116개 분류 및 Civilization roster 설계 — NOT LOCKED**

> 문명/국가 계보에 대해서는 **이 디렉터리의 출처·상태 표시를 우선 확인**하고, 기존 2026-10-16 인계문의 중국·일본 검토안을 최종 확정표로 잘못 인용하지 말 것.

| 파일 | 내용 | 확정 수준 |
|---|---|---|
| [EAST_ASIA_12ERA_RECOVERY_V1.md](EAST_ASIA_12ERA_RECOVERY_V1.md) | 한·중·일 12시대 계보, 한국 미복원, 중국/일본 검토안 | **회수·검토본** |
| [EAST_ASIA_12ERA_RECOVERY_V1.csv](EAST_ASIA_12ERA_RECOVERY_V1.csv) | 12시대 기계 판독 테이블, 국가별 근거 등급 | **NOT_LOCKED** |
| [CONVERSATION_DECISIONS_PROVENANCE_20261118.md](CONVERSATION_DECISIONS_PROVENANCE_20261118.md) | 관련 과거 대화 근거·확정/초안 구분·GitHub 감사·미완료 목록 | **근거 장부** |

## 사용자 지시 및 작업 순서

- **한국·중국·일본부터** 문명 확정. 북미·중앙아메리카·카리브는 현재 **보류**.
- 사용자 고정 **12개 역사시대** 사용, 14~15세기는 르네상스.
- 단순 문화기·시대명·정권명과 독립 Civilization을 혼동 금지.
- 국가 계보의 연속성은 근거 없는 직접 승계로 표시하지 않는다.
- 한국 시대별 원본은 사용자가 제공한 **문명.xlsx의 Sheet1**에 존재함을 확인했다. 이전 AI 복구표는 사용자 원본을 대체하지 않는다.
- 사용자 현재 지시: **지도자 제외하고 문명만**. 이후 문명/지도자 확정 뒤 혁명가 연결.
- 이 디렉터리에서 사용하는 `NOT_LOCKED`를 제거하려면 사용자 명시적 승인과 변경 근거가 필요하다.

## 2026-11-18 한국 원문 추적 및 GitHub 검증

- [KOREA_CHRONOLOGY_SOURCE_TRACE_20261118.md](KOREA_CHRONOLOGY_SOURCE_TRACE_20261118.md): 6월 19일과 9월 17일 **한국 AI 원안·사용자 교정·미복원 상태**를 날짜별로 추적. 사용자 확정표를 재창작하지 않는다.
- [CIV_REPOSITORY_STATIC_AUDIT_20261118.md](../docs/audits/CIV_REPOSITORY_STATIC_AUDIT_20261118.md): 618개 파일·23개 기존 검증기·8개 CSV 29행 수정의 GitHub Actions **실행 증거와 한계**.

## 초기 11시대 자료 (역사 기록)

- [EARLY_JUNE_2026_11ERA_HISTORICAL_SNAPSHOT.md](EARLY_JUNE_2026_11ERA_HISTORICAL_SNAPSHOT.md): 2026-06-19 한국·중국 **초기 AI 시대별 원안**을 별도로 보존. 9월 12시대 원안으로 오인하거나 덮어쓰지 않는다.

## 원래 대화 표의 회수본 (V2)

- [EAST_ASIA_CONVERSATION_SOURCE_RECONSTRUCTION_V2.md](EAST_ASIA_CONVERSATION_SOURCE_RECONSTRUCTION_V2.md): **2026-09-17 한국 AI 최초 초안**, **2026-09-25 중국 계보 AI 초안(사용자 시대구분 요청)**, **2026-09-26 일본 AI 제안**을 출처별로 분리. 한국 초기 AI표는 연대 오류가 있으므로 최종 문명표로 쓰지 않는다. **이전 V1의 한국 '미복원'은 최종 사용자 승인 칸에 한정**한다.

## 과거 문명 프로젝트 대화 색인

- [PROJECT_CONVERSATION_WORKSTREAM_INDEX_20261118.md](PROJECT_CONVERSATION_WORKSTREAM_INDEX_20261118.md): 문명 1~5와 후속 대화에서 확인 가능한 결정사항 및 실제 GitHub 파일 대응표. **모든 메시지 원문을 전수 열람한 것은 아님.**

## 기반 권위 문서

- [기존 2026-10-16 문명/혁명가 인계문](../docs/handoffs/CHATGPT_WORK_HANDOFF_CIVILIZATIONS_REVOLUTIONARIES_20261016_KO.md)
- [Great Revolutionary WORK_STATE](../city_system/great_revolutionaries/WORK_STATE.md)
- [게임 콘텐츠 소스 우선순위](../city_system/PROJECT_CONTENT_SOURCE_PRECEDENCE_V1.md)
