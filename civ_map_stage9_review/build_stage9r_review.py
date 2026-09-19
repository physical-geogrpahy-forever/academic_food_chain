#!/usr/bin/env python3
"""
Stage 9R review package: terrain, relief, biome/vegetation only.

Purpose:
  Give the user a visual QA checkpoint BEFORE any resource design/placement.
  No Stage 10 resource fields are used.

Outputs:
  - world terrain map
  - world relief map
  - world combined terrain+relief+vegetation map
  - regional combined previews
  - regional class-count CSV
  - schema and summary JSON
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon

TERRAIN_COLORS={
    "GRASSLAND":"#8fbf67",
    "PLAINS":"#d4bd7a",
    "DESERT":"#e6cf83",
    "TUNDRA":"#b9b4a5",
    "SNOW":"#f4f5f6",
}
WATER_COLORS={
    "OCEAN":"#4d86b8",
    "COAST":"#76acd0",
    "LAKE":"#699cc4",
    "VOID":"#d8d8d8",
}
RELIEF_COLORS={
    "FLAT":"#e7e7e7",
    "HILL":"#a5a5a5",
    "MOUNTAIN":"#474747",
}
FEATURE_COLORS={
    "FOREST":"#2f6f3e",
    "JUNGLE":"#195a2d",
}
REGIONS=[
    ("World",-180,180,-90,90),
    ("Andes",-82,-63,-56,13),
    ("Himalaya_Tibet",65,105,20,45),
    ("Korea_Japan",123,147,30,47),
    ("Europe",-12,40,34,72),
    ("North_America",-170,-50,10,75),
    ("Africa",-20,55,-37,38),
    ("Australia",110,155,-46,-8),
]

def darken(hexcolor, factor):
    h=hexcolor.lstrip("#")
    rgb=np.array([int(h[i:i+2],16) for i in (0,2,4)],dtype=float)
    rgb=np.clip(rgb*factor,0,255).astype(int)
    return "#%02x%02x%02x"%tuple(rgb)

def color_combined(row):
    surf=row["SURFACE"]
    if surf!="LAND":
        return WATER_COLORS.get(surf,"#d8d8d8")
    base=TERRAIN_COLORS.get(row["TERRAIN"],"#cccccc")
    rel=row["RELIEF"]
    if rel=="HILL": base=darken(base,0.78)
    elif rel=="MOUNTAIN": base=darken(base,0.48)
    feat=row.get("FEATURE_GAME","NONE")
    if feat=="FOREST": base="#366f42" if rel!="MOUNTAIN" else "#294d30"
    elif feat=="JUNGLE": base="#176230" if rel!="MOUNTAIN" else "#124522"
    return base

def plot_polys(gdf, color_series, out, title, bounds=None, dpi=220):
    fig,ax=plt.subplots(figsize=(16,8.5))
    # GeoPandas polygon plotting is reliable here; rasterized output keeps file size sane.
    gdf.plot(ax=ax,color=color_series,linewidth=0,rasterized=True)
    if bounds:
        x0,x1,y0,y1=bounds
        ax.set_xlim(x0,x1); ax.set_ylim(y0,y1)
    ax.set_axis_off()
    ax.set_title(title,fontsize=15,pad=10)
    fig.tight_layout(pad=0.2)
    fig.savefig(out,dpi=dpi,bbox_inches="tight",facecolor="white")
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("gpkg")
    ap.add_argument("--layer",default="game_map_stage9a_consolidated")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE9R_REVIEW")
    args=ap.parse_args()

    g=gpd.read_file(args.gpkg,layer=args.layer)
    if len(g)!=261635 or not g.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    required=["SURFACE","RELIEF","TERRAIN","FEATURE_GAME"]
    missing=[c for c in required if c not in g.columns]
    if missing: raise RuntimeError(f"missing review fields {missing}")

    # Use geographic coordinates so regional boxes are intuitive.
    gg=g.to_crs(4326)
    # Exclude VOID from most display layers except to preserve world silhouette context.
    display=gg.copy()

    terrain_color=[]
    relief_color=[]
    combined_color=[]
    for _,r in display.iterrows():
        s=r.SURFACE
        if s=="LAND":
            terrain_color.append(TERRAIN_COLORS.get(r.TERRAIN,"#cccccc"))
            relief_color.append(RELIEF_COLORS.get(r.RELIEF,"#cccccc"))
        else:
            terrain_color.append(WATER_COLORS.get(s,"#d8d8d8"))
            relief_color.append(WATER_COLORS.get(s,"#d8d8d8"))
        combined_color.append(color_combined(r))

    plot_polys(display,terrain_color,args.prefix+"_WORLD_TERRAIN.png",
               "Stage 9R: Base terrain / biome classes")
    plot_polys(display,relief_color,args.prefix+"_WORLD_RELIEF.png",
               "Stage 9R: Relief classes")
    plot_polys(display,combined_color,args.prefix+"_WORLD_COMBINED.png",
               "Stage 9R: Terrain + relief + forest/jungle")

    rows=[]
    for name,x0,x1,y0,y1 in REGIONS:
        m=(display.LON>=x0)&(display.LON<=x1)&(display.LAT>=y0)&(display.LAT<=y1)
        sub=display.loc[m].copy()
        if name!="World":
            cols=[color_combined(r) for _,r in sub.iterrows()]
            plot_polys(sub,cols,args.prefix+f"_{name}.png",
                       f"Stage 9R: {name} terrain + relief + vegetation",
                       bounds=(x0,x1,y0,y1),dpi=240)
        land=sub[sub.SURFACE.eq("LAND")]
        rec={"region":name,"all_hexes":int(len(sub)),"land_hexes":int(len(land))}
        for c in ["FLAT","HILL","MOUNTAIN"]:
            rec["RELIEF_"+c]=int(land.RELIEF.eq(c).sum())
        for c in ["GRASSLAND","PLAINS","DESERT","TUNDRA","SNOW"]:
            rec["TERRAIN_"+c]=int(land.TERRAIN.eq(c).sum())
        for c in ["NONE","FOREST","JUNGLE"]:
            rec["VEG_"+c]=int(land.FEATURE_GAME.fillna("NONE").eq(c).sum())
        rows.append(rec)
    pd.DataFrame(rows).to_csv(args.prefix+"_REGIONAL_COUNTS.csv",index=False)

    # Basic schema, counts, and explicit review status. This is not a final approval.
    summary={
      "stage":"9R",
      "purpose":"user review checkpoint before any resource selection or placement",
      "source_stage":"Stage 9A consolidated, run 35439673753",
      "rows":int(len(g)),
      "surface_counts":g.SURFACE.value_counts(dropna=False).to_dict(),
      "relief_counts":g.loc[g.SURFACE.eq("LAND"),"RELIEF"].value_counts(dropna=False).to_dict(),
      "terrain_counts":g.loc[g.SURFACE.eq("LAND"),"TERRAIN"].value_counts(dropna=False).to_dict(),
      "vegetation_counts":g.loc[g.SURFACE.eq("LAND"),"FEATURE_GAME"].fillna("NONE").value_counts(dropna=False).to_dict(),
      "columns":list(g.columns),
      "review_status":"AWAITING_USER_REVIEW",
      "resources_included":False,
      "Stage1A_1deg_used":False
    }
    Path(args.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    Path(args.prefix+"_README.md").write_text(
      "# Stage 9R terrain/biome review\n\n"
      "This package is a review checkpoint. It uses Stage 9A only and contains no Stage 10 resource placement.\n\n"
      "Review layers:\n"
      "- Base terrain/biome: GRASSLAND, PLAINS, DESERT, TUNDRA, SNOW\n"
      "- Relief: FLAT, HILL, MOUNTAIN\n"
      "- Vegetation feature: NONE, FOREST, JUNGLE\n\n"
      "No resource stage is authorized by this package.\n",
      encoding="utf-8"
    )
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
