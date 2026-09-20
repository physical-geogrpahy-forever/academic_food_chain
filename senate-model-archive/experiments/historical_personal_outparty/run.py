#!/usr/bin/env python3
import csv, itertools, runpy
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/historical_personal_outparty/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0350_historical-personal-outparty-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ps=runpy.run_path(str(STACK))
hist=ps['hist']
base_ns=ps['ns']
races=base_ns['races']
pvi=base_ns['pvi']
rows=ps['rows']

# Race structural lookup and candidate IDs.
rowby={(int(r['cycle']),str(r['race_id'])):r for r in rows}
raceby={(int(r['cycle']),str(r['race_id'])):r for r in races}

# Cycle-adjusted candidate overperformance from completed Senate races.
rawperf=[]
bycycle=defaultdict(list)
for r in races:
    rid=str(r['race_id']); cyc=int(r['cycle'])
    if rid not in pvi:continue
    resid=float(r['y'])-float(pvi[rid])
    bycycle[cyc].append((r,resid))

for cyc,items in bycycle.items():
    if len(items)<3:continue
    mean=sum(res for _,res in items)/len(items)
    for r,res in items:
        adj=res-mean
        if r.get('d_pid'):
            rawperf.append({'pid':r['d_pid'],'cycle':cyc,'score':adj,'race_id':str(r['race_id']),'side':'D'})
        if r.get('r_pid'):
            rawperf.append({'pid':r['r_pid'],'cycle':cyc,'score':-adj,'race_id':str(r['race_id']),'side':'R'})

by_pid=defaultdict(list)
for x in rawperf:by_pid[x['pid']].append(x)

def prior_personal(pid,cycle):
    vals=[x['score'] for x in by_pid.get(pid,[]) if x['cycle']<cycle]
    if not vals:return 0.0,0
    return sum(vals)/len(vals),len(vals)

# Add out-party flag and historical personal score to every rolling poll-baseline row.
data=[]
for h in hist:
    key=(int(h['cycle']),str(h['race_id']))
    s=rowby.get(key); rr=raceby.get(key)
    if s is None or rr is None:continue
    outparty=int(s.get('outparty',0))
    dpv,dn=prior_personal(rr.get('d_pid',''),int(h['cycle']))
    rpv,rn=prior_personal(rr.get('r_pid',''),int(h['cycle']))
    data.append({**h,'outparty':outparty,'pvi':float(s['pvi']),
                 'dpv':dpv,'dn':dn,'rpv':rpv,'rn':rn})

GAMMA=[0,1,2,3,4,5,6,8,10,12,15,20]
DELTA=[0,0.1,0.2,0.3,0.4,0.5,0.75,1.0,1.5]
KGRID=[0.5,1,2,4,8,16]
THRESH=[2,4,6,8,10,15,25,999]
HOST=[0,0.05,0.1,0.2,0.3]

def signed_personal(r,k):
    if r['outparty']==1:
        return r['dpv']*r['dn']/(r['dn']+k) if r['dn'] else 0.0
    if r['outparty']==-1:
        return -(r['rpv']*r['rn']/(r['rn']+k) if r['rn'] else 0.0)
    return 0.0

def predict(r,gamma,delta,k,thr,host):
    p=float(r['posterior'])
    if r['outparty']==0 or abs(p)>thr:return p
    penalty=(gamma+host*abs(float(r['pvi'])))*r['outparty']
    return p-penalty+delta*signed_personal(r,k)

def evaluate(dat,gamma,delta,k,thr,host):
    ok=flips=0
    for r in dat:
        q=predict(r,gamma,delta,k,thr,host)
        ok+=int((q>0)==(float(r['actual'])>0))
        flips+=int((q>0)!=(float(r['posterior'])>0))
    return ok,flips

OUTER=[2014,2018,2022]
choices=[];pred=[]
for tc in OUTER:
    train=[r for r in data if int(r['cycle'])<tc]
    test=[r for r in data if int(r['cycle'])==tc]
    cand=[]
    for gamma,delta,k,thr,host in itertools.product(GAMMA,DELTA,KGRID,THRESH,HOST):
        ok,flips=evaluate(train,gamma,delta,k,thr,host)
        complexity=gamma+delta+k/10+host*10+(0 if thr==999 else 1)
        cand.append((-ok,flips,complexity,gamma,delta,k,thr,host))
    cand.sort(key=lambda z:(z[0],z[1],z[2]))
    z=cand[0];ok=-z[0];flips=z[1];gamma,delta,k,thr,host=z[3:]
    choices.append({'test_cycle':tc,'gamma_outparty':gamma,'delta_personal':delta,'personal_k':k,'posterior_threshold':thr,
                    'hostility_slope':host,'train_n':len(train),'train_correct':ok,'train_accuracy_pct':100*ok/len(train),
                    'train_flips':flips,'top12':' | '.join(f'g{q[3]} d{q[4]} k{q[5]} t{q[6]} h{q[7]} correct={-q[0]} flips={q[1]}' for q in cand[:12])})
    for r in test:
        q=predict(r,gamma,delta,k,thr,host)
        pred.append({**r,'adjusted':q,'signed_personal':signed_personal(r,k),
                     'baseline_correct':int((float(r['posterior'])>0)==(float(r['actual'])>0)),
                     'adjusted_correct':int((q>0)==(float(r['actual'])>0)),
                     'gamma_outparty':gamma,'delta_personal':delta,'personal_k':k,'posterior_threshold':thr,'hostility_slope':host})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if int(r['cycle'])==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum((r['adjusted']>0)!=(float(r['posterior'])>0) for r in rr)})

for fn,arr in [('historical_personal_summary.csv',summary),('historical_personal_choices.csv',choices),('historical_personal_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
comb=summary[0]
lines=['# Historical PersonalVote + OutPartyIncumbent direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Baseline: fixed 45-day poll blend at 94/99.',
       '- Candidate PersonalVote is reconstructed for historical Senate candidates from prior completed Senate races.',
       '- Prior candidate overperformance = candidate-side residual from PVI after subtracting the same-cycle mean Senate residual.',
       '- Only races before the target cycle enter each candidate personal history.',
       '- Out-party penalty, personal protection, hostility interaction, shrinkage, and posterior threshold are selected using earlier cycles only.','',
       '## Result','',
       '| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected parameters','',
          '| test | gamma | personal delta | k | threshold | hostility slope | train accuracy | flips |',
          '|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['gamma_outparty']} | {r['delta_personal']} | {r['personal_k']} | {r['posterior_threshold']} | {r['hostility_slope']} | {r['train_accuracy_pct']:.1f}% | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, {float(r['posterior']):.2f} -> {r['adjusted']:.2f}, signed personal={r['signed_personal']:.2f}")
lines += ['','## Decision','',
          f"- Combined adjusted result: {comb['adjusted_correct']}/{comb['n']} = {comb['adjusted_accuracy_pct']:.1f}%.",
          '- Adopt only if this exceeds 94/99 and the gain survives cycle-by-cycle inspection.','',
          '## Outputs','',
          '- experiments/historical_personal_outparty/results/historical_personal_summary.csv',
          '- experiments/historical_personal_outparty/results/historical_personal_choices.csv',
          '- experiments/historical_personal_outparty/results/historical_personal_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
