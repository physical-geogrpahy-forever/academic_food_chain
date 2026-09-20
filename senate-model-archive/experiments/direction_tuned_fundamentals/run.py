#!/usr/bin/env python3
import csv, itertools, runpy, math
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
PSTACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/direction_tuned_fundamentals/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0430_direction-tuned-full-fundamentals.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
rows=fns['rows']
pns=runpy.run_path(str(PSTACK))
byrace=pns['byrace']; aggregate=pns['aggregate']; ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]

# Feature families. Crucially, SameSeat is optional rather than always forced into BASE.
FEATURESETS={
 'pvi_context':['pvi','econ','national'],
 'pvi_same_context':['pvi','same_last','same_gap','econ','national'],
 'pvi_context_inc':['pvi','econ','national','inc_diff','outparty'],
 'pvi_same_context_inc':['pvi','same_last','same_gap','econ','national','inc_diff','outparty'],
 'pvi_context_incera':['pvi','econ','national','inc_diff','outparty','inc_era','outparty_era'],
 'pvi_same_context_incera':['pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era'],
 'pvi_same_context_allera':['pvi','same_last','same_gap','econ','national','same_era','inc_diff','outparty','inc_era','outparty_era'],
}

L_PVI=[0.0,1.0,4.0,16.0]
L_LOCAL=[4.0,16.0,64.0,256.0,1024.0,4096.0]
L_CONTEXT=[1.0,4.0,16.0,64.0,256.0]
L_INC=[4.0,16.0,64.0,256.0,1024.0,4096.0]
L_ERA=[16.0,64.0,256.0,1024.0,4096.0,16384.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(tr,te,features,lp,ll,lc,li,lr):
    X,st=design(tr,features);Xt,_=design(te,features,st);y=np.array([r['y'] for r in tr],float)
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1):
        if f=='pvi':pen[j]=lp
        elif f in ('same_last','same_gap'):pen[j]=ll
        elif f in ('econ','national'):pen[j]=lc
        elif f in ('inc_diff','outparty'):pen[j]=li
        elif f.endswith('_era') or f=='same_era':pen[j]=lr
        else:pen[j]=0.0
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta

def poll_post(r,prior):
    cyc=int(r['cycle'])
    if cyc not in ELECTION:return float(prior),'',0.0,0
    target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    if agg is None:return float(prior),'',0.0,0
    pm,neff,n=agg
    w=.75*neff/(neff+.5)
    return (1-w)*float(prior)+w*pm,pm,w,int(n)

def metric(dat,pri):
    correct=0;mae=0.;brier=0.
    for r,p in zip(dat,pri):
        post,pm,w,n=poll_post(r,p)
        y=1.0 if r['y']>0 else 0.0
        correct+=int((post>0)==(r['y']>0))
        mae+=abs(post-r['y'])
        # monotone confidence transform only for tie breaking
        prob=1/(1+math.exp(-max(min(post/6.0,30),-30)))
        brier+=(prob-y)**2
    n=len(dat)
    return correct,mae/n,brier/n

def choose(train):
    cycles=sorted(set(int(r['cycle']) for r in train))
    grid=[]
    for name,features in FEATURESETS.items():
      has_same=any(f.startswith('same_') for f in features)
      has_inc=any(f in ('inc_diff','outparty') for f in features)
      has_era=any(f.endswith('_era') for f in features)
      llocal=L_LOCAL if has_same else [4096.0]
      linc=L_INC if has_inc else [4096.0]
      lera=L_ERA if has_era else [16384.0]
      for lp,ll,lc,li,lr in itertools.product(L_PVI,llocal,L_CONTEXT,linc,lera):
        vr=[];vp=[]
        # strict forward inner OOS; only cycles with poll infrastructure are scored
        for vc in cycles[1:]:
            if vc not in ELECTION:continue
            a=[r for r in train if int(r['cycle'])<vc]
            b=[r for r in train if int(r['cycle'])==vc]
            if len(a)<20 or not b:continue
            q=fitpred(a,b,features,lp,ll,lc,li,lr)
            vr+=b;vp+=q.tolist()
        if not vr:continue
        ok,mae,brier=metric(vr,vp)
        # Primary winner count, then Brier, then MAE, then fewer features and stronger shrinkage.
        shrink_pref=-(lp+ll+lc+li+lr)
        grid.append((-ok,brier,mae,len(features),shrink_pref,name,lp,ll,lc,li,lr,len(vr)))
    grid.sort()
    return grid[0],grid[:25]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc]
    te=[r for r in rows if int(r['cycle'])==tc]
    best,trace=choose(tr)
    negok,ibrier,imae,nf,sp,name,lp,ll,lc,li,lr,innern=best
    features=FEATURESETS[name]
    pri=fitpred(tr,te,features,lp,ll,lc,li,lr)
    choices.append({'test_cycle':tc,'feature_set':name,'lambda_pvi':lp,'lambda_local':ll,'lambda_context':lc,
                    'lambda_inc':li,'lambda_era':lr,'inner_n':innern,'inner_correct':-negok,
                    'inner_accuracy_pct':100*(-negok)/innern,'inner_brier':ibrier,'inner_post_mae':imae,
                    'top25':' | '.join(f'{z[5]} P{z[6]} L{z[7]} C{z[8]} I{z[9]} E{z[10]} correct={-z[0]}/{z[11]} brier={z[1]:.3f} mae={z[2]:.2f}' for z in trace)})
    for r,p in zip(te,pri):
        post,pm,w,n=poll_post(r,p)
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],
                     'prior':float(p),'poll_margin':pm,'poll_weight':w,'poll_count':n,'posterior':post,
                     'correct':int((post>0)==(r['y']>0)),'feature_set':name,
                     'pvi':r['pvi'],'same_last':r['same_last'],'inc_diff':r['inc_diff'],'outparty':r['outparty']})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n})

for fn,arr in [('direction_tuned_summary.csv',summary),('direction_tuned_choices.csv',choices),('direction_tuned_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

wrong=[r for r in pred if not r['correct']]
target={('2014','NC'),('2018','NV'),('2018','MO'),('2018','FL'),('2018','IN')}
lines=['# Direction-tuned full fundamentals','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- This corrects the objective mismatch in the previous 94/99 baseline: the prior model hyperparameters had been selected by RMSE even after winner-direction became the primary goal.',
'- All structure/ridge choices here are selected by chronological inner OOS winner count AFTER the fixed 45-day poll blend.',
'- SameSeat is optional; the selector may drop it entirely.',
'- Ties use Brier score, then posterior MAE, then model simplicity and stronger shrinkage.','',
'## Result','',
'| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Selected model by outer cycle','',
'| test | features | PVI ridge | local ridge | context ridge | incumbent ridge | era ridge | inner accuracy | Brier | posterior MAE |',
'|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda_pvi']} | {r['lambda_local']} | {r['lambda_context']} | {r['lambda_inc']} | {r['lambda_era']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_brier']:.3f} | {r['inner_post_mae']:.2f} |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} race {r['race_id']}: actual={r['actual']:.2f}, prior={r['prior']:.2f}, poll={r['poll_margin']}, posterior={r['posterior']:.2f}, model={r['feature_set']}")
lines += ['','## Previously unresolved five','']
for r in pred:
    if (str(r['test_cycle']),r['state_abbrev']) in target:
        lines.append(f"- {r['test_cycle']} {r['state_abbrev']}: {'CORRECT' if r['correct'] else 'WRONG'}, actual={r['actual']:.2f}, prior={r['prior']:.2f}, posterior={r['posterior']:.2f}, PVI={r['pvi']:.2f}, SameSeat={r['same_last']:.2f}, OutParty={r['outparty']}")
lines += ['','## Benchmark','',
'- Current accepted fixed-poll baseline: 94/99 = 94.9%.',
'- Adopt this model only if it exceeds 94/99 under the same 99-race OOS universe.','',
'## Outputs','',
'- experiments/direction_tuned_fundamentals/results/direction_tuned_summary.csv',
'- experiments/direction_tuned_fundamentals/results/direction_tuned_choices.csv',
'- experiments/direction_tuned_fundamentals/results/direction_tuned_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
