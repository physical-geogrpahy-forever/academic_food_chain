#!/usr/bin/env python3
import csv,re,unicodedata
from pathlib import Path
from datetime import datetime, timezone
from difflib import SequenceMatcher
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
AUTO=ROOT/'data/processed/core_v2r_headline_candidate_experience_audit.csv'
NGA=ROOT/'data/processed/source_snapshots/nga_former_governors_snapshot.csv'
BASE=ROOT/'data/processed/core_v2r_headline_design_matrix_with_congress_experience.csv'
OUT=ROOT/'data/processed/core_v2r_headline_governor_experience_crosscheck.csv'
OVR=ROOT/'config/governor_experience_overrides_v1.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_candidate_experience.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0134_governor-experience-audit.md'
OVR.parent.mkdir(parents=True,exist_ok=True)

def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode('ascii').lower()
    s=re.sub(r'\b(gov|jr|sr|ii|iii|iv)\.?\b',' ',s)
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def suffix(s):
    x=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode('ascii').lower()
    m=re.findall(r'\b(jr|sr|ii|iii|iv)\.?\b',x)
    return m[-1] if m else ''
def b(v): return str(v).lower()=='true'

with TARGET.open('r',encoding='utf-8-sig',newline='') as f: target=list(csv.DictReader(f))
with AUTO.open('r',encoding='utf-8-sig',newline='') as f: auto=list(csv.DictReader(f))
with NGA.open('r',encoding='utf-8-sig',newline='') as f: nga=list(csv.DictReader(f))
with BASE.open('r',encoding='utf-8-sig',newline='') as f: base=list(csv.DictReader(f))
auto_by={r['race_id']:r for r in auto}

gov_terms=defaultdict(list)
for g in nga:
    gov_terms[g['governor_name']].append(g)
by_last=defaultdict(list)
for name,terms in gov_terms.items():
    n=norm(name);
    if n: by_last[n.split()[-1]].append((name,n,terms))

def match(name):
    q=norm(name)
    if not q: return None,0,0,'EMPTY'
    pool=by_last.get(q.split()[-1],[])
    scored=[]
    for display,n,terms in pool:
        s=1.0 if q==n else SequenceMatcher(None,q,n).ratio()
        scored.append((s,display,terms))
    scored.sort(reverse=True,key=lambda x:x[0])
    if not scored: return None,0,0,'NO_MATCH'
    top=scored[0]; second=scored[1][0] if len(scored)>1 else 0
    accepted=(top[0]>=0.92 and top[0]-second>=0.05) or (q==norm(top[1]))
    return (top if accepted else None),top[0],second,('ACCEPTED' if accepted else 'AMBIGUOUS')

rows=[]; overrides=[]
for t in target:
    rid=t['race_id']; cyc=int(t['cycle']); a=auto_by[rid]
    for side in ['D','R']:
        sl=side.lower(); cand=t[f'{sl}_side_candidate']; auto_flag=1 if b(a[f'{sl}_governor_prior_election_win']) else 0
        m,score,second,status=match(cand)
        nga_prior=''; matched=''; term_desc=''; suffix_mismatch=False
        if m:
            _,matched,terms=m
            # NGA has year-level intervals. A term beginning in the election year is not used as a new override,
            # because exact pre-election start date is unknown from this table.
            prior=[g for g in terms if int(g['term_start_year']) < cyc]
            nga_prior=1 if prior else 0
            term_desc=';'.join(f"{g['state']}:{g['term_start_year']}-{g['term_end_year']}" for g in terms)
            suffix_mismatch = bool((suffix(cand) or suffix(matched)) and suffix(cand) != suffix(matched))
        final=auto_flag
        source='election_history_fallback'
        if status=='ACCEPTED' and nga_prior!='' and not suffix_mismatch:
            final=max(auto_flag,nga_prior)
            source='NGA_or_election_history'
        elif suffix_mismatch:
            source='election_history_fallback_identity_suffix_mismatch'
        rec={
          'race_id':rid,'cycle':cyc,'state_abbrev':t['state_abbrev'],'side':side,'candidate_name':cand,
          'auto_governor_experience':auto_flag,'match_status':status,'match_score':f'{score:.4f}','second_score':f'{second:.4f}',
          'matched_nga_name':matched,'identity_suffix_mismatch':str(suffix_mismatch).lower(),'nga_prior_governor':nga_prior,'final_governor_experience':final,'source':source,'nga_terms':term_desc
        }
        rows.append(rec)
        if final!=auto_flag:
            overrides.append({
              'race_id':rid,'cycle':cyc,'state_abbrev':t['state_abbrev'],'side':side,'candidate_name':cand,
              'auto_governor_experience':auto_flag,'nga_governor_experience':nga_prior,'final_governor_experience':final,
              'matched_nga_name':matched,'nga_terms':term_desc,'evidence':'National Governors Association former-governors search'
            })

fields=list(rows[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
ofields=list(overrides[0].keys()) if overrides else ['race_id']
with OVR.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ofields); w.writeheader(); w.writerows(overrides)

rby={(r['race_id'],r['side']):r for r in rows}
dm=[]
for x in base:
    d=rby[(x['race_id'],'D')]; r=rby[(x['race_id'],'R')]
    y=dict(x)
    y['d_governor_experience']=d['final_governor_experience']; y['r_governor_experience']=r['final_governor_experience']
    y['GovernorExperienceDiff']=int(d['final_governor_experience'])-int(r['final_governor_experience'])
    dm.append(y)
df=list(dm[0].keys())
with DM.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=df); w.writeheader(); w.writerows(dm)

auto_pos=sum(int(r['auto_governor_experience']) for r in rows)
final_pos=sum(int(r['final_governor_experience']) for r in rows)
accepted=sum(r['match_status']=='ACCEPTED' for r in rows)
lines=[
 '# GitHub Actions run: GovernorExperience audit','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 f'- Candidate-side rows: {len(rows)}',
 f'- Accepted NGA name matches: {accepted}/{len(rows)}',
 f'- Election-history governor positives: {auto_pos}',
 f'- Final governor positives after NGA cross-check: {final_pos}',
 f'- New supported overrides: {len(overrides)}','',
 '## Rule','',
 'The election-history governor flag is never reduced by an NGA name-match failure. NGA can add a missing prior-governor flag only when the candidate-to-governor name match is accepted, the NGA term starts before the Senate election year, and generational suffixes do not conflict. This prevents a Jr./Sr. parent-child collision from creating false experience.','',
 '## Supported additions','',
 '| cycle | state | side | candidate | auto | NGA | matched governor | terms |',
 '|---:|---|---|---|---:|---:|---|---|'
]
for r in overrides:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['side']} | {r['candidate_name']} | {r['auto_governor_experience']} | {r['nga_governor_experience']} | {r['matched_nga_name']} | {r['nga_terms']} |")
lines += [
 '','## Outputs','',
 '- data/processed/core_v2r_headline_governor_experience_crosscheck.csv',
 '- config/governor_experience_overrides_v1.csv',
 '- data/processed/core_v2r_headline_design_matrix_with_candidate_experience.csv','',
 '## Next','',
 'Add OutPartyIncumbent and PersonalVote, then reconstruct National_t and Era interactions before any coefficient fitting.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))