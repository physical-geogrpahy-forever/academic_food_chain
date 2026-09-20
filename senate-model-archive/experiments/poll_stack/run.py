#!/usr/bin/env python3
import csv, io, math, runpy, urllib.request
from collections import defaultdict
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BASESCRIPT=ROOT/'performance/run_fullcycle_inc_era_oos.py'
OUT=ROOT/'experiments/poll_stack/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0310_poll-fundamentals-stacked-direction.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

POLL_URL='https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'
ELECTION={2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)}
OUTER=[2014,2018,2022]
WMAX=0.75; K=0.5

ns=runpy.run_path(str(BASESCRIPT))
rows=ns['rows']
fitpred=ns['fitpred']
tune=ns['tune']

def parse_date(s):
    s=(s or '').strip()
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None

# Senate polls from pinned GitHub repository content.
req=urllib.request.Request(POLL_URL,headers={'User-Agent':'CoreV2R-poll-stack/1.0'})
raw=urllib.request.urlopen(req,timeout=120).read().decode('utf-8-sig','replace')
pollrows=list(csv.DictReader(io.StringIO(raw)))
fields=set(pollrows[0].keys())

polls=[]
if 'margin_poll' in fields:
    for r in pollrows:
        try:cyc=int(r.get('year') or r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        typ=((r.get('type_simple') or '')+' '+(r.get('type_detail') or '')+' '+(r.get('race') or '')).lower()
        if 'sen' not in typ:continue
        rid=str(r.get('race_id') or '').strip()
        if not rid:continue
        dt=parse_date(r.get('polldate') or r.get('end_date'))
        if not dt:continue
        try:m=float(r.get('margin_poll') or '')
        except:continue
        p1=(r.get('cand1_party') or '').upper();p2=(r.get('cand2_party') or '').upper()
        if p1 and p2:
            if p1.startswith('REP') and p2.startswith('DEM'):m=-m
            elif not (p1.startswith('DEM') and p2.startswith('REP')):continue
        try:n=float(r.get('samplesize') or 600)
        except:n=600.
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':m})
else:
    # modern long format
    grouped=defaultdict(list)
    for r in pollrows:
        try:cyc=int(r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        office=(r.get('office_type') or '').lower()
        if office and 'senate' not in office:continue
        stage=(r.get('stage') or '').lower()
        if stage and 'general' not in stage:continue
        rid=str(r.get('race_id') or '').strip();qid=str(r.get('question_id') or r.get('poll_id') or '').strip()
        if rid and qid:grouped[(cyc,rid,qid)].append(r)
    for (cyc,rid,qid),rr in grouped.items():
        dem=[];rep=[]
        for r in rr:
            party=(r.get('candidate_party') or r.get('party') or '').upper()
            try:pct=float(r.get('pct') or '')
            except:continue
            if party.startswith('DEM'):dem.append(pct)
            elif party.startswith('REP'):rep.append(pct)
        if len(dem)!=1 or len(rep)!=1:continue
        dt=parse_date(rr[0].get('end_date') or rr[0].get('polldate'))
        if not dt:continue
        try:n=float(rr[0].get('sample_size') or 600)
        except:n=600.
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':dem[0]-rep[0]})

byrace=defaultdict(list)
for p in polls:byrace[(p['cycle'],p['race_id'])].append(p)

def aggregate(ps,target,window=45,half_life=14):
    e=[]
    for p in ps:
        age=(target-p['end_date']).days
        if age<0 or age>window:continue
        rec=math.exp(-math.log(2)*age/half_life)
        sw=math.sqrt(min(max(p['sample_size'],100.),5000.)/600.)
        wt=rec*sw;e.append((p,wt))
    if not e:return None
    s=sum(w for _,w in e);m=sum(p['margin']*w for p,w in e)/s
    neff=s*s/sum(w*w for _,w in e)
    return m,neff,len(e)

# Build strictly rolling prior predictions for every cycle that has enough training history.
hist=[]
for cyc in sorted(ELECTION):
    tr=[r for r in rows if int(r['cycle'])<cyc]
    te=[r for r in rows if int(r['cycle'])==cyc]
    if len(tr)<25 or not te:continue
    try:
        best,_=tune(tr)
    except Exception:
        continue
    sc,_,arch,ll,le,ln,li,lr=best
    pp=fitpred(tr,te,arch,ll,le,ln,li,lr)
    for r,p in zip(te,pp):
        target=ELECTION[cyc]-timedelta(days=45)
        agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target)
        if agg is None:
            pollm='';neff=0.;pc=0;post=float(p)
        else:
            pollm,neff,pc=agg
            w=WMAX*neff/(neff+K)
            post=(1-w)*float(p)+w*pollm
        hist.append({'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],'actual':float(r['y']),
                     'prior':float(p),'poll':pollm,'neff':neff,'poll_count':pc,'posterior':post})

# Feature sets for the stacked classifier. Empty-poll races retain baseline posterior and are not stacked.
FEATURESETS={
 'basic':['posterior'],
 'prior_poll':['prior','poll'],
 'disagree':['prior','poll','posterior','neff','abs_gap','sign_disagree'],
 'rich':['prior','poll','posterior','neff','poll_count','abs_gap','abs_prior','abs_poll','sign_disagree']
}
LAM=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]

def feat(r,name):
    vals={'prior':r['prior'],'poll':float(r['poll']),'posterior':r['posterior'],'neff':r['neff'],'poll_count':r['poll_count'],
          'abs_gap':abs(r['prior']-float(r['poll'])),'abs_prior':abs(r['prior']),'abs_poll':abs(float(r['poll'])),
          'sign_disagree':1.0 if (r['prior']>0)!=(float(r['poll'])>0) else 0.0}
    return [vals[k] for k in FEATURESETS[name]]

def sigmoid(z):
    return 1/(1+np.exp(-np.clip(z,-35,35)))

def design(dat,name,stats=None):
    X=np.array([feat(r,name) for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fit_logit(tr,te,name,lam):
    X,st=design(tr,name);Xt,_=design(te,name,st)
    y=np.array([1. if r['actual']>0 else 0. for r in tr]);b=np.zeros(X.shape[1]);pen=np.zeros(X.shape[1]);pen[1:]=lam
    for _ in range(100):
        p=sigmoid(X@b);w=np.clip(p*(1-p),1e-5,None);z=X@b+(y-p)/w
        Xw=X*np.sqrt(w)[:,None];zw=z*np.sqrt(w)
        nb=np.linalg.pinv(Xw.T@Xw+np.diag(pen))@(Xw.T@zw)
        if np.max(np.abs(nb-b))<1e-8:b=nb;break
        b=nb
    return sigmoid(Xt@b)

def accuracy(dat,probs):
    return 100*np.mean([(p>=.5)==(r['actual']>0) for r,p in zip(dat,probs)])
def logloss(dat,probs):
    y=np.array([1. if r['actual']>0 else 0. for r in dat]);p=np.clip(np.asarray(probs),1e-9,1-1e-9)
    return float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))

def select_model(train):
    cycles=sorted(set(r['cycle'] for r in train));grid=[]
    for fs in FEATURESETS:
      for lam in LAM:
        yy=[];pp=[]
        for vc in cycles[1:]:
            a=[r for r in train if r['cycle']<vc and r['poll_count']>0]
            b=[r for r in train if r['cycle']==vc and r['poll_count']>0]
            if len(a)<15 or not b:continue
            q=fit_logit(a,b,fs,lam);yy+=b;pp+=q.tolist()
        if not yy:continue
        grid.append((-accuracy(yy,pp),logloss(yy,pp),len(FEATURESETS[fs]),lam,fs))
    if not grid:return None,[]
    grid.sort()
    return grid[0],grid[:12]

outpred=[];choices=[]
for tc in OUTER:
    train=[r for r in hist if r['cycle']<tc and r['poll_count']>0]
    test=[r for r in hist if r['cycle']==tc]
    best,trace=select_model(train)
    if best is None:
        fs='basic';lam=64.
    else:
        na,ll,nf,lam,fs=best
    covered=[r for r in test if r['poll_count']>0]
    probs=fit_logit(train,covered,fs,lam) if covered and len(train)>=15 else []
    pmap={(r['race_id']):p for r,p in zip(covered,probs)}
    choices.append({'test_cycle':tc,'feature_set':fs,'lambda':lam,'train_poll_rows':len(train),
                    'inner_accuracy_pct':'' if best is None else -best[0],
                    'inner_logloss':'' if best is None else best[1],
                    'top12':' | '.join(f'{z[4]}@{z[3]} acc={-z[0]:.1f} ll={z[1]:.3f}' for z in trace)})
    for r in test:
        base_ok=int((r['posterior']>0)==(r['actual']>0))
        if r['poll_count']>0 and r['race_id'] in pmap:
            prob=float(pmap[r['race_id']]);stack_dir=prob>=.5
        else:
            prob=1. if r['posterior']>0 else 0.;stack_dir=r['posterior']>0
        stack_ok=int(stack_dir==(r['actual']>0))
        outpred.append({**r,'stack_prob_D':prob,'baseline_correct':base_ok,'stack_correct':stack_ok,'feature_set':fs,'lambda':lam})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=outpred if scope=='combined' else [r for r in outpred if r['cycle']==int(scope)]
    n=len(rr);bc=sum(r['baseline_correct'] for r in rr);sc=sum(r['stack_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':bc,'baseline_accuracy_pct':100*bc/n,
                    'stack_correct':sc,'stack_accuracy_pct':100*sc/n,'net_correct_gain':sc-bc,
                    'poll_covered':sum(r['poll_count']>0 for r in rr)})

for fn,data in [('stack_summary.csv',summary),('stack_choices.csv',choices),('stack_predictions.csv',outpred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

comb=summary[0]
changed=[r for r in outpred if r['baseline_correct']!=r['stack_correct']]
lines=['# Poll-fundamentals stacked direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Primary metric: historical OOS winner-direction accuracy.',
       '- Stack training uses only cycles earlier than each outer test cycle.',
       '- Baseline for comparison is the fixed Core V2 poll blend, not an RMSE-selected replacement.','',
       '## Result','',
       '| scope | N | poll-covered | baseline correct | baseline accuracy | stacked correct | stacked accuracy | net |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:
    lines.append(f"| {r['scope']} | {r['n']} | {r['poll_covered']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['stack_correct']} | {r['stack_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} |")
lines += ['','## Outer selected stacks','',
          '| test | feature set | lambda | prior poll rows | inner accuracy |','|---:|---|---:|---:|---:|']
for r in choices:
    ia='NA' if r['inner_accuracy_pct']=='' else f"{float(r['inner_accuracy_pct']):.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda']} | {r['train_poll_rows']} | {ia} |")
lines += ['','## Races whose correctness changed','']
for r in changed:
    lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> stack {'correct' if r['stack_correct'] else 'wrong'}")
lines += ['','## Decision','',
          'Adopt only if stacked accuracy exceeds the fixed-blend 94/99 benchmark and the gain is not created by using the outer test cycle in stack selection.','',
          '## Outputs','',
          '- experiments/poll_stack/results/stack_summary.csv',
          '- experiments/poll_stack/results/stack_choices.csv',
          '- experiments/poll_stack/results/stack_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
