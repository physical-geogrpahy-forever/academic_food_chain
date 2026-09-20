# Recovery status — 2026-09-21

## What is definitely preserved

1. Core V2 formula and design philosophy.
2. `RelativeEconomicGrowth` is a required existing Core term, not a new or replacement variable.
3. Candidate quality is split into Senate, Governor, and House experience.
4. Personal vote, incumbency, same-seat effect, and candidate experience receive Era interactions/shrinkage.
5. Poll layer uses `w_max=0.75`, `k=0.5`.
6. Modern midterm benchmark: RMSE 7.85%p, MAE 5.79%p, direction 91.9%.
7. Direct regional residual correction failed OOS and must not be reused.
8. Regional structure belongs in correlated uncertainty.
9. Historical validation coverage and 2026 production freshness are tracked separately.

## What is not currently recovered

- exact historical design matrix used to obtain 7.85%p
- exact per-race OOS predictions
- exact per-race residual CSV
- exact coefficient-by-cycle CSV
- exact poll snapshot file
- exact Core V2 config implementation
- any later changes that existed only in messages lost to chat-length truncation

## Naming rule

Until exact reproduction succeeds, reconstructed code/results are named `Core V2-R`.

Do not silently overwrite the historical `Core V2` label.
