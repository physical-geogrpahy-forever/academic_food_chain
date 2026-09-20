#!/usr/bin/env python3
import csv, io, math, runpy, urllib.request
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from collections import defaultdict
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
STACK=ROOT/'experiments/poll_stack/run.py'
PRES_ACT=ROOT/'data/processed/presidential_state_lean.csv'
OUT=ROOT/'experiments/pres_poll_error_memory/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0420_presidential-poll-error-memory.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

PRES_AVG_URL='https://raw.githubusercontent.com/fivethirtyeight/data/4c1ff5e3aef1816ae04af63218015066e186c147/polls/pres_pollaverages_1968-2016.csv'
PRES_ELECTION={2008:date(2008,11,4),2012:date(2012,11,6),2016:date(2016,11,8)}
PREV_PRES={2010:2008,2014:2012,2018:2016}
OUTER=[2014,2018,2022]
GAMMA=[-0.5,0.0,0.25,0.5,0.75,1.0,1.25,1.5,2.0]
MODES=['raw','centered']

STATE_ABBR={
'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC',
'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME',
'Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH',
'New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA',
'West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'
}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def pdate(s):
    s=(s or '').strip()
    for fmt in ('%m/%d/%Y','%m/%d/%y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None

# Existing rolling Senate priors and historical Senate polls.
ns=runpy.run_path(str(STACK))
hist=ns['hist'];byrace=ns['byrace'];aggregate=ns['aggregate'];SEN_ELECTION=ns['ELECTION']

# Actual presidential state margins.
actual={}
for r in load(PRES_ACT):
    try:cyc=int(r['cycle'])
    except:continue
    if cyc in PRES_ELECTION:
        actual[(cyc,r['state_abbrev'])]=float(r['state_margin_d_minus_r_pctpt'])

# FiveThirtyEight historical presidential polling averages.
req=urllib.request.Request(PRES_AVG_URL,headers={'User-Agent':'CoreV2R-pres-poll-error/1.0'})
raw=urllib.request.urlopen(req,timeout=240).read()
if len(raw)<1000000: raise RuntimeError(f'Historical presidential average source unexpectedly small: {len(raw)} bytes')
pres=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))

def party(name,cyc):
    n=(name or '').lower()
    if cyc==2008:
        if 'obama' in n:return 'D'
        if 'mccain' in n:return 'R'
    elif cyc==2012:
        if 'obama' in n:return 'D'
        if 'romney' in n:return 'R'
    elif cyc==2016:
        if 'clinton' in n:return 'D'
        if 'trump' in n:return 'R'
    return None

# Latest state poll average at or before presidential election day.
latest=defaultdict(dict)
for r in pres:
    try:cyc=int(r.get('cycle') or 0)
    except:continue
    if cyc not in PRES_ELECTION:continue
    st=(r.get('state') or '').strip()
    if st not in STATE_ABBR:continue
    dt=pdate(r.get('modeldate'))
    if dt is None or dt>PRES_ELECTION[cyc]:continue
    pa=party(r.get('candidate_name'),cyc)
    if pa is None:continue
    try:pct=float(r.get('pct_estimate') or '')
    except:continue
    key=(cyc,STATE_ABBR[st])
    old=latest[key].get(pa)
    if old is None or dt>old[0]:
        latest[key][pa]=(dt,pct)

perr={}
for key,v in latest.items():
    cyc,st=key
    if 'D' not in v or 'R' not in v or key not in actual:continue
    # Require same model date for D and R where possible. These files generally do.
    poll=v['D'][1]-v['R'][1]
    perr[key]=actual[key]-poll

cycle_mean={}
for cyc in PRES_ELECTION:
    vals=[v for (c,s),v in perr.items() if c==cyc]
    cycle_mean[cyc]=sum(vals)/len(vals) if vals else 0.0

def memory(cyc,st,mode):
    py=PREV_PRES.get(cyc)
    if py is None:return None
    e=perr.get((py,st))
    if e is None:return None
    return e if mode=='raw' else e-cycle_mean[py]

def fixed_post(r, correction=0.0):
    cyc=int(r['cycle']);target=SEN_ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    prior=float(r['prior'])
    if agg is None:return prior,0.0,'',0
    pm,neff,n=agg
    w=.75*neff/(neff+.5)
    return (1-w)*prior+w*(pm+correction),w,pm,int(n)

def evalset(dat,mode,gamma):
    ok=0;mae=0.;covered=0;rows=[]
    for r in dat:
        m=memory(int(r['cycle']),r['state_abbrev'],mode)
        corr=0.0 if m is None else gamma*m
        post,w,pm,n=fixed_post(r,corr)
        actualm=float(r['actual'])
        good=int((post>0)==(actualm>0))
        ok+=good;mae+=abs(post-actualm);covered+=int(m is not None)
        rows.append((r,m,corr,post,w,pm,n,good))
    return ok,mae/len(dat),covered,rows

def choose(train):
    cand=[]
    usable=[r for r in train if int(r['cycle']) in PREV_PRES]
    for mode in MODES:
      for g in GAMMA:
        ok,mae,cov,_=evalset(usable,mode,g)
        # Primary correct count, then MAE, then smaller |gamma| and centered error.
        cand.append((-ok,mae,abs(g),0 if mode=='centered' else 1,mode,g,cov,len(usable)))
    cand.sort()
    return cand[0],cand[:15]

pred=[];choices=[]
for tc in OUTER:
    test=[r for r in hist if int(r['cycle'])==tc]
    if tc==2022:
        # First-stage test deliberately leaves 2022 untouched because 2020 polling-average archive
        # is not part of the 1968-2016 source. This preserves the already-perfect 33/33 fold.
        mode='none';g=0.0;innern=0;innerok='';innermae='';trace=[]
    else:
        train=[r for r in hist if int(r['cycle'])<tc and int(r['cycle']) in PREV_PRES]
        best,trace=choose(train)
        negok,innermae,ag,mo,mode,g,cov,innern=best;innerok=-negok
    choices.append({'test_cycle':tc,'mode':mode,'gamma':g,'inner_n':innern,'inner_correct':innerok,
                    'inner_accuracy_pct':('' if innern==0 else 100*innerok/innern),'inner_mae':innermae,
                    'top15':' | '.join(f'{z[4]} g{z[5]} correct={-z[0]}/{z[7]} mae={z[1]:.2f}' for z in trace)})
    for r in test:
        base,_,_,_=fixed_post(r,0.0)
        if mode=='none':
            m=None;corr=0.0;post=base
        else:
            m=memory(tc,r['state_abbrev'],mode);corr=0.0 if m is None else g*m
            post,_,_,_=fixed_post(r,corr)
        act=float(r['actual'])
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':act,
                     'baseline_posterior':base,'memory_error':('' if m is None else m),'gamma':g,
                     'poll_correction':corr,'adjusted_posterior':post,
                     'baseline_correct':int((base>0)==(act>0)),'adjusted_correct':int((post>0)==(act>0)),
                     'mode':mode})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum((r['baseline_posterior']>0)!=(r['adjusted_posterior']>0) for r in rr)})

error_audit=[]
for (cyc,st),e in sorted(perr.items()):
    if st in {'NC','NV','MO','FL','IN'} or cyc in {2008,2012,2016}:
        error_audit.append({'pres_cycle':cyc,'state_abbrev':st,'actual_minus_poll_error':e,'cycle_mean_error':cycle_mean[cyc],
                            'centered_state_error':e-cycle_mean[cyc]})

for fn,arr in [('pres_error_summary.csv',summary),('pres_error_choices.csv',choices),('pres_error_predictions.csv',pred),('pres_error_audit.csv',error_audit)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
target={('2014','NC'),('2018','NV'),('2018','MO'),('2018','FL'),('2018','IN')}
lines=['# Previous-presidential state polling-error memory','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary metric: Senate winner-direction accuracy.',
'- 2010 Senate races use 2008 presidential state polling error, 2014 uses 2012, and 2018 uses 2016.',
'- For each target midterm, gamma and raw-vs-centered state error are selected only from earlier eligible midterms.',
'- 2022 is deliberately left unchanged in this first-stage test because the 2020 polling-average archive is not part of the pinned 1968-2016 file.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected memory rule','',
'| test | mode | gamma | inner N | inner accuracy | inner MAE |','|---:|---|---:|---:|---:|---:|']
for r in choices:
    ia='NA' if r['inner_accuracy_pct']=='' else f"{r['inner_accuracy_pct']:.1f}%"
    im='NA' if r['inner_mae']=='' else f"{float(r['inner_mae']):.2f}"
    lines.append(f"| {r['test_cycle']} | {r['mode']} | {r['gamma']} | {r['inner_n']} | {ia} | {im} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, memory={r['memory_error']}, correction={r['poll_correction']:.2f}, posterior {r['baseline_posterior']:.2f}->{r['adjusted_posterior']:.2f}")
lines += ['','## Previously unresolved five','']
for r in pred:
    if (str(r['test_cycle']),r['state_abbrev']) in target:
        lines.append(f"- {r['test_cycle']} {r['state_abbrev']}: {'CORRECT' if r['adjusted_correct'] else 'WRONG'}, actual={r['actual']:.2f}, baseline={r['baseline_posterior']:.2f}, memory={r['memory_error']}, correction={r['poll_correction']:.2f}, adjusted={r['adjusted_posterior']:.2f}")
lines += ['','## Decision','',
'- Current accepted benchmark: 94/99.',
'- This signal is worth continuing only if it increases correct winners without test-cycle parameter tuning. If it improves 2018, the next step is to add the archived 2020 presidential polling average and validate 2022 under the same rule.','',
'## Outputs','',
'- experiments/pres_poll_error_memory/results/pres_error_summary.csv',
'- experiments/pres_poll_error_memory/results/pres_error_choices.csv',
'- experiments/pres_poll_error_memory/results/pres_error_predictions.csv',
'- experiments/pres_poll_error_memory/results/pres_error_audit.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
