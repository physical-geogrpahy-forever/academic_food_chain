#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent

STEPS = [
    'build_historical_senate_audit.py',
    'audit_oos_exception_races.py',
    'infer_headline_sample_size.py',
]

for name in STEPS:
    path = ROOT / name
    print(f'=== RUN {name} ===')
    runpy.run_path(str(path), run_name='__main__')

print('=== PIPELINE COMPLETE ===')