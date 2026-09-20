#!/usr/bin/env python3
import csv, io, zipfile, statistics
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone, date, timedelta
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
CAND=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0215_national-generic-ballot-oos.md'

HIST_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_topline_historical.csv'
AVG_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_ballot_averages.csv'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
ELECTION={2006:date(2006,11,7),2010:date(2010,11,2),2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
PRES_SIGN={2006:-1,2010:1,2014:1,2018:-1,2022:1}
OUTER=[2014,2018,2022]

STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
  with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def fetch_csv(url):
  raw=urlopen(Request(url,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
  return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace')))),len(raw)

# Build structural panel.
base=load(BASE); ss=load(HEADSS); cand=load(CAND); candby={r['race_id']:r for r in cand}
rows=[]
for r in base:
  if int(r['cycle']) in (2006,2010):
    rows.append({'race_id':r['race_id'],'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'y':float(r['y']),'pvi':float(r['pvi']),'same_last':float(r['same_seat']),'same_gap':6.0})
for s in ss:
  c=candby[s['race_id']]
  rows.append({'race_id':s['race_id'],'cycle':int(s['cycle']),'state_abbrev':s['state_abbrev'],'y':float(s['margin_d_minus_r_two_party_pctpt']),'pvi':float(c['pvi_default_067_033_pctpt']),'same_last':float(s['same_seat_last_prior_margin_two_party_pctpt']),'same_gap':float(s['same_seat_last_prior_year_gap'])})

# National generic ballot D-R at target date = election day - 45 days.
hist,hbytes=fetch_csv(HIST_URL); avg,abytes=fetch_csv(AVG_URL)
nat={}; nat_meta={}
def pdate(s):
  m,d,y=[int(x) for x in s.split('/')]; return date(y,m,d)

for cyc in (2006,2010,2014):
  target=ELECTION[cyc]-timedelta(days=45)
  candidates=[]
  for r in hist:
    if (r.get('subgroup') or '').strip()!='All polls': continue
    try:dt=pdate((r.get('modeldate') or '').strip())
    except:continue
    if dt.year not in (cyc-1,cyc): continue
    try:margin=float(r['dem_estimate'])-float(r['rep_estimate'])
    except:continue
    candidates.append((abs((dt-target).days),0 if dt<=target else 1,dt,margin))
  if not candidates:raise RuntimeError(f'No historical national rows for {cyc}')
  candidates.sort(key=lambda z:(z[0],z[1])); z=candidates[0]
  nat[cyc]=z[3]; nat_meta[cyc]=(target,z[2],z[3],'historical_topline')

for cyc in (2018,2022):
  target=ELECTION[cyc]-timedelta(days=45)
  bydate={}
  for r in avg:
    try:
      if int(r.get('cycle') or 0)!=cyc:continue
      dt=date.fromisoformat((r.get('date') or '').strip())
      bydate.setdefault(dt,{})[(r.get('candidate') or '').strip()]=float(r['pct_estimate'])
    except:continue
  candidates=[]
  for dt,v in bydate.items():
    if 'Democrats' in v and 'Republicans' in v:
      candidates.append((abs((dt-target).days),0 if dt<=target else 1,dt,v['Democrats']-v['Republicans']))
  if not candidates:raise RuntimeError(f'No average national rows for {cyc}')
  candidates.sort(key=lambda z:(z[0],z[1])); z=candidates[0]
  nat[cyc]=z[3]; nat_meta[cyc]=(target,z[2],z[3],'generic_ballot_averages')

# Economic signal from exact SQINC1, same fixed coding that improved OOS.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw)); names=zf.namelist()
csvnames=[n for n in names if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not csvnames:raise RuntimeError('No exact SQINC1 file')
bname=max(csvnames,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))))
pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,col):
  try:return float((r.get(col) or '').replace(',','').strip())
  except:return None
growth={}; us={}
for r in pi:
  name=(r.get('GeoName') or '').replace('*','').strip()
  for cyc in ELECTION:
    a=val(r,f'{cyc}:Q1'); b=val(r,f'{cyc-1}:Q1')
    if a is None or b in (None,0):continue
    g=100*(a/b-1)
    if name in STATE_ABBR:growth[(cyc,STATE_ABBR[name])]=g
    elif name=='United States':us[cyc]=g

for r in rows:
  cyc=int(r['cycle']); st=r['state_abbrev']
  vals=[growth[(cyc,s)] for s in STATE_ABBR.values() if (cyc,s) in growth]
  natg=us.get(cyc,statistics.mean(vals))
  r['econ']= (growth[(cyc,st)]-natg)*PRES_SIGN[cyc]
  r['national']=nat[cyc]

BASEFEAT=['pvi','same_last','same_gap']

def design(dat,features,stats=None):
  X=np.array([[float(r[f]) for f in features] for r in dat],dtype=float)
  if stats is None:
    mu=X.mean(axis=0);sd=X.std(axis=0);sd=np.where(sd<1e-9,1.0,sd)
  else:mu,sd=stats
  return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def pred(train,test,features,penalties=None):
  X,st=design(train,features);Xt,_=design(test,features,st);y=np.array([r['y'] for r in train])
  pen=np.zeros(X.shape[1]);
  if penalties:
    for j,f in enumerate(features,start=1):pen[j]=penalties.get(f,0.0)
  A=X.T@X+np.diag(pen+1e-8);A[0,0]-=1e-8
  beta=np.linalg.pinv(A)@(X.T@y)
  return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

variants={
 'structural':(BASEFEAT,{}),
 'structural_econ':(BASEFEAT+['econ'],{}),
 'structural_national':(BASEFEAT+['national'],{}),
 'structural_econ_national':(BASEFEAT+['econ','national'],{}),
}
# Also test modest pre-specified shrinkage on national only; not tuned on test folds.
for lam in (1.0,4.0,16.0,64.0):
  variants[f'structural_econ_national_ridge{lam:g}']=(BASEFEAT+['econ','national'],{'national':lam})

summary=[]; predrows=[]
for name,(feats,pens) in variants.items():
  yy=[];pp=[]
  for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
    q=pred(tr,te,feats,pens)
    yy.extend(r['y'] for r in te);pp.extend(q.tolist())
    for r,p in zip(te,q):predrows.append({'variant':name,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y']})
  summary.append({'variant':name,'n':len(yy),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)})

for fn,data in [('national_oos_summary.csv',summary),('national_oos_predictions.csv',predrows)]:
  with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

with (OUTDIR/'national_45d_values.csv').open('w',encoding='utf-8',newline='') as f:
  fields=['cycle','election_date','target_date','source_date','national_margin_d_minus_r','source']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for cyc in sorted(nat_meta):
    target,src,margin,source=nat_meta[cyc]
    w.writerow({'cycle':cyc,'election_date':ELECTION[cyc].isoformat(),'target_date':target.isoformat(),'source_date':src.isoformat(),'national_margin_d_minus_r':margin,'source':source})

best=min(summary,key=lambda z:float(z['rmse']));basev=next(z for z in summary if z['variant']=='structural');econv=next(z for z in summary if z['variant']=='structural_econ')
lines=['# Performance experiment: National generic-ballot signal OOS','',
f'- Generated UTC: {datetime.now(timezone.utc).isoformat()}',
f'- Historical source bytes: {hbytes}',f'- 2018+ average source bytes: {abytes}',
f'- BEA member: {bname}','',
'## 45-day national values','',
'| cycle | election | target | source date | D-R generic margin | source |','|---:|---|---|---|---:|---|']
for cyc in sorted(nat_meta):
  target,src,margin,source=nat_meta[cyc];lines.append(f'| {cyc} | {ELECTION[cyc]} | {target} | {src} | {margin:.4f} | {source} |')
lines += ['','## Combined 99-row modern OOS','',
'| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|']
for z in summary:lines.append(f"| {z['variant']} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += ['','## Decision','',
f'- Structural baseline RMSE: {float(basev["rmse"]):.4f}.',
f'- Structural + fixed economic signal RMSE: {float(econv["rmse"]):.4f}.',
f'- Best tested National architecture: {best["variant"]} with RMSE {float(best["rmse"]):.4f}.',
f'- Improvement vs structural: {float(basev["rmse"])-float(best["rmse"]):+.4f}.',
f'- Improvement vs structural+econ: {float(econv["rmse"])-float(best["rmse"]):+.4f}.',
'- This is still a reconstruction diagnostic, not the preserved 7.99 headline Core V2, because candidate and PersonalVote architecture are not yet fully restored.','',
'## Outputs','',
'- performance/results/national_oos_summary.csv',
'- performance/results/national_oos_predictions.csv',
'- performance/results/national_45d_values.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))