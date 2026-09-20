# Poll-blend oracle headroom audit

- Generated UTC: 2026-09-20T18:09:33.570214+00:00
- This is diagnostic only. Outer 2014/2018/2022 outcomes are used to measure theoretical headroom, so these parameters are NOT eligible for adoption.
- Purpose: determine whether the current poll-blend functional form can ever exceed the 94/99 fixed benchmark.

## Oracle maximum

- Maximum correct within the searched poll-blend family: 94/99 = 94.9%.
- Oracle-best parameters: window=7, half-life=3, w_max=0.75, k=0.5.

## Per-cycle oracle maxima

- 2014: 32/33 with (7, 3, 0.6, 0.01)
- 2018: 31/33 with (14, 3, 1.25, 0.01)
- 2022: 33/33 with (7, 3, 0.4, 0.01)

## Correctness changes vs fixed 94/99 blend


## Interpretation

If the oracle maximum is still 94/99, further poll-weight tuning has no structural headroom. If it is higher, the next task is to find a leakage-free training rule that selects a similar regime, not to adopt the oracle parameters themselves.

## Outputs

- experiments/oracle_poll_headroom/results/oracle_top50.csv
- experiments/oracle_poll_headroom/results/oracle_cycle_max.csv
- experiments/oracle_poll_headroom/results/oracle_best_changes.csv
