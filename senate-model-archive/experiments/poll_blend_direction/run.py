#!/usr/bin/env python3
import runpy, csv, itertools, math
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/poll_blend_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0370_poll-blend-direction-nested.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ns=runpy.run_path(str(STACK))
hist=ns['hist'];byrace=ns['byrace'];aggregate=ns['aggregate'];ELECTION=ns['ELECTION']
OUTER=[2014,2018,2022]

WINDOWS=[14,21,30,45,60,90]
HALF=[7,14,30,90,999]
WMAX=[0.5,0.6,0.7,0.75,0.8,0.9,1.0]
KGRID=[0.1,0.25,0.5,1.0,2.0,4.0,8.0]

def predict_row(r,window,hl,wmax,k):
    cyc=int(r['cycle']);rid=str(r['race_id']);target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,rid),[]),target,window,hl)
    prior=float(r['prior'])
    if agg is None:
        return prior,0.0,0,''
    pm,neff,n_poll=agg
    w=wmax*neff/(neff+k)
    return (1-w)*prior+w*pm,w,int(n_poll),pm

def evalset(dat,params):
    window,hl,wmax,k=params
    ok=0;errs=[];covered=0;flips=0
    for r in dat:
        p,w,n,pm=predict_row(r,window,hl,wmax,k)
        ok+=int((p>0)==(float(r['actual'])>0))
        errs.append(abs(p-float(r['actual'])))
        covered+=int(n>0)
        flips+=int((p>0)!=(float(r['prior'])>0))
    return ok,100*ok/len(dat),float(np.mean(errs)),covered,flips

def choose(train):
    cand=[]
    for params in itertools.product(WINDOWS,HALF,WMAX,KGRID):
        ok,acc,mae,cov,flips=evalset(train,params)
        window,hl,wmax,k=params
        # Primary winner count, secondary MAE, tertiary closeness to preserved Core V2 blend.
        distance=abs(wmax-.75)+abs(math.log(k/.5))*.05+abs(window-30)/100+abs(hl-14)/200
        cand.append((-ok,mae,distance,window,hl,wmax,k,cov,flips))
    cand.sort()
    return cand[0],cand[:20]

pred=[];choices=[]
for tc in OUTER:
    train=[r for r in hist if int(r['cycle'])<tc]
    test=[r for r in hist if int(r['cycle'])==tc]
    best,trace=choose(train)
    negok,mae,dist,window,hl,wmax,k,cov,flips=best
    choices.append({'test_cycle':tc,'window_days':window,'half_life_days':hl,'w_max':wmax,'k':k,
                    'train_n':len(train),'train_correct':-negok,'train_accuracy_pct':100*(-negok)/len(train),
                    'train_mae':mae,'train_poll_covered':cov,'train_direction_flips':flips,
                    'top20':' | '.join(f'w{z[3]} h{z[4]} max{z[5]} k{z[6]} correct={-z[0]} mae={z[1]:.2f}' for z in trace)})
    for r in test:
        p,w,n,pm=predict_row(r,window,hl,wmax,k)
        # fixed 94/99 baseline: 30d, h14, wmax=.75, k=.5
        bp,bw,bn,bpm=predict_row(r,30,14,.75,.5)
        act=float(r['actual'])
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':act,
                     'prior':r['prior'],'selected_posterior':p,'selected_weight':w,'selected_poll_count':n,'selected_poll_margin':pm,
                     'baseline_posterior':bp,'baseline_correct':int((bp>0)==(act>0)),
                     'selected_correct':int((p>0)==(act>0)),
                     'window_days':window,'half_life_days':hl,'w_max':wmax,'k':k})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);s=sum(r['selected_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'selected_correct':s,'selected_accuracy_pct':100*s/n,'net_correct_gain':s-b})

for fn,data in [('blend_summary.csv',summary),('blend_choices.csv',choices),('blend_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

changed=[r for r in pred if r['baseline_correct']!=r['selected_correct']]
lines=['# Direction-first nested poll blend optimization','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: winner-direction accuracy.',
'- The prior model is unchanged.',
'- For each outer cycle, poll window, half-life, w_max, and k are selected only from earlier cycles.',
'- Fixed comparison benchmark is window=30, half-life=14, w_max=0.75, k=0.5, which produced 94/99.','',
'## Result','',
'| scope | N | fixed correct | fixed acc | nested correct | nested acc | net |',
'|---|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['selected_correct']} | {r['selected_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} |")
lines += ['','## Selected blend by outer cycle','',
'| test | window | half-life | w_max | k | prior rows | train accuracy | train MAE |',
'|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['window_days']} | {r['half_life_days']} | {r['w_max']} | {r['k']} | {r['train_n']} | {r['train_accuracy_pct']:.1f}% | {r['train_mae']:.2f} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: fixed {'correct' if r['baseline_correct'] else 'wrong'} -> nested {'correct' if r['selected_correct'] else 'wrong'}, fixed {r['baseline_posterior']:.2f}, nested {r['selected_posterior']:.2f}")
lines += ['','## Decision','',
'Adopt only if nested poll blend exceeds 94/99 without using outer-cycle outcomes in parameter selection.','',
'## Outputs','',
'- experiments/poll_blend_direction/results/blend_summary.csv',
'- experiments/poll_blend_direction/results/blend_choices.csv',
'- experiments/poll_blend_direction/results/blend_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
