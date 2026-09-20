#!/usr/bin/env python3
import csv, re, unicodedata, yaml
from pathlib import Path
from datetime import date, datetime, timezone
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'data/processed/core_v2r_headline_target_hypothesis_A.csv'
AUTO = ROOT / 'data/processed/core_v2r_headline_candidate_experience_audit.csv'
CURRENT = ROOT / 'data/raw/congress-legislators/legislators-current.yaml'
HIST = ROOT / 'data/raw/congress-legislators/legislators-historical.yaml'
OUT = ROOT / 'data/processed/core_v2r_headline_congress_service_crosscheck.csv'
REVIEW = ROOT / 'data/processed/core_v2r_candidate_name_match_review.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0122_congress-service-crosscheck.md'

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii','ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'\b(jr|sr|ii|iii|iv)\.?\b', ' ', s)
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def variants(person):
    n = person.get('name', {})
    vals = set()
    for k in ['official_full','first','middle','last','nickname']:
        if n.get(k): vals.add(norm(n[k]))
    first=n.get('first',''); middle=n.get('middle',''); last=n.get('last',''); nick=n.get('nickname','')
    combos=[f'{first} {last}', f'{first} {middle} {last}', f'{nick} {last}']
    for x in combos:
        if norm(x): vals.add(norm(x))
    return vals

people=[]
for path in [CURRENT,HIST]:
    data=yaml.safe_load(path.read_text(encoding='utf-8')) or []
    people.extend(data)

index=[]
for p in people:
    vs=variants(p)
    if not vs: continue
    states=set(t.get('state','') for t in p.get('terms',[]) if t.get('state'))
    index.append((p,vs,states))

with TARGET.open('r',encoding='utf-8-sig',newline='') as f:
    target=list(csv.DictReader(f))
with AUTO.open('r',encoding='utf-8-sig',newline='') as f:
    auto=list(csv.DictReader(f))

# map automatic audit by race + side if columns allow; preserve all original columns for merge inspection
auto_by={}
for r in auto:
    key=(r.get('race_id',''),r.get('side',''))
    auto_by[key]=r

def election_day(year):
    # General election date not needed exactly for prior-service flag; Nov 1 is safe pre-election anchor.
    return date(year,11,1)

def score_candidate(name,state,p):
    q=norm(name)
    best=max((SequenceMatcher(None,q,v).ratio() for v in variants(p)), default=0)
    # modest state bonus, but do not require state because prior House/Senate service may be elsewhere
    states=set(t.get('state','') for t in p.get('terms',[]) if t.get('state'))
    if state in states: best += 0.05
    return best

def match(name,state):
    scored=[]
    for p,vs,states in index:
        s=score_candidate(name,state,p)
        if s>=0.72:
            scored.append((s,p))
    scored.sort(key=lambda x:x[0], reverse=True)
    if not scored: return None,0,0
    top=scored[0]
    second=scored[1][0] if len(scored)>1 else 0
    return top[1],top[0],second

def term_flags(p,cycle):
    anchor=election_day(cycle)
    prior_sen=0; prior_house=0; incumbent_sen=0
    terms=[]
    for t in p.get('terms',[]):
        try:
            start=date.fromisoformat(str(t.get('start')))
            end=date.fromisoformat(str(t.get('end')))
        except Exception:
            continue
        typ=t.get('type')
        if start < anchor:
            if typ=='sen': prior_sen=1
            if typ=='rep': prior_house=1
        if typ=='sen' and start <= anchor <= end:
            incumbent_sen=1
        terms.append(f"{typ}:{t.get('state','')}:{start}:{end}")
    return prior_sen,prior_house,incumbent_sen,';'.join(terms)

rows=[]; reviews=[]
for r in target:
    cycle=int(r['cycle']); state=r['state_abbrev']; race=r['race_id']
    # target panel fields are inspected dynamically; candidate names expected from side candidate columns
    candidates=[]
    for side in ['D','R']:
        name = r.get(f'{side.lower()}_candidate_name') or r.get(f'candidate_{side}') or r.get(f'{side}_candidate_name') or ''
        if not name:
            # fallback from aligned display fields if present
            name = r.get(f'{side.lower()}_side_candidate') or ''
        candidates.append((side,name))
    for side,name in candidates:
        p,top,second=match(name,state) if name else (None,0,0)
        rec={
            'race_id':race,'cycle':cycle,'state_abbrev':state,'side':side,'candidate_name':name,
            'match_score':f'{top:.4f}','second_score':f'{second:.4f}','match_margin':f'{top-second:.4f}',
            'matched':str(p is not None).lower(),
            'matched_name':'','bioguide':'','prior_senate_service':'','prior_house_service':'','senate_incumbent_on_anchor':'','terms':''
        }
        if p:
            n=p.get('name',{})
            rec['matched_name']=n.get('official_full') or (n.get('first','')+' '+n.get('last','')).strip()
            rec['bioguide']=p.get('id',{}).get('bioguide','')
            ps,ph,inc,terms=term_flags(p,cycle)
            rec['prior_senate_service']=ps; rec['prior_house_service']=ph; rec['senate_incumbent_on_anchor']=inc; rec['terms']=terms
        rows.append(rec)
        if (not p) or top<0.90 or (top-second)<0.08:
            reviews.append(rec.copy())

fields=list(rows[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
with REVIEW.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(reviews)

matched=sum(r['matched']=='true' for r in rows)
lines=[
    '# GitHub Actions run: congressional service cross-check',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    f'- Candidate-side rows: {len(rows)}',
    f'- Matched to congress-legislators: {matched}/{len(rows)}',
    f'- Name matches requiring review: {len(reviews)}',
    '',
    '## Purpose',
    '',
    'Cross-check prior Senate service, prior House service, and Senate incumbency using actual term dates rather than election-win history alone. This captures appointments and service that the first automatic election-history proxy can miss.',
    '',
    '## Limits',
    '',
    '- Name matching is still a reconstruction step and ambiguous matches are never silently accepted.',
    '- Governor experience is not covered by this source.',
    '- The Nov 1 anchor is used only to determine whether service predates the general election; later work can replace it with exact election dates.',
    '',
    '## Outputs',
    '',
    '- data/processed/core_v2r_headline_congress_service_crosscheck.csv',
    '- data/processed/core_v2r_candidate_name_match_review.csv',
    '',
    '## Next',
    '',
    'Resolve reviewed name matches, then compare term-date flags against the election-history flags and create explicit overrides only where supported.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))