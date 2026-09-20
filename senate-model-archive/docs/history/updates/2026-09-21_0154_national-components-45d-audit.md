# GitHub Actions run: 45-day National component audit

- Generated UTC: 2026-09-20T16:59:39.783185+00:00
- Cycles: 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022

## Rule

Snapshot date = federal general-election date minus 45 days.
Generic ballot uses the latest FiveThirtyEight All polls topline modeldate on or before the snapshot.
Approval uses the latest presidential-approval observation whose field end date is on or before the snapshot.

## Component availability

| cycle | snapshot | generic date | generic D-R | approval end | net approval |
|---:|---|---|---:|---|---:|
| 2006 | 2006-09-23 | 2006-09-23 | 9.20 | 2006-09-17 | -7.00 |
| 2008 | 2008-09-20 | 2008-09-20 | 6.94 | 2008-09-11 | -34.00 |
| 2010 | 2010-09-18 | 2010-09-18 | -3.62 | 2010-09-12 | 0.00 |
| 2012 | 2012-09-22 | 2012-09-22 | 2.89 | 2012-09-16 | 6.00 |
| 2014 | 2014-09-20 | 2014-09-20 | -1.80 | 2014-09-14 | -13.00 |
| 2016 | 2016-09-24 | 2016-09-24 | 2.74 | 2016-09-18 | 8.00 |
| 2018 | 2018-09-22 | 2016-11-06 | 2.36 | 2018-09-16 | -18.00 |
| 2020 | 2020-09-19 | 2016-11-06 | 2.36 | 2020-09-13 | -14.00 |
| 2022 | 2022-09-24 | 2016-11-06 | 2.36 | 2022-09-16 | -14.00 |

## Status

These are National_t ingredients, not National_t itself. The exact Core V2 component standardization, weights, and any latent-factor model remain unrecovered. No weights are fit here.

## Output

- data/processed/core_v2r_national_components_45d_audit.csv
