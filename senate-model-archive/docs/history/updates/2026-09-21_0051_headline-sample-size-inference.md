# GitHub Actions run: headline validation sample-size inference

- Generated UTC: 2026-09-20T17:05:47.304746+00:00
- Execution: GitHub Actions
- 2014/2018/2022 general-election race_id total: 104
- Preserved direction accuracies: 90.9% and 91.9%

## Arithmetic inference

- Unique denominator matching both one-decimal percentages: 99
- 90.9% corresponds to 90/99
- 91.9% corresponds to 91/99
- Implied exclusions from the 104 general-race universe: 5

This inference assumes direction accuracy was an unweighted fraction of correctly called races and rounded to one decimal place. It is strong evidence, not proof of the original row filter.

## Structurally irregular headline races

- Count: 7

| cycle | state | reasons | winner |
|---:|---|---|---|
| 2014 | AL | non_unique_or_missing_D_R | Jeff Sessions [REP] 795606 |
| 2014 | KS | non_unique_or_missing_D_R | Pat Roberts [REP] 460350 |
| 2018 | CA | non_unique_or_missing_D_R | Dianne Feinstein [DEM] 6019422 |
| 2018 | ME | winner_not_major_party;ranked_choice | Angus S. King Jr. [IND] 344575 |
| 2018 | VT | non_unique_or_missing_D_R;winner_not_major_party | Bernie Sanders [IND] 183649 |
| 2022 | AK | non_unique_or_missing_D_R;ranked_choice;fusion_or_multiline | Lisa Murkowski [REP] 366207 |
| 2022 | UT | non_unique_or_missing_D_R | Mike Lee [REP] 571974 |

## Hypothesis A for the five implied exclusions

If special elections and fusion-ballot races remain included, there are seven structurally irregular headline races. A 99-race denominator implies that exactly two of those seven were handled through a partisan-alignment rule rather than excluded.

Hypothesis A includes 2018 Maine and 2018 Vermont as Democratic-aligned independents, and excludes 2014 Alabama, 2014 Kansas, 2018 California, 2022 Alaska, and 2022 Utah.

Why this is plausible but not yet locked:
- U.S. Senate party-division history for the 115th Congress reports two Independents, both caucusing with Democrats.
- The two Independents serving in that Congress were Angus King of Maine and Bernie Sanders of Vermont.
- FEC official results show Greg Orman as IND in the 2014 Kansas general election after the Democratic nominee withdrew.
- FEC official results show the 2018 California general election was Democrat vs Democrat.
- FEC official results show Evan McMullin as unaffiliated in the 2022 Utah general election.
- Alaska official materials show the 2022 Senate contest used ranked-choice voting with multiple Republican candidates.

Sources:
- https://www.senate.gov/history/partydiv.htm/
- https://www.fec.gov/documents/1698/2014senate.pdf
- https://www.fec.gov/documents/2705/federalelections2018.pdf
- https://www.fec.gov/documents/5675/federalelections2022.pdf
- https://www.elections.alaska.gov/election-results/e/?id=22genr

## Status

Hypothesis A is a reconstruction candidate only. It is not authoritative until the downstream historical design matrix and OOS benchmark reproduce the preserved Core V2 metrics without post-election leakage.

## Next

Build a documented partisan-alignment map for non-major-party Senate candidates in 2006-2022, then regenerate the canonical historical target panel and verify that the headline row count is 99.
