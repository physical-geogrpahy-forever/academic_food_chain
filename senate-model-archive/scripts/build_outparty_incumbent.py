#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/processed/core_v2r_headline_design_matrix_with_candidate_experience.csv'
OUT=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
AUDIT=ROOT/'data/processed/core_v2r_outparty_incumbent_audit.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0142_outparty-incumbent-hypothesis-A.md'

with BASE.open('r',encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))

out=[]; audit=[]
for r in rows:
    pvi=float(r['pvi_default_067_033_pctpt'])
    d_inc=int(r['d_incumbency']); r_inc=int(r['r_incumbency'])
    d_flag=1 if d_inc==1 and pvi<0 else 0
    r_flag=1 if r_inc==1 and pvi>0 else 0
    signed=d_flag-r_flag
    x=dict(r)
    x['d_outparty_incumbent']=d_flag
    x['r_outparty_incumbent']=r_flag
    x['OutPartyIncumbent']=signed
    out.append(x)
    if d_flag or r_flag:
        audit.append({
          'race_id':r['race_id'],'cycle':r['cycle'],'state_abbrev':r['state_abbrev'],'seat':r['seat'],
          'd_candidate':r['d_side_candidate'],'r_candidate':r['r_side_candidate'],
          'pvi_default_067_033_pctpt':r['pvi_default_067_033_pctpt'],
          'd_incumbency':d_inc,'r_incumbency':r_inc,
          'd_outparty_incumbent':d_flag,'r_outparty_incumbent':r_flag,'OutPartyIncumbent':signed
        })

fields=list(out[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
af=list(audit[0].keys()) if audit else ['race_id']
with AUDIT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=af); w.writeheader(); w.writerows(audit)

lines=[
 '# GitHub Actions run: OutPartyIncumbent reconstruction hypothesis A','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Headline rows: {len(out)}',
 f'- Out-party incumbent rows: {len(audit)}','',
 '## Status','',
 'The surviving Core V2 handoff preserves the concept and model term but not the exact historical binary coding rule. This file is therefore an explicit Core V2-R reconstruction hypothesis, not a recovered exact implementation.','',
 '## Hypothesis A','',
 'Using Democratic-minus-Republican PVI sign and the corrected Senate incumbency flags:','',
 '- Democratic incumbent in a Republican-leaning state (PVI < 0): d_outparty_incumbent = 1',
 '- Republican incumbent in a Democratic-leaning state (PVI > 0): r_outparty_incumbent = 1',
 '- signed model variable: OutPartyIncumbent = d_outparty_incumbent - r_outparty_incumbent',
 '- PVI = 0 produces no out-party flag.','',
 'No magnitude threshold is chosen from 2014/2018/2022 outcomes. Alternative thresholds, if tested, must be selected only inside nested rolling OOS.','',
 '## Flagged headline races','',
 '| cycle | state | D candidate | R candidate | PVI | D flag | R flag | signed |',
 '|---:|---|---|---|---:|---:|---:|---:|'
]
for r in audit:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['d_candidate']} | {r['r_candidate']} | {float(r['pvi_default_067_033_pctpt']):.2f} | {r['d_outparty_incumbent']} | {r['r_outparty_incumbent']} | {r['OutPartyIncumbent']} |")
lines += [
 '','## Outputs','',
 '- data/processed/core_v2r_outparty_incumbent_audit.csv',
 '- data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv','',
 '## Next','',
 'Construct pre-election candidate personal-vote history as sufficient statistics without choosing the lost shrinkage hyperparameters from headline outcomes.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))