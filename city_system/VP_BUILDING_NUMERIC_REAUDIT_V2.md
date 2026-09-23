# VP 건물 수치 전수감사 V2

기준일: 2026-09-23

## 결과

- 감사 대상: **102개 건물 전부**
- VP exact 채택: **35개**
- 프로젝트 VP 확장: **39개**
- V1 유지: **28개**

이번 패스는 VP 공식 master의 BuildingChanges.sql, PreBuildingChanges.sql, NewConceptText.xml을 직접 대조했다. 특히 VP가 기존 Building_YieldChanges와 Building_YieldModifiers를 초기화한 뒤 건물별 산출을 다시 정의한다는 점을 확인하여, 단순 BNW 수치 위에 VP 효과를 덧붙이지 않고 확인 가능한 항목은 실제로 교체했다.

## 핵심 변경 원칙

1. VP Needs는 우선 flat reduction 1 구조를 그대로 사용한다.
2. Barracks, Armory, Military Academy는 Supply +1, Distress -1을 채택한다.
3. Walls 계열은 Supply % 증가, Harbor/Stable은 Supply flat 증가를 채택한다.
4. Library → University → Public School → Research Lab은 Illiteracy -1을 각 단계에 적용한다.
5. Arena/Circus/Zoo는 VP식 Boredom 구조로 바꾸고 직접 Happiness 남발을 줄인다.
6. Health와 Stability는 VP 원본에 없는 우리 게임 확장값이므로 PROVISIONAL로 명시했다.
7. 전체 비용곡선은 기술/사회제도 비용이 확정된 뒤 다시 맞추되, 명백한 시대상 비용 이상치 3개만 먼저 수정했다.

## 비용 조정

| 건물 | V1 | V2 | 이유 |
|---|---:|---:|---|
| Workshop | 120 | 180 | High Medieval 배치에서 지나치게 저렴 |
| University | 160 | 200 | High Medieval 과학 핵심 건물의 시대 비용 정렬 |
| Constabulary | 160 | 220 | Renaissance 행정/첩보 건물 비용 정렬 |

## 변경/확장 건물 전수표

| 건물 | 시대 | 판정 | Distress | Poverty | Illiteracy | Boredom | Religious | Supply flat | Supply % | Health | Stability | 이유 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Palace | Ancient | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | VP verified: Palace yields 3 Production, 5 Gold, 6 Science, 1 Culture and 3 Literature slots; project adds provisional capital Stability +2. |
| Walls | Ancient | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP defense-line adaptation: +5% city military supply; existing defense/HP values retained. |
| Monument | Ancient | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Monument keeps 2 Culture and gains one Art/Artifact slot. |
| Granary | Ancient | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | VP verified: Granary +1 Food, 15% food kept, instant Food 25. Project Health +1 provisional for food storage/sanitation role. |
| Courthouse | Ancient | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | Occupation/administration building: provisional local Stability +2; occupied-status removal retained. |
| Government Plaza | Ancient | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | Central government hub: provisional Stability +2; tier building unlock role retained. |
| Barracks | Ancient | VP_EXACT_ADOPTED | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | VP verified: Barracks gives Supply +1, Distress reduction 1 and +1 Science; existing XP retained. |
| Shrine | Ancient | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Shrine yields 2 Faith and has one Music slot. |
| Library | Ancient | VP_EXACT_ADOPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Library is +2 Science, one Scientist slot, Illiteracy reduction 1; Civ5 science-per-2-pop effect removed. |
| Recycling Center | Information | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Project environmental/Health adaptation: Health +2 provisional and existing pollution -25% retained. |
| Caravansary | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Caravansary +1 Gold, land trade Gold +3, trade-finish Tourism 10 and desert/tundra scaling yields. |
| Market | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified Market gains +3 flat Gold; existing project 25% Gold and Merchant slot retained. |
| Amphitheater | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Amphitheater/Theater has 2 Culture, two Great Work slots and +33% Great Writer generation. |
| Arena | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP verified Arena/Colosseum: direct Happiness removed, Boredom reduction 1, +1 Culture. |
| Circus | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP verified: Circus +1 Happiness, Boredom reduction 1, 10 WLTKD turns and instant 100 Culture. |
| Aqueduct | Classical | VP_EXACT_ADOPTED | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | VP verified: Aqueduct +1 Food, 15% food kept, Poverty reduction 1, lake/oasis food and era-scaled Production on birth; Health +2 is project adaptation. |
| Ancestral Hall | Classical | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Audience Chamber | Classical | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Consulate | Classical | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Warlord's Throne | Classical | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Harbor | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | VP verified: Harbor Supply +1, +1 Gold, sea-tile Food +1, sea-resource Production +1 and naval Production +15%; project connection/trade rules retained. |
| Stable | Classical | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | VP verified Stable gives Supply +1 and +3 Production; project pasture/mounted effects retained. |
| Paper Workshop | Classical | PROJECT_VP_ADAPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Project paper/record building: VP-style Illiteracy reduction 1 added; existing +1 Science retained. |
| Castle | Early Medieval | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP defense-line adaptation: +5% city military supply; existing defense/HP values retained. |
| Court | Early Medieval | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Customs Office | Enlightenment | PROJECT_VP_ADAPTED | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Mapped to VP Customs House role: Poverty reduction 1 and trade route sender/recipient Gold +2 each; project international-trade modifier retained. |
| Stock Exchange | Enlightenment | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Stock Exchange +3 Gold, one Merchant slot, +0.5 Gold/pop, -20% Gold purchase cost and +2 Gold on Trading Post/Customs House. |
| Archaeological Museum | Enlightenment | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP Museum analogue: flat Boredom reduction 1 and 0.25 Culture/Tourism per population; applied to mutually exclusive museum branches. |
| Newspaper Office | Enlightenment | PROJECT_VP_ADAPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Project mass-literacy/public-sphere building: Illiteracy reduction 1 added; Gold/Culture/Great Work values retained. |
| Aquarium | Enlightenment | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Civ6 entertainment branch adapted to VP Needs: Boredom reduction 1; existing local Happiness retained. |
| Ferris Wheel | Enlightenment | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Civ6 entertainment branch adapted to VP Needs: Boredom reduction 1; existing local Happiness retained. |
| Zoo | Enlightenment | VP_EXACT_ADOPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP verified Zoo/Theatre: direct Happiness removed, Boredom -1, +2 Culture, trade Tourism, instant Science and forest/jungle Culture/Tourism. |
| Military Academy | Enlightenment | VP_EXACT_ADOPTED | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | VP verified: Military Academy gives Supply +1, Distress reduction 1, +1 Science, 25 XP and +15% land unit Production. |
| Chemical Laboratory | Enlightenment | PROJECT_VP_ADAPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Project intermediate science building: Illiteracy reduction 1 added to keep VP Needs progression. |
| Public School | Enlightenment | VP_EXACT_ADOPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Public School +3 Science and Illiteracy reduction 1; science-per-pop carryover removed. |
| Star Fort | Exploration | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP defense-line adaptation: +5% city military supply; existing defense/HP values retained. |
| Opera House | Exploration | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Opera House has 3 Culture, +5% Culture and +33% Great Musician generation. |
| Seaport | Exploration | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | VP verified: Seaport +10% supply, +1 Production/+1 Gold on sea tiles and +2 Production/+2 Gold on sea resources. |
| Workshop | High Medieval | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP production role adopted; project-era cost raised 120→180 because High Medieval placement made the BNW-era cost an outlier. |
| University | High Medieval | VP_EXACT_ADOPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | VP science role adopted; project-era cost raised 160→200 to fit High Medieval progression without changing later science-chain costs. |
| Foreign Ministry | High Medieval/Exploration | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Grand Master's Chapel | High Medieval/Exploration | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Intelligence Agency | High Medieval/Exploration | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Military Base | Industrial | VP_EXACT_ADOPTED | 1 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP verified: Military Base +5% supply, Distress -1, heal +20, air-strike defense +15 and air unit Production +25%. |
| Shopping Mall | Industrial | PROJECT_VP_ADAPTED | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Project retail capstone: Poverty reduction 1 added; Tourism/Power interactions retained. |
| Cinema | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Project film building: adopt VP entertainment/media role with Boredom reduction 1; existing Film slots retained. |
| Cold Storage | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Project refrigeration/food-chain building: Health +2 provisional; current Food/storage role retained. |
| Food Market | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Food-distribution building: Health +1 provisional; current Food output retained. |
| Hospital | Industrial | VP_EXACT_ADOPTED | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | VP verified: Hospital Poverty reduction 1, heal +15, specialist-unhappiness relief and specialist yields. Project Health +4 provisional; BNW +5 Food retained. |
| Sewer | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | Project sanitation building: Health +4 provisional. Housing +2 retained; no unsupported direct VP counterpart forced. |
| Telegraph Office | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Factory | Industrial | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Factory +10 Production, +0.25 Production/pop, one Engineer slot and Manufactory +2 Production; existing project percent modifier retained. |
| Sanctuary | Industrial | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | Late conservation/religion-nature capstone: Religious Unrest reduction 1 added as VP-style role; natural-tile effects retained. |
| Apothecary | Late Antiquity | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Project Health building: Health +2 provisional; existing Food/Science retained. |
| Armory | Late Antiquity | VP_EXACT_ADOPTED | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | VP verified: Armory gives Supply +1, Distress reduction 1, +2 Science and 20 XP. |
| Garden | Late Antiquity | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified Garden keeps Great Person role and removes specialist unhappiness at 1-per-specialist scale; oasis Gold +2 added. |
| Temple | Late Antiquity | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | VP verified: Temple yields 3 Faith, Religious Unrest reduction 1, and +25% religious pressure. |
| Airport | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Existing BNW airlift/tourism role retained; no speculative Needs modifier added. |
| Radar Station | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Existing project air-defense values retained; no extra VP Needs value added. |
| Broadcast Center | Modern | VP_EXACT_ADOPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP verified Broadcast Tower analogue: Boredom -1, two music slots, +0.5 Culture and Tourism per population; old flat/percent Culture removed. |
| Aquatics Center | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Civ6 entertainment branch adapted to VP Needs: Boredom reduction 1; existing local Happiness retained. |
| Stadium | Modern | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Stadium direct Happiness removed; +20 city-state friendship, +50% Great Work Tourism and +0.5 Golden Age points/pop. |
| Medical Lab | Modern | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | VP verified: Medical Lab gives +2 population, 15% food kept and 50 Science per birth retroactively. Project Health +5 provisional. |
| National History Museum | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | Tier-3 national institutional choice: provisional Stability +2; Great Work role retained. |
| Royal Society | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| War Department | Modern | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Research Lab | Modern | VP_EXACT_ADOPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Research Lab +4 Science, Illiteracy reduction 1, Academy +4 Science and +33% Scientist generation; old +50% Science removed. |
| Bastion Walls | Renaissance | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP defense-line adaptation: +5% city military supply; existing defense/HP values retained. |
| Bank | Renaissance | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | VP verified: Bank +2 Gold, +3 local Gold from Caravansary/Mint analogues, and Science equal to 15% of Gold purchases; existing project percent Gold retained. |
| Art Museum | Exploration | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | VP Museum analogue: flat Boredom reduction 1 and 0.25 Culture/Tourism per population; applied to mutually exclusive museum branches. |
| Printing Press | Renaissance | PROJECT_VP_ADAPTED | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Project print infrastructure: Illiteracy reduction 1 added; writing slot and Culture retained. |
| Chancery | Renaissance | PROJECT_VP_ADAPTED | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Government/institution building: provisional Stability +1 added while existing unique effect is retained. |
| Constabulary | Renaissance | VP_EXACT_ADOPTED | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | VP espionage/Distress role adopted; Renaissance cost raised 160→220 to avoid an anomalously cheap late administrative building. |
| Arsenal | Renaissance | VP_EXACT_ADOPTED | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | VP verified: Arsenal +5% supply and +5 healing; defense values retained. |

## 아직 의도적으로 잠그지 않은 값

- Power Plant 계열의 실제 Power 생산량: 도시 전력 수요 단위가 아직 최종 확정되지 않아 기존 PENDING 유지.
- Health 수치: 이번 V2에서 상대적 단계값을 넣었지만 Health/질병 전역식과 함께 재보정해야 한다.
- Stability 수치: 정부교체 비용과 국가 Stability 범위가 확정된 뒤 절대값 재보정이 필요하다.
- 나머지 건물 Production Cost: 기술/사회제도 비용곡선 및 시대별 평균 도시 Production 확정 후 일괄 정규화한다.

## 공식 VP 확인 포인트

- PreBuildingChanges.sql: Building_YieldChanges, Building_YieldModifiers 등을 초기화하여 VP가 건물 산출을 전면 재구성함.
- BuildingChanges.sql: Needs, Supply, 문화, 과학, 상업, 군사, 방어, 해양 건물 수치를 확인.
- NewConceptText.xml: War Weariness, Military Supply, Local Happiness, Needs Threshold의 실제 작동 설명 확인.

## 상태

**102개 건물 전수감사 완료. V2 CSV는 구현 후보값이며, VP exact 항목과 project-provisional 항목을 명시적으로 분리했다.**
