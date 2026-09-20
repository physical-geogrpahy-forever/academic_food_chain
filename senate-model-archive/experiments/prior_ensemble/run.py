#!/usr/bin/env python3
import runpy, csv
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
POLLSTACK=ROOT/'experiments/poll_stack/run.py'
PRES=ROOT/'data/processed/presidential_state_lean.csv'
OUT=ROOT/'experiments/prior_ensemble/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0370_prior-ensemble-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ps=runpy.run_path(str(POLLSTACK))
hist=ps['hist']; rows=ps['rows']

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
pres=load(PRES)
lean={}; years=set()
for r in pres:
    try:y=int(r['cycle']);st=r['state_abbrev'];v=float(r['lean_vs_national_pctpt'])
    except:continue
    lean[(y,st)]=v;years.add(y)
years=sorted(years)

def recent_lean(cyc,st):
    ys=[y for y in years if y<cyc and (y,st) in lean]
    return None if not ys else lean[(ys[-1],st)]

# Frozen secondary-prior architecture selected in the 2014 fold using only pre-2014 inner validation:
# recent presidential lean weight=1.0, raw SameSeat, ridge PVI=4, local=64, econ=4096, national=0.
FEATURES=['recent_lean','same_last','same_gap','econ','national']
PEN=np.array([0.,4.,64.,64.,4096.,0.])

srows=[]
for r in rows:
    rl=recent_lean(int(r['cycle']),r['state_abbrev'])
    if rl is None:continue
    x=dict(r);x['recent_lean']=rl;srows.append(x)

def design(dat,stats=None):
    X=np.array([[float(r[f]) for f in FEATURES] for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def seat_predict(tr,te):
    X,st=design(tr);Xt,_=design(te,st);y=np.array([float(r['y']) for r in tr])
    b=np.linalg.pinv(X.T@X+np.diag(PEN))@(X.T@y)
    return Xt@b

seat_hist={}
for cyc in sorted(set(int(r['cycle']) for r in srows)):
    tr=[r for r in srows if int(r['cycle'])<cyc];te=[r for r in srows if int(r['cycle'])==cyc]
    if len(tr)<25 or not te:continue
    pp=seat_predict(tr,te)
    for r,p in zip(te,pp):seat_hist[(cyc,str(r['race_id']))]=float(p)

data=[]
for r in hist:
    key=(int(r['cycle']),str(r['race_id']))
    if key in seat_hist:data.append({**r,'seat_prior':seat_hist[key]})

WEIGHTS=[0.0,0.1,0.25,0.5,0.75,0.9,1.0]
OUTER=[2014,2018,2022];WMAX=.75;K=.5

def posterior(r,w):
    prior=(1-w)*float(r['prior'])+w*float(r['seat_prior'])
    if r['poll_count']<=0 or r['poll']=='':return prior
    pw=WMAX*float(r['neff'])/(float(r['neff'])+K)
    return (1-pw)*prior+pw*float(r['poll'])
def stat(dat,w):
    ok=0;mae=0.
    for r in dat:
        p=posterior(r,w);a=float(r['actual']);ok+=int((p>0)==(a>0));mae+=abs(p-a)
    return ok,mae/len(dat)

choices=[];pred=[]
for tc in OUTER:
    train=[r for r in data if int(r['cycle'])<tc];test=[r for r in data if int(r['cycle'])==tc]
    cand=[]
    for w in WEIGHTS:
        ok,mae=stat(train,w)
        cand.append((-ok,mae,abs(w-.25),w))
    cand.sort();z=cand[0];w=z[3]
    choices.append({'test_cycle':tc,'seat_prior_weight':w,'inc_prior_weight':1-w,'train_n':len(train),
                    'train_correct':-z[0],'train_accuracy_pct':100*(-z[0])/len(train),'train_mae':z[1],
                    'top_weights':' | '.join(f'w={q[3]} correct={-q[0]} mae={q[1]:.2f}' for q in cand)})
    for r in test:
        p=posterior(r,w);a=float(r['actual'])
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':a,
                     'inc_prior':r['prior'],'seat_prior':r['seat_prior'],'seat_weight':w,'poll':r['poll'],
                     'n_eff':r['neff'],'posterior':p,'correct':int((p>0)==(a>0))})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if int(r['test_cycle'])==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n})
for fn,arr in [('ensemble_summary.csv',summary),('ensemble_choices.csv',choices),('ensemble_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as fo:
        w=csv.DictWriter(fo,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

comb=summary[0];wrong=[r for r in pred if not r['correct']]
lines=['# Rolling prior-ensemble direction experiment','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Primary prior: fullcycle incumbency-era rolling OOS prior.',
 '- Secondary prior architecture is frozen from the 2014 fold pre-2014 inner selection: recent presidential lean only, raw SameSeat, ridge PVI=4/local=64/econ=4096/national=0.',
 '- Same fixed 45-day poll layer is applied after prior ensembling.',
 '- Ensemble weight for each outer cycle is selected only from earlier cycles; correct-winner count is primary and MAE is tie-breaker.','',
 '## Result','',
 '| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Selected weights','',
 '| test | inc weight | seat/PVI weight | train N | train accuracy | train MAE |','|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['inc_prior_weight']:.2f} | {r['seat_prior_weight']:.2f} | {r['train_n']} | {r['train_accuracy_pct']:.1f}% | {r['train_mae']:.2f} |")
lines += ['','## Wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: posterior={r['posterior']:.2f}, actual={r['actual']:.2f}")
lines += ['','## Benchmark','',
 '- Validated fixed-blend benchmark: 94/99 = 94.9%.',
 '- Descriptive 75/25 blend was 95/99 but is not accepted unless rolling historical weight selection reproduces the gain.','',
 '## Decision',f"- Rolling-selected ensemble: {comb['correct']}/{comb['n']} = {comb['direction_accuracy_pct']:.1f}%.",
 '- Adopt only if it exceeds 94/99.']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
