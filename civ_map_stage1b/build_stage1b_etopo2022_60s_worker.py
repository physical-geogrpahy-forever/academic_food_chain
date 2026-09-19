#!/usr/bin/env python3
"""
Stage 1B high-resolution relief worker for the Civilization-style world hex map.

Source:
- NOAA NCEI ETOPO 2022 v1 60 arc-second surface GeoTIFF.
- Natural Earth 1:10m land polygons used ONLY to mask ocean/bathymetry from LAND-hex relief stats.

This script does NOT use the old 1-degree checkpoint.
It reconstructs the canonical 781 x 335 parent lattice from the verified Stage 0 constants,
selects the 68,048 current LAND hexes from an embedded compressed bitset, and aggregates
native 60-arc-second numeric elevations directly inside each hex.

Output CSV contains raw statistics only. Final FLAT/HILL/MOUNTAIN thresholds are calibrated
after QA from these statistics; they are not inherited from Stage 1A.
"""
import os, sys, math, base64, zlib, zipfile, argparse, hashlib, shutil
from pathlib import Path
import numpy as np
import pandas as pd

ROWS = 335
COLS = 781
N = ROWS * COLS
HEX_W = 57735.0269189626
HEX_H = 50000.0
X_STEP = 43301.27018922195
BASE_LEFT = -16920565.0448
BASE_TOP = 8315130.3484
LAND_BITS_B64 = """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"""

ETOPO_URL = "https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/60s/60s_surface_elev_gtif/ETOPO_2022_v1_60s_N90W180_surface.tif"
NE_URL = "https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_land.zip"

def decode_land_mask():
    raw = zlib.decompress(base64.b64decode(LAND_BITS_B64))
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="little")[:N]
    assert bits.size == N
    return bits.astype(bool)

def hex_polygon_xy(col, row):
    left = BASE_LEFT + col * X_STEP
    top = BASE_TOP - row * HEX_H - (col % 2) * (HEX_H / 2.0)
    right = left + HEX_W
    bottom = top - HEX_H
    cy = 0.5 * (top + bottom)
    qx = HEX_W / 4.0
    return [(left, cy),(left + qx, top),(right - qx, top),(right, cy),
            (right - qx, bottom),(left + qx, bottom),(left, cy)]

def reconstruct_land_gdf():
    import geopandas as gpd
    from shapely.geometry import Polygon
    mask = decode_land_mask()
    ids = np.flatnonzero(mask) + 1
    cols = (ids - 1) // ROWS
    rows = (ids - 1) % ROWS
    geoms = [Polygon(hex_polygon_xy(int(c), int(r))) for c, r in zip(cols, rows)]
    gdf = gpd.GeoDataFrame({"id": ids.astype(np.int64), "row_index": rows.astype(np.int32),
                            "col_index": cols.astype(np.int32)}, geometry=geoms, crs="EPSG:8857")
    assert len(gdf) == 68048
    return gdf

def sha256(path, chunk=8*1024*1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def download(url, out):
    import requests
    out = Path(out)
    if out.exists() and out.stat().st_size > 0:
        return out
    tmp = out.with_suffix(out.suffix + ".part")
    with requests.get(url, stream=True, timeout=(30,300)) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done=0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=8*1024*1024):
                if chunk:
                    f.write(chunk); done += len(chunk)
                    if total:
                        print(f"download {out.name} {done/total:.1%}", flush=True)
    tmp.replace(out)
    return out

def prepare_land_mask(dem_path, work):
    import geopandas as gpd
    import rasterio
    from rasterio.features import rasterize
    work=Path(work)
    nezip=download(NE_URL, work/"ne_10m_land.zip")
    nedir=work/"ne_10m_land"
    shp=nedir/"ne_10m_land.shp"
    if not shp.exists():
        nedir.mkdir(exist_ok=True)
        with zipfile.ZipFile(nezip) as z: z.extractall(nedir)
    land=gpd.read_file(shp)
    with rasterio.open(dem_path) as src:
        # ETOPO 2022 GeoTIFF may expose a compound horizontal+vertical CRS
        # (WGS84 horizontal + EGM2008 vertical), so src.crs.to_epsg() need not
        # equal 4326. Validate the actual global lon/lat grid instead.
        transform=src.transform
        shape=(src.height,src.width)
        b=src.bounds
        xres=abs(src.transform.a); yres=abs(src.transform.e)
        if not (abs(b.left + 180.0) < 1e-4 and abs(b.right - 180.0) < 1e-4
                and abs(b.bottom + 90.0) < 1e-4 and abs(b.top - 90.0) < 1e-4):
            raise RuntimeError(f"unexpected ETOPO2022 bounds: {b}")
        if not (abs(xres - 1/60) < 1e-8 and abs(yres - 1/60) < 1e-8):
            raise RuntimeError(f"unexpected ETOPO2022 resolution: {xres}, {yres}")
        print("DEM_CRS", src.crs, "BOUNDS", b, "RES", (xres,yres), flush=True)
    shapes=((geom,1) for geom in land.geometry if geom is not None and not geom.is_empty)
    mask=rasterize(shapes,out_shape=shape,transform=transform,fill=0,dtype="uint8",all_touched=False)
    mpath=work/"landmask_60s.tif"
    mprof={"driver":"GTiff","height":shape[0],"width":shape[1],"count":1,"dtype":"uint8",
           "crs":"EPSG:4326","transform":transform,"nodata":0,"compress":"DEFLATE","tiled":True,
           "blockxsize":512,"blockysize":512,"BIGTIFF":"YES"}
    with rasterio.open(mpath,"w",**mprof) as dst:
        for _,win in dst.block_windows(1):
            r0=int(win.row_off); r1=r0+int(win.height)
            c0=int(win.col_off); c1=c0+int(win.width)
            dst.write(mask[r0:r1,c0:c1],1,window=win)
    return mpath

def make_land_dem_and_slope(dem_path, mask_path, work):
    import rasterio
    from rasterio.windows import Window
    work=Path(work)
    landdem=work/"ETOPO2022_60s_landonly.tif"
    slope=work/"ETOPO2022_60s_land_slope_deg.tif"
    nodata=-99999.0
    with rasterio.open(dem_path) as src, rasterio.open(mask_path) as msrc:
        prof=src.profile.copy()
        # Use the verified horizontal CRS only for derived rasters. The source
        # may carry a vertical CRS component that exactextract does not need.
        prof.update(crs="EPSG:4326",dtype="float32",nodata=nodata,compress="DEFLATE",tiled=True,
                    blockxsize=512,blockysize=512,BIGTIFF="YES")
        with rasterio.open(landdem,"w",**prof) as dst:
            for _,win in src.block_windows(1):
                z=src.read(1,window=win).astype("float32")
                m=msrc.read(1,window=win).astype(bool)
                z[~m]=nodata
                dst.write(z,1,window=win)
        with rasterio.open(slope,"w",**prof) as dst:
            H,W=src.height,src.width
            for r in range(H):
                rr0=max(0,r-1); rr1=min(H-1,r+1)
                zprev=src.read(1,window=Window(0,rr0,W,1)).astype("float32")[0]
                zcur =src.read(1,window=Window(0,r,W,1)).astype("float32")[0]
                znext=src.read(1,window=Window(0,rr1,W,1)).astype("float32")[0]
                mprev=msrc.read(1,window=Window(0,rr0,W,1)).astype(bool)[0]
                mcur =msrc.read(1,window=Window(0,r,W,1)).astype(bool)[0]
                mnext=msrc.read(1,window=Window(0,rr1,W,1)).astype(bool)[0]
                zl=np.roll(zcur,1); zr=np.roll(zcur,-1)
                ml=np.roll(mcur,1); mr=np.roll(mcur,-1)
                valid=mcur & mprev & mnext & ml & mr
                valid[0]=False; valid[-1]=False
                lat=src.xy(r,0)[1]
                dy=111132.0/60.0
                dx=max(25.0,111320.0*math.cos(math.radians(lat))/60.0)
                dzdx=(zr-zl)/(2.0*dx)
                dzdy=(zprev-znext)/(2.0*dy)
                sl=np.full(W,nodata,dtype="float32")
                sl[valid]=np.degrees(np.arctan(np.sqrt(dzdx[valid]**2+dzdy[valid]**2))).astype("float32")
                dst.write(sl.reshape(1,-1),1,window=Window(0,r,W,1))
                if r%500==0: print("slope row",r,"/",H,flush=True)
    return landdem,slope

def run_exactextract(raster_path, gdf4326, stats):
    from exactextract import exact_extract
    return exact_extract(str(raster_path), gdf4326, stats, include_cols=["id"], output="pandas")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--work",default="stage1b_work")
    ap.add_argument("--dem",default=None)
    ap.add_argument("--out",default="CIV_GAME_MAP_STAGE1B_ETOPO2022_60S_STATS.csv")
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    work=Path(args.work); work.mkdir(parents=True,exist_ok=True)
    land=reconstruct_land_gdf()
    print("LAND hexes",len(land),"id range",land.id.min(),land.id.max())
    if args.self_test:
        print("SELF_TEST_OK")
        return
    dem=Path(args.dem) if args.dem else work/"ETOPO_2022_v1_60s_N90W180_surface.tif"
    if not dem.exists(): download(ETOPO_URL,dem)
    print("DEM",dem,dem.stat().st_size,sha256(dem))
    mpath=prepare_land_mask(dem,work)
    landdem,slope=make_land_dem_and_slope(dem,mpath,work)
    g=land.to_crs("EPSG:4326")
    estats=["count","min","max","mean","quantile(q=0.1)","quantile(q=0.5)","quantile(q=0.9)"]
    elev=run_exactextract(landdem,g,estats)
    elev=elev.rename(columns={
        "count":"DEM_N","min":"ELEV_MIN","max":"ELEV_MAX","mean":"ELEV_MEAN",
        "quantile_q_0_1":"ELEV_P10","quantile_q_0_5":"ELEV_MED","quantile_q_0_9":"ELEV_P90",
        "quantile(q=0.1)":"ELEV_P10","quantile(q=0.5)":"ELEV_MED","quantile(q=0.9)":"ELEV_P90",
    })
    qcols=[c for c in elev.columns if "quantile" in c.lower()]
    if "ELEV_P10" not in elev.columns and len(qcols)>=3:
        elev=elev.rename(columns={qcols[0]:"ELEV_P10",qcols[1]:"ELEV_MED",qcols[2]:"ELEV_P90"})
    sl=run_exactextract(slope,g,["mean","quantile(q=0.9)","count"])
    sl=sl.rename(columns={"mean":"SLOPE_MEAN","count":"SLOPE_N",
                          "quantile_q_0_9":"SLOPE_P90","quantile(q=0.9)":"SLOPE_P90"})
    qcols=[c for c in sl.columns if "quantile" in c.lower()]
    if "SLOPE_P90" not in sl.columns and qcols:
        sl=sl.rename(columns={qcols[0]:"SLOPE_P90"})
    out=elev.merge(sl,on="id",how="left")
    out["RELIEF_P90P10"]=out["ELEV_P90"]-out["ELEV_P10"]
    out["ELEV_RANGE"]=out["ELEV_MAX"]-out["ELEV_MIN"]
    out["DEM_SRC"]="ETOPO2022_v1_60s_surface"
    out=out.merge(land.drop(columns="geometry"),on="id",how="left")
    cols=["id","row_index","col_index","DEM_N","ELEV_MIN","ELEV_P10","ELEV_MEAN","ELEV_MED",
          "ELEV_P90","ELEV_MAX","RELIEF_P90P10","ELEV_RANGE","SLOPE_N","SLOPE_MEAN","SLOPE_P90","DEM_SRC"]
    out[cols].sort_values("id").to_csv(args.out,index=False)
    print("WROTE",args.out,len(out))
    print(out[cols].describe(include="all").to_string())

if __name__=="__main__":
    main()
