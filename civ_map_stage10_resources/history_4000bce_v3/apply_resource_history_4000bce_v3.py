#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import geopandas as gpd

DYNAMIC = {
    "MAIZE","WHEAT","RICE","BANANAS","CITRUS","COCOA","COTTON","SUGAR",
    "COFFEE","TEA","TOBACCO","OLIVES","WINE","DYES","SPICES",
    "HORSES","CATTLE","SHEEP"
}

def ensure_lonlat(g):
    if "lon" in g.columns and "lat" in g.columns:
        return g
    gg = g.copy()
    cent = gg.geometry.centroid
    ll = gpd.GeoSeries(cent, crs=gg.crs).to_crs(4326)
    gg["lon"] = ll.x.to_numpy()
    gg["lat"] = ll.y.to_numpy()
    return gg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grid_gpkg")
    ap.add_argument("placement_csv")
    ap.add_argument("mask_csv")
    ap.add_argument("--layer", default=None)
    ap.add_argument("--out", default="CIV_GAME_MAP_STAGE10_RESOURCE_HISTORY_4000BCE_V3.csv")
    args = ap.parse_args()

    g = gpd.read_file(args.grid_gpkg, layer=args.layer) if args.layer else gpd.read_file(args.grid_gpkg)
    g = ensure_lonlat(g)
    coords = g[["id","lon","lat"]].copy()
    if coords["id"].duplicated().any():
        raise SystemExit("Grid id is not unique")

    p = pd.read_csv(args.placement_csv)
    if p["id"].duplicated().any():
        raise SystemExit("Placement id is not unique")
    p = p.merge(coords, on="id", how="left", validate="one_to_one")
    if p[["lon","lat"]].isna().any().any():
        raise SystemExit(f"Missing coordinates for {int(p['lon'].isna().sum())} placement rows")

    masks = pd.read_csv(args.mask_csv)
    byres = {r: d.reset_index(drop=True) for r, d in masks.groupby("RESOURCE_ID")}

    states, regions = [], []
    for row in p.itertuples(index=False):
        r = str(row.RESOURCE_ID)
        if r not in DYNAMIC:
            states.append("STATIC")
            regions.append("")
            continue
        hit = []
        for m in byres.get(r, pd.DataFrame()).itertuples(index=False):
            if m.LON_MIN <= row.lon <= m.LON_MAX and m.LAT_MIN <= row.lat <= m.LAT_MAX:
                hit.append(str(m.REGION_ID))
        states.append("START_VISIBLE" if hit else "LATENT")
        regions.append(";".join(hit))

    p["HIST_4000_STATE"] = states
    p["HIST_4000_REGION"] = regions
    p.to_csv(args.out, index=False)

    summary = p.groupby(["RESOURCE_ID","HIST_4000_STATE"]).size().rename("count").reset_index()
    summary.to_csv(Path(args.out).with_name(Path(args.out).stem + "_SUMMARY.csv"), index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
