# 538 deluxe-minus-classic external candidate/context signal

- Generated UTC: 2026-09-20T18:17:00.971547+00:00
- This experiment does NOT import FiveThirtyEight win probabilities.
- It uses only the margin difference between the deluxe and classic model at the latest published date on or before the 45-day snapshot.
- The difference is treated as an external candidate/expert/context adjustment signal.
- 2014 has no corresponding source in the public repository and is left unchanged.

## Source snapshots

- 2018: snapshot used 2018-09-22, matched classic/deluxe districts=33, downloaded bytes=2191238
- 2018 fields: rownames, forecastdate, state, class, special, candidate, party, incumbent, model, win_probability, voteshare, p10_voteshare, p90_voteshare
- 2022: snapshot used 2022-09-24, matched classic/deluxe districts=35, downloaded bytes=6404405
- 2022 fields: cycle, branch, district, forecastdate, expression, name_D1, name_D2, name_D3, name_D4, name_I1, name_R1, name_R2, name_R3, name_R4, name_O1, winner_D1, winner_D2, winner_D3, winner_D4, winner_R1, winner_R2, winner_R3, winner_R4, winner_I1, winner_O1, winner_Dparty, winner_Rparty, tipping, vpi, mean_predicted_turnout, p90_simmed_turnout_gross, p10_simmed_turnout_gross, voteshare_mean_D1, voteshare_mean_D2, voteshare_mean_D3, voteshare_mean_D4, voteshare_mean_I1, voteshare_mean_R1, voteshare_mean_R2, voteshare_mean_R3, voteshare_mean_R4, voteshare_mean_O1, p90_voteshare_simmed_I1, p90_voteshare_simmed_O1, p90_voteshare_simmed_D1, p90_voteshare_simmed_R1, p90_voteshare_simmed_D2, p90_voteshare_simmed_R2, p90_voteshare_simmed_R3, p90_voteshare_simmed_R4, p90_voteshare_simmed_D3, p90_voteshare_simmed_D4, p10_voteshare_simmed_I1, p10_voteshare_simmed_O1, p10_voteshare_simmed_D1, p10_voteshare_simmed_R1, p10_voteshare_simmed_D2, p10_voteshare_simmed_R2, p10_voteshare_simmed_R3, p10_voteshare_simmed_R4, p10_voteshare_simmed_D3, p10_voteshare_simmed_D4, pvi_538, vep, elasticity, mean_netpartymargin, p90_netpartymargin, p10_netpartymargin, wonrunoff_D1, lostrunoff_D1, wonrunoff_D2, lostrunoff_D2, wonrunoff_D3, lostrunoff_D3, wonrunoff_D4, lostrunoff_D4, wonrunoff_R1, lostrunoff_R1, wonrunoff_R2, lostrunoff_R2, wonrunoff_R3, lostrunoff_R3, wonrunoff_R4, lostrunoff_R4, wonrunoff_I1, lostrunoff_I1, simulations, timestamp

## Result

| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | nonzero external |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 99 | 94 | 94.9% | 94 | 94.9% | +0 | 60 |
| 2014 | 33 | 32 | 97.0% | 32 | 97.0% | +0 | 0 |
| 2018 | 33 | 29 | 87.9% | 29 | 87.9% | +0 | 29 |
| 2022 | 33 | 33 | 100.0% | 33 | 100.0% | +0 | 31 |

## Correctness changes


## Decision

This is an external-signal experiment, not a pure internal Core V2-R model. Keep it separate unless it materially improves direction accuracy and the user chooses to allow externally produced candidate/expert adjustments in the production model.

## Outputs

- experiments/external_candidate_signal/results/external_signal_summary.csv
- experiments/external_candidate_signal/results/external_signal_predictions.csv
