#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'data/processed/historical_senate_race_audit.csv'
EXC = ROOT / 'data/processed/historical_senate_oos_exception_races.csv'
OUT = ROOT / 'data/processed/headline_sample_size_inference.csv'
HYP = ROOT / 'data/processed/headline_exception_rule_hypothesis_A.csv'
DOC = ROOT / 'docs/history/updates/2026-09-21_0051_headline-sample-size-inference.md'

with AUDIT.open('r', encoding='utf-8-sig', newline='') as f:
    audit = list(csv.DictReader(f))
with EXC.open('r', encoding='utf-8-sig', newline='') as f:
    exc = list(csv.DictReader(f))

headline = [r for r in audit if int(r['cycle']) in {2014, 2018, 2022}]
N = len(headline)
targets = [90.9, 91.9]

def fmt1(x):
    return float(f'{x:.1f}')

candidates = []
for n in range(1, N + 1):
    ks = []
    ok = True
    for target in targets:
        hit = [k for k in range(n + 1) if fmt1(100.0 * k / n) == target]
        if not hit:
            ok = False
            break
        ks.append(hit)
    if ok:
        candidates.append((n, ks[0], ks[1]))

with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['headline_total_general_races','candidate_denominator','correct_for_90_9','correct_for_91_9','implied_exclusions'])
    for n, k1, k2 in candidates:
        w.writerow([N, n, ';'.join(map(str,k1)), ';'.join(map(str,k2)), N-n])

headline_exc = [r for r in exc if r['headline_cycle'] == 'true']
irregular = []
for r in headline_exc:
    reasons = set(r['reasons'].split(';'))
    if reasons & {'non_unique_or_missing_D_R','winner_not_major_party','ranked_choice','missing_votes'}:
        irregular.append(r)

include_pairs = {(2018,'ME'), (2018,'VT')}
exclude_pairs = {(2014,'AL'), (2014,'KS'), (2018,'CA'), (2022,'AK'), (2022,'UT')}
hyp_rows = []
for r in irregular:
    key = (int(r['cycle']), r['state_abbrev'])
    if key in include_pairs:
        decision = 'INCLUDE_AS_DEM_ALIGNED_INDEPENDENT_HYPOTHESIS'
    elif key in exclude_pairs:
        decision = 'EXCLUDE_HYPOTHESIS'
    else:
        decision = 'UNRESOLVED'
    hyp_rows.append({
        'cycle': r['cycle'],
        'state_abbrev': r['state_abbrev'],
        'seat': r['seat'],
        'reasons': r['reasons'],
        'winner': r['winner'],
        'hypothesis_A_decision': decision
    })

with HYP.open('w', encoding='utf-8', newline='') as f:
    fields = ['cycle','state_abbrev','seat','reasons','winner','hypothesis_A_decision']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(hyp_rows)

unique = len(candidates) == 1
n = candidates[0][0] if unique else None
k90 = candidates[0][1] if unique else []
k91 = candidates[0][2] if unique else []
lines = [
    '# GitHub Actions run: headline validation sample-size inference',
    '',
    '- Generated UTC: ' + datetime.now(timezone.utc).isoformat(),
    '- Execution: GitHub Actions',
    f'- 2014/2018/2022 general-election race_id total: {N}',
    '- Preserved direction accuracies: 90.9% and 91.9%',
    '',
    '## Arithmetic inference',
    ''
]
if unique:
    lines += [
        f'- Unique denominator matching both one-decimal percentages: {n}',
        f'- 90.9% corresponds to {k90[0]}/{n}',
        f'- 91.9% corresponds to {k91[0]}/{n}',
        f'- Implied exclusions from the 104 general-race universe: {N-n}',
    ]
else:
    lines.append('- Denominator is not uniquely identified by the preserved percentages.')

lines += [
    '',
    'This inference assumes direction accuracy was an unweighted fraction of correctly called races and rounded to one decimal place. It is strong evidence, not proof of the original row filter.',
    '',
    '## Structurally irregular headline races',
    '',
    f'- Count: {len(irregular)}',
    '',
    '| cycle | state | reasons | winner |',
    '|---:|---|---|---|'
]
for r in irregular:
    lines.append(f"| {r['cycle']} | {r['state_abbrev']} | {r['reasons']} | {r['winner'].replace('|','/')} |")

lines += [
    '',
    '## Hypothesis A for the five implied exclusions',
    '',
    'If special elections and fusion-ballot races remain included, there are seven structurally irregular headline races. A 99-race denominator implies that exactly two of those seven were handled through a partisan-alignment rule rather than excluded.',
    '',
    'Hypothesis A includes 2018 Maine and 2018 Vermont as Democratic-aligned independents, and excludes 2014 Alabama, 2014 Kansas, 2018 California, 2022 Alaska, and 2022 Utah.',
    '',
    'Why this is plausible but not yet locked:',
    '- U.S. Senate party-division history for the 115th Congress reports two Independents, both caucusing with Democrats.',
    '- The two Independents serving in that Congress were Angus King of Maine and Bernie Sanders of Vermont.',
    '- FEC official results show Greg Orman as IND in the 2014 Kansas general election after the Democratic nominee withdrew.',
    '- FEC official results show the 2018 California general election was Democrat vs Democrat.',
    '- FEC official results show Evan McMullin as unaffiliated in the 2022 Utah general election.',
    '- Alaska official materials show the 2022 Senate contest used ranked-choice voting with multiple Republican candidates.',
    '',
    'Sources:',
    '- https://www.senate.gov/history/partydiv.htm/',
    '- https://www.fec.gov/documents/1698/2014senate.pdf',
    '- https://www.fec.gov/documents/2705/federalelections2018.pdf',
    '- https://www.fec.gov/documents/5675/federalelections2022.pdf',
    '- https://www.elections.alaska.gov/election-results/e/?id=22genr',
    '',
    '## Status',
    '',
    'Hypothesis A is a reconstruction candidate only. It is not authoritative until the downstream historical design matrix and OOS benchmark reproduce the preserved Core V2 metrics without post-election leakage.',
    '',
    '## Next',
    '',
    'Build a documented partisan-alignment map for non-major-party Senate candidates in 2006-2022, then regenerate the canonical historical target panel and verify that the headline row count is 99.'
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines[:35]))