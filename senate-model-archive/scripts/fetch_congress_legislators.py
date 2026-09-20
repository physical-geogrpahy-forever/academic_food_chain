#!/usr/bin/env python3
from pathlib import Path
from urllib.request import urlopen
from datetime import datetime, timezone
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/raw/congress-legislators'
DOC = ROOT / 'docs/history/updates/2026-09-21_0120_congress-legislators-source-freeze.md'
OUT.mkdir(parents=True, exist_ok=True)
DOC.parent.mkdir(parents=True, exist_ok=True)

BASE = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/main/'
FILES = ['legislators-current.yaml', 'legislators-historical.yaml']
rows = []
for name in FILES:
    data = urlopen(BASE + name, timeout=60).read()
    path = OUT / name
    path.write_bytes(data)
    rows.append((name, len(data), hashlib.sha256(data).hexdigest()))

lines = [
    '# GitHub Actions run: congress-legislators source freeze',
    '',
    '- Generated UTC: ' + datetime.now(timezone.utc).isoformat(),
    '- Source repository: unitedstates/congress-legislators',
    '- Source branch: main',
    '- Purpose: authoritative-ish term-date cross-check for prior Senate and House service, including appointments not recoverable from election-win history alone.',
    '',
    '## Frozen files',
    '',
    '| file | bytes | sha256 |',
    '|---|---:|---|'
]
for name, size, sha in rows:
    lines.append(f'| {name} | {size} | `{sha}` |')
lines += [
    '',
    '## Rule',
    '',
    'These term records are used to audit congressional service only. Governor experience remains a separate source problem and is not inferred from congressional data.',
    '',
    '## Next',
    '',
    'Match the 198 headline candidates to legislator records and compare Senate/House service plus incumbency against the election-history proxy.'
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines))