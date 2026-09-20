#!/usr/bin/env python3
import runpy, csv, math, itertools
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
PSTACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/outparty_survival/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0380_outparty-incumbent-survival-model.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
rows=fns['rows']
pns=runpy.run_path(str(PSTACK))
hist=pns['hist']; byr=pns['byrace']; aggregate=pns['aggregate']; ELECTION=pns['ELECTION']

struct={(int(r['cycle']),str(r['race_id'])):r for r in rows}
data=[]
for h in hist:
    key=(int(h['cycle']),str(h['race_id']))
    s=struct.get(key)
    if s is None or int(s['outparty'])==0:
        continue
    sign=1.0 if int(s['outparty'])==1 else -1.0
    target=ELECTION[int(h['cycle'])]-timedelta(days=45)
    agg=aggregate(byr.get((int(h['cycle']),str(h['race_id'])),[]),target,30,14)
    prior=float(h['prior'])
    if agg is None:
        poll=0.0; neff=0.0; poll_count=0; post=prior; poll_missing=1.0
    else:
        poll,neff,poll_count=agg
        w=.75*neff/(neff+.5)
        post=(1-w)*prior+w*poll
        poll_missing=0.0
    actual=float(h['actual'])
    pvi=float(s['pvi']); same=float(s['same_last']); gap=float(s['same_gap'])
    data.append({
      'cycle':int(h['cycle']),'race_id':str(h['race_id']),'state_abbrev':h['state_abbrev'],
      'actual':actual,'inc_sign':sign,'survived':1 if actual*sign>0 else 0,
      'baseline_posterior':post,'baseline_correct':int((post>0)==(actual>0)),
      'posterior_inc':post*sign,'prior_inc':prior*sign,'poll_inc':poll*sign,
      'pvi_disadv':-pvi*sign,'same_inc':same*sign,'same_vs_pvi_inc':(same-pvi)*sign,
      'same_gap':gap,'national_inc':float(s['national'])*sign,'econ_inc':float(s['econ'])*sign,
      'neff':float(neff),'poll_count':int(poll_count),'poll_missing':poll_missing,
      'poll_prior_shift_inc':(poll-prior)*sign if not poll_missing else 0.0,
      'abs_posterior':abs(post),'abs_poll':abs(poll) if not poll_missing else 0.0
    })

OUTER=[2014,2018,2022]
FEATURESETS={
 'core':['posterior_inc','pvi_disadv','same_inc'],
 'poll':['posterior_inc','pvi_disadv','same_inc','poll_inc','neff','poll_missing'],
 'personal_proxy':['posterior_inc','pvi_disadv','same_inc','same_vs_pvi_inc','same_gap'],
 'rich':['posterior_inc','prior_inc','poll_inc','pvi_disadv','same_inc','same_vs_pvi_inc','same_gap','national_inc','econ_inc','neff','poll_count','poll_missing','poll_prior_shift_inc','abs_posterior','abs_poll'],
}
LAMS=[0.1,0.5,1,2,4,8,16,32,64,128]
CONF=[0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.90]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],float)
    if stats is None:
        mu=X.mean(0); sd=X.std(0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def sig(z): return 1/(1+np.exp(-np.clip(z,-35,35)))

def fit(tr,te,features,lam):
    X,st=design(tr,features); Xt,_=design(te,features,st)
    y=np.array([float(r['survived']) for r in tr])
    b=np.zeros(X.shape[1]); pen=np.zeros(X.shape[1]); pen[1:]=lam
    for _ in range(100):
        p=sig(X@b); w=np.clip(p*(1-p),1e-5,None); z=X@b+(y-p)/w
        Xw=X*np.sqrt(w)[:,None]; zw=z*np.sqrt(w)
        nb=np.linalg.pinv(Xw.T@Xw+np.diag(pen))@(Xw.T@zw)
        if np.max(np.abs(nb-b))<1e-8:
            b=nb; break
        b=nb
    return sig(Xt@b)

def apply(dat,probs,conf):
    ok=0; overrides=0
    details=[]
    for r,p in zip(dat,probs):
        baseline_survive=(r['baseline_posterior']*r['inc_sign'])>0
        cls_survive=p>=.5
        cls_conf=max(p,1-p)
        use=cls_conf>=conf and cls_survive!=baseline_survive
        survive=cls_survive if use else baseline_survive
        pred_d = survive if r['inc_sign']>0 else (not survive)
        correct=int(pred_d==(r['actual']>0))
        ok+=correct; overrides+=int(use)
        details.append((correct,use,p,survive))
    return ok,overrides,details

def choose(train):
    cycles=sorted(set(r['cycle'] for r in train)); grid=[]
    for fs,features in FEATURESETS.items():
      for lam in LAMS:
        fold_rows=[]; fold_probs=[]
        for vc in cycles[1:]:
            a=[r for r in train if r['cycle']<vc]; b=[r for r in train if r['cycle']==vc]
            if len(a)<8 or not b: continue
            # Need both outcomes in training for logistic.
            if len(set(r['survived'] for r in a))<2: continue
            p=fit(a,b,features,lam)
            fold_rows+=b; fold_probs+=p.tolist()
        if not fold_rows: continue
        for conf in CONF:
            ok,ov,_=apply(fold_rows,fold_probs,conf)
            # primary correct count; tie fewer overrides; simpler feature set; stronger regularization preference
            grid.append((-ok,ov,len(features),-lam,conf,fs,lam,len(fold_rows)))
    if not grid: return None,[]
    grid.sort()
    return grid[0],grid[:15]

# Full 99-race fixed blend baseline for outer comparison.
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
with BASE.open('r',encoding='utf-8-sig',newline='') as f:
    base99=[r for r in csv.DictReader(f) if r['variant']=='w30_h14_all']
base_by={(int(r['test_cycle']),str(r['race_id'])):r for r in base99}

pred=[]; choices=[]
for tc in OUTER:
    train=[r for r in data if r['cycle']<tc]
    test=[r for r in data if r['cycle']==tc]
    best,trace=choose(train)
    if best is None or len(set(r['survived'] for r in train))<2:
        fs='core'; lam=64; conf=.9
        probs=np.array([.5]*len(test))
        inner_n=0; inner_ok=0; inner_ov=0
    else:
        negok,inner_ov,nf,nlam,conf,fs,lam,inner_n=best
        inner_ok=-negok
        probs=fit(train,test,FEATURESETS[fs],lam)
    choices.append({
      'test_cycle':tc,'feature_set':fs,'lambda':lam,'confidence_threshold':conf,
      'train_outparty_n':len(train),'inner_eval_n':inner_n,'inner_correct':inner_ok,
      'inner_accuracy_pct':(100*inner_ok/inner_n if inner_n else ''),'inner_overrides':inner_ov,
      'top15':' | '.join(f'{z[5]} lam{z[6]} c{z[4]} correct={-z[0]}/{z[7]} ov={z[1]}' for z in trace)
    })
    ok,ov,details=apply(test,probs,conf)
    detail_by={r['race_id']:(p,d) for r,p,d in zip(test,probs,details)}
    # Emit every outer race, leaving non-outparty races untouched.
    for key,b in [(k,v) for k,v in base_by.items() if k[0]==tc]:
        rid=key[1]; actual=float(b['actual']); basepost=float(b['posterior'])
        baseline_correct=int((basepost>0)==(actual>0))
        if rid in detail_by:
            p,d=detail_by[rid]; correct,use,pp,survive=d
            s=next(x for x in test if x['race_id']==rid)
            if use:
                pred_d = survive if s['inc_sign']>0 else (not survive)
            else:
                pred_d = basepost>0
            adjusted_correct=int(pred_d==(actual>0))
            prob_survival=float(p)
        else:
            use=False; adjusted_correct=baseline_correct; prob_survival=''
        pred.append({
          'test_cycle':tc,'race_id':rid,'state_abbrev':b['state_abbrev'],'actual':actual,
          'baseline_posterior':basepost,'baseline_correct':baseline_correct,
          'outparty_override_applied':int(use),'survival_probability':prob_survival,
          'adjusted_correct':adjusted_correct,'feature_set':fs,'lambda':lam,'confidence_threshold':conf
        })

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr); b=sum(r['baseline_correct'] for r in rr); a=sum(r['adjusted_correct'] for r in rr)
    summary.append({
      'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
      'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
      'outparty_overrides':sum(r['outparty_override_applied'] for r in rr)
    })

for fn,dat in [('survival_summary.csv',summary),('survival_choices.csv',choices),('survival_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dat[0].keys())); w.writeheader(); w.writerows(dat)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
counts={c:sum(r['cycle']==c for r in data) for c in sorted(set(r['cycle'] for r in data))}
lines=['# Out-party incumbent survival model','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- The 94/99 fixed-poll baseline is left unchanged for every non-out-party-incumbent race.',
'- A separate survival classifier is trained only on historical out-party incumbents.',
'- Features are oriented to the incumbent: fixed-poll posterior, PVI disadvantage, prior same-seat performance, poll signal, national/economic context, and related interactions.',
'- An override occurs only when the survival classifier disagrees with the baseline and exceeds a confidence threshold selected on earlier-cycle OOS.','',
'## Historical out-party incumbent counts','']
for c,n in counts.items():lines.append(f'- {c}: {n}')
lines += ['','## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['outparty_overrides']} |")
lines += ['','## Selected survival models','',
'| test | feature set | lambda | confidence | train outparty N | inner accuracy | inner overrides |',
'|---:|---|---:|---:|---:|---:|---:|']
for r in choices:
    ia='NA' if r['inner_accuracy_pct']=='' else f"{r['inner_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda']} | {r['confidence_threshold']} | {r['train_outparty_n']} | {ia} | {r['inner_overrides']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> survival {'correct' if r['adjusted_correct'] else 'wrong'}")
lines += ['','## Decision','',
'Adopt only if adjusted accuracy exceeds 94/99 while non-out-party races remain untouched.','',
'## Outputs','',
'- experiments/outparty_survival/results/survival_summary.csv',
'- experiments/outparty_survival/results/survival_choices.csv',
'- experiments/outparty_survival/results/survival_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('\n'.join(lines))
