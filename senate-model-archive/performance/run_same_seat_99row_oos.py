#!/usr/bin/env python3
import csv, itertools, math
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0204_same-seat-99row-performance.md'

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

base=load(BASE)
ss=load(HEADSS)

# Existing candidate-block panel is reliable for candidate/PVI fields on its retained rows.
# For the 8 headline rows dropped only because exact-6 SameSeat was missing, reconstruct
# the row from the 99-row SameSeat audit and candidate feature tables already committed.
cand=load(ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv')
cand_by={r['race_id']:r for r in cand}
base_by={r['race_id']:r for r in base}

rows=[]
# keep 2006/2010 training rows from prior panel
for r in base:
    if int(r['cycle']) in (2006,2010):
        x=dict(r)
        x['same_exact_available']='1'
        x['same_exact']=r['same_seat']
        x['same_last']=r['same_seat']
        x['same_gap']='6'
        rows.append(x)

# rebuild all 99 headline rows with exact/last/gap fields
for s in ss:
    rid=s['race_id']; c=cand_by[rid]
    exact_av=s['same_seat_exact6_available'].lower()=='true'
    exact=s['same_seat_exact6_margin_two_party_pctpt']
    last=s['same_seat_last_prior_margin_two_party_pctpt']
    gap=s['same_seat_last_prior_year_gap']
    rows.append({
      'race_id':rid,'cycle':int(s['cycle']),'state_abbrev':s['state_abbrev'],'seat':s['seat'],
      'y':float(s['margin_d_minus_r_two_party_pctpt']),
      'pvi':float(c['pvi_default_067_033_pctpt']),
      'same_seat':float(last) if last else 0.0,
      'inc_diff':int(c['IncumbencyDiff']),
      'outparty':int(c['OutPartyIncumbent']),
      'sen_exp_diff':int(c['SenateExperienceDiff']),
      'gov_exp_diff':int(c['GovernorExperienceDiff']),
      'house_exp_diff':int(c['HouseExperienceDiff']),
      'same_exact_available':'1' if exact_av else '0',
      'same_exact':float(exact) if exact else 0.0,
      'same_last':float(last) if last else 0.0,
      'same_gap':float(gap) if gap else 99.0
    })

OUTER=[2014,2018,2022]
CAND=['inc_diff','outparty','sen_exp_diff','gov_exp_diff','house_exp_diff']

# Three leakage-safe SameSeat encodings.
STRUCTS={
 'exact6_zero_plus_missing':['pvi','same_exact','same_exact_missing'],
 'last_prior_plus_gap':['pvi','same_last','same_gap'],
 'hybrid_exact_else_last':['pvi','same_hybrid','same_fallback','same_gap_excess']
}

for r in rows:
    av=int(r['same_exact_available'])
    r['same_exact_missing']=1-av
    r['same_hybrid']=float(r['same_exact']) if av else float(r['same_last'])
    r['same_fallback']=1-av
    r['same_gap_excess']=max(float(r['same_gap'])-6.0,0.0)

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(train,test,features,lam=0.0,cand_features=()):
    X,st=design(train,features); Xt,_=design(test,features,st)
    y=np.array([float(r['y']) for r in train])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1):
        pen[j]=lam if f in cand_features else 1e-8
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def inner_score(train,struct_name,subset,lam):
    features=STRUCTS[struct_name]+list(subset)
    cycles=sorted(set(int(r['cycle']) for r in train))
    yy=[]; pp=[]
    for vc in cycles[1:]:
        tr=[r for r in train if int(r['cycle'])<vc]
        va=[r for r in train if int(r['cycle'])==vc]
        if len(tr)<10 or not va: continue
        pred=fitpred(tr,va,features,lam,subset)
        yy += [float(r['y']) for r in va]; pp += pred.tolist()
    return rmse(yy,pp) if yy else 1e9

subsets=[()]
for k in range(1,len(CAND)+1): subsets += list(itertools.combinations(CAND,k))
lams=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

preds=[]; choices=[]
for tc in OUTER:
    train=[r for r in rows if int(r['cycle'])<tc]
    test=[r for r in rows if int(r['cycle'])==tc]
    search=[]
    for sn in STRUCTS:
        # allow structural-only and candidate subsets
        for subset in subsets:
            use_lams=[0.0] if not subset else lams
            for lam in use_lams:
                sc=inner_score(train,sn,subset,lam)
                search.append((sc,len(subset),lam,sn,subset))
    search.sort(key=lambda z:(z[0],z[1],z[2]))
    best=search[0]
    sc,_,lam,sn,subset=best
    features=STRUCTS[sn]+list(subset)
    pp=fitpred(train,test,features,lam,subset)
    choices.append({'test_cycle':tc,'selected_same_seat':sn,'selected_candidate_features':';'.join(subset),'lambda_candidate':lam,'inner_rmse':sc,'top10':' | '.join(f'{z[3]}+{z[4]}@{z[2]}:{z[0]:.3f}' for z in search[:10])})
    for r,p in zip(test,pp):
        preds.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-float(r['y']),'same_seat':sn,'candidate_features':';'.join(subset),'lambda_candidate':lam})

# Also evaluate each SameSeat encoding with no candidate block for transparent comparison.
summary=[]
for sn in STRUCTS:
    pr=[]
    for tc in OUTER:
        tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
        pp=fitpred(tr,te,STRUCTS[sn],0.0,())
        for r,p in zip(te,pp): pr.append((float(r['y']),float(p),tc))
    y=[x[0] for x in pr]; p=[x[1] for x in pr]
    summary.append({'variant':'struct_'+sn,'n':len(pr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':acc(y,p)})

y=[float(r['actual']) for r in preds]; p=[float(r['predicted']) for r in preds]
summary.append({'variant':'nested_joint_sameSeat_plus_candidate','n':len(preds),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':acc(y,p)})

for name,data in [('same_seat_99row_predictions.csv',preds),('same_seat_99row_choices.csv',choices),('same_seat_99row_summary.csv',summary)]:
    path=OUTDIR/name
    fields=list(data[0].keys())
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)

best_struct=min([r for r in summary if r['variant'].startswith('struct_')],key=lambda z:float(z['rmse']))
joint=next(r for r in summary if r['variant']=='nested_joint_sameSeat_plus_candidate')
delta=float(best_struct['rmse'])-float(joint['rmse'])
lines=[
 '# Performance experiment: SameSeat handling on full 99-row headline sample','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Outer validation rows: 99 exactly (2014, 2018, 2022 preserved headline universe).','',
 '## Results','',
 '| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|'
]
for r in summary: lines.append(f"| {r['variant']} | {r['n']} | {float(r['rmse']):.4f} | {float(r['mae']):.4f} | {float(r['direction_pct']):.1f}% |")
lines += [
 '','## Nested choices by outer cycle','',
 '| test cycle | SameSeat encoding | candidate features | lambda | inner RMSE |','|---:|---|---|---:|---:|'
]
for r in choices: lines.append(f"| {r['test_cycle']} | {r['selected_same_seat']} | {r['selected_candidate_features'] or 'NONE'} | {r['lambda_candidate']} | {float(r['inner_rmse']):.4f} |")
lines += [
 '','## Decision','',
 f'- Best structural SameSeat encoding: {best_struct["variant"]} with RMSE {float(best_struct["rmse"]):.4f}.',
 f'- Joint nested selection RMSE: {float(joint["rmse"]):.4f}.',
 f'- Joint improvement versus best no-candidate structural encoding: {delta:+.4f} RMSE points.',
 '- Keep candidate augmentation only if the improvement is positive. Otherwise use the best SameSeat structural encoding and move to National/economic/personal-vote terms.','',
 '## Why this supersedes the 91-row candidate experiment','',
 'The prior experiment dropped 8 headline races because it required an exact six-year SameSeat record. The preserved handoff benchmark uses 99 races. This experiment keeps all 99 and treats missing exact-six information explicitly rather than deleting the race.','',
 '## Outputs','',
 '- performance/results/same_seat_99row_summary.csv',
 '- performance/results/same_seat_99row_choices.csv',
 '- performance/results/same_seat_99row_predictions.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))