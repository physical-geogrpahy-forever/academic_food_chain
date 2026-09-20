#!/usr/bin/env python3
import csv, io, json, re, urllib.request, urllib.parse, zipfile, itertools
from pathlib import Path
from datetime import datetime, timezone
from difflib import SequenceMatcher

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
OUT=ROOT/'experiments/fec18m_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0382_fec-form3-june30-fundraising-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

YEARS=[2014,2018,2022]
GAMMA=[0,0.5,1,2,3,4,5,6,8,10,12,15,20]
SIGNALS=['individual_share','receipts_share','cash_share']
API='https://api.open.fec.gov/v1/reports/house-senate/'

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):
    s=(s or '').strip().lower()
    if ',' in s:
        left,right=s.split(',',1)
        s=right+' '+left
    s=re.sub(r'\b(jr|sr|ii|iii|iv)\b',' ',s)
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'CoreV2R-FEC-Form3/1.0'})
    return urllib.request.urlopen(req,timeout=120).read()
def fnum(v):
    try:return float(v or 0)
    except:return 0.0

# FEC candidate master: pipe-delimited bulk files.
CAND_COLS=['cand_id','cand_name','party','election_year','state','office','district','ici','status','pcc',
           'st1','st2','city','mail_state','zip']
masters=[]
source_meta=[]
for year in YEARS:
    yy=str(year)[-2:]
    urls=[
      f'https://www.fec.gov/files/bulk-downloads/{year}/cn{yy}.zip',
      f'https://www.fec.gov/files/bulk-downloads/{year}/cn{year}.zip'
    ]
    raw=None;used=None
    for u in urls:
        try:
            b=get(u)
            if b[:2]==b'PK':raw=b;used=u;break
        except Exception:pass
    if raw is None:raise RuntimeError(f'FEC candidate master not found for {year}')
    z=zipfile.ZipFile(io.BytesIO(raw))
    member=next((n for n in z.namelist() if n.lower().endswith('.txt')),z.namelist()[0])
    txt=z.read(member).decode('latin-1','replace')
    count=0
    for line in txt.splitlines():
        parts=line.split('|')
        if len(parts)<10:continue
        d={CAND_COLS[i]:(parts[i].strip() if i<len(parts) else '') for i in range(len(CAND_COLS))}
        try:ey=int(d['election_year'] or 0)
        except:ey=0
        if d['office']!='S' or ey!=year:continue
        d['year']=year;masters.append(d);count+=1
    source_meta.append({'year':year,'source':'candidate_master','url':used,'rows_senate':count})

byys={}
for x in masters:byys.setdefault((x['year'],x['state']),[]).append(x)

def party_ok(code,side):
    p=(code or '').upper()
    return ('DEM' in p or p in {'D','DFL'}) if side=='D' else ('REP' in p or p=='R')

def match_candidate(year,state,name,side):
    q=norm(name);pool=byys.get((year,state),[])
    scored=[]
    for x in pool:
        n=norm(x['cand_name'])
        seq=1.0 if q==n else SequenceMatcher(None,q,n).ratio()
        qt=q.split();nt=n.split()
        qlast=qt[-1] if qt else '';nlast=nt[-1] if nt else ''
        qfirst=qt[0] if qt else '';nfirst=nt[0] if nt else ''
        surname=1.0 if qlast and qlast==nlast else 0.0
        first=1.0 if qfirst and nfirst and (qfirst==nfirst or qfirst[0]==nfirst[0]) else 0.0
        qset=set(qt);nset=set(nt)
        jacc=len(qset & nset)/max(len(qset | nset),1)
        sim=0.50*seq+0.25*surname+0.15*first+0.10*jacc
        if party_ok(x['party'],side):sim+=0.08
        elif x['party']:sim-=0.12
        scored.append((sim,x))
    scored.sort(key=lambda z:z[0],reverse=True)
    if not scored or scored[0][0]<0.72:return None,(scored[0][0] if scored else 0)
    if len(scored)>1 and scored[0][0]-scored[1][0]<0.04:return None,scored[0][0]
    return scored[0][1],scored[0][0]

base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dm=load(DM);dby={r['race_id']:r for r in dm}
matches=[];committee_ids={y:set() for y in YEARS}
for r in base:
    year=int(r['test_cycle']);d=dby[r['race_id']];state=r['state_abbrev']
    for side in ['D','R']:
        name=d['d_side_candidate'] if side=='D' else d['r_side_candidate']
        m,score=match_candidate(year,state,name,side)
        rec={'cycle':year,'race_id':r['race_id'],'state':state,'side':side,'candidate':name,'score':score,
             'fec_candidate_id':'','fec_candidate_name':'','party':'','pcc':''}
        if m:
            rec.update({'fec_candidate_id':m['cand_id'],'fec_candidate_name':m['cand_name'],'party':m['party'],'pcc':m['pcc']})
            if m['pcc']:committee_ids[year].add(m['pcc'])
        matches.append(rec)

# Fetch Form 3 committee summaries in batches. API accepts repeated committee_id.
reports={}
api_keys_seen=set()
for year in YEARS:
    ids=sorted(committee_ids[year])
    for i in range(0,len(ids),20):
        batch=ids[i:i+20]
        params=[('api_key','DEMO_KEY'),('cycle',str(year)),('year',str(year)),('per_page','100'),
                ('most_recent','true'),('report_type','Q2'),('sort','-coverage_end_date')]
        params += [('committee_id',x) for x in batch]
        url=API+'?'+urllib.parse.urlencode(params)
        payload=json.loads(get(url).decode('utf-8'))
        results=payload.get('results',[])
        if results:api_keys_seen.update(results[0].keys())
        for x in results:
            cid=str(x.get('committee_id') or '')
            cov_raw=str(x.get('coverage_end_date') or '')
            cov=cov_raw[:10]
            valid_cov=(cov==f'{year}-06-30' or cov_raw.startswith(f'06/30/{year}'))
            if cid not in batch or not valid_cov:continue
            oldr=reports.get((year,cid))
            # Prefer the highest file number / newest receipt among duplicate amendments.
            rank=(int(x.get('file_number') or 0),str(x.get('receipt_date') or ''))
            oldrank=(-1,'') if oldr is None else (int(oldr.get('file_number') or 0),str(oldr.get('receipt_date') or ''))
            if rank>oldrank:reports[(year,cid)]=x
        source_meta.append({'year':year,'source':'openfec_form3_batch','url':url.replace('DEMO_KEY','REDACTED_DEMO_KEY'),
                            'rows_senate':len(results)})

def firstnum(r,names):
    for k in names:
        if k in r and r.get(k) is not None:return fnum(r.get(k))
    return 0.0

def finance(r):
    # Form 3 field aliases vary somewhat across OpenFEC versions.
    individual=firstnum(r,['individual_contributions_ytd','contributions_from_individuals_ytd',
                           'individual_itemized_contributions_ytd'])
    if individual==0:
        individual=firstnum(r,['individual_itemized_contributions_ytd'])+firstnum(r,['individual_unitemized_contributions_ytd'])
    receipts=firstnum(r,['total_receipts_ytd','receipts_ytd'])
    cash=firstnum(r,['cash_on_hand_end_period','cash_on_hand_end_period_amount'])
    return {'individual':individual,'receipts':receipts,'cash':cash}

match_by={(m['cycle'],m['race_id'],m['side']):m for m in matches}
rows=[]
for b in base:
    year=int(b['test_cycle']);rid=b['race_id'];state=b['state_abbrev']
    dmch=match_by[(year,rid,'D')];rmch=match_by[(year,rid,'R')]
    dr=reports.get((year,dmch['pcc'])) if dmch['pcc'] else None
    rr=reports.get((year,rmch['pcc'])) if rmch['pcc'] else None
    if not dr or not rr:continue
    df=finance(dr);rf=finance(rr)
    def share(k):
        a=max(df[k],0);c=max(rf[k],0)
        return 0.0 if a+c<=0 else (a-c)/(a+c)
    rows.append({'cycle':year,'race_id':rid,'state':state,'actual':float(b['actual']),'posterior':float(b['posterior']),
                 'individual_share':share('individual'),'receipts_share':share('receipts'),'cash_share':share('cash'),
                 'd_pcc':dmch['pcc'],'r_pcc':rmch['pcc'],
                 'd_individual':df['individual'],'r_individual':rf['individual'],
                 'd_receipts':df['receipts'],'r_receipts':rf['receipts'],
                 'd_cash':df['cash'],'r_cash':rf['cash']})

def evalset(dat,signal,gamma):
    ok=flips=0
    for r in dat:
        q=r['posterior']+gamma*r[signal]
        ok+=int((q>0)==(r['actual']>0));flips+=int((q>0)!=(r['posterior']>0))
    return ok,flips

choices=[];pred=[]
for tc in YEARS:
    train=[r for r in rows if r['cycle']<tc];test=[r for r in rows if r['cycle']==tc]
    if not train:
        signal='individual_share';gamma=0;ok=0;flips=0
    else:
        cand=[]
        for signal,gamma in itertools.product(SIGNALS,GAMMA):
            ok,flips=evalset(train,signal,gamma)
            cand.append((-ok,flips,gamma,signal))
        cand.sort(key=lambda z:(z[0],z[1],z[2],z[3]))
        z=cand[0];ok=-z[0];flips=z[1];gamma=z[2];signal=z[3]
    choices.append({'test_cycle':tc,'signal':signal,'gamma':gamma,'train_n':len(train),
                    'train_correct':ok if train else '','train_accuracy_pct':100*ok/len(train) if train else '',
                    'train_flips':flips,'test_finance_covered':len(test)})
    for r in test:
        q=r['posterior']+gamma*r[signal]
        pred.append({**r,'selected_signal':signal,'gamma':gamma,'adjusted_posterior':q,
                     'baseline_correct':int((r['posterior']>0)==(r['actual']>0)),
                     'adjusted_correct':int((q>0)==(r['actual']>0))})

pmap={(r['cycle'],r['race_id']):r for r in pred}
allpred=[]
for b in base:
    key=(int(b['test_cycle']),b['race_id'])
    if key in pmap:allpred.append(pmap[key]);continue
    act=float(b['actual']);post=float(b['posterior'])
    allpred.append({'cycle':key[0],'race_id':key[1],'state':b['state_abbrev'],'actual':act,'posterior':post,
                    'individual_share':'','receipts_share':'','cash_share':'','d_pcc':'','r_pcc':'',
                    'd_individual':'','r_individual':'','d_receipts':'','r_receipts':'','d_cash':'','r_cash':'',
                    'selected_signal':'UNMATCHED_OR_NO_Q2_BASELINE','gamma':0,'adjusted_posterior':post,
                    'baseline_correct':int((post>0)==(act>0)),'adjusted_correct':int((post>0)==(act>0))})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=allpred if scope=='combined' else [r for r in allpred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'finance_covered':sum(r['selected_signal']!='UNMATCHED_OR_NO_Q2_BASELINE' for r in rr),
                    'baseline_correct':b,'baseline_accuracy_pct':100*b/n,'adjusted_correct':a,
                    'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b})

for fn,data in [('fec_form3_summary.csv',summary),('fec_form3_choices.csv',choices),('fec_form3_predictions.csv',allpred),
                ('fec_form3_candidate_matches.csv',matches),('fec_form3_source_meta.csv',source_meta)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys()) if data else ['empty'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

changed=[r for r in allpred if r['baseline_correct']!=r['adjusted_correct']]
lines=['# Candidate-level FEC Form 3 June-30 fundraising direction experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- The discarded FEC Table 2 aggregate workbook is not used.',
'- Senate candidates are matched to the FEC candidate master and principal campaign committee (PCC).',
'- Finance values come from the latest Form 3 report whose coverage_end_date is June 30 of the election year.',
'- Candidate matching/report gaps preserve the 94/99 baseline unchanged.',
'- Signal/gamma for each outer cycle is selected only from prior outer cycles with finance coverage.','',
'## Coverage and result','',
'| scope | N | finance-covered | baseline correct | baseline acc | finance correct | finance acc | net |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['finance_covered']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} |")
lines += ['','## Selected signal','',
'| test | signal | gamma | train N | train accuracy | test finance coverage |',
'|---:|---|---:|---:|---:|---:|']
for r in choices:
    ta='NA' if r['train_accuracy_pct']=='' else f"{r['train_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['signal']} | {r['gamma']} | {r['train_n']} | {ta} | {r['test_finance_covered']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state']} {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> finance {'correct' if r['adjusted_correct'] else 'wrong'}")
lines += ['','## API field audit','',f"- OpenFEC report keys observed: {', '.join(sorted(api_keys_seen))}",'',
'## Decision','',
'Adopt only if candidate-level June-30 fundraising exceeds 94/99 without outer-test tuning and finance coverage is adequate.','',
'## Outputs','',
'- experiments/fec18m_direction/results/fec_form3_summary.csv',
'- experiments/fec18m_direction/results/fec_form3_choices.csv',
'- experiments/fec18m_direction/results/fec_form3_predictions.csv',
'- experiments/fec18m_direction/results/fec_form3_candidate_matches.csv',
'- experiments/fec18m_direction/results/fec_form3_source_meta.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
