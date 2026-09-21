# 2026 canonical 45-day poll layer

- Frozen information cutoff: 2026-09-19 U.S. calendar date.
- This reproduces the weighting rule used by the canonical 98/99 production path.
- Poll values come from the already frozen RCP snapshot; audited external sources supply sample sizes and actual field-end dates.
- Window: 30 days before the 45-day snapshot.
- Recency half-life: 14 days.
- Per-poll weight: 2^(-age/14) * sqrt(clamp(sample_size,100,5000)/600).
- Effective poll count: (sum(w))^2 / sum(w^2).
- Downstream locked poll-blend weight is stored for audit as 0.75*n_eff/(n_eff+0.5).
- This artifact is the poll input layer only. It does not combine polls with fundamentals and does not emit election-outcome directions or probabilities.

## Integrity checks

- frozen rows: 42
- audited rows: 42
- states: 9
- unmatched frozen rows: 0

## Outputs

- data/snapshots/2026_poll_45d_canonical_weight_detail.csv
- data/snapshots/2026_poll_45d_canonical_sample_weighted.csv
- data/snapshots/2026_poll_sample_size_audit.csv
