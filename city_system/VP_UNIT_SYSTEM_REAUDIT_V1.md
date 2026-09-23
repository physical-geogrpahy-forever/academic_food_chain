# VP 유닛 시스템 전수감사 V1

기준일: 2026-09-23

## 감사 범위

현재 `FINAL_UNIT_NUMERIC_BALANCE_V1.csv`의 **89개 유닛 전부**를 VP 공식 master의:
- `UnitStatChanges.sql`
- `UnitCostSweeps.sql`
- `UnitChanges.sql`
- `UnitChanges2.sql`

과 대조했다.

## 판정

- VP 직접 대응: **56**
- VP 유사계보 적용: **9**
- 역할 충돌 검토: **4**
- 프로젝트 고유/직접대응 없음: **20**

## 매우 큰 차이

현재 프로젝트는 상당 부분 Civ V BNW 전투력을 그대로 사용하지만 VP는 전투력 곡선을 전면 재작성한다.

대표 예:

| 유닛 | 현재 | VP |
|---|---:|---:|
| Spearman | 11 | 12 |
| Swordsman | 14 | 16 |
| Pikeman | 16 | 18 |
| Knight | 20 | 24 |
| Lancer | 25 | 37 |
| Rifleman | 34 | 38 |
| Infantry | 50 | 62 |
| Mechanized Infantry | 70 | 80 |
| Tank | 70 | 75 |
| Modern Armor | 100 | 100 |
| Trireme | 10 | 18 |
| Ironclad | 45 | 55 |
| Destroyer | 55 | 70 |

Ranged 계열도 VP값을 우선한다. 예:
- Archer 6/9
- Composite Bowman 11/14
- Crossbowman 15/19
- Gatling Gun 32/44
- Machine Gun 45/58
- Catapult 5/13
- Trebuchet 8/20
- Field Gun 17/40
- Artillery 27/50
- Rocket Artillery 37/75

## 해군과 항공

VP는 해군과 항공 비용도 별도 class table로 명시한다.

예:
- Trireme 120
- Caravel 160
- Privateer 350
- Ironclad 900
- Destroyer 1300
- Frigate 375
- Cruiser 900
- Battleship 1800
- Missile Cruiser 2500
- Submarine 1300
- Nuclear Submarine 2500
- Triplane 800
- Fighter 1400
- Jet Fighter 2100
- WWI Bomber 850
- Bomber 1500
- Stealth Bomber 2200

단, 우리 건물 Production 비용 전체가 아직 VP 생산비용 곡선으로 최종 정규화되지 않았으므로 이 비용은 현재 CSV에서 **REFERENCE**로 분리한다. 전투력/사거리/이동력은 직접 대응이 명확한 경우 바로 채택 후보로 본다.

## 역할 충돌 4개

1. **Cavalry**
   - 프로젝트: melee LIGHT_CAVALRY
   - VP: range-1 mounted skirmisher, 40/31, Moves 5
2. **Anti-Tank Gun**
   - 프로젝트: anti-armor
   - VP: ranged light-tank/skirmisher 성격
3. **Helicopter**
   - 프로젝트: melee light cavalry
   - VP: 70/70 ranged skirmisher
4. **Aircraft Carrier**
   - 프로젝트: 비공격 플랫폼 중심
   - VP: 70/45, Range 2의 자체 전투능력 보유

이 네 항목은 VP 숫자만 복사하면 우리 역할체계가 바뀌므로 별도 결정이 필요하다.

## VP에서 추가 채택할 전투 원칙

- Mounted, Armor, Siege는 방어지형/fortify 이점을 제한
- Mounted와 Armor는 공격 후 이동
- Mounted는 도시공격 페널티
- Siege는 도시공격 특화 + 야전 정확도 페널티 + setup 성격
- Submarine은 은폐/대함 특화, 도시공격 약화
- Fighter는 air sweep/interception/anti-air 정체성 강화
- Recon은 정찰과 기동에 명확한 역할 부여
- 유닛 구매에는 시대별 Barracks/Armory/Military Academy/Harbor/Seaport/Airport 요구를 검토

## 생산비용 처리

VP land unit은 기술 GridX에 따라 basic/advanced cost를 정한다. 우리 109-tech tree는 GridX가 다르므로 **VP 비용 숫자를 이름만 보고 직접 복사하지 않는다**.

다음 단계에서:
`project tech tier → VP-equivalent tier → land basic/advanced cost`
매핑을 만든 뒤 전체 건물비용과 함께 정규화한다.

## 결론

직접 대응되는 유닛의 VP 전투력, 사거리, 이동력은 도입하는 것이 현재 'VP 거의 전면 채택' 원칙과 맞다. 다만 프로젝트 고유 중간유닛과 Civ6에서 가져온 역할은 VP 유사계보로 보간하며, 역할 자체가 충돌하는 4개는 별도 잠금 후 수치화한다.
