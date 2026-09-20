#!/usr/bin/env python3
import csv, itertools
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
OUT=ROOT/'experiments/outparty_personal/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0340_outparty-personal-postpoll-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dm=load(DM)
dby={r['race_id']:r for r in dm}

# One row per headline race.
rows=[]
for r in base:
    d=dby[r['race_id']]
    outparty=int(d['OutPartyIncumbent'])
    dpv=float(d['d_personal_mean_overperf_cycle_adjusted_pctpt']) if d['d_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0
    rpv=float(d['r_personal_mean_overperf_cycle_adjusted_pctpt']) if d['r_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0
    dn=int(d['d_personal_prior_statewide_count'] or 0);rn=int(d['r_personal_prior_statewide_count'] or 0)
    rows.append({'cycle':int(r['test_cycle']),'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                 'actual':float(r['actual']),'posterior':float(r['posterior']),
                 'outparty':outparty,'dpv':dpv,'rpv':rpv,'dn':dn,'rn':rn})

GAMMA=[0,1,2,3,4,5,6,8,10,12,15,20]
DELTA=[0,0.1,0.2,0.3,0.4,0.5,0.75,1.0]
KGRID=[0.5,1,2,4,8,16]
THRESH=[2,4,6,8,10,15,25,999]

def signed_inc_pv(r,k):
    if r['outparty']==1:
        return r['dpv']*r['dn']/(r['dn']+k) if r['dn']>0 else 0.0
    if r['outparty']==-1:
        # R incumbent personal vote is R-direction, so negative in D-R margin.
        return -(r['rpv']*r['rn']/(r['rn']+k) if r['rn']>0 else 0.0)
    return 0.0

def predict(r,gamma,delta,k,threshold):
    p=r['posterior']
    if r['outparty']==0 or abs(p)>threshold:
        return p
    return p - gamma*r['outparty'] + delta*signed_inc_pv(r,k)

def evaluate(data,gamma,delta,k,threshold):
    ok=flips=0
    for r in data:
        q=predict(r,gamma,delta,k,threshold)
        ok+=int((q>0)==(r['actual']>0))
        flips+=int((q>0)!=(r['posterior']>0))
    return ok,flips

pred=[];choices=[]
for tc in [2014,2018,2022]:
    train=[r for r in rows if r['cycle']<tc]
    test=[r for r in rows if r['cycle']==tc]
    if not train:
        best=(0,0,0,1,999,0)
    else:
        cand=[]
        for gamma,delta,k,thr in itertools.product(GAMMA,DELTA,KGRID,THRESH):
            ok,flips=evaluate(train,gamma,delta,k,thr)
            # Primary correct count. Tie-break fewer flips, then smaller adjustment complexity.
            complexity=gamma+delta+k/10+(0 if thr==999 else 1)
            cand.append((-ok,flips,complexity,gamma,delta,k,thr))
        cand.sort()
        z=cand[0];best=(-z[0],z[3],z[4],z[5],z[6],z[1])
    ok,gamma,delta,k,thr,trainflips=best
    choices.append({'test_cycle':tc,'gamma_outparty':gamma,'delta_personal':delta,'personal_k':k,'posterior_threshold':thr,
                    'train_n':len(train),'train_correct':ok if train else '',
                    'train_accuracy_pct':(100*ok/len(train) if train else ''),'train_flips':trainflips})
    for r in test:
        q=predict(r,gamma,delta,k,thr)
        pred.append({**r,'adjusted_posterior':q,
                     'baseline_correct':int((r['posterior']>0)==(r['actual']>0)),
                     'adjusted_correct':int((q>0)==(r['actual']>0)),
                     'gamma_outparty':gamma,'delta_personal':delta,'personal_k':k,'posterior_threshold':thr,
                     'signed_inc_personal':signed_inc_pv(r,k)})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum((r['adjusted_posterior']>0)!=(r['posterior']>0) for r in rr)})

for fn,data in [('outparty_personal_summary.csv',summary),('outparty_personal_choices.csv',choices),('outparty_personal_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# OutPartyIncumbent + PersonalVote post-poll direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Baseline: fixed Core V2 poll blend, 94/99 = 94.9%.',
       '- Adjustment is applied only to out-party incumbents and optionally only when posterior margin is within a learned threshold.',
       '- Out-party penalty moves toward the state-favored party.',
       '- Incumbent PersonalVote protects candidates with demonstrated prior overperformance.',
       '- 2018 parameters are learned from 2014 only; 2022 parameters are learned from 2014+2018; 2014 receives no learned adjustment.','',
       '## Result','',
       '| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected parameters','',
          '| test | gamma out-party | delta personal | personal k | posterior threshold | train accuracy | train flips |',
          '|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:
    ta='NA' if r['train_accuracy_pct']=='' else f"{r['train_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['gamma_outparty']} | {r['delta_personal']} | {r['personal_k']} | {r['posterior_threshold']} | {ta} | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:
    lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, posterior {r['posterior']:.2f} -> {r['adjusted_posterior']:.2f}")
lines += ['','## Decision','',
          'Adopt only if combined adjusted direction accuracy exceeds 94/99 and the gain comes from parameters selected on earlier cycles only.','',
          '## Outputs','',
          '- experiments/outparty_personal/results/outparty_personal_summary.csv',
          '- experiments/outparty_personal/results/outparty_personal_choices.csv',
          '- experiments/outparty_personal/results/outparty_personal_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
