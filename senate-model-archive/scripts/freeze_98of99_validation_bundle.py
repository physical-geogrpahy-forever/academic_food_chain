#!/usr/bin/env python3
import csv, json, hashlib, runpy, shutil
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
FINAL=ROOT/'final/validation'
FINAL.mkdir(parents=True,exist_ok=True)

SRC={
 'production_predictions': ROOT/'experiments/production_selector_2026/results/production_selector_diagnostic.csv',
 'selector_grid': ROOT/'experiments/production_selector_2026/results/production_selector_top_grid.csv',
 'production_config': ROOT/'config/core_v2r_direction_2026_production.json',
 'clean_predictions': ROOT/'experiments/outparty_closepoll_calibrated/results/calibrated_predictions.csv',
 'clean_choices': ROOT/'experiments/outparty_closepoll_calibrated/results/calibrated_choices.csv',
 'base_predictions': ROOT/'performance/results/fullcycle_inc_era_predictions.csv',
 'base_choices': ROOT/'performance/results/fullcycle_inc_era_choices.csv',
 'base_script': ROOT/'performance/run_fullcycle_inc_era_oos.py',
 'production_script': ROOT/'experiments/production_selector_2026/run.py',
}

def rows(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

copies={
 'production_predictions':'production_98of99_predictions.csv',
 'selector_grid':'production_selector_top_grid.csv',
 'production_config':'core_v2r_direction_2026_production.json',
 'clean_predictions':'clean_nested_96of99_predictions.csv',
 'clean_choices':'clean_nested_96of99_choices.csv',
 'base_predictions':'base_prior_99_predictions.csv',
 'base_choices':'base_prior_choices.csv',
 'base_script':'run_fullcycle_inc_era_oos.py',
 'production_script':'run_production_selector_2026.py',
}
for key,name in copies.items():
    shutil.copy2(SRC[key],FINAL/name)

prod=rows(SRC['production_predictions'])
clean=rows(SRC['clean_predictions'])
base=rows(SRC['base_predictions'])
assert len(prod)==99, f'production rows={len(prod)}'
assert len(clean)==99, f'clean rows={len(clean)}'
assert len(base)==99, f'base rows={len(base)}'

prod_correct=sum(int(r['adjusted_correct']) for r in prod)
prod_base_correct=sum(int(r['baseline_correct']) for r in prod)
prod_wrong=[r for r in prod if int(r['adjusted_correct'])==0]
prod_changed=[r for r in prod if int(r['baseline_correct'])!=int(r['adjusted_correct'])]
clean_correct=sum(int(r['adjusted_correct']) for r in clean)

assert prod_correct==98
assert prod_base_correct==94
assert len(prod_wrong)==1
assert prod_wrong[0]['cycle']=='2014' and prod_wrong[0]['state_abbrev']=='NC'
assert {(r['cycle'],r['state_abbrev']) for r in prod_changed}=={('2018','NV'),('2018','MO'),('2018','FL'),('2018','IN')}
assert clean_correct==96

ns=runpy.run_path(str(SRC['base_script']))
model_rows=ns['rows']
BASE=ns['BASE']
ARCH=ns['ARCH']
choices=rows(SRC['base_choices'])

coef_rows=[]
std_rows=[]

def design(dat,feats):
    X=np.array([[float(r[f]) for f in feats] for r in dat],dtype=float)
    mu=X.mean(0)
    sd=X.std(0)
    sd=np.where(sd<1e-9,1.0,sd)
    Xs=np.column_stack([np.ones(len(dat)),(X-mu)/sd])
    return Xs,mu,sd

for ch in choices:
    tc=int(ch['test_cycle'])
    arch=ch['arch']
    ll=float(ch['lambda_local'])
    le=float(ch['lambda_econ'])
    ln=float(ch['lambda_national'])
    li=float(ch['lambda_inc'])
    lr=float(ch['lambda_era'])
    tr=[r for r in model_rows if int(r['cycle'])<tc]
    feats=BASE+ARCH[arch]
    X,mu,sd=design(tr,feats)
    y=np.array([float(r['y']) for r in tr],dtype=float)
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(feats,start=1):
        if f in ('same_last','same_gap'): pen[j]=ll
        elif f=='econ': pen[j]=le
        elif f=='national': pen[j]=ln
        elif f in ('inc_diff','outparty'): pen[j]=li
        elif f.endswith('_era') or f=='same_era': pen[j]=lr
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    raw_coef=beta[1:]/sd
    raw_intercept=float(beta[0]-np.sum(beta[1:]*mu/sd))
    coef_rows.append({
        'test_cycle':tc,'architecture':arch,'term':'Intercept',
        'standardized_beta':float(beta[0]),'raw_scale_beta':raw_intercept,
        'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,
        'lambda_inc':li,'lambda_era':lr,'train_n':len(tr)
    })
    for j,f in enumerate(feats):
        coef_rows.append({
            'test_cycle':tc,'architecture':arch,'term':f,
            'standardized_beta':float(beta[j+1]),'raw_scale_beta':float(raw_coef[j]),
            'lambda_local':ll,'lambda_econ':le,'lambda_national':ln,
            'lambda_inc':li,'lambda_era':lr,'train_n':len(tr)
        })
        std_rows.append({
            'test_cycle':tc,'architecture':arch,'term':f,
            'mean':float(mu[j]),'sd':float(sd[j]),'train_n':len(tr)
        })

with (FINAL/'base_prior_coefficients_by_cycle.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(coef_rows[0].keys()))
    w.writeheader();w.writerows(coef_rows)
with (FINAL/'base_prior_standardization_by_cycle.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(std_rows[0].keys()))
    w.writeheader();w.writerows(std_rows)

coef_by={}
for tc in (2014,2018,2022):
    cr=[r for r in coef_rows if int(r['test_cycle'])==tc]
    coef_by[tc]={r['term']:float(r['raw_scale_beta']) for r in cr}

max_abs=0.0
for r in base:
    tc=int(r['test_cycle'])
    mr=next(x for x in model_rows if int(x['cycle'])==tc and str(x['race_id'])==str(r['race_id']))
    raw=coef_by[tc]
    p=raw['Intercept']
    for term,b in raw.items():
        if term=='Intercept': continue
        p+=b*float(mr[term])
    max_abs=max(max_abs,abs(p-float(r['predicted'])))
assert max_abs<1e-8, max_abs

manifest={
  'locked_date':'2026-09-21',
  'headline_universe_n':99,
  'base_fixed_poll_correct':prod_base_correct,
  'clean_nested_oos':{
      'correct':clean_correct,'n':99,'accuracy_pct':clean_correct/99*100,
      'canonical_file':'clean_nested_96of99_predictions.csv'
  },
  'production_retrospective':{
      'correct':prod_correct,'n':99,'accuracy_pct':prod_correct/99*100,
      'is_oos':False,
      'canonical_file':'production_98of99_predictions.csv',
      'single_wrong_race':{
          'cycle':int(prod_wrong[0]['cycle']),
          'state_abbrev':prod_wrong[0]['state_abbrev'],
          'race_id':prod_wrong[0]['race_id'],
          'actual_d_minus_r':float(prod_wrong[0]['actual']),
          'adjusted_margin':float(prod_wrong[0]['adjusted_margin'])
      },
      'correctness_changes_vs_fixed_poll_baseline':[
          {'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'race_id':r['race_id'],
           'baseline_correct':int(r['baseline_correct']),
           'adjusted_correct':int(r['adjusted_correct']),
           'override_reason':r['override_reason']}
          for r in prod_changed
      ]
  },
  'base_prior':{
      'canonical_predictions':'base_prior_99_predictions.csv',
      'coefficients':'base_prior_coefficients_by_cycle.csv',
      'standardization':'base_prior_standardization_by_cycle.csv',
      'max_reconstruction_abs_error':max_abs
  },
  'source_sha256':{key:sha256(path) for key,path in SRC.items()},
  'canonical_sha256':{}
}

for p in sorted(FINAL.iterdir()):
    if p.is_file() and p.name!='manifest.json':
        manifest['canonical_sha256'][p.name]=sha256(p)

(FINAL/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc=[
'# Production validation lock: 96/99 clean OOS and 98/99 retrospective','',
'## Permanent distinction','',
'- Clean nested OOS: **96/99 = 97.0%**.',
'- Production retrospective diagnostic: **98/99 = 99.0%**.',
'- The 98/99 result is NOT OOS because the production selector is fit using history through 2022.','',
'## 98/99 exact race table','',
'- Canonical file: final/validation/production_98of99_predictions.csv',
'- Rows: 99.',
'- Fixed-poll baseline correct: 94.',
'- Production-selector correct: 98.',
'- Only wrong race: **2014 North Carolina**.',
'- Corrected relative to the 94/99 baseline: **2018 Nevada, Missouri, Florida, Indiana**.','',
'## Base prior reproduction','',
'- Canonical base-prior predictions: final/validation/base_prior_99_predictions.csv',
'- Exact fitted coefficients by outer cycle: final/validation/base_prior_coefficients_by_cycle.csv',
'- Standardization means and standard deviations: final/validation/base_prior_standardization_by_cycle.csv',
f'- Maximum absolute reconstruction error over all 99 base-prior predictions: **{max_abs:.3e}**.','',
'## Selector reproduction','',
'- Production config: final/validation/core_v2r_direction_2026_production.json',
'- Full selector grid: final/validation/production_selector_top_grid.csv',
'- Clean nested 96/99 race table and choices are frozen alongside the retrospective files.','',
'## Integrity','',
'- manifest.json stores SHA-256 checksums of source and canonical files.',
'- Future experiments must not overwrite this directory.',
'- Any changed production model must use a new versioned directory.'
]
(ROOT/'docs/final/PRODUCTION_VALIDATION_LOCK_2026-09-21.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
