# Great Scientist longlist and ability design V1

Date: 2026-09-22
Status: DRAFT CONTENT PASS

## Purpose

This directory stores the expanded Great Scientist candidate pool and first-pass individual abilities.
Candidate count is deliberately not capped at 100. Era/region counts are not quota-balanced.

## Design rules

1. Keep the candidate pool broad first; prune only after other Great Person classes are also built.
2. Every named Scientist has an individual ability. Exact duplicate effect strings are prohibited in V1.
3. Abilities use the project's existing systems wherever possible: technology progress/Eureka, Library/University/Observatory/Public School/Research Lab, specialists/GPP, tile improvements/resources, Health/Plague, trade routes, power, archaeology and space projects.
4. Do not use vague map-reveal effects that require difficult bespoke area calculations unless a later implementation pass explicitly adopts them.
5. A Scientist does not require a building or technology that does not yet exist at recruitment. MIN_CONDITION gates entry to the eligible candidate pool.
6. Flat Science/Production values are Standard-speed draft numbers and scale with game speed.
7. CROSS_CLASS_REVIEW means the person remains in the Scientist longlist now but must be resolved against Engineer/Merchant/Writer/Prophet/etc. after those rosters exist.

## Civ VI reference principle

Civ VI is used for the principle that named Great People have individual historically grounded abilities, not as a template that must be copied. The project is Civ V city/specialist based and may use permanent specialists, city buildings, Health/Plague, trade, resources and other project systems in ways Civ VI does not.

## Counts

| Project era | Candidates |
|---|---:|
| Ancient | 7 |
| Classical | 13 |
| Late Antiquity | 13 |
| Early Medieval | 17 |
| High Medieval | 22 |
| Renaissance | 10 |
| Exploration | 30 |
| Enlightenment | 19 |
| Industrial | 46 |
| Modern | 32 |
| Atomic | 37 |
| Information | 28 |
| Future | 5 |
| **Total** | **279** |

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

## Next QA pass

- historical active-period/era check
- cross-class duplicate check after Engineer/Merchant/etc. rosters
- ability power-band comparison within each project era
- implementation audit against the locked 109-tech tree and final building roster
- exact numerical balance after game-speed scaling is defined
