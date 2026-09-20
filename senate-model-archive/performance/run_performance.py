#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parent
STEPS=['run_fullcycle_national_econ_oos.py']

for name in STEPS:
    print('=== PERFORMANCE RUN',name,'===')
    runpy.run_path(str(ROOT/name),run_name='__main__')

print('=== PERFORMANCE PIPELINE COMPLETE ===')
