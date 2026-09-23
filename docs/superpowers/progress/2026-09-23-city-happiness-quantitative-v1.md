# SDD ledger — plan: docs/superpowers/plans/2026-09-23-city-happiness-quantitative-v1.md

Execution mode: native / inline
Branch: `civ-game-map-stage1b-etopo2022`
Spec: `docs/superpowers/specs/2026-09-23-city-happiness-quantitative-v1-design.md`

Pre-flight shared interfaces:
- Task 1 -> Task 2: `load_expectations`, `get_effective_expectations`, category names `basic/gold/science/culture`; consistent with spec.
- Task 2 -> Task 4: `calculate_city_happiness` structured breakdown; QA fields match plan and spec.
- Task 3 -> Task 5: real Building-master validator command and PASS summary; consistent.
- Tasks 1-4 -> Task 5: final CI runs the same four authoritative commands; consistent.

Ruling: The harness has GitHub connector access but no checked-out repository/worktree execution environment. Use the existing non-main feature branch as the isolated workspace and GitHub Actions as the command runner. This preserves RED/GREEN evidence but means test execution evidence comes from Actions rather than a local worktree. Cost if wrong: workflow latency and extra CI commits, not gameplay semantics.

Ruling: Create the City Happiness CI harness early, before Task 5, because it is required to observe TDD RED/GREEN in this connector-only environment. Task 5 will finalize its triggers and command set. Cost if wrong: CI configuration appears earlier in history than the plan's nominal task order; implementation interfaces are unchanged.

Task 1: complete. RED run 35861270501 failed exactly because `calculate_city_happiness_v1.py` did not exist. GREEN run 35861345013 passed after adding the 13-era expectation table and expectation loader/clamp implementation. Commits: e1544da, 5b8b781, b2830a2, 8a54fab.

Task 2: complete. RED run 35861499245 failed exactly because `calculate_city_happiness` was not implemented. GREEN run 35861622924 passed the full calculator suite covering scenarios A-H, zero population, invalid inputs and floating-point floor boundaries. Commits: 059fbc1, b4fa8bc.

Task 3: validator TDD complete, real-data repair pending final recheck. RED run 35861781749 failed because the validator file did not exist. Fixture GREEN was observed in run 35861856992. Real-master run 35861896284 then found a genuine defect: Smokehouse had blank `LOCAL_HAPPINESS`. A regression test was added; Building master run 35862030736 failed exactly on that assertion. The merge generator was fixed generically so every V3 ADD row starts with `LOCAL_HAPPINESS` and all five Needs reduction fields at zero. Building workflow run 35862138621 then passed every build/master validation step and generated commit dabe06f8. The Happiness validator still needs a fresh run against that regenerated master before Task 3 is marked complete.

Ruling for Task 4 scenario count: the plan requires `scenarios=12`, but its additional `relative clamp high/low` case duplicates approved design scenario G. Keep G as the high/low clamp test and add a distinct `religion inactive` scenario as the twelfth unique scenario. This is directly required by the spec's Religious Unrest behavior and adds coverage without changing gameplay rules.
