#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/processed/core_v2r_headline_design_matrix_with_outparty_incumbent.csv'
STATS=ROOT/'data/processed/core_v2r_personal_vote_sufficient_statistics.csv'
OUT=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0148_personal-vote-audit-join.md'

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
base=load(BASE); stats=load(STATS)
sby={(r['target_race_id'],r['side']):r for r in stats}

rows=[]
for b in base:
    d=sby[(b['race_id'],'D')]; r=sby[(b['race_id'],'R')]
    x=dict(b)
    for prefix,src in [('d',d),('r',r)]:
        x[f'{prefix}_personal_prior_statewide_count']=src['prior_statewide_count']
        x[f'{prefix}_personal_prior_senate_count']=src['prior_senate_count']
        x[f'{prefix}_personal_prior_governor_count']=src['prior_governor_count']
        x[f'{prefix}_personal_mean_overperf_vs_pvi_pctpt']=src['mean_own_party_overperf_vs_pvi_pctpt']
        x[f'{prefix}_personal_mean_overperf_cycle_adjusted_pctpt']=src['mean_own_party_overperf_cycle_adjusted_pctpt']
        x[f'{prefix}_personal_latest_prior_statewide_cycle']=src['latest_prior_statewide_cycle']
    dv=d['mean_own_party_overperf_cycle_adjusted_pctpt']; rv=r['mean_own_party_overperf_cycle_adjusted_pctpt']
    x['PersonalVoteDiff_raw_unshrunk_audit']='' if not dv or not rv else f"{float(dv)-float(rv):.8f}"
    x['PersonalVoteDiff_finalized']='false'
    rows.append(x)

fields=list(rows[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

both=sum(bool(r['PersonalVoteDiff_raw_unshrunk_audit']) for r in rows)
lines=[
 '# GitHub Actions run: PersonalVote audit-only design-matrix join','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Headline rows: {len(rows)}',
 f'- Rows where both sides have cycle-adjusted prior statewide history: {both}','',
 '## Important','',
 'PersonalVoteDiff_raw_unshrunk_audit is not the Core V2 model term. It is emitted only when both D and R candidates have prior statewide cycle-adjusted performance. Missing candidate history is not silently treated as zero in this diagnostic difference.','',
 'The final PersonalVoteDiff still requires partial pooling, era interaction, candidate-history-count shrinkage, and any statewide-vs-district information weighting to be selected inside rolling nested OOS.','',
 '## Output','',
 '- data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv','',
 '## Next','',
 'Audit reconstructable historical sources for National_t and RelativeEconomicGrowth before any regression fitting.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))