#!/usr/bin/env python3
"""
Stage 10B source audit for MAPSPAM 2020 v2r2 global physical-area COG.

The file contains one band per crop. This probe records band descriptions/tags,
dimensions, CRS, transform, and identifies crop bands potentially usable for
Civ-style bonus/luxury resources. No placement is performed yet.
"""
import argparse, json, re
from pathlib import Path
import rasterio

TARGETS={
 "WHEAT":["wheat"],
 "BANANAS":["banana","plantain"],
 "SUGAR":["sugarcane","sugar cane","sugar beet"],
 "COTTON":["cotton"],
 "CITRUS":["orange","citrus"],
 "GRAPES_WINE":["grape"],
 "RICE":["rice"],
 "COCOA":["cocoa","cacao"],
 "COFFEE":["coffee"],
 "TEA":["tea"],
 "SPICES":["spice","pepper"],
 "OIL_PALM":["oil palm","palm oil"],
}

def norm(s):
    return re.sub(r"[^a-z0-9]+"," ",str(s).lower()).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10B_MAPSPAM_PROBE")
    a=ap.parse_args()
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
        with rasterio.open(a.url) as src:
            bands=[]
            descs=list(src.descriptions)
            for i in range(1,src.count+1):
                tags=src.tags(i)
                desc=descs[i-1] or tags.get("DESCRIPTION") or tags.get("long_name") or tags.get("crop") or ""
                rec={"band":i,"description":desc,"tags":tags}
                bands.append(rec)
            meta={
              "source":"MAPSPAM 2020 v2r2 physical area COG",
              "url":a.url,
              "width":src.width,"height":src.height,"count":src.count,
              "crs":str(src.crs),"transform":list(src.transform)[:6],
              "bounds":list(src.bounds),"dtype":src.dtypes[0],
              "nodata":src.nodata,
            }
    # Search both description and serialized tags.
    matches={}
    for target,keys in TARGETS.items():
        hit=[]
        for b in bands:
            text=norm(b["description"]+" "+json.dumps(b["tags"],sort_keys=True))
            if any(norm(k) in text for k in keys):
                hit.append({"band":b["band"],"description":b["description"],"tags":b["tags"]})
        matches[target]=hit
    out={"metadata":meta,"bands":bands,"target_matches":matches}
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({"metadata":meta,"target_matches":matches},indent=2))
if __name__=="__main__":main()
