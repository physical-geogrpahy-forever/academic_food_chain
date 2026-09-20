#!/usr/bin/env python3
import csv, io, zipfile, re, statistics, itertools
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
PVI=ROOT/'data/processed/historical_senate_pvi_default_067_033.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0220_full-cycle-national-econ-ridge-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

HIST_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_topline_historical.csv'
AVG_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_ballot_averages.csv'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'

ELECTION={
 2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),
 2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)
}
PRES_SIGN={2006:-1,2008:-1,2010:1,2012:1,2014:1,2016:1,2018:-1,2020:-1,2022:1}
OUTER=[2014,2018,2022]

STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def truth(v): return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower()
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def fetch_csv(url):
    raw=urlopen(Request(url,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace')))),len(raw)

sen=load(SEN); pvirows=load(PVI); head=load(HEAD); ss=load(HEADSS); align=load(ALIGN)
pvi={r['race_id']:float(r['pvi_default_067_033_pctpt']) for r in pvirows}
head_by={r['race_id']:r for r in head}; ss_by={r['race_id']:r for r in ss}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general':
        by[r['race_id']].append(r)

def group_candidates(rr):
    out={}
    for r in rr:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key: continue
        c=out.setdefault(key,{'name':r.get('candidate_name') or '','votes':0,'parties':set(),'missing':False})
        for q in [(r.get('ballot_party') or ''),(r.get('party') or '')]:
            if q.strip(): c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v: c['missing']=True
        else:
            try: c['votes']+=int(float(v))
            except: c['missing']=True
    return list(out.values())

def extract(rr):
    first=rr[0]; cyc=int(first['cycle']); st=first['state_abbrev']; seat=first['office_seat_name']
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
    cs=group_candidates(use)
    ov=align_by.get((cyc,st,seat))
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}: return None
    d=r=None
    if ov and ov['action']=='ALIGN':
        ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])]
        rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
        d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None
    if d is None and r is None:
        ds=[c for c in cs if 'DEM' in c['parties']]
        rs=[c for c in cs if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None
    if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0: return None
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,
            'y':(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0}

races=[]
for rid,rr in by.items():
    try:
        x=extract(rr)
        if x and x['cycle'] in ELECTION: races.append(x)
    except: pass

# Preserve exact 99 headline margins.
rb={r['race_id']:r for r in races}
for rid,h in head_by.items():
    if rid in rb: rb[rid]['y']=float(h['margin_d_minus_r_two_party_pctpt'])

# Same-seat last prior.
seat_hist=defaultdict(list)
for r in sorted(races,key=lambda z:(z['state_abbrev'],z['seat'],z['cycle'])):
    seat_hist[(r['state_abbrev'],r['seat'])].append(r)

# Generic ballot values for all cycles.
hist,hbytes=fetch_csv(HIST_URL); avg,abytes=fetch_csv(AVG_URL)
def pdate(s):
    m,d,y=[int(x) for x in s.split('/')]; return date(y,m,d)
national={}
nmeta={}
for cyc in (2006,2008,2010,2012,2014,2016):
    target=ELECTION[cyc]-timedelta(days=45)
    cand=[]
    for r in hist:
        if (r.get('subgroup') or '').strip()!='All polls': continue
        try: dt=pdate((r.get('modeldate') or '').strip())
        except: continue
        if dt>target: continue
        try: margin=float(r['dem_estimate'])-float(r['rep_estimate'])
        except: continue
        cand.append((target-dt,dt,margin))
    if not cand: raise RuntimeError(f'No historical generic ballot for {cyc}')
    cand.sort(key=lambda z:z[0]); lag,dtv,margin=cand[0]
    national[cyc]=margin; nmeta[cyc]=(target,dtv,margin,'historical_topline')
for cyc in (2018,2020,2022):
    target=ELECTION[cyc]-timedelta(days=45)
    bydate={}
    for r in avg:
        try:
            if int(r.get('cycle') or 0)!=cyc: continue
            dt=date.fromisoformat((r.get('date') or '').strip())
            if dt>target: continue
            bydate.setdefault(dt,{})[(r.get('candidate') or '').strip()]=float(r['pct_estimate'])
        except: continue
    cand=[]
    for dtv,v in bydate.items():
        if 'Democrats' in v and 'Republicans' in v:
            cand.append((target-dtv,dtv,v['Democrats']-v['Republicans']))
    if not cand: raise RuntimeError(f'No modern generic ballot for {cyc}')
    cand.sort(key=lambda z:z[0]); lag,dtv,margin=cand[0]
    national[cyc]=margin; nmeta[cyc]=(target,dtv,margin,'generic_ballot_averages')

# Economic Q1 YoY signal.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw))
csvnames=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not csvnames: raise RuntimeError('No SQINC1 all-areas CSV')
bname=max(csvnames,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))))
pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,col):
    try: return float((r.get(col) or '').replace(',','').strip())
    except: return None
growth={}; us={}
for r in pi:
    name=(r.get('GeoName') or '').replace('*','').strip()
    for cyc in ELECTION:
        a=val(r,f'{cyc}:Q1'); b=val(r,f'{cyc-1}:Q1')
        if a is None or b in (None,0): continue
        g=100*(a/b-1)
        if name in STATE_ABBR: growth[(cyc,STATE_ABBR[name])]=g
        elif name=='United States': us[cyc]=g

rows=[]
for r in races:
    cyc=r['cycle']
    if cyc not in ELECTION: continue
    if cyc in OUTER and r['race_id'] not in head_by: continue
    pv=pvi.get(r['race_id'])
    if pv is None: continue
    if cyc in OUTER:
        s=ss_by[r['race_id']]
        same=float(s['same_seat_last_prior_margin_two_party_pctpt']); gap=float(s['same_seat_last_prior_year_gap'])
    else:
        prev=[x for x in seat_hist[(r['state_abbrev'],r['seat'])] if x['cycle']<cyc]
        if not prev: continue
        q=max(prev,key=lambda z:z['cycle']); same=float(q['y']); gap=float(cyc-q['cycle'])
    vals=[growth[(cyc,st)] for st in STATE_ABBR.values() if (cyc,st) in growth]
    if (cyc,r['state_abbrev']) not in growth or len(vals)<48: continue
    natg=us.get(cyc,statistics.mean(vals))
    econ=(growth[(cyc,r['state_abbrev'])]-natg)*PRES_SIGN[cyc]
    rows.append({'race_id':r['race_id'],'cycle':cyc,'state_abbrev':r['state_abbrev'],'y':r['y'],
                 'pvi':pv,'same_last':same,'same_gap':gap,'econ':econ,'national':national[cyc]})

FEATURES=['pvi','same_last','same_gap','econ','national']
GROUP={'pvi':'pvi','same_last':'local','same_gap':'local','econ':'econ','national':'national'}
L_LOCAL=[0.0,1.0,4.0,16.0,64.0]
L_ECON=[0.0,1.0,4.0,16.0,64.0,256.0]
L_NAT=[0.0,1.0,4.0,16.0,64.0,256.0,1024.0]

def design(dat,stats=None):
    X=np.array([[float(r[f]) for f in FEATURES] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(train,test,ll,le,ln):
    X,st=design(train); Xt,_=design(test,st); y=np.array([r['y'] for r in train])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(FEATURES,start=1):
        if GROUP[f]=='local': pen[j]=ll
        elif GROUP[f]=='econ': pen[j]=le
        elif GROUP[f]=='national': pen[j]=ln
        else: pen[j]=1e-8
    A=X.T@X+np.diag(pen); beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train))
    cand=[]
    for ll,le,ln in itertools.product(L_LOCAL,L_ECON,L_NAT):
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<25 or not va: continue
            q=fitpred(tr,va,ll,le,ln)
            yy.extend(r['y'] for r in va); pp.extend(q.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,ll,le,ln))
    cand.sort(key=lambda z:z[0])
    return cand[0],cand[:20]

preds=[]; choices=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc]
    te=[r for r in rows if int(r['cycle'])==tc]
    best,trace=tune(tr); sc,ll,le,ln=best
    q=fitpred(tr,te,ll,le,ln)
    choices.append({'test_cycle':tc,'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,'inner_rmse':sc,
                    'top20':' | '.join(f'L{z[1]} E{z[2]} N{z[3]}:{z[0]:.3f}' for z in trace)})
    for r,p in zip(te,q):
        preds.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                      'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],
                      'lambda_local':ll,'lambda_econ':le,'lambda_national':ln})

yy=[float(r['actual']) for r in preds]; pp=[float(r['predicted']) for r in preds]
summary=[{'variant':'fullcycle_nested_group_ridge','n':len(preds),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)}]

# Fixed comparison using the prior midterm-only winning architecture.
fixed=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc]; te=[r for r in rows if int(r['cycle'])==tc]
    q=fitpred(tr,te,0.0,0.0,64.0)
    fixed += [(r['y'],float(p)) for r,p in zip(te,q)]
fy=[x[0] for x in fixed]; fp=[x[1] for x in fixed]
summary.append({'variant':'fullcycle_fixed_N64','n':len(fixed),'rmse':rmse(fy,fp),'mae':mae(fy,fp),'direction_pct':acc(fy,fp)})

for fn,data in [('fullcycle_national_econ_summary.csv',summary),('fullcycle_national_econ_choices.csv',choices),('fullcycle_national_econ_predictions.csv',preds)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)

lines=[
 '# Performance experiment: full-cycle National + economic group-ridge OOS','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Total modeling rows: {len(rows)}',
 '- Training uses all available Senate cycles from 2006 through 2022, including presidential-election years.',
 '- Outer headline validation remains exactly the preserved 99 races in 2014, 2018, 2022.','',
 '## Results','',
 '| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|'
]
for r in summary:
    lines.append(f"| {r['variant']} | {r['n']} | {float(r['rmse']):.4f} | {float(r['mae']):.4f} | {float(r['direction_pct']):.1f}% |")
lines += ['','## Nested choices','',
 '| test cycle | lambda local | lambda econ | lambda national | inner RMSE |','|---:|---:|---:|---:|---:|']
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['lambda_local']} | {r['lambda_econ']} | {r['lambda_national']} | {float(r['inner_rmse']):.4f} |")
lines += ['','## Comparison target','',
 '- Previous best 99-row reconstruction diagnostic: RMSE 8.9084 from midterm-only structural + economic + national with national ridge 64.',
 '- This experiment is retained only if the full-cycle chronological training lowers that OOS RMSE.','',
 '## Leakage guard','',
 '- 45-day generic-ballot values use only dates on or before the snapshot.',
 '- Headline outcomes are never used in hyperparameter selection for their own outer fold.',
 '- Economic values are still current revised SQINC1 Q1 values, so this remains a signal/performance experiment rather than final vintage-clean Core V2 reproduction.','',
 '## Outputs','',
 '- performance/results/fullcycle_national_econ_summary.csv',
 '- performance/results/fullcycle_national_econ_choices.csv',
 '- performance/results/fullcycle_national_econ_predictions.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
