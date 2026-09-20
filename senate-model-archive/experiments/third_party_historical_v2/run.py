#!/usr/bin/env python3
import csv, re, urllib.request, statistics
from pathlib import Path
from datetime import date, timedelta, datetime, timezone
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[2]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
OUT=ROOT/'experiments/third_party_historical_v2/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0500_third-party-historical-v2.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

ELECTION={
2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),
2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)
}
WINDOW=14
UA={'User-Agent':'CoreV2R-third-party-history-v2/1.0'}

STATE={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE',
'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE',
'Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH',
'Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX',
'Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def strip_tags(s):
    s=re.sub(r'<br\s*/?>',' ',s,flags=re.I);s=re.sub(r'<[^>]+>',' ',s)
    s=s.replace('&nbsp;',' ').replace('&amp;','&')
    return re.sub(r'\s+',' ',s).strip()
def tables(html):
    out=[]
    for tb in re.findall(r'<table\b.*?</table>',html,flags=re.S|re.I):
        rr=[]
        for tr in re.findall(r'<tr\b.*?</tr>',tb,flags=re.S|re.I):
            cells=[strip_tags(x) for x in re.findall(r'<t[dh]\b.*?</t[dh]>',tr,flags=re.S|re.I)]
            if cells:rr.append(cells)
        if rr:out.append(rr)
    return out
def pct(s):
    m=re.search(r'-?\d+(?:\.\d+)?',s or '')
    return float(m.group()) if m else None

# Actual all-candidate shares.
sen=load(SEN);by=defaultdict(list)
for r in sen:
    if (r.get('stage') or '').lower()=='general':by[(int(r['cycle']),str(r['race_id']))].append(r)
actual={}
for (cyc,rid),rr0 in by.items():
    if cyc not in ELECTION:continue
    rr=list(rr0);nums=[]
    for x in rr:
        v=(x.get('ranked_choice_round') or '').strip()
        if v:
            try:nums.append(int(float(v)))
            except:pass
    if nums:
        mx=max(nums)
        rr=[x for x in rr if (x.get('ranked_choice_round') or '').strip() and int(float(x['ranked_choice_round']))==mx]
    st=rr[0]['state_abbrev'];cand=defaultdict(lambda:{'votes':0,'parties':set()})
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
    if tot and D+R:
        actual[(cyc,st)]={'d_all':100*D/tot,'r_all':100*R/tot,'t_all':100*T/tot,
                          'dr_margin':100*(D-R)/(D+R)}

# Archived daily poll scraper.
polls=[];coverage=[]
for cyc,eday in ELECTION.items():
    snap=eday-timedelta(days=45)
    pages=0
    for delta in range(WINDOW):
        d=snap-timedelta(days=delta)
        url=f'https://www.electoral-vote.com/evp{cyc}/Senate/Maps/{d.strftime("%b")}{d.day:02d}.html'
        try:
            html=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8','replace')
        except Exception:
            continue
        page_rows=0
        for tb in tables(html):
            if len(tb)<2:continue
            hdr=[x.lower().strip() for x in tb[0]]
            def ix(pred):
                for i,x in enumerate(hdr):
                    if pred(x):return i
                return None
            ist=ix(lambda x:x=='state');idn=ix(lambda x:x.startswith('democrat'));idp=ix(lambda x:x in {'d %','d%'} or x.startswith('d %'))
            irn=ix(lambda x:x.startswith('republican'));irp=ix(lambda x:x in {'r %','r%'} or x.startswith('r %'))
            iin=ix(lambda x:x=='i' or x.startswith('independent'));iip=ix(lambda x:x in {'i %','i%'} or x.startswith('i %'))
            istart=ix(lambda x:x=='start');iend=ix(lambda x:x=='end');ipol=ix(lambda x:x=='pollster')
            if None in (ist,idn,idp,irn,irp):continue
            for z in tb[1:]:
                if len(z)<=max(ist,idn,idp,irn,irp):continue
                stname=z[ist].strip();st=STATE.get(stname)
                D=pct(z[idp]);R=pct(z[irp])
                if not st or D is None or R is None:continue
                tn=z[iin].strip() if iin is not None and iin<len(z) else ''
                T=pct(z[iip]) if iip is not None and iip<len(z) else None
                polls.append({'cycle':cyc,'snapshot_date':snap.isoformat(),'page_date':d.isoformat(),'state_abbrev':st,
                              'democrat':z[idn],'d_pct':D,'republican':z[irn],'r_pct':R,
                              'third_name':tn,'third_pct':'' if T is None else T,
                              'start':z[istart] if istart is not None and istart<len(z) else '',
                              'end':z[iend] if iend is not None and iend<len(z) else '',
                              'pollster':z[ipol] if ipol is not None and ipol<len(z) else '','source_url':url})
                page_rows+=1
        if page_rows:pages+=1
    coverage.append({'cycle':cyc,'snapshot_date':snap.isoformat(),'pages_with_senate_polls':pages})

# Deduplicate same poll repeated on multiple daily pages.
ded={}
for r in polls:
    key=(r['cycle'],r['state_abbrev'],r['pollster'],r['start'],r['end'],r['d_pct'],r['r_pct'],r['third_name'],r['third_pct'])
    if key not in ded or r['page_date']>ded[key]['page_date']:ded[key]=r
polls=list(ded.values())

race=[]
for key in sorted(set((r['cycle'],r['state_abbrev']) for r in polls)):
    rr=[r for r in polls if (r['cycle'],r['state_abbrev'])==key]
    act=actual.get(key)
    if not act:continue
    D=statistics.mean(r['d_pct'] for r in rr);R=statistics.mean(r['r_pct'] for r in rr)
    thirds=[float(r['third_pct']) for r in rr if r['third_pct']!='']
    third=statistics.mean(thirds) if thirds else 0.0
    names=sorted(set(r['third_name'] for r in rr if r['third_name']))
    if third>=15 or act['d_all']<15 or act['r_all']<15:
        context='major_independent_or_party_replacement'
    elif third>=3:
        context='minor_third_3_to_15'
    else:
        context='two_party_or_under3'
    m=D-R;err=act['dr_margin']-m
    race.append({'cycle':key[0],'state_abbrev':key[1],'context':context,'poll_count':len(rr),
                 'multi_candidate_poll_count':len(thirds),'third_names':' | '.join(names),
                 'poll_d_pct':D,'poll_r_pct':R,'poll_third_pct':third,'poll_margin_dr':m,
                 'actual_d_all':act['d_all'],'actual_r_all':act['r_all'],'actual_third_share':act['t_all'],
                 'actual_margin_dr':act['dr_margin'],'margin_error_actual_minus_poll':err,
                 'direction_correct':int((m>0)==(act['dr_margin']>0))})

def summarise(label):
    arr=[r for r in race if r['context']==label]
    if not arr:return {'context':label,'n':0,'direction_accuracy_pct':'','mean_abs_error':'','mean_signed_error':''}
    return {'context':label,'n':len(arr),'direction_accuracy_pct':100*sum(r['direction_correct'] for r in arr)/len(arr),
            'mean_abs_error':statistics.mean(abs(r['margin_error_actual_minus_poll']) for r in arr),
            'mean_signed_error':statistics.mean(r['margin_error_actual_minus_poll'] for r in arr)}
summary=[summarise(x) for x in ['two_party_or_under3','minor_third_3_to_15','major_independent_or_party_replacement']]

for fn,arr in [('race_context.csv',race),('context_summary.csv',summary),('coverage.csv',coverage),('poll_rows.csv',polls)]:
    if not arr:continue
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(arr[0].keys()));w.writeheader();w.writerows(arr)

minor=[r for r in race if r['context']=='minor_third_3_to_15']
lines=['# Historical third-party Senate polling effect v2','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Cycles attempted: 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022.',
'- Window: 14 days ending at election minus 45 days.',
'- Source: archived Electoral-vote.com daily Senate poll tables.',
'- Major independents/party-replacement cases are separated from ordinary minor-third-party cases.','',
'## Coverage','',
'| cycle | snapshot | pages with Senate polls |','|---:|---|---:|']
for r in coverage:lines.append(f"| {r['cycle']} | {r['snapshot_date']} | {r['pages_with_senate_polls']} |")
lines += ['','## Context summary','',
'| context | N | direction accuracy | mean abs D-R error | mean signed error |','|---|---:|---:|---:|---:|']
for r in summary:
    da='NA' if r['direction_accuracy_pct']=='' else f"{r['direction_accuracy_pct']:.1f}%"
    ma='NA' if r['mean_abs_error']=='' else f"{r['mean_abs_error']:.2f}"
    ms='NA' if r['mean_signed_error']=='' else f"{r['mean_signed_error']:.2f}"
    lines.append(f"| {r['context']} | {r['n']} | {da} | {ma} | {ms} |")
lines += ['','## Minor-third-party race-cycles','']
for r in minor:
    lines.append(f"- {r['cycle']} {r['state_abbrev']}: third poll={r['poll_third_pct']:.2f}, actual third={r['actual_third_share']:.2f}, poll D-R={r['poll_margin_dr']:.2f}, actual D-R={r['actual_margin_dr']:.2f}, error={r['margin_error_actual_minus_poll']:.2f}, correct={r['direction_correct']}, third={r['third_names']}")
lines += ['','## Interpretation','',
'- Do not infer a directional third-party correction if the minor-third sample is small or signed error is unstable.',
'- A stable increase in absolute error without stable signed error supports an uncertainty inflation term rather than a point-margin correction.',
'- Major independent cases require a separate multi-candidate model because D/R two-party margin is not the correct target when one major party is effectively replaced.','',
'## Outputs','',
'- experiments/third_party_historical_v2/results/race_context.csv',
'- experiments/third_party_historical_v2/results/context_summary.csv',
'- experiments/third_party_historical_v2/results/coverage.csv',
'- experiments/third_party_historical_v2/results/poll_rows.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
