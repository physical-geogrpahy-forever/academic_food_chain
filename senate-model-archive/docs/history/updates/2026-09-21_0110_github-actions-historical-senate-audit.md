# GitHub Actions run: historical Senate race audit

- Generated UTC: 2026-09-20T16:01:06.414875+00:00
- Execution: GitHub Actions
- Input: data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv

## Summary

- General-election race_id count: 848
- Mechanically standard D/R race count: 818
- Special-election races: 29
- Races without a unique DEM candidate: 21
- Races without a unique REP candidate: 11
- Races with missing vote totals: 2
- Unopposed races: 2
- Fusion or multi-line candidate races: 31
- Ranked-choice records: 3

## Cycle counts

| cycle | all general races | mechanical standard D/R |
|---:|---:|---:|
| 1976 | 33 | 30 |
| 1978 | 34 | 33 |
| 1980 | 33 | 33 |
| 1982 | 33 | 33 |
| 1984 | 32 | 32 |
| 1986 | 34 | 34 |
| 1988 | 33 | 33 |
| 1990 | 34 | 30 |
| 1992 | 34 | 34 |
| 1994 | 35 | 35 |
| 1996 | 33 | 33 |
| 1998 | 33 | 33 |
| 2000 | 33 | 32 |
| 2002 | 33 | 28 |
| 2004 | 33 | 32 |
| 2006 | 33 | 31 |
| 2008 | 35 | 33 |
| 2010 | 39 | 38 |
| 2012 | 33 | 32 |
| 2013 | 2 | 2 |
| 2014 | 35 | 33 |
| 2016 | 33 | 32 |
| 2017 | 1 | 1 |
| 2018 | 34 | 32 |
| 2020 | 33 | 32 |
| 2022 | 35 | 33 |
| 2024 | 35 | 34 |

## Interpretation

This is a mechanical audit, not the final Core V2-R model panel.
Independent-aligned candidates, special elections, fusion voting, ranked choice, unopposed races, and missing historical votes require explicit inclusion rules.

## Next

Extract exception races for 2006-2022 OOS and 2014/2018/2022 headline validation, then lock the inclusion rule.
