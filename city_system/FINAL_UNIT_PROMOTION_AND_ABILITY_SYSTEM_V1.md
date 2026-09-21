# Final Unit Promotion and Innate Ability System V1

Date: 2026-09-21  
Status: **LOCKED V1**

Authorities:
- `city_system/FINAL_UNIT_PROMOTION_SYSTEM_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_PROFILE_ASSIGNMENT_V1.csv`
- `city_system/FINAL_UNIT_INNATE_ABILITIES_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_INHERITANCE_V1.csv`

## 1. Design principle

The project separates three concepts that are often mixed together:

1. **base numeric stats**
   - Combat
   - Ranged Combat
   - Movement
   - Range
   - Production

2. **innate unit/class abilities**
   - anti-cavalry bonus
   - siege bonus vs cities
   - must set up
   - submarine stealth
   - support aura
   - paradrop capability

3. **earned promotions**
   - Shock / Drill
   - Accuracy / Barrage
   - Targeting / Bombardment
   - Wolfpack
   - Interception / Dogfighting
   - and their advanced unlocks

An upgrade always receives the successor's innate abilities.
Earned promotions are retained only according to the promotion-inheritance rules.

## 2. Promotion profiles

Every one of the 89 generic units has exactly one profile.

Profiles:
- LAND_MELEE
- LAND_RANGED
- RECON
- NAVAL_MELEE
- NAVAL_RANGED
- NAVAL_RAIDER
- CARRIER
- AIR_FIGHTER
- AIR_BOMBER
- NONE

Current assignment counts:
- LAND_MELEE: 27
- LAND_RANGED: 13
- RECON: 4
- NAVAL_MELEE: 6
- NAVAL_RANGED: 7
- NAVAL_RAIDER: 2
- CARRIER: 1
- AIR_FIGHTER: 3
- AIR_BOMBER: 3
- NONE: 23

Privateer is the intentional exception:
although its canonical project role is NAVAL_RAIDER, it uses the **NAVAL_MELEE** promotion profile while it is a surface raider.

## 3. Land melee promotion structure

Primary branch A:
- Shock I: +15% in open terrain
- Shock II: +15%
- Shock III: +15%

Primary branch B:
- Drill I: +15% in rough terrain
- Drill II: +15%
- Drill III: +15%

Advanced promotions include:
- Cover I / II: +33% ranged defense each
- Charge: +33% vs wounded
- Formation I / II: +33% vs mounted each
- Ambush I / II: +33% vs armor each
- March: heal every turn
- Blitz: +1 attack
- Woodsman: double Forest/Jungle movement
- Repair for armored/GDR: heal every turn

The two-branch terrain specialization and advanced promotions follow Civ V BNW.

## 4. Land ranged and siege promotion structure

Primary branches:
- Accuracy I / II / III: +15% ranged strength in open terrain each
- Barrage I / II / III: +15% ranged strength in rough terrain each

Advanced:
- Volley: +50% vs fortified units and cities
- Logistics: +1 attack
- Range: +1 Range
- Cover: ranged defense
- March where applicable

These promotion choices are separate from the siege class's innate +200% city attack.

## 5. Recon

Two main branches:

Scouting:
- Scouting I: +1 Sight
- Scouting II: +1 Sight
- Scouting III: +1 Movement

Survivalism:
- Survivalism I: +5 HP healing outside friendly territory and +25% Defense
- Survivalism II: another +5 HP and +25% Defense
- Survivalism III: always heal plus melee-withdraw behavior

This profile follows the Civ V recon identity and is used by:
Scout -> Explorer -> Ranger -> Spec Ops.

## 6. Naval melee

Coastal Raider:
- I: +20% city attack, Gold equal to 33% of damage
- II: same
- III: +20%, Gold equal to 34% of damage

Boarding Party:
- I / II / III: +15% melee strength vs naval units each

Advanced naval utility:
- Supply
- Mobility
- Logistics

## 7. Naval ranged

Targeting:
- I / II / III: +15% vs naval units each

Bombardment:
- I: +33% vs land
- II: +33%
- III: +34%

Advanced:
- Range +1
- Supply
- Mobility
- Logistics

## 8. Naval raider

Submarine promotion branch:
- Wolfpack I: +25% when attacking
- Wolfpack II: +25%
- Wolfpack III: +25%

Privateer does not use the submarine Wolfpack profile before upgrade.

## 9. Carrier

Aircraft Carrier uses its own Flight Deck profile:
- Flight Deck I: +1 air cargo
- Flight Deck II: +1
- Flight Deck III: +1

Base cargo capacity is 2 in the numeric table; Flight Deck I/II/III raise it to 3/4/5.

## 10. Fighters

Interception:
- I: +33% interception strength
- II: +33%
- III: +34%

Dogfighting:
- I: +33% air-sweep strength
- II: +33%
- III: +34%

Advanced:
- Sortie: +1 interception
- Range: +2 operational range
- Logistics: +1 attack

## 11. Bombers

Siege:
- I / II / III: +33 / +33 / +34% vs cities

Bombardment:
- I / II / III: +33 / +33 / +34% vs land targets

Advanced:
- Evasion: interception damage -50%
- Range: +2 operational range
- Logistics: +1 attack

Stealth Bomber separately has its innate 100% Evasion baseline from Civ V.

## 12. Innate anti-class rules

Premodern anti-cavalry:
- Spearman
- Pikeman
- Pike and Shot
-> +50% vs mounted classes

Modern anti-armor:
- Anti-Tank Gun
- Modern AT
-> +100% vs ARMORED

Helicopter:
- +100% vs ARMORED
- ignores ordinary terrain costs
- no defensive terrain bonus
- cannot capture cities

These innate counters do not consume promotion choices.

## 13. Mounted and armored identity

Horseman / Knight / Lancer / Cavalry:
- can move after attacking
- no defensive terrain bonus
- -33% attack strength vs cities

Lancer additionally begins with Formation I.

Landship / Tank / Modern Armor:
- can move after attacking
- no defensive terrain bonus

GDR can move after attacking and then receives separate Future modules.

## 14. Siege identity

All SIEGE units:
- may not initiate melee attack
- +200% vs cities
- no defensive terrain bonus
- limited sight

Must set up before firing:
- Catapult
- Trebuchet
- Bombard
- Field Gun
- Artillery

Indirect Fire:
- Artillery
- Rocket Artillery

Rocket Artillery:
- does **not** need to set up before firing

This preserves the Civ V tactical transition where Rocket Artillery becomes much more mobile.

## 15. Naval special rules

Submarine / Nuclear Submarine:
- invisible except to adjacent/detection-capable units
- may enter Ice
- may not melee attack
- cannot attack cities
- +75% attack strength

Destroyer / Missile Cruiser:
- reveal submarines
- +100% vs submarines

Privateer:
- starts with Coastal Raider I
- Prize Ships while it remains a Privateer

Aircraft Carrier:
- cannot initiate attacks
- Combat value is defensive
- base air capacity 2

Nuclear Submarine:
- missile cargo 2

Missile Cruiser:
- missile cargo 3

## 16. Support-unit abilities

Battering Ram:
- adjacent melee and anti-cavalry units deal full damage to Ancient Walls

Siege Tower:
- adjacent melee and anti-cavalry units ignore Ancient and Medieval Walls when attacking the city itself

Medic:
- stationary adjacent units heal +20 HP/turn

Supply Convoy:
- stationary adjacent units heal +20 HP/turn
- adjacent units gain +1 Movement at turn start

Observation Balloon:
- adjacent siege units +1 Range

Drone:
- adjacent siege units +1 Range
- adjacent siege units +5 Ranged Strength

Support auras of the same kind do not stack.

## 17. Upgrade promotion inheritance

Default:
**retain an earned promotion if the successor remains eligible for it.**

### Chariot Archer -> Knight

The class changes from ranged cavalry to melee heavy cavalry.

Conversion:
- Accuracy I/II/III -> Shock I/II/III
- Barrage I/II/III -> Drill I/II/III
- Logistics -> Blitz
- Range -> Mobility

This preserves the value of veteran experience instead of leaving dead ranged promotions on a melee Knight.

### Privateer -> Submarine

Surface-raider promotions cannot remain literally.

Highest earned rank among:
- Coastal Raider
- Boarding Party

converts into the corresponding:
- Wolfpack I / II / III

Prize Ships is lost.

Generic naval utility promotions such as Supply / Mobility / Logistics remain when eligible.

### Support upgrades

Battering Ram / Siege Tower / Medic / Supply Convoy and Observation Balloon / Drone do not use ordinary combat-promotion conversion.

## 18. GDR

GDR remains the same unit and does not upgrade into another class.

It also **does not earn ordinary XP or promotions**. Its promotion profile is `NONE`.

Future modules:
- Advanced AI -> Drone Air Defense: anti-air defense strength 130
- Advanced Power Cells -> Particle Beam Siege Cannon: city/defense ranged strength 130 and full effectiveness
- Cybernetics -> Enhanced Mobility: movement 5 -> 8 plus Mountain Jump
- Smart Materials -> Reinforced Armor Plating: +10 defense vs land/naval attacks

Additional Gathering Storm identity retained:
- may move/fight on Coast/Ocean without ordinary embarkation
- heals only in friendly territory

Authority:
- `city_system/FINAL_GDR_MODULE_BALANCE_V1.csv`

## 19. What remains after V1

Still to lock numerically:
- Prize Ships conversion probability
- support aura interaction with stacked/formation units
- promotion XP thresholds if the project deviates from Civ V
- exact cargo eligibility by aircraft/missile type

The existence, profile ownership, promotion effects, core innate abilities and upgrade-inheritance logic are now locked.


## 20. Air combat V1 — LOCKED

Authorities:
- `city_system/FINAL_AIR_INTERCEPTION_UNIT_RULES_V1.csv`
- `city_system/FINAL_AIR_COMBAT_GLOBAL_RULES_V1.csv`

Interception chances:
- Triplane 50%
- Fighter 100%
- Jet Fighter 100%
- Anti-Air Gun 100%
- Mobile SAM 100%
- Destroyer 40%
- Missile Cruiser 100%
- GDR after Drone Air Defense: project-adapted 100%, AA strength 130

Resolution:
1. check target aircraft's innate evasion chance;
2. if not evaded, check interceptor chance;
3. only one interceptor resolves each air attack;
4. each interceptor normally intercepts once per turn;
5. Sortie grants fighters one additional interception.

Air Sweep:
- fighter-only;
- deliberately consumes one enemy interception;
- fighter-vs-fighter becomes a dogfight;
- surface interceptors inflict reduced damage during a sweep, but V1 does not invent an unsupported fixed percentage.

Innate 100% evasion:
- Stealth Bomber
- Guided Missile

Earned Evasion promotion:
- interception damage -50%, not +50% evasion chance.

Fighters:
- normal ground/naval air strike strength -50%
- +150% vs bombers and helicopters
- Air Recon radius 6

Anti-Air Gun / Mobile SAM:
- +150% vs aircraft and helicopters.
