#!/usr/bin/env python3
import csv, math
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PANEL=ROOT/'performance/results/candidate_block_oos_panel.csv'
PV=ROOT/'data/processed/core_v2r_personal_vote_sufficient_statistics.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0204_personal-vote-rolling-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True)

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
panel=load(PANEL); pv=load(PV)
pvby={(r['target_race_id'],r['side']):r for r in pv}

def side_stats(rid,side):
    r=pvby.get((rid,side))
    if not r: return 0.0,0
    v=r['mean_own_party_overperf_cycle_adjusted_pctpt']
    n=int(r['prior_statewide_count'])
    return (float(v) if v else 0.0),n

for r in panel:
    dm,dn=side_stats(r['race_id'],'D'); rm,rn=side_stats(r['race_id'],'R')
    r['d_pv_mean']=dm; r['d_pv_n']=dn; r['r_pv_mean']=rm; r['r_pv_n']=rn

STRUCT=['pvi','same_seat']
KGRID=[0.5,1.0,2.0,4.0,8.0,16.0,32.0]
LGRID=[0.0,0.1,0.5,1.0,4.0,16.0,64.0]
OUTER=[2014,2018,2022]

def pvscore(r,k):
    d=float(r['d_pv_mean'])*int(r['d_pv_n'])/(int(r['d_pv_n'])+k) if int(r['d_pv_n'])>0 else 0.0
    q=float(r['r_pv_mean'])*int(r['r_pv_n'])/(int(r['r_pv_n'])+k) if int(r['r_pv_n'])>0 else 0.0
    return d-q

def design(rows,extra=None,stats=None):
    feats=STRUCT+([extra] if extra else [])
    vals=[]
    for r in rows:
        row=[float(r[f]) for f in STRUCT]
        if extra: row.append(float(r[extra]))
        vals.append(row)
    X=np.array(vals,dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(rows)),(X-mu)/sd]),(mu,sd)

def fit_basic(train,test,y_override=None,extra=None,lam=0.0):
    X,stats=design(train,extra); Xt,_=design(test,extra,stats)
    y=np.array(y_override if y_override is not None else [float(r['y']) for r in train])
    pen=np.zeros(X.shape[1]);
    if extra: pen[-1]=lam
    A=X.T@X+np.diag(pen+1e-8)
    A[0,0]-=1e-8
    beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def direction(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100.0)

def predict_struct(train,test): return fit_basic(train,test)

def predict_offset(train,test,k):
    yadj=[float(r['y'])-pvscore(r,k) for r in train]
    base=fit_basic(train,test,y_override=yadj)
    return np.array([b+pvscore(r,k) for b,r in zip(base,test)])

def predict_reg(train,test,k,lam):
    col='__pv'
    for r in train+test: r[col]=pvscore(r,k)
    return fit_basic(train,test,extra=col,lam=lam)

def tune_offset(train):
    cycles=sorted(set(int(r['cycle']) for r in train))
    cand=[]
    for k in KGRID:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr=predict_offset(tr,va,k); yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,-k,k))
    cand.sort(); return cand[0][2],cand

def tune_reg(train):
    cycles=sorted(set(int(r['cycle']) for r in train))
    cand=[]
    for k in KGRID:
      for lam in LGRID:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr=predict_reg(tr,va,k,lam); yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,-k,-lam,k,lam))
    cand.sort(); return cand[0][3],cand[0][4],cand

variants=['structural_only','personal_offset_nested','personal_regression_nested']
pred=[]; hyper=[]
for tc in OUTER:
    train=[r for r in panel if int(r['cycle'])<tc]; test=[r for r in panel if int(r['cycle'])==tc]
    for v in variants:
        if v=='structural_only': pr=predict_struct(train,test); k=''; lam=''
        elif v=='personal_offset_nested':
            k,trace=tune_offset(train); lam=''; pr=predict_offset(train,test,k)
            hyper.append({'test_cycle':tc,'variant':v,'k':k,'lambda':'','inner_trace':' | '.join(f'k={x[2]}:{x[0]:.4f}' for x in trace)})
        else:
            k,lam,trace=tune_reg(train); pr=predict_reg(train,test,k,lam)
            hyper.append({'test_cycle':tc,'variant':v,'k':k,'lambda':lam,'inner_trace':' | '.join(f'k={x[3]},l={x[4]}:{x[0]:.4f}' for x in trace[:15])})
        for r,p in zip(test,pr): pred.append({'variant':v,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual_margin':r['y'],'predicted_margin':float(p),'error':float(p)-float(r['y']),'k':k,'lambda':lam})

summary=[]
for v in variants:
    rr=[r for r in pred if r['variant']==v]
    y=[float(r['actual_margin']) for r in rr]; p=[float(r['predicted_margin']) for r in rr]
    summary.append({'variant':v,'scope':'2014_2018_2022_combined','n':len(rr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':direction(y,p)})
    for tc in OUTER:
        z=[r for r in rr if int(r['test_cycle'])==tc]; yy=[float(r['actual_margin']) for r in z]; pp=[float(r['predicted_margin']) for r in z]
        summary.append({'variant':v,'scope':str(tc),'n':len(z),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':direction(yy,pp)})

for name,data in [('personal_vote_oos_predictions.csv',pred),('personal_vote_oos_summary.csv',summary),('personal_vote_oos_hyperparams.csv',hyper)]:
    with (OUTDIR/name).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)

comb={r['variant']:r for r in summary if r['scope']=='2014_2018_2022_combined'}
base=comb['structural_only']; off=comb['personal_offset_nested']; reg=comb['personal_regression_nested']
do=float(base['rmse'])-float(off['rmse']); dr=float(base['rmse'])-float(reg['rmse'])
best='personal_offset_nested' if off['rmse']<reg['rmse'] else 'personal_regression_nested'
bestdelta=max(do,dr)
decision='KEEP_PERSONAL_VOTE_ARCHITECTURE' if bestdelta>0 else 'REJECT_PERSONAL_VOTE_ARCHITECTURE'
lines=[
 '# Performance experiment: PersonalVote rolling OOS','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Same 91-race modern validation universe as the candidate-block diagnostic.',
 '- 2006/2010 rows have no reconstructed headline PersonalVote sufficient-statistics file and therefore receive the zero prior, not a fabricated score.','',
 '## Combined results','',
 '| variant | N | RMSE | MAE | direction |',
 '|---|---:|---:|---:|---:|'
]
for v in variants:
    z=comb[v]; lines.append(f"| {v} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += [
 '','## Decision','',
 f'- Personal offset improvement vs structural: {do:+.4f} RMSE points.',
 f'- Personal regression improvement vs structural: {dr:+.4f} RMSE points.',
 f'- Best PersonalVote architecture: {best}.',
 f'- Decision: {decision}','',
 '## Interpretation guard','',
 'This experiment tests only whether pre-election candidate overperformance contains transferable OOS signal after count shrinkage. It is still not the complete Core V2 because National_t, RelativeEconomicGrowth, and poll update are absent.','',
 '## Outputs','',
 '- performance/results/personal_vote_oos_predictions.csv',
 '- performance/results/personal_vote_oos_summary.csv',
 '- performance/results/personal_vote_oos_hyperparams.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))