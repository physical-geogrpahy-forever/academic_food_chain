#!/usr/bin/env python3
"""
Stage 10H: aggregate MAPSPAM 2020 v2r2 physical crop area to canonical LAND hexes.

Source is the 5 arc-minute global physical-area COG. Values are preserved as
source-backed crop area evidence; this stage does not thin or randomly place
resources.

Groups:
  WHEAT       band 1
  RICE        band 2
  SUGAR       band 28 (sugarcane)
  COTTON      band 30
  COFFEE      bands 32+33 (arabica + robusta)
  COCOA       band 34
  TEA         band 35
  BANANAS     bands 37+38 (banana + plantain)
  CITRUS      band 39

Outputs per LAND hex:
  <GROUP>_SPAM_HA       approximate physical crop hectares inside hex
  <GROUP>_SPAM_FRAC     hectares / canonical hex hectares
  <GROUP>_SPAM_ANY      any positive source evidence
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from exactextract import exact_extract

GROUPS={
 "WHEAT":[1],
 "RICE":[2],
 "SUGAR":[28],
 "COTTON":[30],
 "COFFEE":[32,33],
 "COCOA":[34],
 "TEA":[35],
 "BANANAS":[37,38],
 "CITRUS":[39],
}
EXPECTED_NAMES={
 1:"Wheat",2:"Rice",28:"Sugarcane",30:"Cotton",32:"Arabic Coffee",
 33:"Robusta Coffee",34:"Cocoa",35:"Tea",37:"Banana",38:"Plantain",39:"Citrus"
}

def write_group(src, bands, out):
    prof=src.profile.copy()
    prof.pop("blockxsize",None);prof.pop("blockysize",None)
    prof.update(count=1,dtype="float32",nodata=-9999.0,compress="DEFLATE",tiled=False)
    with rasterio.open(out,"w",**prof) as dst:
        for _,win in src.block_windows(1):
            s=np.zeros((int(win.height),int(win.width)),dtype=np.float32)
            valid_any=np.zeros(s.shape,dtype=bool)
            for b in bands:
                a=src.read(b,window=win,masked=True)
                valid=~np.ma.getmaskarray(a)
                z=np.asarray(a.filled(0),dtype=np.float32)
                # MAPSPAM physical area should be non-negative; ignore any
                # residual negative sentinel values not handled by nodata.
                z=np.where(z>0,z,0)
                s += z
                valid_any |= valid
            w=np.where(valid_any,s,-9999.0).astype(np.float32)
            dst.write(w,1,window=win)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("mapspam_tif")
    ap.add_argument("--layer",default="game_map_stage10f_goget_evidence")
    ap.add_argument("--work",default="stage10h_work")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10H_MAPSPAM_EVIDENCE")
    a=ap.parse_args()
    work=Path(a.work);work.mkdir(parents=True,exist_ok=True)

    board=gpd.read_file(a.board,layer=a.layer)
    if len(board)!=261635 or not board.id.is_unique:
        raise RuntimeError("canonical board audit failed")
    land=board[board.SURFACE.eq("LAND")][["id","geometry"]].copy()
    if len(land)!=68048:raise RuntimeError(len(land))
    land["HEX_HA"]=land.geometry.area/10000.0
    land4326=land[["id","geometry"]].rename(columns={"id":"HEX_ID"}).to_crs(4326)

    with rasterio.open(a.mapspam_tif) as src:
        if src.count<39:raise RuntimeError(f"unexpected band count {src.count}")
        descriptions=list(src.descriptions)
        audit=[]
        out=land[["id","HEX_HA"]].copy()
        for group,bands in GROUPS.items():
            seen=[]
            for b in bands:
                desc=descriptions[b-1] or src.tags(b).get("long_name") or ""
                seen.append({"band":b,"description":desc,"long_name":src.tags(b).get("long_name","")})
            p=work/f"{group.lower()}_physical_area.tif"
            print("build",group,seen,flush=True)
            write_group(src,bands,p)
            x=exact_extract(str(p),land4326,["sum"],include_cols=["HEX_ID"],
                            output="pandas",strategy="raster-sequential")
            if "id" in x.columns:x=x.drop(columns=["id"])
            x=x.rename(columns={"HEX_ID":"id","sum":group+"_SPAM_HA"})
            x["id"]=pd.to_numeric(x.id,errors="raise").astype("int64")
            out=out.merge(x,on="id",how="left",validate="one_to_one")
            out[group+"_SPAM_HA"]=out[group+"_SPAM_HA"].fillna(0).clip(lower=0)
            out[group+"_SPAM_FRAC"]=(out[group+"_SPAM_HA"]/out["HEX_HA"]).clip(lower=0,upper=1)
            out[group+"_SPAM_ANY"]=(out[group+"_SPAM_HA"]>0).astype("uint8")
            audit.append({
              "group":group,
              "bands":bands,
              "band_metadata":seen,
              "hexes_with_evidence":int(out[group+"_SPAM_ANY"].sum()),
              "total_physical_area_ha":float(out[group+"_SPAM_HA"].sum()),
              "max_hex_area_ha":float(out[group+"_SPAM_HA"].max()),
              "max_hex_fraction":float(out[group+"_SPAM_FRAC"].max()),
            })
            p.unlink(missing_ok=True)

    evcols=[c for c in out.columns if c not in ["id","HEX_HA"]]
    board=board.merge(out[["id"]+evcols],on="id",how="left",validate="one_to_one")
    for c in evcols:board[c]=board[c].fillna(0)
    board.to_file(a.prefix+".gpkg",layer="game_map_stage10h_mapspam_evidence",driver="GPKG")
    out.to_csv(a.prefix+"_LAND_EVIDENCE.csv",index=False)
    pd.DataFrame([{k:v for k,v in r.items() if k!="band_metadata"} for r in audit]).to_csv(
        a.prefix+"_AUDIT.csv",index=False)

    summary={
      "stage":"10H",
      "source":"MAPSPAM 2020 v2r2 global physical area, 5 arc-minute",
      "groups":audit,
      "land_hexes":68048,
      "placement_policy":"Evidence only; no random placement and no gameplay thinning.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
