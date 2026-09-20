#!/usr/bin/env python3
import csv, itertools
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_stack/run.py'
PRES=ROOT/'data/processed/presidential_state_lean.csv'
OUT=ROOT/'experiments/state_trend_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0400_state-partisan-trend-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

import runpy
ns=runpy.run_path(str(BASE))
hist=ns['hist']

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
pres=load(PRES)
lean={}
years=set()
for r in pres:
    try:
        y=int(r['cycle']);st=r['state_abbrev'];v=float(r['lean_vs_national_pctpt'])
    except:continue
    lean[(y,st)]=v;years.add(y)
years=sorted(years)

def state_info(cycle,state):
    ys=[y for y in years if y<cycle and (y,state) in lean]
    if len(ys)<2:return None
    recent,older=ys[-1],ys[-2]
    rv=lean[(recent,state)];ov=lean[(older,state)]
    return recent,older,rv,ov,rv-ov

data=[]
for r in hist:
    info=state_info(int(r['cycle']),r['state_abbrev'])
    if info is None:continue
    recent,older,rv,ov,tr=info
    x=dict(r)
    x.update({'recent_pres_year':recent,'older_pres_year':older,'recent_lean':rv,'older_lean':ov,'state_trend':tr})
    data.append(x)

OUTER=[2014,2018,2022]
GAMMA=[-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,1.5,2]
THRESH=[2,3,4,5,6,8,10,15,20,999]
TRENDMIN=[0,1,2,3,5,8,12]

def predict(r,gamma,post_thr,trend_min):
    post=float(r['posterior'])
    tr=float(r['state_trend'])
    if abs(post)>post_thr or abs(tr)<trend_min:return post,0
    q=post+gamma*tr
    return q,int((q>0)!=(post>0))

def evalset(dat,gamma,post_thr,trend_min):
    ok=flips=0
    for r in dat:
        q,f=predict(r,gamma,post_thr,trend_min)
        ok+=int((q>0)==(float(r['actual'])>0));flips+=f
    return ok,flips

choices=[];pred=[]
for tc in OUTER:
    train=[r for r in data if int(r['cycle'])<tc]
    test=[r for r in data if int(r['cycle'])==tc]
    cand=[]
    for gamma,pt,tm in itertools.product(GAMMA,THRESH,TRENDMIN):
        ok,flips=evalset(train,gamma,pt,tm)
        complexity=abs(gamma)+(0 if pt==999 else 1)+tm/20
        cand.append((-ok,flips,complexity,gamma,pt,tm))
    cand.sort()
    z=cand[0];ok=-z[0];flips=z[1];gamma=z[3];pt=z[4];tm=z[5]
    choices.append({'test_cycle':tc,'gamma':gamma,'posterior_threshold':pt,'trend_min':tm,
                    'train_n':len(train),'train_correct':ok,'train_accuracy_pct':100*ok/len(train),
                    'train_flips':flips,'top15':' | '.join(f'g{q[3]} p{q[4]} t{q[5]} correct={-q[0]} flips={q[1]}' for q in cand[:15])})
    for r in test:
        q,f=predict(r,gamma,pt,tm)
        act=float(r['actual']);post=float(r['posterior'])
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':act,
                     'baseline_posterior':post,'state_trend':r['state_trend'],'recent_lean':r['recent_lean'],'older_lean':r['older_lean'],
                     'adjusted_posterior':q,'direction_flip':f,
                     'baseline_correct':int((post>0)==(act>0)),'adjusted_correct':int((q>0)==(act>0)),
                     'gamma':gamma,'posterior_threshold':pt,'trend_min':tm})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'direction_flips':sum(r['direction_flip'] for r in rr)})

for fn,dat in [('state_trend_summary.csv',summary),('state_trend_choices.csv',choices),('state_trend_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dat[0].keys()));w.writeheader();w.writerows(dat)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# State partisan trend direction experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Baseline: fixed 45-day poll blend, 94/99.',
'- State trend = most recent completed presidential state lean minus the preceding presidential state lean.',
'- This adds information that the 0.67/0.33 PVI average can damp when a state is moving quickly.',
'- Gamma, posterior threshold, and minimum trend magnitude are selected only from cycles earlier than each outer test cycle.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected trend rule','',
'| test | gamma | posterior threshold | minimum | train accuracy | train flips |',
'|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['gamma']} | {r['posterior_threshold']} | {r['trend_min']} | {r['train_accuracy_pct']:.1f}% | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> trend {'correct' if r['adjusted_correct'] else 'wrong'}, trend={r['state_trend']:.2f}, post {r['baseline_posterior']:.2f}->{r['adjusted_posterior']:.2f}")
lines += ['','## Decision','',
'Adopt only if historical winner-direction accuracy exceeds 94/99 under chronological OOS.','',
'## Outputs','',
'- experiments/state_trend_direction/results/state_trend_summary.csv',
'- experiments/state_trend_direction/results/state_trend_choices.csv',
'- experiments/state_trend_direction/results/state_trend_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
