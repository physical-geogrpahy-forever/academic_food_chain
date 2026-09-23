# VP 기술-사회제도-유닛-타일-자원 2차 QA V2

Date: 2026-09-23
Status: PASS WITH NUMERIC DEFERMENTS

## 범위

이번 QA는 다음 순서를 대상으로 한다.

1. 기술 및 사회제도
2. 유닛
3. 타일개선
4. 자원
5. 네 영역 사이의 교차 연결

## 1. 기술 및 사회제도 QA

- 기술 roster: 109
- civic roster: 72
- 별도 Future Era 유지
- 후기 civic 시대 불일치: 수정 완료
- VP형 Science/Culture 비용곡선: provisional 작성 완료
- 기존 tech master와 VP tile progression 충돌: override V2 작성 완료

판정: **PASS**

남은 작업은 roster 구조가 아니라 global numeric calibration이다.

## 2. 유닛 QA

V2 감사에서 발견된 role conflict 4개:

- Cavalry
- Anti-Tank Gun
- Helicopter
- Aircraft Carrier

모두 V2 resolution에서 처리 완료.

판정:

- Cavalry -> mounted skirmisher
- Anti-Tank Gun -> dedicated anti-armor 유지
- Helicopter -> mounted skirmisher/gunship
- Aircraft Carrier -> carrier platform 유지, VP-era defense만 채택

VP unit cost sweep도 별도 cost anchor table로 연결했다.

판정: **PASS FOR ROLE STRUCTURE**

아직 provisional:

- global Production multiplier
- upgrade Gold
- anti-armor bonus magnitude
- strategic-resource upkeep

## 3. 타일개선 QA

29개 개선을 다시 점검했다.

확정된 주요 progression:

- Farm: Mathematics / Civil Service / Fertilizer / Robotics
- Village: Guilds / Railroad
- Mine: Steel / Steam Power / Combustion / Robotics
- Quarry: Machinery / Steam Power / Dynamite
- Pasture: Civil Service / Fertilizer / Robotics
- Plantation: Chemistry / Economics / Plastics
- Camp: Guilds / Gunpowder / Rifling / Refrigeration
- Fishing Boats: Compass / Navigation / Refrigeration
- Lumber Mill: Metallurgy / Combustion
- Fort: Chemistry / Military Science / Stealth Technology / Electronics

Customs House V1 오류:

- Banking upgrade: 제거
- Architecture upgrade: 제거

이유:

- Banking은 Customs House 해금보다 빠르다.
- Architecture는 프로젝트 기술 roster에 없다.

판정: **PASS**

## 4. 자원 QA

- 47개 프로젝트 자원에 VP yield/monopoly mapping 유지
- 실제 Stage10 배치 우선
- 동적 생물자원 visibility 우선
- Horses tech reveal 충돌 제거
- Niter monopoly 신규 확정

Niter:

- Monopoly = gunpowder and siege unit Production +10%

판정: **PASS**

## 5. 자원-건물 interaction QA

V1 미해결 4행:

- Bison -> Smokehouse
- Deer -> Smokehouse
- Iron -> Forge
- Copper -> Forge

V2 해결:

- Smokehouse를 실제 generic building으로 추가 예정
- Forge를 Bronze Working generic building으로 추가 예정
- 기존 늦은 건물에 임시 mapping하지 않음

판정: **RESOLVED, BUILDING ROSTER UPDATE REQUIRED**

## 6. 아직 의도적으로 미확정인 것

### Power improvements

- Solar Farm
- Geothermal Plant
- Wind Farm
- Offshore Wind Farm

정확한 산출은 Power demand/supply 단위 확정 후 결정한다.

### GP-derived Worker improvements

- Academy
- Manufactory
- Landmark
- Holy Site
- Customs House

이들은 위인을 소비하지 않으므로 full VP GPTI보다 약하게 유지한다.

건물 V2의 다음 보너스는 재검토 대상:

- Research Lab -> Academy Science +4
- Factory -> Manufactory Production +2

일반 Worker가 반복 건설할 수 있기 때문에 VP 원본 보너스를 그대로 쓰면 과도할 가능성이 높다.

### Global cost multiplier

VP unit cost ratios는 채택했지만, 프로젝트는 109 tech / 72 civic / 13 eras 체계이므로 최종 Production multiplier는 autoplay 후 고정한다.

## 7. 권위 파일

이번 범위에서 충돌 시 다음 파일을 우선한다.

1. `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V2.md`
2. `tech_reference/VP_TECH_TILE_RESOURCE_OVERRIDE_V2.csv`
3. `civics_reference/VP_CIVIC_TILE_OVERRIDE_V2.csv`
4. `city_system/VP_UNIT_ROLE_CONFLICT_RESOLUTION_V2.csv`
5. `city_system/VP_TILE_IMPROVEMENT_ADOPTION_V2.csv`
6. `civ_map_stage10_resources/VP_RESOURCE_OVERRIDE_V2.csv`
7. 기존 V1 master/summary

## 최종 판정

**기술/사회제도 -> 유닛 -> 타일개선/자원의 2차 구조 QA는 통과.**

남은 항목은 구조적 충돌이 아니라 다음 단계의 수치 통합과 building roster 반영이다.
