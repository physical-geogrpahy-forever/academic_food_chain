#!/usr/bin/env python3
import csv, io, re, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'experiments/third_party_poll_audit/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0480_third-party-poll-source-audit.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

URL='https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'
raw=urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'CoreV2R-third-party-audit/1.0'}),timeout=240).read()
text=raw.decode('utf-8-sig','replace')
rows=list(csv.DictReader(io.StringIO(text)))
fields=list(rows[0].keys()) if rows else []
cand_cols=[f for f in fields if re.search(r'(cand|candidate|party|pct|vote|margin)',f,re.I)]

nc=[]
for r in rows:
    yr=str(r.get('year') or r.get('cycle') or '')
    typ=' '.join(str(r.get(k) or '') for k in ['type_simple','type_detail','race','office_type','office'])
    state=' '.join(str(r.get(k) or '') for k in ['state','state_abbrev'])
    if '2014' not in yr: continue
    if 'sen' not in typ.lower(): continue
    if not (state.strip()=='NC' or 'north carolina' in state.lower()): continue
    nc.append(r)

multi_capable=False
multi_reason=[]
if all(f in fields for f in ['candidate_name','candidate_party','pct']):
    multi_capable=True;multi_reason.append('long candidate-level schema')
if any(re.search(r'(cand|candidate)3',f,re.I) for f in fields):
    multi_capable=True;multi_reason.append('third-candidate wide columns')

haugh=[]
for r in nc:
    blob=' | '.join(str(r.get(f) or '') for f in fields)
    low=blob.lower()
    if 'haugh' in low or 'libertarian' in low:
        haugh.append(r)

keep=['poll_id','question_id','year','cycle','state','state_abbrev','race_id','pollster','polldate','start_date','end_date',
      'type_simple','type_detail','race','office_type','candidate_name','candidate_party','party','pct',
      'cand1_name','cand1_party','cand1_pct','cand2_name','cand2_party','cand2_pct','cand3_name','cand3_party','cand3_pct',
      'margin_poll','samplesize','sample_size']
keep=[k for k in keep if k in fields]
audit=[{k:r.get(k,'') for k in keep} for r in nc[:500]]
if audit:
    with (OUT/'nc2014_senate_raw_poll_rows.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keep);w.writeheader();w.writerows(audit)

meta=[{
 'source_url':URL,'bytes':len(raw),'rows':len(rows),'field_count':len(fields),
 'multi_candidate_capable':multi_capable,'multi_candidate_reason':';'.join(multi_reason),
 'nc2014_senate_rows':len(nc),'nc2014_haugh_or_libertarian_rows':len(haugh)
}]
with (OUT/'third_party_source_meta.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(meta[0].keys()));w.writeheader();w.writerows(meta)

lines=[
'# Third-party Senate poll source audit','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
f'- Source: {URL}',f'- Bytes: {len(raw)}',f'- Rows: {len(rows)}',f'- Field count: {len(fields)}','',
'## Schema','',
', '.join(fields),'',
'## Candidate/result-like fields','',
', '.join(cand_cols),'',
'## Multi-candidate capability','',
f'- Capable: {multi_capable}',
f'- Reason: {"; ".join(multi_reason) if multi_reason else "no explicit third-candidate representation detected"}','',
'## North Carolina 2014 Senate','',
f'- Matching Senate rows: {len(nc)}',
f'- Rows explicitly containing Haugh or Libertarian text: {len(haugh)}',''
]
if haugh:
    lines += ['### Haugh/Libertarian rows (compact)','']
    for r in haugh[:20]:
        bits=[f'{k}={r.get(k,"")}' for k in keep if r.get(k,'')!='']
        lines.append('- '+'; '.join(bits))
else:
    lines += ['No explicit Haugh/Libertarian row was found in this source. If the schema is only two-candidate, a different archived poll source is required for a true D/R/T layer.','']
lines += ['## Decision rule','',
'If explicit third-candidate support exists, build a historical third-party-aware poll layer from this source. If not, do not fabricate third-party poll shares; locate another archived source or limit the next step to a source-coverage audit.','',
'## Outputs','',
'- experiments/third_party_poll_audit/results/third_party_source_meta.csv',
'- experiments/third_party_poll_audit/results/nc2014_senate_raw_poll_rows.csv (if rows exist)'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
