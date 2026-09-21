# Final Unit Operational Rules V1

Date: 2026-09-21
Status: **LOCKED V1**

Authorities:
- `city_system/FINAL_UNIT_CARGO_BASING_RULES_V1.csv`
- `city_system/FINAL_PRIVATEER_PRIZE_SHIPS_V1.csv`
- `city_system/FINAL_SUPPORT_UNIT_OPERATION_RULES_V1.csv`
- `city_system/FINAL_UNIT_XP_PROGRESSION_V1.csv`

## 1. Air and missile basing

### City
Base air stacking capacity: **6**.

Eligible project units:
- Triplane
- Fighter
- Jet Fighter
- Great War Bomber
- Bomber
- Stealth Bomber
- Guided Missile

### Aircraft Carrier
Base aircraft capacity: **2**.

Flight Deck:
- Flight Deck I -> 3
- Flight Deck II -> 4
- Flight Deck III -> 5

Eligible:
- Triplane
- Fighter
- Jet Fighter
- Great War Bomber
- Bomber

Excluded:
- Stealth Bomber
- Guided Missile

This follows Civ V: carriers can base ordinary fighters/bombers, but not Stealth Bombers or missiles.

### Nuclear Submarine
Capacity: **2**
Eligible cargo: Guided Missile.

### Missile Cruiser
Capacity: **3**
Eligible cargo: Guided Missile.

Standalone Nuclear Missile remains excluded from the project roster. Any nuclear-payload delivery system must therefore use the project's later nuclear-device rules rather than silently adding a Nuclear Missile unit here.

## 2. Prize Ships

Privateer retains Civ V's Prize Ships ability while it remains a Privateer.

Trigger:
- Privateer deals lethal melee damage to an eligible enemy naval combat unit.

Chance:

`capture chance = min(80, 10 + int((attacker base combat / defender base combat) * 40))`

Constants:
- minimum chance: 10%
- maximum chance: 80%
- strength-ratio multiplier: 40

Examples:
- equal base strength -> 50%
- attacker 25 vs defender 20 -> 60%
- attacker 25 vs defender 30 -> 43%

On success:
- captured ship changes owner
- captured ship appears at **50 HP**
- captured ship keeps **no previous promotions**

Project-specific upgrade decision:
- Privateer -> Submarine
- Prize Ships is lost on this upgrade
- surface-raider promotion rank instead converts into Wolfpack rank according to the promotion inheritance table

## 3. Support formation and stacking

Support units use a dedicated SUPPORT formation slot.

Rule:
- one friendly SUPPORT-class unit may share a tile with one friendly land combat unit
- two SUPPORT units may not occupy the same support slot on one tile

This prevents support pieces from displacing the combat unit they are designed to assist.

### Aura stacking
For the same aura category:
- effects do **not** add
- use the strongest applicable value only

Different aura categories may coexist.

Examples:
- Medic + Supply Convoy healing does not become +40; use +20
- Balloon + Drone range does not become +2; use +1
- Drone's +1 Range and +5 Ranged Strength both apply because they are different categories
- Supply Convoy's +20 healing and +1 Movement both apply because they are different categories

## 4. Support abilities

Battering Ram:
- radius 1
- lets adjacent eligible melee/anti-cavalry attackers deal full damage to Ancient Walls

Siege Tower:
- radius 1
- lets adjacent eligible melee/anti-cavalry attackers bypass Ancient/Medieval Walls and damage city HP

Medic:
- radius 1
- +20 HP healing for adjacent friendly land combat units that did not move that turn

Supply Convoy:
- radius 1
- +20 HP healing for stationary adjacent friendly land combat units
- +1 Movement for friendly land combat units beginning their turn in the aura

Observation Balloon:
- radius 1
- adjacent SIEGE +1 Range

Drone:
- radius 1
- adjacent SIEGE +1 Range
- adjacent SIEGE +5 Ranged Strength

Military Engineer:
- no aura
- builds unlocked military infrastructure

## 5. XP progression

The project retains the Civ V cumulative XP curve.

Cumulative thresholds:
- Level 1: 0
- Level 2: 10
- Level 3: 30
- Level 4: 60
- Level 5: 100
- Level 6: 150
- Level 7: 210
- Level 8: 280
- Level 9: 360
- Level 10: 450

General formula:

`XP_required(level L) = 5 * (L - 1) * L`

Each new level gives the normal Civ V choice:
- take an eligible promotion
- or heal instantly for 50 HP

Units with no ordinary promotion profile do not use the standard promotion choice.

GDR specifically cannot gain ordinary XP/promotions.

## 6. Combat XP gains

Civ V baseline:

- initiate melee attack: +5 XP
- defend against melee attack: +4 XP
- initiate ranged attack: +2 XP
- defend against ranged attack: +2 XP
- initiate air attack: +4 XP
- defend against air attack: +2 XP
- initiate Air Sweep: +5 XP
- fighter defending Air Sweep: +5 XP
- ground/naval interceptor defending Air Sweep: +2 XP
- melee attack against city: +5 XP
- ranged attack against city: +3 XP
- air attack against city: +4 XP

Ranged/city attacks must actually inflict damage to grant attack XP.

## 7. Barbarian XP limit

A unit stops gaining further XP from Barbarian combat once it reaches **30 cumulative XP**.

This cap does not delete existing XP or promotions. It only blocks additional Barbarian-derived XP above that point.

## 8. What remains

This closes the generic military operational baseline except for systems that belong elsewhere:
- founding-unit economic pricing
- Faith price curves for Missionary/Inquisitor/Naturalist/Rock Band
- Spy acquisition/capacity economy
- nuclear-device delivery model
- Great General / Great Admiral aura and generation
- civilization-specific unique-unit exceptions
