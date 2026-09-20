#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import csv

ROOT=Path(__file__).resolve().parents[1]
OUTDIR=ROOT/'data/processed/source_snapshots'
OUTDIR.mkdir(parents=True,exist_ok=True)
COMMIT='d7a7cff101da28f4ff77114450a964874800ca54'
SOURCES=[
    ('election_results_house.csv','562c150fe6e375b73c9a8876b042ccdfc12aa45e'),
    ('election_results_gubernatorial.csv','575b4382ccf52917f634de784c7be8d01a0011ba'),
]

def git_blob_sha(data):
    h=hashlib.sha1()
    h.update(f'blob {len(data)}\0'.encode())
    h.update(data)
    return h.hexdigest()

manifest=[]
for name,expected_blob in SOURCES:
    url=f'https://raw.githubusercontent.com/fivethirtyeight/election-results/{COMMIT}/{name}'
    req=Request(url,headers={'User-Agent':'Core-V2-R-reconstruction'})
    with urlopen(req,timeout=180) as resp: data=resp.read()
    if not data.startswith(b'id,race_id,state_abbrev'):
        raise RuntimeError(f'Header validation failed for {name}')
    actual_blob=git_blob_sha(data)
    if actual_blob!=expected_blob:
        raise RuntimeError(f'Git blob mismatch for {name}: expected {expected_blob}, got {actual_blob}')
    dest=OUTDIR/f'{Path(name).stem}_{COMMIT[:12]}.csv'
    dest.write_bytes(data)
    manifest.append({
        'source_repo':'fivethirtyeight/election-results','source_path':name,'source_commit':COMMIT,
        'expected_blob_sha':expected_blob,'actual_blob_sha':actual_blob,'sha256':hashlib.sha256(data).hexdigest(),
        'bytes':len(data),'archive_path':str(dest.relative_to(ROOT))
    })

with (OUTDIR/'candidate_experience_source_manifest.csv').open('w',encoding='utf-8',newline='') as f:
    fields=list(manifest[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(manifest)
print('Frozen and verified candidate experience sources:')
for r in manifest: print(r)