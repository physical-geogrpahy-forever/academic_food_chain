#!/usr/bin/env python3
import runpy,csv,itertools
from pathlib import Path
from datetime import datetime,timezone,timedelta
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
PSTACK=ROOT/'experiments/poll_stack/run.py'
OUT=ROOT/'experiments/incumbency_shrink_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0430_incumbency-shrink-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

pns=runpy.run_path(str(PSTACK))
fns=pns['fns']; rows=fns['rows']; fitpred=fns['fitpred']
byrace=pns['byrace']; aggregate=pns['aggregate']; ELECTION=pns['ELECTION']
OUTER=[2014,2018,2022]

# Structural regularization is frozen at the stable values selected in all headline
# fullcycle-incumbency-era fits. Only incumbency and era shrinkage are re-selected here.
LL=256.0; LE=256.0; LN=0.0
L_INC=[64.,128.,256.,512.,1024.,2048.,4096.,8192.,16384.,65536.,1e9]
L_ERA=[64.,128.,256.,512.,1024.,2048.,4096.,8192.,16384.,65536.,1e9]

def blend(prior,cyc,rid):
    target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(byrace.get((cyc,str(rid)),[]),target,30,14)
    if agg is None:return float(prior)
    pm,neff,n=agg
    w=.75*neff/(neff+.5)
    return (1-w)*float(prior)+w*pm

def predict_cycle(cyc,li,lr):
    tr=[r for r in rows if int(r['cycle'])<cyc]
    te=[r for r in rows if int(r['cycle'])==cyc]
    if len(tr)<20 or not te:return []
    pp=fitpred(tr,te,'inc_era',LL,LE,LN,li,lr)
    out=[]
    for r,p in zip(te,pp):
        post=blend(p,cyc,r['race_id']); actual=float(r['y'])
        out.append({'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],
                    'actual':actual,'prior':float(p),'posterior':post,'correct':int((post>0)==(actual>0))})
    return out

cache={}
def get(cyc,li,lr):
    key=(cyc,li,lr)
    if key not in cache:cache[key]=predict_cycle(cyc,li,lr)
    return cache[key]

def score_history(cycles,li,lr):
    rr=[]
    for c in cycles:rr+=get(c,li,lr)
    if not rr:return (0,0,1e9)
    correct=sum(r['correct'] for r in rr)
    mae=float(np.mean([abs(r['posterior']-r['actual']) for r in rr]))
    return correct,len(rr),mae

choices=[];final=[]
for tc in OUTER:
    hc=[c for c in sorted(ELECTION) if 2010<=c<tc]
    cand=[]
    for li,lr in itertools.product(L_INC,L_ERA):
        ok,n,mae=score_history(hc,li,lr)
        # Winner count first; then lower MAE; then stronger shrinkage as conservative tie break.
        cand.append((-ok,mae,-min(li,1e9),-min(lr,1e9),li,lr,n))
    cand.sort()
    z=cand[0];li,lr=z[4],z[5]
    choices.append({'test_cycle':tc,'history_cycles':';'.join(map(str,hc)),'lambda_inc':li,'lambda_era':lr,
                    'history_correct':-z[0],'history_n':z[6],'history_accuracy_pct':100*(-z[0])/z[6] if z[6] else '',
                    'history_mae':z[1],
                    'top15':' | '.join(f'I{x[4]} R{x[5]} correct={-x[0]}/{x[6]} mae={x[1]:.2f}' for x in cand[:15])})
    final+=get(tc,li,lr)

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=final if scope=='combined' else [r for r in final if r['cycle']==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'accuracy_pct':100*ok/n})

# Oracle headroom within the same shrinkage family. Diagnostic only, never adoptable.
oracle=[]
for li,lr in itertools.product(L_INC,L_ERA):
    rr=[]
    for tc in OUTER:rr+=get(tc,li,lr)
    ok=sum(r['correct'] for r in rr)
    oracle.append((ok,li,lr,float(np.mean([abs(r['posterior']-r['actual']) for r in rr]))))
oracle.sort(key=lambda z:(-z[0],z[3],-min(z[1],1e9),-min(z[2],1e9)))
oracle_rows=[{'rank':i+1,'correct':x[0],'accuracy_pct':100*x[0]/99,'lambda_inc':x[1],'lambda_era':x[2],'mae':x[3]} for i,x in enumerate(oracle[:25])]

for fn,dat in [('shrink_summary.csv',summary),('shrink_choices.csv',choices),('shrink_predictions.csv',final),('shrink_oracle_top25.csv',oracle_rows)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dat[0].keys()));w.writeheader();w.writerows(dat)

wrong=[r for r in final if not r['correct']]
best=oracle_rows[0]
lines=['# Direction-first incumbency shrinkage experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Architecture remains incumbency-era. Structural ridge is frozen at local=256, econ=256, national=0.',
'- Only incumbency/out-party level shrinkage and era-interaction shrinkage are selected by earlier-cycle post-poll winner accuracy.',
'- Candidate lambdas extend to effectively zero incumbency contribution (1e9), allowing continuous shrinkage rather than all-on/all-off architecture selection.','',
'## Leakage-free outer result','',
'| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['accuracy_pct']:.1f}% |")
lines += ['','## Selected shrinkage before each outer cycle','',
'| test | history cycles | lambda inc | lambda era | history correct/N | history accuracy |',
'|---:|---|---:|---:|---:|---:|']
for r in choices:
    lines.append(f"| {r['test_cycle']} | {r['history_cycles']} | {r['lambda_inc']} | {r['lambda_era']} | {r['history_correct']}/{r['history_n']} | {r['history_accuracy_pct']:.1f}% |")
lines += ['','## Oracle headroom diagnostic','',
f"- Best possible fixed shrinkage pair on the outer 99, using outcomes only as a diagnostic: {best['correct']}/99 = {best['accuracy_pct']:.1f}% at lambda_inc={best['lambda_inc']}, lambda_era={best['lambda_era']}.",
'- Oracle values are not eligible for adoption. They only show whether this functional family has headroom beyond 94/99.','',
'## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: posterior={r['posterior']:.2f}, actual={r['actual']:.2f}")
lines += ['','## Benchmark','',
'- Current fixed incumbency-era + poll benchmark: 94/99 = 94.9%.',
'- Adopt only if leakage-free nested result exceeds 94/99.','',
'## Outputs','',
'- experiments/incumbency_shrink_direction/results/shrink_summary.csv',
'- experiments/incumbency_shrink_direction/results/shrink_choices.csv',
'- experiments/incumbency_shrink_direction/results/shrink_predictions.csv',
'- experiments/incumbency_shrink_direction/results/shrink_oracle_top25.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
