#!/usr/bin/env python3
"""
Stage 8A Oasis candidates from Hernández-Agüero et al. (2025) PeerJ global oasis
prediction vector (Supplemental Information 9, 1-km vector map).

No random oasis seeds are used. Oasis is treated as a Desert-land feature
candidate only when the published oasis polygon overlaps the canonical hex.
"""
from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
import pandas as pd
import geopandas as gpd

QA=[
 ("Tarim Basin",75,90,36,43),
 ("Turpan-Hami",87,96,39,44),
 ("Hexi Corridor",94,103,37,42),
 ("Central Asian oases",55,75,35,45),
 ("Iranian oases",48,61,27,36),
 ("Sahara oases",-10,30,20,32),
 ("Arabian oases",35,58,16,30),
]
NEG=[
 ("Empty Sahara sector",5,20,24,30),
 ("Rub al Khali interior",45,55,18,25),
]

def discover_vector(root:Path):
    exts=[".gpkg",".shp",".geojson",".json"]
    files=[]
    for e in exts: files.extend(root.rglob("*"+e))
    if not files: raise RuntimeError("no vector file found in oasis supplement")
    # Prefer the largest plausible map file.
    files=sorted(files,key=lambda p:p.stat().st_size,reverse=True)
    return files[0]

def box(df,b):
    _,x0,x1,y0,y1=b
    return (df.LON>=x0)&(df.LON<=x1)&(df.LAT>=y0)&(df.LAT<=y1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage7_gpkg")
    ap.add_argument("oasis_zip")
    ap.add_argument("--layer",default="game_map_stage7a_seaice")
    ap.add_argument("--work",default="stage8a_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE8A_OASIS")
    a=ap.parse_args()
    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.oasis_zip) as z:z.extractall(work/"oasis")
    src=discover_vector(work/"oasis")
    print("oasis source",src,src.stat().st_size,flush=True)

    board=gpd.read_file(a.stage7_gpkg,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    if board.crs.to_epsg()!=8857: board=board.to_crs(8857)

    oasis=gpd.read_file(src)
    if oasis.crs is None: raise RuntimeError("oasis vector CRS missing")
    oasis=oasis[oasis.geometry.notna() & ~oasis.geometry.is_empty].copy()
    oasis=oasis.to_crs(8857)
    oasis=oasis.explode(index_parts=False,ignore_index=True)
    oasis=oasis[oasis.geom_type.isin(["Polygon","MultiPolygon"])].copy()
    if len(oasis)==0: raise RuntimeError("no polygon oasis features")

    desert=board[(board.SURFACE=="LAND")&(board.TERRAIN=="DESERT")][["id","LON","LAT","geometry"]].copy()
    pairs=gpd.sjoin(desert,oasis[["geometry"]],predicate="intersects",how="inner")
    rows=[]
    for ridx,grp in pairs.groupby(level=0):
        h=desert.loc[ridx].geometry
        # Avoid double counting overlapping source polygons.
        geoms=[oasis.loc[i].geometry for i in grp.index_right.unique()]
        u=gpd.GeoSeries(geoms,crs=8857).union_all()
        inter=h.intersection(u)
        area=float(inter.area)
        rows.append({"id":int(desert.loc[ridx,"id"]),
                     "OASIS_AREA_KM2":area/1e6,
                     "OASIS_FRAC":area/float(h.area) if h.area>0 else 0})
    m=pd.DataFrame(rows)
    board=board.merge(m,on="id",how="left",validate="one_to_one")
    board["OASIS_AREA_KM2"]=board["OASIS_AREA_KM2"].fillna(0.0)
    board["OASIS_FRAC"]=board["OASIS_FRAC"].fillna(0.0)

    thresholds=[0.0025,0.005,0.01,0.02,0.05,0.10]
    scans=[]; detail=[]
    for t in thresholds:
        cand=(board.OASIS_FRAC>=t)&board.SURFACE.eq("LAND")&board.TERRAIN.eq("DESERT")
        pos=[]
        for b in QA:
            q=box(board,b); n=int(q.sum()); nc=int((cand&q).sum())
            pos.append(1 if nc>0 else 0)
            detail.append({"threshold":t,"region":b[0],"kind":"positive","n":n,"candidate_hexes":nc})
        neg=[]
        for b in NEG:
            q=box(board,b);n=int(q.sum());nc=int((cand&q).sum());sh=nc/n if n else 0
            neg.append(max(0,1-sh/0.05))
            detail.append({"threshold":t,"region":b[0],"kind":"negative","n":n,"candidate_hexes":nc})
        ncan=int(cand.sum())
        # Keep a representative but non-random set.
        balance=1.0 if 50<=ncan<=1500 else max(0,1-abs(ncan-500)/2000)
        score=3*sum(pos)/len(pos)+1.5*sum(neg)/len(neg)+0.5*balance
        scans.append({"threshold":t,"oasis_hexes":ncan,"positive_score":sum(pos)/len(pos),
                      "negative_score":sum(neg)/len(neg),"balance":balance,"total_score":score})
    scan=pd.DataFrame(scans).sort_values(["total_score","threshold"],ascending=[False,False])
    best=float(scan.iloc[0].threshold)
    board["OASIS"]=((board.OASIS_FRAC>=best)&board.SURFACE.eq("LAND")&board.TERRAIN.eq("DESERT")).astype("uint8")

    d=pd.DataFrame(detail);chosen=d[d.threshold.eq(best)]
    failures=[]
    for r in chosen.itertuples():
        if r.kind=="positive" and r.candidate_hexes==0:failures.append(r.region+": no oasis candidate")
    non_des=int(board.loc[board.OASIS.eq(1)&~board.TERRAIN.eq("DESERT")].shape[0])
    nonland=int(board.loc[board.OASIS.eq(1)&~board.SURFACE.eq("LAND")].shape[0])
    if non_des:failures.append(f"non-desert oasis {non_des}")
    if nonland:failures.append(f"non-land oasis {nonland}")

    summary={"stage":"8A","source":"PeerJ 2025 global oasis prediction, Supplemental Information 9",
             "source_vector":str(src),"source_features":int(len(oasis)),
             "threshold_frac":best,"oasis_hexes":int(board.OASIS.sum()),
             "qa_gate":"PASS" if not failures else "REVIEW","qa_failures":failures,
             "rule":"published oasis polygon overlap >= threshold AND canonical LAND AND DESERT terrain",
             "random_seeds_used":False,"Stage1A_1deg_used":False}
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    scan.to_csv(a.prefix+"_THRESHOLD_SCAN.csv",index=False)
    chosen.to_csv(a.prefix+"_QA.csv",index=False)
    board.loc[board.OASIS.eq(1),["id","LON","LAT","OASIS_AREA_KM2","OASIS_FRAC"]].to_csv(a.prefix+"_CANDIDATES.csv",index=False)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage8a_oasis",driver="GPKG")
    print(json.dumps(summary,indent=2))
    print(scan.to_string(index=False))
    print(chosen.to_string(index=False))

if __name__=="__main__":main()
