#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
from datetime import datetime, timezone
import csv, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
OUTDIR=ROOT/'data/processed/source_snapshots'
OUTDIR.mkdir(parents=True,exist_ok=True)
URL='https://apps.bea.gov/histdata/RegionalAccounts.html'
HTML=OUTDIR/'bea_regional_accounts_archive_index.html'
LINKS=OUTDIR/'bea_regional_accounts_archive_links.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0156_bea-regional-archive-discovery.md'

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag!='a': return
        d=dict(attrs); href=d.get('href')
        if href: self.links.append(href)

raw=urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0 CoreV2R-reconstruction/1.0'}),timeout=90).read()
HTML.write_bytes(raw)
text=raw.decode('utf-8','replace')
if 'Previously Published Estimates' not in text and 'Regional' not in text:
    raise RuntimeError('BEA archive page content validation failed')
p=LinkParser(); p.feed(text)
links=[]
for href in p.links:
    full=urljoin(URL,href)
    low=full.lower()
    links.append({'href':href,'url':full,'looks_data':str(any(x in low for x in ['.zip','.csv','.xlsx','.xls','download','regionalaccounts','histdata'])).lower()})
with LINKS.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['href','url','looks_data']); w.writeheader(); w.writerows(links)

data_like=[r for r in links if r['looks_data']=='true']
lines=[
 '# GitHub Actions run: BEA Regional Accounts archive discovery','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Source: '+URL,
 f'- HTML bytes: {len(raw)}',
 f'- HTML sha256: `{hashlib.sha256(raw).hexdigest()}`',
 f'- Anchor links discovered: {len(links)}',
 f'- Data/archive-looking links: {len(data_like)}','',
 '## Purpose','',
 'Core V2 RelativeEconomicGrowth must not use today revised historical SQINC1 values as if they were known at an earlier 45-day snapshot. This discovery freezes the official BEA previously-published-estimates index before selecting historical release vintages.','',
 '## Rule','',
 'No economic value is emitted by this step. A later step may select a vintage only if its publication/release date is on or before the relevant historical snapshot.','',
 '## Outputs','',
 '- data/processed/source_snapshots/bea_regional_accounts_archive_index.html',
 '- data/processed/source_snapshots/bea_regional_accounts_archive_links.csv','',
 '## Data-looking links sample',''
]
for r in data_like[:30]: lines.append('- '+r['url'])
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))