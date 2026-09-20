#!/usr/bin/env python3
import csv, io, urllib.request, re
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
OUT=ROOT/'experiments/external_candidate_signal/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0400_538-deluxe-minus-classic-signal.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

URL2018='https://projects.fivethirtyeight.com/congress-model-2018/senate_seat_forecast.csv'
URL2022='https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv'
ELECTION={2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def fetch(url):
    raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CoreV2R-external-signal/1.0'}),timeout=120).read()
    txt=raw.decode('utf-8-sig','replace')
    if '<html' in txt[:300].lower():raise RuntimeError('HTML returned instead of CSV: '+url)
    return list(csv.DictReader(io.StringIO(txt))),len(raw)
def pdate(s):
    s=(s or '').strip()
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None
def normseat(s):
    s=(s or '').upper().strip()
    # Normalize 2018/2022 district identifiers to ST-S1/ST-S2/ST-S3 when possible.
    m=re.search(r'([A-Z]{2}).*?S(?:ENATE)?[- _]?([123])',s)
    if m:return f'{m.group(1)}-S{m.group(2)}'
    m=re.search(r'([A-Z]{2})-S([123])',s)
    if m:return f'{m.group(1)}-S{m.group(2)}'
    return s
def branch_expression(r):
    for k in ['expression','model','version','type']:
        if k in r and r[k]:return r[k].strip().lower()
    return ''
def get_margin(r):
    for k in ['mean_netpartymargin','mean_predicted_margin','margin','voteshare_mean_Dparty']:
        if k in r and r[k] not in ('',None):
            try:
                v=float(r[k])
                if k=='voteshare_mean_Dparty':
                    # only usable if R counterpart exists
                    rk='voteshare_mean_Rparty'
                    if rk in r and r[rk] not in ('',None):return v-float(r[rk])
                    continue
                return v
            except:pass
    return None
def get_district(r):
    for k in ['district','race','seat','state']:
        if k in r and r[k]:
            x=r[k].strip()
            if k=='state' and len(x)==2:return x
            return x
    return ''

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dm=load(DM)
dm_by={r['race_id']:r for r in dm}

sources={}
for cyc,url in [(2018,URL2018),(2022,URL2022)]:
    rows,nbytes=fetch(url)
    target=ELECTION[cyc]-timedelta(days=45)
    fields=list(rows[0].keys()) if rows else []
    # latest available forecast date <= 45-day snapshot, separately by expression/district
    usable=[]
    for r in rows:
        d=pdate(r.get('forecastdate') or r.get('date') or '')
        if d is None or d>target:continue
        ex=branch_expression(r)
        if ex not in {'classic','deluxe'}:continue
        m=get_margin(r)
        if m is None:continue
        usable.append((d,r,ex,m))
    if not usable:raise RuntimeError(f'No classic/deluxe rows for {cyc}; fields={fields}')
    latest=max(x[0] for x in usable)
    day=[x for x in usable if x[0]==latest]
    bydist=defaultdict(dict)
    for d,r,ex,m in day:
        dist=normseat(get_district(r))
        bydist[dist][ex]=m
    adj={}
    for dist,v in bydist.items():
        if 'classic' in v and 'deluxe' in v:
            adj[dist]=v['deluxe']-v['classic']
    sources[cyc]={'date':latest,'fields':fields,'adjustment':adj,'bytes':nbytes,'districts':len(adj)}

# map our race to external district. DM seat is commonly "Class 1" etc.
def ourdist(r):
    st=r['state_abbrev'].upper()
    seat=(r.get('seat') or '').lower()
    m=re.search(r'([123])',seat)
    if m:return f'{st}-S{m.group(1)}'
    return st

pred=[]
for r in base:
    cyc=int(r['test_cycle']);rid=r['race_id'];bpost=float(r['posterior']);actual=float(r['actual'])
    d=dm_by[rid];dist=ourdist(d)
    ext=0.0;extdate=''
    if cyc in sources:
        # direct district first, then state-only fallback if unique
        ext=sources[cyc]['adjustment'].get(dist,0.0)
        if ext==0.0:
            matches=[v for k,v in sources[cyc]['adjustment'].items() if k.startswith(d['state_abbrev'].upper())]
            if len(matches)==1:ext=matches[0]
        extdate=sources[cyc]['date'].isoformat()
    adjusted=bpost+ext
    pred.append({'test_cycle':cyc,'race_id':rid,'state_abbrev':r['state_abbrev'],'external_district':dist,
                 'external_forecast_date':extdate,'deluxe_minus_classic_margin':ext,
                 'baseline_posterior':bpost,'adjusted_posterior':adjusted,'actual':actual,
                 'baseline_correct':int((bpost>0)==(actual>0)),'adjusted_correct':int((adjusted>0)==(actual>0))})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [x for x in pred if x['test_cycle']==int(scope)]
    n=len(rr);b=sum(x['baseline_correct'] for x in rr);a=sum(x['adjusted_correct'] for x in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,
                    'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,
                    'nonzero_external_adjustments':sum(abs(x['deluxe_minus_classic_margin'])>1e-12 for x in rr)})

for fn,dat in [('external_signal_summary.csv',summary),('external_signal_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dat[0].keys()));w.writeheader();w.writerows(dat)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# 538 deluxe-minus-classic external candidate/context signal','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- This experiment does NOT import FiveThirtyEight win probabilities.',
'- It uses only the margin difference between the deluxe and classic model at the latest published date on or before the 45-day snapshot.',
'- The difference is treated as an external candidate/expert/context adjustment signal.',
'- 2014 has no corresponding source in the public repository and is left unchanged.','',
'## Source snapshots','']
for cyc in [2018,2022]:
    s=sources[cyc]
    lines.append(f"- {cyc}: snapshot used {s['date']}, matched classic/deluxe districts={s['districts']}, downloaded bytes={s['bytes']}")
    lines.append(f"- {cyc} fields: {', '.join(s['fields'])}")
lines += ['','## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | nonzero external |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['nonzero_external_adjustments']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, external adjustment={r['deluxe_minus_classic_margin']:+.2f}")
lines += ['','## Decision','',
'This is an external-signal experiment, not a pure internal Core V2-R model. Keep it separate unless it materially improves direction accuracy and the user chooses to allow externally produced candidate/expert adjustments in the production model.','',
'## Outputs','',
'- experiments/external_candidate_signal/results/external_signal_summary.csv',
'- experiments/external_candidate_signal/results/external_signal_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
