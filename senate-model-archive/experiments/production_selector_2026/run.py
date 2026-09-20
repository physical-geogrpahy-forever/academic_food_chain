#!/usr/bin/env python3
import runpy,csv,json,math
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
SPLIT=ROOT/'experiments/outparty_closepoll_split/run.py'
THIRD=ROOT/'experiments/third_party_historical_v2/results/context_summary.csv'
OUT=ROOT/'experiments/production_selector_2026/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0520_production-selector-2026.md'
CFG=ROOT/'config/core_v2r_direction_2026_production.json'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True);CFG.parent.mkdir(parents=True,exist_ok=True)

ns=runpy.run_path(str(SPLIT))
data=ns['data'];choose=ns['choose'];margin=ns['margin']
best,grid=choose(data)
negok,br,ll,mae,flips,width,npmin,td,ta,pmin=best

# Retrospective diagnostic on headline cycles only. Not an OOS claim because these params use all data through 2022.
headline=[r for r in data if r['cycle'] in (2014,2018,2022)]
diag=[]
for r in headline:
    q,f,reason=margin(r,td,ta,pmin)
    act=r['actual']>0;base=r['posterior']>0;adj=q>0
    diag.append({'cycle':r['cycle'],'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],
                 'actual':r['actual'],'baseline_posterior':r['posterior'],'adjusted_margin':q,
                 'override_applied':f,'override_reason':reason,
                 'baseline_correct':int(base==act),'adjusted_correct':int(adj==act)})
b=sum(r['baseline_correct'] for r in diag);a=sum(r['adjusted_correct'] for r in diag)

config={
 'as_of':'2026-09-21',
 'primary_objective':'winner_direction_accuracy',
 'base_prior':'fullcycle_inc_era rolling model',
 'poll_snapshot_days_before_election':45,
 'poll_blend':{'w_max':0.75,'k':0.5,'window_days':30,'half_life_days':14},
 'outparty_closepoll_selector':{
   'threshold_poll_pvi_disagree_pctpt':td,
   'threshold_poll_pvi_agree_pctpt':ta,
   'min_abs_pvi_when_agree_pctpt':pmin,
   'action':'if eligible, use state PVI direction while preserving posterior magnitude'
 },
 'third_party':{
   'point_margin_correction':'disabled',
   'mode':'uncertainty_only',
   'reason':'historical minor-third-party directional sample too sparse; only NC 2014 recovered in 3-15% ordinary minor-third context',
   'flag_threshold_poll_share_pct':3.0
 },
 'validation':{
   'accepted_clean_nested_headline_correct':96,
   'accepted_clean_nested_headline_n':99,
   'accepted_clean_nested_accuracy_pct':96/99*100,
   'production_parameter_fit_uses_history_through':2022,
   'retrospective_headline_diagnostic_correct':a,
   'retrospective_headline_diagnostic_n':len(diag),
   'retrospective_headline_diagnostic_is_oos':False
 }
}
CFG.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

with (OUT/'production_selector_diagnostic.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(diag[0].keys()));w.writeheader();w.writerows(diag)
with (OUT/'production_selector_top_grid.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['rank','correct','n','brier','logloss','mae','flips','threshold_disagree','threshold_agree','min_abs_pvi_agree']
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for i,z in enumerate(grid[:25],1):
        w.writerow({'rank':i,'correct':-z[0],'n':len(data),'brier':z[1],'logloss':z[2],'mae':z[3],'flips':z[4],
                    'threshold_disagree':z[7],'threshold_agree':z[8],'min_abs_pvi_agree':z[9]})

wrong=[r for r in diag if not r['adjusted_correct']]
lines=['# 2026 production direction selector','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Purpose: fit the production rule for 2026 using all historical information available through 2022.',
'- This is distinct from clean rolling OOS validation.','',
'## Accepted clean validation','',
'- Clean nested headline benchmark: **96/99 = 97.0%**.',
'- This remains the reported historical OOS performance.','',
'## 2026 fitted selector','',
f'- poll-PVI disagree threshold: {td}%p',
f'- poll-PVI agree threshold: {ta}%p',
f'- minimum |PVI| when poll and PVI agree: {pmin}%p',
f'- full-history training correct under selector objective: {-negok}/{len(data)}',
f'- Brier: {br:.4f}',
f'- log loss: {ll:.4f}',
f'- MAE: {mae:.2f}','',
'## Retrospective headline diagnostic','',
f'- fixed baseline: {b}/{len(diag)}',
f'- 2026 fitted rule applied retrospectively: {a}/{len(diag)}',
'- This number is NOT labeled OOS because 2014/2018/2022 participated in production parameter fitting.','',
'## Retrospective remaining wrong','']
for r in wrong:lines.append(f"- {r['cycle']} {r['state_abbrev']}: actual={r['actual']:.2f}, adjusted={r['adjusted_margin']:.2f}, reason={r['override_reason']}")
lines += ['','## Third-party policy','',
'- No directional point correction is applied from third-party share.',
'- Historical multi-candidate audit recovered only one ordinary minor-third 3-15% race-cycle with usable explicit support: NC 2014.',
'- Therefore third-party support is an uncertainty flag only until a broader historical source is assembled.',
'- Major independent/party-replacement races are handled as a separate multi-candidate problem rather than ordinary D/R Senate races.','',
'## Files','',
'- config/core_v2r_direction_2026_production.json',
'- experiments/production_selector_2026/results/production_selector_diagnostic.csv',
'- experiments/production_selector_2026/results/production_selector_top_grid.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
