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
