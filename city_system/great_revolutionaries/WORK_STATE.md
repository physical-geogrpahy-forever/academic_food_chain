# Great Revolutionary Work State

Date: 2026-09-25
Status: SYSTEM V2 QUANTITATIVE RULES LOCKED — HISTORICAL ROSTER PAUSED PENDING CIVILIZATION / LEADER SELECTION

## Current project decision

Great Revolutionary roster work is intentionally paused before final historical selection.

Reason:
- some historically central revolutionaries are also natural civilization-leader candidates;
- excluding them merely because they may become leaders would remove figures such as George Washington, Oliver Cromwell or Vladimir Lenin from the Revolutionary system;
- the project will therefore choose civilizations and their historical leaders first, then return to Great Revolutionary roster construction.

Required work order from this point:

1. select the civilizations / historical successor states represented by the game;
2. assign their eligible leaders by era and historical context;
3. return to Great Revolutionary candidates;
4. determine which revolutionaries are `REVOLUTIONARY_ONLY` and which may transition into a civilization leader;
5. connect Revolutionary use to independence, regime change, successor-state creation and leader assignment;
6. only then lock the historical Great Revolutionary roster and individual abilities.

The existing Exploration and Enlightenment candidate research remains reference material. It is not a final roster.

## Leader overlap: revised direction

The previous assumption that a civilization leader and a Great Revolutionary should normally be mutually exclusive is no longer valid as a design rule.

Current direction to formalize after civilization/leader selection:

```text
Great Revolutionary appears
-> revolutionary / independence / regime-change action succeeds
-> new civilization or successor state is created when applicable
-> if that Revolutionary is the linked historical leader,
   the same historical person becomes leader of the resulting political entity
```

This avoids duplicate simultaneous instances of the same historical person while allowing one person to occupy two sequential gameplay roles:

```text
Great Revolutionary -> Civilization Leader
```

Provisional role labels for the later design pass:

- `REVOLUTIONARY_ONLY`
- `REVOLUTIONARY_TO_LEADER`
- `LEADER_ONLY`

These labels are not yet a finalized data schema. They record the intended distinction for the later V3 design pass.

### Illustrative cases, not yet final roster locks

- George Washington (조지 워싱턴): an Enlightenment-era Revolutionary linked to American colonial independence could become the leader of the resulting United States if Washington is selected and his independence action succeeds.
- Oliver Cromwell (올리버 크롬웰): an Exploration-era English regime-change Revolutionary could become leader of the resulting Commonwealth / Protectorate path when that historical route is produced.
- Vladimir Lenin (블라디미르 레닌): a Modern-era Russian social/regime Revolutionary could become leader of a Soviet successor-state path when the relevant revolution succeeds.

Exact civilization identities, leader availability, historical successor mapping and alternative-history behavior must be decided in the civilization/leader work before these examples become locked content.

## Civilization dependency

Great Revolutionary candidate scoring will eventually need information that does not yet exist in a locked form:

- which civilizations are playable or dynamically emergent;
- which predecessor and successor political entities are represented;
- which leaders belong to each civilization and era;
- whether a revolution creates a new civilization, transforms the existing civilization, or begins a civil war;
- which historical Revolutionary is the preferred founding / successor leader for that transition;
- what happens when the player chooses a different eligible Revolutionary instead of the historical default.

Therefore final `LEADER_CONFLICT` filtering is suspended. Existing candidate files using `LEADER_CONFLICT` or similar labels should be interpreted as "requires civilization/leader review," not "exclude this person from Great Revolutionary."

## Locked system retained from V2

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

These V2 quantitative rules remain active unless the later civilization/successor-state design creates a direct contradiction.

## Anti-exploit rules retained

- Low Happiness alone never generates GReP.
- Ordinary voluntary government switching never generates GReP.
- Milestone GReP is one-time per persistent milestone ID.
- War Weariness threshold events are once per war state.
- Colonial and occupation recurring events use cooldowns.
- Successor-state formation does not reset GReP progression.
- Historical named candidates remain globally unique.

## Common ability families retained

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

These templates may later gain a successor-state / leader-transition effect when the selected Revolutionary is linked to an emergent civilization.

## Existing candidate research

Current research material includes:

- Exploration-era preliminary Revolutionary discussion and candidate work;
- `GREAT_REVOLUTIONARY_ENLIGHTENMENT_BROAD_CANDIDATES_V1.md`, currently a broad research pool rather than final selection.

Do not continue reducing these pools until the civilization and leader roster is available.

## Authority files

- `city_system/great_revolutionaries/GREAT_REVOLUTIONARY_SYSTEM_V2.md`
- `city_system/great_revolutionaries/GREP_EVENT_VALUES_V1.csv`
- `city_system/great_revolutionaries/GREP_RECRUITMENT_THRESHOLDS_V1.csv`
- `city_system/FINAL_GREAT_PERSON_RECRUITMENT_SYSTEM_V2.md`

Previous structural draft retained for provenance:
- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`

## Next task outside this subsystem

**Move to civilization selection and civilization-leader design.**

Great Revolutionary work resumes only after enough of the civilization/leader structure is fixed to determine historical state transitions and leader assignments.

## Remaining Great Revolutionary work after civilization / leader pass

1. revise Great Revolutionary V2 into a leader-transition-aware V3 design;
2. replace `LEADER_CONFLICT` exclusion logic with explicit Revolutionary-to-Leader transition rules;
3. build/revise historical candidate pools by era;
4. map candidates to possible predecessor/successor civilizations;
5. assign activity era and primary/secondary tags;
6. audit overlap with Great General, Great Philosopher and Great Writer;
7. audit the Great Philosopher roster for GReP-linked thinkers;
8. draft candidate-specific unique abilities;
9. run regional and era coverage audit without artificial quota balancing;
10. after State Stability numeric rules are finalized, validate Stability-shock templates;
11. implement political-unit GReP and state-transition hooks when the game runtime exists.
