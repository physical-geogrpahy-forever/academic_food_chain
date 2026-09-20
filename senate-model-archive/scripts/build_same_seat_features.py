#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OVR=ROOT/'config/partisan_alignment_overrides_v1.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
OUT=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0114_same-seat-feature-audit.md'

with OVR.open('r',encoding='utf-8-sig',newline='') as f:
    overrides={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in csv.DictReader(f)}

rows=[]
with RAW.open('r',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage')!='general': continue
        try: cyc=int(r['cycle'])
        except Exception: continue
        if 2000<=cyc<=2022: rows.append(r)

by_race=defaultdict(list)
for r in rows: by_race[r['race_id']].append(r)

def truth(v): return str(v).strip().lower()=='true'
def pround(v):
    s=(v or '').strip()
    if not s: return None
    try: return int(float(s))
    except Exception: return None

def cands_for_race(rr):
    nums=[pround(r.get('ranked_choice_round')) for r in rr if pround(r.get('ranked_choice_round')) is not None]
    selected=max(nums) if nums else None
    use=[r for r in rr if pround(r.get('ranked_choice_round'))==selected] if selected is not None else rr
    cand={}
    for r in use:
        cid=r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        name=r.get('candidate_name') or r.get('alt_result_text') or ''
        key=(cid,name)
        if key not in cand: cand[key]={'name':name,'votes':0,'parties':set(),'missing':False}
        c=cand[key]
        bp=(r.get('ballot_party') or '').strip().upper()
        if bp: c['parties'].add(bp)
        v=(r.get('votes') or '').strip()
        if not v: c['missing']=True
        else:
            try: c['votes']+=int(float(v))
            except Exception: c['missing']=True
    return list(cand.values()),selected

def find_name(cands,name):
    t=(name or '').strip().lower()
    exact=[c for c in cands if c['name'].strip().lower()==t]
    if len(exact)==1: return exact[0]
    partial=[c for c in cands if t and t in c['name'].strip().lower()]
    return partial[0] if len(partial)==1 else None

margin_records=[]
for race_id,rr in by_race.items():
    first=rr[0]
    cyc=int(first['cycle']); st=first['state_abbrev']; seat=first['office_seat_name']
    key=(cyc,st,seat); ov=overrides.get(key)
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}: continue
    cands,selected=cands_for_race(rr)
    if ov and ov['action']=='ALIGN':
        d=find_name(cands,ov['d_side_name']); r=find_name(cands,ov['r_side_name']); rule='override_ALIGN'
    else:
        ds=[c for c in cands if 'DEM' in c['parties']]; rs=[c for c in cands if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None; rule='unique_DEM_REP'
    if d is None or r is None or d['missing'] or r['missing']: continue
    total=sum(c['votes'] for c in cands if not c['missing']); dr=d['votes']+r['votes']
    if total<=0 or dr<=0: continue
    margin_records.append({
        'race_id':race_id,'cycle':cyc,'state_abbrev':st,'seat':seat,'special':truth(first.get('special','false')),
        'd_candidate':d['name'],'r_candidate':r['name'],
        'margin_total':100*(d['votes']-r['votes'])/total,
        'margin_two_party':100*(d['votes']-r['votes'])/dr,
        'rule':rule,'ranked_round':selected if selected is not None else ''
    })

by_key=defaultdict(list)
for r in margin_records: by_key[(r['cycle'],r['state_abbrev'],r['seat'])].append(r)

def choose_record(records):
    if not records: return None
    regular=[r for r in records if not r['special']]
    pool=regular if regular else records
    return sorted(pool,key=lambda x:x['race_id'])[0]

with HEAD.open('r',encoding='utf-8-sig',newline='') as f:
    head=list(csv.DictReader(f))

out=[]
for cur in head:
    cyc=int(cur['cycle']); st=cur['state_abbrev']; seat=cur['seat']
    exact=choose_record(by_key.get((cyc-6,st,seat),[]))
    prior_cycles=sorted({y for (y,s,q) in by_key if s==st and q==seat and y<cyc},reverse=True)
    last=None
    for y in prior_cycles:
        last=choose_record(by_key[(y,st,seat)])
        if last: break
    rec=dict(cur)
    rec.update({
        'same_seat_exact6_available':str(exact is not None).lower(),
        'same_seat_exact6_cycle':'' if exact is None else exact['cycle'],
        'same_seat_exact6_race_id':'' if exact is None else exact['race_id'],
        'same_seat_exact6_margin_total_pctpt':'' if exact is None else f"{exact['margin_total']:.8f}",
        'same_seat_exact6_margin_two_party_pctpt':'' if exact is None else f"{exact['margin_two_party']:.8f}",
        'same_seat_last_prior_available':str(last is not None).lower(),
        'same_seat_last_prior_cycle':'' if last is None else last['cycle'],
        'same_seat_last_prior_year_gap':'' if last is None else cyc-last['cycle'],
        'same_seat_last_prior_race_id':'' if last is None else last['race_id'],
        'same_seat_last_prior_margin_total_pctpt':'' if last is None else f"{last['margin_total']:.8f}",
        'same_seat_last_prior_margin_two_party_pctpt':'' if last is None else f"{last['margin_two_party']:.8f}"
    })
    out.append(rec)

fields=list(out[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)

exactn=sum(r['same_seat_exact6_available']=='true' for r in out)
lastn=sum(r['same_seat_last_prior_available']=='true' for r in out)
missing=[r for r in out if r['same_seat_exact6_available']!='true']
lines=[
    '# GitHub Actions run: SameSeat feature audit',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Headline target input: Core V2-R Hypothesis A, 99 races',
    '',
    '## Handoff rule',
    '',
    'The preserved handoff explicitly defines SameSeat as the result from the same Senate Class exactly six years earlier: SameSeat_{i,t-6}. The reconstruction therefore does not silently replace it with the most recent prior election.',
    '',
    '## Coverage',
    '',
    f'- headline rows: {len(out)}',
    f'- exact 6-year same-class available: {exactn}',
    f'- exact 6-year missing: {len(out)-exactn}',
    f'- last-prior-same-class available: {lastn}',
    '',
    'Both total-vote and D/R two-party margin versions are preserved until the original target denominator is recovered through OOS reproduction.',
    '',
    '## Missing exact-6-year rows',
    '',
    '| cycle | state | seat | special | last prior cycle | gap |',
    '|---:|---|---|---|---:|---:|'
]
for r in missing:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['seat']} | {r['special']} | {r['same_seat_last_prior_cycle']} | {r['same_seat_last_prior_year_gap']} |")
lines += [
    '',
    '## Rule status',
    '',
    '- Core candidate feature: exact-6-year same-class margin.',
    '- Audit-only comparator: last prior same-class margin and year gap.',
    '- Missing exact-6-year values are not silently filled from last-prior values.',
    '- How the original Core V2 encoded missing SameSeat values remains unresolved and must be tested without leakage.',
    '',
    '## Output',
    '',
    '- data/processed/core_v2r_headline_same_seat_features.csv',
    '',
    '## Next',
    '',
    'Join PVI to the 99-race target panel, then reconstruct incumbency and candidate-experience variables before attempting any regression.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:35]))