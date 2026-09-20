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
    'audit_presidential_national_margin.py',
    'audit_presidential_2000_duplicates.py',
]

for name in STEPS:
    path = ROOT / name
    print(f'=== RUN {name} ===')
    runpy.run_path(str(path), run_name='__main__')

print('=== PIPELINE COMPLETE ===')