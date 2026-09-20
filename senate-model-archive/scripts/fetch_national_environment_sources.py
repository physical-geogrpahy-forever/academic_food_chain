#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from datetime import datetime, timezone
import csv, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/processed/source_snapshots'
OUT.mkdir(parents=True,exist_ok=True)
DOC=ROOT/'docs/history/updates/2026-09-21_0152_national-environment-source-freeze.md'

GEN_COMMIT='4c1ff5e3aef1816ae04af63218015066e186c147'
GEN_URL=f'https://raw.githubusercontent.com/fivethirtyeight/data/{GEN_COMMIT}/congress-generic-ballot/generic_topline_historical.csv'
gen=urlopen(Request(GEN_URL,headers={'User-Agent':'CoreV2R-reconstruction/1.0'}),timeout=90).read()
(OUT/'generic_topline_historical_538_4c1ff5e3.csv').write_bytes(gen)

APP={
 'George W. Bush':'https://www.presidency.ucsb.edu/statistics/data/george-w-bush-public-approval',
 'Barack Obama':'https://www.presidency.ucsb.edu/statistics/data/barack-obama-public-approval',
 'Donald J. Trump I':'https://www.presidency.ucsb.edu/statistics/data/donald-j-trump-public-approval',
 'Joseph R. Biden Jr.':'https://www.presidency.ucsb.edu/statistics/data/joseph-r-biden-public-approval',
}

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_tr=False; self.in_cell=False; self.cell=[]; self.row=[]; self.rows=[]
    def handle_starttag(self,tag,attrs):
        if tag=='tr': self.in_tr=True; self.row=[]
        elif tag in ('td','th') and self.in_tr: self.in_cell=True; self.cell=[]
    def handle_data(self,data):
        if self.in_cell: self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.in_cell:
            self.row.append(re.sub(r'\s+',' ',' '.join(self.cell)).strip()); self.in_cell=False; self.cell=[]
        elif tag=='tr' and self.in_tr:
            if self.row: self.rows.append(self.row)
            self.in_tr=False

approval=[]; manifests=[]
for president,url in APP.items():
    raw=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 CoreV2R-reconstruction/1.0'}),timeout=90).read()
    sha=hashlib.sha256(raw).hexdigest()
    fname='app_'+re.sub(r'[^a-z0-9]+','_',president.lower()).strip('_')+'.html'
    (OUT/fname).write_bytes(raw)
    p=TableParser(); p.feed(raw.decode('utf-8','replace'))
    parsed=0
    for cells in p.rows:
        if len(cells)<5: continue
        sd,ed,ap,dis,uns=cells[:5]
        if not re.search(r'\d',sd) or not re.search(r'\d',ed): continue
        try:
            apf=float(ap); disf=float(dis)
        except: continue
        approval.append({'president':president,'start_date':sd,'end_date':ed,'approval':apf,'disapproval':disf,'unsure':uns,'source_url':url})
        parsed+=1
    manifests.append({'source':'American Presidency Project','president':president,'url':url,'sha256':sha,'bytes':len(raw),'parsed_rows':parsed})

if len(approval)<300:
    raise RuntimeError(f'Approval parser found only {len(approval)} total rows; refusing likely-broken parse')
with (OUT/'app_presidential_approval_historical.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(approval[0].keys())); w.writeheader(); w.writerows(approval)
with (OUT/'national_environment_source_manifest.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['source','president','url','sha256','bytes','parsed_rows']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    w.writerow({'source':'FiveThirtyEight generic ballot','president':'','url':GEN_URL,'sha256':hashlib.sha256(gen).hexdigest(),'bytes':len(gen),'parsed_rows':''})
    w.writerows(manifests)

lines=[
 '# GitHub Actions run: National environment source freeze','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- FiveThirtyEight generic-ballot source commit: '+GEN_COMMIT,
 '- FiveThirtyEight generic-ballot blob expected from repository audit: 6a341f0ef020f9d8a46a45c5a2380d8215da866e',
 f'- Generic-ballot raw bytes: {len(gen)}',
 f'- Parsed presidential-approval rows: {len(approval)}','',
 '## Sources','',
 '- FiveThirtyEight historical generic-ballot topline, preserved from the pinned GitHub commit.',
 '- American Presidency Project public-approval tables for George W. Bush, Barack Obama, Donald Trump first term, and Joseph Biden. The prior-president tables are historical series; raw HTML is frozen with SHA256 for reproducibility.','',
 '## Important','',
 'These are source components only. They do not define the final Core V2 National_t factor. Component weighting and latent-factor construction remain unrecovered and must not be tuned on headline test outcomes.','',
 '## Outputs','',
 '- data/processed/source_snapshots/generic_topline_historical_538_4c1ff5e3.csv',
 '- data/processed/source_snapshots/app_presidential_approval_historical.csv',
 '- data/processed/source_snapshots/national_environment_source_manifest.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))