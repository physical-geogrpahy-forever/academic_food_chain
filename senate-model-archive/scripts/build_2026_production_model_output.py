#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STRUCT=ROOT/'data/snapshots/2026_structural_input_matrix_45d.csv'
COEF=ROOT/'data/snapshots/2026_production_fundamentals_coefficients.csv'
POLL=ROOT/'data/snapshots/2026_poll_45d_canonical_sample_weighted.csv'
LEGACY=ROOT/'data/snapshots/2026_PRODUCTION_INPUT_MATRIX_FINAL_45D.csv'
CONFIG=ROOT/'final/validation/core_v2r_direction_2026_production.json'
OUT=ROOT/'data/snapshots/2026_PRODUCTION_MODEL_OUTPUT_45D.csv'
DOC=ROOT/'docs/analysis/2026_PRODUCTION_MODEL_OUTPUT_45D.md'

def read(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

struct=read(STRUCT)
coefrows=read(COEF)
poll={r['state']:r for r in read(POLL)}
legacy={r['state_abbrev']:r for r in read(LEGACY)}
config=json.loads(CONFIG.read_text(encoding='utf-8'))

b={r['term']:float(r['raw_scale_beta']) for r in coefrows}
required=['Intercept','pvi','same_last','same_gap','econ','national','inc_diff','outparty','inc_era','outparty_era']
miss=[x for x in required if x not in b]
if miss: raise RuntimeError(f'missing coefficients: {miss}')

td=float(config['outparty_closepoll_selector']['threshold_poll_pvi_disagree_pctpt'])
ta=float(config['outparty_closepoll_selector']['threshold_poll_pvi_agree_pctpt'])
pmin=float(config['outparty_closepoll_selector']['min_abs_pvi_when_agree_pctpt'])

def sign(x):
    return 1 if x>0 else (-1 if x<0 else 0)

rows=[]
for r in struct:
    st=r['state_abbrev']
    p=poll[st]
    pvi=float(r['pvi_2026_d_minus_r_pctpt'])
    same=float(r['same_seat_d_minus_r_pctpt'])
    gap=2026-int(r['same_seat_prior_cycle'])
    econ=float(r['relative_economic_growth_presparty_signed'])
    national=float(r['national_generic_ballot_D_minus_R_pctpt'])
    inc=float(r['incumbency_diff_D_minus_R'])
    outparty=float(r['outparty_incumbent_signed'])
    era=(2026-2006)/4.0
    inc_era=inc*era
    out_era=outparty*era
    prior=(b['Intercept']+b['pvi']*pvi+b['same_last']*same+b['same_gap']*gap+
           b['econ']*econ+b['national']*national+b['inc_diff']*inc+
           b['outparty']*outparty+b['inc_era']*inc_era+b['outparty_era']*out_era)
    pollm=float(p['poll_margin_D_minus_R_pctpt'])
    alpha=float(p['locked_poll_blend_weight_from_neff'])
    posterior=(1-alpha)*prior+alpha*pollm

    agree=(sign(pollm)==sign(pvi) and sign(pollm)!=0)
    eligible=False; reason='none'
    if outparty!=0:
        if (not agree) and abs(pollm)<=td:
            eligible=True; reason='poll_PVI_disagree_close_poll'
        elif agree and abs(pollm)<=ta and abs(pvi)>=pmin:
            eligible=True; reason='poll_PVI_agree_close_poll_strong_PVI'
    final=(sign(pvi)*abs(posterior)) if eligible and sign(pvi)!=0 else posterior
    changed=int(sign(final)!=sign(posterior))
    direction='D' if final>0 else ('R' if final<0 else 'TIE')
    lead=abs(final)
    label=(f"D +{lead:.2f}" if direction=='D' else (f"R +{lead:.2f}" if direction=='R' else 'Tie'))
    third=int(float(legacy[st]['third_party_or_multicandidate_flag']))
    rows.append({
      'snapshot_date':'2026-09-19',
      'state_abbrev':st,
      'candidate_D':r['candidate_D'],
      'candidate_R':r['candidate_R'],
      'fundamentals_prior_D_minus_R_pctpt':prior,
      'poll_D_minus_R_pctpt':pollm,
      'poll_n_eff':float(p['n_eff']),
      'poll_blend_weight':alpha,
      'posterior_before_selector_D_minus_R_pctpt':posterior,
      'selector_eligible':int(eligible),
      'selector_reason':reason,
      'selector_changed_direction':changed,
      'final_model_margin_D_minus_R_pctpt':final,
      'model_output_direction':direction,
      'model_output_label':label,
      'third_party_or_multicandidate_flag':third,
      'status':'locked_model_output_at_2026-09-19_cutoff_not_observed_result'
    })

with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

lines=['# 2026 production model output at 45-day cutoff','',
'- Snapshot: 2026-09-19.',
'- This is the output of the locked Core V2-R Direction Production 2026 calculation, not an observed election result.',
'- Positive margin means Democratic two-party margin; negative margin means Republican two-party margin.',
'- No 2026 observed election outcome is used.','',
'| State | fundamentals | poll | alpha | posterior | selector eligible | final model output |',
'|---|---:|---:|---:|---:|---|---:|']
for x in rows:
    lines.append(f"| {x['state_abbrev']} | {x['fundamentals_prior_D_minus_R_pctpt']:+.2f} | {x['poll_D_minus_R_pctpt']:+.2f} | {x['poll_blend_weight']:.3f} | {x['posterior_before_selector_D_minus_R_pctpt']:+.2f} | {'yes' if x['selector_eligible'] else 'no'} | {x['model_output_label']} |")
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
