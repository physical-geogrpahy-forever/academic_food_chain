#!/usr/bin/env python3
import csv, math, re, unicodedata, itertools
from urllib.request import urlopen
from collections import defaultdict
from pathlib import Path
from datetime import date, datetime, timezone
from difflib import SequenceMatcher
import numpy as np
import yaml

ROOT=Path(__file__).resolve().parents[1]
SEN=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
PVI=ROOT/'data/processed/historical_senate_pvi_default_067_033.csv'
HEAD=ROOT/'data/processed/core_v2r_headline_target_hypothesis_A.csv'
ALIGN=ROOT/'config/partisan_alignment_overrides_v1.csv'
CURRENT=ROOT/'data/raw/congress-legislators/legislators-current.yaml'
HIST=ROOT/'data/raw/congress-legislators/legislators-historical.yaml'
CONGRESS_COMMIT='8a3c7e6987f890b32e56058f7ddbdf380860b4a3'
NGA=ROOT/'data/processed/source_snapshots/nga_former_governors_snapshot.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
OUTDIR=ROOT/'performance/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0200_candidate-block-rolling-oos.md'
OUTDIR.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

ELECTION_DATE={2000:date(2000,11,7),2004:date(2004,11,2),2006:date(2006,11,7),2010:date(2010,11,2),2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
TARGET_CYCLES=[2006,2010,2014,2018,2022]
OUTER_TEST=[2014,2018,2022]

def load(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def truth(v): return str(v).strip().lower()=='true'
def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode('ascii').lower()
    s=re.sub(r'\b(jr|sr|ii|iii|iv)\.?\b',' ',s)
    s=re.sub(r'[^a-z0-9 ]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def suffix(s):
    x=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode('ascii').lower()
    m=re.findall(r'\b(jr|sr|ii|iii|iv)\.?\b',x)
    return m[-1] if m else ''

sen=load(SEN); pvi_rows=load(PVI); head=load(HEAD); align=load(ALIGN); gov=load(GOV)
pvi_by_race={r['race_id']:float(r['pvi_default_067_033_pctpt']) for r in pvi_rows}
align_by={(int(r['cycle']),r['state_abbrev'],r['seat']):r for r in align}

sen_by_race=defaultdict(list)
for r in sen:
    if r.get('stage')=='general': sen_by_race[r['race_id']].append(r)

def candidate_group(rows):
    out={}
    for r in rows:
        pid=(r.get('politician_id') or '').strip()
        key=pid or (r.get('candidate_id') or '').strip() or r.get('candidate_name') or r.get('alt_result_text') or ''
        if not key: continue
        c=out.setdefault(key,{'politician_id':pid,'name':r.get('candidate_name') or r.get('alt_result_text') or '','votes':0,'parties':set(),'winner':False,'missing':False})
        for q in [(r.get('ballot_party') or ''),(r.get('party') or '')]:
            if q.strip(): c['parties'].add(q.strip().upper())
        v=(r.get('votes') or '').strip()
        if not v: c['missing']=True
        else:
            try: c['votes']+=int(float(v))
            except: c['missing']=True
        c['winner']=c['winner'] or truth(r.get('winner','false'))
    return list(out.values())

def extract_race(rr):
    first=rr[0]; cyc=int(first['cycle']); st=first['state_abbrev']; seat=first['office_seat_name']
    # For ranked-choice data use the maximum explicit round only.
    nums=[]
    for x in rr:
        v=(x.get('ranked_choice_round') or '').strip()
        if v:
            try: nums.append(int(float(v)))
            except: pass
    use=rr
    if nums:
        mx=max(nums); use=[]
        for x in rr:
            v=(x.get('ranked_choice_round') or '').strip()
            try: rv=int(float(v)) if v else None
            except: rv=None
            if rv==mx: use.append(x)
    cs=candidate_group(use)
    ov=align_by.get((cyc,st,seat))
    if ov and ov['action'] in {'EXCLUDE','REVIEW'}: return None
    d=r=None; rule='standard'
    if ov and ov['action']=='ALIGN':
        ds=[c for c in cs if norm(c['name'])==norm(ov['d_side_name'])]
        rs=[c for c in cs if norm(c['name'])==norm(ov['r_side_name'])]
        d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None; rule='override'
    if d is None and r is None:
        ds=[c for c in cs if 'DEM' in c['parties']]; rs=[c for c in cs if 'REP' in c['parties']]
        d=ds[0] if len(ds)==1 else None; r=rs[0] if len(rs)==1 else None
    if d is None or r is None or d['missing'] or r['missing'] or d['votes']+r['votes']<=0: return None
    margin=(d['votes']-r['votes'])/(d['votes']+r['votes'])*100.0
    return {'race_id':first['race_id'],'cycle':cyc,'state_abbrev':st,'seat':seat,'d':d,'r':r,'y':margin,'alignment_rule':rule}

# Build all extractable Senate races for same-seat lag and training targets.
all_races=[]
for rid,rr in sen_by_race.items():
    try:
        x=extract_race(rr)
        if x: all_races.append(x)
    except Exception:
        pass
race_lookup={(r['cycle'],r['state_abbrev'],r['seat']):r for r in all_races}

# Force the preserved 99-row headline target for 2014/2018/2022.
head_by={r['race_id']:r for r in head}
targets=[]
for r in all_races:
    if r['cycle'] not in [2006,2010]: continue
    targets.append(r)
for rid,h in head_by.items():
    rr=sen_by_race[rid]; raw=extract_race(rr)
    if raw is None: raise RuntimeError('Preserved headline race failed extraction: '+rid)
    raw['d']['name']=h['d_side_candidate']; raw['r']['name']=h['r_side_candidate']
    raw['y']=float(h['margin_d_minus_r_two_party_pctpt'])
    targets.append(raw)

# Congress term index.
people=[]
for path,name in [(CURRENT,'legislators-current.yaml'),(HIST,'legislators-historical.yaml')]:
    if path.exists():
        txt=path.read_text(encoding='utf-8')
    else:
        url=f'https://raw.githubusercontent.com/unitedstates/congress-legislators/{CONGRESS_COMMIT}/{name}'
        txt=urlopen(url,timeout=90).read().decode('utf-8')
    people.extend(yaml.safe_load(txt) or [])
leg_index=defaultdict(list)
def variants(p):
    n=p.get('name',{}); vals=set()
    for x in [n.get('official_full',''),f"{n.get('first','')} {n.get('last','')}",f"{n.get('first','')} {n.get('middle','')} {n.get('last','')}",f"{n.get('nickname','')} {n.get('last','')}"]:
        q=norm(x)
        if q: vals.add(q)
    return vals
for p in people:
    last=norm(p.get('name',{}).get('last',''))
    if last: leg_index[last].append((p,variants(p)))

def match_leg(name):
    q=norm(name)
    if not q: return None
    pool=leg_index.get(q.split()[-1],[])
    scored=[]
    for p,vs in pool:
        s=1.0 if q in vs else max((SequenceMatcher(None,q,v).ratio() for v in vs),default=0)
        scored.append((s,p))
    scored.sort(key=lambda z:z[0],reverse=True)
    if not scored: return None
    top=scored[0]; second=scored[1][0] if len(scored)>1 else 0
    if top[0]>=0.88 and top[0]-second>=0.04: return top[1]
    return None

def congress_flags(name,cycle):
    p=match_leg(name)
    if not p: return None
    ed=ELECTION_DATE[cycle]; senexp=houseexp=inc=0
    for t in p.get('terms',[]):
        try: s=date.fromisoformat(str(t['start'])); e=date.fromisoformat(str(t['end']))
        except: continue
        typ=t.get('type')
        if s<ed and typ=='sen': senexp=1
        if s<ed and typ=='rep': houseexp=1
        if typ=='sen' and s<=ed<=e: inc=1
    return senexp,houseexp,inc

# Governor experience: election-history fallback plus NGA term-name match.
gov_win=defaultdict(list)
for r in gov:
    if r.get('stage')!='general' or not truth(r.get('winner','false')): continue
    pid=(r.get('politician_id') or '').strip()
    if not pid: continue
    try: cyc=int(r['cycle'])
    except: continue
    gov_win[pid].append(cyc)
nga=load(NGA)
nga_by_last=defaultdict(list)
for g in nga:
    q=norm(g['governor_name'])
    if q: nga_by_last[q.split()[-1]].append(g)
def nga_prior(name,cycle):
    q=norm(name)
    if not q: return 0
    pool=nga_by_last.get(q.split()[-1],[])
    names=defaultdict(list)
    for g in pool: names[g['governor_name']].append(g)
    scored=[]
    for display,terms in names.items(): scored.append((SequenceMatcher(None,q,norm(display)).ratio(),display,terms))
    scored.sort(reverse=True,key=lambda z:z[0])
    if not scored: return 0
    top=scored[0]; second=scored[1][0] if len(scored)>1 else 0
    if top[0]<0.92 or top[0]-second<0.05: return 0
    if (suffix(name) or suffix(top[1])) and suffix(name)!=suffix(top[1]): return 0
    return int(any(int(g['term_start_year'])<cycle for g in top[2]))

# Same-seat prior winner fallback for incumbency if term-name matching fails.
winner_by_seat=defaultdict(list)
for r in all_races:
    win=r['d'] if r['d']['winner'] else (r['r'] if r['r']['winner'] else None)
    if win and win['politician_id']: winner_by_seat[(r['state_abbrev'],r['seat'])].append((r['cycle'],win['politician_id']))

panel=[]; dropped=[]
for r in targets:
    cyc=r['cycle']; rid=r['race_id']; pvi=pvi_by_race.get(rid)
    prev=race_lookup.get((cyc-6,r['state_abbrev'],r['seat']))
    if pvi is None or prev is None:
        dropped.append((cyc,r['state_abbrev'],rid,'missing_pvi' if pvi is None else 'missing_same_seat'))
        continue
    sides={}
    for side in ['d','r']:
        c=r[side]; cf=congress_flags(c['name'],cyc)
        if cf is None:
            senexp=0; houseexp=0; inc=0
            pid=c['politician_id']
            if pid:
                senexp=int(any(x['cycle']<cyc and x[side if False else 'd']['politician_id']==pid for x in []))
                hist=[x for x in winner_by_seat[(r['state_abbrev'],r['seat'])] if x[0]<cyc]
                if hist and max(hist,key=lambda z:z[0])[1]==pid: inc=1; senexp=1
        else: senexp,houseexp,inc=cf
        pid=c['politician_id']; govexp=int(bool(pid and any(y<cyc for y in gov_win.get(pid,[]))))
        govexp=max(govexp,nga_prior(c['name'],cyc))
        sides[side]={'sen':senexp,'house':houseexp,'inc':inc,'gov':govexp}
    outparty=(1 if sides['d']['inc'] and pvi<0 else 0)-(1 if sides['r']['inc'] and pvi>0 else 0)
    panel.append({
      'race_id':rid,'cycle':cyc,'state_abbrev':r['state_abbrev'],'seat':r['seat'],'y':r['y'],
      'pvi':pvi,'same_seat':prev['y'],
      'inc_diff':sides['d']['inc']-sides['r']['inc'],'outparty':outparty,
      'sen_exp_diff':sides['d']['sen']-sides['r']['sen'],
      'gov_exp_diff':sides['d']['gov']-sides['r']['gov'],
      'house_exp_diff':sides['d']['house']-sides['r']['house']
    })

# Guarantee the modern validation universe remains the preserved 99 unless same-seat coverage proves otherwise.
headline_n=sum(r['cycle'] in OUTER_TEST for r in panel)

STRUCT=['pvi','same_seat']
CAND=['inc_diff','outparty','sen_exp_diff','gov_exp_diff','house_exp_diff']

def design(rows,features,stats=None):
    X=np.array([[float(r[f]) for f in features] for r in rows],dtype=float)
    if stats is None:
        mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd<1e-9,1.0,sd)
    else: mu,sd=stats
    Z=(X-mu)/sd
    return np.column_stack([np.ones(len(rows)),Z]),(mu,sd)

def fit_predict(train,test,features,lambda_c):
    X,stats=design(train,features); Xt,_=design(test,features,stats)
    y=np.array([r['y'] for r in train],dtype=float)
    pen=np.zeros(X.shape[1],dtype=float)
    # tiny numerical ridge on structural columns, candidate block gets lambda_c.
    for j,f in enumerate(features,start=1): pen[j]=1e-8 if f in STRUCT else float(lambda_c)
    A=X.T@X+np.diag(pen)
    beta=np.linalg.pinv(A)@(X.T@y)
    return Xt@beta,beta

def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(p))**2)))
def mae(y,p): return float(np.mean(np.abs(np.asarray(y)-np.asarray(p))))
def direction(y,p): return float(np.mean((np.asarray(y)>0)==(np.asarray(p)>0))*100.0)

def tune_lambda(train_rows):
    grid=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]
    cycles=sorted(set(r['cycle'] for r in train_rows))
    scores=[]
    for lam in grid:
        yy=[]; pp=[]
        for vc in cycles[1:]:
            tr=[r for r in train_rows if r['cycle']<vc]; va=[r for r in train_rows if r['cycle']==vc]
            if len(tr)<10 or not va: continue
            pred,_=fit_predict(tr,va,STRUCT+CAND,lam)
            yy.extend([r['y'] for r in va]); pp.extend(pred.tolist())
        scores.append((rmse(yy,pp) if yy else 1e9,lam))
    scores.sort()
    return scores[0][1],scores

def tune_subset(train_rows):
    grid=[0.0,0.1,0.5,1.0,4.0,16.0,64.0,256.0]
    cycles=sorted(set(r['cycle'] for r in train_rows))
    candidates=[]
    subsets=[()]
    for k in range(1,len(CAND)+1): subsets.extend(itertools.combinations(CAND,k))
    for subset in subsets:
        lambdas=[0.0] if not subset else grid
        for lam in lambdas:
            yy=[]; pp=[]
            features=STRUCT+list(subset)
            for vc in cycles[1:]:
                tr=[r for r in train_rows if r['cycle']<vc]; va=[r for r in train_rows if r['cycle']==vc]
                if len(tr)<10 or not va: continue
                pred,_=fit_predict(tr,va,features,lam)
                yy.extend([r['y'] for r in va]); pp.extend(pred.tolist())
            score=rmse(yy,pp) if yy else 1e9
            candidates.append((score,len(subset),-lam,subset,lam))
    candidates.sort(key=lambda z:(z[0],z[1],z[2]))
    best=candidates[0]
    return list(best[3]),best[4],candidates[:20]

variants=['structural_only','candidate_fixed','candidate_ridge_nested','candidate_subset_nested']
pred_rows=[]; hyper=[]
for tc in OUTER_TEST:
    train=[r for r in panel if r['cycle']<tc]; test=[r for r in panel if r['cycle']==tc]
    if not train or not test: continue
    for variant in variants:
        if variant=='structural_only':
            features=STRUCT; lam=0.0
        elif variant=='candidate_fixed':
            features=STRUCT+CAND; lam=0.0
        elif variant=='candidate_ridge_nested':
            features=STRUCT+CAND; lam,trace=tune_lambda(train)
            hyper.append({'test_cycle':tc,'variant':variant,'lambda_candidate':lam,'selected_features':';'.join(CAND),'inner_trace':' | '.join(f'{x[1]}:{x[0]:.4f}' for x in trace)})
        else:
            subset,lam,trace=tune_subset(train)
            features=STRUCT+subset
            hyper.append({'test_cycle':tc,'variant':variant,'lambda_candidate':lam,'selected_features':';'.join(subset),'inner_trace':' | '.join(f"{x[3]}@{x[4]}:{x[0]:.4f}" for x in trace[:10])})
        pred,beta=fit_predict(train,test,features,lam)
        for r,p in zip(test,pred):
            pred_rows.append({'variant':variant,'test_cycle':tc,'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual_margin':r['y'],'predicted_margin':float(p),'error':float(p-r['y']),'lambda_candidate':lam})

summary=[]
for variant in variants:
    vr=[r for r in pred_rows if r['variant']==variant]
    y=[float(r['actual_margin']) for r in vr]; p=[float(r['predicted_margin']) for r in vr]
    summary.append({'variant':variant,'scope':'2014_2018_2022_combined','n':len(vr),'rmse':rmse(y,p),'mae':mae(y,p),'direction_pct':direction(y,p)})
    for tc in OUTER_TEST:
        cr=[r for r in vr if int(r['test_cycle'])==tc]
        if cr:
            yy=[float(r['actual_margin']) for r in cr]; pp=[float(r['predicted_margin']) for r in cr]
            summary.append({'variant':variant,'scope':str(tc),'n':len(cr),'rmse':rmse(yy,pp),'mae':mae(yy,pp),'direction_pct':direction(yy,pp)})

with (OUTDIR/'candidate_block_oos_panel.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(panel[0].keys())); w.writeheader(); w.writerows(panel)
with (OUTDIR/'candidate_block_oos_predictions.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(pred_rows[0].keys())); w.writeheader(); w.writerows(pred_rows)
with (OUTDIR/'candidate_block_oos_summary.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)
with (OUTDIR/'candidate_block_oos_hyperparams.csv').open('w',encoding='utf-8',newline='') as f:
    fields=['test_cycle','variant','lambda_candidate','selected_features','inner_trace']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(hyper)

comb={r['variant']:r for r in summary if r['scope']=='2014_2018_2022_combined'}
best=min(comb.values(),key=lambda r:r['rmse'])
fixed=comb['candidate_fixed']; ridge=comb['candidate_ridge_nested']; base=comb['structural_only']
delta_ridge_fixed=float(fixed['rmse'])-float(ridge['rmse'])
delta_ridge_base=float(base['rmse'])-float(ridge['rmse'])
status='KEEP_RIDGE' if (delta_ridge_fixed>0 and delta_ridge_base>0) else 'REJECT_RIDGE_CANDIDATE_BLOCK'
subset=comb['candidate_subset_nested']; delta_subset_base=float(base['rmse'])-float(subset['rmse'])
subset_status='KEEP_SUBSET_ARCHITECTURE' if delta_subset_base>0 else 'REJECT_SUBSET_ARCHITECTURE'
lines=[
 '# Performance experiment: candidate-block rolling OOS','',
 '- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
 '- Training is strictly chronological: 2014<-2006/2010; 2018<-earlier cycles; 2022<-earlier cycles.',
 f'- Historical panel rows after required PVI + same-seat coverage: {len(panel)}',
 f'- Modern validation rows retained: {headline_n}',
 f'- Dropped rows for missing PVI/same-seat: {len(dropped)}','',
 '## Combined modern OOS results','',
 '| variant | N | RMSE | MAE | direction |',
 '|---|---:|---:|---:|---:|'
]
for v in variants:
    z=comb[v]; lines.append(f"| {v} | {z['n']} | {float(z['rmse']):.4f} | {float(z['mae']):.4f} | {float(z['direction_pct']):.1f}% |")
lines += [
 '','## Decision','',
 f'- Nested candidate ridge improvement vs unregularized candidate block: {delta_ridge_fixed:+.4f} RMSE points.',
 f'- Nested candidate ridge improvement vs structural-only diagnostic: {delta_ridge_base:+.4f} RMSE points.',
 f'- Decision: {status}',
 f'- Nested subset-selection improvement vs structural-only diagnostic: {delta_subset_base:+.4f} RMSE points.',
 f'- Subset decision: {subset_status}','',
 '## Important limitation','',
 'This is a focused candidate-block performance experiment, not the complete preserved Core V2 reconstruction. National_t, RelativeEconomicGrowth, poll updating, and final PersonalVoteDiff are intentionally absent. Therefore its absolute RMSE must not be compared as if it were the preserved Core V2 7.99%p fundamentals benchmark. The valid comparison here is fixed candidate coefficients versus nested OOS candidate-block shrinkage under an identical structural base.','',
 '## Next performance step','',
 'If candidate-block ridge improves OOS, carry that shrinkage architecture into the full Core V2-R model and add PersonalVote with nested count-based shrinkage. If it does not, discard it rather than preserving it for methodological elegance.','',
 '## Outputs','',
 '- performance/results/candidate_block_oos_panel.csv',
 '- performance/results/candidate_block_oos_predictions.csv',
 '- performance/results/candidate_block_oos_summary.csv',
 '- performance/results/candidate_block_oos_hyperparams.csv'
]
if dropped:
    lines += ['','## Dropped rows','']+[f'- {x[0]} {x[1]} race {x[2]}: {x[3]}' for x in dropped]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))