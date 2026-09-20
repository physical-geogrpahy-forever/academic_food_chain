#!/usr/bin/env python3
import runpy,csv,math,itertools
from pathlib import Path
from datetime import timedelta,datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/outparty_closepoll_split/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0510_split-closepoll-selector.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

fns=runpy.run_path(str(FULL))
struct={(int(r['cycle']),str(r['race_id'])):r for r in fns['rows']}
pns=runpy.run_path(str(STACK))
hist=pns['hist'];byrace=pns['byrace'];aggregate=pns['aggregate'];ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]

TD=[-1,0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0,5.0]
TA=[-1,0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0,5.0]
PMIN=[0,2,5,10,15,20]

def enrich(r):
    s=struct.get((int(r['cycle']),str(r['race_id'])))
    if s is None:return None
    cyc=int(r['cycle']);target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    prior=float(r['prior'])
    if agg is None:pm=None;post=prior
    else:
        pm,neff,n=agg;w=.75*neff/(neff+.5);post=(1-w)*prior+w*pm
    return {'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],'actual':float(r['actual']),
            'posterior':post,'poll':pm,'pvi':float(s['pvi']),'outparty':float(s['outparty'])}
data=[x for x in (enrich(r) for r in hist) if x is not None]

def signed(v):
    return 1 if v>0 else (-1 if v<0 else 0)

def margin(r,td,ta,pmin):
    base=float(r['posterior'])
    if r['outparty']==0 or r['poll'] is None:return base,0,'none'
    ps=signed(float(r['poll']));vs=signed(float(r['pvi']))
    agree=(ps==vs and ps!=0)
    ap=abs(float(r['poll']));av=abs(float(r['pvi']))
    use=False;reason='none'
    if not agree and td>=0 and ap<=td:
        use=True;reason='disagree'
    elif agree and ta>=0 and ap<=ta and av>=pmin:
        use=True;reason='agree_strong_pvi'
    if not use:return base,0,reason
    q=(1 if r['pvi']>0 else -1)*abs(base)
    return q,int((q>0)!=(base>0)),reason

def metrics(dat,params):
    td,ta,pmin=params
    ok=flips=0;mae=br=ll=0.
    for r in dat:
        q,f,_=margin(r,td,ta,pmin);y=1. if r['actual']>0 else 0.
        ok+=int((q>0)==(r['actual']>0));flips+=f;mae+=abs(q-r['actual'])
        p=1/(1+math.exp(-max(min(q/6.0,30),-30)));p=min(max(p,1e-9),1-1e-9)
        br+=(p-y)**2;ll+=-(y*math.log(p)+(1-y)*math.log(1-p))
    n=len(dat)
    return ok,br/n,ll/n,mae/n,flips

def choose(train):
    grid=[]
    for params in itertools.product(TD,TA,PMIN):
        ok,br,ll,mae,flips=metrics(train,params)
        td,ta,pmin=params
        width=(0 if td<0 else td)+(0 if ta<0 else ta)
        grid.append((-ok,br,ll,mae,flips,width,-pmin,td,ta,pmin))
    grid.sort()
    return grid[0],grid[:25]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in data if r['cycle']<tc];te=[r for r in data if r['cycle']==tc]
    best,grid=choose(tr)
    negok,br,ll,mae,trflips,width,npmin,td,ta,pmin=best
    choices.append({'test_cycle':tc,'threshold_disagree':td,'threshold_agree':ta,'min_abs_pvi_agree':pmin,
                    'train_n':len(tr),'train_correct':-negok,'train_accuracy_pct':100*(-negok)/len(tr),
                    'train_brier':br,'train_logloss':ll,'train_mae':mae,'train_flips':trflips,
                    'top25':' | '.join(f'd={z[7]} a={z[8]} pmin={z[9]} correct={-z[0]}/{len(tr)} br={z[1]:.4f} mae={z[3]:.2f} flips={z[4]}' for z in grid)})
    for r in te:
        q,f,reason=margin(r,td,ta,pmin);base=r['posterior'];act=r['actual']
        pred.append({**r,'threshold_disagree':td,'threshold_agree':ta,'min_abs_pvi_agree':pmin,
                     'adjusted_margin':q,'override_applied':f,'override_reason':reason,
                     'baseline_correct':int((base>0)==(act>0)),'adjusted_correct':int((q>0)==(act>0))})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'overrides':sum(r['override_applied'] for r in rr)})

for fn,arr in [('split_summary.csv',summary),('split_choices.csv',choices),('split_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
wrong=[r for r in pred if not r['adjusted_correct']]
lines=['# Split close-poll selector: poll-PVI agreement aware','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: winner-direction accuracy.',
'- The override threshold is estimated separately when poll and PVI disagree versus agree.',
'- When poll and PVI agree, override additionally requires a minimum absolute PVI.',
'- All parameters for each outer cycle are selected only from earlier cycles.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | overrides |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['overrides']} |")
lines += ['','## Selected parameters','',
'| test | disagree threshold | agree threshold | min abs PVI if agree | train accuracy | Brier | MAE | flips |',
'|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['threshold_disagree']} | {r['threshold_agree']} | {r['min_abs_pvi_agree']} | {r['train_accuracy_pct']:.1f}% | {r['train_brier']:.4f} | {r['train_mae']:.2f} | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, reason={r['override_reason']}, poll={r['poll']}, PVI={r['pvi']:.2f}")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['cycle']} {r['state_abbrev']}: actual={r['actual']:.2f}, posterior={r['posterior']:.2f}, poll={r['poll']}, PVI={r['pvi']:.2f}")
lines += ['','## Benchmark','',
'- Current accepted clean nested benchmark: 96/99 = 97.0%.',
'- Adopt this split selector only if it exceeds 96/99 under the same 99-race universe.','',
'## Outputs','',
'- experiments/outparty_closepoll_split/results/split_summary.csv',
'- experiments/outparty_closepoll_split/results/split_choices.csv',
'- experiments/outparty_closepoll_split/results/split_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
