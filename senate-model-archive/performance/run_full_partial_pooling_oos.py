#!/usr/bin/env python3
import csv, io, zipfile, statistics, itertools
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
TRAIN=ROOT/'performance/results/candidate_block_oos_panel.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
NAT=ROOT/'performance/results/national_45d_values.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0220_full-partial-pooling-oos.md'
BEA_URL='https://apps.bea.gov/regional/zip/SQINC.zip'
OUTDIR.mkdir(parents=True,exist_ok=True)

STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
PRES_SIGN={2006:-1,2010:1,2014:1,2018:-1,2022:1}
OUTER=[2014,2018,2022]

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
train=load(TRAIN); head=load(HEAD); natrows=load(NAT); nat={int(r['cycle']):float(r['national_margin_d_minus_r']) for r in natrows}

rows=[]
for r in train:
    if int(r['cycle']) not in (2006,2010):continue
    rows.append({'race_id':r['race_id'],'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'y':float(r['y']),
      'pvi':float(r['pvi']),'same_last':float(r['same_seat']),'same_gap':6.0,
      'inc_diff':float(r['inc_diff']),'outparty':float(r['outparty']),'sen_exp_diff':float(r['sen_exp_diff']),
      'gov_exp_diff':float(r['gov_exp_diff']),'house_exp_diff':float(r['house_exp_diff']),
      'd_pv_mean':0.0,'d_pv_n':0,'r_pv_mean':0.0,'r_pv_n':0})
for r in head:
    rows.append({'race_id':r['race_id'],'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'y':float(r['margin_d_minus_r_two_party_pctpt']),
      'pvi':float(r['pvi_default_067_033_pctpt']),'same_last':float(r['same_seat_last_prior_margin_two_party_pctpt']),'same_gap':float(r['same_seat_last_prior_year_gap']),
      'inc_diff':float(r['IncumbencyDiff']),'outparty':float(r['OutPartyIncumbent']),'sen_exp_diff':float(r['SenateExperienceDiff']),
      'gov_exp_diff':float(r['GovernorExperienceDiff']),'house_exp_diff':float(r['HouseExperienceDiff']),
      'd_pv_mean':float(r['d_personal_mean_overperf_cycle_adjusted_pctpt']) if r['d_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0,
      'd_pv_n':int(r['d_personal_prior_statewide_count']),'r_pv_mean':float(r['r_personal_mean_overperf_cycle_adjusted_pctpt']) if r['r_personal_mean_overperf_cycle_adjusted_pctpt'] else 0.0,
      'r_pv_n':int(r['r_personal_prior_statewide_count'])})

# Economic coding: revised SQINC1 diagnostic, same as prior signal test.
raw=urlopen(Request(BEA_URL,headers={'User-Agent':'CoreV2R-performance/1.0'}),timeout=120).read(); zf=zipfile.ZipFile(io.BytesIO(raw))
csvnames=[n for n in zf.namelist() if n.lower().endswith('.csv') and Path(n).name.upper().startswith('SQINC1__ALL_AREAS_')]
if not csvnames:raise RuntimeError('No SQINC1 all-areas CSV')
name=max(csvnames,key=lambda n:zf.getinfo(n).file_size)
bea=list(csv.DictReader(io.StringIO(zf.read(name).decode('utf-8-sig','replace')))); pi=[r for r in bea if (r.get('LineCode') or '').strip()=='1']
def val(r,c):
    try:return float((r.get(c) or '').replace(',','').strip())
    except:return None
growth={};us={};cycles=sorted(set(r['cycle'] for r in rows))
for x in pi:
    nm=(x.get('GeoName') or '').replace('*','').strip()
    for cyc in cycles:
        a=val(x,f'{cyc}:Q1');b=val(x,f'{cyc-1}:Q1')
        if a is None or b in (None,0):continue
        g=100*(a/b-1)
        if nm in STATE_ABBR:growth[(cyc,STATE_ABBR[nm])]=g
        elif nm=='United States':us[cyc]=g
for r in rows:
    cyc=r['cycle']; vals=[growth[(cyc,s)] for s in STATE_ABBR.values() if (cyc,s) in growth]; ng=us.get(cyc,statistics.mean(vals))
    r['econ']=(growth[(cyc,r['state_abbrev'])]-ng)*PRES_SIGN[cyc]
    r['national']=nat[cyc]

BASE=['pvi','same_last','same_gap','econ','national']
GROUPS={
 'inc':['inc_diff','outparty'],
 'exp':['sen_exp_diff','gov_exp_diff','house_exp_diff'],
 'pv':['pv_diff'],
}
NG=[16.0,64.0,256.0,1024.0]
EG=[0.0,16.0,64.0,256.0]
LG=[16.0,64.0,256.0,1024.0]
KG=[1.0,4.0,16.0,64.0]

def pvscore(r,k):
    dn=r['d_pv_n'];rn=r['r_pv_n']
    d=r['d_pv_mean']*dn/(dn+k) if dn>0 else 0.0
    q=r['r_pv_mean']*rn/(rn+k) if rn>0 else 0.0
    return d-q
def prep(data,k):
    out=[]
    for r in data:
        x=dict(r);x['pv_diff']=pvscore(r,k);out.append(x)
    return out
def design(data,feats,stats=None):
    X=np.array([[float(r[f]) for f in feats] for r in data])
    if stats is None:
        mu=X.mean(0);sd=X.std(0);sd=np.where(sd<1e-9,1.0,sd)
    else:mu,sd=stats
    return np.column_stack([np.ones(len(data)),(X-mu)/sd]),(mu,sd)
def fitpred(tr,te,groups=(),ln=64.0,le=0.0,ll=64.0,k=16.0):
    tr=prep(tr,k);te=prep(te,k)
    feats=list(BASE)
    for g in groups:feats+=GROUPS[g]
    X,st=design(tr,feats);Xt,_=design(te,feats,st);y=np.array([r['y'] for r in tr])
    pen=np.zeros(X.shape[1])
    for j,f in enumerate(feats,start=1):
        if f=='national':pen[j]=ln
        elif f=='econ':pen[j]=le
        elif f in sum((GROUPS[g] for g in groups),[]):pen[j]=ll
        else:pen[j]=1e-8
    A=X.T@X+np.diag(pen);beta=np.linalg.pinv(A)@(X.T@y);return Xt@beta
def rmse(y,p):return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p):return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def acc(y,p):return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100)

def tune(tr,allow_groups=True):
    cycs=sorted(set(r['cycle'] for r in tr));cands=[]
    subsets=[()]
    if allow_groups:
        names=list(GROUPS)
        for n in range(1,len(names)+1):subsets.extend(itertools.combinations(names,n))
    for gs in subsets:
      klist=KG if 'pv' in gs else [16.0]
      for k in klist:
       for ln in NG:
        for le in EG:
         for ll in ([64.0] if not gs else LG):
          yy=[];pp=[]
          for vc in cycs[1:]:
            a=[r for r in tr if r['cycle']<vc];b=[r for r in tr if r['cycle']==vc]
            if len(a)<10 or not b:continue
            q=fitpred(a,b,gs,ln,le,ll,k);yy.extend(r['y'] for r in b);pp.extend(q.tolist())
          cands.append((rmse(yy,pp) if yy else 1e9,len(gs),ln,le,ll,k,gs))
    cands.sort(key=lambda z:(z[0],z[1],z[2]+z[3]+z[4]));return cands[0],cands

predrows=[];choices=[]
for tc in OUTER:
    tr=[r for r in rows if r['cycle']<tc];te=[r for r in rows if r['cycle']==tc]
    for variant,allow in [('base_nested',False),('full_nested',True)]:
        best,trace=tune(tr,allow);sc,_,ln,le,ll,k,gs=best;q=fitpred(tr,te,gs,ln,le,ll,k)
        choices.append({'test_cycle':tc,'variant':variant,'groups':';'.join(gs),'lambda_national':ln,'lambda_econ':le,'lambda_local':ll,'personal_k':k,'inner_rmse':sc,'top10':' | '.join(f'{z[6]} n{z[2]} e{z[3]} l{z[4]} k{z[5]}:{z[0]:.3f}' for z in trace[:10])})
        for r,p in zip(te,q):predrows.append({'variant':variant,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':r['y'],'predicted':float(p),'error':float(p)-r['y'],'groups':';'.join(gs),'lambda_national':ln,'lambda_econ':le,'lambda_local':ll,'personal_k':k})

summary=[]
for v in ['base_nested','full_nested']:
    z=[r for r in predrows if r['variant']==v];y=[float(r['actual']) for r in z];p=[float(r['predicted']) for r in z]
    summary.append({'variant':v,'n':len(z),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':acc(y,p)})
for fn,data in [('full_partial_pooling_summary.csv',summary),('full_partial_pooling_choices.csv',choices),('full_partial_pooling_predictions.csv',predrows)]:
    with (OUTDIR/fn).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0].keys()));w.writeheader();w.writerows(data)
b=summary[0];f=summary[1];delta=float(b['rmse'])-float(f['rmse'])
lines=['# Full partial-pooling performance experiment','',f'- Generated UTC: {datetime.now(timezone.utc).isoformat()}',
'- 99 preserved headline rows for 2014, 2018, 2022.',
'- Structural base: PVI + last-prior SameSeat + gap + signed relative income growth + 45-day generic ballot.',
'- Candidate groups: incumbency/out-party, prior elected-office experience, PersonalVote.',
'- All optional groups are selected only inside chronological inner OOS and use shared ridge shrinkage.','',
'## Results','', '| variant | N | RMSE | MAE | direction |','|---|---:|---:|---:|---:|']
for z in summary:lines.append(f"| {z['variant']} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += ['','## Choices by outer cycle','', '| cycle | variant | groups | lambda N | lambda econ | lambda local | personal k | inner RMSE |','|---:|---|---|---:|---:|---:|---:|---:|']
for z in choices:lines.append(f"| {z['test_cycle']} | {z['variant']} | {z['groups'] or 'NONE'} | {z['lambda_national']} | {z['lambda_econ']} | {z['lambda_local']} | {z['personal_k']} | {float(z['inner_rmse']):.4f} |")
lines += ['','## Decision','',f'- Candidate/PersonalVote increment versus nested strong base: {delta:+.4f} RMSE points.',f'- Decision: {"KEEP_FULL_LOCAL_BLOCK" if delta>0 else "REJECT_FULL_LOCAL_BLOCK"}.',
'- Economic data remain revised-vintage diagnostic until historical release vintages are substituted.','',
'## Outputs','', '- performance/results/full_partial_pooling_summary.csv','- performance/results/full_partial_pooling_choices.csv','- performance/results/full_partial_pooling_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))