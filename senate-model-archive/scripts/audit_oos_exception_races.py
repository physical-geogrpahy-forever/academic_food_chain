#!/usr/bin/env python3
import csv
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OUT = ROOT / 'data/processed/historical_senate_oos_exception_races.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0051_oos-exception-race-audit.md'
OUT.parent.mkdir(parents=True, exist_ok=True)
DOC.parent.mkdir(parents=True, exist_ok=True)

def truth(v):
    return str(v).strip().lower() == 'true'

rows = []
with RAW.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        try:
            cycle = int(r['cycle'])
        except Exception:
            continue
        if 2006 <= cycle <= 2022:
            rows.append(r)

by_race = defaultdict(list)
for r in rows:
    by_race[r['race_id']].append(r)

out = []
for race_id, rr in by_race.items():
    first = rr[0]
    cand = {}
    for r in rr:
        cid = r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        name = r.get('candidate_name') or r.get('alt_result_text') or ''
        key = (cid, name)
        if key not in cand:
            cand[key] = {'name': name, 'votes': 0, 'missing': False, 'parties': set(), 'winner': False, 'lines': 0}
        c = cand[key]
        c['lines'] += 1
        bp = (r.get('ballot_party') or '').strip().upper()
        if bp:
            c['parties'].add(bp)
        v = (r.get('votes') or '').strip()
        if v:
            try:
                c['votes'] += int(float(v))
            except ValueError:
                c['missing'] = True
        else:
            c['missing'] = True
        c['winner'] = c['winner'] or truth(r.get('winner', 'false'))

    dem = [c for c in cand.values() if 'DEM' in c['parties']]
    rep = [c for c in cand.values() if 'REP' in c['parties']]
    winners = [c for c in cand.values() if c['winner']]
    winner = winners[0] if len(winners) == 1 else None
    winner_major = bool(winner and (('DEM' in winner['parties']) or ('REP' in winner['parties'])))
    ranked = any((r.get('ranked_choice_round') or '').strip() for r in rr)
    fusion = any(c['lines'] > 1 for c in cand.values())
    special = truth(first.get('special', 'false'))
    missing = any(c['missing'] for c in cand.values())
    unique_dr = len(dem) == 1 and len(rep) == 1

    reasons = []
    if special: reasons.append('special')
    if not unique_dr: reasons.append('non_unique_or_missing_D_R')
    if not winner_major: reasons.append('winner_not_major_party')
    if ranked: reasons.append('ranked_choice')
    if fusion: reasons.append('fusion_or_multiline')
    if missing: reasons.append('missing_votes')

    if not reasons:
        continue

    if ranked:
        classification = 'FINAL_ROUND_RULE_REQUIRED'
    elif not winner_major:
        classification = 'MANUAL_PARTY_ALIGNMENT_REQUIRED'
    elif not unique_dr or missing:
        classification = 'MANUAL_RACE_RULE_REQUIRED'
    elif special:
        classification = 'SPECIAL_ELECTION_POLICY_REQUIRED'
    elif fusion:
        classification = 'SAFE_IF_AGGREGATE_SAME_CANDIDATE'
    else:
        classification = 'REVIEW'

    def label(c):
        if not c:
            return ''
        p = '/'.join(sorted(c['parties'])) if c['parties'] else 'NONE'
        return f"{c['name']} [{p}] {c['votes']}"

    candidates = ' | '.join(sorted(label(c) for c in cand.values()))
    out.append({
        'race_id': race_id,
        'cycle': int(first['cycle']),
        'state_abbrev': first['state_abbrev'],
        'state': first['state'],
        'seat': first['office_seat_name'],
        'special': str(special).lower(),
        'headline_cycle': str(int(first['cycle']) in {2014,2018,2022}).lower(),
        'classification': classification,
        'reasons': ';'.join(reasons),
        'winner': label(winner),
        'dem_candidate': label(dem[0]) if len(dem) == 1 else '',
        'rep_candidate': label(rep[0]) if len(rep) == 1 else '',
        'all_candidates': candidates
    })

out.sort(key=lambda x: (x['cycle'], x['state_abbrev'], x['race_id']))
fields = list(out[0].keys()) if out else []
with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(out)

counts = Counter(r['classification'] for r in out)
headline = [r for r in out if r['headline_cycle'] == 'true']
lines = [
    '# GitHub Actions run: 2006-2022 Senate exception-race audit',
    '',
    '- Generated UTC: ' + datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Scope: all general-election records with cycle 2006 through 2022, including odd-year special cycles',
    '',
    '## Why this audit was added',
    '',
    'The first mechanical D/R audit can misclassify races where a non-major-party candidate wins even though both DEM and REP candidates are present. Ranked-choice records also require final-round handling rather than naive summation across rounds.',
    '',
    '## Exception counts',
    ''
]
for k in sorted(counts):
    lines.append(f'- {k}: {counts[k]}')
lines += [
    '',
    f'- Total exception/review races: {len(out)}',
    f'- Headline-cycle exceptions (2014, 2018, 2022): {len(headline)}',
    '',
    '## Headline-cycle exception races',
    '',
    '| cycle | state | seat | class | reasons | winner |',
    '|---:|---|---|---|---|---|'
]
for r in headline:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['seat']} | {r['classification']} | {r['reasons']} | {r['winner'].replace('|','/')} |")
lines += [
    '',
    '## Provisional handling rules',
    '',
    '1. Fusion or multi-line only: aggregate ballot lines belonging to the same candidate; do not treat them as separate candidates.',
    '2. Ranked choice: do not sum across rounds; use the final certified round/result.',
    '3. Winner not major party: require explicit partisan alignment or a documented exclusion rule before constructing D-minus-R margin.',
    '4. Special election: keep separate until the original Core V2 inclusion policy is recovered or reproduced by OOS comparison.',
    '5. Missing D/R or missing votes: manual rule required; never silently coerce to zero.',
    '',
    '## Output',
    '',
    '- data/processed/historical_senate_oos_exception_races.csv',
    '',
    '## Next',
    '',
    'Resolve the headline-cycle exceptions first, then compare inclusion-rule variants by historical OOS without using 2026 outcomes.'
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines[:40]))