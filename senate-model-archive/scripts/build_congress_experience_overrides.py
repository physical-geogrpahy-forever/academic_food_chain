#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CROSS = ROOT / 'data/processed/core_v2r_headline_congress_service_crosscheck.csv'
AUTO = ROOT / 'data/processed/core_v2r_headline_candidate_experience_audit.csv'
SKEL = ROOT / 'data/processed/core_v2r_headline_design_matrix_skeleton.csv'
OVR = ROOT / 'config/congress_experience_overrides_v1.csv'
HYB = ROOT / 'data/processed/core_v2r_headline_candidate_experience_hybrid.csv'
DM = ROOT / 'data/processed/core_v2r_headline_design_matrix_with_congress_experience.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0129_congress-experience-overrides-v1.md'
OVR.parent.mkdir(parents=True, exist_ok=True)

def i(v):
    try: return int(v)
    except: return 0

with CROSS.open('r',encoding='utf-8-sig',newline='') as f:
    cross=list(csv.DictReader(f))
with AUTO.open('r',encoding='utf-8-sig',newline='') as f:
    auto=list(csv.DictReader(f))
with SKEL.open('r',encoding='utf-8-sig',newline='') as f:
    skel=list(csv.DictReader(f))

# Explicit overrides require an accepted term-record match and an actual flag difference.
over=[]
for r in cross:
    if r['match_status'] != 'ACCEPTED':
        continue
    diffs = {
        'SenateExperience': i(r['senate_flag_diff']),
        'HouseExperience': i(r['house_flag_diff']),
        'Incumbency': i(r['incumbency_flag_diff'])
    }
    changed=[k for k,v in diffs.items() if v!=0]
    if not changed:
        continue
    over.append({
        'race_id':r['race_id'],'cycle':r['cycle'],'state_abbrev':r['state_abbrev'],
        'side':r['side'],'candidate_name':r['candidate_name'],'bioguide':r['bioguide'],
        'changed_fields':';'.join(changed),
        'auto_prior_senate':r['auto_prior_senate'],'term_prior_senate':r['term_prior_senate'],
        'auto_prior_house':r['auto_prior_house'],'term_prior_house':r['term_prior_house'],
        'auto_incumbency_proxy':r['auto_incumbency_proxy'],'term_senate_incumbent':r['term_senate_incumbent'],
        'evidence':'unitedstates/congress-legislators term dates'
    })

ofields=list(over[0].keys()) if over else ['race_id']
with OVR.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ofields); w.writeheader(); w.writerows(over)

cross_by={(r['race_id'],r['side']):r for r in cross}
hybrid=[]
for a in auto:
    rid=a['race_id']
    row={
        'race_id':rid,'cycle':a['cycle'],'state_abbrev':a['state_abbrev'],'seat':a['seat'],
        'd_candidate':a['d_candidate'],'r_candidate':a['r_candidate']
    }
    for side in ['D','R']:
        sl=side.lower(); c=cross_by[(rid,side)]
        accepted=c['match_status']=='ACCEPTED'
        auto_s=i(a[f'{sl}_senate_prior_election_win']) if a[f'{sl}_senate_prior_election_win'] in ['0','1'] else (1 if a[f'{sl}_senate_prior_election_win'].lower()=='true' else 0)
        auto_h=i(a[f'{sl}_house_prior_election_win']) if a[f'{sl}_house_prior_election_win'] in ['0','1'] else (1 if a[f'{sl}_house_prior_election_win'].lower()=='true' else 0)
        auto_inc=i(a[f'{sl}_incumbency_election_history_proxy']) if a[f'{sl}_incumbency_election_history_proxy'] in ['0','1'] else (1 if a[f'{sl}_incumbency_election_history_proxy'].lower()=='true' else 0)
        row[f'{sl}_senate_experience'] = i(c['term_prior_senate']) if accepted and c['term_prior_senate']!='' else auto_s
        row[f'{sl}_house_experience'] = i(c['term_prior_house']) if accepted and c['term_prior_house']!='' else auto_h
        row[f'{sl}_incumbency'] = i(c['term_senate_incumbent']) if accepted and c['term_senate_incumbent']!='' else auto_inc
        row[f'{sl}_congress_source'] = 'term_date' if accepted else 'election_history_fallback'
    row['SenateExperienceDiff'] = row['d_senate_experience'] - row['r_senate_experience']
    row['HouseExperienceDiff'] = row['d_house_experience'] - row['r_house_experience']
    row['IncumbencyDiff'] = row['d_incumbency'] - row['r_incumbency']
    hybrid.append(row)

hfields=list(hybrid[0].keys())
with HYB.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=hfields); w.writeheader(); w.writerows(hybrid)

hby={r['race_id']:r for r in hybrid}
dm=[]
for s in skel:
    h=hby[s['race_id']]
    out=dict(s)
    for k in ['d_senate_experience','r_senate_experience','SenateExperienceDiff',
              'd_house_experience','r_house_experience','HouseExperienceDiff',
              'd_incumbency','r_incumbency','IncumbencyDiff']:
        out[k]=h[k]
    dm.append(out)

dfields=list(dm[0].keys())
with DM.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=dfields); w.writeheader(); w.writerows(dm)

unique_candidates=sorted(set((r['cycle'],r['candidate_name']) for r in over))
sen_changes=sum('SenateExperience' in r['changed_fields'].split(';') for r in over)
house_changes=sum('HouseExperience' in r['changed_fields'].split(';') for r in over)
inc_changes=sum('Incumbency' in r['changed_fields'].split(';') for r in over)
lines=[
    '# GitHub Actions run: Congress experience overrides v1',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    f'- Candidate-side override rows: {len(over)}',
    f'- Unique cycle-candidate overrides: {len(unique_candidates)}',
    f'- SenateExperience corrections: {sen_changes}',
    f'- HouseExperience corrections: {house_changes}',
    f'- Incumbency corrections: {inc_changes}',
    '',
    '## Rule',
    '',
    'An override is created only when the candidate has an ACCEPTED match to unitedstates/congress-legislators and the actual term-date flag differs from the election-history proxy. Ambiguous or unmatched names never overwrite the election-history value.',
    '',
    '## Overrides',
    '',
    '| cycle | state | side | candidate | changed fields | Senate auto->term | House auto->term | Inc auto->term |',
    '|---:|---|---|---|---|---|---|---|'
]
for r in over:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['side']} | {r['candidate_name']} | {r['changed_fields']} | {r['auto_prior_senate']}->{r['term_prior_senate']} | {r['auto_prior_house']}->{r['term_prior_house']} | {r['auto_incumbency_proxy']}->{r['term_senate_incumbent']} |")
lines += [
    '',
    '## Interpretation',
    '',
    'The important Senate/incumbency corrections are appointments or mid-cycle accessions that a prior-general-election-win proxy cannot see. House corrections capture candidates who had House service even when the election-history winner query missed it.',
    '',
    '## Outputs',
    '',
    '- config/congress_experience_overrides_v1.csv',
    '- data/processed/core_v2r_headline_candidate_experience_hybrid.csv',
    '- data/processed/core_v2r_headline_design_matrix_with_congress_experience.csv',
    '',
    '## Not yet final',
    '',
    'GovernorExperience remains election-history based and still needs a separate term-history audit. OutPartyIncumbent and PersonalVote are not yet joined.',
    '',
    '## Next',
    '',
    'Audit GovernorExperience for succession/non-election entry, then join GovernorExperienceDiff and construct the final incumbency variables.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))