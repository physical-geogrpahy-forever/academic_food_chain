#!/usr/bin/env python3
import csv, itertools
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
OUT=ROOT/'experiments/outparty_favored/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0350_outparty-incumbent-favored-posterior-rule.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dm=load(DM);dby={r['race_id']:r for r in dm}

rows=[]
for r in base:
    d=dby[r['race_id']]
    outparty=int(d['OutPartyIncumbent'])
    if outparty==1:
        pv=float(d['d_personal_mean_overperf_cycle_adjusted_pctpt']) if d['d_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0
        n=int(d['d_personal_prior_statewide_count'] or 0)
    elif outparty==-1:
        pv=float(d['r_personal_mean_overperf_cycle_adjusted_pctpt']) if d['r_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0
        n=int(d['r_personal_prior_statewide_count'] or 0)
    else:
        pv=0.0;n=0
    rows.append({'cycle':int(r['test_cycle']),'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                 'actual':float(r['actual']),'posterior':float(r['posterior']),'outparty':outparty,
                 'pv_raw':pv,'pv_n':n})

THRESH=[0,3,5,7,8,9,10,12,15,20,25,30,40,999]
KGRID=[0.5,1,2,4,8,16]
GAMMA=[1,2,3,4,5,6,8,10,12,15,20]

def shrunk_pv(r,k):
    return r['pv_raw']*r['pv_n']/(r['pv_n']+k) if r['pv_n']>0 else 0.0

def incumbent_favored(r):
    if r['outparty']==1:return r['posterior']>0
    if r['outparty']==-1:return r['posterior']<0
    return False

def predict(r,thr,k,gamma):
    p=r['posterior']
    if r['outparty']==0 or not incumbent_favored(r):
        return p
    pv=abs(shrunk_pv(r,k))
    if pv>=thr:
        return p
    return p-gamma*r['outparty']

def evalset(dat,thr,k,gamma):
    ok=flips=0
    for r in dat:
        q=predict(r,thr,k,gamma)
        ok+=int((q>0)==(r['actual']>0))
        flips+=int((q>0)!=(r['posterior']>0))
    return ok,flips

pred=[];choices=[]
for tc in [2014,2018,2022]:
    train=[r for r in rows if r['cycle']<tc]
    test=[r for r in rows if r['cycle']==tc]
    if not train:
        thr,k,gamma=0,1,1;ok=0;flips=0
    else:
        cand=[]
        for thr,k,gamma in itertools.product(THRESH,KGRID,GAMMA):
            ok,flips=evalset(train,thr,k,gamma)
            complexity=gamma+(999 if thr==999 else thr)/100+k/100
            cand.append((-ok,flips,complexity,thr,k,gamma))
        cand.sort(key=lambda z:(z[0],z[1],z[2]))
        z=cand[0];ok=-z[0];flips=z[1];thr,k,gamma=z[3],z[4],z[5]
    choices.append({'test_cycle':tc,'pv_threshold':thr,'personal_k':k,'gamma':gamma,
                    'train_n':len(train),'train_correct':ok if train else '',
                    'train_accuracy_pct':(100*ok/len(train) if train else ''),'train_flips':flips})
    for r in test:
        q=predict(r,thr,k,gamma)
        pred.append({**r,'shrunk_personal':shrunk_pv(r,k),'adjusted_posterior':q,
                     'baseline_correct':int((r['posterior']>0)==(r['actual']>0)),
                     'adjusted_correct':int((q>0)==(r['actual']>0)),
                     'rule_eligible':int(r['outparty']!=0 and incumbent_favored(r)),
                     'pv_threshold':thr,'personal_k':k,'gamma':gamma})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum((r['adjusted_posterior']>0)!=(r['posterior']>0) for r in rr)})

for fn,data in [('favored_summary.csv',summary),('favored_choices.csv',choices),('favored_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# Out-party incumbent favored-posterior rule','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Baseline: fixed Core V2 poll blend, 94/99.',
       '- Rule is eligible only when an out-party incumbent exists AND the fixed-poll posterior still favors that incumbent.',
       '- Strong incumbent PersonalVote can protect the incumbent from the state-partisan penalty.',
       '- Parameters for each outer cycle are selected only from earlier cycles by number of correctly classified winners.','',
       '## Result','',
       '| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected parameters','',
          '| test | PersonalVote threshold | shrink k | gamma | train accuracy | train flips |',
          '|---:|---:|---:|---:|---:|---:|']
for r in choices:
    ta='NA' if r['train_accuracy_pct']=='' else f"{r['train_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['pv_threshold']} | {r['personal_k']} | {r['gamma']} | {ta} | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, posterior {r['posterior']:.2f} -> {r['adjusted_posterior']:.2f}, shrunk PV {r['shrunk_personal']:.2f}")
lines += ['','## Decision','',
          'Adopt only if combined adjusted direction accuracy exceeds 94/99 with parameters selected strictly from earlier cycles.','',
          '## Outputs','',
          '- experiments/outparty_favored/results/favored_summary.csv',
          '- experiments/outparty_favored/results/favored_choices.csv',
          '- experiments/outparty_favored/results/favored_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
