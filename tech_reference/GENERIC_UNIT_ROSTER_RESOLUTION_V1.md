# Generic Unit Roster Resolution V1

Date: 2026-09-21

## Resolved deferred baseline units

| Item | Final decision | Gate |
|---|---|---|
| Heavy Chariot | DROP as separate generic unit | Civ6 checked; retain Civ5-style Chariot Archer + Horseman structure |
| Ranger | KEEP | Rifling |
| Submarine | KEEP | Electricity |
| Spec Ops | KEEP | Radar + Rapid Deployment |
| Nuclear Missile | DROP as separate unit | use Nuclear/Thermonuclear Devices + Missile Silo/delivery platforms |

## Recon progression

Scout -> Explorer -> Ranger -> Spec Ops

Ranger is adopted from Civ6 at Rifling.
Spec Ops remains a later recon/special-operations upgrade under Radar + Rapid Deployment.

## Submarine progression

Electricity -> Submarine
Nuclear Fission + Cold War -> Nuclear Submarine

## Nuclear delivery

No standalone generic Nuclear Missile unit.

Use the Civ6-style strategic device model:
- Nuclear Fission + Nuclear Program -> Nuclear Device
- Nuclear Fusion + Nuclear Program -> Thermonuclear Device
- Guidance Systems + Nuclear Program -> Missile Silo
- eligible air/naval delivery platforms may also deliver devices if the final combat rules allow it.

## Optional endgame units

Giant Death Robot and its four future upgrades are not baseline units.
They remain in the **OPTIONAL_ENDGAME** queue and do not block the generic unit roster.


## Final consolidation status — 2026-09-21

The generic unit existence/gate roster is now consolidated at:

- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1.md`
- `city_system/FINAL_GENERIC_UNIT_ROSTER_V1_QA.md`

Current baseline:
- 85 generic non-Great-Person units
- 73 technology-master units
- 7 civic-only/civic-owned units
- 5 recovered game-start/religion-system units
- GitHub Actions QA: PASS

The consolidation also recovered two audit-to-master omissions:
- Mechanized Infantry -> Combined Arms
- Missile Cruiser -> Guidance Systems + Warships

Great People remain separate. Giant Death Robot remains optional. Nuclear Missile remains replaced by the strategic-device delivery model.
