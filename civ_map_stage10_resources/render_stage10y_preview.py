#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("gpkg")
    ap.add_argument("--layer",default="game_map_stage10y_resource_placement_preview")
    ap.add_argument("--outdir",default="stage10y_maps")
    a=ap.parse_args()
    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)

    g=gpd.read_file(a.gpkg,layer=a.layer)
    ll=g.to_crs(4326)
    base=ll[ll.SURFACE.eq("LAND")]
    cent=ll.loc[ll.RESOURCE_PRESENT.eq(1)].copy()
    cent.geometry=cent.geometry.centroid

    for klass in ["strategic","bonus","luxury"]:
        p=cent.loc[cent.RESOURCE_CLASS.eq(klass)].copy()
        fig,ax=plt.subplots(figsize=(17,9))
        base.boundary.plot(ax=ax,linewidth=0.05)
        if len(p):
            if klass=="strategic":
                sizes=8+6*pd.to_numeric(p.RESOURCE_QTY,errors="coerce").fillna(1)
            else:
                sizes=8
            p.plot(ax=ax,markersize=sizes,alpha=0.70)
        ax.set_xlim(-180,180); ax.set_ylim(-90,90); ax.set_aspect("equal",adjustable="box")
        ax.set_title(f"Stage 10Y preview: {klass} resources")
        fig.tight_layout()
        fig.savefig(out/f"stage10y_{klass}_world.png",dpi=180)
        plt.close(fig)

    fig,ax=plt.subplots(figsize=(18,9))
    base.boundary.plot(ax=ax,linewidth=0.05)
    for klass in ["strategic","luxury","bonus"]:
        p=cent.loc[cent.RESOURCE_CLASS.eq(klass)]
        if len(p):
            p.plot(ax=ax,markersize=5,alpha=0.55,label=klass)
    ax.legend(loc="lower left")
    ax.set_xlim(-180,180); ax.set_ylim(-90,90); ax.set_aspect("equal",adjustable="box")
    ax.set_title("Stage 10Y resource placement preview")
    fig.tight_layout()
    fig.savefig(out/"stage10y_all_resources_world.png",dpi=180)
    plt.close(fig)

if __name__=="__main__":
    main()
