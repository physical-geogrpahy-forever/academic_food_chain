#!/usr/bin/env python3
"""
Build strategic-resource candidate strengths and Civ-style integer quantities.

This stage does NOT perform final gameplay thinning. It converts heterogeneous
source evidence into within-resource percentile strength and candidate quantity.

Output fields for each strategic resource:
  <ID>_EVIDENCE_RAW
  <ID>_STRENGTH      0..1 within-resource percentile among positive evidence
  <ID>_CANDIDATE_QTY integer Civ quantity; 0 means no evidence

Physical magnitudes are never compared across different resources.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

RANGES={
    "HORSES":(2,4),
    "IRON":(2,6),
    "NITER":(2,6),
    "COAL":(2,7),
    "OIL":(2,7),
    "ALUMINUM":(3,8),
    "URANIUM":(1,4),
}

def col(df,name):
    return pd.to_numeric(df[name],errors="coerce").fillna(0).clip(lower=0) if name in df.columns else pd.Series(0.0,index=df.index)

def pct_positive(x):
    x=pd.to_numeric(x,errors="coerce").fillna(0).clip(lower=0)
    out=pd.Series(0.0,index=x.index,dtype="float64")
    pos=x.gt(0)
    if not pos.any(): return out
    # Average ranks are deterministic for ties.
    out.loc[pos]=x.loc[pos].rank(method="average",pct=True)
    return out

def max_pct(*xs):
    if not xs: raise ValueError("no evidence")
    pp=[pct_positive(x) for x in xs]
    return pd.concat(pp,axis=1).max(axis=1)

def qty_from_strength(strength,raw,qmin,qmax):
    n=qmax-qmin+1
    s=pd.to_numeric(strength,errors="coerce").fillna(0).clip(0,1)
    q=(qmin+np.floor(np.minimum(s,1-1e-12)*n)).astype("int16")
    q=pd.Series(q,index=s.index)
    q.loc[pd.to_numeric(raw,errors="coerce").fillna(0).le(0)]=0
    return q

def build(board):
    # HORSES: livestock density is the quantitative evidence.
    horse_mean=col(board,"HORSE_GLW_MEAN")
    horse_max=col(board,"HORSE_GLW_MAX")
    horse_raw=np.log1p(horse_mean)+0.20*np.log1p(horse_max)
    horse_s=pct_positive(horse_raw)

    # IRON / ALUMINUM: MRDS commodity priority + deposit-size evidence.
    def mrds_resource(prefix):
        score=col(board,f"{prefix}_MRDS_SCORE")
        smax=col(board,f"{prefix}_MRDS_SIZE_MAX")
        ssum=col(board,f"{prefix}_MRDS_SIZE_SUM")
        raw=np.log1p(score)+0.75*smax+0.25*np.log1p(ssum)
        return raw,pct_positive(raw)

    iron_raw,iron_s=mrds_resource("IRON")
    alu_raw,alu_s=mrds_resource("ALUMINUM")

    # OIL: preserve both reserves and production. Use the strongest percentile
    # among quantitative measures and field/status evidence.
    oil_res=col(board,"OIL_GEM_RESERVE_EV")
    oil_prod=col(board,"OIL_GEM_PRODUCTION_EV")
    oil_fields=col(board,"OIL_GEM_FIELDS")
    oil_status=col(board,"OIL_GEM_SCORE")
    oil_raw=np.log1p(oil_res)+np.log1p(oil_prod)+0.25*np.log1p(oil_fields)+0.10*np.log1p(oil_status)
    oil_s=max_pct(oil_res,oil_prod,oil_raw)

    # COAL: production/capacity dominate; reserve/resource fields are used when
    # a later evidence stage provides them.
    coal_prod=col(board,"COAL_GEM_PROD_MT")
    coal_cap=col(board,"COAL_GEM_CAP_MTPA")
    coal_res=col(board,"COAL_GEM_RESERVE_MT")
    coal_resource=col(board,"COAL_GEM_RESOURCE_MT")
    coal_score=col(board,"COAL_GEM_SCORE")
    coal_raw=np.log1p(coal_prod)+np.log1p(coal_cap)+np.log1p(coal_res)+0.5*np.log1p(coal_resource)+0.10*np.log1p(coal_score)
    coal_s=max_pct(coal_prod,coal_cap,coal_res,coal_resource,coal_raw)

    # URANIUM: UThDEPO resource-range evidence takes priority when available.
    # MRDS remains a fallback so the pipeline is auditable while the IAEA
    # spreadsheet ingestion is developed.
    uth=col(board,"URANIUM_UTHDEPO_RESOURCE_TU")
    uth_n=col(board,"URANIUM_UTHDEPO_DEPOSITS")
    um_score=col(board,"URANIUM_MRDS_SCORE")
    um_size=col(board,"URANIUM_MRDS_SIZE_MAX")
    uranium_raw=np.where(
        uth.gt(0),
        np.log1p(uth)+0.20*np.log1p(uth_n),
        np.log1p(um_score)+0.75*um_size,
    )
    uranium_raw=pd.Series(uranium_raw,index=board.index)
    uranium_s=pct_positive(uranium_raw)

    # NITER: populated by a dedicated historical/geological evidence stage.
    niter_raw=col(board,"NITER_EVIDENCE_SCORE")
    niter_s=pct_positive(niter_raw)

    vals={
      "HORSES":(horse_raw,horse_s),
      "IRON":(iron_raw,iron_s),
      "NITER":(niter_raw,niter_s),
      "COAL":(coal_raw,coal_s),
      "OIL":(oil_raw,oil_s),
      "ALUMINUM":(alu_raw,alu_s),
      "URANIUM":(uranium_raw,uranium_s),
    }
    summary={}
    for rid,(raw,s) in vals.items():
        qmin,qmax=RANGES[rid]
        board[f"{rid}_EVIDENCE_RAW"]=pd.to_numeric(raw,errors="coerce").fillna(0)
        board[f"{rid}_STRENGTH"]=pd.to_numeric(s,errors="coerce").fillna(0).clip(0,1)
        board[f"{rid}_CANDIDATE_QTY"]=qty_from_strength(s,raw,qmin,qmax)
        q=board[f"{rid}_CANDIDATE_QTY"]
        summary[rid]={
          "qty_min":qmin,"qty_max":qmax,
          "evidence_hexes":int(q.gt(0).sum()),
          "candidate_quantity_counts":{str(int(k)):int(v) for k,v in q[q.gt(0)].value_counts().sort_index().items()},
        }
    return board,summary

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10_STRATEGIC_CANDIDATES")
    a=ap.parse_args()
    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    board,summary=build(board)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10_strategic_candidates",driver="GPKG")
    cols=["id","SURFACE"]+[f"{r}_{s}" for r in RANGES for s in ["EVIDENCE_RAW","STRENGTH","CANDIDATE_QTY"]]
    board[cols].to_csv(a.prefix+"_EVIDENCE.csv",index=False)
    meta={
      "stage":"10 strategic candidates",
      "final_placement":False,
      "gameplay_thinning_applied":False,
      "quantity_policy":"within-resource evidence percentile; never compare physical magnitudes across resource types",
      "resources":summary,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(json.dumps(meta,indent=2))

if __name__=="__main__": main()
