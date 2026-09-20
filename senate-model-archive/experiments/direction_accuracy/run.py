#!/usr/bin/env python3
import csv, math, runpy
from pathlib import Path
import numpy as np
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'experiments/direction_accuracy/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0250_direction-accuracy-primary-oos.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

# Reuse the already audited extended-history data builder.
ns=runpy.run_path(str(ROOT/'experiments/history_extension/run.py'))
rows=ns['rows']
OUTER=[2014,2018,2022]

GROUPS={
 'pvi':['pvi'],
 'local':['same_last','same_gap'],
 'econ':['econ'],
 'national':['national'],
}
ARCHS=[
 ('pvi', ['pvi']),
 ('pvi_local',['pvi','same_last','same_gap']),
 ('pvi_national',['pvi','national']),
 ('pvi_local_national',['pvi','same_last','same_gap','national']),
 ('pvi_local_econ',['pvi','same_last','same_gap','econ']),
 ('full',['pvi','same_last','same_gap','econ','national']),
]
LAM=[0.0,1.0,4.0,16.0,64.0,256.0,1024.0,4096.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def sigmoid(z):
    z=np.clip(z,-35,35)
    return 1.0/(1.0+np.exp(-z))

def fit_logit(train,test,features,lam):
    X,st=design(train,features); Xt,_=design(test,features,st)
    y=np.array([1.0 if float(r['y'])>0 else 0.0 for r in train])
    b=np.zeros(X.shape[1])
    pen=np.zeros(X.shape[1]); pen[1:]=lam
    for _ in range(100):
        eta=X@b; p=sigmoid(eta); w=np.clip(p*(1-p),1e-5,None)
        z=eta+(y-p)/w
        Xw=X*np.sqrt(w)[:,None]; zw=z*np.sqrt(w)
        A=Xw.T@Xw+np.diag(pen)
        nb=np.linalg.pinv(A)@(Xw.T@zw)
        if np.max(np.abs(nb-b))<1e-8:
            b=nb; break
        b=nb
    return sigmoid(Xt@b)

def fit_margin(train,test,features,lam):
    X,st=design(train,features); Xt,_=design(test,features,st)
    y=np.array([float(r['y']) for r in train])
    pen=np.zeros(X.shape[1]); pen[1:]=lam
    b=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    m=Xt@b
    # A monotonic probability transform used only for tie-breaking calibration.
    scale=max(float(np.std(y-X@b)),4.0)
    return sigmoid(m/scale),m

def metrics(actual,prob):
    y=np.asarray([1 if x>0 else 0 for x in actual])
    p=np.asarray(prob)
    pred=(p>=0.5).astype(int)
    acc=float(np.mean(pred==y)*100.0)
    brier=float(np.mean((p-y)**2))
    eps=1e-9
    logloss=float(-np.mean(y*np.log(np.clip(p,eps,1-eps))+(1-y)*np.log(np.clip(1-p,eps,1-eps))))
    return acc,brier,logloss

def inner_eval(train,kind,features,lam):
    cycles=sorted(set(int(r['cycle']) for r in train))
    yy=[]; pp=[]; folds=0
    for vc in cycles[1:]:
        tr=[r for r in train if int(r['cycle'])<vc]
        va=[r for r in train if int(r['cycle'])==vc]
        if len(tr)<25 or not va: continue
        if kind=='logit':
            p=fit_logit(tr,va,features,lam)
        else:
            p,_=fit_margin(tr,va,features,lam)
        yy.extend(float(r['y']) for r in va); pp.extend(p.tolist()); folds+=1
    if not folds: return None
    return (*metrics(yy,pp),folds)

predrows=[]; choices=[]
for tc in OUTER:
    train=[r for r in rows if int(r['cycle'])<tc]
    test=[r for r in rows if int(r['cycle'])==tc]
    grid=[]
    for kind in ['logit','margin']:
        for aname,features in ARCHS:
            for lam in LAM:
                m=inner_eval(train,kind,features,lam)
                if m is None: continue
                acc,brier,ll,folds=m
                # Primary: highest direction accuracy. Secondary: lower log loss, then simpler architecture.
                grid.append((-acc,ll,brier,len(features),lam,kind,aname,features,folds))
    grid.sort()
    z=grid[0]
    negacc,ll,brier,nf,lam,kind,aname,features,folds=z
    if kind=='logit':
        probs=fit_logit(train,test,features,lam)
    else:
        probs,_=fit_margin(train,test,features,lam)
    choices.append({
      'test_cycle':tc,'model':kind,'architecture':aname,'lambda':lam,
      'inner_accuracy_pct':-negacc,'inner_logloss':ll,'inner_brier':brier,
      'inner_folds':folds,'train_n':len(train),'test_n':len(test),
      'top10':' | '.join(f"{q[5]}/{q[6]}@{q[4]} acc={-q[0]:.2f} ll={q[1]:.3f}" for q in grid[:10])
    })
    for r,p in zip(test,probs):
        pred=1 if p>=0.5 else 0
        act=1 if float(r['y'])>0 else 0
        predrows.append({
          'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
          'actual_margin':r['y'],'actual_direction':'D' if act else 'R',
          'pred_probability_D':float(p),'pred_direction':'D' if pred else 'R',
          'correct':1 if pred==act else 0,'model':kind,'architecture':aname,'lambda':lam
        })

def summarize(rs,scope):
    n=len(rs); correct=sum(int(r['correct']) for r in rs)
    y=[1 if r['actual_direction']=='D' else 0 for r in rs]
    p=[float(r['pred_probability_D']) for r in rs]
    eps=1e-9
    brier=float(np.mean((np.asarray(p)-np.asarray(y))**2))
    ll=float(-np.mean(np.asarray(y)*np.log(np.clip(p,eps,1-eps))+(1-np.asarray(y))*np.log(np.clip(1-np.asarray(p),eps,1-eps))))
    return {'scope':scope,'n':n,'correct':correct,'wrong':n-correct,'direction_accuracy_pct':100*correct/n,'brier':brier,'logloss':ll}

summary=[summarize(predrows,'combined')]
for tc in OUTER:
    summary.append(summarize([r for r in predrows if int(r['test_cycle'])==tc],str(tc)))

for fn,data in [('direction_summary.csv',summary),('direction_choices.csv',choices),('direction_predictions.csv',predrows)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

comb=summary[0]
wrong=[r for r in predrows if int(r['correct'])==0]
lines=[
 '# Primary-objective experiment: Senate direction accuracy OOS','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Primary objective is win/loss direction accuracy, not margin RMSE.',
 '- Hyperparameters and model family are selected using chronological inner OOS direction accuracy.',
 '- Tie-breakers are lower log loss, lower Brier score, then simpler architecture.','',
 '## Combined result','',
 '| N | correct | wrong | direction accuracy | Brier | log loss |',
 '|---:|---:|---:|---:|---:|---:|',
 f"| {comb['n']} | {comb['correct']} | {comb['wrong']} | {comb['direction_accuracy_pct']:.1f}% | {comb['brier']:.4f} | {comb['logloss']:.4f} |",'',
 '## By cycle','',
 '| cycle | N | correct | wrong | accuracy |',
 '|---:|---:|---:|---:|---:|'
]
for r in summary[1:]:
    lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Outer-fold selected models','',
 '| test | model | architecture | lambda | inner accuracy | inner log loss |',
 '|---:|---|---|---:|---:|---:|']
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['model']} | {r['architecture']} | {r['lambda']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_logloss']:.4f} |")
lines += ['','## Benchmarks','',
 '- Preserved Core V2 fundamentals direction accuracy: 90.9%.',
 '- Preserved Core V2 + poll direction accuracy: 91.9%.',
 '- New model is considered better on the primary task only if it exceeds those comparable direction benchmarks without test-fold tuning.','',
 '## Misclassified historical races','']
for r in wrong:
    lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: actual {r['actual_direction']}, predicted {r['pred_direction']}, P(D)={float(r['pred_probability_D']):.3f}")
lines += ['','## Outputs','',
 '- experiments/direction_accuracy/results/direction_summary.csv',
 '- experiments/direction_accuracy/results/direction_choices.csv',
 '- experiments/direction_accuracy/results/direction_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
