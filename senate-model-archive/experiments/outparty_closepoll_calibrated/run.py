#!/usr/bin/env python3
import runpy,csv,math
from pathlib import Path
from datetime import timedelta,datetime,timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/outparty_closepoll_calibrated/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0470_closepoll-calibrated-selector.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
struct={(int(r['cycle']),str(r['race_id'])):r for r in fns['rows']}
pns=runpy.run_path(str(STACK))
hist=pns['hist'];byrace=pns['byrace'];aggregate=pns['aggregate'];ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]
THRESH=[-1,0.25,0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0,5.0]

def enrich(r):
    s=struct.get((int(r['cycle']),str(r['race_id'])))
    if s is None:return None
    cyc=int(r['cycle']);target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    prior=float(r['prior'])
    if agg is None:
        pm=None;post=prior
    else:
        pm,neff,n=agg;w=.75*neff/(neff+.5);post=(1-w)*prior+w*pm
    return {'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],'actual':float(r['actual']),
            'posterior':post,'poll':pm,'pvi':float(s['pvi']),'outparty':float(s['outparty'])}

data=[x for x in (enrich(r) for r in hist) if x is not None]

def margin(r,t):
    base=float(r['posterior'])
    if t<0 or r['outparty']==0 or r['poll'] is None or abs(float(r['poll']))>t:
        return base,0
    # Directional override, but preserve the baseline confidence magnitude.
    sg=1.0 if r['pvi']>0 else -1.0
    q=sg*abs(base)
    return q,int((q>0)!=(base>0))

def metrics(dat,t):
    correct=flips=0;mae=0.;brier=0.;ll=0.
    for r in dat:
        q,f=margin(r,t);y=1. if r['actual']>0 else 0.
        correct+=int((q>0)==(r['actual']>0));flips+=f;mae+=abs(q-r['actual'])
        p=1/(1+math.exp(-max(min(q/6.0,30),-30)))
        p=min(max(p,1e-9),1-1e-9)
        brier+=(p-y)**2
        ll+=-(y*math.log(p)+(1-y)*math.log(1-p))
    n=len(dat)
    return correct,brier/n,ll/n,mae/n,flips

def choose(train):
    grid=[]
    for t in THRESH:
        ok,br,ll,mae,flips=metrics(train,t)
        # Declared project ordering: direction -> Brier/log loss -> MAE -> parsimony.
        complexity=0 if t<0 else t
        grid.append((-ok,br,ll,mae,complexity,flips,t))
    grid.sort()
    return grid[0],grid

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in data if r['cycle']<tc];te=[r for r in data if r['cycle']==tc]
    best,grid=choose(tr);negok,br,ll,mae,comp,trflips,t=best
    choices.append({'test_cycle':tc,'threshold_abs_poll_pctpt':t,'train_n':len(tr),'train_correct':-negok,
                    'train_accuracy_pct':100*(-negok)/len(tr),'train_brier':br,'train_logloss':ll,
                    'train_mae':mae,'train_flips':trflips,
                    'grid':' | '.join(f't={z[6]} correct={-z[0]}/{len(tr)} br={z[1]:.4f} ll={z[2]:.4f} mae={z[3]:.2f} flips={z[5]}' for z in grid)})
    for r in te:
        q,f=margin(r,t);base=r['posterior'];act=r['actual']
        pred.append({**r,'threshold':t,'adjusted_margin':q,'override_applied':f,
                     'baseline_correct':int((base>0)==(act>0)),'adjusted_correct':int((q>0)==(act>0))})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'overrides':sum(r['override_applied'] for r in rr)})

for fn,arr in [('calibrated_summary.csv',summary),('calibrated_choices.csv',choices),('calibrated_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# Calibrated selector for out-party close-poll PVI rule','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Fixes a methodological inconsistency in the previous selector.',
'- Project decision order is direction accuracy first, then Brier/log loss, then MAE.',
'- Previous close-poll selector incorrectly used fewer overrides as the first tie-break.',
'- For an override, the posterior magnitude is preserved and only its sign is set to the PVI direction, enabling consistent Brier/log-loss/MAE comparison.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['overrides']} |")
lines += ['','## Strictly prior-cycle selected threshold','',
'| test | threshold | train correct | train accuracy | Brier | log loss | MAE | flips |',
'|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['threshold_abs_poll_pctpt']} | {r['train_correct']} | {r['train_accuracy_pct']:.1f}% | {r['train_brier']:.4f} | {r['train_logloss']:.4f} | {r['train_mae']:.2f} | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, poll={r['poll']}, PVI={r['pvi']:.2f}, threshold={r['threshold']}")
lines += ['','## Decision','',
'- If this prior-cycle selector chooses a nonzero threshold and exceeds 94/99, it qualifies as a clean nested improvement under the declared metric hierarchy.',
'- Otherwise the fixed 1.0pp 97/99 result remains post-hoc only.','',
'## Outputs','',
'- experiments/outparty_closepoll_calibrated/results/calibrated_summary.csv',
'- experiments/outparty_closepoll_calibrated/results/calibrated_choices.csv',
'- experiments/outparty_closepoll_calibrated/results/calibrated_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
