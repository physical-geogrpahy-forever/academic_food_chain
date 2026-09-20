# GitHub Actions run: congressional service cross-check

- Generated UTC: 2026-09-20T16:28:31.480210+00:00
- Candidate-side rows: 198
- Candidates matched to a Congress term record: 116/198
- Review rows: 61
- Matched rows with term-date vs election-history discrepancy: 12
- Election-history expected Congress service but no accepted term-record match: 49

## Method correction

The first implementation compared every candidate against every historical legislator and treated unmatched candidates as a generic problem. This version indexes candidates by normalized surname and treats unmatched candidates with no election-history congressional signal as normal non-members.

## Purpose

Actual congressional term dates are used to detect prior Senate service, prior House service, and Senate incumbency, including appointments that election-win history can miss.

## Review rule

A row is sent to review only when the name match is ambiguous, election history expects congressional service but no term record is accepted, or term-date flags disagree with election-history flags.

## Limits

- Governor experience remains separate.
- Name matching is reconstruction logic; ambiguous cases are never silently accepted.

## Outputs

- data/processed/core_v2r_headline_congress_service_crosscheck.csv
- data/processed/core_v2r_candidate_name_match_review.csv

## Next

Resolve the review rows and convert supported term-date corrections into an explicit candidate-experience override table before joining them to the design matrix.
