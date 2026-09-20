#!/usr/bin/env python3
import csv, io, zipfile, re, statistics, itertools
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
OUTDIR=ROOT/'experiments/history_extension/direction_results'
DOC=ROOT/'docs/history/updates/2026-09-21_0235_direction-first-extended-history-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

HIST_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_topline_historical.csv'
AVG_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_ballot_averages.csv'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'

ELECTION={
 2004:date(2004,11,2),2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),
 2012:date(2012,11,6),2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),
 2020:date(2020,11,3),2022:date(2022,11,8)
}
PRES_SIGN={2004:-1,2006:-1,2008:-1,2010:1,2012:1,2014:1,2016:1,2018:-1,2020:-1,2022:1}
OUTER=[2014,2018,2022]
STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def truth(v):return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower();s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def fetch_csv(url):
    raw=urlopen(Request(url,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace')))),len(raw)

sen=load(SEN);pres=load(PRES);head=load(HEAD);headss=load(HEADSS);align=load(ALIGN)
head_by={r['race_id']:r for r in head}; ss_by={r['race_id']:r for r in headss}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

# Rebuild PVI directly from presidential state leans, avoiding any midterm-only prebuilt PVI table.
lean={}
years=set()
for r in pres:
    try:y=int(r['cycle']);st=r['state_abbrev'];v=float(r['lean_vs_national_pctpt'])
    except:continue
    lean[(y,st)]=v;years.add(y)
years=sorted(years)
def pvi_for(cycle,st):
    ys=[y for y in years if y<cycle and (y,st) in lean]
    if len(ys)<2:return None
    return .67*lean[(ys[-1],st)]+.33*lean[(ys[-2],st)]

by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general':by[r['race_id']].append(r)

def candidates(rr):
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
    cs=candidates(use)
    ov=align_by.get((cyc,st,seat))
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}:return None
    d=r=None
    if ov and ov['action']=='ALIGN':
        ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])]
        rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
        d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None
    if d is None and r is None:
        ds=[c for c in cs if 'DEM' in c['parties']];rs=[c for c in cs if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None;r=rs[0] if len(rs)==1 else None
    if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0:return None
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,
            'y':(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0}

# Include 1998 onward in seat history; model years are 2004 onward.
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
for r in sorted(allr,key=lambda z:(z['state_abbrev'],z['seat'],z['cycle'])):
    seat_hist[(r['state_abbrev'],r['seat'])].append(r)

# 45-day generic ballot.
hist,hbytes=fetch_csv(HIST_URL);avg,abytes=fetch_csv(AVG_URL)
def pdate(s):
    m,d,y=[int(x) for x in s.split('/')];return date(y,m,d)
national={};nmeta={}
for cyc in (2004,2006,2008,2010,2012,2014,2016):
    target=ELECTION[cyc]-timedelta(days=45);cand=[]
    for r in hist:
        if (r.get('subgroup') or '').strip()!='All polls':continue
        try:dt=pdate((r.get('modeldate') or '').strip())
        except:continue
        if dt>target:continue
        try:m=float(r['dem_estimate'])-float(r['rep_estimate'])
        except:continue
        cand.append((target-dt,dt,m))
    if cand:
        cand.sort(key=lambda z:z[0]);lag,dtv,m=cand[0];national[cyc]=m;nmeta[cyc]=(target,dtv,m,'historical_topline')
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
    for dtv,v in bd.items():
        if 'Democrats' in v and 'Republicans' in v:cand.append((target-dtv,dtv,v['Democrats']-v['Republicans']))
    if cand:
        cand.sort(key=lambda z:z[0]);lag,dtv,m=cand[0];national[cyc]=m;nmeta[cyc]=(target,dtv,m,'generic_ballot_averages')

# BEA signed relative-U.S. Q1 YoY personal-income growth.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
zf=zipfile.ZipFile(io.BytesIO(raw))
members=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not members:raise RuntimeError('No SQINC1 all-areas CSV')
bname=max(members,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))))
pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
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

rows=[];skip=defaultdict(int)
for r in allr:
    cyc=r['cycle']
    if cyc not in ELECTION:continue
    if cyc in OUTER and r['race_id'] not in head_by:continue
    pv=pvi_for(cyc,r['state_abbrev'])
    if pv is None:skip['pvi']+=1;continue
    if cyc not in national:skip['national']+=1;continue
    if cyc in OUTER:
        s=ss_by[r['race_id']]
        if not s['same_seat_last_prior_margin_two_party_pctpt'] or not s['same_seat_last_prior_year_gap']:skip['same']+=1;continue
        same=float(s['same_seat_last_prior_margin_two_party_pctpt']);gap=float(s['same_seat_last_prior_year_gap'])
    else:
        prev=[x for x in seat_hist[(r['state_abbrev'],r['seat'])] if x['cycle']<cyc]
        if not prev:skip['same']+=1;continue
        q=max(prev,key=lambda z:z['cycle']);same=float(q['y']);gap=float(cyc-q['cycle'])
    vals=[growth[(cyc,st)] for st in STATE_ABBR.values() if (cyc,st) in growth]
    if (cyc,r['state_abbrev']) not in growth or len(vals)<48:skip['econ']+=1;continue
    natg=us.get(cyc,statistics.mean(vals))
    econ=(growth[(cyc,r['state_abbrev'])]-natg)*PRES_SIGN[cyc]
    rows.append({'race_id':r['race_id'],'cycle':cyc,'state_abbrev':r['state_abbrev'],'y':r['y'],
                 'pvi':pv,'same_last':same,'same_gap':gap,'econ':econ,'national':national[cyc]})

FEATURES=['pvi','same_last','same_gap','econ','national']
LP=[0.0,1.0,4.0,16.0]
LL=[0.0,1.0,4.0,16.0,64.0,256.0]
LE=[0.0,1.0,4.0,16.0,64.0,256.0,1024.0]
LN=[0.0,1.0,4.0,16.0,64.0,256.0,1024.0,4096.0]

def design(dat,stats=None):
    X=np.array([[float(r[f]) for f in FEATURES] for r in dat],dtype=float)
    if stats is None:
        mu=X.mean(axis=0);sd=X.std(axis=0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)
def fitpred(tr,te,lp,ll,le,ln):
    X,st=design(tr);Xt,_=design(te,st);y=np.array([r['y'] for r in tr])
    pen=np.array([0.0,lp,ll,ll,le,ln])
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train));grid=[]
    for lp,ll,le,ln in itertools.product(LP,LL,LE,LN):
        yy=[];pp=[];folds=0
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc];va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<25 or not va:continue
            q=fitpred(tr,va,lp,ll,le,ln);yy.extend(r['y'] for r in va);pp.extend(q.tolist());folds+=1
        if folds:
            correct=sum((a>0)==(b>0) for a,b in zip(yy,pp))
            accuracy=100.0*correct/len(yy)
            grid.append((-correct,mae(yy,pp),rmse(yy,pp),lp,ll,le,ln,folds,accuracy,len(yy)))
    if not grid:raise RuntimeError('No valid inner folds')
    grid.sort(key=lambda z:(z[0],z[1],z[2],z[3]+z[4]+z[5]+z[6]))
    return grid[0],grid[:20]

# Prequential fundamentals priors for poll-layer tuning.
# Every cycle is predicted using only earlier cycles; no target-cycle outcome enters its hyperparameter selection.
preq=[]; preq_choices=[]
for tc in [2010,2012,2014,2016,2018,2020,2022]:
    tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
    if not tr or not te: continue
    try:
        best,trace=tune(tr)
    except RuntimeError:
        continue
    negcorrect,inner_mae,inner_rmse,lp,ll,le,ln,folds,inner_acc,inner_n=best
    q=fitpred(tr,te,lp,ll,le,ln)
    preq_choices.append({'test_cycle':tc,'lambda_pvi':lp,'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,
                         'inner_correct':-negcorrect,'inner_n':inner_n,'inner_direction_pct':inner_acc,
                         'inner_mae':inner_mae,'inner_rmse':inner_rmse,'inner_folds':folds,'train_n':len(tr),'test_n':len(te)})
    for r,p in zip(te,q):
        preq.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                     'actual':r['y'],'predicted':float(p),'error':float(p)-r['y']})

for fn,data in [('prequential_priors.csv',preq),('prequential_prior_choices.csv',preq_choices)]:
    if data:
        with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in rows if int(r['cycle'])<tc];te=[r for r in rows if int(r['cycle'])==tc]
    best,trace=tune(tr)
    negcorrect,inner_mae,inner_rmse,lp,ll,le,ln,folds,inner_acc,inner_n=best
    q=fitpred(tr,te,lp,ll,le,ln)
    choices.append({'test_cycle':tc,'lambda_pvi':lp,'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,
                    'inner_correct':-negcorrect,'inner_n':inner_n,'inner_direction_pct':inner_acc,
                    'inner_mae':inner_mae,'inner_rmse':inner_rmse,'inner_folds':folds,'train_n':len(tr),'test_n':len(te),
                    'top20':' | '.join(f'correct={-z[0]}/{z[9]} acc={z[8]:.1f}% MAE={z[1]:.3f} RMSE={z[2]:.3f} P{z[3]} L{z[4]} E{z[5]} N{z[6]}' for z in trace)})
    for r,p in zip(te,q):pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                                      'actual':r['y'],'predicted':float(p),'error':float(p)-r['y']})

yy=[r['actual'] for r in pred];pp=[r['predicted'] for r in pred]
summary=[{'variant':'extended_history_direction_first_nested','n':len(pred),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp),
          'model_rows':len(rows),'earliest_cycle':min(r['cycle'] for r in rows)}]

for fn,data in [('direction_first_summary.csv',summary),('direction_first_choices.csv',choices),('direction_first_predictions.csv',pred)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

cycle_counts={c:sum(int(r['cycle'])==c for r in rows) for c in sorted(set(int(r['cycle']) for r in rows))}
lines=['# Performance experiment: extended-history National + economic nested OOS','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       f'- Model rows: {len(rows)}',
       f'- Earliest modeled cycle: {min(cycle_counts)}',
       '- PVI is rebuilt directly from the two most recent completed presidential-election state leans before each Senate cycle.',
       '- SameSeat uses the most recent prior same-seat result plus year gap.',
       '- National uses 45-day Generic Ballot D-R.',
       '- Economic signal uses president-party-signed state Q1 YoY personal-income growth relative to U.S.','',
       '## Cycle coverage','']
for c,n in cycle_counts.items():lines.append(f'- {c}: {n} races')
lines += ['','## OOS result','',
          '| N | RMSE | MAE | direction |','|---:|---:|---:|---:|',
          f"| {len(pred)} | {summary[0]['rmse']:.4f} | {summary[0]['mae']:.4f} | {summary[0]['direction_pct']:.1f}% |",'',
          '## Nested choices','',
          '| test | train N | inner folds | inner correct | inner direction | inner MAE | inner RMSE | PVI ridge | local ridge | econ ridge | National ridge |',
          '|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['train_n']} | {r['inner_folds']} | {r['inner_correct']}/{r['inner_n']} | {r['inner_direction_pct']:.1f}% | {r['inner_mae']:.4f} | {r['inner_rmse']:.4f} | {r['lambda_pvi']} | {r['lambda_local']} | {r['lambda_econ']} | {r['lambda_national']} |")
lines += ['','## Benchmarks','',
          '- Previous leakage-safe midterm-only National nested RMSE: 9.1890.',
          '- Previous full-cycle attempt RMSE: 9.0712, but its 2014 inner tuning had no valid fold.',
          '- Best descriptive fixed-grid diagnostic: 8.9084.',
          '- Preserved original Core V2 fundamentals benchmark: 7.99.','',
          '## Objective correction','',
          'PRIMARY: maximize strictly chronological inner-OOS winner/direction correctness. Ties are broken by lower MAE, then lower RMSE.','',
          'The outer 99-race result is judged first by correct winner count / direction percentage, not by RMSE.','',
          '## Decision rule','',
          'Keep this architecture only if its strictly chronological outer OOS direction correctness exceeds the preserved benchmark; use MAE/RMSE only as tie-breakers.','',
          '## Data limitation','',
          'The BEA economic series is still the current revised SQINC1 history rather than release-vintage snapshots, so this remains a performance experiment, not final vintage-clean replication.','',
          '## Outputs','',
          '- experiments/history_extension/direction_results/direction_first_summary.csv',
          '- experiments/history_extension/direction_results/direction_first_choices.csv',
          '- experiments/history_extension/direction_results/direction_first_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
