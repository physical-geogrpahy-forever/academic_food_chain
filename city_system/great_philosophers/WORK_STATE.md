# Great Philosopher Work State

Date: 2026-09-22
Status: FIRST-PASS HISTORICAL EFFECT QA COMPLETE

## System

- Class: Great Philosopher / 위대한 철학가
- No dedicated Philosopher specialist.
- GPhP comes from institutional diversity.
- Five thought chains: knowledge, religion/nature, culture/media, government/diplomacy, commerce/trade.
- City GPhP per turn = max(0, active thought chains - 1).
- Same-chain buildings do not stack for GPhP.
- Recruitment uses globally unique named candidates with retained overflow.

## Roster

- broad candidate pool: 228
- active Philosopher roster: 227
- Great Writer priority: Rabindranath Tagore
- Laozi: HISTORICITY_REVIEW
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

## QA completed

Initial individual ability draft:
- 227 / 227

Second-pass historical/gameplay effect QA:
- rewritten in second pass: 131
- duplicate names: 0
- exact duplicate effects: 0
- normalized near-duplicate effects: 0
- later-era technology/civic/building references: 0
- Future references: 0

The second pass specifically reduced repeated patterns such as:
- Temple + University -> +1 Faith/+1 Science
- Public School + culture building -> +1 Science/+1 Culture
- Government building -> flat +Culture
- flat Science/Culture bursts without a historical mechanic

## Completed audits

- SCIENTIST_TO_PHILOSOPHER_TRANSFER_AUDIT_V1.md
- ACTIVITY_PERIOD_AUDIT_MASTER_V1.md
- CLASS_BOUNDARY_AUDIT_V1.md
- GREAT_PHILOSOPHER_CURRENT_SUMMARY.md

## Numerical balance screen

- POWER_BAND_AUDIT_V1.md completed.
- no obvious within-era outlier requires immediate retuning;
- final numerical tuning deferred until game-speed costs and GP recruitment thresholds are locked.

## Remaining work

1. final numerical power-band balance and game-speed scaling after global thresholds are defined;
2. decide Laozi historicity policy;
3. cross-class review after Writer/Prophet/Merchant rosters are locked;
4. implement GPhP generation in city logic;
5. later playtest whether institutional-diversity GPhP generation is too fast in large late-game empires.
