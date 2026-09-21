# 2026 FEC June-30 18-month block

## Project priority status

- **Auxiliary diagnostic only.** This block is not required to run the locked Core V2-R Direction Production 2026 model.
- **Deferred.** Missing June-30 finance values must not block the production workflow.
- Do not spend production-model time reconstructing this block unless a later analysis explicitly requires finance diagnostics.

- Generated UTC: 2026-09-21T01:06:58.756919+00:00
- Required cutoff: activity through 2026-06-30.
- Source family: official FEC congressional candidate statistical tables 6a, 6b, 6f.
- Missing Top-50 membership is retained as missing, never zero.

## Source availability

- receipts: available=False, parsed_rows=0, source=NA
- individual: available=False, parsed_rows=0, source=NA
- cash: available=False, parsed_rows=0, source=NA

## Race-level coverage

| State | receipts share D-R | individual share D-R | cash share D-R |
|---|---:|---:|---:|
| AK | NA | NA | NA |
| GA | NA | NA | NA |
| IA | NA | NA | NA |
| ME | NA | NA | NA |
| MI | NA | NA | NA |
| NC | NA | NA | NA |
| NH | NA | NA | NA |
| OH | NA | NA | NA |
| TX | NA | NA | NA |

## Interpretation

- Finance is an auxiliary input only. The locked historical production model did not promote FEC finance to a universal structural term.
- These values are retained for race diagnostics and for the narrow finance-aware post-hoc candidate analysis already documented.
- Do not infer a zero financial position from a missing Top-50 match.
