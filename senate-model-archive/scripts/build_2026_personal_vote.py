#!/usr/bin/env python3
import csv,re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
PRES=ROOT/'data/processed/presidential_state_lean.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
OUT=ROOT/'data/snapshots/2026_personal_vote_core.csv'
HIST=ROOT/'data/snapshots/2026_personal_vote_prior_history.csv'
DOC=ROOT/'docs/analysis/2026_PERSONAL_VOTE_CORE.md'

TARGET=[
('AK','D','Mary Peltola'),('AK','R','Dan Sullivan'),
('GA','D','Jon Ossoff'),('GA','R','Mike Collins'),
('IA','D','Josh Turek'),('IA','R','Ashley Hinson'),
('ME','D','Troy Jackson'),('ME','R','Susan Collins'),
('MI','D','Abdul El-Sayed'),('MI','R','Mike Rogers'),
('NH','D','Chris Pappas'),('NH','R','John Sununu'),
('NC','D','Roy Cooper'),('NC','R','Michael Whatley'),
('OH','D','Sherrod Brown'),('OH','R','Jon Husted'),
('TX','D','James Talarico'),('TX','R','Ken Paxton')
]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):
    s=(s or '').lower()
    s=re.sub(r'\b(jr|sr|ii|iii|iv|mr|mrs|ms|dr|sen|governor|gov)\b',' ',s)
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def parse_round(v):
    try:return int(float(v)) if str(v).strip() else None
    except:return None

sen=load(SEN);gov=load(GOV);pres=load(PRES);align=load(ALIGN)
lean={(int(r['cycle']),r['state_abbrev']):float(r['lean_vs_national_pctpt']) for r in pres}
pres_years=sorted(set(int(r['cycle']) for r in pres))
def pvi_for(cycle,state):
    ys=[y for y in pres_years if y<cycle and (y,state) in lean]
    if len(ys)<2:return None
    return .67*lean[(ys[-1],state)]+.33*lean[(ys[-2],state)]

override={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

def build_statewide(rows,office):
    by=defaultdict(list)
    for r in rows:
        if (r.get('stage') or '').lower()!='general':continue
        try:cyc=int(r['cycle'])
        except:continue
        by[str(r['race_id'])].append(r)
    out=[]
    for rid,rr in by.items():
        first=rr[0];cyc=int(first['cycle']);st=first['state_abbrev']
        nums=[parse_round(x.get('ranked_choice_round')) for x in rr]
        nums=[x for x in nums if x is not None]
        use=rr
        if nums:
            mx=max(nums);sub=[x for x in rr if parse_round(x.get('ranked_choice_round'))==mx]
            if sub:use=sub
        cand={}
        for x in use:
            pid=(x.get('politician_id') or '').strip()
            key=pid or (x.get('candidate_id') or '').strip() or (x.get('candidate_name') or '')
            if not key:continue
            c=cand.setdefault(key,{'pid':pid,'name':x.get('candidate_name') or '','votes':0,'parties':set(),'missing':False})
            for q in ((x.get('ballot_party') or ''),(x.get('party') or '')):
                if q.strip():c['parties'].add(q.strip().upper())
            v=(x.get('votes') or '').strip()
            if not v:c['missing']=True
            else:
                try:c['votes']+=int(float(v))
                except:c['missing']=True
        cs=list(cand.values());d=r=None;rule='standard_dem_rep'
        if office=='Senate':
            ov=override.get((cyc,st,first.get('office_seat_name') or ''))
            if ov and ov['action']=='ALIGN':
                ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])]
                rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
                d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None;rule='alignment_override'
            elif ov and ov['action'] in {'EXCLUDE','REVIEW'}:continue
        if d is None and r is None:
            ds=[c for c in cs if 'DEM' in c['parties']]
            rs=[c for c in cs if 'REP' in c['parties']]
            d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None
        if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0:continue
        pvi=pvi_for(cyc,st)
        if pvi is None:continue
        margin=100*(d['votes']-r['votes'])/(d['votes']+r['votes'])
        out.append({'office':office,'race_id':rid,'cycle':cyc,'state_abbrev':st,
                    'd_name':d['name'],'d_pid':d['pid'],'r_name':r['name'],'r_pid':r['pid'],
                    'margin':margin,'pvi':pvi,'resid':margin-pvi,'rule':rule})
    return out

statewide=build_statewide(sen,'Senate')+build_statewide(gov,'Governor')
groups=defaultdict(list)
for i,r in enumerate(statewide):groups[(r['office'],r['cycle'])].append(i)
for key,inds in groups.items():
    for i in inds:
        others=[statewide[j]['resid'] for j in inds if j!=i]
        statewide[i]['loo']=sum(others)/len(others) if len(others)>=2 else None
        statewide[i]['adj']=None if statewide[i]['loo'] is None else statewide[i]['resid']-statewide[i]['loo']

def score_name(query,cand):
    q=norm(query);n=norm(cand)
    qt=q.split();nt=n.split()
    seq=1 if q==n else SequenceMatcher(None,q,n).ratio()
    surname=1 if qt and nt and qt[-1]==nt[-1] else 0
    first=1 if qt and nt and (qt[0]==nt[0] or qt[0][0]==nt[0][0]) else 0
    return .6*seq+.25*surname+.15*first

history=[];stats=[]
for st,side,name in TARGET:
    candidates=[]
    for r in statewide:
        if r['state_abbrev']!=st or r['cycle']>=2026:continue
        cname=r['d_name'] if side=='D' else r['r_name']
        sc=score_name(name,cname)
        if sc>=.72:
            candidates.append((sc,r,cname))
    # disambiguate by candidate identity via best normalized name cluster
    if candidates:
        best=max(candidates,key=lambda z:z[0])[2]
        bnorm=norm(best)
        selected=[(sc,r,cname) for sc,r,cname in candidates if norm(cname)==bnorm or score_name(best,cname)>=.92]
    else:selected=[]
    own=[]
    for sc,r,cname in sorted(selected,key=lambda z:z[1]['cycle']):
        raw=r['resid'] if side=='D' else -r['resid']
        adj=None if r['adj'] is None else (r['adj'] if side=='D' else -r['adj'])
        own.append((r['cycle'],r['office'],raw,adj,r['race_id'],cname,sc))
        history.append({'state_abbrev':st,'side':side,'target_candidate':name,'matched_candidate':cname,
                        'match_score':sc,'prior_cycle':r['cycle'],'prior_office':r['office'],'prior_race_id':r['race_id'],
                        'own_party_overperf_vs_pvi_pctpt':raw,
                        'own_party_overperf_cycle_adjusted_pctpt':'' if adj is None else adj})
    rawvals=[x[2] for x in own];adjvals=[x[3] for x in own if x[3] is not None]
    stats.append({'state_abbrev':st,'side':side,'candidate_name':name,
                  'matched_name':'' if not selected else selected[0][2],
                  'prior_statewide_count':len(own),
                  'prior_senate_count':sum(x[1]=='Senate' for x in own),
                  'prior_governor_count':sum(x[1]=='Governor' for x in own),
                  'mean_own_party_overperf_vs_pvi_pctpt':'' if not rawvals else sum(rawvals)/len(rawvals),
                  'mean_own_party_overperf_cycle_adjusted_pctpt':'' if not adjvals else sum(adjvals)/len(adjvals),
                  'latest_prior_statewide_cycle':'' if not own else max(x[0] for x in own)})

# race-level D-R PersonalVote difference
by={(r['state_abbrev'],r['side']):r for r in stats}
out=[]
for st in sorted(set(x[0] for x in TARGET)):
    d=by[(st,'D')];r=by[(st,'R')]
    dv=d['mean_own_party_overperf_cycle_adjusted_pctpt'];rv=r['mean_own_party_overperf_cycle_adjusted_pctpt']
    diff='' if dv=='' and rv=='' else (0 if dv=='' else float(dv))-(0 if rv=='' else float(rv))
    out.append({'state_abbrev':st,'candidate_D':d['candidate_name'],'candidate_R':r['candidate_name'],
                'd_prior_statewide_count':d['prior_statewide_count'],'r_prior_statewide_count':r['prior_statewide_count'],
                'd_personal_vote_cycle_adjusted_pctpt':dv,'r_personal_vote_cycle_adjusted_pctpt':rv,
                'PersonalVoteDiff_D_minus_R_pctpt':diff,
                'personal_vote_status':'both_missing' if dv=='' and rv=='' else 'available_with_missing_side_zero_for_diff'})

for path,arr in [(OUT,out),(HIST,history)]:
    with path.open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys()) if arr else ['none'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

lines=['# 2026 Core PersonalVote reconstruction','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Uses prior statewide Senate and Governor general elections only.',
'- PVI is reconstructed from the two previous presidential state leans with 0.67/0.33 weights.',
'- Candidate overperformance is adjusted by leave-one-out office-cycle residual, matching the archived sufficient-statistics procedure.',
'- House and state-office races are not converted into PersonalVote.','',
'| State | D PV | R PV | D-R PV diff | D prior N | R prior N |',
'|---|---:|---:|---:|---:|---:|']
for z in out:
    def fmt(v):return 'NA' if v=='' else f"{float(v):.2f}"
    lines.append(f"| {z['state_abbrev']} | {fmt(z['d_personal_vote_cycle_adjusted_pctpt'])} | {fmt(z['r_personal_vote_cycle_adjusted_pctpt'])} | {fmt(z['PersonalVoteDiff_D_minus_R_pctpt'])} | {z['d_prior_statewide_count']} | {z['r_prior_statewide_count']} |")
lines += ['','## Notes','',
'- A missing candidate-side PersonalVote means no prior Senate/Governor general-election evidence was found; it is not evidence of zero candidate quality.',
'- The race-level difference uses zero only as a neutral placeholder when the opposite candidate has an observed PersonalVote. Both-missing races remain flagged separately.',
'- This file is an input reconstruction and does not change the locked historical model.','',
'## Files','',
'- data/snapshots/2026_personal_vote_core.csv',
'- data/snapshots/2026_personal_vote_prior_history.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
