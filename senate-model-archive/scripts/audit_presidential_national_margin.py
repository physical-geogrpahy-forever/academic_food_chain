#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'data/processed/source_snapshots/election_results_presidential_d7a7cff101da.csv'
STATE = ROOT / 'data/processed/presidential_state_lean.csv'
OUT = ROOT / 'data/processed/presidential_national_margin_audit.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0112_presidential-national-margin-audit.md'

# Read state-summed national margins already produced by PVI builder.
state_sum = {}
with STATE.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        cyc = int(r['cycle'])
        state_sum.setdefault(cyc, float(r['national_margin_d_minus_r_pctpt']))

# Read explicit national general-election rows from the pinned source.
nat_rows = defaultdict(list)
with SRC.open('r', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if r.get('stage') != 'general':
            continue
        if (r.get('state_abbrev') or '').strip():
            continue
        try:
            cyc = int(r['cycle'])
        except Exception:
            continue
        if cyc >= 2000:
            nat_rows[cyc].append(r)

records = []
for cyc in sorted(state_sum):
    rr = nat_rows.get(cyc, [])
    cand = {}
    sources = set()
    for r in rr:
        cid = r.get('candidate_id') or r.get('politician_id') or r.get('candidate_name') or 'UNKNOWN'
        name = r.get('candidate_name') or ''
        key = (cid, name)
        if key not in cand:
            cand[key] = {'votes':0, 'parties':set()}
        c = cand[key]
        bp = (r.get('ballot_party') or '').strip().upper()
        pp = (r.get('party') or '').strip().upper()
        if bp: c['parties'].add(bp)
        if pp: c['parties'].add(pp)
        v = (r.get('votes') or '').strip()
        if v:
            try:
                c['votes'] += int(float(v))
            except ValueError:
                pass
        if r.get('source'): sources.add(r['source'])
    dv = sum(c['votes'] for c in cand.values() if 'DEM' in c['parties'])
    rv = sum(c['votes'] for c in cand.values() if 'REP' in c['parties'])
    explicit = ((dv-rv)/(dv+rv)*100.0) if dv+rv > 0 else None
    diff = (state_sum[cyc] - explicit) if explicit is not None else None
    records.append({
        'cycle':cyc,
        'state_sum_margin_pctpt':state_sum[cyc],
        'explicit_national_d_votes':dv,
        'explicit_national_r_votes':rv,
        'explicit_national_margin_pctpt':'' if explicit is None else explicit,
        'difference_pctpt':'' if diff is None else diff,
        'explicit_national_row_count':len(rr),
        'source_urls':' ; '.join(sorted(sources)),
        'status':'NO_NATIONAL_ROW' if explicit is None else ('OK' if abs(diff) <= 0.02 else 'MISMATCH')
    })

with OUT.open('w', encoding='utf-8', newline='') as f:
    fields=list(records[0].keys())
    w=csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in records:
        w.writerow({k:(f'{r[k]:.8f}' if isinstance(r[k],float) else r[k]) for k in fields})

lines=[
    '# GitHub Actions run: presidential national-margin audit',
    '',
    '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    '- Purpose: compare 50-state+DC aggregation against explicit national general-election rows in the same pinned source.',
    '',
    '| cycle | state-sum D-R two-party margin | explicit national margin | difference | status |',
    '|---:|---:|---:|---:|---|'
]
for r in records:
    e = 'NA' if r['explicit_national_margin_pctpt']=='' else f"{r['explicit_national_margin_pctpt']:.4f}"
    d = 'NA' if r['difference_pctpt']=='' else f"{r['difference_pctpt']:.4f}"
    lines.append(f"| {r['cycle']} | {r['state_sum_margin_pctpt']:.4f} | {e} | {d} | {r['status']} |")

bad=[r for r in records if r['status']=='MISMATCH']
lines += [
    '',
    '## Interpretation',
    '',
    'A mismatch means the state-level source cannot be assumed to reproduce the official national popular-vote total for that cycle. Such a cycle requires official FEC cross-check or correction before its national baseline is locked.',
    '',
    f'- Mismatch cycles: {", ".join(str(r["cycle"]) for r in bad) if bad else "none"}',
    '',
    '## Output',
    '',
    '- data/processed/presidential_national_margin_audit.csv',
    '',
    '## Next',
    '',
    'For mismatch or missing-national-row cycles, compare against the FEC official Federal Elections publication and store an explicit official national-margin table.'
]
DOC.write_text('\n'.join(lines)+'\n', encoding='utf-8')
print('\n'.join(lines))