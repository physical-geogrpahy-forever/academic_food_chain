# Great Scientist longlist and ability design V1

Date: 2026-09-22
Status: DRAFT CONTENT PASS — PREMODERN QA1 APPLIED

## Purpose

This directory stores the expanded Great Scientist candidate pool and first-pass individual abilities.
Candidate count is deliberately not capped at 100. Era/region counts are not quota-balanced.

## Design rules

1. Keep the candidate pool broad first; prune only after other Great Person classes are also built.
2. Every named Scientist has an individual ability. Exact name-swapped copies should be rewritten during QA.
3. Abilities use the project's existing systems wherever possible: technology progress/Eureka, city science buildings, specialists/GPP, tile improvements/resources, Health/Plague, trade routes, power, archaeology and space projects.
4. Avoid vague map-reveal effects requiring bespoke area calculations unless a later implementation pass explicitly adopts them.
5. A Scientist must not depend on a building/system unavailable at recruitment. A condition marked `researchable` means the named technology can legally be researched; it need not already be completed.
6. Flat Science/Production values are Standard-speed draft numbers and scale with game speed.
7. CROSS_CLASS_REVIEW keeps ambiguous figures until Engineer/Merchant/Writer/Prophet/etc. rosters exist for final de-duplication.
8. Civ VI provides the named-person/individual-ability principle, not a mandatory ability template.

## Current counts after Premodern QA1

| Project era | Candidates |
|---|---:|
| Ancient | 5 |
| Classical | 22 |
| Late Antiquity | 13 |
| Early Medieval | 17 |
| High Medieval | 18 |
| Renaissance | 7 |
| Exploration | 37 |
| Enlightenment | 29 |
| Industrial | 47 |
| Modern | 50 |
| Atomic | 64 |
| Information | 23 |
| Future | 0 |
| **Total** | **332** |

## Premodern QA1 changes

- Moved Ptolemy, Galen, Diophantus, Liu Hui, Zhang Zhongjing, Wang Fan and Hua Tuo from Late Antiquity to Classical.
- Added Theon of Alexandria, Marinus of Neapolis, John Philoponus, Anthemius of Tralles, Aëtius of Amida, Alexander of Tralles and Boethius to Late Antiquity.
- Moved Madhava of Sangamagrama, Ibn al-Shatir and Ibn Khaldun from High Medieval to Renaissance.
- Rewrote affected abilities so moved candidates do not require buildings that belong to a later era.
- Preserved boundary cases such as Kamal al-Din al-Farisi and Guo Shoujing for a later exact boundary-policy pass.

## Files

- GREAT_SCIENTIST_ANCIENT_V1.md
- GREAT_SCIENTIST_CLASSICAL_V1.md
- GREAT_SCIENTIST_LATE_ANTIQUITY_V1.md
- GREAT_SCIENTIST_EARLY_MEDIEVAL_V1.md
- GREAT_SCIENTIST_HIGH_MEDIEVAL_V1.md
- GREAT_SCIENTIST_RENAISSANCE_V1.md
- GREAT_SCIENTIST_EXPLORATION_V1.md
- GREAT_SCIENTIST_ENLIGHTENMENT_V1.md
- GREAT_SCIENTIST_INDUSTRIAL_V1.md
- GREAT_SCIENTIST_MODERN_V1.md
- GREAT_SCIENTIST_ATOMIC_V1.md
- GREAT_SCIENTIST_INFORMATION_V1.md
- GREAT_SCIENTIST_FUTURE_V1.md
- PREMODERN_QA1.md

## Next QA passes

- Early Medieval ability-overlap cleanup
- Exploration/Enlightenment candidate expansion and ability-overlap QA2: APPLIED
- Industrial/Modern ability-overlap and candidate QA3: APPLIED
- Atomic QA4: APPLIED
- Information QA5: APPLIED
- Future historical-person roster removed; 5 candidates reassigned by activity period
- cross-class duplicate check after Engineer/Merchant/etc. rosters
- exact numerical balance after game-speed scaling is defined


## Activity-period full audit status

Completed audit files:
- ACTIVITY_PERIOD_AUDIT_01_PREMODERN.md
- ACTIVITY_PERIOD_AUDIT_02_EARLY_MODERN.md
- ACTIVITY_PERIOD_AUDIT_03_INDUSTRIAL_MODERN.md
- ACTIVITY_PERIOD_AUDIT_04_LATE_MODERN.md

The actual roster files are now only **partially reconciled** to these audits. Future has been fully reconciled. The remaining era-to-era moves should follow the activity-period audit rather than technology-gate convenience.

Target counts after full reconciliation:
- Ancient 5
- Classical 22
- Late Antiquity 13
- Early Medieval 17
- High Medieval 18
- Renaissance 7
- Exploration 37
- Enlightenment 29
- Industrial 47
- Modern 50
- Atomic 64
- Information 23
- Future 0
- Total 332


## Full activity and effect QA status

Completed on 2026-09-22:

- 332 historical Great Scientists audited by principal activity period.
- Era placement reconciled across all roster files.
- Historical-person Future roster removed; Future remains a gameplay/technology era only.
- First-pass individual effect QA completed for all 332 candidates.
- Final validation:
  - total roster rows: 332
  - duplicate names: 0
  - exact duplicate effects: 0
  - normalized/near-exact duplicate effect groups: 0
  - later-era technology/building references: 0
  - Future-technology references in historical Scientist abilities: 0

The remaining work is numerical balance and eventual cross-class review against Engineers, Merchants, Writers and other Great Person rosters.
