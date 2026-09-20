#!/usr/bin/env python3
import runpy,csv,itertools
from pathlib import Path
from datetime import timedelta,datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
STACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/oracle_poll_headroom/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0390_poll-blend-oracle-headroom.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ns=runpy.run_path(str(STACK))
hist=ns['hist'];byr=ns['byrace'];aggregate=ns['aggregate'];ELECTION=ns['ELECTION']
OUTER=[2014,2018,2022]
WINDOWS=[7,14,21,30,45,60,90]
HALF=[3,7,14,30,60,90,999]
WMAX=[0.4,0.5,0.6,0.7,0.75,0.8,0.9,1.0,1.1,1.25]
K=[0.01,0.05,0.1,0.25,0.5,1,2,4,8]

outer=[r for r in hist if int(r['cycle']) in OUTER]

def evalp(params,subset):
    window,hl,wmax,k=params
    ok=0;details=[]
    for r in subset:
        target=ELECTION[int(r['cycle'])]-timedelta(days=45)
        agg=aggregate(byr.get((int(r['cycle']),str(r['race_id'])),[]),target,window,hl)
        prior=float(r['prior'])
        if agg is None:
            post=prior;pm='';neff=0
        else:
            pm,neff,n=agg;w=wmax*neff/(neff+k);post=(1-w)*prior+w*pm
        corr=int((post>0)==(float(r['actual'])>0));ok+=corr
        details.append((r,post,pm,neff,corr))
    return ok,details

grid=[]
for p in itertools.product(WINDOWS,HALF,WMAX,K):
    ok,_=evalp(p,outer)
    grid.append((ok,p))
grid.sort(key=lambda z:(-z[0],abs(z[1][2]-.75),abs(z[1][3]-.5),z[1][0],z[1][1]))
best_ok,best=grid[0]
_,details=evalp(best,outer)

cycle=[]
for tc in OUTER:
    rr=[r for r in outer if int(r['cycle'])==tc]
    vals=[]
    for p in itertools.product(WINDOWS,HALF,WMAX,K):
        ok,_=evalp(p,rr);vals.append((ok,p))
    vals.sort(key=lambda z:-z[0])
    cycle.append({'cycle':tc,'max_correct':vals[0][0],'n':len(rr),'params':str(vals[0][1])})

top=[{'rank':i+1,'correct':z[0],'accuracy_pct':100*z[0]/len(outer),
      'window':z[1][0],'half_life':z[1][1],'w_max':z[1][2],'k':z[1][3]} for i,z in enumerate(grid[:50])]
changes=[]
for r,post,pm,neff,corr in details:
    # compare to fixed 30,14,.75,.5
    _,bd=evalp((30,14,.75,.5),[r]);bc=bd[0][4]
    if bc!=corr:
        changes.append({'cycle':r['cycle'],'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                        'actual':r['actual'],'best_posterior':post,'best_correct':corr,'fixed_correct':bc})

for fn,data in [('oracle_top50.csv',top),('oracle_cycle_max.csv',cycle),('oracle_best_changes.csv',changes)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()) if data else ['none']);w.writeheader();w.writerows(data)

lines=['# Poll-blend oracle headroom audit','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- This is diagnostic only. Outer 2014/2018/2022 outcomes are used to measure theoretical headroom, so these parameters are NOT eligible for adoption.',
'- Purpose: determine whether the current poll-blend functional form can ever exceed the 94/99 fixed benchmark.','',
'## Oracle maximum','',
f'- Maximum correct within the searched poll-blend family: {best_ok}/{len(outer)} = {100*best_ok/len(outer):.1f}%.',
f'- Oracle-best parameters: window={best[0]}, half-life={best[1]}, w_max={best[2]}, k={best[3]}.','',
'## Per-cycle oracle maxima','']
for r in cycle:lines.append(f"- {r['cycle']}: {r['max_correct']}/{r['n']} with {r['params']}")
lines += ['','## Correctness changes vs fixed 94/99 blend','']
for r in changes:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: fixed {'correct' if r['fixed_correct'] else 'wrong'} -> oracle {'correct' if r['best_correct'] else 'wrong'}")
lines += ['','## Interpretation','',
'If the oracle maximum is still 94/99, further poll-weight tuning has no structural headroom. If it is higher, the next task is to find a leakage-free training rule that selects a similar regime, not to adopt the oracle parameters themselves.','',
'## Outputs','',
'- experiments/oracle_poll_headroom/results/oracle_top50.csv',
'- experiments/oracle_poll_headroom/results/oracle_cycle_max.csv',
'- experiments/oracle_poll_headroom/results/oracle_best_changes.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
