#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent

STEPS = [
    'build_historical_senate_audit.py',
    'audit_oos_exception_races.py',
    'infer_headline_sample_size.py',
    'build_headline_target_panel.py',
    'fetch_presidential_source.py',
    'build_historical_pvi.py',
    'build_same_seat_features.py',
    'build_design_matrix_skeleton.py',
    'fetch_candidate_experience_sources.py',
    'audit_candidate_experience.py',
    'fetch_congress_legislators.py',
    'crosscheck_congress_service.py',
    'build_congress_experience_overrides.py',
    'fetch_nga_former_governors.py',
    'audit_governor_experience.py',
    'build_outparty_incumbent.py',
    'build_personal_vote_sufficient_stats.py',
    'join_personal_vote_audit.py',
    'fetch_national_environment_sources.py',
    'audit_national_components_45d.py',
    'audit_presidential_national_margin.py',
    'audit_presidential_2000_duplicates.py',
]

for name in STEPS:
    path = ROOT / name
    print(f'=== RUN {name} ===')
    runpy.run_path(str(path), run_name='__main__')

print('=== PIPELINE COMPLETE ===')