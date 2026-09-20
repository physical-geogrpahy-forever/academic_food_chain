#!/usr/bin/env python3
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / 'data/processed/source_snapshots'
OUTDIR.mkdir(parents=True, exist_ok=True)
COMMIT = 'd7a7cff101da28f4ff77114450a964874800ca54'
BLOB = '0e4171053b71363a31669137cb9a86289e58d438'
URL = f'https://raw.githubusercontent.com/fivethirtyeight/election-results/{COMMIT}/election_results_presidential.csv'
DEST = OUTDIR / f'election_results_presidential_{COMMIT[:12]}.csv'
MANIFEST = OUTDIR / 'presidential_source_manifest.csv'

req = Request(URL, headers={'User-Agent':'Core-V2-R-reconstruction'})
with urlopen(req, timeout=120) as resp:
    data = resp.read()
if len(data) < 1000000 or not data.startswith(b'id,race_id,state_abbrev'):
    raise RuntimeError('Downloaded presidential source failed size/header validation')
DEST.write_bytes(data)
sha256 = hashlib.sha256(data).hexdigest()
MANIFEST.write_text(
    'source_repo,source_path,source_commit,source_blob_sha,sha256,bytes,archive_path\n'
    + f'fivethirtyeight/election-results,election_results_presidential.csv,{COMMIT},{BLOB},{sha256},{len(data)},{DEST.relative_to(ROOT)}\n',
    encoding='utf-8'
)
print(f'Frozen presidential source: {DEST}')
print(f'bytes={len(data)} sha256={sha256}')