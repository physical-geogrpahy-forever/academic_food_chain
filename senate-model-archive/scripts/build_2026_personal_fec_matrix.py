#!/usr/bin/env python3
import csv, io, re, urllib.request, zipfile, statistics
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
SEN_HIST=ROOT/'data/raw/fivethirtyeight/election_results_senate_2026-09-21.csv'
GOV=ROOT/'data/processed/source_snapshots/election_results_gubernatorial_d7a7cff101da.csv'
LEAN=ROOT/'data/processed/presidential_state_lean.csv'
STRUCT=ROOT/'data/snapshots/2026_structural_input_matrix_45d.csv'
EXP=ROOT/'data/snapshots/2026_candidate_experience_core.csv'
POLL=ROOT/'data/snapshots/2026_poll_45d_recency_proxy.csv'
OUT=ROOT/'data/snapshots/2026_production_input_matrix_45d.csv'
PVOUT=ROOT/'data/snapshots/2026_personal_vote_core.csv'
FECOUT=ROOT/'data/snapshots/2026_fec_june30_top50.csv'
DOC=ROOT/'docs/analysis/2026_PRODUCTION_INPUT_MATRIX_45D.md'

SEN2024_URL='https://raw.githubusercontent.com/MEDSL/2024-elections-official/main/2024-senate-state.csv'
FEC_TABLES={'receipts':'6a','individual':'6b','cash':'6f'}

TARGETS={
'AK':('Mary Peltola','Dan Sullivan'),
'GA':('Jon Ossoff','Mike Collins'),
'IA':('Josh Turek','Ashley Hinson'),
'ME':('Troy Jackson','Susan Collins'),
'MI':('Abdul El-Sayed','Mike Rogers'),
'NH':('Chris Pappas','John Sununu'),
'NC':('Roy Cooper','Michael Whatley'),
'OH':('Sherrod Brown','Jon Husted'),
'TX':('James Talarico','Ken Paxton'),
}

ALIASES={
'Mary Peltola':['mary peltola'],
'Dan Sullivan':['dan sullivan','daniel sullivan'],
'Jon Ossoff':['jon ossoff','thomas jonathan ossoff'],
'Mike Collins':['mike collins','michael collins'],
'Josh Turek':['josh turek','joshua turek'],
'Ashley Hinson':['ashley hinson'],
'Troy Jackson':['troy jackson'],
'Susan Collins':['susan collins','susan m collins','susan margaret collins'],
'Abdul El-Sayed':['abdul el sayed','abdul elsayed'],
'Mike Rogers':['mike rogers','michael rogers'],
'Chris Pappas':['chris pappas','christopher pappas'],
'John Sununu':['john sununu','john e sununu'],
'Roy Cooper':['roy cooper','roy asberry cooper'],
'Michael Whatley':['michael whatley'],
'Sherrod Brown':['sherrod brown'],
'Jon Husted':['jon husted','jon a husted'],
'James Talarico':['james talarico'],
'Ken Paxton':['ken paxton','warren kenneth paxton'],
}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):
    s=(s or '').lower().replace("’","'")
    s=re.sub(r'\b(jr|sr|ii|iii|iv|mr|mrs|ms|dr|sen)\b',' ',s)
    s=re.sub(r"[^a-z0-9 ]+",' ',s)
    return re.sub(r'\s+',' ',s).strip()
def party_side(text):
    t=(text or '').upper()
    if 'DEM' in t or 'DFL' in t:return 'D'
    if 'REP' in t or 'GOP' in t:return 'R'
    return ''
def two_party_margin(d,r):
    return 100*(d-r)/(d+r) if d+r else None

# Presidential state lean and PVI for arbitrary cycle.
lean={}
for r in load(LEAN):
    try:lean[(int(r['cycle']),r['state_abbrev'])]=float(r['lean_vs_national_pctpt'])
    except:pass
def pvi_for(cycle,st):
    ys=sorted(y for (y,s) in lean if s==st and y<cycle)
    if len(ys)<2:return None
    return .67*lean[(ys[-1],st)]+.33*lean[(ys[-2],st)]

# Historical Senate races through 2022.
sen_rows=load(SEN_HIST)
sen_races=[]
grp=defaultdict(list)
for r in sen_rows:
    if (r.get('stage') or '').lower()=='general':
        grp[(int(r['cycle']),str(r['race_id']),r['state_abbrev'])].append(r)
for (cyc,rid,st),rr in grp.items():
    # RCV: highest round only.
    rounds=[]
    for x in rr:
        q=(x.get('ranked_choice_round') or '').strip()
        if q:
            try:rounds.append(int(float(q)))
            except:pass
    if rounds:
        mx=max(rounds);rr=[x for x in rr if (x.get('ranked_choice_round') or '').strip() and int(float(x['ranked_choice_round']))==mx]
    cands={}
    for x in rr:
        key=(x.get('politician_id') or x.get('candidate_id') or x.get('candidate_name') or '').strip()
        if not key:continue
        c=cands.setdefault(key,{'name':x.get('candidate_name') or '','votes':0,'party':''})
        try:c['votes']+=int(float(x.get('votes') or 0))
        except:pass
        ps=party_side((x.get('ballot_party') or '')+' '+(x.get('party') or ''))
        if ps:c['party']=ps
    ds=[c for c in cands.values() if c['party']=='D'];rs=[c for c in cands.values() if c['party']=='R']
    if len(ds)==1 and len(rs)==1 and ds[0]['votes']+rs[0]['votes']>0:
        sen_races.append({'cycle':cyc,'state':st,'margin':two_party_margin(ds[0]['votes'],rs[0]['votes']),
                          'D':ds[0]['name'],'R':rs[0]['name'],'source':'538 election-results'})

# Add MEDSL 2024 statewide Senate results only when the historical raw does not already contain 2024.
if not any(r['cycle']==2024 for r in sen_races):
    raw=urllib.request.urlopen(urllib.request.Request(SEN2024_URL,headers={'User-Agent':'CoreV2R-2026-personal/1.0'}),timeout=120).read()
    med=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig','replace'))))
    grp=defaultdict(list)
    for r in med:
        if (r.get('stage') or '').upper()=='GEN' and (r.get('mode') or '').upper()=='TOTAL':
            grp[r['state_po']].append(r)
    for st,rr in grp.items():
        cands=defaultdict(lambda:{'votes':0,'party':'','name':''})
        for x in rr:
            name=x.get('candidate') or ''
            if not name or name.upper() in {'UNDERVOTES','OVERVOTES','VOID','SCATTERING','WRITE-IN'}:continue
            key=norm(name)
            c=cands[key];c['name']=name
            try:c['votes']+=int(float(x.get('votes') or 0))
            except:pass
            ps=party_side(x.get('party_simplified') or x.get('party_detailed') or '')
            if ps:c['party']=ps
        ds=[c for c in cands.values() if c['party']=='D'];rs=[c for c in cands.values() if c['party']=='R']
        if len(ds)==1 and len(rs)==1 and ds[0]['votes']+rs[0]['votes']>0:
            sen_races.append({'cycle':2024,'state':st,'margin':two_party_margin(ds[0]['votes'],rs[0]['votes']),
                              'D':ds[0]['name'],'R':rs[0]['name'],'source':'MEDSL 2024 official collection'})

# Governor general elections.
gov_rows=load(GOV);gov_races=[]
grp=defaultdict(list)
for r in gov_rows:
    if (r.get('stage') or '').lower()=='general':
        grp[(int(r['cycle']),str(r['race_id']),r['state_abbrev'])].append(r)
for (cyc,rid,st),rr in grp.items():
    cands={}
    for x in rr:
        key=(x.get('politician_id') or x.get('candidate_id') or x.get('candidate_name') or '').strip()
        if not key:continue
        c=cands.setdefault(key,{'name':x.get('candidate_name') or '','votes':0,'party':''})
        try:c['votes']+=int(float(x.get('votes') or 0))
        except:pass
        ps=party_side((x.get('ballot_party') or '')+' '+(x.get('party') or ''))
        if ps:c['party']=ps
    ds=[c for c in cands.values() if c['party']=='D'];rs=[c for c in cands.values() if c['party']=='R']
    if len(ds)==1 and len(rs)==1 and ds[0]['votes']+rs[0]['votes']>0:
        gov_races.append({'cycle':cyc,'state':st,'margin':two_party_margin(ds[0]['votes'],rs[0]['votes']),
                          'D':ds[0]['name'],'R':rs[0]['name'],'source':'538 election-results gubernatorial'})

# Cycle mean residual by office.
def scored(races):
    cycvals=defaultdict(list);valid=[]
    for r in races:
        pv=pvi_for(r['cycle'],r['state'])
        if pv is None:continue
        resid=r['margin']-pv
        cycvals[r['cycle']].append(resid);valid.append((r,pv,resid))
    means={c:statistics.mean(v) for c,v in cycvals.items() if v}
    out=[]
    for r,pv,resid in valid:
        if r['cycle'] not in means:continue
        adj=resid-means[r['cycle']]
        out.append({**r,'pvi':pv,'raw_resid':resid,'cycle_mean_resid':means[r['cycle']],'adj_resid':adj})
    return out,means
sen_scored,sen_means=scored(sen_races)
gov_scored,gov_means=scored(gov_races)

def candidate_match(target, observed):
    q=norm(observed)
    aliases=ALIASES.get(target,[norm(target)])
    if q in aliases:return True
    for a in aliases:
        if SequenceMatcher(None,a,q).ratio()>=0.88:return True
    return False

def history_for(target,cycle=2026):
    hist=[]
    for office,arr in [('Senate',sen_scored),('Governor',gov_scored)]:
        for r in arr:
            if r['cycle']>=cycle:continue
            if candidate_match(target,r['D']):
                hist.append({'office':office,'cycle':r['cycle'],'state':r['state'],'side':'D','candidate':r['D'],
                             'score':r['adj_resid'],'raw_resid':r['raw_resid'],'source':r['source']})
            if candidate_match(target,r['R']):
                hist.append({'office':office,'cycle':r['cycle'],'state':r['state'],'side':'R','candidate':r['R'],
                             'score':-r['adj_resid'],'raw_resid':-r['raw_resid'],'source':r['source']})
    return sorted(hist,key=lambda x:(x['cycle'],x['office']))

pvrows=[]
for st,(dc,rc) in TARGETS.items():
    rec={'state_abbrev':st,'candidate_D':dc,'candidate_R':rc}
    for side,cand in [('D',dc),('R',rc)]:
        h=history_for(cand)
        rec[side+'_prior_statewide_count']=len(h)
        rec[side+'_prior_senate_count']=sum(x['office']=='Senate' for x in h)
        rec[side+'_prior_governor_count']=sum(x['office']=='Governor' for x in h)
        rec[side+'_personal_mean_cycle_adjusted_pctpt']=statistics.mean(x['score'] for x in h) if h else ''
        rec[side+'_personal_latest_cycle']=max((x['cycle'] for x in h),default='')
        rec[side+'_personal_history']=' | '.join(f"{x['office']} {x['cycle']} {x['state']} score={x['score']:.2f}" for x in h)
    d=rec['D_personal_mean_cycle_adjusted_pctpt'];r=rec['R_personal_mean_cycle_adjusted_pctpt']
    rec['PersonalVoteDiff_D_minus_R_pctpt']=(float(d) if d!='' else 0.0)-(float(r) if r!='' else 0.0)
    pvrows.append(rec)

PVOUT.parent.mkdir(parents=True,exist_ok=True)
with PVOUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(pvrows[0].keys()));w.writeheader();w.writerows(pvrows)

# FEC candidate-summary bulk, strict June-30 coverage.
WEBALL_URL='https://www.fec.gov/files/bulk-downloads/2026/weball26.zip'
WEBALL_HEADER_URL='https://www.fec.gov/files/bulk-downloads/data_dictionaries/weball_header_file.csv'

def parse_money(v):
    s=str(v or '').replace('$','').replace(',','').strip()
    try:return float(s)
    except:return None

bulk=get(WEBALL_URL)
zf=zipfile.ZipFile(io.BytesIO(bulk))
txtname=next(n for n in zf.namelist() if n.lower().endswith('.txt'))
lines=zf.read(txtname).decode('utf-8-sig','replace').splitlines()

# FEC publishes the header dictionary separately.
hraw=get(WEBALL_HEADER_URL).decode('utf-8-sig','replace')
hrows=list(csv.reader(io.StringIO(hraw)))
headers=hrows[0]
fec_records=[]
for line in lines:
    vals=line.split('|')
    if len(vals)<len(headers):
        vals += ['']*(len(headers)-len(vals))
    rec={headers[i]:vals[i] if i<len(vals) else '' for i in range(len(headers))}
    fec_records.append(rec)

def hget(rec,*names):
    low={k.lower():v for k,v in rec.items()}
    for n in names:
        if n.lower() in low:return low[n.lower()]
    return ''

strict=[]
for r in fec_records:
    office=hget(r,'CAND_OFFICE','Cand_Office')
    st=hget(r,'CAND_OFFICE_ST','Cand_Office_St').upper()
    cov=hget(r,'CVG_END_DT','Coverage_End_Date')
    if office.upper()!='S' or len(st)!=2:continue
    if cov not in ('06/30/2026','06/30/26'):continue
    strict.append(r)

def match_bulk(st,target,side):
    aliases=ALIASES.get(target,[norm(target)])
    pool=[]
    for r in strict:
        rst=hget(r,'CAND_OFFICE_ST','Cand_Office_St').upper()
        if rst!=st:continue
        name=hget(r,'CAND_NAME','Cand_Name')
        n=norm(name)
        if not n:continue
        score=max(SequenceMatcher(None,a,n).ratio() for a in aliases)
        party=party_side(hget(r,'CAND_PTY_AFFILIATION','Cand_Party_Affiliation'))
        if party==side:score+=.06
        pool.append((score,r))
    pool.sort(key=lambda z:z[0],reverse=True)
    if not pool or pool[0][0]<.72:return None
    if len(pool)>1 and pool[0][0]-pool[1][0]<.03:return None
    return pool[0][1]

fecrows=[]
for st,(dc,rc) in TARGETS.items():
    rec={'state_abbrev':st,'candidate_D':dc,'candidate_R':rc}
    dm=match_bulk(st,dc,'D');rm=match_bulk(st,rc,'R')
    for side,obj in [('D',dm),('R',rm)]:
        if obj:
            rec[side+'_fec_name']=hget(obj,'CAND_NAME','Cand_Name')
            rec[side+'_fec_coverage_end']=hget(obj,'CVG_END_DT','Coverage_End_Date')
            rec[side+'_receipts']=parse_money(hget(obj,'TTL_RECEIPTS','Total_Receipt'))
            rec[side+'_individual']=parse_money(hget(obj,'INDV_CONTRIB','Individual_Contribution'))
            rec[side+'_cash']=parse_money(hget(obj,'COH_COP','Cash_On_Hand_COP'))
        else:
            rec[side+'_fec_name']='';rec[side+'_fec_coverage_end']=''
            rec[side+'_receipts']='';rec[side+'_individual']='';rec[side+'_cash']=''
    for metric in ['receipts','individual','cash']:
        dv=rec['D_'+metric];rv=rec['R_'+metric]
        rec[metric+'_share_D_minus_R']=(dv-rv)/(dv+rv) if dv!='' and rv!='' and dv+rv>0 else ''
    rec['fec_source']=WEBALL_URL
    rec['fec_cutoff_rule']='Coverage_End_Date exactly 06/30/2026'
    fecrows.append(rec)

with FECOUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(fecrows[0].keys()));w.writeheader();w.writerows(fecrows)

# Join structural, experience, poll, PersonalVote, FEC.
def index(rows,key='state_abbrev'):return {r[key]:r for r in rows}
S=index(load(STRUCT));E=index(load(EXP));P=index(load(POLL));PV=index(pvrows);F=index(fecrows)
joined=[]
for st in TARGETS:
    r={}
    for block in (S[st],E[st],P[st],PV[st],F[st]):
        for k,v in block.items():
            if k in ('candidate_D','candidate_R','state_abbrev') and k in r:continue
            r[k]=v
    joined.append(r)
with OUT.open('w',encoding='utf-8',newline='') as f:
    fields=[]
    for r in joined:
        for k in r:
            if k not in fields:fields.append(k)
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(joined)

# Documentation.
DOC.parent.mkdir(parents=True,exist_ok=True)
lines=['# 2026 production input matrix at the exact 45-day cutoff','',
'- Cutoff: 2026-09-19 U.S. calendar date.',
'- This matrix joins the frozen structural layer, Core candidate experience, PersonalVote history, poll diagnostic rows, and FEC June-30 Top-50 finance fields.',
'- No 2026-09-20 or later information is used.','',
'## PersonalVote','',
'PersonalVote follows the Core historical definition:',
'- prior Senate and Governor general elections only',
'- candidate-side two-party margin residual versus cycle-specific PVI',
'- subtract the same-office same-cycle mean residual',
'- House and state-legislative performance are not inserted into PersonalVote',
'- 2024 Senate races are added from MEDSL 2024 official results collection','',
'| State | D candidate | D prior statewide | D PV | R candidate | R prior statewide | R PV | PV diff D-R |',
'|---|---|---:|---:|---|---:|---:|---:|']
for r in pvrows:
    d='NA' if r['D_personal_mean_cycle_adjusted_pctpt']=='' else f"{float(r['D_personal_mean_cycle_adjusted_pctpt']):.2f}"
    q='NA' if r['R_personal_mean_cycle_adjusted_pctpt']=='' else f"{float(r['R_personal_mean_cycle_adjusted_pctpt']):.2f}"
    lines.append(f"| {r['state_abbrev']} | {r['candidate_D']} | {r['D_prior_statewide_count']} | {d} | {r['candidate_R']} | {r['R_prior_statewide_count']} | {q} | {r['PersonalVoteDiff_D_minus_R_pctpt']:.2f} |")
lines += ['','## FEC June-30 block','',
'- Source family: FEC 2025-2026 candidate-summary bulk file (weball26.zip), filtered to Coverage_End_Date exactly 06/30/2026.',
'- Metrics: total receipts, contributions from individuals, cash on hand.',
'- A D-R share is computed only when both candidates have an exact 06/30/2026 candidate-summary record.',
'- Candidates whose latest bulk-summary coverage does not equal 06/30/2026 remain missing; later reporting periods are never back-filled or treated as June-30 data.','',
'| State | receipts share | individual share | cash share |',
'|---|---:|---:|---:|']
for r in fecrows:
    def fmt(k):
        return 'NA' if r[k]=='' else f"{float(r[k]):.3f}"
    lines.append(f"| {r['state_abbrev']} | {fmt('receipts_share_D_minus_R')} | {fmt('individual_share_D_minus_R')} | {fmt('cash_share_D_minus_R')} |")
lines += ['','## Output','',
'- data/snapshots/2026_production_input_matrix_45d.csv',
'- data/snapshots/2026_personal_vote_core.csv',
'- data/snapshots/2026_fec_june30_top50.csv','',
'## Interpretation boundary','',
'This file is a model-input artifact. It does not itself constitute a winner forecast or election-outcome probability.']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
