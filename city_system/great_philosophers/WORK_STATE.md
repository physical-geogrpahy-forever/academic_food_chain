# Great Philosopher Work State

Date: 2026-09-23
Status: FIRST-PASS HISTORICAL EFFECT QA COMPLETE — ROSTER REVISED

## System

- Class: Great Philosopher / 위대한 철학가
- No dedicated Philosopher specialist.
- GPhP comes from institutional diversity.
- Five thought chains: knowledge, religion/nature, culture/media, government/diplomacy, commerce/trade.
- City GPhP per turn = max(0, active thought chains - 1).
- Same-chain buildings do not stack for GPhP.
- Recruitment uses globally unique named candidates with retained overflow.

## Current roster

- broad research candidate pool: 228
- active Philosopher roster: **220**
- Great Writer priority: Rabindranath Tagore
- Laozi: HISTORICITY_REVIEW
- Future historical-person roster: 0

### Korean roster review 2026-09-23

Retained:
- Wonhyo (원효)
- Uisang (의상)
- Chinul (지눌)
- Jeong Do-jeon (정도전)
- Yi Hwang (이황)
- Yi I (이이)
- Jeong Je-du (정제두)
- Hong Dae-yong (홍대용)
- Park Ji-won (박지원)
- Jeong Yak-yong (정약용)
- Choe Han-gi (최한기)
- Ham Seok-heon (함석헌)
- Byung-Chul Han (한병철)

Removed from active roster:
- Yi Saek (이색)
- Jeong Mong-ju (정몽주)
- Kwon Geun (권근)
- Gihwa (기화)
- Seo Gyeong-deok (서경덕)
- Gi Dae-seung (기대승)
- Seong Hon (성혼)

Choe Han-gi correction:
- removed Telegraph / Telegraph Office dependency;
- Choe Han-gi died in 1877, before Korea's first operational telegraph line in 1885;
- current ability is tied to Scientific Theory, international knowledge exchange, empirical inquiry and global geography.

## Era counts

- Ancient: 5
- Classical: 23
- Late Antiquity: 12
- Early Medieval: 11
- High Medieval: 17
- Renaissance: 10
- Exploration: 26
- Enlightenment: 25
- Industrial: 19
- Modern: 24
- Atomic: 33
- Information: 15
- Total: **220**

## QA completed

Initial individual ability draft completed for the pre-review roster.

Second-pass historical/gameplay effect QA:
- duplicate names: 0 before the 2026-09-23 roster reduction
- exact duplicate effects: 0 before the 2026-09-23 roster reduction
- normalized near-duplicate effects: 0 before the 2026-09-23 roster reduction
- later-era technology/civic/building references: 0 before the Choe Han-gi historical correction
- Future references: 0

The 2026-09-23 removals cannot introduce duplicates. Choe Han-gi's anachronistic Telegraph dependency was removed.

## Completed audits

- SCIENTIST_TO_PHILOSOPHER_TRANSFER_AUDIT_V1.md
- ACTIVITY_PERIOD_AUDIT_MASTER_V1.md
- CLASS_BOUNDARY_AUDIT_V1.md
- POWER_BAND_AUDIT_V1.md

## Remaining work

1. regenerate the repository-wide consolidated summary from the 220-person era files;
2. final numerical power-band balance and game-speed scaling after global thresholds are defined;
3. decide Laozi historicity policy;
4. cross-class review after Writer/Prophet/Merchant rosters are locked;
5. implement GPhP generation in city logic;
6. later playtest whether institutional-diversity GPhP generation is too fast in large late-game empires.
