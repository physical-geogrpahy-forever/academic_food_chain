#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
HOUSE=ROOT/'data/processed/source_snapshots/election_results_house_d7a7cff101da.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
OUT=ROOT/'data/processed/core_v2r_headline_candidate_experience_audit.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0118_candidate-experience-auto-audit.md'

def truth(v): return str(v).strip().lower()=='true'

def load(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

target=load(TARGET); sen=load(SEN); house=load(HOUSE); gov=load(GOV)

# Identify selected candidate politician_id within each headline race.
sen_by_race=defaultdict(list)
for r in sen:
    if r.get('stage')=='general': sen_by_race[r['race_id']].append(r)

def normalize(s): return ' '.join((s or '').lower().replace('.','').replace(',','').split())

def find_candidate_rows(race_rows,name):
    n=normalize(name)
    exact=[r for r in race_rows if normalize(r.get('candidate_name'))==n]
    if exact: return exact
    partial=[r for r in race_rows if n and (n in normalize(r.get('candidate_name')) or normalize(r.get('candidate_name')) in n)]
    return partial

# Previous winners by politician_id.
def winner_index(rows):
    idx=defaultdict(list)
    for r in rows:
        pid=(r.get('politician_id') or '').strip()
        if not pid or r.get('stage')!='general' or not truth(r.get('winner','false')): continue
        try: cyc=int(r['cycle'])
        except Exception: continue
        idx[pid].append(r)
    return idx

sen_win=winner_index(sen); house_win=winner_index(house); gov_win=winner_index(gov)

# Most recent prior Senate winner for state+class, used only as an election-history incumbency proxy.
same_seat_winners=defaultdict(list)
for r in sen:
    if r.get('stage')!='general' or not truth(r.get('winner','false')): continue
    pid=(r.get('politician_id') or '').strip()
    if not pid: continue
    try: cyc=int(r['cycle'])
    except Exception: continue
    same_seat_winners[(r['state_abbrev'],r['office_seat_name'])].append((cyc,pid,r.get('candidate_name') or '',r['race_id']))

out=[]; unresolved=[]
for race in target:
    cyc=int(race['cycle']); rr=sen_by_race[race['race_id']]
    sides=[]
    for side,name in [('D',race['d_side_candidate']),('R',race['r_side_candidate'])]:
        cr=find_candidate_rows(rr,name)
        pids=sorted({(r.get('politician_id') or '').strip() for r in cr if (r.get('politician_id') or '').strip()})
        pid=pids[0] if len(pids)==1 else ''
        if len(pids)!=1: unresolved.append((race['cycle'],race['state_abbrev'],side,name,'politician_id_not_unique'))
        def prior_any(index):
            return bool(pid and any(int(x['cycle'])<cyc for x in index.get(pid,[])))
        s_exp=prior_any(sen_win); h_exp=prior_any(house_win); g_exp=prior_any(gov_win)
        seat_hist=[x for x in same_seat_winners.get((race['state_abbrev'],race['seat']),[]) if x[0]<cyc]
        latest=max(seat_hist,key=lambda x:x[0]) if seat_hist else None
        inc_proxy=bool(pid and latest and latest[1]==pid)
        sides.append({
            'side':side,'name':name,'politician_id':pid,
            'senate_prior_election_win':s_exp,'house_prior_election_win':h_exp,'governor_prior_election_win':g_exp,
            'incumbency_election_history_proxy':inc_proxy,
            'latest_prior_same_seat_winner_cycle':'' if latest is None else latest[0],
            'latest_prior_same_seat_winner_name':'' if latest is None else latest[2]
        })
    d,r=sides
    out.append({
        'race_id':race['race_id'],'cycle':cyc,'state_abbrev':race['state_abbrev'],'seat':race['seat'],
        'd_candidate':d['name'],'d_politician_id':d['politician_id'],
        'r_candidate':r['name'],'r_politician_id':r['politician_id'],
        'd_senate_prior_election_win':str(d['senate_prior_election_win']).lower(),
        'r_senate_prior_election_win':str(r['senate_prior_election_win']).lower(),
        'SenateExperienceDiff_auto':int(d['senate_prior_election_win'])-int(r['senate_prior_election_win']),
        'd_governor_prior_election_win':str(d['governor_prior_election_win']).lower(),
        'r_governor_prior_election_win':str(r['governor_prior_election_win']).lower(),
        'GovernorExperienceDiff_auto':int(d['governor_prior_election_win'])-int(r['governor_prior_election_win']),
        'd_house_prior_election_win':str(d['house_prior_election_win']).lower(),
        'r_house_prior_election_win':str(r['house_prior_election_win']).lower(),
        'HouseExperienceDiff_auto':int(d['house_prior_election_win'])-int(r['house_prior_election_win']),
        'd_incumbency_election_history_proxy':str(d['incumbency_election_history_proxy']).lower(),
        'r_incumbency_election_history_proxy':str(r['incumbency_election_history_proxy']).lower(),
        'IncumbencyDiff_proxy':int(d['incumbency_election_history_proxy'])-int(r['incumbency_election_history_proxy']),
        'd_latest_prior_same_seat_winner_cycle':d['latest_prior_same_seat_winner_cycle'],
        'r_latest_prior_same_seat_winner_cycle':r['latest_prior_same_seat_winner_cycle'],
        'd_latest_prior_same_seat_winner_name':d['latest_prior_same_seat_winner_name'],
        'r_latest_prior_same_seat_winner_name':r['latest_prior_same_seat_winner_name']
    })

fields=list(out[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)

matched=sum(bool(r['d_politician_id'])+bool(r['r_politician_id']) for r in out)
total=2*len(out)
senD=sum(r['d_senate_prior_election_win']=='true' for r in out); senR=sum(r['r_senate_prior_election_win']=='true' for r in out)
govD=sum(r['d_governor_prior_election_win']=='true' for r in out); govR=sum(r['r_governor_prior_election_win']=='true' for r in out)
houD=sum(r['d_house_prior_election_win']=='true' for r in out); houR=sum(r['r_house_prior_election_win']=='true' for r in out)
incD=sum(r['d_incumbency_election_history_proxy']=='true' for r in out); incR=sum(r['r_incumbency_election_history_proxy']=='true' for r in out)
lines=[
 '# GitHub Actions run: candidate experience auto-audit',
 '',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Execution: GitHub Actions',
 '- Headline races: 99',
 f'- Candidate politician_id matched uniquely: {matched}/{total}',
 f'- Unresolved candidate-id cases: {len(unresolved)}',
 '',
 '## Automatic pre-election history flags',
 '',
 f'- prior Senate general-election winners: D-side {senD}, R-side {senR}',
 f'- prior Governor general-election winners: D-side {govD}, R-side {govR}',
 f'- prior House general-election winners: D-side {houD}, R-side {houR}',
 f'- same-seat prior-winner incumbency proxy: D-side {incD}, R-side {incR}',
 '',
 '## Important limitation',
 '',
 'These are reconstruction audit variables, not yet authoritative Core V2 variables. A prior election win can miss appointed officeholders, succession to a governorship, and service that did not originate in a general-election win. The incumbency field is explicitly a proxy based on the most recent prior winner of the same state/class, not a final incumbency coding.',
 '',
 'No test-election outcome is used to create these flags; only election history strictly before each Senate cycle is queried.',
 '',
 '## Outputs',
 '',
 '- data/processed/source_snapshots/election_results_house_d7a7cff101da.csv',
 '- data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv',
 '- data/processed/source_snapshots/candidate_experience_source_manifest.csv',
 '- data/processed/core_v2r_headline_candidate_experience_audit.csv',
 '',
 '## Next',
 '',
 'Identify false negatives caused by appointments/succession and compare automatic experience flags with official biographies before joining them to the Core V2-R design matrix.'
]
if unresolved:
    lines += ['', '## Unresolved candidate IDs', '']
    for x in unresolved: lines.append('- '+' | '.join(map(str,x)))
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:35]))