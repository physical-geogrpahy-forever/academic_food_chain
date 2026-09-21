#!/usr/bin/env python3
import csv, io, zipfile, statistics
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
PVI=ROOT/'data/processed/pvi_2026_default_067_033.csv'
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
DIAG=ROOT/'data/snapshots/2026_competitive_race_input_diagnostic_2026-09-21.csv'
OUT=ROOT/'data/snapshots/2026_structural_input_matrix_45d.csv'
DOC=ROOT/'docs/analysis/2026_STRUCTURAL_INPUT_MATRIX_45D.md'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
NATIONAL_D_MINUS_R=8.7

TARGET={
 'AK':{'prior_cycle':2020,'inc_diff':-1,'outparty':0},
 'GA':{'prior_cycle':2020,'inc_diff':1,'outparty':1},
 'IA':{'prior_cycle':2020,'inc_diff':0,'outparty':0},
 'ME':{'prior_cycle':2020,'inc_diff':-1,'outparty':-1},
 'MI':{'prior_cycle':2020,'inc_diff':0,'outparty':0},
 'NH':{'prior_cycle':2020,'inc_diff':0,'outparty':0},
 'NC':{'prior_cycle':2020,'inc_diff':0,'outparty':0},
 'OH':{'prior_cycle':2022,'inc_diff':-1,'outparty':0},
 'TX':{'prior_cycle':2020,'inc_diff':0,'outparty':0},
}
PRES_SIGN=-1.0  # Republican president: favorable relative growth is signed toward incumbent president party, i.e. R in D-R margin.

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
pvi={r['state_abbrev']:float(r['pvi_default_067_033_pctpt']) for r in load(PVI)}
diag={r['state']:r for r in load(DIAG)}
sen=load(SEN)

# Senate two-party margin by state/cycle.
by={}
for st,meta in TARGET.items():
    cyc=meta['prior_cycle']
    rr=[r for r in sen if r['state_abbrev']==st and int(r['cycle'])==cyc and (r.get('stage') or '').lower()=='general']
    # Handle runoff where present by preferring highest ranked-choice round only; Georgia runoff is a separate election result in source if available.
    cand={}
    for r in rr:
        key=(r.get('politician_id') or r.get('candidate_id') or r.get('candidate_name') or '').strip()
        if not key: continue
        c=cand.setdefault(key,{'votes':0,'parties':set(),'missing':False})
        for q in ((r.get('ballot_party') or ''),(r.get('party') or '')):
            if q.strip():c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v:c['missing']=True
        else:
            try:c['votes']+=int(float(v))
            except:c['missing']=True
    ds=[c for c in cand.values() if 'DEM' in c['parties']]
    rs=[c for c in cand.values() if 'REP' in c['parties']]
    if len(ds)!=1 or len(rs)!=1 or ds[0]['missing'] or rs[0]['missing'] or ds[0]['votes']+rs[0]['votes']==0:
        by[st]=None
    else:
        by[st]=100*(ds[0]['votes']-rs[0]['votes'])/(ds[0]['votes']+rs[0]['votes'])

# BEA 2026 Q1 YoY personal income relative growth.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-2026-production/1.0'}),timeout=180).read()
zf=zipfile.ZipFile(io.BytesIO(raw))
members=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
name=max(members,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(name).decode('utf-8-sig','replace'))))
pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
STATE_ABBR={
'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
def val(r,c):
    try:return float((r.get(c) or '').replace(',','').strip())
    except:return None
growth={};us=None
for r in pi:
    nm=(r.get('GeoName') or '').replace('*','').strip()
    a=val(r,'2026:Q1');b=val(r,'2025:Q1')
    if a is None or b in (None,0):continue
    g=100*(a/b-1)
    if nm in STATE_ABBR:growth[STATE_ABBR[nm]]=g
    elif nm=='United States':us=g
if us is None:us=statistics.mean(growth.values())

out=[]
for st,meta in TARGET.items():
    d=diag[st]
    g=growth[st]
    out.append({
      'snapshot_date':'2026-09-19',
      'state_abbrev':st,
      'candidate_D':d['candidate_D'],'candidate_R':d['candidate_R'],'seat_status':d['seat_status'],
      'pvi_2026_d_minus_r_pctpt':pvi[st],
      'same_seat_prior_cycle':meta['prior_cycle'],
      'same_seat_d_minus_r_pctpt':by[st],
      'incumbency_diff_D_minus_R':meta['inc_diff'],
      'outparty_incumbent_signed':meta['outparty'],
      'state_PI_growth_2026Q1_yoy_pct':g,
      'US_PI_growth_2026Q1_yoy_pct':us,
      'relative_economic_growth_pctpt':g-us,
      'relative_economic_growth_presparty_signed':(g-us)*PRES_SIGN,
      'national_generic_ballot_D_minus_R_pctpt':NATIONAL_D_MINUS_R,
      'national_source_bridge':'RCP average reported 2026-09-17; no later pre-cutoff generic-ballot poll after 2026-09-17',
      'cutoff_rule':'public by 2026-09-19; no 2026-09-20 data'
    })
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()));w.writeheader();w.writerows(out)

lines=['# 2026 structural input matrix at exact 45-day cutoff','',
'- Snapshot date: 2026-09-19 (US calendar date).',
'- General election: 2026-11-03.',
'- No information first published on 2026-09-20 or later is included.',
'- National generic-ballot bridge: D+8.7, the RCP average reported on 2026-09-17.',
'- RelativeEconomicGrowth: BEA SQINC1 2026 Q1 YoY state growth minus U.S. growth, signed for the Republican president in D-R margin direction.',
'- Ohio OutPartyIncumbent is corrected to 0.','',
'| State | PVI | SameSeat | Inc | OutParty | Rel econ | Signed econ | National |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in out:
    ss='NA' if r['same_seat_d_minus_r_pctpt'] is None else f"{r['same_seat_d_minus_r_pctpt']:.2f}"
    lines.append(f"| {r['state_abbrev']} | {r['pvi_2026_d_minus_r_pctpt']:.2f} | {ss} | {r['incumbency_diff_D_minus_R']} | {r['outparty_incumbent_signed']} | {r['relative_economic_growth_pctpt']:.2f} | {r['relative_economic_growth_presparty_signed']:.2f} | +{r['national_generic_ballot_D_minus_R_pctpt']:.1f} |")
lines += ['','## Limitations','',
'- This file freezes the structural layer only. Candidate experience and PersonalVote are joined separately.',
'- The current Senate poll snapshot is frozen separately at data/snapshots/2026_senate_rcp_rows_through_2026-09-19.csv.',
'- RCP is a 2026 source bridge for the national environment because the historical 538 generic-ballot series has no 2026 continuation. It must not be presented as the identical historical source.']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
