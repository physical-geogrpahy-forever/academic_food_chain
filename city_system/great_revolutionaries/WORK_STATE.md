# Great Revolutionary Work State

Date: 2026-09-24
Status: SYSTEM V2 QUANTITATIVE RULES LOCKED — HISTORICAL ROSTER NOT YET BUILT

## Locked system

- Class: Great Revolutionary / 위대한 혁명가
- No generic Revolutionary specialist.
- GReP belongs to political units, including separate colonial-government pools.
- Recurring GReP requires Movement Capacity plus grievance.
- Structural-pressure check interval: 5 turns on Standard speed.
- Structural-pressure GReP: 4 / 6 / 8 for 1 / 2 / 3+ grievances.
- Discrete event values: `GREP_EVENT_VALUES_V1.csv`.
- Recruitment threshold progression: 100 / 120 / 140 / 160 / 180.
- Pool cap: 2x current threshold.
- Overflow retained.
- One unresolved Great Revolutionary per political unit.
- 15-turn recruitment cooldown after resolution.
- Colonial independence carries GReP pool, recruitment count and cooldown into the successor state.
- Candidate recruitment uses a context-filtered globally unique historical pool rather than one unconditional global queue.
- Up to three highest-scoring eligible candidates are shown.
- Default Great Revolutionary is a political-person entity, not a standard roaming civilian unit.
- Great Philosopher can feed GReP without changing class.

## Anti-exploit rules

- Low Happiness alone never generates GReP.
- Ordinary voluntary government switching never generates GReP.
- Milestone GReP is one-time per persistent milestone ID.
- War Weariness threshold events are once per war state.
- Colonial and occupation recurring events use cooldowns.
- Successor-state formation does not reset GReP progression.
- Historical named candidates remain globally unique.

## Common ability families

1. Regime change
2. Independence / anti-colonial
3. Social revolution
4. Revolutionary internationalism, candidate-specific only

Default regime-change template:
- government switch Culture cost -100%;
- transition duration x0.50, minimum 1 turn when applicable;
- government-switch Stability shock x0.50;
- one free policy reorganization.

Default independence template:
- independence decision immediately available;
- independence transition duration x0.50;
- initial independence Stability shock x0.50;
- one free post-independence policy reorganization.

## Authority files

- `city_system/great_revolutionaries/GREAT_REVOLUTIONARY_SYSTEM_V2.md`
- `city_system/great_revolutionaries/GREP_EVENT_VALUES_V1.csv`
- `city_system/great_revolutionaries/GREP_RECRUITMENT_THRESHOLDS_V1.csv`

Previous structural draft retained for provenance:
- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`

## Remaining work

1. Build broad historical Great Revolutionary candidate pool.
2. Assign activity era and primary/secondary tags.
3. Audit overlap with Great General, Great Philosopher and civilization leaders.
4. Audit the 220-person Great Philosopher roster for GReP-linked thinkers.
5. Draft candidate-specific unique abilities.
6. Run regional and era coverage audit without artificial quota balancing.
7. After State Stability numeric rules are finalized, validate the x0.50 Stability-shock templates against actual transition magnitudes.
8. Implement political-unit GReP state and event hooks when the game runtime exists.
