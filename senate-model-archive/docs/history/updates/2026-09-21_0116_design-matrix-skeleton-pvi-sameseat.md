# GitHub Actions run: Core V2-R design matrix skeleton

- Generated UTC: 2026-09-20T16:51:54.253203+00:00
- Execution: GitHub Actions
- Rows: 99

## Variables currently joined

- actual target margin: total-vote D-R and D/R two-party D-R versions
- direction_actual
- PVI reconstruction default: 0.67 recent presidential lean + 0.33 older presidential lean
- SameSeat exact 6-year same-class margin, both target denominator versions
- SameSeat exact-6 availability flag
- last-prior-same-class fields retained for audit only

## Validation

- PVI join coverage: 99/99
- SameSeat exact-6 missing: 8/99
- No regression or coefficient fitting has been performed yet.

## Important unresolved choices

1. Original Core V2 target margin denominator: total vote vs D/R two-party vote.
2. Original treatment of missing SameSeat values.
3. Exact PVI recent/older weights beyond the preserved 0.67/0.33 default.

These are retained as explicit reconstruction uncertainties rather than tuned against the 2014/2018/2022 test outcomes.

## Output

- data/processed/core_v2r_headline_design_matrix_skeleton.csv

## Next

Reconstruct candidate-level incumbency and Senate/Governor/House experience from pre-election information only, with a separate manual audit for appointments and party-aligned independents.
