#!/usr/bin/env python3
"""
Stage 4A: snap Natural Earth 1:10m river centerlines to canonical 50-km hex EDGES.

The river is represented as six edge flags per hex:
  RIV_E0 upper-left
  RIV_E1 top
  RIV_E2 upper-right
  RIV_E3 lower-right
  RIV_E4 bottom
  RIV_E5 lower-left

Method
------
1. Read the final Stage 2B canonical board.
2. Build a unique edge network only from LAND/COAST/LAKE cells.
3. Densify each Natural Earth river line to 5 km.
4. For each sample, choose the nearby hex edge minimizing:
       point-to-edge distance + orientation penalty
   so the river is snapped to one game edge rather than buffered onto parallel
   edges.
5. Store each selected physical edge once, with minimum Natural Earth scalerank,
   source-name provenance, and hit count.
6. Promote rank <= --rank-cutoff to RIV_E0..RIV_E5 on every incident active
   hex. Shared physical edges therefore receive mirrored flags automatically.

No Stage 1A / 1-degree relief is used.
"""
from __future__ import annotations
import argparse, json, math
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

ACTIVE={"LAND","COAST","LAKE"}
TARGET_ANGLES=np.array([150.0,90.0,30.0,-30.0,-90.0,-150.0])
DIR_NAMES=["upper-left","top","upper-right","lower-right","bottom","lower-left"]

def edge_dir(poly):
    c=poly.centroid
    xy=np.asarray(poly.exterior.coords[:-1],dtype=float)
    out=[]
    for i in range(len(xy)):
        a=xy[i]; b=xy[(i+1)%len(xy)]
        m=(a+b)/2
        ang=math.degrees(math.atan2(m[1]-c.y,m[0]-c.x))
        # circular angular distance
        d=np.abs(((TARGET_ANGLES-ang+180)%360)-180)
        k=int(np.argmin(d))
        out.append((a,b,k))
    if len(out)!=6 or len({x[2] for x in out})!=6:
        raise RuntimeError("hex edge direction classification failed")
    return out

def key_for(a,b,prec=3):
    aa=(round(float(a[0]),prec),round(float(a[1]),prec))
    bb=(round(float(b[0]),prec),round(float(b[1]),prec))
    return (aa,bb) if aa<=bb else (bb,aa)

def parts(geom):
    if geom is None or geom.is_empty:return []
    if geom.geom_type=="LineString":return [geom]
    if geom.geom_type=="MultiLineString":return list(geom.geoms)
    return []

def sample_line(ls,spacing=5000.0):
    L=float(ls.length)
    if L<=0:return []
    ds=np.arange(0,L+spacing*0.5,spacing)
    ds=np.minimum(ds,L)
    # de-duplicate possible final repeated distance
    ds=np.unique(ds)
    pts=[]; tang=[]
    eps=min(1000.0,max(100.0,L/20))
    for d in ds:
        p=ls.interpolate(float(d))
        p0=ls.interpolate(max(0.0,float(d)-eps))
        p1=ls.interpolate(min(L,float(d)+eps))
        vx=p1.x-p0.x; vy=p1.y-p0.y
        n=math.hypot(vx,vy)
        if n==0: vx,vy=1.0,0.0
        else: vx/=n;vy/=n
        pts.append((p.x,p.y));tang.append((vx,vy))
    return np.asarray(pts,float),np.asarray(tang,float)

def point_segment_dist(px,py,ax,ay,bx,by):
    vx=bx-ax;vy=by-ay
    wx=px-ax;wy=py-ay
    den=vx*vx+vy*vy
    t=np.where(den>0,(wx*vx+wy*vy)/den,0.0)
    t=np.clip(t,0,1)
    qx=ax+t*vx;qy=ay+t*vy
    return np.hypot(px-qx,py-qy)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage2b_gpkg")
    ap.add_argument("river_shp")
    ap.add_argument("--layer",default="game_map_stage2b_biomes")
    ap.add_argument("--rank-cutoff",type=int,default=7)
    ap.add_argument("--spacing-m",type=float,default=5000)
    ap.add_argument("--max-snap-m",type=float,default=32000)
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE4A_RIVERS")
    a=ap.parse_args()

    board=gpd.read_file(a.stage2b_gpkg,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError(f"canonical board audit failed n={len(board)} unique={board.id.is_unique}")
    if board.crs.to_epsg()!=8857:board=board.to_crs(8857)
    active=board[board.SURFACE.isin(ACTIVE)].copy()
    print("board",len(board),"active",len(active),flush=True)

    # Unique physical edge network.
    edge_index={}
    edge_a=[];edge_b=[];edge_inc=[]
    for ridx,row in active.iterrows():
        hid=int(row.id)
        for aa,bb,d in edge_dir(row.geometry):
            k=key_for(aa,bb)
            ei=edge_index.get(k)
            if ei is None:
                ei=len(edge_a);edge_index[k]=ei
                edge_a.append(aa);edge_b.append(bb);edge_inc.append([])
            edge_inc[ei].append((ridx,hid,d))
    A=np.asarray(edge_a,float);B=np.asarray(edge_b,float)
    M=(A+B)/2
    V=B-A
    VL=np.hypot(V[:,0],V[:,1]); U=V/VL[:,None]
    tree=cKDTree(M)
    print("unique active edges",len(A),flush=True)

    rivers=gpd.read_file(a.river_shp)
    rivers=rivers[rivers.featurecla.eq("River")].copy()
    rivers=rivers[pd.to_numeric(rivers.scalerank,errors="coerce").fillna(99)<=8].copy()
    rivers=rivers.to_crs(8857)
    print("source permanent rivers rank<=8",len(rivers),flush=True)

    hit=np.zeros(len(A),dtype=np.int32)
    minrank=np.full(len(A),99,dtype=np.int16)
    names=defaultdict(set)
    far_samples=0; total_samples=0
    by_source=[]

    for ri,row in rivers.iterrows():
        rank=int(row.scalerank)
        nm=str(row.get("name_en") or row.get("name") or "")
        src_edges=set();src_samples=0
        for ls in parts(row.geometry):
            sampled=sample_line(ls,a.spacing_m)
            if len(sampled)==0:continue
            P,T=sampled;src_samples+=len(P);total_samples+=len(P)
            kq=min(12,len(A))
            dmid,idx=tree.query(P,k=kq)
            if kq==1:
                idx=idx[:,None]
            for j,p in enumerate(P):
                cand=np.atleast_1d(idx[j]).astype(int)
                ax=A[cand,0];ay=A[cand,1];bx=B[cand,0];by=B[cand,1]
                dist=point_segment_dist(p[0],p[1],ax,ay,bx,by)
                # unsigned line-orientation difference. Parallel/opposite are equivalent.
                dot=np.abs(U[cand,0]*T[j,0]+U[cand,1]*T[j,1])
                dot=np.clip(dot,0,1)
                # 8 km penalty at 90-degree mismatch.
                score=dist+8000.0*(1-dot)
                z=int(np.argmin(score));ei=int(cand[z]);dd=float(dist[z])
                if dd>a.max_snap_m:
                    far_samples+=1
                    continue
                hit[ei]+=1
                if rank<minrank[ei]:minrank[ei]=rank
                if nm:names[ei].add(nm)
                src_edges.add(ei)
        by_source.append({"name":nm,"scalerank":rank,"samples":src_samples,"snapped_edges":len(src_edges)})

    selected=np.where(hit>0)[0]
    print("samples",total_samples,"far",far_samples,"selected edges all rank<=8",len(selected),flush=True)

    # Build edge table.
    erows=[]
    egeoms=[]
    for ei in selected:
        inc=edge_inc[ei]
        erows.append({
            "EDGE_ID":int(ei),
            "SCALERANK":int(minrank[ei]),
            "HIT_COUNT":int(hit[ei]),
            "N_INCIDENT":len(inc),
            "CELL_IDS":";".join(str(x[1]) for x in inc),
            "CELL_DIRS":";".join(f"E{x[2]}" for x in inc),
            "RIVER_NAMES":"; ".join(sorted(names.get(ei,set())))[:1000],
        })
        egeoms.append(LineString([tuple(A[ei]),tuple(B[ei])]))
    eg=gpd.GeoDataFrame(erows,geometry=egeoms,crs=8857)

    # Threshold scan is free once all rank<=8 edges are snapped.
    scans=[]
    for cut in [4,5,6,7,8]:
        m=eg.SCALERANK<=cut
        eids=set(eg.loc[m,"EDGE_ID"].astype(int))
        cells=set()
        shared=0
        for ei in eids:
            inc=edge_inc[ei]
            cells.update(x[1] for x in inc)
            if len(inc)==2:shared+=1
        scans.append({"rank_cutoff":cut,"river_edges":len(eids),"active_cells_touched":len(cells),"shared_edges":shared})
    scan=pd.DataFrame(scans)
    scan.to_csv(a.prefix+"_RANK_SCAN.csv",index=False)
    print(scan.to_string(index=False),flush=True)

    use=set(eg.loc[eg.SCALERANK<=a.rank_cutoff,"EDGE_ID"].astype(int))
    for d in range(6):board[f"RIV_E{d}"]=np.uint8(0)
    board["RIVER_ANY"]=np.uint8(0)
    board["RIVER_MINR"]=pd.Series([pd.NA]*len(board),dtype="Int16")
    cell_min={}
    symmetry_bad=0
    for ei in use:
        inc=edge_inc[ei]
        for ridx,hid,d in inc:
            board.at[ridx,f"RIV_E{d}"]=1
            board.at[ridx,"RIVER_ANY"]=1
            cell_min[ridx]=min(cell_min.get(ridx,99),int(minrank[ei]))
        if len(inc)==2:
            # both incident cells were just flagged by construction
            if not all(int(board.at[x[0],f"RIV_E{x[2]}"])==1 for x in inc):
                symmetry_bad+=1
    for ridx,r in cell_min.items():board.at[ridx,"RIVER_MINR"]=r

    # Named-river audit, based on edge provenance.
    qa_names=["Amazon","Nile","Mississippi","Yangtze","Huang","Ganges","Brahmaputra",
              "Mekong","Congo","Niger","Danube","Rhine","Indus","Paraná","Volga"]
    qa=[]
    for q in qa_names:
        m=eg.RIVER_NAMES.str.contains(q,case=False,na=False)&(eg.SCALERANK<=a.rank_cutoff)
        qa.append({"river":q,"edges":int(m.sum()),"pass":bool(m.sum()>0)})
    qa=pd.DataFrame(qa)
    qa.to_csv(a.prefix+"_NAMED_QA.csv",index=False)

    surf_bad=int(board.loc[board.SURFACE.isin(["OCEAN","VOID"]),"RIVER_ANY"].sum())
    summary={
      "stage":"4A",
      "source":"Natural Earth 1:10m rivers_lake_centerlines",
      "source_filter":"featurecla == River; scalerank <= 8 snapped, cutoff applied afterward",
      "rank_cutoff":a.rank_cutoff,
      "sample_spacing_m":a.spacing_m,
      "max_snap_m":a.max_snap_m,
      "source_features":int(len(rivers)),
      "source_samples":int(total_samples),
      "samples_beyond_snap_tolerance":int(far_samples),
      "selected_physical_edges":int(len(use)),
      "river_flagged_cells":int(board.RIVER_ANY.sum()),
      "shared_edge_symmetry_failures":int(symmetry_bad),
      "ocean_void_river_flags":surf_bad,
      "named_QA_pass":int(qa["pass"].sum()),
      "named_QA_total":int(len(qa)),
      "edge_convention":{f"RIV_E{i}":DIR_NAMES[i] for i in range(6)},
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2),flush=True)
    print(qa.to_string(index=False),flush=True)

    out=a.prefix+".gpkg"
    board.to_file(out,layer="game_map_stage4a_rivers",driver="GPKG")
    eg.to_file(out,layer="river_edges_stage4a",driver="GPKG")

    # Preview only the physical snapped edges.
    fig,ax=plt.subplots(figsize=(18,9))
    board.loc[board.SURFACE.isin(["LAND","COAST","LAKE"])].boundary.plot(ax=ax,linewidth=0.03)
    eg.loc[eg.SCALERANK<=a.rank_cutoff].plot(ax=ax,linewidth=0.35)
    ax.set_axis_off();ax.set_title(f"Stage 4A river-edge snap — Natural Earth 10m, scalerank <= {a.rank_cutoff}")
    fig.tight_layout();fig.savefig(a.prefix+"_WORLD_PREVIEW.png",dpi=180,bbox_inches="tight");plt.close(fig)

    # Compact edge CSV.
    eg.drop(columns="geometry").to_csv(a.prefix+"_EDGES.csv",index=False)
    pd.DataFrame(by_source).to_csv(a.prefix+"_SOURCE_AUDIT.csv",index=False)

if __name__=="__main__":main()
