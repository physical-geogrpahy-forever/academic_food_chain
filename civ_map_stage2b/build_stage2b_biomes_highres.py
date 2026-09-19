#!/usr/bin/env python3
"""
Stage 2B corrected biomes/features for the Civilization-style global 50-km hex board.

Inputs
------
1. Stage 1B ETOPO2022 60-second classified LAND CSV downloaded from the
   successful GitHub Actions QA artifact.
2. The Stage 0A/0B surface mask, embedded here as a compressed uint8 array.
3. The packaged 0.5-degree RESOLVE/WWF terrestrial-biome proxy grid, embedded
   here in the same compact RLE representation used by the prior Stage 2 build.

Important
---------
- NO Stage 1A / 1-degree relief data are read or reused.
- LAND/OCEAN/COAST/LAKE/VOID are preserved from Stage 0A/0B.
- Relief and biome remain separate attributes.
- Forest/Jungle game features are recalculated after the new Stage 1B relief.
- Full parent-grid geometry is reconstructed from the locked EPSG:8857 lattice
  constants. This is coordinate-equivalent reconstruction, not a claim of
  byte-for-byte WKB identity with the archived Stage 0 GPKG.
"""
import argparse, base64, zlib, json, hashlib, math, os, zipfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import Transformer

ROWS=335
COLS=781
N=ROWS*COLS
HEX_W=57735.0269189626
HEX_H=50000.0
X_STEP=43301.27018922195
BASE_LEFT=-16920565.0448
BASE_TOP=8315130.3484

SURFACE_B64="""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"""
WWF_B64="""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"""

SURFACE_NAMES=np.array(["VOID","OCEAN","COAST","LAND","LAKE"],dtype=object)

BIOME={
'A':'Boreal Forests/Taiga','B':'Deserts & Xeric Shrublands','C':'Flooded Grasslands & Savannas','D':'Mangroves',
'E':'Mediterranean Forests, Woodlands & Scrub','F':'Montane Grasslands & Shrublands','G':'Temperate Broadleaf & Mixed Forests',
'H':'Temperate Conifer Forests','I':'Temperate Grasslands, Savannas & Shrublands','J':'Tropical & Subtropical Coniferous Forests',
'K':'Tropical & Subtropical Dry Broadleaf Forests','L':'Tropical & Subtropical Grasslands, Savannas & Shrublands',
'M':'Tropical & Subtropical Moist Broadleaf Forests','N':'Tundra','R':'Rock and Ice'}
TF={
'A':('TUNDRA','FOREST'),'B':('DESERT','NONE'),'C':('GRASSLAND','MARSH_CANDIDATE'),'D':('GRASSLAND','MARSH_CANDIDATE'),
'E':('PLAINS','FOREST'),'F':('PLAINS','NONE'),'G':('GRASSLAND','FOREST'),'H':('GRASSLAND','FOREST'),
'I':('PLAINS','NONE'),'J':('GRASSLAND','FOREST'),'K':('PLAINS','FOREST'),'L':('PLAINS','NONE'),
'M':('GRASSLAND','JUNGLE'),'N':('TUNDRA','NONE'),'R':('SNOW','NONE')}
VALID=set(BIOME)

def decode_surface():
    raw=zlib.decompress(base64.b64decode(SURFACE_B64))
    a=np.frombuffer(raw,dtype=np.uint8).copy()
    if len(a)!=N: raise RuntimeError(("surface length",len(a),N))
    exp=[27723,156201,8781,68048,882]
    got=np.bincount(a,minlength=5).tolist()
    if got!=exp: raise RuntimeError(("surface counts",got,exp))
    return a

def decode_wwf():
    text=zlib.decompress(base64.b64decode(WWF_B64)).decode("utf-8")
    rows=text.split("|")
    if len(rows)!=360: raise RuntimeError(("WWF rows",len(rows)))
    def decode_row(s):
        vals=[]; i=0
        while i<len(s):
            j=i
            while j<len(s) and (s[j].isdigit() or ('a'<=s[j]<='z')): j+=1
            if j==i or j>=len(s): raise ValueError((i,s[max(0,i-5):i+10]))
            n=int(s[i:j],36); vals.extend([s[j]]*n); i=j+1
        if len(vals)!=720: raise ValueError(("WWF row width",len(vals)))
        return vals
    return np.asarray([decode_row(r) for r in rows],dtype="U1")

def hex_xy(col,row):
    left=BASE_LEFT+col*X_STEP
    top=BASE_TOP-row*HEX_H-(col%2)*(HEX_H/2.0)
    right=left+HEX_W
    bottom=top-HEX_H
    cy=(top+bottom)/2.0
    qx=HEX_W/4.0
    return [(left,cy),(left+qx,top),(right-qx,top),(right,cy),
            (right-qx,bottom),(left+qx,bottom),(left,cy)]

def make_parent():
    ids=np.arange(1,N+1,dtype=np.int64)
    cols=((ids-1)//ROWS).astype(np.int32)
    rows=((ids-1)%ROWS).astype(np.int32)
    geoms=[Polygon(hex_xy(int(c),int(r))) for c,r in zip(cols,rows)]
    g=gpd.GeoDataFrame({"id":ids,"row_index":rows,"col_index":cols},geometry=geoms,crs="EPSG:8857")
    return g

def land_samples(land_ids):
    ids=np.asarray(land_ids,dtype=np.int64)
    cols=((ids-1)//ROWS).astype(np.int64)
    rows=((ids-1)%ROWS).astype(np.int64)
    left=BASE_LEFT+cols*X_STEP
    top=BASE_TOP-rows*HEX_H-(cols%2)*(HEX_H/2.0)
    right=left+HEX_W
    bottom=top-HEX_H
    cx=(left+right)/2.0
    cy=(top+bottom)/2.0
    qx=HEX_W/4.0
    # Six vertices excluding closing point, vectorized.
    vx=np.column_stack([left,left+qx,right-qx,right,right-qx,left+qx])
    vy=np.column_stack([cy,top,top,cy,bottom,bottom])
    ns=len(ids); S=13
    xs=np.empty((ns,S),dtype=float); ys=np.empty((ns,S),dtype=float)
    xs[:,0]=cx; ys[:,0]=cy
    k=1
    for t in (0.45,0.80):
        xs[:,k:k+6]=cx[:,None]+t*(vx-cx[:,None])
        ys[:,k:k+6]=cy[:,None]+t*(vy-cy[:,None])
        k+=6
    return xs,ys,cx,cy

def classify_biomes(grid,land_ids):
    xs,ys,cx,cy=land_samples(land_ids)
    tr=Transformer.from_crs("EPSG:8857","EPSG:4326",always_xy=True)
    lon,lat=tr.transform(xs.ravel(),ys.ravel())
    lon=np.asarray(lon).reshape(xs.shape); lat=np.asarray(lat).reshape(ys.shape)
    rr=np.clip(np.floor((90-lat)/0.5).astype(int),0,359)
    cc=np.mod(np.floor((lon+180)/0.5).astype(int),720)
    codes=grid[rr,cc]
    n=len(land_ids)
    out_code=np.full(n,"?",dtype="U1")
    conf=np.zeros(n,float); fall=np.zeros(n,dtype=np.int16); nsamp=np.zeros(n,dtype=np.int16)
    for j in range(n):
        vals=[x for x in codes[j].tolist() if x in VALID]
        nsamp[j]=len(vals)
        if vals:
            cnt=Counter(vals); m=max(cnt.values()); tied=sorted(k for k,v in cnt.items() if v==m); cent=codes[j,0]
            win=cent if cent in tied else tied[0]
            out_code[j]=win; conf[j]=m/len(vals)
        else:
            r0,c0=rr[j,0],cc[j,0]
            for rad in range(1,6):
                cand=[]
                for dr in range(-rad,rad+1):
                    for dc in range(-rad,rad+1):
                        if max(abs(dr),abs(dc))!=rad: continue
                        r=r0+dr
                        if 0<=r<360:
                            q=grid[r,(c0+dc)%720]
                            if q in VALID: cand.append((dr*dr+dc*dc,q))
                if cand:
                    cand.sort(key=lambda z:(z[0],z[1])); out_code[j]=cand[0][1]; fall[j]=1; break
            if out_code[j]=="?":
                alat=abs(lat[j,0]); out_code[j]="R" if alat>=75 else ("N" if alat>=60 else "I"); fall[j]=2
    clon,clat=tr.transform(cx,cy)
    return out_code,conf,fall,nsamp,np.asarray(clon),np.asarray(clat)

def sha256(path,chunk=8*1024*1024):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stage1b_classified")
    ap.add_argument("--outdir",default="stage2b_out")
    a=ap.parse_args()
    od=Path(a.outdir); od.mkdir(parents=True,exist_ok=True)

    surf_code=decode_surface()
    surface=SURFACE_NAMES[surf_code]
    land_ids=np.flatnonzero(surf_code==3).astype(np.int64)+1

    r=pd.read_csv(a.stage1b_classified)
    if len(r)!=68048 or not r["id"].is_unique:
        raise RuntimeError("Stage1B classified LAND table is not canonical 68,048 unique IDs")
    r["id"]=r["id"].astype(np.int64)
    if not np.array_equal(np.sort(r.id.to_numpy()),land_ids):
        raise RuntimeError("Stage1B LAND ID set differs from Stage0 LAND ID set")
    rel_counts=r["RELIEF"].value_counts().to_dict()
    print("Stage1B relief counts",rel_counts,flush=True)

    grid=decode_wwf()
    code,conf,fall,nsamp,land_lon,land_lat=classify_biomes(grid,land_ids)

    # Full-board geometry from locked parent lattice.
    g=make_parent()
    g["SURFACE"]=surface
    # Centroids in geographic coordinates for all cells.
    cent=g.geometry.centroid
    tr=Transformer.from_crs("EPSG:8857","EPSG:4326",always_xy=True)
    lon,lat=tr.transform(cent.x.to_numpy(),cent.y.to_numpy())
    g["LON"]=np.asarray(lon)
    g["LAT"]=np.asarray(lat)

    # Stage1B metrics/relief, LAND only.
    keep=[c for c in ["id","RELIEF","DEM_N","ELEV_MIN","ELEV_P10","ELEV_P25","ELEV_MEAN","ELEV_MED",
                       "ELEV_P75","ELEV_P90","ELEV_MAX","RELIEF_P90P10","ELEV_RANGE",
                       "SLOPE_N","SLOPE_MEAN","SLOPE_MED","SLOPE_P75","SLOPE_P90","DEM_SRC"] if c in r.columns]
    g=g.merge(r[keep],on="id",how="left",validate="one_to_one")
    landmask=g["SURFACE"].eq("LAND").to_numpy()

    # Allocate biome/terrain fields.
    n=len(g)
    wwf_code=np.full(n,"",dtype=object); wwf_biome=np.full(n,"",dtype=object)
    terrain=np.full(n,"",dtype=object); eco=np.full(n,"NONE",dtype=object); game=np.full(n,"NONE",dtype=object)
    bconf=np.full(n,np.nan); bfall=np.full(n,-1,dtype=np.int16); bsamp=np.zeros(n,dtype=np.int16)

    li=np.flatnonzero(landmask)
    wwf_code[li]=code
    wwf_biome[li]=[BIOME[c] for c in code]
    terrain[li]=[TF[c][0] for c in code]
    eco[li]=[TF[c][1] for c in code]
    bconf[li]=conf; bfall[li]=fall; bsamp[li]=nsamp

    terrain[surface=="OCEAN"]="OCEAN"
    terrain[surface=="COAST"]="COAST"
    terrain[surface=="LAKE"]="LAKE"
    terrain[surface=="VOID"]="VOID"

    rel=g["RELIEF"].fillna("").astype(str).to_numpy()
    for feat in ("FOREST","JUNGLE"):
        m=landmask & (eco==feat) & (rel!="MOUNTAIN")
        game[m]=feat
    marshcand=landmask & (eco=="MARSH_CANDIDATE") & (rel!="MOUNTAIN")

    g["WWF_CODE"]=wwf_code
    g["WWF_BIOME"]=wwf_biome
    g["TERRAIN"]=terrain
    g["FEATURE_ECO"]=eco
    g["FEATURE_GAME"]=game
    g["MARSH_CAND"]=marshcand.astype(np.int8)
    g["BIO_CONF"]=np.round(bconf,3)
    g["BIO_FALL"]=bfall
    g["BIO_NSAMP"]=bsamp
    g["BIO_SRC"]="RESOLVE2017_0p5deg"
    g["BIO_STAGE"]="STAGE2B_HIGHRES_RELIEF"

    # Hard gates.
    expected_surface={"LAND":68048,"LAKE":882,"COAST":8781,"OCEAN":156201,"VOID":27723}
    got_surface=g["SURFACE"].value_counts().to_dict()
    if any(int(got_surface.get(k,0))!=v for k,v in expected_surface.items()):
        raise RuntimeError(("surface gate",got_surface))
    if g.loc[landmask,"RELIEF"].isna().any():
        raise RuntimeError("LAND relief contains NA after Stage1B merge")

    gpkg=od/"CIV_GAME_MAP_STAGE2B_BIOMES_HIGHRES.gpkg"
    g.to_file(gpkg,layer="game_map_stage2b_biomes",driver="GPKG")

    # Summary.
    rows=[]
    for col,mask in [("SURFACE",np.ones(n,bool)),("TERRAIN",np.ones(n,bool)),("RELIEF",landmask),
                     ("FEATURE_ECO",landmask),("FEATURE_GAME",landmask),("MARSH_CAND",landmask)]:
        for k,v in g.loc[mask,col].value_counts(dropna=False).items():
            rows.append({"group":col,"class":str(k),"count":int(v)})
    pd.DataFrame(rows).to_csv(od/"CIV_GAME_MAP_STAGE2B_BIOMES_SUMMARY.csv",index=False)

    # Broad terrain QA: nearest LAND center.
    qa_pts=[
      ("Seoul",37.57,126.98,{"GRASSLAND"}),("Tokyo",35.68,139.76,{"GRASSLAND"}),
      ("Amazon",-3.1,-60.0,{"GRASSLAND"}),("Congo",0.5,23.5,{"GRASSLAND"}),
      ("Sahara",24,12,{"DESERT"}),("Arabia",24,45,{"DESERT"}),("Mongolia",46,103,{"PLAINS","DESERT"}),
      ("Siberia",62,100,{"TUNDRA"}),("Greenland",72,-40,{"SNOW","TUNDRA"}),("Sahel",14,0,{"PLAINS"}),
      ("Central_Australia",-24,134,{"DESERT","PLAINS"}),("Patagonia",-47,-70,{"PLAINS","TUNDRA"})]
    L=g.loc[landmask].reset_index(drop=True)
    la=L["LAT"].to_numpy(); lo=L["LON"].to_numpy()
    q=[]
    for name,plat,plon,exp in qa_pts:
        dl=np.abs(lo-plon); dl=np.minimum(dl,360-dl)
        d2=(la-plat)**2+(dl*np.cos(np.deg2rad(plat)))**2
        j=int(np.argmin(d2)); rr=L.iloc[j]
        q.append({"name":name,"hex_id":int(rr.id),"hex_lat":float(rr.LAT),"hex_lon":float(rr.LON),
                  "terrain":rr.TERRAIN,"feature_eco":rr.FEATURE_ECO,"feature_game":rr.FEATURE_GAME,
                  "relief":rr.RELIEF,"expected_terrain":"/".join(sorted(exp)),
                  "pass":bool(rr.TERRAIN in exp)})
    qdf=pd.DataFrame(q)
    qdf.to_csv(od/"CIV_GAME_MAP_STAGE2B_BIOMES_QA.csv",index=False)

    # Audit.
    audit=[
      {"check":"parent_cells","value":len(g),"expected":N,"pass":len(g)==N},
      {"check":"land_cells","value":int(landmask.sum()),"expected":68048,"pass":int(landmask.sum())==68048},
      {"check":"lake_cells","value":int((surface=="LAKE").sum()),"expected":882,"pass":int((surface=="LAKE").sum())==882},
      {"check":"coast_cells","value":int((surface=="COAST").sum()),"expected":8781,"pass":int((surface=="COAST").sum())==8781},
      {"check":"ocean_cells","value":int((surface=="OCEAN").sum()),"expected":156201,"pass":int((surface=="OCEAN").sum())==156201},
      {"check":"void_cells","value":int((surface=="VOID").sum()),"expected":27723,"pass":int((surface=="VOID").sum())==27723},
      {"check":"terrain_spot_QA","value":int(qdf["pass"].sum()),"expected":len(qdf),"pass":bool(qdf["pass"].all())},
      {"check":"geometry_method","value":"locked 781x335 EPSG:8857 lattice constants","expected":"coordinate-equivalent Stage0 reconstruction","pass":True},
      {"check":"Stage1A_1deg_used","value":"NO","expected":"NO","pass":True},
    ]
    pd.DataFrame(audit).to_csv(od/"CIV_GAME_MAP_STAGE2B_AUDIT.csv",index=False)

    # Preview.
    import matplotlib.pyplot as plt
    colors={"VOID":"white","OCEAN":"#9fc8e5","COAST":"#b8dcf0","LAKE":"#8bc2df",
            "GRASSLAND":"#7da85b","PLAINS":"#c6b56f","DESERT":"#e5ce8d","TUNDRA":"#a6a893","SNOW":"#edf1f3"}
    fig,ax=plt.subplots(figsize=(18,9),dpi=150)
    for k,col in colors.items():
        sel=g[g["TERRAIN"]==k]
        if len(sel): sel.plot(ax=ax,color=col,edgecolor="none",linewidth=0)
    ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_title("Civilization-style GAME MAP — Stage 2B biomes with ETOPO2022 60-second relief\n(Stage 0 water preserved; no 1-degree relief used)",fontsize=12)
    plt.tight_layout()
    fig.savefig(od/"CIV_GAME_MAP_STAGE2B_BIOMES_PREVIEW.png",bbox_inches="tight",facecolor="white")
    plt.close(fig)

    meta={
      "stage":"2B",
      "rows":int(len(g)),
      "surface_counts":{k:int(v) for k,v in got_surface.items()},
      "relief_counts":{k:int(v) for k,v in g.loc[landmask,"RELIEF"].value_counts().items()},
      "terrain_counts":{k:int(v) for k,v in g["TERRAIN"].value_counts().items()},
      "feature_game_counts":{k:int(v) for k,v in g.loc[landmask,"FEATURE_GAME"].value_counts().items()},
      "marsh_candidates":int(marshcand.sum()),
      "terrain_QA_pass":int(qdf["pass"].sum()),
      "terrain_QA_total":int(len(qdf)),
      "Stage1A_1deg_used":False,
      "geometry_note":"reconstructed from locked EPSG:8857 parent-lattice constants; join attributes back to archived Stage0AB GPKG for byte-identical geometry if required",
      "gpkg_sha256":sha256(gpkg),
    }
    (od/"CIV_GAME_MAP_STAGE2B_METADATA.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")

    readme=f"""# Civilization-style GAME MAP — Stage 2B high-resolution relief integration

This build uses Stage 1B relief derived from NOAA ETOPO 2022 60-arc-second numeric DEM.
The discarded Stage 1A 1-degree relief is not read or reused.

Stage 0A/0B surface classes are preserved at the canonical counts:
LAND 68,048; LAKE 882; COAST 8,781; OCEAN 156,201; VOID 27,723.

Terrestrial biome assignment uses the packaged RESOLVE/WWF 0.5-degree proxy grid and
the same 13-sample majority-vote method as the corrected Stage 2 logic. Forest and
Jungle game features are recomputed so that MOUNTAIN cells do not retain them.
Flooded-grassland/mangrove classes remain MARSH_CAND only.

Geometry in this GitHub build is reconstructed from the locked 781 x 335 EPSG:8857
parent-lattice constants. It is intended to be coordinate-equivalent to Stage 0.
For a strict byte-identical geometry release, join these attributes by canonical id
back onto the archived Stage0AB GPKG.

Terrain QA passed {int(qdf['pass'].sum())}/{len(qdf)} broad regional checks.
"""
    (od/"CIV_GAME_MAP_STAGE2B_README.md").write_text(readme,encoding="utf-8")

    # Package.
    zpath=od/"CIV_GAME_MAP_STAGE2B_BIOMES_PACKAGE.zip"
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(od.iterdir()):
            if p.name!=zpath.name:
                z.write(p,p.name)

    print(json.dumps(meta,indent=2),flush=True)
    print(qdf.to_string(index=False),flush=True)

if __name__=="__main__":
    main()
