# GitHub Actions run: OutPartyIncumbent reconstruction hypothesis A

- Generated UTC: 2026-09-20T16:50:03.016599+00:00
- Headline rows: 99
- Out-party incumbent rows: 18

## Status

The surviving Core V2 handoff preserves the concept and model term but not the exact historical binary coding rule. This file is therefore an explicit Core V2-R reconstruction hypothesis, not a recovered exact implementation.

## Hypothesis A

Using Democratic-minus-Republican PVI sign and the corrected Senate incumbency flags:

- Democratic incumbent in a Republican-leaning state (PVI < 0): d_outparty_incumbent = 1
- Republican incumbent in a Democratic-leaning state (PVI > 0): r_outparty_incumbent = 1
- signed model variable: OutPartyIncumbent = d_outparty_incumbent - r_outparty_incumbent
- PVI = 0 produces no out-party flag.

No magnitude threshold is chosen from 2014/2018/2022 outcomes. Alternative thresholds, if tested, must be selected only inside nested rolling OOS.

## Flagged headline races

| cycle | state | D candidate | R candidate | PVI | D flag | R flag | signed |
|---:|---|---|---|---:|---:|---:|---:|
| 2014 | AK | Mark Begich | Dan Sullivan | -22.16 | 1 | 0 | 1 |
| 2014 | AR | Mark L. Pryor | Tom Cotton | -28.06 | 1 | 0 | 1 |
| 2014 | ME | Shenna Bellows | Susan M. Collins | 11.30 | 0 | 1 | -1 |
| 2014 | NC | Kay R. Hagan | Thomas Roland Tillis | -6.33 | 1 | 0 | 1 |
| 2014 | VA | Mark R. Warner | Ed W. Gillespie | -0.32 | 1 | 0 | 1 |
| 2018 | FL | Bill Nelson | Rick Scott | -3.32 | 1 | 0 | 1 |
| 2018 | IN | Joe Donnelly | Mike Braun | -19.77 | 1 | 0 | 1 |
| 2018 | MO | Claire McCaskill | Josh Hawley | -19.10 | 1 | 0 | 1 |
| 2018 | MT | Jon Tester | Matt Rosendale | -22.31 | 1 | 0 | 1 |
| 2018 | ND | Heidi Heitkamp | Kevin Cramer | -36.00 | 1 | 0 | 1 |
| 2018 | NV | Jacky S. Rosen | Dean Heller | 1.20 | 0 | 1 | -1 |
| 2018 | OH | Sherrod Brown | Jim Renacci | -7.50 | 1 | 0 | 1 |
| 2018 | PA | Robert P. Casey Jr. | Lou Barletta | -1.48 | 1 | 0 | 1 |
| 2018 | WI | Tammy Baldwin | Leah Vukmir | -1.05 | 1 | 0 | 1 |
| 2018 | WV | Joe Manchin, III | Patrick Morrisey | -41.51 | 1 | 0 | 1 |
| 2022 | AZ | Mark Kelly | Blake Masters | -4.81 | 1 | 0 | 1 |
| 2022 | GA | Raphael Warnock | Herschel Junior Walker | -5.37 | 1 | 0 | 1 |
| 2022 | NV | Catherine Cortez Masto | Adam Paul Laxalt | -1.28 | 1 | 0 | 1 |

## Outputs

- data/processed/core_v2r_outparty_incumbent_audit.csv
- data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv

## Next

Construct pre-election candidate personal-vote history as sufficient statistics without choosing the lost shrinkage hyperparameters from headline outcomes.
