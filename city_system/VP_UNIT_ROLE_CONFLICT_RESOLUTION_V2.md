# VP Unit Role Conflict Resolution V2

Date: 2026-09-23
Status: SECOND-PASS ROLE RESOLUTION

This document resolves the four `ROLE_CONFLICT_REVIEW` cases left by `FINAL_UNIT_NUMERIC_BALANCE_V2_VP_AUDIT.csv`.

## Rule

Vox Populi remains the default combat-system reference, but a VP class reassignment is not copied when it would erase a role that the project explicitly needs. The project keeps a larger Civ V/Civ VI hybrid roster, so role coverage is checked before adopting the VP class identity.

## 1. Cavalry

Decision: **ADOPT VP ROLE**

- Project old role: `LIGHT_CAVALRY`
- New role: `MOUNTED_SKIRMISHER`
- Provisional combat: 40
- Provisional ranged combat: 31
- Range: 1
- Moves: 5

Reason:
- A pure melee Cavalry overlaps too strongly with the existing mounted shock/heavy-cavalry line.
- VP gives the firearm-era Cavalry a distinct mobile-fire role.
- This creates a useful historical/mechanical bridge from horse-mounted ranged/mobile combat to the later attack-helicopter gunship role.

This is a role lock, not a final Production-cost lock.

## 2. Anti-Tank Gun

Decision: **KEEP PROJECT ROLE**

- Final role: `ANTI_ARMOR`
- Provisional combat: 50
- Range: 0
- Moves: 2

Reason:
- VP repurposes the underlying class as a fast ranged/skirmisher unit.
- Our game already has mounted/skirmisher and armored lines.
- Removing a dedicated anti-armor counter would weaken combined-arms counterplay.
- Therefore VP's class reassignment is intentionally overridden here.

The final anti-armor combat modifier remains to be tuned with Tank and Modern Armor values.

## 3. Helicopter

Decision: **ADOPT VP ROLE**

- Project old role: `LIGHT_CAVALRY`
- New role: `MOUNTED_SKIRMISHER`
- Provisional combat: 70
- Provisional ranged combat: 70
- Range: 1
- Moves: 6

Reason:
- An attack helicopter is poorly represented as a melee cavalry unit.
- VP's range-1 gunship model better captures stand-off fire while retaining high mobility.
- It also provides a late upgrade endpoint for the mobile mounted-skirmisher family.

## 4. Aircraft Carrier

Decision: **KEEP PROJECT PLATFORM ROLE, ADOPT VP-ERA DEFENSE ONLY**

- Final role: `NAVAL_CARRIER`
- Provisional defensive combat: 70
- Ranged combat: none
- Range: 0
- Moves: 5
- Base air cargo: 2

Reason:
- VP gives the Carrier an organic ranged attack.
- In this project the carrier's offensive arm is the aircraft it carries.
- Giving the hull a strong independent ranged attack would double-count its offensive function.
- VP-era defensive strength is useful, but the platform identity is retained.

Flight Deck promotions or later carrier upgrades may expand cargo separately.

## Role-family consequences

Provisional family structure after this pass:

- `MOUNTED_SKIRMISHER`: Chariot Archer-style early mobile ranged units -> Cavalry -> Helicopter
- `HEAVY_CAVALRY / SHOCK`: Knight -> Lancer and any later shock-cavalry remnant
- `ANTI_ARMOR`: Anti-Tank Gun -> Modern AT
- `NAVAL_CARRIER`: Aircraft Carrier and later carrier variants, with aircraft rather than hull guns as the main offensive payload

The exact direct upgrade edges are not locked by this document. Only role identity is locked.

## Remaining numeric work

Still deferred:

- Production costs under the new 13-era cost curve
- Anti-armor bonus percentages
- carrier aircraft capacity progression
- upgrade Gold costs
- strategic-resource upkeep
- promotion-tree interaction

These are tuned after the tech/civic cost curve and full VP unit-cost sweep are synchronized.
