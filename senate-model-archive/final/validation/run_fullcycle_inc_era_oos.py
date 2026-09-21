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
HEADCAND=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0226_fullcycle-incumbency-era-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

HIST_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_topline_historical.csv'
AVG_URL='https://raw.githubusercontent.com/kitsbits/aiml/bc92061a0d638afac14aac3e6bd1166539985fe9/python-fundamentals/congress-generic-ballot/generic_ballot_averages.csv'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
ELECTION={2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)}
PRES_SIGN={2006:-1,2008:-1,2010:1,2012:1,2014:1,2016:1,2018:-1,2020:-1,2022:1}
LAG_SOURCE={2000,2002,2004}
OUTER=[2014,2018,2022]

STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def truth(v): return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower()
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def fetch_csv(url):
    raw=urlopen(Request(url,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read()
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace')))),len(raw)

sen=load(SEN); pvirows=load(PVI); head=load(HEAD); ss=load(HEADSS); headcand=load(HEADCAND); align=load(ALIGN)
pvi={r['race_id']:float(r['pvi_default_067_033_pctpt']) for r in pvirows}
head_by={r['race_id']:r for r in head}; ss_by={r['race_id']:r for r in ss}; hc_by={r['race_id']:r for r in headcand}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general': by[r['race_id']].append(r)

def groups(rr):
    out={}
    for r in rr:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key: continue
        c=out.setdefault(key,{'pid':pid,'name':r.get('candidate_name') or '','votes':0,'parties':set(),'winner':False,'missing':False})
        for q in [(r.get('ballot_party') or ''),(r.get('party') or '')]:
            if q.strip():c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v:c['missing']=True
        else:
            try:c['votes']+=int(float(v))
            except:c['missing']=True
        c['winner']=c['winner'] or truth(r.get('winner','false'))
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
    cs=groups(use)
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
    winner_pid=''
    for c in cs:
        if c['winner'] and c['pid']: winner_pid=c['pid'];break
    if not winner_pid:
        winner_pid=d['pid'] if d['votes']>r['votes'] else r['pid']
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,'y':(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0,'d_pid':d['pid'],'r_pid':r['pid'],'winner_pid':winner_pid}

races=[]
allowed=set(ELECTION)|LAG_SOURCE
for rid,rr in by.items():
    try:
        x=extract(rr)
        if x and x['cycle'] in allowed:races.append(x)
    except:pass

# Preserve exact headline targets.
rb={r['race_id']:r for r in races}
for rid,h in head_by.items():
    if rid in rb:rb[rid]['y']=float(h['margin_d_minus_r_two_party_pctpt'])

seat_hist=defaultdict(list)
for r in sorted(races,key=lambda z:(z['state_abbrev'],z['seat'],z['cycle'])):
    seat_hist[(r['state_abbrev'],r['seat'])].append(r)

# National generic ballot.
hist,_=fetch_csv(HIST_URL);avg,_=fetch_csv(AVG_URL)
def pdate(s):
    m,d,y=[int(x) for x in s.split('/')];return date(y,m,d)
national={}
for cyc in (2006,2008,2010,2012,2014,2016):
    target=ELECTION[cyc]-timedelta(days=45);cand=[]
    for r in hist:
        if (r.get('subgroup') or '').strip()!='All polls':continue
        try:dt=pdate((r.get('modeldate') or '').strip())
        except:continue
        if dt>target:continue
        try:m=float(r['dem_estimate'])-float(r['rep_estimate'])
        except:continue
        cand.append((target-dt,dt,m))
    cand.sort(key=lambda z:z[0]);national[cyc]=cand[0][2]
for cyc in (2018,2020,2022):
    target=ELECTION[cyc]-timedelta(days=45);bd={}
    for r in avg:
        try:
            if int(r.get('cycle') or 0)!=cyc:continue
            dt=date.fromisoformat((r.get('date') or '').strip())
            if dt>target:continue
            bd.setdefault(dt,{})[(r.get('candidate') or '').strip()]=float(r['pct_estimate'])
        except:continue
    cand=[(target-dt,dt,v['Democrats']-v['Republicans']) for dt,v in bd.items() if 'Democrats' in v and 'Republicans' in v]
    cand.sort(key=lambda z:z[0]);national[cyc]=cand[0][2]

# Economic signal.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read();zf=zipfile.ZipFile(io.BytesIO(raw))
members=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
bname=max(members,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(bname).decode('utf-8-sig','replace'))));pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,c):
    try:return float((r.get(c) or '').replace(',','').strip())
    except:return None
growth={};us={}
for x in pi:
    nm=(x.get('GeoName') or '').replace('*','').strip()
    for cyc in ELECTION:
        a=val(x,f'{cyc}:Q1');b=val(x,f'{cyc-1}:Q1')
        if a is None or b in (None,0):continue
        g=100*(a/b-1)
        if nm in STATE_ABBR:growth[(cyc,STATE_ABBR[nm])]=g
        elif nm=='United States':us[cyc]=g

rows=[]
for r in races:
    cyc=r['cycle']
    if cyc not in ELECTION:continue
    if cyc in OUTER and r['race_id'] not in head_by:continue
    pv=pvi.get(r['race_id'])
    if pv is None:continue
    prev=[x for x in seat_hist[(r['state_abbrev'],r['seat'])] if x['cycle']<cyc]
    if not prev:continue
    q=max(prev,key=lambda z:z['cycle'])
    if cyc in OUTER:
        s=ss_by[r['race_id']];same=float(s['same_seat_last_prior_margin_two_party_pctpt']);gap=float(s['same_seat_last_prior_year_gap'])
        hc=hc_by[r['race_id']];inc_diff=float(hc['IncumbencyDiff']);outparty=float(hc['OutPartyIncumbent'])
    else:
        same=float(q['y']);gap=float(cyc-q['cycle'])
        dinc=1 if r['d_pid'] and r['d_pid']==q['winner_pid'] else 0
        rinc=1 if r['r_pid'] and r['r_pid']==q['winner_pid'] else 0
        inc_diff=dinc-rinc
        outparty=(1 if dinc and pv<0 else 0)-(1 if rinc and pv>0 else 0)
    vals=[growth[(cyc,s)] for s in STATE_ABBR.values() if (cyc,s) in growth]
    ng=us.get(cyc,statistics.mean(vals))
    econ=(growth[(cyc,r['state_abbrev'])]-ng)*PRES_SIGN[cyc]
    era=(cyc-2006)/4.0
    rows.append({'race_id':r['race_id'],'cycle':cyc,'state_abbrev':r['state_abbrev'],'y':r['y'],'pvi':pv,'same_last':same,'same_gap':gap,'econ':econ,'national':national[cyc],'inc_diff':inc_diff,'outparty':outparty,'same_era':same*era,'inc_era':inc_diff*era,'outparty_era':outparty*era})

BASE=['pvi','same_last','same_gap','econ','national']
ARCH={
 'none':[],
 'seat_era':['same_era'],
 'inc_level':['inc_diff','outparty'],
 'inc_era':['inc_diff','outparty','inc_era','outparty_era'],
 'seat_inc_era':['same_era','inc_diff','outparty','inc_era','outparty_era']
}
L_LOCAL=[0.0,4.0,16.0,64.0,256.0]
L_ECON=[0.0,16.0,64.0,256.0]
L_NAT=[0.0,1.0,4.0,16.0,64.0]
L_INC=[4.0,16.0,64.0,256.0,1024.0]
L_ERA=[16.0,64.0,256.0,1024.0,4096.0]

def design(dat,feats,stats=None):
    X=np.array([[float(r[f]) for f in feats] for r in dat])
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)
def fitpred(tr,te,arch,ll,le,ln,li,lr):
    local=ARCH[arch];feats=BASE+local
    X,st=design(tr,feats);Xt,_=design(te,feats,st);y=np.array([r['y'] for r in tr])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(feats,start=1):
        if f in ('same_last','same_gap'):pen[j]=ll
        elif f=='econ':pen[j]=le
        elif f=='national':pen[j]=ln
        elif f in ('inc_diff','outparty'):pen[j]=li
        elif f.endswith('_era') or f=='same_era':pen[j]=lr
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(tr):
    cycs=sorted(set(r['cycle'] for r in tr));cand=[]
    for arch in ARCH:
        il=[64.0] if arch in ('none','seat_era') else L_INC
        er=[256.0] if arch in ('none','inc_level') else L_ERA
        for ll,le,ln,li,lr in itertools.product(L_LOCAL,L_ECON,L_NAT,il,er):
            yy=[];pp=[]
            for vc in cycs[1:]:
                a=[r for r in tr if r['cycle']<vc];b=[r for r in tr if r['cycle']==vc]
                if len(a)<10 or not b:continue
                q=fitpred(a,b,arch,ll,le,ln,li,lr);yy.extend(r['y'] for r in b);pp.extend(q.tolist())
            cand.append((rmse(yy,pp) if yy else 1e9,len(ARCH[arch]),arch,ll,le,ln,li,lr))
    cand.sort(key=lambda z:(z[0],z[1],z[3]+z[4]+z[5]+z[6]+z[7]))
    return cand[0],cand[:20]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in rows if r['cycle']<tc];te=[r for r in rows if r['cycle']==tc]
    best,trace=tune(tr);sc,_,arch,ll,le,ln,li,lr=best
    q=fitpred(tr,te,arch,ll,le,ln,li,lr)
    choices.append({'test_cycle':tc,'arch':arch,'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,'lambda_inc':li,'lambda_era':lr,'inner_rmse':sc,'top20':' | '.join(f'{z[2]} L{z[3]} E{z[4]} N{z[5]} I{z[6]} R{z[7]}:{z[0]:.3f}' for z in trace)})
    for r,p in zip(te,q):pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],'arch':arch})

yy=[r['actual'] for r in pred];pp=[r['predicted'] for r in pred]
summary=[{'variant':'fullcycle_incumbency_era_nested','n':len(pred),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':acc(yy,pp)}]

for fn,data in [('fullcycle_inc_era_summary.csv',summary),('fullcycle_inc_era_choices.csv',choices),('fullcycle_inc_era_predictions.csv',pred)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

z=summary[0]
lines=['# Full-cycle incumbency era-interaction OOS','',f'- Generated UTC: {datetime.now(timezone.utc).isoformat()}',f'- Modeling rows: {len(rows)}','- Outer validation: preserved 99 races in 2014, 2018, 2022.','- 2000, 2002, 2004 are used only as SameSeat lag sources.','- Headline incumbency/out-party flags use the corrected audited features; historical training flags use prior same-seat winner identity.','',
'## Result','',f'- RMSE: {z["rmse"]:.4f}',f'- MAE: {z["mae"]:.4f}',f'- Direction: {z["direction_pct"]:.1f}%','',
'## Nested choices','', '| cycle | architecture | local | econ | national | inc | era | inner RMSE |','|---:|---|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['arch']} | {r['lambda_local']} | {r['lambda_econ']} | {r['lambda_national']} | {r['lambda_inc']} | {r['lambda_era']} | {r['inner_rmse']:.4f} |")
lines += ['','## Comparison','', '- Current leakage-safe full-cycle National+economic benchmark before this experiment: RMSE 8.8467.','- Keep this architecture only if its 99-row RMSE is below 8.8467.','',
'## Outputs','- performance/results/fullcycle_inc_era_summary.csv','- performance/results/fullcycle_inc_era_choices.csv','- performance/results/fullcycle_inc_era_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
