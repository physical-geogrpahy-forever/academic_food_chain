#!/usr/bin/env python3
import csv, runpy, itertools
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/contextual_poll_bias/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0360_contextual-poll-bias-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ps=runpy.run_path(str(STACK))
hist=ps['hist']; rows=ps['rows']
rowby={(int(r['cycle']),str(r['race_id'])):r for r in rows}
WMAX=.75;K=.5;OUTER=[2014,2018,2022]

data=[]
for h in hist:
    s=rowby.get((int(h['cycle']),str(h['race_id'])))
    if s is None:continue
    poll=float(h['poll']) if h['poll']!='' else None
    data.append({**h,'pvi':float(s['pvi']),'outparty':float(s.get('outparty',0)),
                 'gap_prior_poll':(float(h['prior'])-poll if poll is not None else 0.0),
                 'abs_pvi':abs(float(s['pvi']))})

SETS={
 'intercept':[],
 'pvi':['pvi'],
 'pvi_outparty':['pvi','outparty'],
 'pvi_gap':['pvi','gap_prior_poll'],
 'pvi_abs':['pvi','abs_pvi'],
 'pvi_outparty_gap':['pvi','outparty','gap_prior_poll'],
 'full':['pvi','abs_pvi','outparty','gap_prior_poll']
}
LAMS=[0.,0.1,1.,4.,16.,64.,256.,1024.]

def design(dat,features,stats=None):
    if features:
        X=np.array([[float(r[f]) for f in features] for r in dat],float)
        if stats is None:
            mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.,sd)
        else:mu,sd=stats
        Z=(X-mu)/sd
        return np.column_stack([np.ones(len(dat)),Z]),(mu,sd)
    return np.ones((len(dat),1)),(np.array([]),np.array([]))

def fit_error(train,test,features,lam):
    X,st=design(train,features);Xt,_=design(test,features,st)
    y=np.array([float(r['poll'])-float(r['actual']) for r in train])
    pen=np.zeros(X.shape[1]);pen[1:]=lam
    b=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@b

def corrected_post(r,bias):
    if r['poll_count']<=0:return float(r['prior'])
    adj=float(r['poll'])-bias
    w=WMAX*float(r['neff'])/(float(r['neff'])+K)
    return (1-w)*float(r['prior'])+w*adj

def inner_score(train,features,lam):
    cycles=sorted(set(int(r['cycle']) for r in train))
    allrows=[];pred=[];pollmae=[]
    for vc in cycles[1:]:
        tr=[r for r in train if int(r['cycle'])<vc and r['poll_count']>0]
        va=[r for r in train if int(r['cycle'])==vc]
        cov=[r for r in va if r['poll_count']>0]
        if len(tr)<20 or not cov:continue
        bias=fit_error(tr,cov,features,lam)
        bmap={r['race_id']:float(z) for r,z in zip(cov,bias)}
        for r in va:
            q=corrected_post(r,bmap.get(r['race_id'],0.0))
            allrows.append(r);pred.append(q)
        for r,z in zip(cov,bias):
            pollmae.append(abs((float(r['poll'])-float(z))-float(r['actual'])))
    if not allrows:return None
    ok=sum((q>0)==(float(r['actual'])>0) for r,q in zip(allrows,pred))
    return 100*ok/len(allrows),sum(pollmae)/len(pollmae)

choices=[];pred=[]
for tc in OUTER:
    train=[r for r in data if int(r['cycle'])<tc]
    test=[r for r in data if int(r['cycle'])==tc]
    cand=[]
    for name,features in SETS.items():
      for lam in LAMS:
        sc=inner_score(train,features,lam)
        if sc is None:continue
        acc,mae=sc
        cand.append((-acc,mae,len(features),lam,name,features))
    cand.sort(key=lambda z:(z[0],z[1],z[2],z[3]))
    z=cand[0];acc=-z[0];mae=z[1];lam=z[3];name=z[4];features=z[5]
    trcov=[r for r in train if r['poll_count']>0]
    tecov=[r for r in test if r['poll_count']>0]
    bias=fit_error(trcov,tecov,features,lam) if trcov and tecov else []
    bmap={r['race_id']:float(v) for r,v in zip(tecov,bias)}
    choices.append({'test_cycle':tc,'feature_set':name,'lambda':lam,'inner_accuracy_pct':acc,'inner_poll_mae':mae,
                    'train_poll_rows':len(trcov),'top12':' | '.join(f'{q[4]}@{q[3]} acc={-q[0]:.1f} mae={q[1]:.2f}' for q in cand[:12])})
    for r in test:
        b=bmap.get(r['race_id'],0.0);q=corrected_post(r,b)
        pred.append({**r,'predicted_poll_bias':b,'adjusted_poll':('' if r['poll']=='' else float(r['poll'])-b),
                     'adjusted_posterior':q,'baseline_correct':int((float(r['posterior'])>0)==(float(r['actual'])>0)),
                     'adjusted_correct':int((q>0)==(float(r['actual'])>0)),'feature_set':name,'lambda':lam})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if int(r['cycle'])==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum((r['adjusted_posterior']>0)!=(float(r['posterior'])>0) for r in rr)})

for fn,arr in [('contextual_bias_summary.csv',summary),('contextual_bias_choices.csv',choices),('contextual_bias_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
comb=summary[0]
lines=['# Contextual Senate poll-bias direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Baseline: fixed 45-day Core V2 poll blend, 94/99.',
       '- Poll bias models are trained only on poll-covered races in cycles before each test cycle.',
       '- Candidate predictors: PVI, absolute PVI, out-party-incumbent status, and fundamentals-poll gap.',
       '- Model family and ridge strength are selected by chronological inner OOS winner-direction accuracy; poll MAE is only the first tie-breaker.','',
       '## Result','',
       '| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected bias model','',
          '| test | features | lambda | inner accuracy | inner poll MAE | train poll rows |',
          '|---:|---|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_poll_mae']:.2f} | {r['train_poll_rows']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, bias={r['predicted_poll_bias']:.2f}")
lines += ['','## Decision','',
          f"- Combined adjusted result: {comb['adjusted_correct']}/{comb['n']} = {comb['adjusted_accuracy_pct']:.1f}%.",
          '- Adopt only if this exceeds 94/99 without outer-cycle tuning.','',
          '## Outputs','',
          '- experiments/contextual_poll_bias/results/contextual_bias_summary.csv',
          '- experiments/contextual_poll_bias/results/contextual_bias_choices.csv',
          '- experiments/contextual_poll_bias/results/contextual_bias_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
