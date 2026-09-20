#!/usr/bin/env python3
import csv, io, re, urllib.request, itertools
from pathlib import Path
from datetime import datetime, timezone
from difflib import SequenceMatcher
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
OUT=ROOT/'experiments/fec18m_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0385_fec-top50-june30-fundraising-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

YEARS=[2014,2018,2022]
TABLES={'receipts':'6a','individual':'6b','cash':'6f'}
GAMMA=[0,0.5,1,2,3,4,5,6,8,10,12,15,20,25,30]
POST_THRESH=[2,3,4,5,6,8,10,15,20,999]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):
    s=(s or '').strip().lower()
    if ',' in s:
        left,right=s.split(',',1);s=right+' '+left
    s=re.sub(r'\b(jr|sr|ii|iii|iv|mr|mrs|ms|dr|sen)\b',' ',s)
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 CoreV2R-FEC-Top50/1.0'})
    return urllib.request.urlopen(req,timeout=120).read()
def num(v):
    if isinstance(v,(int,float)):return float(v)
    s=str(v or '').replace('$','').replace(',','').replace('(','-').replace(')','').strip()
    try:return float(s)
    except:return None

def parse_top50(year,metric,table):
    urls=[
      f'https://www.fec.gov/resources/campaign-finance-statistics/{year}/tables/congressional/ConCand{table}_{year}_18m.xlsx',
      f'https://www.fec.gov/resources/campaign-finance-statistics/{year}/tables/congressional/ConCand{table}_{year}_18M.xlsx'
    ]
    raw=None;used=None
    for u in urls:
        try:
            b=get(u)
            if b[:2]==b'PK':raw=b;used=u;break
        except Exception:pass
    if raw is None:raise RuntimeError(f'No FEC Top50 workbook: {year} {table}')
    wb=load_workbook(io.BytesIO(raw),data_only=True,read_only=True)
    found=[]
    for ws in wb.worksheets:
        vals=list(ws.iter_rows(values_only=True))
        hi=None
        for i,row in enumerate(vals[:30]):
            text=[str(x or '').strip() for x in row]
            low=[x.lower() for x in text]
            if any('candidate name' in x for x in low) and any(x=='state' or 'state'==x.strip() for x in low):
                hi=i;break
        if hi is None:continue
        headers=[str(x or '').strip() for x in vals[hi]]
        def idx(patterns):
            for p in patterns:
                for j,h in enumerate(headers):
                    if p in h.lower():return j
            return None
        ni=idx(['candidate name','candidate'])
        si=idx(['state'])
        pi=idx(['party'])
        # amount is the rightmost non-empty financial header
        ai=None
        for j in range(len(headers)-1,-1,-1):
            h=headers[j].lower()
            if any(k in h for k in ['receipt','individual','cash on hand','contribution']):
                ai=j;break
        if None in (ni,si,ai):continue
        for row in vals[hi+1:]:
            name=str(row[ni] or '').strip() if ni<len(row) else ''
            state=str(row[si] or '').strip().upper() if si<len(row) else ''
            if not name or len(state)!=2:continue
            amount=num(row[ai] if ai<len(row) else None)
            if amount is None:continue
            party=str(row[pi] or '').strip() if pi is not None and pi<len(row) else ''
            found.append({'year':year,'metric':metric,'name':name,'state':state,'party':party,'amount':amount,'source_url':used})
    if len(found)<35:
        raise RuntimeError(f'Only {len(found)} candidate rows parsed for {year} {metric}')
    return found,used

top=[];source=[]
for year in YEARS:
    for metric,table in TABLES.items():
        rows,u=parse_top50(year,metric,table)
        top+=rows
        source.append({'year':year,'metric':metric,'url':u,'rows':len(rows)})

index={}
for r in top:index.setdefault((r['year'],r['metric'],r['state']),[]).append(r)

def party_bonus(p,side):
    p=(p or '').upper()
    if side=='D':return 0.06 if ('DEM' in p or 'DFL' in p) else 0
    return 0.06 if 'REP' in p else 0

def match(year,metric,state,name,side):
    q=norm(name);qt=q.split();pool=index.get((year,metric,state),[])
    scored=[]
    for x in pool:
        n=norm(x['name']);nt=n.split()
        seq=1 if q==n else SequenceMatcher(None,q,n).ratio()
        surname=1 if qt and nt and qt[-1]==nt[-1] else 0
        first=1 if qt and nt and (qt[0]==nt[0] or qt[0][0]==nt[0][0]) else 0
        jac=len(set(qt)&set(nt))/max(len(set(qt)|set(nt)),1)
        score=.5*seq+.25*surname+.15*first+.1*jac+party_bonus(x['party'],side)
        scored.append((score,x))
    scored.sort(key=lambda z:z[0],reverse=True)
    if not scored or scored[0][0]<.70:return None,(scored[0][0] if scored else 0)
    if len(scored)>1 and scored[0][0]-scored[1][0]<.035:return None,scored[0][0]
    return scored[0][1],scored[0][0]

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dm=load(DM);dby={r['race_id']:r for r in dm}
race_fin={};review=[]
for b in base:
    year=int(b['test_cycle']);rid=b['race_id'];st=b['state_abbrev'];d=dby[rid]
    rec={'cycle':year,'race_id':rid,'state':st,'actual':float(b['actual']),'posterior':float(b['posterior'])}
    for metric in TABLES:
        dmch,ds=match(year,metric,st,d['d_side_candidate'],'D')
        rmch,rs=match(year,metric,st,d['r_side_candidate'],'R')
        review.append({'cycle':year,'race_id':rid,'state':st,'metric':metric,
                       'd_candidate':d['d_side_candidate'],'d_match':'' if not dmch else dmch['name'],'d_score':ds,
                       'r_candidate':d['r_side_candidate'],'r_match':'' if not rmch else rmch['name'],'r_score':rs})
        if dmch and rmch and dmch['amount']+rmch['amount']>0:
            rec[metric+'_share']=(dmch['amount']-rmch['amount'])/(dmch['amount']+rmch['amount'])
            rec['d_'+metric]=dmch['amount'];rec['r_'+metric]=rmch['amount']
        else:
            rec[metric+'_share']='';rec['d_'+metric]='';rec['r_'+metric]=''
    race_fin[(year,rid)]=rec

SIGNALS=[m+'_share' for m in TABLES]

def predict(r,signal,gamma,thr):
    v=r.get(signal,'')
    if v=='' or abs(float(r['posterior']))>thr:return float(r['posterior']),0
    q=float(r['posterior'])+gamma*float(v)
    return q,int((q>0)!=(float(r['posterior'])>0))

def evalset(dat,signal,gamma,thr):
    ok=flips=covered=0
    for r in dat:
        if r.get(signal,'')!='':covered+=1
        q,f=predict(r,signal,gamma,thr)
        ok+=int((q>0)==(float(r['actual'])>0));flips+=f
    return ok,flips,covered

choices=[];pred=[]
allrows=[race_fin[(int(b['test_cycle']),b['race_id'])] for b in base]
for tc in YEARS:
    train=[r for r in allrows if r['cycle']<tc]
    test=[r for r in allrows if r['cycle']==tc]
    if not train:
        signal='receipts_share';gamma=0;thr=999;ok=0;flips=0;cov=0
    else:
        cand=[]
        for signal,gamma,thr in itertools.product(SIGNALS,GAMMA,POST_THRESH):
            ok,flips,cov=evalset(train,signal,gamma,thr)
            # winner count first; then fewer flips; then more finance coverage; then smaller gamma
            cand.append((-ok,flips,-cov,gamma,0 if thr==999 else 1,signal,thr))
        cand.sort()
        z=cand[0];ok=-z[0];flips=z[1];cov=-z[2];gamma=z[3];signal=z[5];thr=z[6]
    choices.append({'test_cycle':tc,'signal':signal,'gamma':gamma,'posterior_threshold':thr,'train_n':len(train),
                    'train_correct':ok if train else '','train_accuracy_pct':100*ok/len(train) if train else '',
                    'train_flips':flips,'train_signal_covered':cov,
                    'test_signal_covered':sum(r.get(signal,'')!='' for r in test)})
    for r in test:
        q,f=predict(r,signal,gamma,thr)
        pred.append({**r,'selected_signal':signal,'gamma':gamma,'posterior_threshold':thr,
                     'adjusted_posterior':q,'direction_flip':f,
                     'baseline_correct':int((float(r['posterior'])>0)==(float(r['actual'])>0)),
                     'adjusted_correct':int((q>0)==(float(r['actual'])>0))})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'any_finance_covered':sum(any(r.get(s,'')!='' for s in SIGNALS) for r in rr),
                    'baseline_correct':b,'baseline_accuracy_pct':100*b/n,'adjusted_correct':a,
                    'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,'direction_flips':sum(r['direction_flip'] for r in rr)})

for fn,data in [('fec_top50_summary.csv',summary),('fec_top50_choices.csv',choices),('fec_top50_predictions.csv',pred),
                ('fec_top50_match_review.csv',review),('fec_top50_source_meta.csv',source)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# FEC Top-50 June-30 fundraising direction experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Uses official FEC 18-month Top 50 Senate tables for receipts (6a), contributions from individuals (6b), and cash on hand (6f).',
'- All tables cover January 1 of the pre-election year through June 30 of the election year.',
'- A finance share is computed only when both major-party general-election candidates appear in the same Top-50 metric table.',
'- Missing Top-50 membership is never treated as zero; uncovered races retain the 94/99 baseline.',
'- Signal, coefficient and optional posterior threshold are selected from earlier cycles only.','',
'## Result','',
'| scope | N | any finance covered | baseline correct | baseline acc | finance correct | finance acc | net | flips |',
'|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['any_finance_covered']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected finance rule','',
'| test | signal | gamma | posterior threshold | train accuracy | train signal coverage | test signal coverage |',
'|---:|---|---:|---:|---:|---:|---:|']
for r in choices:
    ta='NA' if r['train_accuracy_pct']=='' else f"{r['train_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['signal']} | {r['gamma']} | {r['posterior_threshold']} | {ta} | {r['train_signal_covered']} | {r['test_signal_covered']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> finance {'correct' if r['adjusted_correct'] else 'wrong'}")
lines += ['','## Decision','',
'Adopt only if combined winner-direction accuracy exceeds 94/99 without outer-cycle tuning.','',
'## Outputs','',
'- experiments/fec18m_direction/results/fec_top50_summary.csv',
'- experiments/fec18m_direction/results/fec_top50_choices.csv',
'- experiments/fec18m_direction/results/fec_top50_predictions.csv',
'- experiments/fec18m_direction/results/fec_top50_match_review.csv',
'- experiments/fec18m_direction/results/fec_top50_source_meta.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
