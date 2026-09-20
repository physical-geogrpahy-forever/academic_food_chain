# GitHub Actions run: BEA Regional Accounts archive discovery

- Generated UTC: 2026-09-20T17:06:32.141259+00:00
- Source: https://apps.bea.gov/histdata/RegionalAccounts.html
- HTML bytes: 26530
- HTML sha256: `75ea8fd76e6e9f27b15898456474e5b2cd35ed74ee5b645a0de0fccb4f57fc6f`
- Anchor links discovered: 77
- Data/archive-looking links: 2

## Purpose

Core V2 RelativeEconomicGrowth must not use today revised historical SQINC1 values as if they were known at an earlier 45-day snapshot. This discovery freezes the official BEA previously-published-estimates index before selecting historical release vintages.

## Rule

No economic value is emitted by this step. A later step may select a vintage only if its publication/release date is on or before the relevant historical snapshot.

## Outputs

- data/processed/source_snapshots/bea_regional_accounts_archive_index.html
- data/processed/source_snapshots/bea_regional_accounts_archive_links.csv

## Data-looking links sample

- https://apps.bea.gov/histdata/RegionalAccounts.html#main-content
- https://apps.bea.gov/histdata/index.html
