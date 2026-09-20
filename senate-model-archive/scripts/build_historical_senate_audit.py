#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OUTDIR = ROOT / 'data/processed'
DOC = ROOT / 'docs/history/updates/2026-09-21_0110_github-actions-historical-senate-audit.md'
OUTDIR.mkdir(parents=True, exist_ok=True)
DOC.parent.mkdir(parents=True, exist_ok=True)

def truth(v):
    return str(v).strip().lower() == 'true'

rows = []
with RAW.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        try:
            int(r['cycle'])
        except Exception:
            continue
        rows.append(r)

by_race = defaultdict(list)
for r in rows:
    by_race[r['race_id']].append(r)

audit_rows = []
standard_rows = []

for race_id, rr in by_race.items():
    first = rr[0]
    cand = {}
    for r in rr:
        cid = r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        name = r.get('candidate_name') or r.get('alt_result_text') or ''
        key = (cid, name)
        if key not in cand:
            cand[key] = {'name': name, 'votes': 0, 'missing': False, 'parties': set(), 'winner': False, 'unopposed': False, 'lines': 0}
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
        c['unopposed'] = c['unopposed'] or truth(r.get('unopposed', 'false'))

    dem = [c for c in cand.values() if 'DEM' in c['parties']]
    rep = [c for c in cand.values() if 'REP' in c['parties']]
    has_dem = len(dem) == 1
    has_rep = len(rep) == 1
    multiple_dem = len(dem) > 1
    multiple_rep = len(rep) > 1
    any_missing = any(c['missing'] for c in cand.values())
    any_unopposed = any(c['unopposed'] for c in cand.values())
    fusion = any(c['lines'] > 1 for c in cand.values())
    ranked = any((r.get('ranked_choice_round') or '').strip() for r in rr)
    special = truth(first.get('special', 'false'))

    d_votes = dem[0]['votes'] if has_dem else None
    r_votes = rep[0]['votes'] if has_rep else None
    two_party_total = (d_votes + r_votes) if d_votes is not None and r_votes is not None else None
    margin = ((d_votes - r_votes) / two_party_total * 100.0) if two_party_total else None
    standard = has_dem and has_rep and not multiple_dem and not multiple_rep and not any_missing and not any_unopposed and two_party_total and two_party_total > 0

    flags = []
    if special: flags.append('special')
    if not has_dem: flags.append('no_dem')
    if not has_rep: flags.append('no_rep')
    if multiple_dem: flags.append('multiple_dem')
    if multiple_rep: flags.append('multiple_rep')
    if any_missing: flags.append('missing_votes')
    if any_unopposed: flags.append('unopposed')
    if fusion: flags.append('fusion_or_multiline')
    if ranked: flags.append('ranked_choice')
    if not flags: flags.append('none')

    rec = {
        'race_id': race_id,
        'cycle': int(first['cycle']),
        'state_abbrev': first['state_abbrev'],
        'state': first['state'],
        'seat': first['office_seat_name'],
        'special': str(special).lower(),
        'candidate_count': len(cand),
        'has_dem': str(has_dem).lower(),
        'has_rep': str(has_rep).lower(),
        'd_votes': '' if d_votes is None else d_votes,
        'r_votes': '' if r_votes is None else r_votes,
        'two_party_total': '' if two_party_total is None else two_party_total,
        'margin_d_minus_r_pctpt': '' if margin is None else f'{margin:.8f}',
        'standard_dr_race': str(bool(standard)).lower(),
        'flags': ';'.join(flags),
        'source_count': len({r.get('source','') for r in rr if r.get('source','')})
    }
    audit_rows.append(rec)
    if standard:
        standard_rows.append(rec)

audit_rows.sort(key=lambda x: (x['cycle'], x['state_abbrev'], x['race_id']))
standard_rows.sort(key=lambda x: (x['cycle'], x['state_abbrev'], x['race_id']))
fields = list(audit_rows[0].keys())

for name, data in [('historical_senate_race_audit.csv', audit_rows), ('historical_senate_standard_dr_races.csv', standard_rows)]:
    with (OUTDIR / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)

def count_flag(flag):
    return sum(flag in r['flags'].split(';') for r in audit_rows)

cycles = sorted({r['cycle'] for r in audit_rows})
lines = [
    '# GitHub Actions run: historical Senate race audit',
    '',
    '- Generated UTC: ' + datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Input: data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv',
    '',
    '## Summary',
    '',
    f'- General-election race_id count: {len(audit_rows)}',
    f'- Mechanically standard D/R race count: {len(standard_rows)}',
    f'- Special-election races: {sum(r["special"] == "true" for r in audit_rows)}',
    f'- Races without a unique DEM candidate: {sum(r["has_dem"] == "false" for r in audit_rows)}',
    f'- Races without a unique REP candidate: {sum(r["has_rep"] == "false" for r in audit_rows)}',
    f'- Races with missing vote totals: {count_flag("missing_votes")}',
    f'- Unopposed races: {count_flag("unopposed")}',
    f'- Fusion or multi-line candidate races: {count_flag("fusion_or_multiline")}',
    f'- Ranked-choice records: {count_flag("ranked_choice")}',
    '',
    '## Cycle counts',
    '',
    '| cycle | all general races | mechanical standard D/R |',
    '|---:|---:|---:|'
]
for y in cycles:
    alln = sum(r['cycle'] == y for r in audit_rows)
    stdn = sum(r['cycle'] == y for r in standard_rows)
    lines.append(f'| {y} | {alln} | {stdn} |')

lines += [
    '',
    '## Interpretation',
    '',
    'This is a mechanical audit, not the final Core V2-R model panel.',
    'Independent-aligned candidates, special elections, fusion voting, ranked choice, unopposed races, and missing historical votes require explicit inclusion rules.',
    '',
    '## Next',
    '',
    'Extract exception races for 2006-2022 OOS and 2014/2018/2022 headline validation, then lock the inclusion rule.'
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines[:24]))