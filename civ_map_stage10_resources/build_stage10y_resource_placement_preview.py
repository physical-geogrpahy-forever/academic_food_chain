#!/usr/bin/env python3
"""
Stage 10Y PREVIEW: deterministic evidence-ranked placement of all 47 resources.

This is intentionally a review build, not the canonical final map.

Key rules:
- target counts are allocated within each class from sqrt(evidence hex count)
- strategic > luxury > bonus conflict priority
- scarce resources are placed before widespread resources within each class
- one resource type per hex
- same-resource minimum spacing, adaptively relaxed only to the configured floor
- no random numbers
- strategic quantity preserves the selected hex *_CANDIDATE_QTY
- bonus/luxury quantity = 1
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import yaml

STRATEGIC=["HORSES","IRON","NITER","COAL","OIL","ALUMINUM","URANIUM"]
BONUS=["BANANAS","BISON","CATTLE","DEER","FISH","SHEEP","STONE","WHEAT","MAIZE","RICE"]
LUXURY=[
 "CITRUS","COCOA","COPPER","COTTON","CRAB","DYES","FURS","GEMS","GOLD",
 "INCENSE","IVORY","MARBLE","PEARLS","SALT","SILK","SILVER","SPICES","SUGAR",
 "TRUFFLES","WHALES","WINE","COFFEE","TEA","TOBACCO","OLIVES","PERFUME",
 "AMBER","JADE","LAPIS_LAZULI","CORAL"
]
CLASSES={"strategic":STRATEGIC,"bonus":BONUS,"luxury":LUXURY}

def stable_tie(ids):
    a=pd.to_numeric(ids,errors="raise").astype("int64").to_numpy()
    return ((a * 1103515245 + 12345) & 0x7fffffff).astype(np.int64)

def allocate_targets(evidence_counts,total,min_per,max_per):
    ids=list(evidence_counts)
    caps={r:min(int(max_per),int(evidence_counts[r])) for r in ids}
    alloc={r:min(int(min_per),caps[r]) for r in ids}
    total=min(int(total),sum(caps.values()))
    rem=total-sum(alloc.values())
    weights={r:math.sqrt(max(1,evidence_counts[r])) for r in ids}

    while rem>0:
        active=[r for r in ids if alloc[r]<caps[r]]
        if not active: break
        sw=sum(weights[r] for r in active)
        ideal={r:rem*weights[r]/sw for r in active}
        adds={}
        for r in active:
            room=caps[r]-alloc[r]
            adds[r]=min(room,int(math.floor(ideal[r])))
        n=sum(adds.values())
        if n==0:
            # deterministic largest remainder, then resource id
            r=max(active,key=lambda x:(ideal[x]-math.floor(ideal[x]),weights[x],x))
            adds[r]=1; n=1
        for r,v in adds.items():
            if v:
                alloc[r]+=v
        rem-=n
    return alloc,total

def allowed_surfaces(cfg,rid):
    rules=cfg.get("surface_rules",{})
    if rid in rules and isinstance(rules[rid],list):
        return set(rules[rid])
    return {"LAND"}

def fields_for(rid):
    if rid in STRATEGIC:
        return f"{rid}_STRENGTH",f"{rid}_EVIDENCE_RAW",f"{rid}_CANDIDATE_QTY"
    return f"{rid}_FINAL_STRENGTH",f"{rid}_FINAL_EVIDENCE_RAW",None

def make_candidates(board,rid,cfg):
    scol,rcol,qcol=fields_for(rid)
    for c in [scol,rcol]+([qcol] if qcol else []):
        if c not in board.columns:
            raise RuntimeError(f"{rid}: missing {c}")
    surfaces=allowed_surfaces(cfg,rid)
    s=pd.to_numeric(board[scol],errors="coerce").fillna(0)
    mask=s.gt(0) & board.SURFACE.isin(surfaces)
    x=board.loc[mask,["id","SURFACE","geometry",scol,rcol]+([qcol] if qcol else [])].copy()
    x["STRENGTH"]=pd.to_numeric(x[scol],errors="coerce").fillna(0)
    x["RAW"]=pd.to_numeric(x[rcol],errors="coerce").fillna(0)
    x["QTY"]=pd.to_numeric(x[qcol],errors="coerce").fillna(0).astype(int) if qcol else 1
    cent=x.geometry.centroid
    x["X"]=cent.x
    x["Y"]=cent.y
    x["TIE"]=stable_tie(x.id)
    x=x.sort_values(["STRENGTH","RAW","TIE","id"],ascending=[False,False,True,True])
    return x

def spaced_select(cand,target,spacing_km,occupied,floor_km,relax_factor):
    if target<=0 or cand.empty:
        return [],float(spacing_km)
    spacing=max(float(spacing_km),float(floor_km))
    last=[]
    used_spacing=spacing

    while True:
        cell=max(spacing*1000.0,1.0)
        buckets={}
        selected=[]
        d2=cell*cell

        for row in cand.itertuples(index=False):
            hid=int(row.id)
            if hid in occupied: continue
            x=float(row.X); y=float(row.Y)
            bx=int(math.floor(x/cell)); by=int(math.floor(y/cell))
            ok=True
            for ix in range(bx-1,bx+2):
                for iy in range(by-1,by+2):
                    for sx,sy in buckets.get((ix,iy),()):
                        if (x-sx)*(x-sx)+(y-sy)*(y-sy) < d2:
                            ok=False; break
                    if not ok: break
                if not ok: break
            if not ok: continue
            selected.append(hid)
            buckets.setdefault((bx,by),[]).append((x,y))
            if len(selected)>=target: break

        last=selected
        used_spacing=spacing
        if len(selected)>=target or spacing<=floor_km+1e-9:
            break
        new_spacing=max(float(floor_km),spacing*float(relax_factor))
        if abs(new_spacing-spacing)<1e-9: break
        spacing=new_spacing

    return last,used_spacing

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("config")
    ap.add_argument("--layer",default=None)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW")
    a=ap.parse_args()

    cfg=yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    board=gpd.read_file(a.board,layer=a.layer) if a.layer else gpd.read_file(a.board)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    if board.crs is None:
        raise RuntimeError("board CRS missing")

    candidates={}
    evidence_counts={}
    for klass,resources in CLASSES.items():
        for rid in resources:
            x=make_candidates(board,rid,cfg)
            if x.empty:
                raise RuntimeError(f"{rid}: no positive candidate evidence")
            candidates[rid]=x
            evidence_counts[rid]=len(x)

    targets={}
    target_audit={}
    ccfg=cfg["class_targets"]
    acfg=cfg["allocation"]
    for klass,resources in CLASSES.items():
        ec={r:evidence_counts[r] for r in resources}
        al,total=allocate_targets(
            ec,ccfg[klass],
            acfg["class_minimum_per_resource"][klass],
            acfg["class_maximum_per_resource"][klass],
        )
        targets.update(al)
        target_audit[klass]={"requested_total":int(ccfg[klass]),"capacity_limited_total":int(total),"allocated_total":int(sum(al.values()))}

    priority=cfg["conflict_resolution"]["class_priority"]
    placement_order=[]
    for klass in priority:
        rs=CLASSES[klass]
        # scarce first = evidence count per target ascending
        rs=sorted(rs,key=lambda r:(evidence_counts[r]/max(1,targets[r]),r))
        placement_order.extend((klass,r) for r in rs)

    occupied=set()
    selected_rows=[]
    placement_audit=[]
    scfg=cfg["spacing_km"]
    overrides=scfg.get("overrides",{})
    floor=float(scfg["adaptive_floor_km"])
    relax=float(scfg["relaxation_factor"])

    for klass,rid in placement_order:
        base=float(overrides.get(rid,scfg[f"{klass}_default"]))
        ids,used=spaced_select(
            candidates[rid],targets[rid],base,occupied,floor,relax
        )
        idset=set(ids)
        chosen=candidates[rid].loc[candidates[rid].id.isin(idset)].copy()
        # Restore resource evidence ranking in output.
        chosen=chosen.sort_values(["STRENGTH","RAW","TIE","id"],ascending=[False,False,True,True])
        for row in chosen.itertuples(index=False):
            selected_rows.append({
              "id":int(row.id),
              "RESOURCE_ID":rid,
              "RESOURCE_CLASS":klass,
              "RESOURCE_QTY":int(row.QTY) if klass=="strategic" else 1,
              "RESOURCE_STRENGTH":float(row.STRENGTH),
              "RESOURCE_EVIDENCE_RAW":float(row.RAW),
            })
        occupied.update(idset)
        placement_audit.append({
          "resource":rid,"class":klass,
          "evidence_hexes":int(evidence_counts[rid]),
          "target":int(targets[rid]),
          "placed":int(len(ids)),
          "shortfall":int(targets[rid]-len(ids)),
          "configured_spacing_km":base,
          "used_spacing_km":float(used),
          "candidate_to_target_ratio":float(evidence_counts[rid]/max(1,targets[rid])),
        })

    sel=pd.DataFrame(selected_rows)
    if sel.id.duplicated().any():
        raise RuntimeError("one-resource-per-hex audit failed")

    out=board.copy()
    for c in ["RESOURCE_ID","RESOURCE_CLASS"]:
        out[c]=""
    out["RESOURCE_QTY"]=0
    out["RESOURCE_STRENGTH"]=0.0
    out["RESOURCE_EVIDENCE_RAW"]=0.0

    if len(sel):
        sm=sel.set_index("id")
        idx=out.id.isin(sm.index)
        ids=out.loc[idx,"id"]
        out.loc[idx,"RESOURCE_ID"]=ids.map(sm.RESOURCE_ID).to_numpy()
        out.loc[idx,"RESOURCE_CLASS"]=ids.map(sm.RESOURCE_CLASS).to_numpy()
        out.loc[idx,"RESOURCE_QTY"]=ids.map(sm.RESOURCE_QTY).to_numpy()
        out.loc[idx,"RESOURCE_STRENGTH"]=ids.map(sm.RESOURCE_STRENGTH).to_numpy()
        out.loc[idx,"RESOURCE_EVIDENCE_RAW"]=ids.map(sm.RESOURCE_EVIDENCE_RAW).to_numpy()

    out["RESOURCE_PRESENT"]=(out.RESOURCE_ID!="").astype("uint8")
    out.to_file(a.prefix+".gpkg",layer="game_map_stage10y_resource_placement_preview",driver="GPKG")
    sel.sort_values(["RESOURCE_CLASS","RESOURCE_ID","RESOURCE_STRENGTH"],ascending=[True,True,False]).to_csv(
        a.prefix+"_PLACED.csv",index=False
    )
    adf=pd.DataFrame(placement_audit)
    adf.to_csv(a.prefix+"_AUDIT.csv",index=False)

    class_actual=adf.groupby("class")["placed"].sum().to_dict()
    strategic_units=sel.loc[sel.RESOURCE_CLASS.eq("strategic")].groupby("RESOURCE_ID").RESOURCE_QTY.sum().to_dict()
    summary={
      "stage":"10Y PREVIEW",
      "status":"preview_not_final",
      "resource_count":47,
      "selected_resource_hexes":int(len(sel)),
      "selected_fraction_of_all_hexes":float(len(sel)/len(out)),
      "class_target_audit":target_audit,
      "class_actual_counts":{k:int(v) for k,v in class_actual.items()},
      "one_resource_per_hex":bool(not sel.id.duplicated().any()),
      "strategic_total_units":{k:int(v) for k,v in strategic_units.items()},
      "placement_order":[r for _,r in placement_order],
      "allocation_method":"sqrt positive evidence count within class, bounded by class min/max",
      "selection_method":"evidence rank + deterministic tie key + adaptive same-resource spacing",
      "random_numbers_used":False,
      "final_map":False,
      "audit":placement_audit,
      "Stage1A_1deg_used":False,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
