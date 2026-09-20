# Third-party Senate poll source audit

- Generated UTC: 2026-09-20T18:53:51.227908+00:00
- Source: https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv
- Bytes: 4961378
- Rows: 20466
- Field count: 30

## Schema

poll_id, question_id, race_id, cycle, location, type_simple, race, pollster, pollster_rating_id, aapor_roper, inactive, methodology, transparency_score, partisan, polldate, electiondate, time_to_election, samplesize, cand1_name, cand1_id, cand1_party, cand1_pct, cand1_actual, cand2_name, cand2_id, cand2_party, cand2_pct, cand2_actual, margin_poll, margin_actual

## Candidate/result-like fields

cand1_name, cand1_id, cand1_party, cand1_pct, cand1_actual, cand2_name, cand2_id, cand2_party, cand2_pct, cand2_actual, margin_poll, margin_actual

## Multi-candidate capability

- Capable: False
- Reason: no explicit third-candidate representation detected

## North Carolina 2014 Senate

- Matching Senate rows: 0
- Rows explicitly containing Haugh or Libertarian text: 0

No explicit Haugh/Libertarian row was found in this source. If the schema is only two-candidate, a different archived poll source is required for a true D/R/T layer.

## Decision rule

If explicit third-candidate support exists, build a historical third-party-aware poll layer from this source. If not, do not fabricate third-party poll shares; locate another archived source or limit the next step to a source-coverage audit.

## Outputs

- experiments/third_party_poll_audit/results/third_party_source_meta.csv
- experiments/third_party_poll_audit/results/nc2014_senate_raw_poll_rows.csv (if rows exist)
