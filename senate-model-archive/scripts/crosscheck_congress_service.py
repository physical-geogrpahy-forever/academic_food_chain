#!/usr/bin/env python3
import csv, re, unicodedata, yaml
from pathlib import Path
from datetime import date, datetime, timezone
from difflib import SequenceMatcher
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'data/processed/core_v2r_headline_target_hypothesis_A.csv'
AUTO = ROOT / 'data/processed/core_v2r_headline_candidate_experience_audit.csv'
CURRENT = ROOT / 'data/raw/congress-legislators/legislators-current.yaml'
HIST = ROOT / 'data/raw/congress-legislators/legislators-historical.yaml'
OUT = ROOT / 'data/processed/core_v2r_headline_congress_service_crosscheck.csv'
REVIEW = ROOT / 'data/processed/core_v2r_candidate_name_match_review.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0122_congress-service-crosscheck.md'

ELECTION_DATE = {2014: date(2014,11,4), 2018: date(2018,11,6), 2022: date(2022,11,8)}

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii','ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'\b(jr|sr|ii|iii|iv)\.?\b', ' ', s)
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def truth(v):
    return str(v).strip().lower() == 'true'

def person_variants(person):
    n = person.get('name', {})
    vals = set()
    pieces = [
        n.get('official_full',''),
        f"{n.get('first','')} {n.get('last','')}",
        f"{n.get('first','')} {n.get('middle','')} {n.get('last','')}",
        f"{n.get('nickname','')} {n.get('last','')}"
    ]
    for x in pieces:
        x = norm(x)
        if x: vals.add(x)
    return vals

people=[]
for path in [CURRENT,HIST]:
    people.extend(yaml.safe_load(path.read_text(encoding='utf-8')) or [])

index=[]
by_last=defaultdict(list)
for p in people:
    vs=person_variants(p)
    if not vs: continue
    last=norm(p.get('name',{}).get('last',''))
    states=set(t.get('state','') for t in p.get('terms',[]) if t.get('state'))
    item=(p,vs,states,last)
    index.append(item)
    if last: by_last[last].append(item)

with TARGET.open('r',encoding='utf-8-sig',newline='') as f:
    target=list(csv.DictReader(f))
with AUTO.open('r',encoding='utf-8-sig',newline='') as f:
    auto=list(csv.DictReader(f))
auto_by={r['race_id']:r for r in auto}

def score_item(q,state,item):
    p,vs,states,last=item
    if q in vs:
        base=1.0
    else:
        base=max((SequenceMatcher(None,q,v).ratio() for v in vs), default=0.0)
    if state in states:
        base=min(1.0, base+0.03)
    return base

def match(name,state):
    q=norm(name)
    if not q: return None,0.0,0.0,'EMPTY_NAME'
    last=q.split()[-1]
    pool=by_last.get(last) or index
    scored=[]
    for item in pool:
        s=score_item(q,state,item)
        if s>=0.72:
            scored.append((s,item[0]))
    scored.sort(key=lambda x:x[0], reverse=True)
    if not scored: return None,0.0,0.0,'NO_MATCH'
    top_score, top_person=scored[0]
    second=scored[1][0] if len(scored)>1 else 0.0
    exact = q in person_variants(top_person)
    accepted = (exact and (top_score-second)>=0.02) or (top_score>=0.88 and (top_score-second)>=0.05)
    return (top_person if accepted else None), top_score, second, ('ACCEPTED' if accepted else 'AMBIGUOUS')

def term_flags(person,cycle):
    anchor=ELECTION_DATE[cycle]
    prior_sen=0; prior_house=0; incumbent_sen=0
    terms=[]
    for t in person.get('terms',[]):
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
    a=auto_by[race]
    for side in ['D','R']:
        sl=side.lower()
        name=r[f'{sl}_side_candidate']
        auto_sen=1 if truth(a[f'{sl}_senate_prior_election_win']) else 0
        auto_house=1 if truth(a[f'{sl}_house_prior_election_win']) else 0
        auto_inc=1 if truth(a[f'{sl}_incumbency_election_history_proxy']) else 0
        p,top,second,status=match(name,state)
        rec={
            'race_id':race,'cycle':cycle,'state_abbrev':state,'side':side,'candidate_name':name,
            'auto_prior_senate':auto_sen,'auto_prior_house':auto_house,'auto_incumbency_proxy':auto_inc,
            'match_status':status,'match_score':f'{top:.4f}','second_score':f'{second:.4f}','match_margin':f'{top-second:.4f}',
            'matched_name':'','bioguide':'',
            'term_prior_senate':'','term_prior_house':'','term_senate_incumbent':'',
            'senate_flag_diff':'','house_flag_diff':'','incumbency_flag_diff':'','terms':''
        }
        discrepancy=False
        if p:
            n=p.get('name',{})
            rec['matched_name']=n.get('official_full') or (n.get('first','')+' '+n.get('last','')).strip()
            rec['bioguide']=p.get('id',{}).get('bioguide','')
            ps,ph,inc,terms=term_flags(p,cycle)
            rec['term_prior_senate']=ps; rec['term_prior_house']=ph; rec['term_senate_incumbent']=inc; rec['terms']=terms
            rec['senate_flag_diff']=ps-auto_sen
            rec['house_flag_diff']=ph-auto_house
            rec['incumbency_flag_diff']=inc-auto_inc
            discrepancy = (ps!=auto_sen) or (ph!=auto_house) or (inc!=auto_inc)
        expected = bool(auto_sen or auto_house or auto_inc)
        needs_review = (status=='AMBIGUOUS') or (expected and p is None) or discrepancy
        rec['needs_review']=str(needs_review).lower()
        rows.append(rec)
        if needs_review: reviews.append(rec.copy())

fields=list(rows[0].keys())
for path,data in [(OUT,rows),(REVIEW,reviews)]:
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)

matched=sum(bool(r['matched_name']) for r in rows)
discrep=sum(r['needs_review']=='true' and bool(r['matched_name']) for r in rows)
unmatched_expected=sum((r['needs_review']=='true' and not r['matched_name']) for r in rows)
lines=[
    '# GitHub Actions run: congressional service cross-check',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    f'- Candidate-side rows: {len(rows)}',
    f'- Candidates matched to a Congress term record: {matched}/{len(rows)}',
    f'- Review rows: {len(reviews)}',
    f'- Matched rows with term-date vs election-history discrepancy: {discrep}',
    f'- Election-history expected Congress service but no accepted term-record match: {unmatched_expected}',
    '',
    '## Method correction',
    '',
    'The first implementation compared every candidate against every historical legislator and treated unmatched candidates as a generic problem. This version indexes candidates by normalized surname and treats unmatched candidates with no election-history congressional signal as normal non-members.',
    '',
    '## Purpose',
    '',
    'Actual congressional term dates are used to detect prior Senate service, prior House service, and Senate incumbency, including appointments that election-win history can miss.',
    '',
    '## Review rule',
    '',
    'A row is sent to review only when the name match is ambiguous, election history expects congressional service but no term record is accepted, or term-date flags disagree with election-history flags.',
    '',
    '## Limits',
    '',
    '- Governor experience remains separate.',
    '- Name matching is reconstruction logic; ambiguous cases are never silently accepted.',
    '',
    '## Outputs',
    '',
    '- data/processed/core_v2r_headline_congress_service_crosscheck.csv',
    '- data/processed/core_v2r_candidate_name_match_review.csv',
    '',
    '## Next',
    '',
    'Resolve the review rows and convert supported term-date corrections into an explicit candidate-experience override table before joining them to the design matrix.'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))