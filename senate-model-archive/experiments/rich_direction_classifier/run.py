#!/usr/bin/env python3
import runpy, csv, itertools
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
PSTACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/rich_direction_classifier/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0360_rich-direction-classifier.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
rows=fns['rows']
pns=runpy.run_path(str(PSTACK))
hist=pns['hist']

struct={(int(r['cycle']),str(r['race_id'])):r for r in rows}
data=[]
for h in hist:
    key=(int(h['cycle']),str(h['race_id']))
    s=struct.get(key)
    if s is None:continue
    x=dict(h)
    for k in ['pvi','same_last','same_gap','econ','national','inc_diff','outparty','same_era','inc_era','outparty_era']:
        x[k]=float(s[k])
    x['abs_pvi']=abs(x['pvi'])
    x['abs_prior']=abs(x['prior'])
    x['abs_poll']=abs(float(x['poll'])) if x['poll_count']>0 else 0.0
    x['abs_gap_poll_prior']=abs(x['prior']-float(x['poll'])) if x['poll_count']>0 else 0.0
    x['poll_missing']=1.0 if x['poll_count']==0 else 0.0
    x['outparty_abs_pvi']=x['outparty']*x['abs_pvi']
    x['inc_pvi']=x['inc_diff']*x['pvi']
    data.append(x)

OUTER=[2014,2018,2022]
FEATURESETS={
 'posterior':['posterior'],
 'poll_core':['posterior','poll','neff','poll_missing'],
 'structural':['posterior','poll','neff','poll_missing','pvi','same_last','same_gap','econ','national'],
 'candidate':['posterior','poll','neff','poll_missing','pvi','same_last','same_gap','econ','national','inc_diff','outparty'],
 'candidate_interactions':['posterior','poll','neff','poll_missing','pvi','same_last','same_gap','econ','national','inc_diff','outparty','abs_pvi','abs_prior','abs_poll','abs_gap_poll_prior','outparty_abs_pvi','inc_pvi'],
}
LAMS=[0.1,0.5,1,2,4,8,16,32,64,128,256,512]

def val(r,f):
    if f=='poll':
        return float(r['poll']) if r['poll_count']>0 else float(r['posterior'])
    return float(r[f])

def design(dat,features,stats=None):
    X=np.array([[val(r,f) for f in features] for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def sig(z):return 1/(1+np.exp(-np.clip(z,-35,35)))

def fit(tr,te,features,lam):
    X,st=design(tr,features);Xt,_=design(te,features,st)
    y=np.array([1. if r['actual']>0 else 0. for r in tr])
    b=np.zeros(X.shape[1]);pen=np.zeros(X.shape[1]);pen[1:]=lam
    for _ in range(100):
        p=sig(X@b);w=np.clip(p*(1-p),1e-5,None);z=X@b+(y-p)/w
        Xw=X*np.sqrt(w)[:,None];zw=z*np.sqrt(w)
        nb=np.linalg.pinv(Xw.T@Xw+np.diag(pen))@(Xw.T@zw)
        if np.max(np.abs(nb-b))<1e-8:b=nb;break
        b=nb
    return sig(Xt@b)

def metrics(dat,probs):
    y=np.array([1 if r['actual']>0 else 0 for r in dat]);p=np.asarray(probs)
    pred=p>=.5
    acc=100*np.mean(pred==y)
    eps=1e-9
    ll=float(-np.mean(y*np.log(np.clip(p,eps,1-eps))+(1-y)*np.log(np.clip(1-p,eps,1-eps))))
    brier=float(np.mean((p-y)**2))
    return acc,ll,brier

def choose(train):
    cycles=sorted(set(r['cycle'] for r in train));grid=[]
    for name,features in FEATURESETS.items():
      for lam in LAMS:
        allr=[];allp=[]
        for vc in cycles[1:]:
            a=[r for r in train if r['cycle']<vc];b=[r for r in train if r['cycle']==vc]
            if len(a)<30 or not b:continue
            p=fit(a,b,features,lam);allr+=b;allp+=p.tolist()
        if not allr:continue
        acc,ll,br=metrics(allr,allp)
        grid.append((-acc,ll,br,len(features),lam,name))
    grid.sort()
    return grid[0],grid[:15]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in data if r['cycle']<tc];te=[r for r in data if r['cycle']==tc]
    best,trace=choose(tr);na,ll,br,nf,lam,name=best;features=FEATURESETS[name]
    probs=fit(tr,te,features,lam)
    choices.append({'test_cycle':tc,'feature_set':name,'lambda':lam,'inner_accuracy_pct':-na,'inner_logloss':ll,'inner_brier':br,'train_n':len(tr),'test_n':len(te),
                    'top15':' | '.join(f'{z[5]}@{z[4]} acc={-z[0]:.1f} ll={z[1]:.3f}' for z in trace)})
    for r,p in zip(te,probs):
        base=(r['posterior']>0);act=(r['actual']>0);q=(p>=.5)
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['actual'],
                     'baseline_posterior':r['posterior'],'prob_D':float(p),'baseline_correct':int(base==act),'classifier_correct':int(q==act),
                     'feature_set':name,'lambda':lam})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);c=sum(r['classifier_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,'classifier_correct':c,'classifier_accuracy_pct':100*c/n,'net_correct_gain':c-b})

for fn,datax in [('rich_classifier_summary.csv',summary),('rich_classifier_choices.csv',choices),('rich_classifier_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(datax[0].keys()));w.writeheader();w.writerows(datax)

changed=[r for r in pred if r['baseline_correct']!=r['classifier_correct']]
lines=['# Rich direction classifier OOS','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: winner-direction accuracy.',
'- Candidate model families combine the fixed-poll posterior with poll information, PVI, SameSeat, economy, national environment, incumbency, and OutPartyIncumbent.',
'- Feature set and ridge strength are selected only by chronological inner OOS before each outer cycle.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | classifier correct | classifier acc | net |',
'|---|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['classifier_correct']} | {r['classifier_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} |")
lines += ['','## Selected models','',
'| test | feature set | lambda | inner accuracy | inner log loss | train N |',
'|---:|---|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_logloss']:.3f} | {r['train_n']} |")
lines += ['','## Changed correctness','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> classifier {'correct' if r['classifier_correct'] else 'wrong'}")
lines += ['','## Decision','',
'Adopt only if classifier accuracy exceeds 94/99 under the same outer OOS universe.','',
'## Outputs','',
'- experiments/rich_direction_classifier/results/rich_classifier_summary.csv',
'- experiments/rich_direction_classifier/results/rich_classifier_choices.csv',
'- experiments/rich_direction_classifier/results/rich_classifier_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
