# VP 기술 및 사회제도 진행속도 재감사 V1

기준일: 2026-09-23

## 결론

- 기술 109개 roster는 유지한다.
- 사회제도 72개 roster도 유지한다.
- VP의 기술 비용 곡선은 직접 참고하되, 13개 프로젝트 시대에 맞게 중간 단계를 삽입한다.
- 사회제도는 VP의 정책 트리를 그대로 복제하지 않는다. 우리 게임은 Civ VI식 civic node 구조이므로 Culture 비용은 VP 정책비용의 상승 철학과 프로젝트 Science 곡선을 함께 사용한다.
- 모든 비용은 현재 **PROVISIONAL**이다. 건물, 유닛, 타일산출을 VP화한 뒤 자동 시뮬레이션으로 최종 보정한다.

## VP에서 확인한 기술 비용 곡선

VP `TechCostSweeps.sql`의 GridX별 기술 비용:
`20, 60, 100, 130, 275, 500, 700, 1750, 2400, 3600, 5150, 8100, 11000, 13000, 16000, 19100, 23400, 24450, 28550`.

우리 게임은 Late Antiquity, Early Medieval, High Medieval, Exploration, Enlightenment 등을 별도 시대로 세분하므로 이 곡선을 그대로 1:1 매핑하지 않고 형태를 유지하면서 13개 시대에 재분배했다.

## Science 잠정 비용대

| 시대 | 기술 수 | 비용대 |
|---|---:|---:|
| Ancient | 14 | 20–130 |
| Classical | 10 | 200–500 |
| Late Antiquity | 5 | 650–850 |
| Early Medieval | 5 | 950–1300 |
| High Medieval | 6 | 1500–2000 |
| Renaissance | 5 | 2200–2800 |
| Exploration | 8 | 3200–4200 |
| Enlightenment | 6 | 4700–5800 |
| Industrial | 16 | 6500–10500 |
| Modern | 12 | 11500–15500 |
| Atomic | 5 | 17500–20500 |
| Information | 9 | 22500–26000 |
| Future | 8 | 28550–32000 |

## Culture 잠정 비용대

| 시대 | 사회제도 수 | 비용대 |
|---|---:|---:|
| Ancient | 7 | 15–90 |
| Classical | 5 | 140–330 |
| Late Antiquity | 4 | 420–600 |
| Early Medieval | 4 | 650–900 |
| High Medieval | 4 | 1000–1400 |
| Renaissance | 4 | 1550–2000 |
| Exploration | 6 | 2200–2900 |
| Enlightenment | 5 | 3300–4000 |
| Industrial | 9 | 4700–6500 |
| Modern | 6 | 7600–9500 |
| Atomic | 5 | 10500–12500 |
| Information | 7 | 14500–17500 |
| Future | 6 | 20000–23000 |

## 발견된 기존 데이터 오류

`civic_roster_locked_v1.csv`은 2026-09-21 후기시대 분할을 반영했으나 `civic_tree_locked_v1.csv`에는 이전 시대 값이 남아 있었다.

수정:
- Environmentalism: Atomic → Information
- Information Warfare: Information → Future
- Global Warming Mitigation: Information → Future
- Cultural Hegemony: Information → Future
- Smart Power Doctrine: Information → Future
- Exodus Imperative: Information → Future
- Future Civic: Information → Future

그래프의 prerequisite 관계는 그대로 유지되며 후기 시대의 역사적/게임적 순서만 roster와 일치시켰다.

## 과학 시스템에서 VP와 함께 채택할 요소

1. known-civ technology discount
2. prerequisite를 더 많이 확보했을 때의 연구 보정
3. 팀 연구비용 보정
4. 기술비용의 급격한 후기 상승
5. 기술 해금에 따른 타일개선 산출 증가
6. 기술과 유닛/건물 생산비용의 같은 tier 연동

단, Civ VI식 Eureka는 우리 프로젝트에 이미 존재하므로 VP DLL의 선택적 Civ6 Eureka 지원을 우리 룰에 맞게 유지한다.

## 사회제도 시스템

VP의 Social Policy는 우리의 Civic node와 같은 것이 아니므로 직접 숫자 복사는 금지한다.

우리 구조:
`Culture 생산 → Civic 연구 → 정책카드/정부/건물/유닛 해금 → 새 civic 완료 시 무료 정책 재편`

VP에서 가져오는 것은:
- Culture 비용의 비선형 증가
- 제국 규모가 문화 진행에 미치는 부담을 무시하지 않는 설계
- 정책 선택의 장기적 전문화
- 후기 이념/정부 체제의 높은 전환 가치

## 다음 재보정 조건

다음이 끝난 뒤 Science/Culture 절대값을 시뮬레이션한다.
1. 유닛 VP 수치 감사
2. 타일개선 및 자원 산출 VP 감사
3. 전문가 및 위인 발생량 감사
4. 불가사의 감사
5. Standard 속도 AI autoplay

목표는 기술 또는 사회제도 하나가 '몇 턴이어야 한다'를 고정하는 것이 아니라, 각 시대의 평균 체류시간과 주요 군사/경제 업그레이드 간 간격이 VP와 유사한 긴장감을 갖게 하는 것이다.
