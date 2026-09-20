#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OVR = ROOT / 'config/headline_partisan_alignment_hypothesis_A.csv'
OUT = ROOT / 'data/processed/core_v2r_headline_target_hypothesis_A.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0051_headline-target-panel-hypothesis-A.md'

with OVR.open('r', encoding='utf-8-sig', newline='') as f:
    overrides = {(int(r['cycle']), r['state_abbrev'], r['seat']): r for r in csv.DictReader(f)}

rows=[]
with RAW.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        try:
            cycle=int(r['cycle'])
        except Exception:
            continue
        if cycle in {2014,2018,2022}:
            rows.append(r)

by_race=defaultdict(list)
for r in rows:
    by_race[r['race_id']].append(r)

def parse_round(v):
    s=(v or '').strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None

def candidate_groups(rr):
    rounds=[parse_round(r.get('ranked_choice_round')) for r in rr]
    numeric=[x for x in rounds if x is not None]
    use_rr=rr
    selected_round=''
    if numeric:
        selected_round=max(numeric)
        subset=[r for r in rr if parse_round(r.get('ranked_choice_round'))==selected_round]
        if subset:
            use_rr=subset
    cand={}
    for r in use_rr:
        cid=r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        name=r.get('candidate_name') or r.get('alt_result_text') or ''
        key=(cid,name)
        if key not in cand:
            cand[key]={'name':name,'votes':0,'parties':set(),'missing':False}
        c=cand[key]
        bp=(r.get('ballot_party') or '').strip().upper()
        if bp:
            c['parties'].add(bp)
        v=(r.get('votes') or '').strip()
        if not v:
            c['missing']=True
        else:
            try:
                c['votes'] += int(float(v))
            except Exception:
                c['missing']=True
    return list(cand.values()), selected_round

def find_by_name(cands, target):
    target=(target or '').strip().lower()
    exact=[c for c in cands if c['name'].strip().lower()==target]
    if len(exact)==1:
        return exact[0]
    partial=[c for c in cands if target and target in c['name'].strip().lower()]
    return partial[0] if len(partial)==1 else None

out=[]
excluded=[]
issues=[]
for race_id, rr in by_race.items():
    first=rr[0]
    key=(int(first['cycle']), first['state_abbrev'], first['office_seat_name'])
    ov=overrides.get(key)
    if ov and ov['action']=='EXCLUDE':
        excluded.append((key, ov['reason']))
        continue
    cands, selected_round=candidate_groups(rr)
    if ov and ov['action']=='ALIGN':
        d=find_by_name(cands,ov['d_side_name'])
        r=find_by_name(cands,ov['r_side_name'])
        rule='manual_alignment_hypothesis_A'
    else:
        dem=[c for c in cands if 'DEM' in c['parties']]
        rep=[c for c in cands if 'REP' in c['parties']]
        d=dem[0] if len(dem)==1 else None
        r=rep[0] if len(rep)==1 else None
        rule='ballot_party_DEM_REP'
    if d is None or r is None or d['missing'] or r['missing']:
        issues.append((key,race_id,'unable_to_identify_complete_D_R_sides'))
        continue
    total_valid=sum(c['votes'] for c in cands if not c['missing'])
    dr_total=d['votes']+r['votes']
    if total_valid<=0 or dr_total<=0:
        issues.append((key,race_id,'nonpositive_vote_total'))
        continue
    total_margin=100.0*(d['votes']-r['votes'])/total_valid
    two_party_margin=100.0*(d['votes']-r['votes'])/dr_total
    out.append({
        'race_id':race_id,
        'cycle':int(first['cycle']),
        'state_abbrev':first['state_abbrev'],
        'state':first['state'],
        'seat':first['office_seat_name'],
        'special':str(first.get('special','')).lower(),
        'd_side_candidate':d['name'],
        'r_side_candidate':r['name'],
        'd_votes':d['votes'],
        'r_votes':r['votes'],
        'total_valid_candidate_votes':total_valid,
        'dr_votes':dr_total,
        'margin_d_minus_r_total_pctpt':f'{total_margin:.8f}',
        'margin_d_minus_r_two_party_pctpt':f'{two_party_margin:.8f}',
        'direction_actual':'D' if d['votes']>r['votes'] else ('R' if r['votes']>d['votes'] else 'TIE'),
        'alignment_rule':rule,
        'ranked_choice_round_used':selected_round
    })

out.sort(key=lambda r:(r['cycle'],r['state_abbrev'],r['seat']))
fields=list(out[0].keys()) if out else []
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    w.writerows(out)

counts=defaultdict(int)
for r in out:
    counts[r['cycle']]+=1

lines=[
    '# GitHub Actions run: Core V2-R headline target panel, Hypothesis A',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Scope: 2014, 2018, 2022 Senate general elections',
    '',
    '## Result',
    '',
    f'- Included races: {len(out)}',
    f'- Excluded by Hypothesis A: {len(excluded)}',
    f'- Unresolved processing issues: {len(issues)}',
    f"- Cycle counts: 2014={counts[2014]}, 2018={counts[2018]}, 2022={counts[2022]}",
    '',
    '## Margin definitions preserved',
    '',
    '- margin_d_minus_r_total_pctpt = (D-side votes - R-side votes) / all valid candidate votes * 100',
    '- margin_d_minus_r_two_party_pctpt = (D-side votes - R-side votes) / (D-side + R-side votes) * 100',
    '',
    'The surviving handoff does not uniquely identify which target-margin denominator the original Core V2 used, so both are retained. Neither is discarded until OOS reproduction resolves the ambiguity.',
    '',
    '## Hypothesis A alignment',
    '',
    '- 2018 ME Angus King -> Democratic-aligned side',
    '- 2018 VT Bernie Sanders -> Democratic-aligned side',
    '- Exclude 2014 AL, 2014 KS, 2018 CA, 2022 AK, 2022 UT',
    '- Ordinary special elections remain included when a unique D and R side exists',
    '- Fusion ballot lines for the same candidate are aggregated',
    '- Ranked-choice records use the maximum recorded round rather than summing rounds',
    '',
    '## Status',
    '',
    'This is a reconstruction hypothesis, not an assertion that the original Core V2 used exactly these rules.',
    '',
    '## Output',
    '',
    '- data/processed/core_v2r_headline_target_hypothesis_A.csv',
    '',
    '## Next',
    '',
    'Build the 2006-2022 partisan-alignment override map and canonical OOS target panel, then add PVI and SameSeat before fitting any model.'
]
if excluded:
    lines += ['', '## Excluded races', '']
    for key,reason in excluded:
        lines.append(f'- {key[0]} {key[1]} {key[2]}: {reason}')
if issues:
    lines += ['', '## Processing issues', '']
    for key,race_id,reason in issues:
        lines.append(f'- {key} race_id={race_id}: {reason}')
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:35]))