# VP 타일개선 및 자원 시스템 재감사 V1

기준일: 2026-09-23

## 범위

공식 Vox Populi master의 다음 파일을 프로젝트와 대조했다.

- `WorldMap/Improvements/ImprovementChanges.sql`
- `WorldMap/Improvements/ImprovementSweeps.sql`
- `WorldMap/Improvements/BuildChanges.sql`
- `WorldMap/Resources/ResourceSweeps.sql`
- `WorldMap/Resources/ResourceChanges.sql`

프로젝트 측 기준:
- `resource_catalog_v1.yaml`
- `contact_dynamic_resource_system_v2.md`
- `MASTER_TECHNOLOGY_UNLOCKS_109_V1.csv`

## 결론

VP의 **타일 산출 구조, 자원별 개선 보너스, Monopoly 효과, pillage 가치, 시대별 improvement upgrade 철학**은 거의 전부 채택한다.

그러나 다음 프로젝트 규칙이 VP보다 우선한다.

1. Stage10 실제 지리 기반 자원 배치
2. 전략자원 증거기반 quantity
3. 18개 생물자원의 START_VISIBLE/LATENT/ACTIVE_INTRODUCED 동적 확산
4. Niter 프로젝트 추가
5. Saltworks 프로젝트 추가
6. Academy, Manufactory, Landmark, Holy Site, Customs House의 일반 Worker 시설화 및 너프
7. Great General Citadel 제거
8. Civ6에서 가져온 Dam, Canal, Airstrip, Seaside Resort, renewable-energy improvements, Seastead 유지

## 1. 일반 타일개선

### Farm
VP의 인접 Farm 네트워크를 채택한다.

- Fresh Water +1 Food
- Farm 2개 인접마다 +1 Food
- Civil Service +1 Food
- Mathematics +1 Food
- Fertilizer +2 Food
- Robotics +3 Food

### Village

VP Trading Post를 게임 표시상 **Village**로 사용한다.

- Gold +2
- Culture +1
- 인접 Village 금지
- Road 위: Gold +1, Production +1
- Railroad 위: Gold +2, Production +2
- Guilds: Gold +1
- Railroad: Culture +1

### 생산 및 자원 시설

Mine, Quarry, Pasture, Plantation, Camp, Fishing Boats, Lumber Mill은 VP의 기술별 증분을 채택한다. 프로젝트의 기존 기술 unlock 자체는 역사성 때문에 일부 유지한다.

## 2. 일반화된 옛 위인 시설

프로젝트의 기존 확정:
- Academy
- Manufactory
- Landmark
- Holy Site

는 **위인을 소비하지 않는 일반 Worker improvement**다.

따라서 VP의 원래 GPTI 숫자를 그대로 복사하지 않는다.

예를 들어 VP Academy는 기본 Science 6에 Physics, Scientific Theory, Rocketry, Nuclear Fission에서 각각 Science +3을 받는다. 이 값을 일반 Worker 시설에 그대로 주면 타일 스팸이 최적전략이 된다.

V1 잠정 너프:
- Academy: Science +2, 인접 Academy 금지, 주요 시대마다 Science +1
- Manufactory: Production +2, 인접 Manufactory 금지
- Landmark: Culture +2, Gold +1, 인접 Landmark 금지
- Holy Site: Faith +2, Culture +1, 인접 Holy Site 금지

Landmark의 VP `HappinessOnConstruction=3`도 Worker spam 악용 때문에 채택하지 않는다.

Customs House 역시 프로젝트가 이미 Worker-built nerfed improvement로 지정했으므로 VP GPTI보다 약하게 둔다.

## 3. Citadel

**도입하지 않는다.**

Great General Citadel은 프로젝트에서 이미 삭제됐다. VP의 Citadel 산출과 기술 upgrade도 가져오지 않는다.

Fort가 일반 군사 타일시설 역할을 담당한다.

## 4. 47개 자원

프로젝트 47개 자원을 모두 감사표에 넣었다.

- Strategic 7
- Bonus 10
- Luxury 30

VP에 없는 Niter만 프로젝트 확장으로 별도 처리한다.

VP에서 삭제/합병하기로 한 Nutmeg, Cloves, Pepper, Jewelry, Porcelain, Glass는 다시 추가하지 않는다.

## 5. 자원 배치 및 발견

VP의 랜덤 map placement 수치는 **채택하지 않는다**.

우리 게임은 Stage10 실제 분포를 사용한다.

18개 동적 생물자원:
`BANANAS, CATTLE, CITRUS, COCOA, COFFEE, COTTON, DYES, HORSES, MAIZE, OLIVES, RICE, SHEEP, SPICES, SUGAR, TEA, TOBACCO, WHEAT, WINE`

에는 VP TechReveal을 적용하지 않고 기존 V2의:
- START_VISIBLE
- LATENT
- ACTIVE_INTRODUCED
- civilization has_resource

구조를 유지한다.

즉 **VP의 수익/독점 시스템을 가져오되 역사적 이동 규칙은 프로젝트가 우선**한다.

## 6. 전략자원 발견

프로젝트 기존 reveal을 유지한다.

- Iron: Bronze Working
- Niter: Military Engineering
- Coal: Manufacturing
- Oil: Refining
- Aluminum: Electricity
- Uranium: Atomic Theory
- Horses: 동적 생물자원 규칙 우선

이는 VP의 Coal=Chemistry, Oil=Dynamite, Aluminum=Industrialization보다 프로젝트 기술트리의 역사적 배치를 우선한 것이다.

## 7. Monopoly

VP Monopoly를 프로젝트 47-resource 체계에 거의 전부 매핑했다.

대표:
- Iron: 타일 Production +2, 전략 독점 Defense +10%
- Horses: 타일 Science +2, Attack +10%
- Coal: 타일 Gold +3, 해군 Attack/Defense +10%
- Oil: 타일 Science +2, XP +2
- Aluminum: 타일 Production +2, Heal +5
- Uranium: Science +10%, Attack +10%
- Salt/Sugar/Olives: Food +10%
- Copper/Coffee: Production +10%
- Silk/Gems: Gold +10%
- Tea/Marble: Culture +10%
- Luxury는 VP 기준 기본 Happiness +2

Niter Monopoly만 VP 원형이 없으므로 추후 별도 설계한다.

## 8. 교차 수정 필요

이번 감사로 기존 건물 V2에서 한 가지 후속 수정이 필요해졌다.

VP Research Lab의 `Academy Science +4`, Factory의 `Manufactory Production +2`는 VP에서 GPTI가 희소하다는 전제다. 프로젝트에서는 Academy/Manufactory가 Worker-built이므로 **그대로 적용하면 과도하다**.

따라서 전문가/위인 및 최종 도시 산출 감사 때:
- Research Lab → Academy 보너스 축소
- Factory → Manufactory 보너스 축소 또는 제거

를 재조정한다.

## 9. 상태

- VP 일반 improvement 시스템: 채택
- VP resource yield: 47-resource 체계에 매핑 완료
- VP Monopoly: Niter 제외 매핑 완료
- Stage10 placement: 프로젝트 우선
- 동적 자원 확산: 프로젝트 우선
- GPTI: Worker-built nerfed variant
- Citadel: 제외
- Modern Civ6/project improvements: 유지, 전력 시스템에서 수치 확정
