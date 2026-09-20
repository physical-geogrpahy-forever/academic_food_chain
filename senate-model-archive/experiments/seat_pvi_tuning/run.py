#!/usr/bin/env python3
import csv, io, zipfile, re, statistics, itertools, math
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
PRES=ROOT/'data/processed/presidential_state_lean.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
HEADSS=ROOT/'data/processed/core_v2r_headline_same_seat_features.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
OUTDIR=ROOT/'experiments/seat_pvi_tuning/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0240_pvi-sameseat-residualized-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

HIST_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_topline_historical.csv'
AVG_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_ballot_averages.csv'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
ELECTION={2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)}
PRES_SIGN={2006:-1,2008:-1,2010:1,2012:1,2014:1,2016:1,2018:-1,2020:-1,2022:1}
OUTER=[2014,2018,2022]
PVI_W=[0.50,0.67,0.80,1.00]
SEAT_MODES=['raw','resid','resid_decay','resid_ewm2']
LP=[0.0,1.0,4.0,16.0]
LL=[1.0,4.0,16.0,64.0,256.0,1024.0]
LE=[64.0,256.0,1024.0,4096.0]
LN=[0.0,1.0,4.0,16.0,64.0,256.0]
STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def truth(v):return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower();s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def fetch_csv(url):
    raw=urlopen(Request(url,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))

sen=load(SEN);pres=load(PRES);head=load(HEAD);headss=load(HEADSS);align=load(ALIGN)
head_by={r['race_id']:r for r in head};ss_by={r['race_id']:r for r in headss}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

lean={};pyears=set()
for r in pres:
    try:y=int(r['cycle']);st=r['state_abbrev'];v=float(r['lean_vs_national_pctpt'])
    except:continue
    lean[(y,st)]=v;pyears.add(y)
pyears=sorted(pyears)

def pvi_info(cycle,st,w):
    ys=[y for y in pyears if y<cycle and (y,st) in lean]
    if len(ys)<2:return None
    return w*lean[(ys[-1],st)]+(1-w)*lean[(ys[-2],st)]

def prior_partisan_baseline(cycle,st,w):
    ys=[y for y in pyears if y<cycle and (y,st) in lean]
    if len(ys)>=2:return w*lean[(ys[-1],st)]+(1-w)*lean[(ys[-2],st)]
    if len(ys)==1:return lean[(ys[-1],st)]
    return None

by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general':by[r['race_id']].append(r)

def cgroups(rr):
    out={}
    for r in rr:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key:continue
        c=out.setdefault(key,{'name':r.get('candidate_name') or '','votes':0,'parties':set(),'missing':False})
        for q in [(r.get('ballot_party') or ''),(r.get('party') or '')]:
            if q.strip():c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v:c['missing']=True
        else:
            try:c['votes']+=int(float(v))
            except:c['missing']=True
    return list(out.values())

def extract(rr):
    first=rr[0];cyc=int(first['cycle']);st=first['state_abbrev'];seat=first['office_seat_name']
    nums=[]
    for x in rr:
        v=(x.get('ranked_choice_round') or '').strip()
        if v:
            try:nums.append(int(float(v)))
            except:pass
    use=rr
    if nums:
        mx=max(nums);use=[]
        for x in rr:
            v=(x.get('ranked_choice_round') or '').strip()
            try:rv=int(float(v)) if v else None
            except:rv=None
            if rv==mx:use.append(x)
    cs=cgroups(use);ov=align_by.get((cyc,st,seat))
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}:return None
    d=r=None
    if ov and ov['action']=='ALIGN':
        ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])];rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
        d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None
    if d is None and r is None:
        ds=[c for c in cs if 'DEM' in c['parties']];rs=[c for c in cs if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None
    if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0:return None
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,'y':(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0}

allr=[]
for rid,rr in by.items():
    try:
        x=extract(rr)
        if x:allr.append(x)
    except:pass
rb={r['race_id']:r for r in allr}
for rid,h in head_by.items():
    if rid in rb:rb[rid]['y']=float(h['margin_d_minus_r_two_party_pctpt'])
seat_hist=defaultdict(list)
for r in sorted(allr,key=lambda z:(z['state_abbrev'],z['seat'],z['cycle'])):seat_hist[(r['state_abbrev'],r['seat'])].append(r)

hist=fetch_csv(HIST_URL);avg=fetch_csv(AVG_URL)
def pdate(s):
    m,d,y=[int(x) for x in s.split('/')];return date(y,m,d)
national={}
for cyc in (2006,2008,2010,2012,2014,2016):
    target=ELECTION[cyc]-timedelta(days=45);cand=[]
    for r in hist:
        if (r.get('subgroup') or '').strip()!='All polls':continue
        try:dt=pdate((r.get('modeldate') or '').strip());m=float(r['dem_estimate'])-float(r['rep_estimate'])
        except:continue
        if dt<=target:cand.append((target-dt,m))
    if cand:cand.sort(key=lambda z:z[0]);national[cyc]=cand[0][1]
for cyc in (2018,2020,2022):
    target=ELECTION[cyc]-timedelta(days=45);bd={}
    for r in avg:
        try:
            if int(r.get('cycle') or 0)!=cyc:continue
            dt=date.fromisoformat((r.get('date') or '').strip())
            if dt>target:continue
            bd.setdefault(dt,{})[(r.get('candidate') or '').strip()]=float(r['pct_estimate'])
        except:continue
    cand=[]
    for dt,v in bd.items():
        if 'Democrats' in v and 'Republicans' in v:cand.append((target-dt,v['Democrats']-v['Republicans']))
    if cand:cand.sort(key=lambda z:z[0]);national[cyc]=cand[0][1]

raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw));members=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
bname=max(members,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))));pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,col):
    try:return float((r.get(col) or '').replace(',','').strip())
    except:return None
growth={};us={}
for r in pi:
    name=(r.get('GeoName') or '').replace('*','').strip()
    for cyc in ELECTION:
        a=val(r,f'{cyc}:Q1');b=val(r,f'{cyc-1}:Q1')
        if a is None or b in (None,0):continue
        g=100*(a/b-1)
        if name in STATE_ABBR:growth[(cyc,STATE_ABBR[name])]=g
        elif name=='United States':us[cyc]=g

base_rows=[]
for r in allr:
    cyc=r['cycle'];st=r['state_abbrev']
    if cyc not in ELECTION or cyc not in national:continue
    if cyc in OUTER and r['race_id'] not in head_by:continue
    # Require two completed presidential elections so every PVI weight uses identical rows.
    if pvi_info(cyc,st,.67) is None:continue
    if cyc in OUTER:
        s=ss_by[r['race_id']]
        if not s['same_seat_last_prior_margin_two_party_pctpt'] or not s['same_seat_last_prior_year_gap']:continue
        prev=[x for x in seat_hist[(st,r['seat'])] if x['cycle']<cyc]
    else:
        prev=[x for x in seat_hist[(st,r['seat'])] if x['cycle']<cyc]
        if not prev:continue
    prev=sorted(prev,key=lambda z:z['cycle'],reverse=True)
    if not prev:continue
    vals=[growth[(cyc,s)] for s in STATE_ABBR.values() if (cyc,s) in growth]
    if (cyc,st) not in growth or len(vals)<48:continue
    natg=us.get(cyc,statistics.mean(vals))
    base_rows.append({'race_id':r['race_id'],'cycle':cyc,'state_abbrev':st,'seat':r['seat'],'y':r['y'],
                      'prev':prev[:2],'econ':(growth[(cyc,st)]-natg)*PRES_SIGN[cyc],'national':national[cyc]})

def features(row,w,mode):
    cyc=row['cycle'];st=row['state_abbrev'];pv=pvi_info(cyc,st,w)
    prev=row['prev'];q=prev[0];gap=float(cyc-q['cycle'])
    pp=prior_partisan_baseline(q['cycle'],st,w)
    miss=1.0 if pp is None else 0.0
    resid=0.0 if pp is None else q['y']-pp
    if mode=='raw':seat=q['y']
    elif mode=='resid':seat=resid
    elif mode=='resid_decay':seat=resid*math.exp(-max(gap-6.0,0.0)/6.0)
    else:
        nums=[];weights=[]
        for z in prev:
            zp=prior_partisan_baseline(z['cycle'],st,w)
            if zp is None:continue
            zg=float(cyc-z['cycle']);wt=math.exp(-max(zg-6.0,0.0)/6.0)
            nums.append((z['y']-zp)*wt);weights.append(wt)
        seat=sum(nums)/sum(weights) if weights else 0.0
        miss=0.0 if weights else 1.0
    return [pv,seat,gap,miss,row['econ'],row['national']]

def design(dat,w,mode,stats=None):
    X=np.array([features(r,w,mode) for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0);sd=X.std(axis=0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(tr,te,w,mode,lp,ll,le,ln):
    X,st=design(tr,w,mode);Xt,_=design(te,w,mode,st);y=np.array([r['y'] for r in tr])
    # intercept, PVI, seat, gap, seat-missing, econ, national
    pen=np.array([0.0,lp,ll,ll,ll,le,ln])
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train));grid=[]
    for w,mode,lp,ll,le,ln in itertools.product(PVI_W,SEAT_MODES,LP,LL,LE,LN):
        yy=[];pp=[];folds=0
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc];va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<25 or not va:continue
            q=fitpred(tr,va,w,mode,lp,ll,le,ln)
            yy.extend(r['y'] for r in va);pp.extend(q.tolist());folds+=1
        if folds:grid.append((rmse(yy,pp),w,mode,lp,ll,le,ln,folds))
    grid.sort(key=lambda z:(z[0],z[3]+z[4]+z[5]+z[6]))
    return grid[0],grid[:20]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in base_rows if int(r['cycle'])<tc];te=[r for r in base_rows if int(r['cycle'])==tc]
    best,trace=tune(tr);sc,w,mode,lp,ll,le,ln,folds=best
    q=fitpred(tr,te,w,mode,lp,ll,le,ln)
    choices.append({'test_cycle':tc,'pvi_recent_weight':w,'seat_mode':mode,'lambda_pvi':lp,'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,'inner_rmse':sc,'inner_folds':folds,'train_n':len(tr),'test_n':len(te),
                    'top20':' | '.join(f'w{z[1]} {z[2]} P{z[3]} L{z[4]} E{z[5]} N{z[6]}:{z[0]:.3f}' for z in trace)})
    for r,p in zip(te,q):pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],'pvi_recent_weight':w,'seat_mode':mode})

yy=[r['actual'] for r in pred];pp=[r['predicted'] for r in pred]
summary=[{'variant':'nested_pvi_sameseat_tuning','n':len(pred),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp),'model_rows':len(base_rows)}]
for fn,data in [('seat_pvi_summary.csv',summary),('seat_pvi_choices.csv',choices),('seat_pvi_predictions.csv',pred)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

lines=['# Performance experiment: nested PVI weighting + residualized SameSeat','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       f'- Model rows: {len(base_rows)}',
       '- Outer validation: preserved 99 races in 2014, 2018, 2022.',
       '- PVI recent-election weight candidates: 0.50, 0.67, 0.80, 1.00.',
       '- SameSeat modes: raw margin, prior-PVI residual, age-decayed residual, two-observation exponentially weighted residual.',
       '- All architecture choices and ridge strengths are selected inside chronological inner OOS only.','',
       '## Result','',
       '| N | RMSE | MAE | direction |','|---:|---:|---:|---:|',
       f"| {len(pred)} | {summary[0]['rmse']:.4f} | {summary[0]['mae']:.4f} | {summary[0]['direction_pct']:.1f}% |",'',
       '## Outer-fold choices','',
       '| test | PVI recent weight | SameSeat mode | PVI ridge | local ridge | econ ridge | National ridge | inner RMSE |',
       '|---:|---:|---|---:|---:|---:|---:|---:|']
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['pvi_recent_weight']} | {r['seat_mode']} | {r['lambda_pvi']} | {r['lambda_local']} | {r['lambda_econ']} | {r['lambda_national']} | {r['inner_rmse']:.4f} |")
lines += ['','## Benchmarks','',
          '- Current best strict nested OOS: 8.8189 RMSE.',
          '- Best descriptive fixed-grid diagnostic: 8.9084 RMSE.',
          '- Preserved original Core V2 fundamentals: 7.99 RMSE.','',
          '## Decision','',
          'Keep the selected PVI/SameSeat architecture only if RMSE is below 8.8189. Otherwise retain the extended-history baseline unchanged.','',
          '## Outputs','',
          '- experiments/seat_pvi_tuning/results/seat_pvi_summary.csv',
          '- experiments/seat_pvi_tuning/results/seat_pvi_choices.csv',
          '- experiments/seat_pvi_tuning/results/seat_pvi_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
