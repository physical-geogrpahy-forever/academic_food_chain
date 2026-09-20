#!/usr/bin/env python3
import csv
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv'
OUT = ROOT / 'data/processed/presidential_2000_duplicate_audit.csv'
DETAIL = ROOT / 'data/processed/presidential_2000_duplicate_rows.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0114_presidential-2000-duplicate-audit.md'

STATES = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
}
VALID = STATES | {'DC'}

rows=[]
with SRC.open('r',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage')!='general':
            continue
        try:
            cyc=int(r['cycle'])
        except Exception:
            continue
        st=(r.get('state_abbrev') or '').strip().upper()
        if cyc==2000 and st in VALID:
            rows.append(r)

by_state=defaultdict(list)
for r in rows:
    by_state[r['state_abbrev'].upper()].append(r)

def party_of(r):
    vals={(r.get('party') or '').strip().upper(),(r.get('ballot_party') or '').strip().upper()}
    if 'DEM' in vals: return 'DEM'
    if 'REP' in vals: return 'REP'
    return 'OTHER'

def votes(r):
    try: return int(float((r.get('votes') or '0').strip() or 0))
    except Exception: return 0

def sig(r):
    # Ignore row id/candidate ids to detect duplicated result lines representing the same ballot line.
    return (
        r.get('candidate_name') or '',
        r.get('ballot_party') or '',
        r.get('party') or '',
        r.get('votes') or '',
        r.get('percent') or '',
        r.get('winner') or '',
        r.get('alt_result_text') or '',
        r.get('source') or '',
    )

audit=[]
detail=[]
for st in sorted(by_state):
    rr=by_state[st]
    counts=Counter(sig(r) for r in rr)
    unique={}
    for r in rr:
        unique.setdefault(sig(r),r)
    raw_d=sum(votes(r) for r in rr if party_of(r)=='DEM')
    raw_r=sum(votes(r) for r in rr if party_of(r)=='REP')
    dedup_d=sum(votes(r) for r in unique.values() if party_of(r)=='DEM')
    dedup_r=sum(votes(r) for r in unique.values() if party_of(r)=='REP')
    raw_margin=(raw_d-raw_r)/(raw_d+raw_r)*100 if raw_d+raw_r else None
    dedup_margin=(dedup_d-dedup_r)/(dedup_d+dedup_r)*100 if dedup_d+dedup_r else None
    sources=sorted({r.get('source','') for r in rr if r.get('source','')})
    dup_count=sum(n-1 for n in counts.values() if n>1)
    audit.append({
        'state_abbrev':st,
        'raw_lines':len(rr),
        'unique_signature_lines':len(unique),
        'duplicate_lines':dup_count,
        'raw_d_votes':raw_d,
        'raw_r_votes':raw_r,
        'dedup_d_votes':dedup_d,
        'dedup_r_votes':dedup_r,
        'raw_margin_pctpt':'' if raw_margin is None else raw_margin,
        'dedup_margin_pctpt':'' if dedup_margin is None else dedup_margin,
        'sources':' ; '.join(sources),
    })
    for r in rr:
        n=counts[sig(r)]
        if n>1 or st=='AL':
            detail.append({
                'state_abbrev':st,
                'race_id':r.get('race_id',''),
                'record_id':r.get('id',''),
                'candidate_name':r.get('candidate_name',''),
                'party':r.get('party',''),
                'ballot_party':r.get('ballot_party',''),
                'votes':r.get('votes',''),
                'percent':r.get('percent',''),
                'source':r.get('source',''),
                'signature_count':n,
            })

with OUT.open('w',encoding='utf-8',newline='') as f:
    fields=list(audit[0].keys())
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for r in audit:
        w.writerow({k:(f'{r[k]:.8f}' if isinstance(r[k],float) else r[k]) for k in fields})

with DETAIL.open('w',encoding='utf-8',newline='') as f:
    fields=['state_abbrev','race_id','record_id','candidate_name','party','ballot_party','votes','percent','source','signature_count']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(detail)

dup_states=[r for r in audit if r['duplicate_lines']>0]
lines=[
    '# GitHub Actions run: 2000 presidential duplicate-row audit',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Reason: 2000 state-summed national D-R margin differs from the source national row and FEC official aggregate.',
    '',
    f'- States/DC with exact duplicate signatures: {len(dup_states)}',
    f'- Total duplicate lines: {sum(r["duplicate_lines"] for r in audit)}',
    '',
    '| state | raw lines | duplicates | raw D | raw R | dedup D | dedup R | raw margin | dedup margin |',
    '|---|---:|---:|---:|---:|---:|---:|---:|---:|'
]
for r in dup_states:
    lines.append(f"| {r['state_abbrev']} | {r['raw_lines']} | {r['duplicate_lines']} | {r['raw_d_votes']} | {r['raw_r_votes']} | {r['dedup_d_votes']} | {r['dedup_r_votes']} | {r['raw_margin_pctpt']:.4f} | {r['dedup_margin_pctpt']:.4f} |")
al=next((r for r in audit if r['state_abbrev']=='AL'),None)
lines += [
    '',
    '## Alabama diagnostic',
    '',
    ('AL raw D/R = '+str(al['raw_d_votes'])+'/'+str(al['raw_r_votes'])+', deduplicated = '+str(al['dedup_d_votes'])+'/'+str(al['dedup_r_votes'])) if al else 'AL not found',
    '',
    'FEC official 2000 Alabama values are Bush 941,173 and Gore 692,611. Exact-duplicate removal is accepted only if it recovers the official state result; otherwise a broader source correction is required.',
    '',
    '## Outputs',
    '',
    '- data/processed/presidential_2000_duplicate_audit.csv',
    '- data/processed/presidential_2000_duplicate_rows.csv',
    '',
    '## Next',
    '',
    'If exact duplicates explain Alabama and the national mismatch, apply deterministic exact-row deduplication before candidate aggregation and re-run all PVI validation gates. Otherwise freeze FEC official state data for 2000.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))