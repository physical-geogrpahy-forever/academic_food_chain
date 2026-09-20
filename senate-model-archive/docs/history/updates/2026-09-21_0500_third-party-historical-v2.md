# Historical third-party Senate polling effect v2

- Generated UTC: 2026-09-20T18:59:28.684587+00:00
- Cycles attempted: 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022.
- Window: 14 days ending at election minus 45 days.
- Source: archived Electoral-vote.com daily Senate poll tables.
- Major independents/party-replacement cases are separated from ordinary minor-third-party cases.

## Coverage

| cycle | snapshot | pages with Senate polls |
|---:|---|---:|
| 2006 | 2006-09-23 | 0 |
| 2008 | 2008-09-20 | 0 |
| 2010 | 2010-09-18 | 0 |
| 2012 | 2012-09-22 | 0 |
| 2014 | 2014-09-20 | 13 |
| 2016 | 2016-09-24 | 0 |
| 2018 | 2018-09-22 | 11 |
| 2020 | 2020-09-19 | 0 |
| 2022 | 2022-09-24 | 11 |

## Context summary

| context | N | direction accuracy | mean abs D-R error | mean signed error |
|---|---:|---:|---:|---:|
| two_party_or_under3 | 66 | 93.9% | 6.10 | -3.09 |
| minor_third_3_to_15 | 1 | 0.0% | 6.06 | -6.06 |
| major_independent_or_party_replacement | 4 | 100.0% | 65.22 | -25.22 |

## Minor-third-party race-cycles

- 2014 NC: third poll=5.60, actual third=3.78, poll D-R=4.43, actual D-R=-1.63, error=-6.06, correct=0, third=Sean Haugh (L)

## Interpretation

- Do not infer a directional third-party correction if the minor-third sample is small or signed error is unstable.
- A stable increase in absolute error without stable signed error supports an uncertainty inflation term rather than a point-margin correction.
- Major independent cases require a separate multi-candidate model because D/R two-party margin is not the correct target when one major party is effectively replaced.

## Outputs

- experiments/third_party_historical_v2/results/race_context.csv
- experiments/third_party_historical_v2/results/context_summary.csv
- experiments/third_party_historical_v2/results/coverage.csv
- experiments/third_party_historical_v2/results/poll_rows.csv
