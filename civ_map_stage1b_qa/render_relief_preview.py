#!/usr/bin/env python3
import argparse, math
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

ROWS=335
HEX_W=57735.0269189626
HEX_H=50000.0
X_STEP=43301.27018922195
BASE_LEFT=-16920565.0448
BASE_TOP=8315130.3484

def hex_polygon_xy(col,row):
    left=BASE_LEFT+col*X_STEP
    top=BASE_TOP-row*HEX_H-(col%2)*(HEX_H/2.0)
    right=left+HEX_W
    bottom=top-HEX_H
    cy=(top+bottom)/2.0
    qx=HEX_W/4.0
    return Polygon([(left,cy),(left+qx,top),(right-qx,top),(right,cy),
                    (right-qx,bottom),(left+qx,bottom),(left,cy)])

def make_gdf(df):
    if "row_index" not in df.columns or "col_index" not in df.columns:
        ids=df["id"].astype("int64")
        df=df.copy()
        df["col_index"]=(ids-1)//ROWS
        df["row_index"]=(ids-1)%ROWS
    geoms=[hex_polygon_xy(int(c),int(r)) for c,r in zip(df.col_index,df.row_index)]
    return gpd.GeoDataFrame(df.copy(),geometry=geoms,crs="EPSG:8857")

def draw(gdf,out,title,world=False):
    fig,ax=plt.subplots(figsize=(18,10) if world else (9,15),dpi=180)
    palette={"FLAT":"#d8c98a","HILL":"#b7894d","MOUNTAIN":"#6d6d6d"}
    for k in ["FLAT","HILL","MOUNTAIN"]:
        sub=gdf[gdf["RELIEF"]==k]
        if len(sub):
            sub.plot(ax=ax,color=palette[k],edgecolor="#f4f0df",linewidth=0.10)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title,fontsize=13)
    plt.tight_layout()
    fig.savefig(out,bbox_inches="tight")
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("classified")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE1B_RELIEF_HIGHRES")
    a=ap.parse_args()
    df=pd.read_csv(a.classified)
    if len(df)!=68048:
        raise SystemExit(f"Expected 68048 LAND hexes, got {len(df)}")
    if not df["id"].is_unique:
        raise SystemExit("Duplicate canonical IDs")
    g=make_gdf(df)
    g.to_file(a.prefix+"_LAND.gpkg",layer="stage1b_land_relief",driver="GPKG")
    draw(g,a.prefix+"_WORLD_PREVIEW.png",
         "Civilization-style GAME MAP — Stage 1B ETOPO2022 60-second relief (LAND)")
    w=g.to_crs("EPSG:4326")
    sa=w.cx[-85:-30,-60:15].to_crs("EPSG:8857")
    draw(sa,a.prefix+"_SOUTH_AMERICA_PREVIEW.png",
         "Stage 1B relief QA — South America")
    andes=w.cx[-82:-64,-56:12].to_crs("EPSG:8857")
    draw(andes,a.prefix+"_ANDES_PREVIEW.png",
         "Stage 1B relief QA — Andes / Peru / Chile")
    counts=df["RELIEF"].value_counts().rename_axis("RELIEF").reset_index(name="COUNT")
    counts["PERCENT"]=counts["COUNT"]/len(df)*100
    counts.to_csv(a.prefix+"_SUMMARY.csv",index=False)

if __name__=="__main__":
    main()
