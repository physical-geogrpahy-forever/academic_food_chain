#!/usr/bin/env python3
import csv, io, zipfile, statistics, itertools
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASEP=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
CANDP=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
NATP=ROOT/'performance/results/national_45d_values.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0220_candidate-era-interactions-oos.md'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
OUTER=[2014,2018,2022]
PRES_SIGN={2006:-1,2010:1,2014:1,2018:-1,2022:1}

STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
  with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

base=load(BASEP); ss=load(HEADSS); cand=load(CANDP); natrows=load(NATP)
candby={r['race_id']:r for r in cand}
nat={int(r['cycle']):float(r['national_margin_d_minus_r']) for r in natrows}

# Rebuild 2006/2010 training plus all 99 headline rows.
rows=[]
for r in base:
  cyc=int(r['cycle'])
  if cyc in (2006,2010):
    rows.append({
      'race_id':r['race_id'],'cycle':cyc,'state_abbrev':r['state_abbrev'],'y':float(r['y']),
      'pvi':float(r['pvi']),'same_last':float(r['same_seat']),'same_gap':6.0,
      'inc_diff':float(r['inc_diff']),'outparty':float(r['outparty']),
      'sen_exp_diff':float(r['sen_exp_diff']),'gov_exp_diff':float(r['gov_exp_diff']),'house_exp_diff':float(r['house_exp_diff'])
    })
for s in ss:
  c=candby[s['race_id']];cyc=int(s['cycle'])
  rows.append({
    'race_id':s['race_id'],'cycle':cyc,'state_abbrev':s['state_abbrev'],'y':float(s['margin_d_minus_r_two_party_pctpt']),
    'pvi':float(c['pvi_default_067_033_pctpt']),'same_last':float(s['same_seat_last_prior_margin_two_party_pctpt']),'same_gap':float(s['same_seat_last_prior_year_gap']),
    'inc_diff':float(c['IncumbencyDiff']),'outparty':float(c['OutPartyIncumbent']),
    'sen_exp_diff':float(c['SenateExperienceDiff']),'gov_exp_diff':float(c['GovernorExperienceDiff']),'house_exp_diff':float(c['HouseExperienceDiff'])
  })

# Exact SQINC1 signed relative-US economic term.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw));names=zf.namelist()
members=[n for n in names if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not members:raise RuntimeError('No exact SQINC1 file')
bname=max(members,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))))
pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,col):
  try:return float((r.get(col) or '').replace(',','').strip())
  except:return None
growth={};us={}
for r in pi:
  name=(r.get('GeoName') or '').replace('*','').strip()
  for cyc in PRES_SIGN:
    a=val(r,f'{cyc}:Q1');b=val(r,f'{cyc-1}:Q1')
    if a is None or b in (None,0):continue
    g=100*(a/b-1)
    if name in STATE_ABBR:growth[(cyc,STATE_ABBR[name])]=g
    elif name=='United States':us[cyc]=g

CAND=['inc_diff','outparty','sen_exp_diff','gov_exp_diff','house_exp_diff']
for r in rows:
  cyc=int(r['cycle']); st=r['state_abbrev']; era=(cyc-2006)/4.0
  vals=[growth[(cyc,s)] for s in STATE_ABBR.values() if (cyc,s) in growth]
  natg=us.get(cyc,statistics.mean(vals))
  r['econ']=(growth[(cyc,st)]-natg)*PRES_SIGN[cyc]
  r['national']=nat[cyc]
  r['era']=era
  r['same_era']=r['same_last']*era
  for f in CAND:r[f+'_era']=r[f]*era

BASE=['pvi','same_last','same_gap','econ','national']
ARCH={
 'none':[],
 'seat_era':['same_era'],
 'inc_level':['inc_diff','outparty'],
 'inc_era':['inc_diff','outparty','inc_diff_era','outparty_era'],
 'candidate_level':CAND,
 'candidate_era':CAND+[f+'_era' for f in CAND],
 'full_local_era':['same_era']+CAND+[f+'_era' for f in CAND]
}
NAT_LAM=[0.0,4.0,16.0,64.0,256.0]
LEVEL_LAM=[4.0,16.0,64.0,256.0,1024.0]
ERA_LAM=[16.0,64.0,256.0,1024.0,4096.0]

def design(dat,features,stats=None):
  X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
  if stats is None:
    mu=X.mean(axis=0);sd=X.std(axis=0);sd=np.where(sd<1e-9,1.0,sd)
  else:mu,sd=stats
  return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(train,test,arch,nlam,llam,elam):
  local=ARCH[arch];feats=BASE+local
  X,st=design(train,feats);Xt,_=design(test,feats,st);y=np.array([r['y'] for r in train])
  pen=np.zeros(X.shape[1])
  for j,f in enumerate(feats,start=1):
    if f=='national':pen[j]=nlam
    elif f.endswith('_era') or f=='same_era':pen[j]=elam
    elif f in CAND:pen[j]=llam
  A=X.T@X+np.diag(pen+1e-8);A[0,0]-=1e-8
  beta=np.linalg.pinv(A)@(X.T@y)
  return Xt@beta

def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def inner_score(train,arch,nlam,llam,elam):
  cycles=sorted(set(int(r['cycle']) for r in train));yy=[];pp=[]
  for vc in cycles[1:]:
    tr=[r for r in train if int(r['cycle'])<vc];va=[r for r in train if int(r['cycle'])==vc]
    if len(tr)<10 or not va:continue
    q=fitpred(tr,va,arch,nlam,llam,elam)
    yy.extend(r['y'] for r in va);pp.extend(q.tolist())
  return rmse(yy,pp) if yy else 1e9

nested=[];choices=[]
for tc in OUTER:
  tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
  grid=[]
  for arch in ARCH:
    nlams=NAT_LAM
    llams=[64.0] if arch in ('none','seat_era') else LEVEL_LAM
    elams=[256.0] if arch in ('none','inc_level','candidate_level') else ERA_LAM
    for nlam,llam,elam in itertools.product(nlams,llams,elams):
      sc=inner_score(tr,arch,nlam,llam,elam)
      grid.append((sc,arch,nlam,llam,elam))
  grid.sort(key=lambda z:(z[0],len(ARCH[z[1]]),z[2],z[3],z[4]))
  sc,arch,nlam,llam,elam=grid[0]
  q=fitpred(tr,te,arch,nlam,llam,elam)
  choices.append({'test_cycle':tc,'arch':arch,'national_lambda':nlam,'level_lambda':llam,'era_lambda':elam,'inner_rmse':sc,'top10':' | '.join(f'{z[1]}@N{z[2]}/L{z[3]}/E{z[4]}:{z[0]:.4f}' for z in grid[:10])})
  for r,p in zip(te,q):nested.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],'arch':arch})

# Transparent fixed diagnostics: no local era vs several predeclared era architectures.
summary=[]
fixed=[('base_national64','none',64,64,256),('seat_era','seat_era',64,64,256),('inc_era','inc_era',64,64,256),('candidate_era','candidate_era',64,64,256),('full_local_era','full_local_era',64,64,256)]
for name,arch,nlam,llam,elam in fixed:
  yy=[];pp=[]
  for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
    q=fitpred(tr,te,arch,nlam,llam,elam);yy.extend(r['y'] for r in te);pp.extend(q.tolist())
  summary.append({'variant':name,'n':len(yy),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})
yy=[r['actual'] for r in nested];pp=[r['predicted'] for r in nested]
summary.append({'variant':'nested_training_only','n':len(yy),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

for fn,data in [('candidate_era_oos_summary.csv',summary),('candidate_era_oos_choices.csv',choices),('candidate_era_oos_predictions.csv',nested)]:
  with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

basev=next(z for z in summary if z['variant']=='base_national64');nest=next(z for z in summary if z['variant']=='nested_training_only')
lines=['# Performance experiment: candidate/local era interactions OOS','',
f'- Generated UTC: {datetime.now(timezone.utc).isoformat()}',
f'- BEA member: {bname}',
'- Baseline includes PVI, last-prior SameSeat, SameSeat gap, signed RelativeEconomicGrowth, and 45-day Generic Ballot National.',
'- Era index is (cycle-2006)/4, so candidate/local coefficients can change linearly across midterm cycles.','',
'## Combined 99-row modern OOS','',
'| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|']
for z in summary:lines.append(f"| {z['variant']} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += ['','## Nested choices','',
'| test cycle | architecture | National ridge | level ridge | era ridge | inner RMSE |','|---:|---|---:|---:|---:|---:|']
for z in choices:lines.append(f"| {z['test_cycle']} | {z['arch']} | {z['national_lambda']} | {z['level_lambda']} | {z['era_lambda']} | {float(z['inner_rmse']):.4f} |")
lines += ['','## Decision','',
f'- Fixed National64 no-local baseline RMSE: {float(basev["rmse"]):.4f}.',
f'- Leakage-safe nested candidate/local era RMSE: {float(nest["rmse"]):.4f}.',
f'- Nested improvement: {float(basev["rmse"])-float(nest["rmse"]):+.4f} RMSE points.',
'- Candidate/local era structure is retained only if the nested training-only result improves on the comparable baseline.','',
'## Outputs','',
'- performance/results/candidate_era_oos_summary.csv',
'- performance/results/candidate_era_oos_choices.csv',
'- performance/results/candidate_era_oos_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))