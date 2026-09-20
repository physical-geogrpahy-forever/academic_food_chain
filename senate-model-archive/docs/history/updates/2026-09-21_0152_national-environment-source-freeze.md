# GitHub Actions run: National environment source freeze

- Generated UTC: 2026-09-20T16:59:39.645591+00:00
- FiveThirtyEight generic-ballot source commit: 4c1ff5e3aef1816ae04af63218015066e186c147
- FiveThirtyEight generic-ballot blob expected from repository audit: 6a341f0ef020f9d8a46a45c5a2380d8215da866e
- Generic-ballot raw bytes: 754089
- Parsed presidential-approval rows: 891

## Sources

- FiveThirtyEight historical generic-ballot topline, preserved from the pinned GitHub commit.
- American Presidency Project public-approval tables for George W. Bush, Barack Obama, Donald Trump first term, and Joseph Biden. The prior-president tables are historical series; raw HTML is frozen with SHA256 for reproducibility.

## Important

These are source components only. They do not define the final Core V2 National_t factor. Component weighting and latent-factor construction remain unrecovered and must not be tuned on headline test outcomes.

## Outputs

- data/processed/source_snapshots/generic_topline_historical_538_4c1ff5e3.csv
- data/processed/source_snapshots/app_presidential_approval_historical.csv
- data/processed/source_snapshots/national_environment_source_manifest.csv
