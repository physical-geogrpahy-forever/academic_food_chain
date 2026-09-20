#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
EXPAUD=ROOT/'data/processed/core_v2r_headline_candidate_experience_audit.csv'
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
HOUSE=ROOT/'data/processed/source_snapshots/election_results_house_d7a7cff101da.csv'
PRES=ROOT/'data/processed/presidential_state_lean.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
LONG=ROOT/'data/processed/core_v2r_personal_vote_prior_statewide_history.csv'
STATS=ROOT/'data/processed/core_v2r_personal_vote_sufficient_statistics.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0145_personal-vote-sufficient-statistics.md'

def load(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

target=load(TARGET); exp=load(EXPAUD); sen=load(SEN); gov=load(GOV); pres=load(PRES)
align=load(ALIGN)

# presidential state lean -> PVI for any later election cycle
lean={}
pres_years=set()
for r in pres:
    y=int(r['cycle']); st=r['state_abbrev']; pres_years.add(y)
    lean[(y,st)]=float(r['lean_vs_national_pctpt'])
pres_years=sorted(pres_years)

def pvi_for(cycle,state):
    ys=[y for y in pres_years if y<cycle and (y,state) in lean]
    if len(ys)<2: return None
    recent,older=ys[-1],ys[-2]
    return 0.67*lean[(recent,state)]+0.33*lean[(older,state)]

override={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

def parse_round(v):
    try: return int(float(v)) if str(v).strip() else None
    except: return None

def norm(s):
    return ' '.join((s or '').lower().replace('.','').replace(',','').split())

def build_statewide(rows,office):
    by=defaultdict(list)
    for r in rows:
        if r.get('stage')!='general': continue
        try: cyc=int(r['cycle'])
        except: continue
        by[r['race_id']].append(r)
    out=[]; irregular=[]
    for race_id, rr in by.items():
        first=rr[0]; cyc=int(first['cycle']); state=first['state_abbrev']
        rounds=[parse_round(x.get('ranked_choice_round')) for x in rr]
        nums=[x for x in rounds if x is not None]
        use=rr
        if nums:
            mx=max(nums); sub=[x for x in rr if parse_round(x.get('ranked_choice_round'))==mx]
            if sub: use=sub
        cand={}
        for x in use:
            pid=(x.get('politician_id') or '').strip()
            key=pid or (x.get('candidate_id') or '').strip() or x.get('candidate_name') or ''
            if not key: continue
            c=cand.setdefault(key,{'politician_id':pid,'candidate_name':x.get('candidate_name') or '','votes':0,'parties':set(),'missing':False})
            bp=(x.get('ballot_party') or '').strip().upper()
            pp=(x.get('party') or '').strip().upper()
            if bp: c['parties'].add(bp)
            if pp: c['parties'].add(pp)
            v=(x.get('votes') or '').strip()
            if not v: c['missing']=True
            else:
                try: c['votes']+=int(float(v))
                except: c['missing']=True
        cs=list(cand.values())
        d=r=None; rule='standard_dem_rep'
        if office=='Senate':
            key=(cyc,state,first.get('office_seat_name') or '')
            ov=override.get(key)
            if ov and ov['action']=='ALIGN':
                ds=[c for c in cs if norm(c['candidate_name'])==norm(ov['d_side_name'])]
                rs=[c for c in cs if norm(c['candidate_name'])==norm(ov['r_side_name'])]
                d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None
                rule='alignment_override'
            elif ov and ov['action'] in {'EXCLUDE','REVIEW'}:
                irregular.append((office,cyc,state,race_id,ov['action']))
                continue
        if d is None and r is None:
            ds=[c for c in cs if 'DEM' in c['parties']]
            rs=[c for c in cs if 'REP' in c['parties']]
            d=ds[0] if len(ds)==1 else None
            r=rs[0] if len(rs)==1 else None
        if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0:
            irregular.append((office,cyc,state,race_id,'non_unique_or_missing_D_R'))
            continue
        pvi=pvi_for(cyc,state)
        if pvi is None:
            irregular.append((office,cyc,state,race_id,'pvi_unavailable'))
            continue
        margin=(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0
        out.append({
          'office':office,'race_id':race_id,'cycle':cyc,'state_abbrev':state,
          'seat':first.get('office_seat_name') or '',
          'd_politician_id':d['politician_id'],'d_candidate':d['candidate_name'],
          'r_politician_id':r['politician_id'],'r_candidate':r['candidate_name'],
          'margin_d_minus_r_two_party_pctpt':margin,'pvi_pctpt':pvi,
          'residual_vs_pvi_pctpt':margin-pvi,'alignment_rule':rule
        })
    return out,irregular

senr,sen_bad=build_statewide(sen,'Senate')
govr,gov_bad=build_statewide(gov,'Governor')
statewide=senr+govr

# Leave-one-out office-cycle national residual. This is a diagnostic baseline, not the recovered final National_t.
groups=defaultdict(list)
for i,r in enumerate(statewide):
    groups[(r['office'],r['cycle'])].append(i)
for key,inds in groups.items():
    vals=[statewide[i]['residual_vs_pvi_pctpt'] for i in inds]
    for i in inds:
        others=[statewide[j]['residual_vs_pvi_pctpt'] for j in inds if j!=i]
        statewide[i]['office_cycle_race_count']=len(inds)
        statewide[i]['loo_office_cycle_residual_pctpt']=sum(others)/len(others) if len(others)>=2 else None
        if statewide[i]['loo_office_cycle_residual_pctpt'] is None:
            statewide[i]['candidate_overperf_cycle_adjusted_d_minus_r_pctpt']=None
        else:
            statewide[i]['candidate_overperf_cycle_adjusted_d_minus_r_pctpt']=(
                statewide[i]['margin_d_minus_r_two_party_pctpt']
                - statewide[i]['pvi_pctpt']
                - statewide[i]['loo_office_cycle_residual_pctpt']
            )

# headline candidate IDs
exp_by={r['race_id']:r for r in exp}
headline=[]
for t in target:
    a=exp_by[t['race_id']]
    for side in ['D','R']:
        sl=side.lower()
        headline.append({
          'target_race_id':t['race_id'],'target_cycle':int(t['cycle']),'target_state':t['state_abbrev'],
          'side':side,'candidate_name':t[f'{sl}_side_candidate'],'politician_id':a[f'{sl}_politician_id']
        })

# index prior statewide appearances by politician_id
prior_by=defaultdict(list)
for r in statewide:
    for side in ['D','R']:
        pid=r[f'{side.lower()}_politician_id']
        if pid:
            own_raw = r['residual_vs_pvi_pctpt'] if side=='D' else -r['residual_vs_pvi_pctpt']
            adj=r['candidate_overperf_cycle_adjusted_d_minus_r_pctpt']
            own_adj = None if adj is None else (adj if side=='D' else -adj)
            prior_by[pid].append({
              **r,'candidate_side':side,
              'own_party_overperf_vs_pvi_pctpt':own_raw,
              'own_party_overperf_cycle_adjusted_pctpt':own_adj
            })

long=[]
stats=[]
for h in headline:
    hist=[r for r in prior_by.get(h['politician_id'],[]) if r['cycle']<h['target_cycle']]
    hist.sort(key=lambda r:(r['cycle'],r['office'],r['race_id']))
    for r in hist:
        long.append({
          'target_race_id':h['target_race_id'],'target_cycle':h['target_cycle'],'target_state':h['target_state'],
          'target_side':h['side'],'target_candidate':h['candidate_name'],'politician_id':h['politician_id'],
          'prior_office':r['office'],'prior_cycle':r['cycle'],'prior_state':r['state_abbrev'],'prior_race_id':r['race_id'],
          'prior_candidate_side':r['candidate_side'],
          'prior_margin_d_minus_r_two_party_pctpt':f"{r['margin_d_minus_r_two_party_pctpt']:.8f}",
          'prior_pvi_pctpt':f"{r['pvi_pctpt']:.8f}",
          'prior_residual_vs_pvi_pctpt':f"{r['residual_vs_pvi_pctpt']:.8f}",
          'prior_office_cycle_race_count':r['office_cycle_race_count'],
          'loo_office_cycle_residual_pctpt':'' if r['loo_office_cycle_residual_pctpt'] is None else f"{r['loo_office_cycle_residual_pctpt']:.8f}",
          'own_party_overperf_vs_pvi_pctpt':f"{r['own_party_overperf_vs_pvi_pctpt']:.8f}",
          'own_party_overperf_cycle_adjusted_pctpt':'' if r['own_party_overperf_cycle_adjusted_pctpt'] is None else f"{r['own_party_overperf_cycle_adjusted_pctpt']:.8f}",
          'alignment_rule':r['alignment_rule']
        })
    raw=[r['own_party_overperf_vs_pvi_pctpt'] for r in hist]
    adj=[r['own_party_overperf_cycle_adjusted_pctpt'] for r in hist if r['own_party_overperf_cycle_adjusted_pctpt'] is not None]
    senhist=[r for r in hist if r['office']=='Senate']; govhist=[r for r in hist if r['office']=='Governor']
    stats.append({
      'target_race_id':h['target_race_id'],'target_cycle':h['target_cycle'],'target_state':h['target_state'],
      'side':h['side'],'candidate_name':h['candidate_name'],'politician_id':h['politician_id'],
      'prior_statewide_count':len(hist),'prior_senate_count':len(senhist),'prior_governor_count':len(govhist),
      'mean_own_party_overperf_vs_pvi_pctpt':'' if not raw else f"{sum(raw)/len(raw):.8f}",
      'mean_own_party_overperf_cycle_adjusted_pctpt':'' if not adj else f"{sum(adj)/len(adj):.8f}",
      'latest_prior_statewide_cycle':'' if not hist else max(r['cycle'] for r in hist),
      'personal_vote_finalized':'false'
    })

long_fields=[
'target_race_id','target_cycle','target_state','target_side','target_candidate','politician_id',
'prior_office','prior_cycle','prior_state','prior_race_id','prior_candidate_side',
'prior_margin_d_minus_r_two_party_pctpt','prior_pvi_pctpt','prior_residual_vs_pvi_pctpt',
'prior_office_cycle_race_count','loo_office_cycle_residual_pctpt',
'own_party_overperf_vs_pvi_pctpt','own_party_overperf_cycle_adjusted_pctpt','alignment_rule']
with LONG.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=long_fields); w.writeheader(); w.writerows(long)
stats_fields=list(stats[0].keys())
with STATS.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=stats_fields); w.writeheader(); w.writerows(stats)

with_hist=sum(int(r['prior_statewide_count'])>0 for r in stats)
with_adj=sum(bool(r['mean_own_party_overperf_cycle_adjusted_pctpt']) for r in stats)
lines=[
 '# GitHub Actions run: PersonalVote sufficient statistics v1','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Headline candidate-side rows: {len(stats)}',
 f'- Candidate-side rows with at least one prior statewide Senate/Governor election: {with_hist}',
 f'- Candidate-side rows with cycle-adjusted prior overperformance available: {with_adj}',
 f'- Long prior-statewide history rows: {len(long)}','',
 '## Status','',
 'This is not a finalized PersonalVoteDiff. The exact Core V2 shrinkage formula, statewide-vs-district information weights, and hyperparameters were not recovered. The pipeline therefore preserves sufficient statistics first and does not tune a shrinkage constant against 2014/2018/2022 headline outcomes.','',
 '## Prior-race diagnostic','',
 'For a completed prior statewide race:','',
 '1. PVI-only residual = actual D-R two-party margin - reconstructed state PVI.',
 '2. A leave-one-out office-cycle residual mean is computed from other Senate races or other gubernatorial races in that same cycle.',
 '3. Cycle-adjusted candidate overperformance = actual margin - PVI - leave-one-out office-cycle residual.',
 '4. Republican candidate values are sign-flipped so positive always means the candidate outperformed their own party-side baseline.','',
 'The leave-one-out office-cycle adjustment is a reconstruction diagnostic for prior personal performance. It is not claimed to be the recovered Core V2 National_t.','',
 '## Leakage rule','',
 'Only prior races with prior_cycle < target_cycle are attached. Same-cycle races are conservatively excluded because the exact election date ordering is not reconstructed here.','',
 '## House elections','',
 'House performance is not converted into PersonalVote using state PVI because House races are district-level. House experience remains available separately, and district-level personal-vote evidence can be added later only with a district partisan baseline.','',
 '## No final shrinkage yet','',
 'The output intentionally keeps count, statewide office type, raw mean, and cycle-adjusted mean separately. A final PersonalVoteDiff must choose pooling/shrinkage only inside rolling nested OOS, never from headline test outcomes.','',
 '## Outputs','',
 '- data/processed/core_v2r_personal_vote_prior_statewide_history.csv',
 '- data/processed/core_v2r_personal_vote_sufficient_statistics.csv','',
 '## Next','',
 'Join these sufficient statistics to the headline design matrix as audit-only columns, reconstruct National_t and RelativeEconomicGrowth, then define candidate-personal shrinkage inside the rolling OOS training loop.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
