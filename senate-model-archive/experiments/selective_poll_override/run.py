#!/usr/bin/env python3
import runpy
from pathlib import Path
from datetime import datetime, timezone
import csv

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'experiments/selective_poll_override/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0330_selective-poll-override-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

ns=runpy.run_path(str(ROOT/'experiments/poll_stack/run.py'))
hist=ns['hist']
OUTER=[2014,2018,2022]

# Only baseline-posterior vs poll disagreements are eligible for override.
def eligible(r):
    return r['poll_count']>0 and ((r['posterior']>0)!=(float(r['poll'])>0))

def rule_defs():
    out=[('none',0,lambda r:False)]
    for t in [2,3,4,5,6,8]:
        out.append((f'neff_le_{t}',1,lambda r,t=t:r['neff']<=t))
        out.append((f'neff_ge_{t}',1,lambda r,t=t:r['neff']>=t))
    for t in [2,3,4,5,6]:
        out.append((f'count_le_{t}',1,lambda r,t=t:r['poll_count']<=t))
        out.append((f'count_ge_{t}',1,lambda r,t=t:r['poll_count']>=t))
    for t in [.25,.5,1,2,3,5]:
        out.append((f'abspoll_ge_{t}',1,lambda r,t=t:abs(float(r['poll']))>=t))
    for t in [3,5,8,10,15,20]:
        out.append((f'gap_ge_{t}',1,lambda r,t=t:abs(r['prior']-float(r['poll']))>=t))
    for n in [3,4,5]:
      for a in [5,10,15]:
        out.append((f'neff_le_{n}_prior_ge_{a}',2,lambda r,n=n,a=a:r['neff']<=n and abs(r['prior'])>=a))
        out.append((f'count_le_{n}_prior_ge_{a}',2,lambda r,n=n,a=a:r['poll_count']<=n and abs(r['prior'])>=a))
      for g in [5,10,15]:
        out.append((f'neff_le_{n}_gap_ge_{g}',2,lambda r,n=n,g=g:r['neff']<=n and abs(r['prior']-float(r['poll']))>=g))
    return out
RULES=rule_defs()

def apply(r,fn):
    base=(r['posterior']>0)
    if eligible(r) and fn(r):
        return float(r['poll'])>0,1
    return base,0

def score(dat,fn):
    ok=flips=0
    for r in dat:
        pred,f=apply(r,fn);ok+=int(pred==(r['actual']>0));flips+=f
    return ok,flips

choices=[];pred=[]
for tc in OUTER:
    train=[r for r in hist if r['cycle']<tc]
    test=[r for r in hist if r['cycle']==tc]
    cand=[]
    for name,complexity,fn in RULES:
        ok,flips=score(train,fn)
        # Primary: more correct. Tie-break: fewer flips, simpler rule, then rule name.
        cand.append((-ok,flips,complexity,name,fn))
    cand.sort(key=lambda z:(z[0],z[1],z[2],z[3]))
    best=cand[0];negok,trainflips,complexity,name,fn=best
    choices.append({'test_cycle':tc,'rule':name,'train_n':len(train),'train_correct':-negok,
                    'train_accuracy_pct':100*(-negok)/len(train),'train_flips':trainflips,'complexity':complexity,
                    'top12':' | '.join(f'{z[3]} correct={-z[0]} flips={z[1]}' for z in cand[:12])})
    for r in test:
        p,flip=apply(r,fn)
        base=(r['posterior']>0);act=(r['actual']>0)
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                     'actual':r['actual'],'prior':r['prior'],'poll':r['poll'],'n_eff':r['neff'],
                     'poll_count':r['poll_count'],'baseline_posterior':r['posterior'],
                     'rule':name,'override_applied':flip,'baseline_correct':int(base==act),'override_correct':int(p==act)})

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);o=sum(r['override_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'override_correct':o,'override_accuracy_pct':100*o/n,'net_correct_gain':o-b,
                    'overrides_applied':sum(r['override_applied'] for r in rr)})

for fn,data in [('override_summary.csv',summary),('override_choices.csv',choices),('override_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

comb=summary[0]
changed=[r for r in pred if r['baseline_correct']!=r['override_correct']]
lines=['# Selective poll override direction experiment','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       '- Baseline is the fixed Core V2 poll blend at 94/99.',
       '- Only races where baseline posterior direction and poll direction disagree are eligible for an override.',
       '- The override rule for each outer cycle is selected only from earlier cycles.',
       '- Primary selection criterion is number of correct winners. Ties prefer fewer overrides, then simpler rules.','',
       '## Result','',
       '| scope | N | baseline correct | baseline acc | override correct | override acc | net | overrides |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['override_correct']} | {r['override_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['overrides_applied']} |")
lines += ['','## Selected rules','',
          '| test | rule | prior rows | prior accuracy | train flips |','|---:|---|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['rule']} | {r['train_n']} | {r['train_accuracy_pct']:.1f}% | {r['train_flips']} |")
lines += ['','## Changed correctness','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> override {'correct' if r['override_correct'] else 'wrong'}, rule={r['rule']}")
lines += ['','## Decision','',
          'Adopt only if the selective override exceeds 94/99 without using the outer test outcome in rule selection.','',
          '## Outputs','',
          '- experiments/selective_poll_override/results/override_summary.csv',
          '- experiments/selective_poll_override/results/override_choices.csv',
          '- experiments/selective_poll_override/results/override_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
