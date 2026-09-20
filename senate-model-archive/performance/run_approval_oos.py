#!/usr/bin/env python3
import csv, io, json
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
import numpy as np
import pandas as pd
import requests

ROOT=Path(__file__).resolve().parents[1]
PANEL=ROOT/'performance/results/candidate_block_oos_panel.csv'
OUTDIR=ROOT/'performance/results'
OUTDIR.mkdir(parents=True,exist_ok=True)

ELECTION={2006:date(2006,11,7),2010:date(2010,11,2),2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
PRESIDENT={2006:'George W. Bush',2010:'Barack Obama',2014:'Barack Obama',2018:'Donald J. Trump',2022:'Joseph R. Biden Jr.'}
PRES_SIGN={2006:-1,2010:1,2014:1,2018:-1,2022:1}
URLS={
 'George W. Bush':'https://www.presidency.ucsb.edu/statistics/data/george-w-bush-public-approval',
 'Barack Obama':'https://www.presidency.ucsb.edu/statistics/data/barack-obama-public-approval',
 'Donald J. Trump':'https://www.presidency.ucsb.edu/statistics/data/donald-j-trump-public-approval',
 'Joseph R. Biden Jr.':'https://www.presidency.ucsb.edu/statistics/data/joseph-r-biden-public-approval',
}
OUTER=[2014,2018,2022]
LGRID=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
panel=load(PANEL)

def normcol(x):
    if isinstance(x,tuple): x=' '.join(str(v) for v in x if str(v)!='nan')
    return ' '.join(str(x).lower().replace('\n',' ').split())

def parse_page(president,url):
    resp=requests.get(url,headers={'User-Agent':'Mozilla/5.0 CoreV2R-performance/1.0'},timeout=60)
    resp.raise_for_status()
    tables=pd.read_html(io.StringIO(resp.text))
    for df in tables:
        cols=[normcol(x) for x in df.columns]
        mapping={c:i for i,c in enumerate(cols)}
        sidx=next((i for i,c in enumerate(cols) if 'start date' in c),None)
        eidx=next((i for i,c in enumerate(cols) if 'end date' in c),None)
        aidx=next((i for i,c in enumerate(cols) if c.startswith('approv') or 'approving' in c),None)
        didx=next((i for i,c in enumerate(cols) if 'disapprov' in c),None)
        if None in [sidx,eidx,aidx,didx]: continue
        out=[]
        for _,row in df.iterrows():
            try:
                sd=pd.to_datetime(row.iloc[sidx]).date(); ed=pd.to_datetime(row.iloc[eidx]).date()
                ap=float(row.iloc[aidx]); dis=float(row.iloc[didx])
            except: continue
            out.append({'president':president,'start':sd,'end':ed,'approval':ap,'disapproval':dis})
        if out: return out,resp.text
    raise RuntimeError('No approval table parsed for '+president)

series={}; manifests=[]
for president,url in URLS.items():
    rows,html=parse_page(president,url); series[president]=rows
    manifests.append({'president':president,'url':url,'rows':len(rows)})

snapshots=[]
for cyc in ELECTION:
    snap=ELECTION[cyc]-timedelta(days=45); pres=PRESIDENT[cyc]
    xs=[r for r in series[pres] if r['end']<=snap]
    if not xs: raise RuntimeError(f'No approval observation for {cyc} snapshot {snap}')
    x=max(xs,key=lambda r:r['end'])
    net=x['approval']-x['disapproval']; sig=PRES_SIGN[cyc]*net
    snapshots.append({'cycle':cyc,'snapshot_date':snap.isoformat(),'president':pres,'observation_end':x['end'].isoformat(),'approval':x['approval'],'disapproval':x['disapproval'],'net_approval':net,'signed_approval_signal':sig,'lag_days':(snap-x['end']).days})
snapby={int(r['cycle']):r for r in snapshots}

STRUCT=['pvi','same_seat']
def attach(rows):
    out=[]
    for r in rows:
        z=dict(r); z['approval_signal']=float(snapby[int(r['cycle'])]['signed_approval_signal']); out.append(z)
    return out

def design(rows,extra=False,stats=None):
    feats=STRUCT+(['approval_signal'] if extra else [])
    X=np.array([[float(r[f]) for f in feats] for r in rows],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(rows)),(X-mu)/sd]),(mu,sd)

def fit(train,test,extra=False,lam=0.0):
    train=attach(train) if extra else train; test=attach(test) if extra else test
    X,stats=design(train,extra); Xt,_=design(test,extra,stats)
    y=np.array([float(r['y']) for r in train])
    pen=np.zeros(X.shape[1]);
    if extra: pen[-1]=lam
    A=X.T@X+np.diag(pen+1e-8); A[0,0]-=1e-8
    beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta,beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def direction(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(train):
    cycles=sorted(set(int(r['cycle']) for r in train)); cand=[]
    for lam in LGRID:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr,_=fit(tr,va,extra=True,lam=lam)
            yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,lam))
    cand.sort(); return cand[0][1],cand

variants=['structural_only','approval_regression_nested']
pred=[]; hyper=[]
for tc in OUTER:
    train=[r for r in panel if int(r['cycle'])<tc]; test=[r for r in panel if int(r['cycle'])==tc]
    for v in variants:
        if v=='structural_only': pr,beta=fit(train,test); lam=''
        else:
            lam,trace=tune(train); pr,beta=fit(train,test,extra=True,lam=lam)
            hyper.append({'test_cycle':tc,'lambda':lam,'inner_trace':' | '.join(f'{x[1]}:{x[0]:.4f}' for x in trace),'beta_approval_standardized':float(beta[-1])})
        for r,p in zip(test,pr): pred.append({'variant':v,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual_margin':r['y'],'predicted_margin':float(p),'error':float(p)-float(r['y']),'lambda':lam})

summary=[]
for v in variants:
    rr=[r for r in pred if r['variant']==v]; y=[float(r['actual_margin']) for r in rr]; p=[float(r['predicted_margin']) for r in rr]
    summary.append({'variant':v,'scope':'2014_2018_2022_combined','n':len(rr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':direction(y,p)})
    for tc in OUTER:
        z=[r for r in rr if int(r['test_cycle'])==tc]; yy=[float(r['actual_margin']) for r in z]; pp=[float(r['predicted_margin']) for r in z]
        summary.append({'variant':v,'scope':str(tc),'n':len(z),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':direction(yy,pp)})

print('SNAP_JSON='+json.dumps(snapshots))
print('SUMMARY_JSON='+json.dumps(summary))
print('HYPER_JSON='+json.dumps(hyper))
print('SOURCE_JSON='+json.dumps(manifests))
comb={r['variant']:r for r in summary if r['scope']=='2014_2018_2022_combined'}
delta=float(comb['structural_only']['rmse'])-float(comb['approval_regression_nested']['rmse'])
print(f'APPROVAL_RMSE_DELTA={delta:+.6f}')