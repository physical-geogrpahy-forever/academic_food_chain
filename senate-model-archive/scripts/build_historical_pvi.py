#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv'
SEN = ROOT / 'data/processed/historical_senate_race_audit.csv'
OUTDIR = ROOT / 'data/processed'
DOC = ROOT / 'docs/history/updates/2026-09-21_0110_historical-pvi-panel.md'

STATES = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
}
VALID_PRES = STATES | {'DC'}

pres_rows = []
excluded_geos = defaultdict(int)
with SRC.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        st = (r.get('state_abbrev') or '').strip().upper()
        try:
            cyc = int(r['cycle'])
        except Exception:
            continue
        if cyc < 2000:
            continue
        if st not in VALID_PRES:
            if st:
                excluded_geos[(cyc, st)] += 1
            continue
        pres_rows.append(r)

by_state_cycle = defaultdict(list)
for r in pres_rows:
    by_state_cycle[(int(r['cycle']), r['state_abbrev'].upper())].append(r)

state_results = []
race_count_diagnostics = []
for (cycle, state), rr in sorted(by_state_cycle.items()):
    race_ids = sorted({r.get('race_id','') for r in rr})
    race_count_diagnostics.append((cycle, state, len(race_ids), ';'.join(race_ids)))

    cand = {}
    for r in rr:
        cid = r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or r.get('alt_result_text') or 'UNKNOWN'
        name = r.get('candidate_name') or r.get('alt_result_text') or ''
        key = (cid, name)
        if key not in cand:
            cand[key] = {'votes': 0, 'parties': set(), 'missing': False}
        c = cand[key]
        bp = (r.get('ballot_party') or '').strip().upper()
        pp = (r.get('party') or '').strip().upper()
        if bp:
            c['parties'].add(bp)
        if pp:
            c['parties'].add(pp)
        v = (r.get('votes') or '').strip()
        if not v:
            c['missing'] = True
        else:
            try:
                c['votes'] += int(float(v))
            except ValueError:
                c['missing'] = True

    d_votes = sum(c['votes'] for c in cand.values() if 'DEM' in c['parties'])
    r_votes = sum(c['votes'] for c in cand.values() if 'REP' in c['parties'])
    denom = d_votes + r_votes
    if denom <= 0:
        raise RuntimeError(f'No D/R two-party votes for {cycle} {state}')

    state_results.append({
        'cycle': cycle,
        'state_abbrev': state,
        'd_votes': d_votes,
        'r_votes': r_votes,
        'two_party_total': denom,
        'state_margin_d_minus_r_pctpt': (d_votes - r_votes) / denom * 100.0,
        'race_id_count': len(race_ids),
        'race_ids': ';'.join(race_ids),
    })

# Presidential general election must yield exactly 50 states + DC for each cycle.
cycles = sorted({r['cycle'] for r in state_results})
for cycle in cycles:
    got = {r['state_abbrev'] for r in state_results if r['cycle'] == cycle}
    missing = VALID_PRES - got
    extra = got - VALID_PRES
    if missing or extra or len(got) != 51:
        raise RuntimeError(f'Presidential geography validation failed for {cycle}: count={len(got)} missing={sorted(missing)} extra={sorted(extra)}')

# Statewide presidential general should map to one race_id per state-cycle.
multi_race = [(c,s,n,ids) for c,s,n,ids in race_count_diagnostics if n != 1]
if multi_race:
    raise RuntimeError('Multiple presidential general race_ids detected for state-cycle: ' + repr(multi_race[:10]))

national = {}
for cycle in cycles:
    rr = [r for r in state_results if r['cycle'] == cycle]
    dv = sum(r['d_votes'] for r in rr)
    rv = sum(r['r_votes'] for r in rr)
    national[cycle] = (dv - rv) / (dv + rv) * 100.0

lean = {}
for r in state_results:
    nm = national[r['cycle']]
    lv = r['state_margin_d_minus_r_pctpt'] - nm
    r['national_margin_d_minus_r_pctpt'] = nm
    r['lean_vs_national_pctpt'] = lv
    lean[(r['cycle'], r['state_abbrev'])] = lv

state_results.sort(key=lambda r: (r['cycle'], r['state_abbrev']))
with (OUTDIR / 'presidential_state_lean.csv').open('w', encoding='utf-8', newline='') as f:
    fields = ['cycle','state_abbrev','d_votes','r_votes','two_party_total','state_margin_d_minus_r_pctpt','national_margin_d_minus_r_pctpt','lean_vs_national_pctpt','race_id_count','race_ids']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in state_results:
        w.writerow({k: (f'{r[k]:.8f}' if isinstance(r[k], float) else r[k]) for k in fields})

with SEN.open('r', encoding='utf-8-sig', newline='') as f:
    senate = list(csv.DictReader(f))

pres_years = sorted(national)
pvi_rows = []
for s in senate:
    cyc = int(s['cycle'])
    st = s['state_abbrev'].upper()
    if st not in STATES:
        continue
    prev = [y for y in pres_years if y < cyc and (y, st) in lean]
    if len(prev) < 2:
        continue
    recent, older = prev[-1], prev[-2]
    lr, lo = lean[(recent, st)], lean[(older, st)]
    pvi = 0.67 * lr + 0.33 * lo
    pvi_rows.append({
        'race_id': s['race_id'],
        'cycle': cyc,
        'state_abbrev': st,
        'seat': s['seat'],
        'recent_pres_year': recent,
        'older_pres_year': older,
        'lean_recent_pctpt': lr,
        'lean_older_pctpt': lo,
        'pvi_default_067_033_pctpt': pvi,
    })

with (OUTDIR / 'historical_senate_pvi_default_067_033.csv').open('w', encoding='utf-8', newline='') as f:
    fields = ['race_id','cycle','state_abbrev','seat','recent_pres_year','older_pres_year','lean_recent_pctpt','lean_older_pctpt','pvi_default_067_033_pctpt']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in pvi_rows:
        w.writerow({k: (f'{r[k]:.8f}' if isinstance(r[k], float) else r[k]) for k in fields})

pvi26 = []
for st in sorted(STATES):
    if (2024, st) not in lean or (2020, st) not in lean:
        raise RuntimeError(f'Missing 2024/2020 presidential lean for 2026 state {st}')
    lr, lo = lean[(2024, st)], lean[(2020, st)]
    pvi26.append({
        'state_abbrev': st,
        'recent_pres_year': 2024,
        'older_pres_year': 2020,
        'lean_recent_pctpt': lr,
        'lean_older_pctpt': lo,
        'pvi_default_067_033_pctpt': 0.67 * lr + 0.33 * lo,
    })

with (OUTDIR / 'pvi_2026_default_067_033.csv').open('w', encoding='utf-8', newline='') as f:
    fields = ['state_abbrev','recent_pres_year','older_pres_year','lean_recent_pctpt','lean_older_pctpt','pvi_default_067_033_pctpt']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in pvi26:
        w.writerow({k: (f'{r[k]:.8f}' if isinstance(r[k], float) else r[k]) for k in fields})

excluded_geo_names = sorted({st for (_, st) in excluded_geos})
lines = [
    '# GitHub Actions run: historical PVI panel v2 — state filter fix',
    '',
    '- Generated UTC: ' + datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Fix: exclude presidential congressional-district rows such as M1/M2/N1/N2/N3 from state and national presidential margins',
    '- Presidential source repo: fivethirtyeight/election-results',
    '- Source commit: d7a7cff101da28f4ff77114450a964874800ca54',
    '- Source blob SHA: 0e4171053b71363a31669137cb9a86289e58d438',
    '',
    '## Geography correction',
    '',
    'Only the 50 states plus DC are used to construct the national presidential two-party margin. U.S. territories are excluded. Senate PVI output contains the 50 states only.',
    f'- Excluded non-state/DC abbreviations observed in source: {", ".join(excluded_geo_names) if excluded_geo_names else "none"}',
    '',
    '## Correction from v1',
    '',
    'The presidential source includes non-state congressional-district result rows used for electoral-vote allocation in Maine and Nebraska. The first reconstruction treated those rows as if they were additional states, producing 55 2026 PVI rows and slightly contaminating national presidential margins. v2 filters to the 50 states plus DC before calculating national margin and state lean.',
    '',
    'The v1 worklog is retained as an audit trail; its generated PVI files are superseded by this run.',
    '',
    '## Reconstruction rule',
    '',
    'For each Senate election cycle, use the two most recent presidential general elections strictly earlier than that Senate election. This prevents same-year presidential final results from leaking into a pre-election Senate forecast.',
    '',
    'State lean = state Democratic-minus-Republican two-party presidential margin minus national Democratic-minus-Republican two-party presidential margin.',
    '',
    'Reconstruction default PVI = 0.67 * recent lean + 0.33 * older lean.',
    '',
    'The 0.67/0.33 weights are preserved handoff defaults, not claimed recovered exact fitted weights.',
    '',
    '## Presidential state rows by cycle',
    '',
    '| presidential cycle | state + DC rows | national D-R two-party margin |',
    '|---:|---:|---:|'
]
for y in cycles:
    count = sum(r['cycle'] == y for r in state_results)
    lines.append(f'| {y} | {count} | {national[y]:.4f} |')
lines += [
    '',
    '## Outputs',
    '',
    '- data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv',
    '- data/processed/source_snapshots/presidential_source_manifest.csv',
    '- data/processed/presidential_state_lean.csv',
    '- data/processed/historical_senate_pvi_default_067_033.csv',
    '- data/processed/pvi_2026_default_067_033.csv',
    '',
    f'- Historical Senate race rows receiving PVI: {len(pvi_rows)}',
    f'- 2026 state PVI rows: {len(pvi26)} (expected 50)',
    '',
    '## Validation gates',
    '',
    '- Every presidential cycle must have exactly 51 state/DC rows.',
    '- Every state-cycle must have exactly one presidential general race_id.',
    '- 2026 PVI must have exactly 50 state rows.',
    '',
    '## Next',
    '',
    'Cross-check national presidential margins against FEC official results, then proceed to SameSeat construction after target-race alignment rules are locked.'
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines[:35]))