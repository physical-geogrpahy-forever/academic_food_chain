#!/usr/bin/env python3
import csv, io, math, re, urllib.request
from collections import defaultdict
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
PRIOR=ROOT/'performance/results/fullcycle_inc_era_predictions.csv'
OUT=ROOT/'experiments/poll_house_effect/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0320_pollster-house-effect-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

POLL_URL='https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'
ELECTION={2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)}
OUTER=[2014,2018,2022]
WMAX=.75;KBLEND=.5
KGRID=[1.,2.,5.,10.,20.,50.]
MODES=['none','global','pollster']

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def truth(v):return str(v).strip().lower()=='true'
def parse_date(s):
    s=(s or '').strip()
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None
def norm(s):
    s=(s or '').lower();s=re.sub(r'[^a-z0-9 ]+',' ',s);return re.sub(r'\s+',' ',s).strip()

# Final D-R two-party margins by race_id.
sen=load(SEN)
by=defaultdict(list)
for r in sen:
    if r.get('stage')=='general':by[str(r['race_id'])].append(r)

def final_margin(rr):
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
    cand={}
    for r in use:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key:continue
        c=cand.setdefault(key,{'votes':0,'parties':set(),'missing':False})
        for q in ((r.get('ballot_party') or ''),(r.get('party') or '')):
            if q.strip():c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v:c['missing']=True
        else:
            try:c['votes']+=int(float(v))
            except:c['missing']=True
    cs=list(cand.values())
    ds=[c for c in cs if 'DEM' in c['parties']];rs=[c for c in cs if 'REP' in c['parties']]
    if len(ds)!=1 or len(rs)!=1 or ds[0]['missing'] or rs[0]['missing']:return None
    d,r=ds[0]['votes'],rs[0]['votes']
    if d+r<=0:return None
    return 100*(d-r)/(d+r)

actual={}
cycle_of={}
for rid,rr in by.items():
    try:cyc=int(rr[0]['cycle'])
    except:continue
    if cyc not in ELECTION:continue
    m=final_margin(rr)
    if m is not None:actual[rid]=m;cycle_of[rid]=cyc

# Poll questions.
req=urllib.request.Request(POLL_URL,headers={'User-Agent':'CoreV2R-house-effect/1.0'})
raw=urllib.request.urlopen(req,timeout=120).read().decode('utf-8-sig','replace')
pr=list(csv.DictReader(io.StringIO(raw)));fields=set(pr[0].keys())
polls=[]
if 'margin_poll' in fields:
    for r in pr:
        try:cyc=int(r.get('year') or r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        typ=((r.get('type_simple') or '')+' '+(r.get('type_detail') or '')+' '+(r.get('race') or '')).lower()
        if 'sen' not in typ:continue
        rid=str(r.get('race_id') or '').strip()
        if rid not in actual:continue
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
        pollster=(r.get('pollster') or r.get('pollster_rating_name') or 'UNKNOWN').strip()
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':m,'pollster':pollster})
else:
    grouped=defaultdict(list)
    for r in pr:
        try:cyc=int(r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        office=(r.get('office_type') or '').lower()
        if office and 'senate' not in office:continue
        stage=(r.get('stage') or '').lower()
        if stage and 'general' not in stage:continue
        rid=str(r.get('race_id') or '').strip();qid=str(r.get('question_id') or r.get('poll_id') or '').strip()
        if rid in actual and qid:grouped[(cyc,rid,qid)].append(r)
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
        pollster=(rr[0].get('pollster') or rr[0].get('pollster_rating_name') or 'UNKNOWN').strip()
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':dem[0]-rep[0],'pollster':pollster})

# One pollster-race error observation, using final 60-day polls so prolific pollsters do not dominate.
per_pr=defaultdict(list)
for p in polls:
    ed=ELECTION[p['cycle']]
    age=(ed-p['end_date']).days
    if 0<=age<=60:
        per_pr[(p['cycle'],p['race_id'],p['pollster'])].append(p['margin']-actual[p['race_id']])
error_obs=[]
for (cyc,rid,pollster),errs in per_pr.items():
    error_obs.append({'cycle':cyc,'race_id':rid,'pollster':pollster,'error':sum(errs)/len(errs)})

byrace=defaultdict(list)
for p in polls:byrace[(p['cycle'],p['race_id'])].append(p)

def bias_map(test_cycle,k,mode):
    obs=[x for x in error_obs if x['cycle']<test_cycle]
    if not obs:return {},0.
    global_mean=sum(x['error'] for x in obs)/len(obs)
    byp=defaultdict(list)
    for x in obs:byp[x['pollster']].append(x['error'])
    out={}
    for p,e in byp.items():
        mu=sum(e)/len(e);n=len(e)
        if mode=='none':b=0.
        elif mode=='global':b=global_mean
        else:b=global_mean+(n/(n+k))*(mu-global_mean)
        out[p]=b
    return out,(0. if mode=='none' else global_mean)

def aggregate(cyc,rid,bias,global_bias,mode,window=45,hl=14):
    target=ELECTION[cyc]-timedelta(days=45)
    e=[]
    for p in byrace.get((cyc,rid),[]):
        age=(target-p['end_date']).days
        if age<0 or age>window:continue
        b=0. if mode=='none' else bias.get(p['pollster'],global_bias)
        adj=p['margin']-b
        wt=math.exp(-math.log(2)*age/hl)*math.sqrt(min(max(p['sample_size'],100.),5000.)/600.)
        e.append((adj,wt))
    if not e:return None
    s=sum(w for _,w in e);m=sum(x*w for x,w in e)/s;neff=s*s/sum(w*w for _,w in e)
    return m,neff,len(e)

# Select poll adjustment using only earlier cycles' poll direction accuracy.
def select(test_cycle):
    train_cycles=[c for c in ELECTION if c<test_cycle]
    cand=[]
    for mode in MODES:
      ks=[10.] if mode!='pollster' else KGRID
      for k in ks:
        bias,gb=bias_map(test_cycle,k,mode)
        ok=n=0;abs_err=[]
        for cyc in train_cycles:
            for rid,m in actual.items():
                if cycle_of.get(rid)!=cyc:continue
                agg=aggregate(cyc,rid,bias,gb,mode)
                if agg is None:continue
                pm,neff,pc=agg;n+=1;ok+=int((pm>0)==(m>0));abs_err.append(abs(pm-m))
        if n:
            cand.append((-100*ok/n,sum(abs_err)/len(abs_err),k,mode,n))
    cand.sort()
    return cand[0],cand[:12]

prior=load(PRIOR)
prior=[r for r in prior if int(r['test_cycle']) in OUTER]
pred=[];choices=[]
for tc in OUTER:
    best,trace=select(tc);negacc,mae,k,mode,ntrain=best
    bias,gb=bias_map(tc,k,mode)
    choices.append({'test_cycle':tc,'mode':mode,'k_house':k,'inner_poll_accuracy_pct':-negacc,'inner_poll_mae':mae,'inner_poll_races':ntrain,
                    'top12':' | '.join(f'{z[3]} k{z[2]} acc={-z[0]:.1f} mae={z[1]:.2f}' for z in trace)})
    for r in prior:
        if int(r['test_cycle'])!=tc:continue
        rid=str(r['race_id']);pm=float(r['predicted']);act=float(r['actual'])
        agg=aggregate(tc,rid,bias,gb,mode)
        if agg is None:
            pollm='';neff=0.;pc=0;post=pm
        else:
            pollm,neff,pc=agg;w=WMAX*neff/(neff+KBLEND);post=(1-w)*pm+w*pollm
        pred.append({'test_cycle':tc,'race_id':rid,'state_abbrev':r['state_abbrev'],'actual':act,'prior':pm,
                     'poll_adjusted':pollm,'n_eff':neff,'poll_count':pc,'posterior':post,
                     'correct':int((post>0)==(act>0)),'mode':mode,'k_house':k})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if int(r['test_cycle'])==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n,'poll_covered':sum(r['poll_count']>0 for r in rr)})

for fn,data in [('house_effect_summary.csv',summary),('house_effect_choices.csv',choices),('house_effect_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

comb=summary[0]
wrong=[r for r in pred if not r['correct']]
lines=['# Pollster house-effect direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Primary metric: winner-direction accuracy.',
       '- Pollster house effects use only Senate poll errors from cycles before each test cycle.',
       '- Pollster errors are first averaged within pollster-race to avoid overweighting repeated polls.',
       '- Shrinkage strength is selected from earlier-cycle poll direction accuracy only.','',
       '## Result','',
       '| scope | N | correct | wrong | accuracy | poll-covered |','|---|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% | {r['poll_covered']} |")
lines += ['','## Selected adjustment by outer cycle','',
          '| test | mode | k | inner poll accuracy | inner poll MAE | prior poll races |','|---:|---|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['mode']} | {r['k_house']} | {r['inner_poll_accuracy_pct']:.1f}% | {r['inner_poll_mae']:.2f} | {r['inner_poll_races']} |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: posterior={r['posterior']:.2f}, actual={r['actual']:.2f}")
lines += ['','## Benchmark','',
          '- Fixed unadjusted poll blend benchmark: 94/99 = 94.9%.',
          '- Keep pollster adjustment only if it exceeds 94/99 without outer-cycle tuning.','',
          '## Outputs','',
          '- experiments/poll_house_effect/results/house_effect_summary.csv',
          '- experiments/poll_house_effect/results/house_effect_choices.csv',
          '- experiments/poll_house_effect/results/house_effect_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
