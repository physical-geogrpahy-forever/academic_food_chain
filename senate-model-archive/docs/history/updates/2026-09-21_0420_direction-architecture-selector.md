# Direction-first fundamentals architecture selector

- Generated UTC: 2026-09-20T18:22:37.557443+00:00
- Candidate families: incumbency-era fundamentals and no-incumbency fundamentals.
- Both families are fitted only on cycles before the cycle being predicted and then receive the same fixed 45-day poll update.
- For each outer test cycle, family selection uses only winner-direction results from earlier cycles starting in 2010.
- Primary selector criterion: cumulative historical correct races. Tie-break: recent two-cycle correct count, then incumbency-era as the preserved default.

## Outer result

| scope | N | correct | wrong | accuracy |
|---|---:|---:|---:|---:|
| combined | 99 | 92 | 7 | 92.9% |
| 2014 | 33 | 30 | 3 | 90.9% |
| 2018 | 33 | 29 | 4 | 87.9% |
| 2022 | 33 | 33 | 0 | 100.0% |

## Architecture chosen before each outer cycle

| test | history cycles | chosen | incumbency correct/N | no-inc correct/N |
|---:|---|---|---:|---:|
| 2014 | 2010;2012 | no_incumbency | 56/68 | 57/68 |
| 2018 | 2010;2012;2014;2016 | incumbency_era | 117/133 | 115/133 |
| 2022 | 2010;2012;2014;2016;2018;2020 | incumbency_era | 175/198 | 174/198 |

## Historical family scores

| cycle | family | N | correct | accuracy |
|---:|---|---:|---:|---:|
| 2008 | incumbency_era | 28 | 24 | 85.7% |
| 2008 | no_incumbency | 28 | 24 | 85.7% |
| 2010 | incumbency_era | 35 | 27 | 77.1% |
| 2010 | no_incumbency | 35 | 29 | 82.9% |
| 2012 | incumbency_era | 33 | 29 | 87.9% |
| 2012 | no_incumbency | 33 | 28 | 84.8% |
| 2014 | incumbency_era | 33 | 32 | 97.0% |
| 2014 | no_incumbency | 33 | 30 | 90.9% |
| 2016 | incumbency_era | 32 | 29 | 90.6% |
| 2016 | no_incumbency | 32 | 28 | 87.5% |
| 2018 | incumbency_era | 33 | 29 | 87.9% |
| 2018 | no_incumbency | 33 | 30 | 90.9% |
| 2020 | incumbency_era | 32 | 29 | 90.6% |
| 2020 | no_incumbency | 32 | 29 | 90.6% |
| 2022 | incumbency_era | 33 | 33 | 100.0% |
| 2022 | no_incumbency | 33 | 32 | 97.0% |

## Remaining wrong races

- 2014 IA 26: family=no_incumbency, posterior=0.79, actual=-8.70
- 2014 ME 9: family=no_incumbency, posterior=1.01, actual=-36.98
- 2014 NC 14: family=no_incumbency, posterior=1.02, actual=-1.63
- 2018 NV 112: family=incumbency_era, posterior=-0.62, actual=5.25
- 2018 MO 109: family=incumbency_era, posterior=4.72, actual=-6.00
- 2018 FL 100: family=incumbency_era, posterior=9.21, actual=-0.12
- 2018 IN 102: family=incumbency_era, posterior=5.41, actual=-6.16

## Benchmark

- Fixed incumbency-era + poll benchmark: 94/99 = 94.9%.
- The selector is an improvement only if it exceeds 94/99 without using the target outer-cycle result in family selection.

## Outputs

- experiments/direction_architecture_selector/results/selector_summary.csv
- experiments/direction_architecture_selector/results/selector_choices.csv
- experiments/direction_architecture_selector/results/family_cycle_scores.csv
- experiments/direction_architecture_selector/results/selector_predictions.csv
