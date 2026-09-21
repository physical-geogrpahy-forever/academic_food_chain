# Final validation bundle

## Status

This directory is the canonical validation bundle for **Core V2-R Direction Production 2026**.

Do not reconstruct the 96/99 or 98/99 results from chat text. Read the files in this directory.

Repository:
- `physical-geogrpahy-forever/academic_food_chain`
- branch: `archive-2026-us-senate-model`
- bundle verified against branch HEAD: `3d33b3b74061eb4481dfafe9c5b216851386460a`
- verification date: 2026-09-21

## Two validation results must remain separate

### Clean nested OOS

Canonical file:

`clean_nested_96of99_predictions.csv`

Verified:
- N = 99
- correct = **96**
- accuracy = **96.97%**
- wrong races:
  - 2014 North Carolina, race_id 14
  - 2018 Montana, race_id 110
  - 2022 Nevada, race_id 8937

This is the official historical OOS direction benchmark.

### Production retrospective diagnostic

Canonical file:

`production_98of99_predictions.csv`

Verified:
- N = 99
- correct = **98**
- accuracy = **98.99%**
- this result is **not OOS**
- only wrong race:
  - 2014 North Carolina, race_id 14

Correctness changes relative to the fixed-poll 94/99 baseline:
- 2018 Nevada, race_id 112: wrong -> correct
- 2018 Missouri, race_id 109: wrong -> correct
- 2018 Florida, race_id 100: wrong -> correct
- 2018 Indiana, race_id 102: wrong -> correct

No other headline race changes are part of the documented 94 -> 98 improvement.

## Base-prior reconstruction

Canonical files:
- `base_prior_99_predictions.csv`
- `base_prior_choices.csv`
- `base_prior_coefficients_by_cycle.csv`
- `base_prior_standardization_by_cycle.csv`

Verified:
- base prediction rows = 99
- coefficient rows = 30
- standardization rows = 27
- maximum stored reconstruction absolute error = 8.526512829121202e-14

The coefficient file contains fitted coefficients by outer test cycle.
The standardization file contains the training mean and standard deviation used for each standardized feature by outer test cycle.

## Production selector

Canonical files:
- `core_v2r_direction_2026_production.json`
- `production_selector_top_grid.csv`
- `run_production_selector_2026.py`

Verified production grid winner:
- training correct = 237 / 259
- Brier = 0.07110360831830437
- log loss = 0.25225898254744633
- MAE = 7.934908771742069
- threshold when poll and PVI disagree = 2.0 percentage points
- threshold when poll and PVI agree = 0.75 percentage points
- minimum absolute PVI when poll and PVI agree = 15 percentage points

## Base-prior code

Canonical code:
- `run_fullcycle_inc_era_oos.py`

Do not silently replace this file with a later experimental runner.

## Integrity

`manifest.json` stores SHA-256 values for the canonical files and source files.

If a future task changes any canonical file:
1. create a new version instead of overwriting this bundle;
2. regenerate a new manifest;
3. record the new clean OOS result separately from any retrospective diagnostic;
4. never label the 98/99 retrospective result as OOS.

## Recovery order for a new chat

1. Read this README.
2. Read `manifest.json`.
3. Read `core_v2r_direction_2026_production.json`.
4. Read `clean_nested_96of99_predictions.csv`.
5. Read `production_98of99_predictions.csv`.
6. Read coefficients and standardization only if model reconstruction is needed.

