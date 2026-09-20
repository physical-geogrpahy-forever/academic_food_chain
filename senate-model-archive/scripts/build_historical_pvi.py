#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv'
SEN = ROOT / 'data/processed/historical_senate_race_audit.csv'
OUTDIR = ROOT / 'data/processed'
DOC = ROOT / 'docs/history/updates/2026-09-21_0051_historical-pvi-panel.md'

def truth(v):
    return str(v).strip().lower() == 'true'

pres_rows = []
with SRC.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        st = (r.get('state_abbrev') or '').strip()
        if not st:
            continue
        try:
            cyc = int(r['cycle'])
        except Exception:
            continue
        if cyc < 2000:
            continue
        pres_rows.append(r)

by_state_cycle = defaultdict(list)
for r in pres_rows:
    by_state_cycle[(int(r['cycle']), r['state_abbrev'])].append(r)

state_results = []
for (cycle, state), rr in by_state_cycle.items():
    cand = {}
    for r in rr:
        cid = r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        key = (cid, r.get('candidate_name') or r.get('alt_result_text') or '')
        if key not in cand:
            cand[key] = {'votes':0, 'parties':set(), 'missing':False}
        c = cand[key]
        bp = (r.get('ballot_party') or '').strip().upper()
        pp = (r.get('party') or '').strip().upper()
        if bp: c['parties'].add(bp)
        if pp: c['parties'].add(pp)
        v = (r.get('votes') or '').strip()
        if not v:
            c['missing'] = True
        else:
            try:
                c['votes'] += int(float(v))
            except ValueError:
                c['missing'] = True

    d_votes = sum(c['votes'] for c in cand.values() if 'DEM' in c['parties'])
    r_votes = sum(c['votes'] for c in cand.values() if 'REP' in c['parties'])
    denom = d_votes + r_votes
    if denom <= 0:
        continue
    state_results.append({
        'cycle': cycle,
        'state_abbrev': state,
        'd_votes': d_votes,
        'r_votes': r_votes,
        'two_party_total': denom,
        'state_margin_d_minus_r_pctpt': (d_votes-r_votes)/denom*100.0
    })

national = {}
for cycle in sorted({r['cycle'] for r in state_results}):
    rr = [r for r in state_results if r['cycle'] == cycle]
    dv = sum(r['d_votes'] for r in rr)
    rv = sum(r['r_votes'] for r in rr)
    national[cycle] = (dv-rv)/(dv+rv)*100.0

lean = {}
for r in state_results:
    nm = national[r['cycle']]
    lv = r['state_margin_d_minus_r_pctpt'] - nm
    r['national_margin_d_minus_r_pctpt'] = nm
    r['lean_vs_national_pctpt'] = lv
    lean[(r['cycle'], r['state_abbrev'])] = lv

state_results.sort(key=lambda r:(r['cycle'],r['state_abbrev']))
with (OUTDIR/'presidential_state_lean.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['cycle','state_abbrev','d_votes','r_votes','two_party_total','state_margin_d_minus_r_pctpt','national_margin_d_minus_r_pctpt','lean_vs_national_pctpt']
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    for r in state_results:
        w.writerow({k:(f'{r[k]:.8f}' if isinstance(r[k],float) else r[k]) for k in fields})

with SEN.open('r',encoding='utf-8-sig',newline='') as f:
    senate=list(csv.DictReader(f))

pres_years=sorted(national)
pvi_rows=[]
for s in senate:
    cyc=int(s['cycle'])
    st=s['state_abbrev']
    prev=[y for y in pres_years if y < cyc and (y,st) in lean]
    if len(prev)<2:
        continue
    recent, older = prev[-1], prev[-2]
    lr, lo = lean[(recent,st)], lean[(older,st)]
    pvi=0.67*lr+0.33*lo
    pvi_rows.append({
        'race_id':s['race_id'],'cycle':cyc,'state_abbrev':st,'seat':s['seat'],
        'recent_pres_year':recent,'older_pres_year':older,
        'lean_recent_pctpt':lr,'lean_older_pctpt':lo,'pvi_default_067_033_pctpt':pvi
    })

with (OUTDIR/'historical_senate_pvi_default_067_033.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['race_id','cycle','state_abbrev','seat','recent_pres_year','older_pres_year','lean_recent_pctpt','lean_older_pctpt','pvi_default_067_033_pctpt']
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    for r in pvi_rows:
        w.writerow({k:(f'{r[k]:.8f}' if isinstance(r[k],float) else r[k]) for k in fields})

pvi26=[]
for st in sorted({s for (y,s) in lean if y==2024 and s!='DC'}):
    if (2020,st) not in lean:
        continue
    lr,lo=lean[(2024,st)],lean[(2020,st)]
    pvi26.append({'state_abbrev':st,'recent_pres_year':2024,'older_pres_year':2020,'lean_recent_pctpt':lr,'lean_older_pctpt':lo,'pvi_default_067_033_pctpt':0.67*lr+0.33*lo})
with (OUTDIR/'pvi_2026_default_067_033.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['state_abbrev','recent_pres_year','older_pres_year','lean_recent_pctpt','lean_older_pctpt','pvi_default_067_033_pctpt']
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    for r in pvi26:
        w.writerow({k:(f'{r[k]:.8f}' if isinstance(r[k],float) else r[k]) for k in fields})

counts={y:sum(r['cycle']==y for r in state_results) for y in sorted(national)}
lines=[
    '# GitHub Actions run: historical PVI panel',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Presidential source repo: fivethirtyeight/election-results',
    '- Source commit: d7a7cff101da28f4ff77114450a964874800ca54',
    '- Source blob SHA: 0e4171053b71363a31669137cb9a86289e58d438',
    '',
    '## Reconstruction rule',
    '',
    'For each Senate election cycle, use the two most recent presidential general elections strictly earlier than that Senate election. This prevents using same-year presidential results that were not known at a 45-day forecast snapshot.',
    '',
    'State lean = state Democratic-minus-Republican two-party presidential margin minus national Democratic-minus-Republican two-party presidential margin.',
    '',
    'Reconstruction default PVI = 0.67 * recent lean + 0.33 * older lean.',
    '',
    'The 0.67/0.33 weights are preserved handoff defaults, not claimed recovered exact fitted weights.',
    '',
    '## Presidential state rows by cycle',
    '',
    '| presidential cycle | state/DC rows | national D-R two-party margin |',
    '|---:|---:|---:|'
]
for y in sorted(national):
    lines.append(f'| {y} | {counts[y]} | {national[y]:.4f} |')
lines += [
    '',
    '## Outputs',
    '',
    '- data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv',
    '- data/processed/source_snapshots/presidential_source_manifest.csv',
    '- data/processed/presidential_state_lean.csv',
    '- data/processed/historical_senate_pvi_default_067_033.csv',
    '- data/processed/pvi_2026_default_067_033.csv',
    '',
    f'- Historical Senate race rows receiving PVI: {len(pvi_rows)}',
    f'- 2026 state PVI rows: {len(pvi26)}',
    '',
    '## Next',
    '',
    'Cross-check presidential state and national margins against FEC official election publications, then add SameSeat six-year lag using the canonical Senate target panel once partisan-alignment exceptions are locked.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:30]))