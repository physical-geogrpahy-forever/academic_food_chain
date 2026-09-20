#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from datetime import datetime, timezone
import csv, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/processed/source_snapshots/nga_former_governors_snapshot.csv'
MAN=ROOT/'data/processed/source_snapshots/nga_former_governors_manifest.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0132_nga-former-governors-source-freeze.md'
URL='https://www.nga.org/former-governors/search/'

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_tr=False; self.in_td=False; self.cur=[]; self.cell=[]; self.rows=[]
    def handle_starttag(self,tag,attrs):
        if tag=='tr': self.in_tr=True; self.cur=[]
        elif tag in ('td','th') and self.in_tr: self.in_td=True; self.cell=[]
    def handle_data(self,data):
        if self.in_td: self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.in_td:
            txt=re.sub(r'\s+',' ',' '.join(self.cell)).strip()
            self.cur.append(txt); self.in_td=False; self.cell=[]
        elif tag=='tr' and self.in_tr:
            if self.cur: self.rows.append(self.cur)
            self.in_tr=False

req=Request(URL,headers={'User-Agent':'Mozilla/5.0 CoreV2R-reconstruction/1.0'})
raw=urlopen(req,timeout=90).read()
html=raw.decode('utf-8','replace')
p=TableParser(); p.feed(html)

rows=[]
for cells in p.rows:
    if len(cells)<4: continue
    name,state,terms,party=cells[:4]
    if 'Governor' in name and 'Time in Office' in terms: continue
    if not re.search(r'\b\d{4}\s*-\s*\d{4}\b',terms): continue
    name=re.sub(r'^Gov\.\s*','',name).strip()
    for start,end in re.findall(r'(\d{4})\s*-\s*(\d{4})',terms):
        rows.append({'governor_name':name,'state':state,'term_start_year':start,'term_end_year':end,'party':party})

if len(rows)<500:
    raise RuntimeError(f'NGA parser returned only {len(rows)} term rows; refusing to freeze likely-broken parse')

OUT.parent.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
sha=hashlib.sha256(raw).hexdigest()
with MAN.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['source_url','retrieved_utc','html_sha256','parsed_term_rows'])
    w.writeheader(); w.writerow({'source_url':URL,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'html_sha256':sha,'parsed_term_rows':len(rows)})
lines=[
 '# GitHub Actions run: NGA former-governors source freeze','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Source: National Governors Association former-governors search page',
 '- URL: '+URL,
 f'- HTML sha256: `{sha}`',
 f'- Parsed governor-term rows: {len(rows)}','',
 '## Use','',
 'This source is used only to audit whether a Senate candidate had gubernatorial service before the Senate election. The election-history flag remains the fallback when name matching is not accepted.','',
 '## Leakage guard','',
 'A governor term counts only when its start year is no later than the Senate election year and the term is chronologically relevant to that election. Later gubernatorial service in the current NGA snapshot does not create prior experience.','',
 '## Outputs','',
 '- data/processed/source_snapshots/nga_former_governors_snapshot.csv',
 '- data/processed/source_snapshots/nga_former_governors_manifest.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))