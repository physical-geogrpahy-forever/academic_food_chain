#!/usr/bin/env python3
import runpy,csv
from pathlib import Path
from datetime import timedelta,datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/outparty_closepoll_pvi/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0450_outparty-closepoll-pvi-rule.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
struct={(int(r['cycle']),str(r['race_id'])):r for r in fns['rows']}
pns=runpy.run_path(str(STACK))
hist=pns['hist'];byrace=pns['byrace'];aggregate=pns['aggregate'];ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]
THRESH=[-1,0.25,0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0,5.0]

def enrich(r):
    s=struct.get((int(r['cycle']),str(r['race_id'])))
    if s is None:return None
    cyc=int(r['cycle']);target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    prior=float(r['prior'])
    if agg is None:
        pm=None;neff=0;n=0;post=prior
    else:
        pm,neff,n=agg;w=.75*neff/(neff+.5);post=(1-w)*prior+w*pm
    return {
      'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],'actual':float(r['actual']),
      'prior':prior,'poll':pm,'neff':neff,'poll_count':n,'posterior':post,
      'pvi':float(s['pvi']),'outparty':float(s['outparty'])
    }

data=[x for x in (enrich(r) for r in hist) if x is not None]

def pred(r,t):
    base=r['posterior']>0
    if t<0 or r['outparty']==0 or r['poll'] is None:return base,0
    # Apply only when the 45-day poll is genuinely close.
    if abs(float(r['poll']))>t:return base,0
    # Out-party means the incumbent's party is opposite the state's PVI direction.
    # In a close poll, defer to state partisan direction rather than the incumbency-heavy posterior.
    pvi_dir=r['pvi']>0
    return pvi_dir, int(pvi_dir!=base)

def score(dat,t):
    ok=flips=0
    changed=[]
    for r in dat:
        p,f=pred(r,t);good=int(p==(r['actual']>0));ok+=good;flips+=f
        if f:changed.append((r,good))
    return ok,flips,changed

def choose(train):
    grid=[]
    for t in THRESH:
        ok,flips,_=score(train,t)
        # Primary correct count, then fewer flips, then smaller threshold; -1 = none.
        complexity=0 if t<0 else t
        grid.append((-ok,flips,complexity,t))
    grid.sort()
    return grid[0],grid

preds=[];choices=[]
for tc in OUTER:
    tr=[r for r in data if r['cycle']<tc]
    te=[r for r in data if r['cycle']==tc]
    best,grid=choose(tr)
    negok,trflips,comp,t=best
    choices.append({'test_cycle':tc,'threshold_abs_poll_pctpt':t,'train_n':len(tr),
                    'train_correct':-negok,'train_accuracy_pct':100*(-negok)/len(tr),'train_flips':trflips,
                    'grid':' | '.join(f't={z[3]} correct={-z[0]}/{len(tr)} flips={z[1]}' for z in grid)})
    for r in te:
        p,f=pred(r,t);base=r['posterior']>0;act=r['actual']>0
        preds.append({**r,'threshold':t,'override_applied':f,
                      'baseline_correct':int(base==act),'adjusted_correct':int(p==act),
                      'adjusted_direction':'D' if p else 'R'})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=preds if scope=='combined' else [r for r in preds if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'overrides':sum(r['override_applied'] for r in rr)})

for fn,arr in [('closepoll_summary.csv',summary),('closepoll_choices.csv',choices),('closepoll_predictions.csv',preds)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

changed=[r for r in preds if r['baseline_correct']!=r['adjusted_correct']]
lines=['# Out-party incumbent close-poll PVI override','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Baseline: fixed 45-day poll blend, 94/99.',
'- Rule applies only to races with an out-party incumbent and a 45-day poll margin whose absolute value is below a threshold.',
'- If eligible, direction is set to the state PVI direction rather than the incumbency-heavy posterior.',
'- The threshold, including a no-rule option, is selected only from cycles before each outer test cycle by winner count.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['overrides']} |")
lines += ['','## Selected threshold','',
'| test | threshold | train N | train correct | train accuracy | train flips |',
'|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['threshold_abs_poll_pctpt']} | {r['train_n']} | {r['train_correct']} | {r['train_accuracy_pct']:.1f}% | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} race {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, poll={r['poll']}, PVI={r['pvi']:.2f}, threshold={r['threshold']}")
lines += ['','## Decision','',
'- Adopt only if combined adjusted accuracy exceeds 94/99 under this strict forward-selection protocol.',
'- This rule is intentionally narrow: it does not alter non-out-party races or out-party races whose 45-day polls show a clear lead.','',
'## Outputs','',
'- experiments/outparty_closepoll_pvi/results/closepoll_summary.csv',
'- experiments/outparty_closepoll_pvi/results/closepoll_choices.csv',
'- experiments/outparty_closepoll_pvi/results/closepoll_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
