#!/usr/bin/env python3
import csv, itertools, re
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
PVI=ROOT/'data/processed/historical_senate_pvi_default_067_033.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
NAT=ROOT/'data/processed/core_v2r_national_components_45d_audit.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0210_national-approval-full-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

OUTER=[2014,2018,2022]
ALLC=[2006,2008,2010,2012,2014,2016,2018,2020,2022]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def truth(v): return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower()
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()

sen=load(SEN); pvirows=load(PVI); head=load(HEAD); ss=load(HEADSS); align=load(ALIGN); nat=load(NAT)
pvi={r['race_id']:float(r['pvi_default_067_033_pctpt']) for r in pvirows}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}
nat_by={int(r['cycle']):r for r in nat}
head_by={r['race_id']:r for r in head}
ss_by={r['race_id']:r for r in ss}

by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general':
        by[r['race_id']].append(r)

def groups(rr):
    out={}
    for r in rr:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key: continue
        c=out.setdefault(key,{'name':r.get('candidate_name') or '','votes':0,'parties':set(),'winner':False,'missing':False})
        for q in [(r.get('ballot_party') or ''),(r.get('party') or '')]:
            if q.strip(): c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v: c['missing']=True
        else:
            try: c['votes']+=int(float(v))
            except: c['missing']=True
        c['winner']=c['winner'] or truth(r.get('winner','false'))
    return list(out.values())

def extract(rr):
    first=rr[0]; cyc=int(first['cycle']); st=first['state_abbrev']; seat=first['office_seat_name']
    # RCV: use maximum explicit round only
    nums=[]
    for x in rr:
        v=(x.get('ranked_choice_round') or '').strip()
        if v:
            try: nums.append(int(float(v)))
            except: pass
    use=rr
    if nums:
        mx=max(nums); use=[]
        for x in rr:
            v=(x.get('ranked_choice_round') or '').strip()
            try: rv=int(float(v)) if v else None
            except: rv=None
            if rv==mx: use.append(x)
    cs=groups(use)
    ov=align_by.get((cyc,st,seat))
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}: return None
    d=r=None
    if ov and ov['action']=='ALIGN':
        ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])]
        rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
        d=ds[0] if len(ds)==1 else None
        r=rs[0] if len(rs)==1 else None
    if d is None and r is None:
        ds=[c for c in cs if 'DEM' in c['parties']]
        rs=[c for c in cs if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None
        r=rs[0] if len(rs)==1 else None
    if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0: return None
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,
            'y':(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0}

races=[]
for rid,rr in by.items():
    try:
        x=extract(rr)
        if x: races.append(x)
    except: pass

# Replace headline targets with preserved 99-row target margins.
rb={r['race_id']:r for r in races}
for rid,h in head_by.items():
    if rid in rb:
        rb[rid]['y']=float(h['margin_d_minus_r_two_party_pctpt'])

# Last-prior same-seat for all historical training races.
seat_hist=defaultdict(list)
for r in sorted(races,key=lambda z:(z['cycle'],z['state_abbrev'],z['seat'])):
    seat_hist[(r['state_abbrev'],r['seat'])].append(r)

rows=[]
for r in races:
    cyc=r['cycle']
    if cyc not in ALLC: continue
    if cyc in OUTER and r['race_id'] not in head_by: continue
    if cyc in OUTER:
        s=ss_by[r['race_id']]
        last=s['same_seat_last_prior_margin_two_party_pctpt']
        gap=s['same_seat_last_prior_year_gap']
        if not last or not gap: continue
        same=float(last); gap=float(gap)
    else:
        prev=[x for x in seat_hist[(r['state_abbrev'],r['seat'])] if x['cycle']<cyc]
        if not prev: continue
        q=max(prev,key=lambda z:z['cycle'])
        same=float(q['y']); gap=float(cyc-q['cycle'])
    pv=pvi.get(r['race_id'])
    n=nat_by.get(cyc)
    if pv is None or n is None or not n.get('net_approval'): continue
    sign=float(n['president_party_sign_D_plus1_R_minus1'])
    net=float(n['net_approval'])
    midterm=1.0 if cyc%4==2 else 0.0
    rows.append({
      'race_id':r['race_id'],'cycle':cyc,'state_abbrev':r['state_abbrev'],'y':float(r['y']),
      'pvi':pv,'same_last':same,'same_gap':gap,
      'approval_partisan':net*sign,
      'midterm_pres_party':midterm*sign,
      'approval_partisan_midterm':net*sign*midterm
    })

BASE=['pvi','same_last','same_gap']
NATFEAT=['approval_partisan','midterm_pres_party','approval_partisan_midterm']

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(train,test,features,lam=0.0,penalized=()):
    X,st=design(train,features); Xt,_=design(test,features,st)
    y=np.array([r['y'] for r in train],dtype=float)
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1):
        pen[j]=lam if f in penalized else 1e-8
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

subsets=[()]
for k in range(1,len(NATFEAT)+1):
    subsets += list(itertools.combinations(NATFEAT,k))
lams=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

def inner_select(train):
    cycles=sorted(set(int(r['cycle']) for r in train))
    cand=[]
    for subset in subsets:
        ls=[0.0] if not subset else lams
        for lam in ls:
            yy=[]; pp=[]
            feat=BASE+list(subset)
            for vc in cycles[1:]:
                tr=[r for r in train if int(r['cycle'])<vc]
                va=[r for r in train if int(r['cycle'])==vc]
                if len(tr)<20 or not va: continue
                pred=fitpred(tr,va,feat,lam,subset)
                yy.extend([r['y'] for r in va]); pp.extend(pred.tolist())
            score=rmse(yy,pp) if yy else 1e9
            cand.append((score,len(subset),lam,subset))
    cand.sort(key=lambda z:(z[0],z[1],z[2]))
    return cand[0],cand[:12]

preds=[]; choices=[]
for tc in OUTER:
    train=[r for r in rows if int(r['cycle'])<tc]
    test=[r for r in rows if int(r['cycle'])==tc]
    best,trace=inner_select(train)
    score,_,lam,subset=best
    feat=BASE+list(subset)
    pp=fitpred(train,test,feat,lam,subset)
    choices.append({'test_cycle':tc,'selected_features':';'.join(subset),'lambda':lam,'inner_rmse':score,
                    'top12':' | '.join(f'{x[3]}@{x[2]}:{x[0]:.3f}' for x in trace)})
    for r,p in zip(test,pp):
        preds.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                      'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],
                      'selected_features':';'.join(subset),'lambda':lam})

# fixed transparent variants
variants={'baseline':BASE,
          'approval_partisan':BASE+['approval_partisan'],
          'midterm_pres_party':BASE+['midterm_pres_party'],
          'approval_plus_midterm':BASE+['approval_partisan','midterm_pres_party'],
          'approval_midterm_interaction':BASE+['approval_partisan_midterm']}

summary=[]
for name,feat in variants.items():
    pr=[]
    for tc in OUTER:
        tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
        pp=fitpred(tr,te,feat,0.0,())
        pr += [(r['y'],float(p),tc) for r,p in zip(te,pp)]
    yy=[x[0] for x in pr]; pp=[x[1] for x in pr]
    summary.append({'variant':name,'n':len(pr),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

yy=[float(r['actual']) for r in preds]; pp=[float(r['predicted']) for r in preds]
summary.append({'variant':'nested_national_selection','n':len(preds),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

for name,data in [('national_approval_oos_summary.csv',summary),('national_approval_oos_choices.csv',choices),('national_approval_oos_predictions.csv',preds)]:
    with (OUTDIR/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)

base=next(x for x in summary if x['variant']=='baseline')
best=min(summary,key=lambda x:float(x['rmse']))
delta=float(base['rmse'])-float(best['rmse'])
lines=[
 '# Performance experiment: National approval on full chronological Senate training set','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Training/validation rows: {len(rows)}',
 '- Outer headline validation uses the preserved 99 races in 2014, 2018, and 2022.',
 '- Training also includes prior presidential-cycle Senate elections when available.','',
 '## Results','',
 '| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|'
]
for r in summary:
    lines.append(f"| {r['variant']} | {r['n']} | {float(r['rmse']):.4f} | {float(r['mae']):.4f} | {float(r['direction_pct']):.1f}% |")
lines += [
 '','## Nested choices','',
 '| test cycle | selected National features | lambda | inner RMSE |','|---:|---|---:|---:|'
]
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['selected_features'] or 'NONE'} | {r['lambda']} | {float(r['inner_rmse']):.4f} |")
lines += [
 '','## Decision','',
 f"- Baseline RMSE: {float(base['rmse']):.4f}.",
 f"- Best tested variant: {best['variant']} with RMSE {float(best['rmse']):.4f}.",
 f"- Improvement: {delta:+.4f} RMSE points.",
 '- A National term is retained only if it improves the identical OOS target universe.','',
 '## Important','',
 'This experiment deliberately uses the presidential-approval series that is available across all required cycles. It does not use the stale 2016 generic-ballot value for 2018 or 2022.','',
 '## Outputs','',
 '- performance/results/national_approval_oos_summary.csv',
 '- performance/results/national_approval_oos_choices.csv',
 '- performance/results/national_approval_oos_predictions.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
