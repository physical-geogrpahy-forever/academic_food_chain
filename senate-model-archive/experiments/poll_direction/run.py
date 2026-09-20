#!/usr/bin/env python3
import csv, io, math, urllib.request, urllib.error
from collections import defaultdict
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
PRIOR=ROOT/'performance/results/fullcycle_inc_era_predictions.csv'
OUT=ROOT/'experiments/poll_direction/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0300_poll-direction-fixed-corev2-weight.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

URLS=[
 'https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv',
 'https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'
]
ELECTION={2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
WMAX=0.75
K=0.5

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def parse_date(s):
    s=(s or '').strip()
    if not s:return None
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None
def truth(s):
    return str(s).strip().lower() in {'1','true','yes','y'}

raw=None; source=None
for u in URLS:
    try:
        req=urllib.request.Request(u,headers={'User-Agent':'CoreV2R-poll-direction/1.0'})
        b=urllib.request.urlopen(req,timeout=120).read()
        t=b.decode('utf-8-sig','replace')
        if '<html' in t[:500].lower() or '<!doctype' in t[:500].lower():
            continue
        rr=list(csv.DictReader(io.StringIO(t)))
        if rr:
            raw=rr;source=u;break
    except Exception:
        continue
if raw is None:raise RuntimeError('No Senate poll source could be loaded')

fields=set(raw[0].keys())
print('POLL SOURCE',source)
print('FIELDS',sorted(fields))

# Produce one D-R margin per poll question/race.
polls=[]
if {'candidate_party','pct'}.issubset(fields):
    grouped=defaultdict(list)
    for r in raw:
        try:cyc=int(r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        office=(r.get('office_type') or '').lower()
        if office and 'senate' not in office:continue
        stage=(r.get('stage') or '').lower()
        if stage and 'general' not in stage:continue
        if truth(r.get('hypothetical','false')):continue
        rid=str(r.get('race_id') or '').strip()
        qid=str(r.get('question_id') or r.get('poll_id') or '').strip()
        if not rid or not qid:continue
        grouped[(cyc,rid,qid)].append(r)
    for (cyc,rid,qid),rr in grouped.items():
        dem=[];rep=[]
        for r in rr:
            party=(r.get('candidate_party') or r.get('party') or '').strip().upper()
            try:pct=float(r.get('pct') or '')
            except:continue
            if party.startswith('DEM'):dem.append(pct)
            elif party.startswith('REP'):rep.append(pct)
        if len(dem)!=1 or len(rep)!=1:continue
        r0=rr[0]
        dt=parse_date(r0.get('end_date') or r0.get('polldate'))
        if not dt:continue
        try:n=float(r0.get('sample_size') or r0.get('samplesize') or 600)
        except:n=600.0
        polls.append({'cycle':cyc,'race_id':rid,'poll_id':r0.get('poll_id') or qid,'question_id':qid,
                      'pollster':r0.get('pollster') or r0.get('pollster_rating_name') or '',
                      'end_date':dt,'sample_size':max(n,1.0),'margin':dem[0]-rep[0],
                      'partisan':r0.get('partisan') or '','population':r0.get('population_full') or r0.get('population') or ''})
elif 'margin_poll' in fields:
    for r in raw:
        try:cyc=int(r.get('year') or r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        typ=((r.get('type_simple') or '')+' '+(r.get('type_detail') or '')+' '+(r.get('race') or '')).lower()
        if 'sen' not in typ:continue
        rid=str(r.get('race_id') or '').strip()
        if not rid:continue
        dt=parse_date(r.get('polldate') or r.get('end_date'))
        if not dt:continue
        try:m=float(r.get('margin_poll') or '')
        except:continue
        # Use explicit party columns when available to guarantee D-R sign.
        p1=(r.get('cand1_party') or '').upper();p2=(r.get('cand2_party') or '').upper()
        if p1 and p2 and p1.startswith('REP') and p2.startswith('DEM'):m=-m
        elif p1 and p2 and not (p1.startswith('DEM') and p2.startswith('REP')):continue
        try:n=float(r.get('samplesize') or r.get('sample_size') or 600)
        except:n=600.0
        polls.append({'cycle':cyc,'race_id':rid,'poll_id':r.get('poll_id') or r.get('pollno') or '',
                      'question_id':r.get('question_id') or '', 'pollster':r.get('pollster') or '',
                      'end_date':dt,'sample_size':max(n,1.0),'margin':m,'partisan':r.get('partisan') or '',
                      'population':r.get('population') or ''})
else:
    raise RuntimeError('Unrecognized poll schema: '+','.join(sorted(fields)))

prior=load(PRIOR)
# Ensure exact 99 outer rows only.
prior=[r for r in prior if int(r['test_cycle']) in ELECTION]
byrace=defaultdict(list)
for p in polls:byrace[(int(p['cycle']),str(p['race_id']))].append(p)

def aggregate(ps,target,window,half_life,nonpartisan=False):
    elig=[]
    for p in ps:
        age=(target-p['end_date']).days
        if age<0 or age>window:continue
        if nonpartisan and str(p['partisan']).strip():continue
        rec=1.0 if half_life>=999 else math.exp(-math.log(2)*age/half_life)
        sw=math.sqrt(min(max(float(p['sample_size']),100.0),5000.0)/600.0)
        w=rec*sw
        elig.append((p,w,age))
    if not elig:return None
    s=sum(w for _,w,_ in elig)
    margin=sum(p['margin']*w for p,w,_ in elig)/s
    neff=(s*s)/sum(w*w for _,w,_ in elig)
    return margin,neff,elig

variants=[
 ('w30_h14_all',30,14,False),
 ('w45_h14_all',45,14,False),
 ('w60_h14_all',60,14,False),
 ('w45_equal_all',45,999,False),
 ('w45_h14_nonpartisan',45,14,True),
]
preds=[];snap=[]
for name,window,hl,np_only in variants:
    for r in prior:
        cyc=int(r['test_cycle']);rid=str(r['race_id']);target=ELECTION[cyc]-timedelta(days=45)
        agg=aggregate(byrace.get((cyc,rid),[]),target,window,hl,np_only)
        prior_m=float(r['predicted']);actual=float(r['actual'])
        if agg is None:
            poll_m='';neff=0.0;w=0.0;post=prior_m;n_poll=0
        else:
            poll_m,neff,elist=agg
            w=WMAX*neff/(neff+K)
            post=(1-w)*prior_m+w*poll_m
            n_poll=len(elist)
            for p,pw,age in elist:
                snap.append({'variant':name,'cycle':cyc,'race_id':rid,'state_abbrev':r['state_abbrev'],
                             'snapshot_date':target.isoformat(),'poll_id':p['poll_id'],'question_id':p['question_id'],
                             'pollster':p['pollster'],'field_end':p['end_date'].isoformat(),'days_old':age,
                             'sample_size':p['sample_size'],'population':p['population'],'partisan':p['partisan'],
                             'margin_d_minus_r':p['margin'],'aggregation_weight':pw})
        correct=int((post>0)==(actual>0))
        prior_correct=int((prior_m>0)==(actual>0))
        preds.append({'variant':name,'test_cycle':cyc,'race_id':rid,'state_abbrev':r['state_abbrev'],
                      'actual':actual,'prior':prior_m,'poll_margin':poll_m,'n_eff':neff,'poll_count':n_poll,
                      'poll_weight':w,'posterior':post,'prior_correct':prior_correct,'posterior_correct':correct})

summary=[]
for name,_,_,_ in variants:
    rr=[r for r in preds if r['variant']==name]
    n=len(rr); pc=sum(int(r['prior_correct']) for r in rr); qc=sum(int(r['posterior_correct']) for r in rr)
    covered=sum(int(r['poll_count'])>0 for r in rr)
    summary.append({'variant':name,'n':n,'poll_covered_races':covered,'prior_correct':pc,'prior_accuracy_pct':100*pc/n,
                    'posterior_correct':qc,'posterior_accuracy_pct':100*qc/n,'net_correct_gain':qc-pc})
    for cyc in ELECTION:
        cc=[r for r in rr if int(r['test_cycle'])==cyc]
        pc2=sum(int(r['prior_correct']) for r in cc);qc2=sum(int(r['posterior_correct']) for r in cc)
        summary.append({'variant':name,'n':len(cc),'poll_covered_races':sum(int(r['poll_count'])>0 for r in cc),
                        'prior_correct':pc2,'prior_accuracy_pct':100*pc2/len(cc),'posterior_correct':qc2,
                        'posterior_accuracy_pct':100*qc2/len(cc),'net_correct_gain':qc2-pc2,'cycle':cyc})

for fn,data in [('poll_fixed_summary.csv',summary),('poll_fixed_predictions.csv',preds),('poll_snapshot_45d_reconstructed.csv',snap)]:
    if not data:continue
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(data[0].keys())
        # union fields for mixed summary rows
        for z in data:
            for k in z:
                if k not in fields:fields.append(k)
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

combined=[r for r in summary if 'cycle' not in r]
best=max(combined,key=lambda z:(float(z['posterior_accuracy_pct']),int(z['poll_covered_races'])))
lines=['# Poll layer diagnostic with fixed Core V2 blend weight','',
       '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
       f'- Poll source: {source}',
       f'- Parsed Senate poll questions: {len(polls)}',
       '- Snapshot date: election day minus 45 days.',
       f'- Core V2 blend fixed at w_max={WMAX}, k={K}.',
       '- This stage does not tune blend weights on the 2014/2018/2022 test outcomes.','',
       '## Combined 99-race direction results','',
       '| aggregation | poll-covered | prior correct | prior acc | posterior correct | posterior acc | net correct |',
       '|---|---:|---:|---:|---:|---:|---:|']
for r in combined:
    lines.append(f"| {r['variant']} | {r['poll_covered_races']} | {r['prior_correct']} | {float(r['prior_accuracy_pct']):.1f}% | {r['posterior_correct']} | {float(r['posterior_accuracy_pct']):.1f}% | {r['net_correct_gain']:+d} |")
lines += ['','## Descriptive best fixed aggregation','',
          f"- {best['variant']}: {best['posterior_correct']}/{best['n']} = {float(best['posterior_accuracy_pct']):.1f}%, net {best['net_correct_gain']:+d} correct races versus the same prior.",
          '- This best row is descriptive only. It is not adopted merely because it is best on the outer test set.','',
          '## Benchmarks','',
          '- Preserved Core V2 fundamentals: 90.9% direction.',
          '- Preserved Core V2 + 45-day poll: 91.9% direction.',
          '- The reconstruction should meet or exceed 91.9% before being considered an improvement on the primary task.','',
          '## Outputs','',
          '- experiments/poll_direction/results/poll_fixed_summary.csv',
          '- experiments/poll_direction/results/poll_fixed_predictions.csv',
          '- experiments/poll_direction/results/poll_snapshot_45d_reconstructed.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
