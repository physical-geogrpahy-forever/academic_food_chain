#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

RESOURCES = [
    ("HORSES","Horses"),
    ("IRON","Iron"),
    ("OIL","Oil"),
    ("ALUMINUM","Aluminum"),
    ("URANIUM","Uranium"),
    ("COAL","Coal"),
    ("NITER","Niter"),
]

def world_base(ax, board_ll):
    land=board_ll[board_ll["SURFACE"].eq("LAND")]
    coast=board_ll[board_ll["SURFACE"].eq("COAST")]
    land.boundary.plot(ax=ax, linewidth=0.05)
    if len(coast):
        coast.boundary.plot(ax=ax, linewidth=0.04)
    ax.set_xlim(-180,180)
    ax.set_ylim(-90,90)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("gpkg")
    ap.add_argument("--outdir",default="strategic_maps")
    a=ap.parse_args()
    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)

    g=gpd.read_file(a.gpkg)
    ll=g.to_crs(4326)
    cent=g.geometry.centroid
    pts=gpd.GeoDataFrame(g.drop(columns="geometry"),geometry=cent,crs=g.crs).to_crs(4326)

    summaries=[]
    available=[]
    for rid,label in RESOURCES:
        qcol=f"{rid}_CANDIDATE_QTY"
        if qcol not in pts.columns:
            continue
        q=pd.to_numeric(pts[qcol],errors="coerce").fillna(0)
        n=int((q>0).sum())
        if n==0:
            summaries.append({"resource":rid,"candidate_hexes":0,"total_units":0,"max_qty":0})
            continue
        available.append((rid,label))
        summaries.append({
            "resource":rid,
            "candidate_hexes":n,
            "total_units":int(q[q>0].sum()),
            "max_qty":int(q.max()),
        })
        fig,ax=plt.subplots(figsize=(16,8))
        world_base(ax,ll)
        p=pts.loc[q>0]
        sizes=4 + 8*pd.to_numeric(p[qcol],errors="coerce").fillna(0)
        p.plot(ax=ax,markersize=sizes,alpha=0.72)
        ax.set_title(f"{label} strategic-resource candidate quantity | 50 km hex")
        fig.tight_layout()
        fig.savefig(out/f"{rid.lower()}_candidate_qty_world.png",dpi=180)
        plt.close(fig)

    pd.DataFrame(summaries).to_csv(out/"strategic_candidate_map_summary.csv",index=False)

    # Combined review map for currently available resources.
    if available:
        fig,ax=plt.subplots(figsize=(17,9))
        world_base(ax,ll)
        for rid,label in available:
            qcol=f"{rid}_CANDIDATE_QTY"
            q=pd.to_numeric(pts[qcol],errors="coerce").fillna(0)
            p=pts.loc[q>0]
            if len(p):
                sizes=2 + 4*pd.to_numeric(p[qcol],errors="coerce").fillna(0)
                p.plot(ax=ax,markersize=sizes,alpha=0.58,label=label)
        ax.legend(loc="lower left",ncol=3,fontsize=8)
        ax.set_title("Strategic-resource candidate review | marker size = candidate quantity")
        fig.tight_layout()
        fig.savefig(out/"strategic_candidates_combined_world.png",dpi=180)
        plt.close(fig)

if __name__=="__main__":
    main()
