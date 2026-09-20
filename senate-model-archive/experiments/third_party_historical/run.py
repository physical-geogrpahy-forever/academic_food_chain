#!/usr/bin/env python3
import csv, io, re, math, urllib.request
from pathlib import Path
from datetime import date, timedelta, datetime, timezone
from collections import defaultdict
import statistics

ROOT=Path(__file__).resolve().parents[2]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OUT=ROOT/'experiments/third_party_historical/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0490_third-party-historical-effect.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

ELECTION={2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
WINDOW_DAYS=14
UA={'User-Agent':'CoreV2R-third-party-history/1.0'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def clean_html(s):
    s=re.sub(r'<script.*?</script>',' ',s,flags=re.S|re.I)
    s=re.sub(r'<style.*?</style>',' ',s,flags=re.S|re.I)
    return s
def strip_tags(s):
    s=re.sub(r'<br\s*/?>',' ',s,flags=re.I)
    s=re.sub(r'<[^>]+>',' ',s)
    s=s.replace('&nbsp;',' ').replace('&amp;','&')
    return re.sub(r'\s+',' ',s).strip()
def tables(html):
    out=[]
    for tb in re.findall(r'<table\b.*?</table>',html,flags=re.S|re.I):
        rows=[]
        for tr in re.findall(r'<tr\b.*?</tr>',tb,flags=re.S|re.I):
            cells=[strip_tags(x) for x in re.findall(r'<t[dh]\b.*?</t[dh]>',tr,flags=re.S|re.I)]
            if cells: rows.append(cells)
        if rows: out.append(rows)
    return out
def parse_pct(x):
    m=re.search(r'-?\d+(?:\.\d+)?',x or '')
    return float(m.group()) if m else None

# Final actual result, including all non-D/R share.
sen=load(SEN)
by=defaultdict(list)
for r in sen:
    if (r.get('stage') or '').lower()=='general':
        by[(int(r['cycle']),str(r['race_id']))].append(r)

actual_by_state_cycle={}
for (cyc,rid),rr in by.items():
    if cyc not in ELECTION:continue
    # highest RCV round if relevant
    nums=[]
    for x in rr:
        v=(x.get('ranked_choice_round') or '').strip()
        if v:
            try:nums.append(int(float(v)))
            except:pass
    if nums:
        mx=max(nums);rr=[x for x in rr if (x.get('ranked_choice_round') or '').strip() and int(float(x['ranked_choice_round']))==mx]
    cand=defaultdict(lambda:{'votes':0,'parties':set()})
    st=rr[0]['state_abbrev']
    for r in rr:
        key=(r.get('politician_id') or r.get('candidate_id') or r.get('candidate_name') or '').strip()
        if not key:continue
        try:v=int(float(r.get('votes') or 0))
        except:v=0
        cand[key]['votes']+=v
        for p in ((r.get('ballot_party') or ''),(r.get('party') or '')):
            if p.strip():cand[key]['parties'].add(p.strip().upper())
    D=R=T=0
    for c in cand.values():
        if 'DEM' in c['parties']:D+=c['votes']
        elif 'REP' in c['parties']:R+=c['votes']
        else:T+=c['votes']
    tot=D+R+T
    if D+R>0 and tot>0:
        actual_by_state_cycle[(cyc,st)]={
          'actual_margin_dr':100*(D-R)/(D+R),
          'actual_third_share':100*T/tot,
          'actual_D_share_all':100*D/tot,'actual_R_share_all':100*R/tot
        }

# Scrape daily Electoral-vote Senate pages ending at the 45-day snapshot.
polls=[]
source_days=[]
for cyc,eday in ELECTION.items():
    snap=eday-timedelta(days=45)
    for delta in range(WINDOW_DAYS):
        d=snap-timedelta(days=delta)
        url=f'https://www.electoral-vote.com/evp{cyc}/Senate/Maps/{d.strftime("%b")}{d.day:02d}.html'
        try:
            raw=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8','replace')
        except Exception:
            continue
        found=0
        for tb in tables(clean_html(raw)):
            if len(tb)<2:continue
            hdr=[x.lower() for x in tb[0]]
            if not ('state' in hdr and any(x.startswith('democrat') for x in hdr) and any(x.startswith('republican') for x in hdr)):
                continue
            # Find columns by labels. I and I% exist only on multi-candidate tables.
            def idx(pred):
                for i,x in enumerate(hdr):
                    if pred(x):return i
                return None
            istate=idx(lambda x:x=='state')
            idname=idx(lambda x:x.startswith('democrat'))
            idpct=idx(lambda x:x in {'d %','d%'} or x.startswith('d %'))
            irname=idx(lambda x:x.startswith('republican'))
            irpct=idx(lambda x:x in {'r %','r%'} or x.startswith('r %'))
            iiname=idx(lambda x:x=='i' or x.startswith('independent'))
            iipct=idx(lambda x:x in {'i %','i%'} or x.startswith('i %'))
            istart=idx(lambda x:x=='start'); iend=idx(lambda x:x=='end'); ipoll=idx(lambda x:x=='pollster')
            if None in (istate,idname,idpct,irname,irpct):continue
            for rr in tb[1:]:
                if len(rr)<=max(istate,idname,idpct,irname,irpct):continue
                state=rr[istate].strip()
                dp=parse_pct(rr[idpct]);rp=parse_pct(rr[irpct])
                if not state or dp is None or rp is None:continue
                third_name=rr[iiname].strip() if iiname is not None and iiname<len(rr) else ''
                tp=parse_pct(rr[iipct]) if iipct is not None and iipct<len(rr) else None
                polls.append({
                  'cycle':cyc,'snapshot_date':snap.isoformat(),'page_date':d.isoformat(),'source_url':url,
                  'state_name':state,'democrat':rr[idname],'d_pct':dp,'republican':rr[irname],'r_pct':rp,
                  'third_name':third_name,'third_pct':('' if tp is None else tp),
                  'start':rr[istart] if istart is not None and istart<len(rr) else '',
                  'end':rr[iend] if iend is not None and iend<len(rr) else '',
                  'pollster':rr[ipoll] if ipoll is not None and ipoll<len(rr) else ''
                })
                found+=1
        if found:source_days.append({'cycle':cyc,'page_date':d.isoformat(),'url':url,'poll_rows':found})

# state name to abbreviation
STATE={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE',
'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE',
'Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH',
'Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX',
'Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

# Deduplicate identical poll observations repeated on consecutive daily pages.
dedup={}
for r in polls:
    st=STATE.get(r['state_name'])
    if not st:continue
    key=(r['cycle'],st,r['pollster'],r['start'],r['end'],r['d_pct'],r['r_pct'],r['third_name'],r['third_pct'])
    if key not in dedup or r['page_date']>dedup[key]['page_date']:
        x=dict(r);x['state_abbrev']=st;dedup[key]=x
polls=list(dedup.values())

# Aggregate within race: equal poll average, compare with actual.
race=[]
for key in sorted(set((r['cycle'],r['state_abbrev']) for r in polls)):
    cyc,st=key
    rr=[r for r in polls if (r['cycle'],r['state_abbrev'])==key]
    act=actual_by_state_cycle.get(key)
    if not act:continue
    d=statistics.mean(r['d_pct'] for r in rr); rp=statistics.mean(r['r_pct'] for r in rr)
    third=[float(r['third_pct']) for r in rr if r['third_pct']!='']
    t=statistics.mean(third) if third else 0.0
    margin=d-rp
    err=act['actual_margin_dr']-margin
    race.append({
      'cycle':cyc,'state_abbrev':st,'poll_count':len(rr),'multi_candidate_poll_count':len(third),
      'poll_d_pct':d,'poll_r_pct':rp,'poll_third_pct':t,'poll_margin_dr':margin,
      'actual_margin_dr':act['actual_margin_dr'],'actual_third_share':act['actual_third_share'],
      'margin_error_actual_minus_poll':err,'direction_correct':int((margin>0)==(act['actual_margin_dr']>0)),
      'large_third_poll':int(t>=3.0)
    })

# Simple descriptive comparison, no causal claim.
multi=[r for r in race if r['poll_third_pct']>=3.0]
two=[r for r in race if r['poll_third_pct']<3.0]
def stats(arr):
    if not arr:return {'n':0,'dir_acc':'','mae':''}
    return {'n':len(arr),'dir_acc':100*sum(r['direction_correct'] for r in arr)/len(arr),
            'mae':statistics.mean(abs(r['margin_error_actual_minus_poll']) for r in arr)}
summary=[
 {'group':'third_poll_ge_3pct',**stats(multi)},
 {'group':'third_poll_lt_3pct_or_none',**stats(two)}
]

# NC 2014 specific.
nc=[r for r in race if r['cycle']==2014 and r['state_abbrev']=='NC']

for fn,arr in [('daily_poll_rows.csv',polls),('race_third_party_audit.csv',race),('third_party_group_summary.csv',summary),('source_days.csv',source_days)]:
    if not arr:continue
    fields=list(arr[0].keys())
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

lines=[
'# Historical third-party Senate polling effect audit','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Source: Electoral-vote.com archived daily Senate pages.',
'- Window: 14 calendar days ending at the election-minus-45-day snapshot.',
'- Purpose: test whether explicit third-candidate support is associated with larger D-R polling error or winner-direction misses.',
'- This is an audit, not yet a production correction.','',
'## Source coverage','',
f'- Unique poll observations: {len(polls)}',
f'- Race-cycle aggregates: {len(race)}',
f'- Race-cycles with explicit third-party poll share >=3%: {len(multi)}','',
'## Descriptive comparison','',
'| group | N | direction accuracy | mean absolute D-R error |','|---|---:|---:|---:|'
]
for r in summary:
    da='NA' if r['dir_acc']=='' else f"{r['dir_acc']:.1f}%"
    ma='NA' if r['mae']=='' else f"{r['mae']:.2f}"
    lines.append(f"| {r['group']} | {r['n']} | {da} | {ma} |")
lines += ['','## North Carolina 2014','']
if nc:
    r=nc[0]
    lines += [
      f"- 45-day-window average D={r['poll_d_pct']:.2f}, R={r['poll_r_pct']:.2f}, explicit third={r['poll_third_pct']:.2f}.",
      f"- Poll D-R margin={r['poll_margin_dr']:.2f}.",
      f"- Actual two-party D-R margin={r['actual_margin_dr']:.2f}.",
      f"- Actual non-D/R share={r['actual_third_share']:.2f}.",
      f"- D-R polling error actual-minus-poll={r['margin_error_actual_minus_poll']:.2f}."
    ]
else:
    lines.append('- NC 2014 was not recovered from the archived daily pages in the requested window.')
lines += ['','## Interpretation rule','',
'- If third-party races show materially worse direction accuracy or error, add third-party share to uncertainty/calibration first.',
'- Only add a directional correction if historical OOS evidence shows a stable sign. Do not assign all minor-party votes to one major party.',
'- NC 2014 will only be corrected by a third-party model if the historical relationship supports such a directional adjustment; otherwise it remains a general polling miss.','',
'## Outputs','',
'- experiments/third_party_historical/results/daily_poll_rows.csv',
'- experiments/third_party_historical/results/race_third_party_audit.csv',
'- experiments/third_party_historical/results/third_party_group_summary.csv',
'- experiments/third_party_historical/results/source_days.csv'
]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
