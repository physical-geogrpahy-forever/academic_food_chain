# CHANGELOG

## 2026-09-21 - Core V2-R 2026 production model locked

### Final validation
- accepted clean nested direction benchmark: **96/99 = 97.0%**
- the previous 94/99 fixed-poll baseline is superseded as the primary direction benchmark
- 2026 production selector is fit using historical information through 2022
- retrospective 98/99 is retained as a diagnostic only and is explicitly not OOS

### Frozen 2026 production selector
- poll-PVI disagree threshold: 2.0 percentage points
- poll-PVI agree threshold: 0.75 percentage points
- minimum absolute PVI when poll and PVI agree: 15 percentage points
- poll blend remains w_max=0.75, k=0.5, 30-day window, 14-day half-life

### Third-party policy
- no directional point correction from minor-party share
- third-party support is uncertainty-only until broader historical multi-candidate coverage exists
- major independent / party-replacement races are modeled separately from ordinary D/R races

### Governance
- production model is frozen in docs/final/MODEL_FINAL_LOCK_2026-09-21.md
- all future structural changes must use a new experimental version
- 2026 observed outcomes may not be used to retune the locked model

### 2026 analysis
- added neutral competitive-race input diagnostic snapshot
- exact poll-row cutoff audit and full production input matrix remain next

## 2026-09-21 - Recovery archive initialized

### Preserved
- Core V2 master handoff
- Core V2 2026 production data audit
- Core V2 headline benchmark
- regional residual summary
- poll blending hyperparameters
- Core V2 formula including `RelativeEconomicGrowth`
- 2026 production snapshot cutoffs

### Recovery findings
- ChatGPT Library search found only two duplicate master handoff copies, not the expected exact Core V2 output CSV/config artifacts.
- Connected GitHub search found no `core_v2`, `RelativeEconomicGrowth`, `7.85`, `SenateExperienceDiff`, or `poll_snapshot_45d` implementation/artifact in the user's currently accessible owned repositories.
- Therefore exact historical implementation is not claimed recovered.
- Any reconstruction from this point must be labeled `Core V2-R` until the preserved 7.85%p benchmark is independently reproduced.

### Snapshot correction
- 2026 election day = 2026-11-03.
- Exact 45-day cutoff = 2026-09-19.
- BEA Q2 release scheduled for 2026-09-30 cannot enter the 45-day snapshot.

### Next
- Build a reproducible Core V2-R dataset and code path from preserved definitions and historical sources.
