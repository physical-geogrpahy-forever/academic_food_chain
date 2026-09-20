#!/usr/bin/env python3
import csv, itertools
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
CAND=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
NAT=ROOT/'data/processed/core_v2r_national_components_45d_audit.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0210_approval-national-99row-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True)

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
base=load(BASE); ss=load(HEADSS); cand=load(CAND); nat=load(NAT)
cby={r['race_id']:r for r in cand}; nby={int(r['cycle']):r for r in nat}

rows=[]
for r in base:
    if int(r['cycle']) in (2006,2010):
        x=dict(r); x['same_last']=float(r['same_seat']); x['same_gap']=6.0; rows.append(x)
for s in ss:
    c=cby[s['race_id']]
    rows.append({'race_id':s['race_id'],'cycle':int(s['cycle']),'state_abbrev':s['state_abbrev'],
      'y':float(s['margin_d_minus_r_two_party_pctpt']),'pvi':float(c['pvi_default_067_033_pctpt']),
      'same_last':float(s['same_seat_last_prior_margin_two_party_pctpt']),
      'same_gap':float(s['same_seat_last_prior_year_gap'])})

for r in rows:
    n=nby[int(r['cycle'])]
    sign=float(n['president_party_sign_D_plus1_R_minus1'])
    net=float(n['net_approval'])
    r['pres_party_sign']=sign
    r['signed_net_approval']=sign*net

OUTER=[2014,2018,2022]
BASEF=['pvi','same_last','same_gap']
EXTRAS=['pres_party_sign','signed_net_approval']
LGRID=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(train,test,extras=(),lam=0.0):
    features=BASEF+list(extras)
    X,st=design(train,features); Xt,_=design(test,features,st)
    y=np.array([float(r['y']) for r in train])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1): pen[j]=lam if f in extras else 1e-8
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train)); candidates=[]
    subsets=[(),('pres_party_sign',),('signed_net_approval',),tuple(EXTRAS)]
    for sub in subsets:
      for lam in ([0.0] if not sub else LGRID):
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr=fitpred(tr,va,sub,lam); yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        candidates.append((rmse(yy,pp) if yy else 1e9,len(sub),lam,sub))
    candidates.sort(key=lambda z:(z[0],z[1],z[2]))
    return candidates[0],candidates

variants=['baseline','approval_signed_fixed','approval_plus_party_fixed','approval_nested']
pred=[]; hyper=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
    for v in variants:
        if v=='baseline': sub=(); lam=0.0
        elif v=='approval_signed_fixed': sub=('signed_net_approval',); lam=0.0
        elif v=='approval_plus_party_fixed': sub=('pres_party_sign','signed_net_approval'); lam=0.0
        else:
            best,trace=tune(tr); _,_,lam,sub=best
            hyper.append({'test_cycle':tc,'selected_features':';'.join(sub),'lambda':lam,'inner_rmse':best[0],'top10':' | '.join(f'{z[3]}@{z[2]}:{z[0]:.4f}' for z in trace[:10])})
        pp=fitpred(tr,te,sub,lam)
        for r,p in zip(te,pp): pred.append({'variant':v,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-float(r['y']),'features':';'.join(sub),'lambda':lam})

summary=[]
for v in variants:
    rr=[r for r in pred if r['variant']==v]; y=[float(r['actual']) for r in rr]; p=[float(r['predicted']) for r in rr]
    summary.append({'variant':v,'scope':'combined','n':len(rr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':acc(y,p)})
    for tc in OUTER:
        z=[r for r in rr if int(r['test_cycle'])==tc]; yy=[float(r['actual']) for r in z]; pp=[float(r['predicted']) for r in z]
        summary.append({'variant':v,'scope':str(tc),'n':len(z),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

for name,data in [('approval_national_99row_predictions.csv',pred),('approval_national_99row_summary.csv',summary),('approval_national_99row_hyperparams.csv',hyper)]:
    with (OUTDIR/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)

comb={r['variant']:r for r in summary if r['scope']=='combined'}
b=comb['baseline']; best=min([comb[x] for x in variants[1:]],key=lambda z:float(z['rmse']))
delta=float(b['rmse'])-float(best['rmse'])
lines=['# Performance experiment: presidential approval National proxy on 99 rows','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Baseline: PVI + last-prior SameSeat + year gap.',
 '- National inputs are fixed at 45 days before each federal general election.',
 '- signed_net_approval = president-party sign in D-minus-R direction multiplied by net approval.','',
 '## Results','', '| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|']
for v in variants:
    z=comb[v]; lines.append(f"| {v} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += ['','## Decision','',
 f'- Best National architecture: {best["variant"]}.',
 f'- Improvement versus 99-row baseline: {delta:+.4f} RMSE points.',
 f'- Decision: {"KEEP_APPROVAL_NATIONAL" if delta>0 else "REJECT_APPROVAL_NATIONAL"}.','',
 '## Next','',
 'If kept, use this National structure as the new structural baseline and test RelativeEconomicGrowth next. Candidate blocks remain excluded unless they improve the stronger baseline.','',
 '## Outputs','',
 '- performance/results/approval_national_99row_summary.csv',
 '- performance/results/approval_national_99row_hyperparams.csv',
 '- performance/results/approval_national_99row_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))