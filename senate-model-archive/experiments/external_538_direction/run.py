#!/usr/bin/env python3
import csv,io,urllib.request,re
from collections import defaultdict
from pathlib import Path
from datetime import datetime,date,timedelta,timezone

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
OUT=ROOT/'experiments/external_538_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0410_external-538-direction-headroom.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

URL18='https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/fivethirtyeight/senate_seat_forecast.csv'
URL22='https://raw.githubusercontent.com/stephensond/election-night-2022/83f2c9867f319b921fa10ad04bc256d8106bc8f4/input/senate_state_toplines_2022.csv'
ELECTION={2018:date(2018,11,6),2022:date(2022,11,8)}

def fetch(url):
    raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CoreV2R-extdir/1.0'}),timeout=120).read()
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))
def pdate(s):
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime((s or '').strip(),fmt).date()
        except:pass
    return None
def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

# 2018 D-R forecast margins by state/class/model at 45-day snapshot.
r18=fetch(URL18); t18=ELECTION[2018]-timedelta(days=45)
u18=[]
for r in r18:
    d=pdate(r.get('forecastdate'))
    if d is None or d>t18:continue
    model=(r.get('model') or '').lower().strip()
    if model not in {'lite','classic','deluxe'}:continue
    party=(r.get('party') or '').upper().strip()
    if party not in {'D','R'}:continue
    try:vs=float(r.get('voteshare') or '')
    except:continue
    u18.append((d,(r.get('state') or '').upper().strip(),str(r.get('class') or '').strip(),model,party,vs))
latest18=max(x[0] for x in u18)
g18=defaultdict(dict)
for d,st,cl,model,party,vs in u18:
    if d==latest18:g18[(st,cl,model)][party]=vs
m18=defaultdict(dict)
for (st,cl,model),v in g18.items():
    if 'D' in v and 'R' in v:m18[st][model]=v['D']-v['R']

# 2022 direct model margins by district/expression.
r22=fetch(URL22); t22=ELECTION[2022]-timedelta(days=45)
u22=[]
for r in r22:
    d=pdate(r.get('forecastdate'))
    if d is None or d>t22:continue
    ex=(r.get('expression') or '').lower().strip().lstrip('_')
    if ex not in {'lite','classic','deluxe'}:continue
    try:m=float(r.get('mean_netpartymargin') or '')
    except:continue
    dist=(r.get('district') or '').upper().strip()
    u22.append((d,dist,ex,m))
latest22=max(x[0] for x in u22)
m22=defaultdict(dict)
for d,dist,ex,m in u22:
    if d==latest22:m22[dist[:2]][ex]=m

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
rows=[]
for r in base:
    cyc=int(r['test_cycle'])
    if cyc not in {2018,2022}:continue
    st=r['state_abbrev'];actual=float(r['actual']);bp=float(r['posterior'])
    models=m18.get(st,{}) if cyc==2018 else m22.get(st,{})
    row={'cycle':cyc,'state':st,'race_id':r['race_id'],'actual':actual,'baseline':bp,
         'baseline_correct':int((bp>0)==(actual>0))}
    for model in ['lite','classic','deluxe']:
        val=models.get(model,'')
        row[model+'_margin']=val
        row[model+'_correct']='' if val=='' else int((float(val)>0)==(actual>0))
    rows.append(row)

summary=[]
for cyc in [2018,2022]:
    rr=[r for r in rows if r['cycle']==cyc]
    for model in ['baseline','lite','classic','deluxe']:
        vals=[]
        for r in rr:
            if model=='baseline':vals.append(r['baseline_correct'])
            elif r[model+'_correct']!='':vals.append(int(r[model+'_correct']))
        summary.append({'cycle':cyc,'model':model,'n':len(vals),'correct':sum(vals),'accuracy_pct':100*sum(vals)/len(vals) if vals else ''})

wrong=[r for r in rows if not r['baseline_correct']]
for fn,data in [('external_direction_summary.csv',summary),('external_direction_races.csv',rows),('baseline_wrong_external_signals.csv',wrong)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

lines=['# External 538 direction headroom diagnostic','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Diagnostic only. No external forecast is adopted here.',
'- Uses only 45-day-or-earlier archived 2018 and 2022 model outputs.',
'- Purpose: determine whether external lite/classic/deluxe direction contains information capable of correcting the current 94/99 baseline errors.','',
f'- 2018 snapshot: {latest18}',
f'- 2022 snapshot: {latest22}','',
'## Accuracy by external model','',
'| cycle | model | N | correct | accuracy |','|---:|---|---:|---:|---:|']
for r in summary:
    acc='NA' if r['accuracy_pct']=='' else f"{r['accuracy_pct']:.1f}%"
    lines.append(f"| {r['cycle']} | {r['model']} | {r['n']} | {r['correct']} | {acc} |")
lines += ['','## Current baseline errors and external direction','',
'| cycle | state | actual | baseline | lite | classic | deluxe |','|---:|---|---:|---:|---:|---:|---:|']
for r in wrong:
    def fmt(k):
        v=r[k];return 'NA' if v=='' else f"{float(v):.2f}"
    lines.append(f"| {r['cycle']} | {r['state']} | {r['actual']:.2f} | {r['baseline']:.2f} | {fmt('lite_margin')} | {fmt('classic_margin')} | {fmt('deluxe_margin')} |")
lines += ['','## Interpretation','',
'If external directions fail on the same races, this source family has no useful directional headroom. If they correctly distinguish some current errors, a leakage-free ensemble gate can be tested separately.','',
'## Outputs','',
'- experiments/external_538_direction/results/external_direction_summary.csv',
'- experiments/external_538_direction/results/external_direction_races.csv',
'- experiments/external_538_direction/results/baseline_wrong_external_signals.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
