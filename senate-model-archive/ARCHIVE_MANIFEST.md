# ARCHIVE MANIFEST
## 2026 U.S. Senate Model Recovery Archive

### GitHub location
- repository: `physical-geogrpahy-forever/academic_food_chain`
- branch: `archive-2026-us-senate-model`
- root path: `senate-model-archive/`
- default `main` branch is untouched.

### Why a dedicated branch
The currently connected GitHub toolset can create branches and files but does not expose repository creation. To prevent further loss immediately, this project was archived on a dedicated branch without modifying the repository's main branch. It can later be migrated verbatim to a standalone repository.

### Preserved files

```text
senate-model-archive/
├── README.md
├── CHANGELOG.md
├── ARCHIVE_MANIFEST.md
├── config/
│   └── core_v2_preserved_config.json
├── data/
│   ├── benchmarks/
│   │   ├── core_v2_benchmarks.csv
│   │   └── core_v2_regional_residuals.csv
│   ├── schema/
│   │   └── expected_core_v2_outputs.md
│   └── snapshots/
│       └── core_v2_2026_snapshot_status.csv
└── docs/
    ├── audits/
    │   └── CORE_V2_2026_PRODUCTION_DATA_AUDIT_2026-09-21.md
    ├── handoffs/
    │   └── 2026_US_SENATE_MODEL_MASTER_HANDOFF_CORE_V2_2026-09-21.md
    └── history/
        └── RECOVERY_STATUS_2026-09-21.md
```

### Missing historical implementation artifacts

The following exact historical artifacts have not been recovered and must not be fabricated:

```text
core_v2_predictions_oos.csv
core_v2_residuals_oos.csv
core_v2_region_summary.csv
core_v2_coefficients_by_cycle.csv
core_v2_poll_snapshot_45d.csv
core_v2_config.json
```

The preserved config in this archive is a reconstruction of the documented settings, not the missing original implementation file.

### Rule going forward
Every model change, new dataset snapshot, benchmark, or methodological decision must be committed here (or to a future standalone migrated repository) before proceeding to the next stage.
