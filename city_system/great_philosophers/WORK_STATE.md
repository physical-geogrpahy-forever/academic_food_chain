# Great Philosopher Work State

Date: 2026-09-22
Status: FIRST-PASS ROSTER AND ABILITY QA COMPLETE

## System

- Class name: Great Philosopher / 위대한 철학가
- No dedicated Philosopher specialist.
- City Great Philosopher Points come from institutional diversity.
- Five thought chains: knowledge, religion/nature, culture/media, government/diplomacy, commerce/trade.
- City GPhP per turn = max(0, active thought chains - 1).
- Same-chain buildings do not stack for GPhP.
- Recruitment uses globally unique named candidates and retained overflow.

## Current roster

- Broad candidate pool: 228
- Great Writer priority: Rabindranath Tagore
- Current ability roster: 227
- Laozi: historicity/textual-era review retained
- Future historical-person roster: 0

## Era counts

- Ancient: 5
- Classical: 23
- Late Antiquity: 12
- Early Medieval: 11
- High Medieval: 17
- Renaissance: 14
- Exploration: 29
- Enlightenment: 25
- Industrial: 19
- Modern: 24
- Atomic: 33
- Information: 15

## QA

- roster rows: 227
- duplicate names: 0
- exact duplicate effects: 0
- normalized near-duplicate effects: 0
- later-era technology/civic/building references: 0
- Future-tech references: 0

## Completed audits

- SCIENTIST_TO_PHILOSOPHER_TRANSFER_AUDIT_V1.md
- ACTIVITY_PERIOD_AUDIT_MASTER_V1.md
- CLASS_BOUNDARY_AUDIT_V1.md

## Remaining work

1. individual historical-effect refinement;
2. numerical balance and game-speed scaling;
3. Laozi historicity decision;
4. cross-class review after Writer/Prophet/Merchant rosters are finalized;
5. implementation of GPhP generation in city logic.
