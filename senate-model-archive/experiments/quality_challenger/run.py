#!/usr/bin/env python3
import csv, json, re, time, math, itertools
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import date, datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
CAND=ROOT/'data/processed/core_v2r_headline_candidate_experience_audit.csv'
DM=ROOT/'data/processed/core_v2r_headline_design_matrix_with_personal_vote_audit.csv'
BASE=ROOT/'experiments/poll_direction/results/poll_fixed_predictions.csv'
OUT=ROOT/'experiments/quality_challenger/results'
DOC=ROOT/'docs/history/updates/2026-09-21_0440_quality-challenger-state-office-direction.md'
OUT.mkdir(parents=True,exist_ok=True); DOC.parent.mkdir(parents=True,exist_ok=True)

ELECTION={2014:date(2014,11,4),2018:date(2018,11,6),2022:date(2022,11,8)}
STATE_FULL={'AK':'Alaska','AL':'Alabama','AR':'Arkansas','AZ':'Arizona','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','IA':'Iowa','ID':'Idaho','IL':'Illinois','IN':'Indiana','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','MA':'Massachusetts','MD':'Maryland','ME':'Maine','MI':'Michigan','MN':'Minnesota','MO':'Missouri','MS':'Mississippi','MT':'Montana','NC':'North Carolina','ND':'North Dakota','NE':'Nebraska','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NV':'Nevada','NY':'New York','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VA':'Virginia','VT':'Vermont','WA':'Washington','WI':'Wisconsin','WV':'West Virginia','WY':'Wyoming'}

def load(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):
    s=(s or '').lower()
    s=re.sub(r'\b(jr|sr|ii|iii|iv)\b',' ',s)
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def api(params,tries=4):
    url='https://www.wikidata.org/w/api.php?'+urlencode(params)
    for t in range(tries):
        try:
            req=Request(url,headers={'User-Agent':'CoreV2R-quality-audit/1.0 research'})
            with urlopen(req,timeout=60) as resp:return json.load(resp)
        except Exception:
            if t==tries-1:raise
            time.sleep(1.2*(t+1))

cands=load(CAND); dm=load(DM); base=[r for r in load(BASE) if r['variant']=='w30_h14_all']
dmby={r['race_id']:r for r in dm}

people={}
for r in cands:
    for side in ('d','r'):
        name=r[f'{side}_candidate']
        people[(int(r['cycle']),r['state_abbrev'],name)]={'cycle':int(r['cycle']),'state_abbrev':r['state_abbrev'],'name':name,'politician_id':r.get(f'{side}_politician_id','')}

# Resolve candidate identities and P39 positions in a single Wikidata SPARQL request.
# This avoids per-candidate API rate limits from GitHub Actions.
variant_to_keys={}
def variants(name):
    out=[name]
    x=re.sub(r'\b(Jr\.?|Sr\.?|II|III|IV)\b','',name,flags=re.I)
    x=re.sub(r'\s+',' ',x.replace(',',' ')).strip()
    out.append(x)
    toks=x.split()
    toks2=[t for t in toks if not re.fullmatch(r'[A-Z]\.?',t)]
    if toks2:out.append(' '.join(toks2))
    if len(toks)>=2:out.append(toks[0]+' '+toks[-1])
    return list(dict.fromkeys(v for v in out if v))
for key,p in people.items():
    for v in variants(p['name']):
        variant_to_keys.setdefault(v,[]).append(key)

def sparql_escape(s):
    return s.replace('\\','\\\\').replace('"','\\"')
vals=' '.join('"'+sparql_escape(v)+'"@en' for v in variant_to_keys)
query='''SELECT ?needle ?person ?personLabel ?personDescription ?position ?positionLabel ?start ?end WHERE {
  VALUES ?needle { %s }
  ?person (rdfs:label|skos:altLabel) ?needle .
  OPTIONAL {
    ?person p:P39 ?statement .
    ?statement ps:P39 ?position .
    OPTIONAL { ?statement pq:P580 ?start . }
    OPTIONAL { ?statement pq:P582 ?end . }
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}''' % vals

body=urlencode({'query':query,'format':'json'}).encode()
req=Request('https://query.wikidata.org/sparql',data=body,headers={
    'User-Agent':'CoreV2R-quality-audit/1.0 research',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept':'application/sparql-results+json'
})
sparql=None
for t in range(5):
    try:
        with urlopen(req,timeout=180) as resp:sparql=json.load(resp)
        break
    except Exception:
        if t==4:raise
        time.sleep(5*(t+1))

raw_candidates={}
for b in sparql.get('results',{}).get('bindings',[]):
    needle=b.get('needle',{}).get('value','')
    pqid=b.get('person',{}).get('value','').rsplit('/',1)[-1]
    if not needle or not pqid:continue
    rec=raw_candidates.setdefault((needle,pqid),{
        'qid':pqid,'label':b.get('personLabel',{}).get('value',''),
        'description':b.get('personDescription',{}).get('value',''),'claims':[]
    })
    pos=b.get('positionLabel',{}).get('value','')
    if pos:
        rec['claims'].append({
            'label':pos,
            'start':b.get('start',{}).get('value',''),
            'end':b.get('end',{}).get('value','')
        })

matches={}
entity_claims={}
for key,p in people.items():
    name=p['name'];st=STATE_FULL.get(p['state_abbrev'],p['state_abbrev'])
    options=[]
    for v in variants(name):
        for (needle,qid),rec in raw_candidates.items():
            if needle!=v:continue
            score=0
            if norm(rec['label'])==norm(name):score+=12
            nt=norm(name).split();lt=norm(rec['label']).split()
            if nt and lt and nt[0]==lt[0] and nt[-1]==lt[-1]:score+=5
            dl=rec['description'].lower()
            if any(w in dl for w in ['politician','senator','representative','governor','attorney general','mayor','legislator']):score+=4
            if st.lower() in dl:score+=2
            if norm(v)==norm(name):score+=2
            options.append((score,qid,rec))
    options.sort(key=lambda z:-z[0])
    if options and options[0][0]>=9:
        score,qid,rec=options[0]
        matches[key]={'qid':qid,'label':rec['label'],'description':rec['description'],'match_score':score,'status':'MATCHED'}
        entity_claims[qid]=rec['claims']
    else:
        matches[key]={'qid':'','label':'','description':'','match_score':options[0][0] if options else 0,'status':'NO_CONFIDENT_MATCH'}

def iso_date(s):
    if not s:return None
    try:
        return datetime.fromisoformat(s.replace('Z','+00:00')).date()
    except:return None

def classify(label):
    x=label.lower()
    if 'united states senator' in x or 'member of the united states house of representatives' in x:return 'federal'
    if 'governor of' in x and 'lieutenant' not in x:return 'governor'
    statewide=['attorney general','lieutenant governor','secretary of state','state treasurer','treasurer of','state auditor','auditor of','comptroller','superintendent of public instruction','commissioner of agriculture','commissioner of insurance','commissioner of public lands']
    if any(k in x for k in statewide):return 'statewide'
    leg=['state senate','senate of ','house of representatives','house of delegates','state assembly','general assembly','legislative assembly','speaker of the']
    if any(k in x for k in leg) and 'united states' not in x:return 'state_legislative'
    if any(k in x for k in ['mayor of','county executive','county commissioner','city council','board of supervisors']):return 'local'
    return ''

audit=[]
for key,p in people.items():
    cyc,st,name=key;m=matches[key];cut=ELECTION[cyc];eligible=[];undated=[]
    for cl in entity_claims.get(m['qid'],[]) if m['qid'] else []:
        lab=cl['label'];cls=classify(lab)
        if not cls:continue
        start=iso_date(cl.get('start',''));end=iso_date(cl.get('end',''))
        prior=(start is not None and start<cut) or (start is None and end is not None and end<cut)
        if prior:eligible.append((cls,lab,start.isoformat() if start else '',end.isoformat() if end else ''))
        elif start is None and end is None:undated.append((cls,lab))
    cs={x[0] for x in eligible}
    tier=3 if 'statewide' in cs else (2 if 'state_legislative' in cs else (1 if 'local' in cs else 0))
    audit.append({'cycle':cyc,'state_abbrev':st,'candidate_name':name,'politician_id':p['politician_id'],'wikidata_qid':m['qid'],'match_status':m['status'],'match_score':m['match_score'],'wikidata_label':m['label'],'wikidata_description':m['description'],'state_local_quality_tier':tier,'prior_eligible_offices':' | '.join(f'{a}:{b}[{c},{d}]' for a,b,c,d in eligible),'undated_eligible_offices_review':' | '.join(f'{a}:{b}' for a,b in undated)})

aby={(int(r['cycle']),r['state_abbrev'],r['candidate_name']):r for r in audit}
raceq=[]
for r in cands:
    cyc=int(r['cycle']);st=r['state_abbrev'];d=dmby[r['race_id']]
    def sideq(side):
        name=r[f'{side}_candidate'];a=aby.get((cyc,st,name),{})
        stier=int(a.get('state_local_quality_tier',0) or 0)
        fed=int(float(d.get(f'{side}_senate_experience',0) or 0)) or int(float(d.get(f'{side}_house_experience',0) or 0))
        gov=int(float(d.get(f'{side}_governor_experience',0) or 0))
        tier=4 if (fed or gov) else stier
        return tier,a.get('wikidata_qid',''),a.get('prior_eligible_offices','')
    dt,dqid,doff=sideq('d');rt,rqid,roff=sideq('r')
    dinc=int(float(d.get('d_incumbency',0) or 0));rinc=int(float(d.get('r_incumbency',0) or 0))
    if dinc and not rinc:chall='R';ct=rt
    elif rinc and not dinc:chall='D';ct=dt
    else:chall='';ct=0
    raceq.append({'race_id':r['race_id'],'cycle':cyc,'state_abbrev':st,'d_candidate':r['d_candidate'],'r_candidate':r['r_candidate'],'d_quality_tier':dt,'r_quality_tier':rt,'d_wikidata_qid':dqid,'r_wikidata_qid':rqid,'d_prior_offices':doff,'r_prior_offices':roff,'incumbent_side':'D' if dinc else ('R' if rinc else ''),'challenger_side':chall,'challenger_quality_tier':ct})
qby={r['race_id']:r for r in raceq}

data=[]
for r in base:
    d=dmby[r['race_id']];q=qby[r['race_id']]
    outparty=int(float(d.get('OutPartyIncumbent',0) or 0))
    dinc=int(float(d.get('d_incumbency',0) or 0));rinc=int(float(d.get('r_incumbency',0) or 0))
    if dinc:
        pv=float(d.get('d_personal_mean_overperf_cycle_adjusted_pctpt') or 0);pn=int(float(d.get('d_personal_prior_statewide_count') or 0));incsign=1
    elif rinc:
        pv=float(d.get('r_personal_mean_overperf_cycle_adjusted_pctpt') or 0);pn=int(float(d.get('r_personal_prior_statewide_count') or 0));incsign=-1
    else:pv=0.;pn=0;incsign=0
    pvi=float(d['pvi_default_067_033_pctpt']);host=max(0.0,-incsign*pvi) if incsign else 0.0
    data.append({'cycle':int(r['test_cycle']),'race_id':r['race_id'],'state_abbrev':r['state_abbrev'],'actual':float(r['actual']),'posterior':float(r['posterior']),'outparty':outparty,'incsign':incsign,'pvi':pvi,'hostility':host,'inc_personal':pv,'inc_personal_n':pn,'challenger_quality_tier':int(q['challenger_quality_tier'])})

GAMMA=[0,1,2,3,4,5,6,8,10,12]
ETA=[0,0.05,0.1,0.15,0.2,0.3,0.4]
TAU=[3,5,8,12,20,40,999]
QTYPES=['binary','tier']
CAP=[3,5,8,12,20,999]

def protection(r,tau):
    if tau>=999:return 1.0
    n=r['inc_personal_n'];pv=max(0.0,r['inc_personal']*(n/(n+1.0) if n else 0.0))
    return 1.0/(1.0+pv/tau)
def qvalue(r,mode):
    q=r['challenger_quality_tier']
    if q<=0:return 0.0
    return 1.0 if mode=='binary' else q/4.0
def predict(r,g,e,t,mode,cap):
    p=r['posterior'];q=qvalue(r,mode)
    if r['incsign']==0 or q<=0:return p
    direction=-r['incsign'];host=r['hostility'] if r['outparty']!=0 else 0.0
    mag=(g+e*host)*q*protection(r,t)
    if cap<999:mag=min(mag,cap)
    return p+direction*mag
def evaluate(dat,p):
    ok=flips=0
    for r in dat:
        q=predict(r,*p);ok+=int((q>0)==(r['actual']>0));flips+=int((q>0)!=(r['posterior']>0))
    return ok,flips

PARAMS=list(itertools.product(GAMMA,ETA,TAU,QTYPES,CAP))
pred=[];choices=[]
for tc in [2014,2018,2022]:
    train=[r for r in data if r['cycle']<tc];test=[r for r in data if r['cycle']==tc]
    if not train:
        best=(0,0,999,'binary',999);trainok=0;trainflips=0;trace=[]
    else:
        cand=[]
        for p in PARAMS:
            ok,flips=evaluate(train,p);g,e,t,m,cap=p
            complexity=g+e*10+(0 if t>=999 else 1)+(0 if m=='binary' else 1)+(0 if cap>=999 else 1)
            cand.append((-ok,flips,complexity,p))
        cand.sort(key=lambda z:(z[0],z[1],z[2]))
        z=cand[0];best=z[3];trainok=-z[0];trainflips=z[1];trace=cand[:20]
    choices.append({'test_cycle':tc,'gamma':best[0],'hostility_eta':best[1],'personal_tau':best[2],'quality_mode':best[3],'cap':best[4],'train_n':len(train),'train_correct':trainok if train else '','train_accuracy_pct':(100*trainok/len(train) if train else ''),'train_flips':trainflips,'top20':' | '.join(f'g{z[3][0]} e{z[3][1]} t{z[3][2]} {z[3][3]} cap{z[3][4]} correct={-z[0]} flips={z[1]}' for z in trace)})
    for r in test:
        p=predict(r,*best)
        pred.append({**r,'adjusted_posterior':p,'baseline_correct':int((r['posterior']>0)==(r['actual']>0)),'adjusted_correct':int((p>0)==(r['actual']>0)),'protection':protection(r,best[2]),'quality_value':qvalue(r,best[3]),'gamma':best[0],'hostility_eta':best[1],'personal_tau':best[2],'quality_mode':best[3],'cap':best[4]})

summary=[]
for scope in ['combined','2014','2018','2022']:
    rr=pred if scope=='combined' else [r for r in pred if r['cycle']==int(scope)]
    n=len(rr);b=sum(r['baseline_correct'] for r in rr);a=sum(r['adjusted_correct'] for r in rr)
    summary.append({'scope':scope,'n':n,'baseline_correct':b,'baseline_accuracy_pct':100*b/n,'adjusted_correct':a,'adjusted_accuracy_pct':100*a/n,'net_correct_gain':a-b,'direction_flips':sum((r['posterior']>0)!=(r['adjusted_posterior']>0) for r in rr)})

for fn,arr in [('quality_candidate_audit.csv',audit),('quality_race_features.csv',raceq),('quality_summary.csv',summary),('quality_choices.csv',choices),('quality_predictions.csv',pred)]:
    with (OUT/fn).open('w',encoding='utf-8',newline='') as f:
        fields=list(arr[0].keys());w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(arr)

changed=[r for r in pred if r['baseline_correct']!=r['adjusted_correct']]
targets={('2014','NC'),('2018','NV'),('2018','MO'),('2018','FL'),('2018','IN')}
review=[r for r in audit if r['match_status']!='MATCHED' or r['undated_eligible_offices_review']]
lines=['# QualityChallenger with state-office audit','',
'- Generated UTC: '+datetime.now(timezone.utc).isoformat(),
'- Primary objective: historical winner-direction accuracy.',
'- Candidate-quality coding is fixed before model scoring and applied uniformly to every headline candidate.',
'- Existing Senate, House, and Governor experience is merged with pre-election Wikidata P39 office history.',
'- New office tiers: statewide elected executive=3, state legislature=2, local elected office=1, existing federal or Governor experience=4.',
'- Undated Wikidata office claims are not automatically counted, preventing post-election office leakage.','',
'## Result','',
'| scope | N | baseline correct | baseline acc | adjusted correct | adjusted acc | net | flips |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append(f"| {r['scope']} | {r['n']} | {r['baseline_correct']} | {r['baseline_accuracy_pct']:.1f}% | {r['adjusted_correct']} | {r['adjusted_accuracy_pct']:.1f}% | {r['net_correct_gain']:+d} | {r['direction_flips']} |")
lines += ['','## Selected rule by outer cycle','',
'| test | gamma | hostility eta | personal tau | quality mode | cap | train accuracy | flips |',
'|---:|---:|---:|---:|---|---:|---:|---:|']
for r in choices:
    ta='NA' if r['train_accuracy_pct']=='' else f"{r['train_accuracy_pct']:.1f}%"
    lines.append(f"| {r['test_cycle']} | {r['gamma']} | {r['hostility_eta']} | {r['personal_tau']} | {r['quality_mode']} | {r['cap']} | {ta} | {r['train_flips']} |")
lines += ['','## Correctness changes','']
for r in changed:lines.append(f"- {r['cycle']} {r['state_abbrev']} race {r['race_id']}: baseline {'correct' if r['baseline_correct'] else 'wrong'} -> adjusted {'correct' if r['adjusted_correct'] else 'wrong'}, posterior {r['posterior']:.2f}->{r['adjusted_posterior']:.2f}, challenger tier={r['challenger_quality_tier']}, hostility={r['hostility']:.2f}, incumbent personal={r['inc_personal']:.2f}")
lines += ['','## Five unresolved races','']
for r in pred:
    if (str(r['cycle']),r['state_abbrev']) in targets:
        q=qby[r['race_id']]
        lines.append(f"- {r['cycle']} {r['state_abbrev']}: {'CORRECT' if r['adjusted_correct'] else 'WRONG'}, challenger={q['challenger_side']} tier={q['challenger_quality_tier']}, baseline={r['posterior']:.2f}, adjusted={r['adjusted_posterior']:.2f}, hostility={r['hostility']:.2f}, incumbent personal={r['inc_personal']:.2f}")
lines += ['','## Audit review load',f'- Candidate-side records requiring review or containing undated eligible office claims: {len(review)} of {len(audit)}.','- Full rows are preserved in quality_candidate_audit.csv; review-only offices are not used automatically.','',
'## Decision','- Current accepted benchmark: 94/99.','- Adopt only if adjusted accuracy exceeds 94/99 with parameters selected from earlier cycles only.','',
'## Outputs','- experiments/quality_challenger/results/quality_candidate_audit.csv','- experiments/quality_challenger/results/quality_race_features.csv','- experiments/quality_challenger/results/quality_summary.csv','- experiments/quality_challenger/results/quality_choices.csv','- experiments/quality_challenger/results/quality_predictions.csv']
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
