#!/usr/bin/env python3
import csv, io, math, runpy, urllib.request
from collections import defaultdict
from pathlib import Path
from datetime import datetime, date, timedelta, timezone

ROOT=Path(__file__).resolve().parents[2]
INC=ROOT/'performance/run_fullcycle_inc_era_oos.py'
NOI=ROOT/'performance/run_fullcycle_national_econ_oos.py'
OUT=ROOT/'experiments/direction_architecture_selector/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0420_direction-architecture-selector.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

POLL_URL='https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'
ELECTION={2006:date(2006,11,7),2008:date(2008,11,4),2010:date(2010,11,2),2012:date(2012,11,6),
          2014:date(2014,11,4),2016:date(2016,11,8),2018:date(2018,11,6),2020:date(2020,11,3),2022:date(2022,11,8)}
OUTER=[2014,2018,2022]

inc=runpy.run_path(str(INC))
noi=runpy.run_path(str(NOI))

def parse_date(s):
    s=(s or '').strip()
    for fmt in ('%m/%d/%y','%m/%d/%Y','%Y-%m-%d'):
        try:return datetime.strptime(s,fmt).date()
        except:pass
    return None

raw=urllib.request.urlopen(urllib.request.Request(POLL_URL,headers={'User-Agent':'CoreV2R-archselector/1.0'}),timeout=120).read()
pollrows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))
fields=set(pollrows[0].keys())
polls=[]
if 'margin_poll' in fields:
    for r in pollrows:
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
        p1=(r.get('cand1_party') or '').upper(); p2=(r.get('cand2_party') or '').upper()
        if p1 and p2:
            if p1.startswith('REP') and p2.startswith('DEM'):m=-m
            elif not (p1.startswith('DEM') and p2.startswith('REP')):continue
        try:n=float(r.get('samplesize') or 600)
        except:n=600.
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':m})
else:
    grouped=defaultdict(list)
    for r in pollrows:
        try:cyc=int(r.get('cycle') or 0)
        except:continue
        if cyc not in ELECTION:continue
        office=(r.get('office_type') or '').lower()
        if office and 'senate' not in office:continue
        stage=(r.get('stage') or '').lower()
        if stage and 'general' not in stage:continue
        rid=str(r.get('race_id') or '').strip(); qid=str(r.get('question_id') or r.get('poll_id') or '').strip()
        if rid and qid:grouped[(cyc,rid,qid)].append(r)
    for (cyc,rid,qid),rr in grouped.items():
        dem=[];rep=[]
        for r in rr:
            party=(r.get('candidate_party') or r.get('party') or '').upper()
            try:pct=float(r.get('pct') or '')
            except:continue
            if party.startswith('DEM'):dem.append(pct)
            elif party.startswith('REP'):rep.append(pct)
        if len(dem)!=1 or len(rep)!=1:continue
        dt=parse_date(rr[0].get('end_date') or rr[0].get('polldate'))
        if not dt:continue
        try:n=float(rr[0].get('sample_size') or 600)
        except:n=600.
        polls.append({'cycle':cyc,'race_id':rid,'end_date':dt,'sample_size':max(n,1.),'margin':dem[0]-rep[0]})

byrace=defaultdict(list)
for p in polls:byrace[(p['cycle'],p['race_id'])].append(p)

def poll_aggregate(cyc,rid):
    target=ELECTION[cyc]-timedelta(days=45); e=[]
    for p in byrace.get((cyc,str(rid)),[]):
        age=(target-p['end_date']).days
        if age<0 or age>30:continue
        wt=math.exp(-math.log(2)*age/14)*math.sqrt(min(max(p['sample_size'],100.),5000.)/600.)
        e.append((p['margin'],wt))
    if not e:return None
    s=sum(w for _,w in e); m=sum(x*w for x,w in e)/s; neff=s*s/sum(w*w for _,w in e)
    return m,neff

def blend(prior,cyc,rid):
    agg=poll_aggregate(cyc,rid)
    if agg is None:return prior
    pm,neff=agg; w=.75*neff/(neff+.5)
    return (1-w)*prior+w*pm

def make_family(name,ns):
    rows=ns['rows']; fitpred=ns['fitpred']; tune=ns['tune']
    out=[]
    for cyc in sorted(ELECTION):
        tr=[r for r in rows if int(r['cycle'])<cyc]
        te=[r for r in rows if int(r['cycle'])==cyc]
        if len(tr)<20 or not te:continue
        try:
            best,_=tune(tr)
        except Exception:
            continue
        if name=='incumbency_era':
            sc,_,arch,ll,le,ln,li,lr=best
            pp=fitpred(tr,te,arch,ll,le,ln,li,lr)
            spec=f'{arch}|L{ll}|E{le}|N{ln}|I{li}|R{lr}'
        else:
            sc,ll,le,ln=best
            pp=fitpred(tr,te,ll,le,ln)
            spec=f'L{ll}|E{le}|N{ln}'
        for r,p in zip(te,pp):
            prior=float(p); post=blend(prior,cyc,r['race_id']); actual=float(r['y'])
            out.append({'family':name,'cycle':cyc,'race_id':str(r['race_id']),'state_abbrev':r['state_abbrev'],
                        'actual':actual,'prior':prior,'posterior':post,'correct':int((post>0)==(actual>0)),'spec':spec})
    return out

allpred=make_family('incumbency_era',inc)+make_family('no_incumbency',noi)

families=['incumbency_era','no_incumbency']
score_rows=[]
for cyc in sorted(set(r['cycle'] for r in allpred)):
    for fam in families:
        rr=[r for r in allpred if r['cycle']==cyc and r['family']==fam]
        if rr:score_rows.append({'cycle':cyc,'family':fam,'n':len(rr),'correct':sum(r['correct'] for r in rr),
                                 'accuracy_pct':100*sum(r['correct'] for r in rr)/len(rr)})

choices=[]; final=[]
for tc in OUTER:
    hist_cycles=[c for c in sorted(set(r['cycle'] for r in allpred)) if 2010<=c<tc]
    stats=[]
    for fam in families:
        rr=[r for r in allpred if r['family']==fam and r['cycle'] in hist_cycles]
        correct=sum(r['correct'] for r in rr); n=len(rr)
        recent_cycles=hist_cycles[-2:]
        recent=[r for r in rr if r['cycle'] in recent_cycles]
        rc=sum(r['correct'] for r in recent); rn=len(recent)
        stats.append((correct,n,rc,rn,fam))
    # Higher cumulative correct first, then recent correct; ties preserve incumbency-era.
    stats.sort(key=lambda z:(-z[0],-z[2],0 if z[4]=='incumbency_era' else 1))
    chosen=stats[0][4]
    choices.append({'test_cycle':tc,'history_cycles':';'.join(map(str,hist_cycles)),'chosen_family':chosen,
                    'inc_correct':next(x[0] for x in stats if x[4]=='incumbency_era'),
                    'inc_n':next(x[1] for x in stats if x[4]=='incumbency_era'),
                    'noinc_correct':next(x[0] for x in stats if x[4]=='no_incumbency'),
                    'noinc_n':next(x[1] for x in stats if x[4]=='no_incumbency')})
    final += [r for r in allpred if r['family']==chosen and r['cycle']==tc]

summary=[]
for scope in ['combined']+list(map(str,OUTER)):
    rr=final if scope=='combined' else [r for r in final if r['cycle']==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'accuracy_pct':100*ok/n})

for fn,data in [('selector_summary.csv',summary),('selector_choices.csv',choices),('family_cycle_scores.csv',score_rows),('selector_predictions.csv',final)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)

comb=summary[0]; wrong=[r for r in final if not r['correct']]
lines=['# Direction-first fundamentals architecture selector','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Candidate families: incumbency-era fundamentals and no-incumbency fundamentals.',
'- Both families are fitted only on cycles before the cycle being predicted and then receive the same fixed 45-day poll update.',
'- For each outer test cycle, family selection uses only winner-direction results from earlier cycles starting in 2010.',
'- Primary selector criterion: cumulative historical correct races. Tie-break: recent two-cycle correct count, then incumbency-era as the preserved default.','',
'## Outer result','',
'| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['accuracy_pct']:.1f}% |")
lines += ['','## Architecture chosen before each outer cycle','',
'| test | history cycles | chosen | incumbency correct/N | no-inc correct/N |','|---:|---|---|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['history_cycles']} | {r['chosen_family']} | {r['inc_correct']}/{r['inc_n']} | {r['noinc_correct']}/{r['noinc_n']} |")
lines += ['','## Historical family scores','',
'| cycle | family | N | correct | accuracy |','|---:|---|---:|---:|---:|']
for r in score_rows:lines.append(f"| {r['cycle']} | {r['family']} | {r['n']} | {r['correct']} | {r['accuracy_pct']:.1f}% |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['cycle']} {r['state_abbrev']} {r['race_id']}: family={r['family']}, posterior={r['posterior']:.2f}, actual={r['actual']:.2f}")
lines += ['','## Benchmark','',
'- Fixed incumbency-era + poll benchmark: 94/99 = 94.9%.',
'- The selector is an improvement only if it exceeds 94/99 without using the target outer-cycle result in family selection.','',
'## Outputs','',
'- experiments/direction_architecture_selector/results/selector_summary.csv',
'- experiments/direction_architecture_selector/results/selector_choices.csv',
'- experiments/direction_architecture_selector/results/family_cycle_scores.csv',
'- experiments/direction_architecture_selector/results/selector_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
