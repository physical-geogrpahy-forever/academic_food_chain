#!/usr/bin/env python3
import csv, itertools, runpy, math
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
PSTACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/outparty_pvi_interaction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0440_outparty-pvi-interaction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
base_rows=fns['rows']
pns=runpy.run_path(str(PSTACK))
byrace=pns['byrace']; aggregate=pns['aggregate']; ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]

rows=[]
for r in base_rows:
    x=dict(r)
    pvi=float(r['pvi']); out=float(r['outparty']); inc=float(r['inc_diff']); same=float(r['same_last'])
    x['abs_pvi']=abs(pvi)
    x['outparty_abs_pvi']=out*abs(pvi)
    x['outparty_pvi_sq']=out*(abs(pvi)**2)/10.0
    x['inc_abs_pvi']=inc*abs(pvi)
    x['same_outparty']=same*out
    x['same_minus_pvi']=same-pvi
    rows.append(x)

FEATURESETS={
 'baseline':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era'],
 'outparty_pvi':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era','outparty_abs_pvi'],
 'outparty_pvi_sq':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era','outparty_abs_pvi','outparty_pvi_sq'],
 'outparty_pvi_inc':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era','outparty_abs_pvi','inc_abs_pvi'],
 'outparty_pvi_same':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era','outparty_abs_pvi','same_outparty'],
 'outparty_pvi_local':['pvi','same_last','same_gap','same_minus_pvi','econ','national','inc_diff','outparty','inc_era','outparty_era','outparty_abs_pvi','same_outparty']
}
L_BASE=[4.0,16.0,64.0,256.0]
L_INC=[16.0,64.0,256.0,1024.0,4096.0]
L_INTER=[1.0,4.0,16.0,64.0,256.0,1024.0]
L_ERA=[64.0,256.0,1024.0,4096.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(tr,te,features,lb,li,lx,le):
    X,st=design(tr,features);Xt,_=design(te,features,st);y=np.array([float(r['y']) for r in tr])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1):
        if f in ('inc_diff','outparty'):pen[j]=li
        elif f in ('inc_era','outparty_era'):pen[j]=le
        elif f in ('outparty_abs_pvi','outparty_pvi_sq','inc_abs_pvi','same_outparty','same_minus_pvi'):pen[j]=lx
        else:pen[j]=lb
    b=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@b

def post(r,prior):
    cyc=int(r['cycle'])
    if cyc not in ELECTION:return float(prior),'',0.0
    target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    if agg is None:return float(prior),'',0.0
    pm,neff,n=agg;w=.75*neff/(neff+.5)
    return (1-w)*float(prior)+w*pm,pm,w

def metric(dat,pri):
    ok=0;mae=0.
    for r,p in zip(dat,pri):
        q,_,_=post(r,p);ok+=int((q>0)==(float(r['y'])>0));mae+=abs(q-float(r['y']))
    return ok,mae/len(dat)

def choose(train):
    cycles=sorted(set(int(r['cycle']) for r in train));grid=[]
    for name,features in FEATURESETS.items():
      for lb,li,lx,le in itertools.product(L_BASE,L_INC,L_INTER,L_ERA):
        rr=[];pp=[]
        for vc in cycles[1:]:
            if vc not in ELECTION:continue
            a=[r for r in train if int(r['cycle'])<vc];b=[r for r in train if int(r['cycle'])==vc]
            if len(a)<25 or not b:continue
            q=fitpred(a,b,features,lb,li,lx,le);rr+=b;pp+=q.tolist()
        if not rr:continue
        ok,mae=metric(rr,pp)
        grid.append((-ok,mae,len(features),-(li+lx+le),name,lb,li,lx,le,len(rr)))
    grid.sort()
    return grid[0],grid[:20]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
    best,trace=choose(tr)
    negok,imae,nf,sp,name,lb,li,lx,le,innern=best
    pri=fitpred(tr,te,FEATURESETS[name],lb,li,lx,le)
    choices.append({'test_cycle':tc,'feature_set':name,'lambda_base':lb,'lambda_inc':li,'lambda_interaction':lx,'lambda_era':le,
                    'inner_n':innern,'inner_correct':-negok,'inner_accuracy_pct':100*(-negok)/innern,'inner_post_mae':imae,
                    'top20':' | '.join(f'{z[4]} B{z[5]} I{z[6]} X{z[7]} E{z[8]} correct={-z[0]}/{z[9]} mae={z[1]:.2f}' for z in trace)})
    for r,p in zip(te,pri):
        q,pm,w=post(r,p)
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':float(r['y']),
                     'prior':float(p),'poll_margin':pm,'posterior':q,'correct':int((q>0)==(float(r['y'])>0)),
                     'feature_set':name,'pvi':r['pvi'],'outparty':r['outparty'],'outparty_abs_pvi':r['outparty_abs_pvi']})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n})

for fn,arr in [('interaction_summary.csv',summary),('interaction_choices.csv',choices),('interaction_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

wrong=[r for r in pred if not r['correct']]
lines=['# OutPartyIncumbent x PVI interaction experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: winner-direction accuracy after the fixed 45-day poll blend.',
'- New structural term: OutPartyIncumbent × |PVI|. A quadratic version and interactions with incumbency/SameSeat are also tested.',
'- Feature family and ridge strengths are selected only by chronological inner OOS winner count.','',
'## Result','',
'| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Selected model','',
'| test | feature set | base ridge | incumbent ridge | interaction ridge | era ridge | inner accuracy | post MAE |',
'|---:|---|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda_base']} | {r['lambda_inc']} | {r['lambda_interaction']} | {r['lambda_era']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_post_mae']:.2f} |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']}: actual={r['actual']:.2f}, prior={r['prior']:.2f}, poll={r['poll_margin']}, posterior={r['posterior']:.2f}, model={r['feature_set']}")
lines += ['','## Benchmark','',
'- Current accepted benchmark: 94/99 = 94.9%.',
'- Adopt only if this interaction model exceeds 94/99 under the same outer OOS universe.','',
'## Outputs','',
'- experiments/outparty_pvi_interaction/results/interaction_summary.csv',
'- experiments/outparty_pvi_interaction/results/interaction_choices.csv',
'- experiments/outparty_pvi_interaction/results/interaction_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
