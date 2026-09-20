#!/usr/bin/env python3
import runpy, csv
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
POLLSTACK=ROOT/'experiments/poll_stack/run.py'
SEATSCRIPT=ROOT/'experiments/seat_pvi_tuning/run.py'
OUT=ROOT/'experiments/prior_ensemble/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0370_prior-ensemble-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

# Historical rolling inc-era prior + fixed poll ingredients.
ps=runpy.run_path(str(POLLSTACK))
hist=ps['hist']

# Historical rolling PVI/SameSeat prior machinery.
ss=runpy.run_path(str(SEATSCRIPT))
base_rows=ss['base_rows']
seat_tune=ss['tune']
seat_fit=ss['fitpred']

WEIGHTS=[0.0,0.1,0.25,0.5,0.75,0.9,1.0]
OUTER=[2014,2018,2022]
WMAX=.75;K=.5

# Generate rolling seat-model prior predictions for every possible cycle.
seat_hist={}
cycles=sorted(set(int(r['cycle']) for r in base_rows))
for cyc in cycles:
    tr=[r for r in base_rows if int(r['cycle'])<cyc]
    te=[r for r in base_rows if int(r['cycle'])==cyc]
    if len(tr)<25 or not te:
        continue
    try:
        best,_=seat_tune(tr)
    except Exception:
        continue
    sc,w,mode,lp,ll,le,ln,folds=best
    pp=seat_fit(tr,te,w,mode,lp,ll,le,ln)
    for r,p in zip(te,pp):
        seat_hist[(cyc,str(r['race_id']))]=float(p)

# Keep only races for which both rolling priors exist.
data=[]
for r in hist:
    key=(int(r['cycle']),str(r['race_id']))
    if key not in seat_hist:
        continue
    data.append({**r,'seat_prior':seat_hist[key]})

def posterior(r,w):
    prior=(1-w)*float(r['prior'])+w*float(r['seat_prior'])
    if r['poll_count']<=0 or r['poll']=='':
        return prior
    pw=WMAX*float(r['neff'])/(float(r['neff'])+K)
    return (1-pw)*prior+pw*float(r['poll'])

def stats(dat,w):
    ok=0;mae=0.0
    for r in dat:
        p=posterior(r,w);a=float(r['actual'])
        ok+=int((p>0)==(a>0));mae+=abs(p-a)
    return ok,mae/len(dat)

choices=[];pred=[]
for tc in OUTER:
    train=[r for r in data if int(r['cycle'])<tc]
    test=[r for r in data if int(r['cycle'])==tc]
    cand=[]
    for w in WEIGHTS:
        ok,mae=stats(train,w)
        # Primary: correct winners. Tie-break: lower MAE, then closer to 0.25 only after performance ties.
        cand.append((-ok,mae,abs(w-.25),w))
    cand.sort()
    z=cand[0];w=z[3]
    choices.append({'test_cycle':tc,'seat_prior_weight':w,'inc_prior_weight':1-w,'train_n':len(train),
                    'train_correct':-z[0],'train_accuracy_pct':100*(-z[0])/len(train),'train_mae':z[1],
                    'top_weights':' | '.join(f'w={q[3]} correct={-q[0]} mae={q[1]:.2f}' for q in cand)})
    for r in test:
        p=posterior(r,w);a=float(r['actual'])
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':a,
                     'inc_prior':r['prior'],'seat_prior':r['seat_prior'],'seat_weight':w,
                     'poll':r['poll'],'n_eff':r['neff'],'posterior':p,'correct':int((p>0)==(a>0))})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if int(r['test_cycle'])==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n})

for fn,arr in [('ensemble_summary.csv',summary),('ensemble_choices.csv',choices),('ensemble_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

wrong=[r for r in pred if not r['correct']]
comb=summary[0]
lines=['# Rolling prior-ensemble direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Candidate priors: current fullcycle incumbency-era prior and nested PVI/SameSeat prior.',
       '- Same fixed 45-day poll layer is applied after prior ensembling.',
       '- Ensemble weight for each outer cycle is selected only from earlier cycles.',
       '- Primary selection criterion is winner-direction correct count; MAE is only the first tie-breaker.','',
       '## Result','',
       '| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Selected ensemble weights','',
          '| test | inc prior weight | seat prior weight | training rows | training accuracy | training MAE |',
          '|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['inc_prior_weight']:.2f} | {r['seat_prior_weight']:.2f} | {r['train_n']} | {r['train_accuracy_pct']:.1f}% | {r['train_mae']:.2f} |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: posterior={r['posterior']:.2f}, actual={r['actual']:.2f}")
lines += ['','## Benchmarks','',
          '- Current validated fixed-blend benchmark: 94/99 = 94.9%.',
          '- Descriptive 75% inc-era + 25% seat-prior blend: 95/99, but that weight was discovered on the outer sample and is not adopted unless rolling selection reproduces the gain.','',
          '## Decision','',
          f"- Rolling-selected ensemble result: {comb['correct']}/{comb['n']} = {comb['direction_accuracy_pct']:.1f}%.",
          '- Adopt only if it exceeds 94/99.','',
          '## Outputs','',
          '- experiments/prior_ensemble/results/ensemble_summary.csv',
          '- experiments/prior_ensemble/results/ensemble_choices.csv',
          '- experiments/prior_ensemble/results/ensemble_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
