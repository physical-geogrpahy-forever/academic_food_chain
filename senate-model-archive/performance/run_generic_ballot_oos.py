#!/usr/bin/env python3
# RUN_TAG_GENERIC_V1
# RUN_TAG_GENERIC_V2
import csv, io, hashlib
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from urllib.request import Request, urlopen
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PANEL=ROOT/'performance/results/candidate_block_oos_panel.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0206_generic-ballot-national-oos.md'
URL='https://projects.fivethirtyeight.com/polls-page/data/generic_ballot_polls_historical.csv'
OUTDIR.mkdir(parents=True,exist_ok=True)

ELECTION={2006:date(2006,11,7),2010:date(2010,11,2),2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
OUTER=[2014,2018,2022]
WGRID=[14,28,42,56]
LGRID=[0.0,0.1,0.5,1.0,4.0,16.0,64.0]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
panel=load(PANEL)

raw=urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0 CoreV2R-performance/1.0'}),timeout=90).read()
sha=hashlib.sha256(raw).hexdigest()
polls=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))
if not polls: raise RuntimeError('generic ballot historical file returned no rows')

def parse_date(s):
    s=(s or '').strip()
    for fmt in ['%m/%d/%y','%m/%d/%Y','%Y-%m-%d','%m-%d-%Y','%m-%d-%y']:
        try: return datetime.strptime(s,fmt).date()
        except: pass
    # created_at often has timestamp
    try: return datetime.fromisoformat(s.replace('Z','+00:00')).date()
    except: return None

# Collapse each question/poll to one DEM-REP margin.
groups={}
for r in polls:
    q=r.get('question_id') or r.get('poll_id') or ''
    if not q: continue
    end=parse_date(r.get('end_date') or r.get('enddate') or '')
    if not end: continue
    created=parse_date(r.get('created_at') or '')
    key=(q,end,created)
    g=groups.setdefault(key,{'end':end,'created':created,'dem':None,'rep':None,'sample':None})
    party=(r.get('party') or '').strip().upper()
    ans=(r.get('answer') or '').strip().lower()
    try: pct=float(r.get('pct') or '')
    except: continue
    if party in {'DEM','D','DEMOCRAT'} or ans.startswith('democrat'): g['dem']=pct
    if party in {'REP','R','REPUBLICAN'} or ans.startswith('republican'): g['rep']=pct
    try: g['sample']=float(r.get('sample_size') or '')
    except: pass

questions=[]
for g in groups.values():
    if g['dem'] is None or g['rep'] is None: continue
    g['margin']=g['dem']-g['rep']; questions.append(g)
if len(questions)<100: raise RuntimeError(f'Only {len(questions)} usable generic-ballot questions parsed')

def snapshot_value(cycle,window):
    snap=ELECTION[cycle]-timedelta(days=45)
    lo=snap-timedelta(days=window-1)
    xs=[g for g in questions if lo<=g['end']<=snap and (g['created'] is None or g['created']<=snap)]
    if not xs:
        xs=[g for g in questions if g['end']<=snap and (snap-g['end']).days<=90 and (g['created'] is None or g['created']<=snap)]
    if not xs: return None,0,None
    return sum(g['margin'] for g in xs)/len(xs),len(xs),max(g['end'] for g in xs)

snapshots=[]
for cyc in ELECTION:
    for w in WGRID:
        v,n,last=snapshot_value(cyc,w)
        snapshots.append({'cycle':cyc,'window_days':w,'snapshot_date':(ELECTION[cyc]-timedelta(days=45)).isoformat(),'generic_margin': '' if v is None else v,'poll_questions':n,'latest_end_date':'' if last is None else last.isoformat(),'source_sha256':sha})
snapby={(int(r['cycle']),int(r['window_days'])):r for r in snapshots}

STRUCT=['pvi','same_seat']
def add_nat(rows,w):
    out=[]
    for r in rows:
        z=dict(r); rec=snapby[(int(r['cycle']),w)]
        if rec['generic_margin']=='': raise RuntimeError(f'Missing generic margin for {r["cycle"]} window {w}')
        z['generic_margin']=float(rec['generic_margin']); out.append(z)
    return out

def design(rows,extra=False,stats=None):
    feats=STRUCT+(['generic_margin'] if extra else [])
    X=np.array([[float(r[f]) for f in feats] for r in rows],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    return np.column_stack([np.ones(len(rows)),(X-mu)/sd]),(mu,sd)

def fit(train,test,extra=False,lam=0.0,y_override=None):
    X,stats=design(train,extra); Xt,_=design(test,extra,stats)
    y=np.array(y_override if y_override is not None else [float(r['y']) for r in train])
    pen=np.zeros(X.shape[1]);
    if extra: pen[-1]=lam
    A=X.T@X+np.diag(pen+1e-8); A[0,0]-=1e-8
    beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def direction(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def pred_offset(train,test,w):
    tr=add_nat(train,w); te=add_nat(test,w)
    yadj=[float(r['y'])-float(r['generic_margin']) for r in tr]
    b=fit(tr,te,extra=False,y_override=yadj)
    return np.array([x+float(r['generic_margin']) for x,r in zip(b,te)])

def pred_reg(train,test,w,lam):
    return fit(add_nat(train,w),add_nat(test,w),extra=True,lam=lam)

def tune_offset(train):
    cycles=sorted(set(int(r['cycle']) for r in train)); cand=[]
    for w in WGRID:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr=pred_offset(tr,va,w); yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,w))
    cand.sort(); return cand[0][1],cand

def tune_reg(train):
    cycles=sorted(set(int(r['cycle']) for r in train)); cand=[]
    for w in WGRID:
      for lam in LGRID:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train if int(r['cycle'])<vc]; va=[r for r in train if int(r['cycle'])==vc]
            if len(tr)<10 or not va: continue
            pr=pred_reg(tr,va,w,lam); yy.extend(float(r['y']) for r in va); pp.extend(pr.tolist())
        cand.append((rmse(yy,pp) if yy else 1e9,w,-lam,lam))
    cand.sort(); return cand[0][1],cand[0][3],cand

variants=['structural_only','generic_offset_nested','generic_regression_nested']
pred=[]; hyper=[]
for tc in OUTER:
    train=[r for r in panel if int(r['cycle'])<tc]; test=[r for r in panel if int(r['cycle'])==tc]
    for v in variants:
        if v=='structural_only': pr=fit(train,test); w=''; lam=''
        elif v=='generic_offset_nested':
            w,trace=tune_offset(train); lam=''; pr=pred_offset(train,test,w)
            hyper.append({'test_cycle':tc,'variant':v,'window':w,'lambda':'','inner_trace':' | '.join(f'w={x[1]}:{x[0]:.4f}' for x in trace)})
        else:
            w,lam,trace=tune_reg(train); pr=pred_reg(train,test,w,lam)
            hyper.append({'test_cycle':tc,'variant':v,'window':w,'lambda':lam,'inner_trace':' | '.join(f'w={x[1]},l={x[3]}:{x[0]:.4f}' for x in trace[:12])})
        for r,p in zip(test,pr): pred.append({'variant':v,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual_margin':r['y'],'predicted_margin':float(p),'error':float(p)-float(r['y']),'window':w,'lambda':lam})

summary=[]
for v in variants:
    rr=[r for r in pred if r['variant']==v]; y=[float(r['actual_margin']) for r in rr]; p=[float(r['predicted_margin']) for r in rr]
    summary.append({'variant':v,'scope':'2014_2018_2022_combined','n':len(rr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':direction(y,p)})
    for tc in OUTER:
        z=[r for r in rr if int(r['test_cycle'])==tc]; yy=[float(r['actual_margin']) for r in z]; pp=[float(r['predicted_margin']) for r in z]
        summary.append({'variant':v,'scope':str(tc),'n':len(z),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':direction(yy,pp)})

for name,data in [('generic_ballot_45d_snapshots.csv',snapshots),('generic_ballot_oos_predictions.csv',pred),('generic_ballot_oos_summary.csv',summary),('generic_ballot_oos_hyperparams.csv',hyper)]:
    with (OUTDIR/name).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)

comb={r['variant']:r for r in summary if r['scope']=='2014_2018_2022_combined'}
base=comb['structural_only']; off=comb['generic_offset_nested']; reg=comb['generic_regression_nested']
do=float(base['rmse'])-float(off['rmse']); dr=float(base['rmse'])-float(reg['rmse'])
best='generic_offset_nested' if off['rmse']<reg['rmse'] else 'generic_regression_nested'; delta=max(do,dr)
decision='KEEP_GENERIC_NATIONAL' if delta>0 else 'REJECT_GENERIC_NATIONAL'
lines=[
 '# Performance experiment: 45-day generic ballot National proxy','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Source SHA256: {sha}',
 f'- Parsed usable poll questions: {len(questions)}',
 '- All poll end dates and available created_at dates are constrained to the 45-day snapshot or earlier.','',
 '## Combined results','',
 '| variant | N | RMSE | MAE | direction |',
 '|---|---:|---:|---:|---:|'
]
for v in variants:
    z=comb[v]; lines.append(f"| {v} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += [
 '','## Decision','',
 f'- Generic offset improvement vs structural: {do:+.4f} RMSE points.',
 f'- Generic regression improvement vs structural: {dr:+.4f} RMSE points.',
 f'- Best architecture: {best}.',
 f'- Decision: {decision}','',
 '## Next','',
 'If this National proxy improves OOS, retain it as the first reconstructable National_t component and test whether approval adds incremental OOS value. If not, reject it rather than forcing a national polling term.','',
 '## Outputs','',
 '- performance/results/generic_ballot_45d_snapshots.csv',
 '- performance/results/generic_ballot_oos_predictions.csv',
 '- performance/results/generic_ballot_oos_summary.csv',
 '- performance/results/generic_ballot_oos_hyperparams.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))