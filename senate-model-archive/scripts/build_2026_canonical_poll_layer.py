#!/usr/bin/env python3
import csv
import math
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/'data/snapshots/2026_senate_rcp_rows_through_2026-09-19.csv'
AUDIT=ROOT/'data/snapshots/2026_poll_sample_size_audit.csv'
STRUCT=ROOT/'data/snapshots/2026_structural_input_matrix_45d.csv'
DETAIL=ROOT/'data/snapshots/2026_poll_45d_canonical_weight_detail.csv'
OUT=ROOT/'data/snapshots/2026_poll_45d_canonical_sample_weighted.csv'
DOC=ROOT/'docs/analysis/2026_POLL_45D_CANONICAL_LAYER.md'

TARGET=date(2026,9,19)
WINDOW=30
HALF_LIFE=14
WMAX=.75
K=.5

def read_csv(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

frozen=read_csv(FROZEN)
audit=read_csv(AUDIT)
struct=read_csv(STRUCT)
party_by_state={r['state_abbrev']:{'D':r['candidate_D'],'R':r['candidate_R']} for r in struct}

if len(frozen)!=42:
    raise RuntimeError(f'Expected 42 frozen RCP rows, got {len(frozen)}')
if len(audit)!=42:
    raise RuntimeError(f'Expected 42 audited sample rows, got {len(audit)}')

def key(r):
    return (r['date'],r['state'],r['pollster'])

aidx={}
for r in audit:
    k=key(r)
    if k in aidx:
        raise RuntimeError(f'Duplicate audit key: {k}')
    aidx[k]=r

missing=[key(r) for r in frozen if key(r) not in aidx]
extra=[key(r) for r in audit if key(r) not in {key(x) for x in frozen}]
if missing or extra:
    raise RuntimeError(f'Audit/frozen key mismatch. missing={missing}, extra={extra}')

detail=[]
by_state=defaultdict(list)

def surname(name):
    return (name or '').strip().split()[-1].lower()

def normalized_d_minus_r(r):
    # IMPORTANT: the frozen RCP bridge file retained candidate-order values in
    # columns historically named D/R/D_minus_R. Normalize here using the
    # candidate names rather than trusting those legacy column labels.
    st=r['state']
    left,right=[x.strip() for x in r['race'].split(' vs ',1)]
    d=party_by_state[st]['D']; rr=party_by_state[st]['R']
    ls,rs=surname(left),surname(right)
    ds,rrs=surname(d),surname(rr)
    raw=float(r['D_minus_R'])  # actually left candidate minus right candidate
    if ls==rrs and rs==ds:
        return -raw,'R_vs_D_inverted'
    if ls==ds and rs==rrs:
        return raw,'D_vs_R_kept'
    raise RuntimeError(
        f'Cannot determine candidate-order party orientation for {st}: '
        f'race={r["race"]}, candidate_D={d}, candidate_R={rr}'
    )

for r in frozen:
    a=aidx[key(r)]
    dmr,orientation=normalized_d_minus_r(r)
    end=date.fromisoformat(a['field_end_date'])
    age=(TARGET-end).days
    if age<0:
        raise RuntimeError(f'Future field end for {key(r)}: {end}')
    if age>WINDOW:
        included=0
        rec=0.0
        sw=0.0
        wt=0.0
    else:
        included=1
        n=float(a['sample_size'])
        rec=math.exp(-math.log(2)*age/HALF_LIFE)
        sw=math.sqrt(min(max(n,100.0),5000.0)/600.0)
        wt=rec*sw
    row={
        'snapshot_target':'2026-09-19',
        'release_or_listing_date':r['date'],
        'field_end_date':a['field_end_date'],
        'state':r['state'],
        'race':r['race'],
        'pollster':r['pollster'],
        'raw_left_value':r['D'],
        'raw_right_value':r['R'],
        'raw_left_minus_right':r['D_minus_R'],
        'normalized_D_minus_R':dmr,
        'orientation_fix':orientation,
        'sample_size':a['sample_size'],
        'population':a['population'],
        'age_days':age,
        'included_30d':included,
        'recency_weight':rec,
        'sample_size_weight':sw,
        'combined_weight':wt,
        'match_status':a['match_status'],
        'sample_source_name':a['source_name'],
        'sample_source_url':a['source_url'],
    }
    detail.append(row)
    if included:
        by_state[r['state']].append(row)

if len(detail)!=42:
    raise RuntimeError('Detail row count changed unexpectedly')

states=sorted(by_state)
out=[]
for st in states:
    rows=by_state[st]
    weights=[float(x['combined_weight']) for x in rows]
    margins=[float(x['D_minus_R']) for x in rows]
    s=sum(weights)
    if s<=0:
        raise RuntimeError(f'Non-positive weight sum for {st}')
    poll_margin=sum(m*w for m,w in zip(margins,weights))/s
    neff=s*s/sum(w*w for w in weights)
    poll_blend_weight=WMAX*neff/(neff+K)
    out.append({
        'snapshot_target':'2026-09-19',
        'state':st,
        'poll_margin_D_minus_R_pctpt':poll_margin,
        'n_eff':neff,
        'poll_count':len(rows),
        'weight_sum':s,
        'locked_poll_blend_weight_from_neff':poll_blend_weight,
        'window_days':WINDOW,
        'half_life_days':HALF_LIFE,
        'sample_weight_rule':'sqrt(clamp(n,100,5000)/600)',
        'status':'poll_layer_only_not_forecast',
    })

DETAIL.parent.mkdir(parents=True,exist_ok=True)
with DETAIL.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(detail[0].keys()))
    w.writeheader();w.writerows(detail)
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()))
    w.writeheader();w.writerows(out)

lines=[
'# 2026 canonical 45-day poll layer',
'',
'- Frozen information cutoff: 2026-09-19 U.S. calendar date.',
'- This reproduces the weighting rule used by the canonical 98/99 production path.',
"- Poll values come from the already frozen RCP snapshot; audited external sources supply sample sizes and actual field-end dates.\n- The frozen bridge file's legacy D/R labels actually preserve left-candidate/right-candidate order. The builder verifies candidate names against the structural matrix and normalizes every row to true D-minus-R before aggregation.",
'- Window: 30 days before the 45-day snapshot.',
'- Recency half-life: 14 days.',
'- Per-poll weight: 2^(-age/14) * sqrt(clamp(sample_size,100,5000)/600).',
'- Effective poll count: (sum(w))^2 / sum(w^2).',
'- Downstream locked poll-blend weight is stored for audit as 0.75*n_eff/(n_eff+0.5).',
'- This artifact is the poll input layer only. It does not combine polls with fundamentals and does not emit election-outcome directions or probabilities.',
'',
'## Integrity checks',
'',
f'- frozen rows: {len(frozen)}',
f'- audited rows: {len(audit)}',
f'- states: {len(states)}',
f'- unmatched frozen rows: {len(missing)}',
'',
'## Outputs',
'',
'- data/snapshots/2026_poll_45d_canonical_weight_detail.csv',
'- data/snapshots/2026_poll_45d_canonical_sample_weighted.csv',
'- data/snapshots/2026_poll_sample_size_audit.csv',
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
print('\nState poll-layer metrics:')
for r in out:
    print(r['state'], 'poll_count=',r['poll_count'],
          'margin=',round(r['poll_margin_D_minus_R_pctpt'],6),
          'n_eff=',round(r['n_eff'],6),
          'blend_w=',round(r['locked_poll_blend_weight_from_neff'],6))
