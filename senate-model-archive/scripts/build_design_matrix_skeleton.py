#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
PVI=ROOT/'data/processed/historical_senate_pvi_default_067_033.csv'
OUT=ROOT/'data/processed/core_v2r_headline_design_matrix_skeleton.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0116_design-matrix-skeleton-pvi-sameseat.md'

with BASE.open('r',encoding='utf-8-sig',newline='') as f: base=list(csv.DictReader(f))
with PVI.open('r',encoding='utf-8-sig',newline='') as f: pvi={r['race_id']:r for r in csv.DictReader(f)}

out=[]; missing=[]
for r in base:
    q=pvi.get(r['race_id'])
    if q is None:
        missing.append(r['race_id']); continue
    z=dict(r)
    z.update({
        'pvi_recent_pres_year':q['recent_pres_year'],
        'pvi_older_pres_year':q['older_pres_year'],
        'pvi_lean_recent_pctpt':q['lean_recent_pctpt'],
        'pvi_lean_older_pctpt':q['lean_older_pctpt'],
        'pvi_default_067_033_pctpt':q['pvi_default_067_033_pctpt']
    })
    out.append(z)

if missing: raise RuntimeError('Missing PVI race_ids: '+','.join(missing))
if len(out)!=99: raise RuntimeError(f'Expected 99 headline rows, got {len(out)}')

fields=list(out[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)

same_missing=sum(r['same_seat_exact6_available']!='true' for r in out)
lines=[
    '# GitHub Actions run: Core V2-R design matrix skeleton',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Rows: 99',
    '',
    '## Variables currently joined',
    '',
    '- actual target margin: total-vote D-R and D/R two-party D-R versions',
    '- direction_actual',
    '- PVI reconstruction default: 0.67 recent presidential lean + 0.33 older presidential lean',
    '- SameSeat exact 6-year same-class margin, both target denominator versions',
    '- SameSeat exact-6 availability flag',
    '- last-prior-same-class fields retained for audit only',
    '',
    '## Validation',
    '',
    f'- PVI join coverage: {len(out)}/99',
    f'- SameSeat exact-6 missing: {same_missing}/99',
    '- No regression or coefficient fitting has been performed yet.',
    '',
    '## Important unresolved choices',
    '',
    '1. Original Core V2 target margin denominator: total vote vs D/R two-party vote.',
    '2. Original treatment of missing SameSeat values.',
    '3. Exact PVI recent/older weights beyond the preserved 0.67/0.33 default.',
    '',
    'These are retained as explicit reconstruction uncertainties rather than tuned against the 2014/2018/2022 test outcomes.',
    '',
    '## Output',
    '',
    '- data/processed/core_v2r_headline_design_matrix_skeleton.csv',
    '',
    '## Next',
    '',
    'Reconstruct candidate-level incumbency and Senate/Governor/House experience from pre-election information only, with a separate manual audit for appointments and party-aligned independents.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))