#!/usr/bin/env python3
import csv, io, re, runpy, itertools, math
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone, timedelta
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FULL=ROOT/'performance/run_fullcycle_inc_era_oos.py'
POLL=ROOT/'experiments/poll_stack/run.py'
LEAN=ROOT/'data/processed/presidential_state_lean.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
OUT=ROOT/'experiments/deduplicated_fundamentals/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0410_deduplicated-fundamentals-direction.md'
OUT.mkdir(parents=True,exist_ok=True);DOC.parent.mkdir(parents=True,exist_ok=True)

HOUSE_URL='https://raw.githubusercontent.com/fivethirtyeight/election-results/d7a7cff101da28f4ff77114450a964874800ca54/election_results_house.csv'
OUTER=[2014,2018,2022]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def truth(v):return str(v).strip().lower()=='true'
def norm(s):
    s=(s or '').lower();s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()

# Reuse the audited Senate structural panel and candidate IDs.
fns=runpy.run_path(str(FULL))
rows=fns['rows'];races=fns['races'];seat_hist=fns['seat_hist']
rowby={(int(r['cycle']),str(r['race_id'])):r for r in rows}
raceby={(int(r['cycle']),str(r['race_id'])):r for r in races}

# Reuse poll parser/aggregator only; the old prior from that script is not used as a model input.
pns=runpy.run_path(str(POLL))
poll_byrace=pns['byrace'];aggregate=pns['aggregate'];ELECTION=pns['ELECTION']

# State PVI function from presidential state lean.
leanrows=load(LEAN)
lean={};years=set()
for r in leanrows:
    try:
        y=int(r['cycle']);st=r['state_abbrev'];v=float(r['lean_vs_national_pctpt'])
    except:continue
    lean[(y,st)]=v;years.add(y)
years=sorted(years)
def pvi_state(cyc,st):
    ys=[y for y in years if y<cyc and (y,st) in lean]
    if len(ys)<2:return None
    return .67*lean[(ys[-1],st)]+.33*lean[(ys[-2],st)]

# Senate cycle-adjusted residuals.
sen_cycle_raw=defaultdict(list)
for r in races:
    pv=pvi_state(int(r['cycle']),r['state_abbrev'])
    if pv is not None:
        sen_cycle_raw[int(r['cycle'])].append(float(r['y'])-pv)
sen_cycle_mean={c:sum(v)/len(v) for c,v in sen_cycle_raw.items() if v}

sen_perf=[]
for r in races:
    cyc=int(r['cycle']);pv=pvi_state(cyc,r['state_abbrev'])
    if pv is None or cyc not in sen_cycle_mean:continue
    resid=float(r['y'])-pv-sen_cycle_mean[cyc]
    if r.get('d_pid'):sen_perf.append({'pid':r['d_pid'],'cycle':cyc,'race_id':str(r['race_id']),'score':resid})
    if r.get('r_pid'):sen_perf.append({'pid':r['r_pid'],'cycle':cyc,'race_id':str(r['race_id']),'score':-resid})
sen_by_pid=defaultdict(list)
for x in sen_perf:sen_by_pid[x['pid']].append(x)

# Governor cycle-adjusted candidate residuals.
govraw=load(GOV)
gov_by_race=defaultdict(list)
for r in govraw:
    if (r.get('stage') or '').lower()=='general':gov_by_race[str(r['race_id'])].append(r)

def parse_party_race(rr,seat_key='office_seat_name'):
    cand={}
    for r in rr:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or ''
        if not key:continue
        c=cand.setdefault(key,{'pid':pid,'votes':0,'parties':set(),'missing':False,'name':r.get('candidate_name') or ''})
        for q in ((r.get('ballot_party') or ''),(r.get('party') or '')):
            if q.strip():c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v:c['missing']=True
        else:
            try:c['votes']+=int(float(v))
            except:c['missing']=True
    cs=list(cand.values());ds=[c for c in cs if 'DEM' in c['parties']];rs=[c for c in cs if 'REP' in c['parties']]
    if len(ds)!=1 or len(rs)!=1 or ds[0]['missing'] or rs[0]['missing'] or ds[0]['votes']+rs[0]['votes']<=0:return None
    first=rr[0]
    try:cyc=int(first['cycle'])
    except:return None
    return {'cycle':cyc,'state_abbrev':first['state_abbrev'],'seat':first.get(seat_key,''),
            'y':100*(ds[0]['votes']-rs[0]['votes'])/(ds[0]['votes']+rs[0]['votes']),
            'd_pid':ds[0]['pid'],'r_pid':rs[0]['pid']}

govr=[]
for rr in gov_by_race.values():
    q=parse_party_race(rr)
    if q:govr.append(q)
gov_cycle_raw=defaultdict(list)
for r in govr:
    pv=pvi_state(r['cycle'],r['state_abbrev'])
    if pv is not None:gov_cycle_raw[r['cycle']].append(r['y']-pv)
gov_cycle_mean={c:sum(v)/len(v) for c,v in gov_cycle_raw.items() if v}
gov_by_pid=defaultdict(list)
for r in govr:
    pv=pvi_state(r['cycle'],r['state_abbrev'])
    if pv is None or r['cycle'] not in gov_cycle_mean:continue
    resid=r['y']-pv-gov_cycle_mean[r['cycle']]
    if r['d_pid']:gov_by_pid[r['d_pid']].append({'cycle':r['cycle'],'score':resid})
    if r['r_pid']:gov_by_pid[r['r_pid']].append({'cycle':r['cycle'],'score':-resid})

# House candidate residual: candidate D-R margin minus prior same-district D-R margin,
# adjusted for the national House swing between those cycles.
raw=urlopen(Request(HOUSE_URL,headers={'User-Agent':'CoreV2R-deduplicated/1.0'}),timeout=180).read()
if not raw.startswith(b'id,race_id,state_abbrev'):
    raise RuntimeError('House source header validation failed')
house_rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))
house_by_race=defaultdict(list)
for r in house_rows:
    if (r.get('stage') or '').lower()=='general':house_by_race[str(r['race_id'])].append(r)
houser=[]
for rr in house_by_race.values():
    q=parse_party_race(rr)
    if q:
        # District label must distinguish seats within state.
        q['seat']=(rr[0].get('office_seat_name') or rr[0].get('district') or rr[0].get('office_name') or '').strip()
        houser.append(q)
house_cycle_mean={}
for cyc in sorted(set(r['cycle'] for r in houser)):
    vals=[r['y'] for r in houser if r['cycle']==cyc]
    if vals:house_cycle_mean[cyc]=sum(vals)/len(vals)
house_seat=defaultdict(list)
for r in sorted(houser,key=lambda z:(z['state_abbrev'],z['seat'],z['cycle'])):
    house_seat[(r['state_abbrev'],r['seat'])].append(r)
house_by_pid=defaultdict(list)
for r in houser:
    prev=[x for x in house_seat[(r['state_abbrev'],r['seat'])] if x['cycle']==r['cycle']-2]
    if not prev or r['cycle'] not in house_cycle_mean or r['cycle']-2 not in house_cycle_mean:continue
    q=prev[-1]
    expected=q['y']+(house_cycle_mean[r['cycle']]-house_cycle_mean[r['cycle']-2])
    resid=r['y']-expected
    if r['d_pid']:house_by_pid[r['d_pid']].append({'cycle':r['cycle'],'score':resid,'seat':r['seat']})
    if r['r_pid']:house_by_pid[r['r_pid']].append({'cycle':r['cycle'],'score':-resid,'seat':r['seat']})

def prior_score(store,pid,cyc,k=2.0,exclude_race_id=None):
    vals=[]
    for x in store.get(pid,[]):
        if int(x['cycle'])>=cyc:continue
        if exclude_race_id is not None and str(x.get('race_id',''))==str(exclude_race_id):continue
        vals.append((int(x['cycle']),float(x['score'])))
    if not vals:return 0.0,0
    # recency weighting; latest statewide/district evidence dominates older evidence.
    vals.sort()
    num=den=0.0
    for y,s in vals:
        wt=math.exp(-(cyc-y)/8.0)
        num+=wt*s;den+=wt
    rawmean=num/den
    n=len(vals)
    return rawmean*n/(n+k),n

# Construct de-duplicated modeling panel.
data=[]
audit=[]
for s in rows:
    cyc=int(s['cycle']);rid=str(s['race_id'])
    rr=raceby.get((cyc,rid))
    if rr is None:continue
    prev=[x for x in seat_hist[(rr['state_abbrev'],rr['seat'])] if int(x['cycle'])<cyc]
    if not prev:continue
    q=max(prev,key=lambda x:int(x['cycle']))
    qpv=pvi_state(int(q['cycle']),q['state_abbrev'])
    if qpv is not None and int(q['cycle']) in sen_cycle_mean:
        same_resid=float(q['y'])-qpv-sen_cycle_mean[int(q['cycle'])]
        same_missing=0.0
    else:
        same_resid=0.0;same_missing=1.0

    dsen,dsen_n=prior_score(sen_by_pid,rr.get('d_pid',''),cyc,exclude_race_id=q['race_id'])
    rsen,rsen_n=prior_score(sen_by_pid,rr.get('r_pid',''),cyc,exclude_race_id=q['race_id'])
    dh,dh_n=prior_score(house_by_pid,rr.get('d_pid',''),cyc)
    rh,rh_n=prior_score(house_by_pid,rr.get('r_pid',''),cyc)
    dg,dg_n=prior_score(gov_by_pid,rr.get('d_pid',''),cyc)
    rg,rg_n=prior_score(gov_by_pid,rr.get('r_pid',''),cyc)

    x={
      'cycle':cyc,'race_id':rid,'state_abbrev':s['state_abbrev'],'y':float(s['y']),
      'pvi':float(s['pvi']),'same_raw':float(s['same_last']),'same_resid':same_resid,
      'same_gap':float(s['same_gap']),'same_missing':same_missing,
      'econ':float(s['econ']),'national':float(s['national']),
      'inc_diff':float(s['inc_diff']),'outparty':float(s['outparty']),
      'sen_personal_diff':dsen-rsen,'house_personal_diff':dh-rh,'gov_personal_diff':dg-rg,
      'candidate_evidence_n':dsen_n+rsen_n+dh_n+rh_n+dg_n+rg_n
    }
    data.append(x)
    if cyc in OUTER:
        audit.append({**x,'d_pid':rr.get('d_pid',''),'r_pid':rr.get('r_pid',''),
                      'same_source_race_id':q['race_id'],'same_source_cycle':q['cycle'],
                      'd_sen_n':dsen_n,'r_sen_n':rsen_n,'d_house_n':dh_n,'r_house_n':rh_n,'d_gov_n':dg_n,'r_gov_n':rg_n})

FEATURESETS={
 'raw_core':['pvi','same_raw','same_gap','econ','national','inc_diff','outparty'],
 'resid_core':['pvi','same_resid','same_gap','same_missing','econ','national','inc_diff','outparty'],
 'resid_sen':['pvi','same_resid','same_gap','same_missing','econ','national','inc_diff','outparty','sen_personal_diff'],
 'resid_house':['pvi','same_resid','same_gap','same_missing','econ','national','inc_diff','outparty','house_personal_diff'],
 'resid_state_house':['pvi','same_resid','same_gap','same_missing','econ','national','inc_diff','outparty','sen_personal_diff','house_personal_diff'],
 'resid_all_candidate':['pvi','same_resid','same_gap','same_missing','econ','national','inc_diff','outparty','sen_personal_diff','house_personal_diff','gov_personal_diff']
}
L_LOCAL=[4.0,16.0,64.0,256.0]
L_CONTEXT=[1.0,4.0,16.0,64.0]
L_INC=[4.0,16.0,64.0,256.0]
L_CAND=[4.0,16.0,64.0,256.0,1024.0]

def design(dat,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in dat],float)
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(dat)),(X-mu)/sd]),(mu,sd)

def fitpred(tr,te,features,ll,lc,li,lq):
    X,st=design(tr,features);Xt,_=design(te,features,st);y=np.array([r['y'] for r in tr],float)
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(features,start=1):
        if f in ('same_raw','same_resid','same_gap','same_missing'):pen[j]=ll
        elif f in ('econ','national'):pen[j]=lc
        elif f in ('inc_diff','outparty'):pen[j]=li
        elif 'personal_diff' in f:pen[j]=lq
        else:pen[j]=1e-8
    beta=np.linalg.pinv(X.T@X+np.diag(pen))@(X.T@y)
    return Xt@beta

def poll_post(r,prior):
    cyc=int(r['cycle']);target=ELECTION[cyc]-timedelta(days=45)
    agg=aggregate(poll_byrace.get((cyc,str(r['race_id'])),[]),target,30,14)
    if agg is None:return float(prior),0.0,0,''
    pm,neff,n=agg;w=.75*neff/(neff+.5)
    return (1-w)*float(prior)+w*pm,w,int(n),pm

def score(dat,preds):
    ok=0;mae=0.0
    for r,p in zip(dat,preds):
        post,_,_,_=poll_post(r,p)
        ok+=int((post>0)==(r['y']>0));mae+=abs(post-r['y'])
    return ok,mae/len(dat)

def choose(train):
    cycles=sorted(set(r['cycle'] for r in train));grid=[]
    for name,features in FEATURESETS.items():
      for ll,lc,li,lq in itertools.product(L_LOCAL,L_CONTEXT,L_INC,L_CAND):
        vr=[];vp=[]
        for vc in cycles[1:]:
            a=[r for r in train if r['cycle']<vc];b=[r for r in train if r['cycle']==vc]
            if len(a)<20 or not b:continue
            q=fitpred(a,b,features,ll,lc,li,lq);vr+=b;vp+=q.tolist()
        if not vr:continue
        ok,mae=score(vr,vp)
        # Primary: winner count after poll blend. Secondary: posterior MAE. Then simpler model.
        grid.append((-ok,mae,len(features),ll+lc+li+lq,name,ll,lc,li,lq,len(vr)))
    grid.sort()
    return grid[0],grid[:20]

pred=[];choices=[]
for tc in OUTER:
    tr=[r for r in data if r['cycle']<tc];te=[r for r in data if r['cycle']==tc]
    best,trace=choose(tr)
    negok,imae,nf,pen,name,ll,lc,li,lq,innern=best
    features=FEATURESETS[name]
    pri=fitpred(tr,te,features,ll,lc,li,lq)
    choices.append({'test_cycle':tc,'feature_set':name,'lambda_local':ll,'lambda_context':lc,'lambda_inc':li,'lambda_candidate':lq,
                    'inner_n':innern,'inner_correct':-negok,'inner_accuracy_pct':100*(-negok)/innern,'inner_post_mae':imae,
                    'top20':' | '.join(f'{z[4]} L{z[5]} C{z[6]} I{z[7]} Q{z[8]} correct={-z[0]}/{z[9]} mae={z[1]:.2f}' for z in trace)})
    for r,p in zip(te,pri):
        post,w,npoll,pm=poll_post(r,p)
        pred.append({'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],
                     'prior':float(p),'poll_margin':pm,'poll_weight':w,'poll_count':npoll,'posterior':post,
                     'correct':int((post>0)==(r['y']>0)),'feature_set':name,
                     'same_resid':r['same_resid'],'sen_personal_diff':r['sen_personal_diff'],
                     'house_personal_diff':r['house_personal_diff'],'gov_personal_diff':r['gov_personal_diff']})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['test_cycle']==int(scope)]
    n=len(rr);ok=sum(r['correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'correct':ok,'wrong':n-ok,'direction_accuracy_pct':100*ok/n})

for fn,arr in [('deduplicated_summary.csv',summary),('deduplicated_choices.csv',choices),('deduplicated_predictions.csv',pred),('deduplicated_feature_audit.csv',audit)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

wrong=[r for r in pred if not r['correct']]
target_states={('2014','NC'),('2018','NV'),('2018','MO'),('2018','FL'),('2018','IN')}
lines=['# De-duplicated fundamentals direction experiment','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: winner-direction accuracy after the fixed 45-day poll blend.',
'- This rebuild changes the fundamentals themselves rather than applying a post-hoc correction.','',
'## De-duplication','',
'1. SameSeat raw margin is replaced by a residual after removing the prior-cycle state PVI and the Senate cycle mean residual.',
'2. Senate candidate PersonalVote excludes the exact prior same-seat race used by SameSeat, preventing the same incumbent performance from entering twice.',
'3. Prior House candidate quality is measured as candidate-side district overperformance relative to the same district two years earlier after adjusting for the national House swing.',
'4. Prior governor candidate quality is measured as candidate-side gubernatorial residual from state PVI and the governor-cycle mean.',
'5. Incumbency and OutPartyIncumbent remain current-office effects rather than proxies for the prior election result.','',
'## Result','',
'| scope | N | correct | wrong | accuracy |','|---|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['correct']} | {r['wrong']} | {r['direction_accuracy_pct']:.1f}% |")
lines += ['','## Selected model by outer cycle','',
'| test | features | local ridge | context ridge | incumbent ridge | candidate ridge | inner accuracy | post MAE |',
'|---:|---|---:|---:|---:|---:|---:|---:|']
for r in choices:lines.append(f"| {r['test_cycle']} | {r['feature_set']} | {r['lambda_local']} | {r['lambda_context']} | {r['lambda_inc']} | {r['lambda_candidate']} | {r['inner_accuracy_pct']:.1f}% | {r['inner_post_mae']:.2f} |")
lines += ['','## Remaining wrong races','']
for r in wrong:lines.append(f"- {r['test_cycle']} {r['state_abbrev']} race {r['race_id']}: actual={r['actual']:.2f}, prior={r['prior']:.2f}, poll={r['poll_margin']}, posterior={r['posterior']:.2f}, features={r['feature_set']}")
lines += ['','## Five previously unresolved races','']
for r in pred:
    if (str(r['test_cycle']),r['state_abbrev']) in target_states:
        lines.append(f"- {r['test_cycle']} {r['state_abbrev']}: {'CORRECT' if r['correct'] else 'WRONG'}, actual={r['actual']:.2f}, prior={r['prior']:.2f}, posterior={r['posterior']:.2f}, SameSeatResidual={r['same_resid']:.2f}, SenatePV={r['sen_personal_diff']:.2f}, HousePV={r['house_personal_diff']:.2f}, GovPV={r['gov_personal_diff']:.2f}")
lines += ['','## Benchmark','',
'- Current accepted direction benchmark: fixed-poll reconstruction 94/99 = 94.9%.',
'- Adopt this rebuilt fundamentals architecture only if it exceeds 94/99 under chronological nested OOS.','',
'## Outputs','',
'- experiments/deduplicated_fundamentals/results/deduplicated_summary.csv',
'- experiments/deduplicated_fundamentals/results/deduplicated_choices.csv',
'- experiments/deduplicated_fundamentals/results/deduplicated_predictions.csv',
'- experiments/deduplicated_fundamentals/results/deduplicated_feature_audit.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
