#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import datetime, timedelta, timezone

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'data/processed/source_snapshots/generic_topline_historical_538_4c1ff5e3.csv'
APP=ROOT/'data/processed/source_snapshots/app_presidential_approval_historical.csv'
OUT=ROOT/'data/processed/core_v2r_national_components_45d_audit.csv'
DOC=ROOT/'docs/history/updates/2026-09-21_0154_national-components-45d-audit.md'

ELECTION={
 2006:'2006-11-07',2008:'2008-11-04',2010:'2010-11-02',2012:'2012-11-06',2014:'2014-11-04',
 2016:'2016-11-08',2018:'2018-11-06',2020:'2020-11-03',2022:'2022-11-08'}
PRESIDENT={2006:'George W. Bush',2008:'George W. Bush',2010:'Barack Obama',2012:'Barack Obama',2014:'Barack Obama',2016:'Barack Obama',2018:'Donald J. Trump I',2020:'Donald J. Trump I',2022:'Joseph R. Biden Jr.'}
PRES_SIGN={2006:-1,2008:-1,2010:1,2012:1,2014:1,2016:1,2018:-1,2020:-1,2022:1}

def dt(s):
    for fmt in ['%Y-%m-%d','%m/%d/%Y','%m/%d/%y']:
        try: return datetime.strptime(s.strip(),fmt).date()
        except: pass
    raise ValueError(s)

with GEN.open('r',encoding='utf-8-sig',newline='') as f: gen=list(csv.DictReader(f))
with APP.open('r',encoding='utf-8-sig',newline='') as f: app=list(csv.DictReader(f))

g=[]
for r in gen:
    if r.get('subgroup')!='All polls': continue
    try: d=dt(r['modeldate'])
    except: continue
    g.append((d,r))

a=[]
for r in app:
    try: ed=dt(r['end_date'])
    except: continue
    a.append((r['president'],ed,r))

out=[]
for cyc,eds in ELECTION.items():
    election=dt(eds); snap=election-timedelta(days=45)
    gc=[x for x in g if x[0]<=snap]
    gr=max(gc,key=lambda x:x[0]) if gc else None
    pres=PRESIDENT[cyc]
    ac=[x for x in a if x[0]==pres and x[1]<=snap]
    ar=max(ac,key=lambda x:x[1]) if ac else None
    row={'cycle':cyc,'election_date':election.isoformat(),'snapshot_45d':snap.isoformat(),'president':pres,'president_party_sign_D_plus1_R_minus1':PRES_SIGN[cyc]}
    if gr:
        r=gr[1]; row.update({'generic_modeldate':gr[0].isoformat(),'generic_dem':r['dem_estimate'],'generic_rep':r['rep_estimate'],'generic_margin_d_minus_r':f"{float(r['dem_estimate'])-float(r['rep_estimate']):.8f}",'generic_lag_days':(snap-gr[0]).days})
    else:
        row.update({'generic_modeldate':'','generic_dem':'','generic_rep':'','generic_margin_d_minus_r':'','generic_lag_days':''})
    if ar:
        r=ar[2]; row.update({'approval_end_date':ar[1].isoformat(),'approval':r['approval'],'disapproval':r['disapproval'],'net_approval':f"{float(r['approval'])-float(r['disapproval']):.8f}",'approval_lag_days':(snap-ar[1]).days})
    else:
        row.update({'approval_end_date':'','approval':'','disapproval':'','net_approval':'','approval_lag_days':''})
    out.append(row)

fields=list(out[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)

lines=[
 '# GitHub Actions run: 45-day National component audit','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Cycles: 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022','',
 '## Rule','',
 'Snapshot date = federal general-election date minus 45 days.',
 'Generic ballot uses the latest FiveThirtyEight All polls topline modeldate on or before the snapshot.',
 'Approval uses the latest presidential-approval observation whose field end date is on or before the snapshot.','',
 '## Component availability','',
 '| cycle | snapshot | generic date | generic D-R | approval end | net approval |',
 '|---:|---|---|---:|---|---:|'
]
for r in out:
    gm=r['generic_margin_d_minus_r']; na=r['net_approval']
    lines.append(f"| {r['cycle']} | {r['snapshot_45d']} | {r['generic_modeldate'] or 'MISSING'} | {float(gm):.2f if False else gm or 'MISSING'} | {r['approval_end_date'] or 'MISSING'} | {na or 'MISSING'} |")
# replace invalid formatting artifact above by rebuilding table rows safely
lines=lines[:-len(out)]
for r in out:
    gm='MISSING' if not r['generic_margin_d_minus_r'] else f"{float(r['generic_margin_d_minus_r']):.2f}"
    na='MISSING' if not r['net_approval'] else f"{float(r['net_approval']):.2f}"
    lines.append(f"| {r['cycle']} | {r['snapshot_45d']} | {r['generic_modeldate'] or 'MISSING'} | {gm} | {r['approval_end_date'] or 'MISSING'} | {na} |")
lines += [
 '','## Status','',
 'These are National_t ingredients, not National_t itself. The exact Core V2 component standardization, weights, and any latent-factor model remain unrecovered. No weights are fit here.','',
 '## Output','',
 '- data/processed/core_v2r_national_components_45d_audit.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))