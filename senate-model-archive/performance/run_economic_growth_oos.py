#!/usr/bin/env python3
import csv, io, zipfile, statistics
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
CAND=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0210_relative-economic-growth-oos.md'
URL='https://apps.bea.gov/regional/zip/SQINC.zip'
OUTDIR.mkdir(parents=True,exist_ok=True)

STATE_ABBR={
'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
PRES_SIGN={2006:-1,2010:1,2014:1,2018:-1,2022:1}
OUTER=[2014,2018,2022]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
base=load(BASE); ss=load(HEADSS); cand=load(CAND); candby={r['race_id']:r for r in cand}

# Build the same 99-row last-prior+gap structural panel plus 2006/2010 training rows.
rows=[]
for r in base:
    if int(r['cycle']) in (2006,2010):
        x={'race_id':r['race_id'],'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'y':float(r['y']),'pvi':float(r['pvi']),'same_last':float(r['same_seat']),'same_gap':6.0}
        rows.append(x)
for s in ss:
    c=candby[s['race_id']]
    rows.append({'race_id':s['race_id'],'cycle':int(s['cycle']),'state_abbrev':s['state_abbrev'],'y':float(s['margin_d_minus_r_two_party_pctpt']),'pvi':float(c['pvi_default_067_033_pctpt']),'same_last':float(s['same_seat_last_prior_margin_two_party_pctpt']),'same_gap':float(s['same_seat_last_prior_year_gap'])})

# Download BEA SQINC1 ZIP and locate the all-areas CSV.
raw=urlopen(Request(URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw))
names=zf.namelist()
csvnames=[n for n in names if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not csvnames: raise RuntimeError('No exact SQINC1__ALL_AREAS CSV in zip; matching candidates='+str([n for n in names if 'SQINC1' in n.upper()][:30]))
name=max(csvnames,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(name).decode('utf-8-sig','replace'))))
if not bea: raise RuntimeError('Empty SQINC1 CSV')

# Personal income level is LineCode 1 in SQINC1. Fallback to description prefix if needed.
pirows=[]
for r in bea:
    lc=(r.get('LineCode') or '').strip()
    desc=(r.get('Description') or '').lower()
    if lc=='1' or desc.startswith('personal income'): pirows.append(r)
if len(pirows)<50: raise RuntimeError(f'Only {len(pirows)} PI rows; fields={list(bea[0].keys())}; sample={bea[:2]}')

def clean_name(x): return (x or '').replace('*','').strip()
def val(r,col):
    x=(r.get(col) or '').replace(',','').strip()
    try:return float(x)
    except:return None

# Collect state and U.S. Q1 YoY growth.
growth={}; us_growth={}
for r in pirows:
    gname=clean_name(r.get('GeoName'))
    for cyc in PRES_SIGN:
        a=val(r,f'{cyc}:Q1'); b=val(r,f'{cyc-1}:Q1')
        if a is None or b in (None,0): continue
        g=100.0*(a/b-1.0)
        if gname in STATE_ABBR: growth[(cyc,STATE_ABBR[gname])]=g
        elif gname in {'United States','United States '}: us_growth[cyc]=g

for cyc in PRES_SIGN:
    vals=[growth[(cyc,st)] for st in STATE_ABBR.values() if (cyc,st) in growth]
    if len(vals)<48: raise RuntimeError(f'Only {len(vals)} state growth values for {cyc}')
    med=statistics.median(vals)
    # If US row absent, use arithmetic state mean as a transparent fallback diagnostic.
    nat=us_growth.get(cyc,statistics.mean(vals))
    for r in rows:
        if int(r['cycle'])!=cyc: continue
        g=growth.get((cyc,r['state_abbrev']))
        if g is None: raise RuntimeError(f'Missing growth {cyc} {r["state_abbrev"]}')
        r['econ_rel_us']=g-nat
        r['econ_rel_median']=g-med
        r['econ_rel_us_signed']=(g-nat)*PRES_SIGN[cyc]
        r['econ_rel_median_signed']=(g-med)*PRES_SIGN[cyc]

STRUCT=['pvi','same_last','same_gap']
ECON=['econ_rel_us','econ_rel_median','econ_rel_us_signed','econ_rel_median_signed']
LGRID=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)
def pred(train,test,econ=None,lam=0.0):
    feats=STRUCT+([econ] if econ else [])
    X,st=design(train,feats); Xt,_=design(test,feats,st); y=np.array([r['y'] for r in train])
    pen=np.zeros(X.shape[1]);
    if econ: pen[-1]=lam
    A=X.T@X+np.diag(pen+1e-8); A[0,0]-=1e-8
    beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train)); cand=[]
    for e in [None]+ECON:
      lams=[0.0] if e is None else LGRID
      for lam in lams:
        yy=[];pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            q=pred(tr,va,e,lam); yy.extend(r['y'] for r in va); pp.extend(q.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,0 if e is None else 1,lam,'' if e is None else e))
    cand.sort(key=lambda x:(x[0],x[1],x[2])); return cand[0],cand

predrows=[]; choices=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
    best,trace=tune(tr); sc,_,lam,e=best; econ=e or None
    q=pred(tr,te,econ,lam)
    choices.append({'test_cycle':tc,'selected_econ':e or 'NONE','lambda':lam,'inner_rmse':sc,'top10':' | '.join(f'{z[3] or "NONE"}@{z[2]}:{z[0]:.4f}' for z in trace[:10])})
    for r,p in zip(te,q): predrows.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],'selected_econ':e or 'NONE','lambda':lam})

# fixed transparent baselines for comparison
summary=[]
for e in [None]+ECON:
    prs=[]
    for tc in OUTER:
      tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
      q=pred(tr,te,e,0.0)
      prs += [(r['y'],float(p)) for r,p in zip(te,q)]
    yy=[x[0] for x in prs]; pp=[x[1] for x in prs]
    summary.append({'variant':'structural' if e is None else e,'n':len(prs),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})
yy=[float(r['actual']) for r in predrows]; pp=[float(r['predicted']) for r in predrows]
summary.append({'variant':'econ_nested_selection','n':len(predrows),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

for fn,data in [('economic_growth_oos_summary.csv',summary),('economic_growth_oos_choices.csv',choices),('economic_growth_oos_predictions.csv',predrows)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
      w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

basev=next(x for x in summary if x['variant']=='structural'); best=min(summary,key=lambda x:float(x['rmse']))
delta=float(basev['rmse'])-float(best['rmse'])
lines=['# Performance experiment: RelativeEconomicGrowth OOS','',
' - Generated UTC: '+datetime.now(timezone.utc).isoformat(),
f'- BEA source: {URL}',f'- ZIP bytes: {len(raw)}',f'- CSV member: {name}',
'- Economic diagnostic uses Q1 year-over-year personal-income growth from current revised SQINC1 values. This is a signal test, not yet a historical-vintage-valid headline model.','',
'## Combined 99-row modern OOS results','',
'| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|']
for z in summary:lines.append(f"| {z['variant']} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += ['','## Nested choices','',
'| test cycle | selected economic coding | lambda | inner RMSE |','|---:|---|---:|---:|']
for z in choices:lines.append(f"| {z['test_cycle']} | {z['selected_econ']} | {z['lambda']} | {float(z['inner_rmse']):.4f} |")
lines += ['','## Decision','',
f'- Structural baseline RMSE: {float(basev["rmse"]):.4f}.',
f'- Best observed architecture: {best["variant"]}, RMSE {float(best["rmse"]):.4f}.',
f'- Improvement: {delta:+.4f} RMSE points.',
'- Retain the economic architecture for full Core V2-R only if improvement is positive. Before claiming headline comparability, rerun with release-vintage-consistent BEA data.','',
'## Outputs','',
'- performance/results/economic_growth_oos_summary.csv',
'- performance/results/economic_growth_oos_choices.csv',
'- performance/results/economic_growth_oos_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))