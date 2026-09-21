# Final Unit Operational Rules V1 QA

Date: 2026-09-21
Status: **PASS — current repository structural validation**

Authorities:
- `city_system/FINAL_UNIT_CARGO_BASING_RULES_V1.csv`
- `city_system/FINAL_PRIVATEER_PRIZE_SHIPS_V1.csv`
- `city_system/FINAL_SUPPORT_UNIT_OPERATION_RULES_V1.csv`
- `city_system/FINAL_UNIT_XP_PROGRESSION_V1.csv`
- `city_system/validate_final_unit_operational_rules_v1.py`

Current result:
- cargo/basing rows: 4
- Prize Ships rows: 1
- support-operation rows: 9
- XP rules: 24
- Carrier base cargo mismatch: 0
- missile-platform cargo mismatch: 0
- Prize Ships constant/formula mismatch: 0
- support aura value/stacking mismatch: 0
- XP threshold/gain mismatch: 0
- result: **PASS**

Locked cargo:
- City air capacity 6
- Aircraft Carrier 2 aircraft, Flight Deck I/II/III -> 3/4/5
- Nuclear Submarine 2 Guided Missiles
- Missile Cruiser 3 Guided Missiles
- Carrier excludes Stealth Bomber and Guided Missile

Locked Prize Ships:
- chance = min(80, 10 + int((attacker base combat / defender base combat) * 40))
- minimum 10%
- maximum 80%
- captured unit 50 HP
- captured promotions none

Locked support stacking:
- one SUPPORT slot may share a tile with one friendly land combat unit
- same aura category uses strongest effect only
- different categories may coexist

Locked XP:
- level thresholds 10 / 30 / 60 / 100 / 150 / 210 / 280 / 360 / 450
- melee attack 5, melee defense 4
- ranged attack/defense 2
- air attack 4, air defense 2
- Air Sweep attacker/air defender 5, surface defender 2
- Barbarian XP cap 30
- level reward = promotion or heal 50 HP

No current GitHub Actions run ID is claimed until an actual completed run is retrieved.
