# Expected exact Core V2 outputs

These artifacts must be regenerated and committed once Core V2-R reproduces the historical benchmark.

```text
core_v2_predictions_oos.csv
core_v2_residuals_oos.csv
core_v2_region_summary.csv
core_v2_coefficients_by_cycle.csv
core_v2_poll_snapshot_45d.csv
core_v2_config.json
```

## Minimum keys

### predictions/residuals
`cycle, state, senate_class, candidate_D, candidate_R, actual_margin_D_minus_R, prior_margin, poll_adj_margin, posterior_margin, residual, snapshot_date`

### coefficients
`train_end_cycle, test_cycle, term, estimate, standard_error_or_posterior_sd, era_parameterization`

### poll snapshot
`cycle, state, poll_id, pollster, field_start, field_end, publication_date, sample_size, population_type, margin_D_minus_R, included_45d, exclusion_reason`
