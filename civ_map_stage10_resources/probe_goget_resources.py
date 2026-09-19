#!/usr/bin/env python3
"""Stage 10D source audit for Global Energy Monitor GOGET March 2026 field-level data."""
import argparse, json
from pathlib import Path
import pandas as pd

def pick(cols,needles):
    for c in cols:
        lc=c.lower()
        if all(n in lc for n in needles): return c
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10D_GOGET_PROBE")
    a=ap.parse_args()
    df=pd.read_csv(a.csv,low_memory=False,encoding_errors="replace")
    cols=list(df.columns)
    lat=pick(cols,["lat"])
    lon=pick(cols,["lon"])
    fuel=next((c for c in cols if "fuel" in c.lower() or "type" in c.lower() and "field" in c.lower()),None)
    status=next((c for c in cols if c.lower()=="status" or "status" in c.lower()),None)
    name=next((c for c in cols if "unit name" in c.lower() or "field name" in c.lower() or c.lower()=="name"),None)
    country=next((c for c in cols if "country" in c.lower()),None)
    if not lat or not lon: raise SystemExit(f"lat/lon not found: {cols}")
    la=pd.to_numeric(df[lat],errors="coerce")
    lo=pd.to_numeric(df[lon],errors="coerce")
    valid=la.between(-90,90)&lo.between(-180,180)
    summary={
      "source":"Global Energy Monitor Global Oil and Gas Extraction Tracker, March 2026",
      "rows":int(len(df)),
      "columns":cols,
      "latitude_column":lat,"longitude_column":lon,
      "fuel_column":fuel,"status_column":status,"name_column":name,"country_column":country,
      "valid_coordinate_rows":int(valid.sum()),
      "license_note":"Source workbook About sheet states CC BY 4.0.",
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    if fuel:
        df[fuel].value_counts(dropna=False).rename_axis("fuel").reset_index(name="records").to_csv(a.prefix+"_FUEL_COUNTS.csv",index=False)
    else:
        pd.DataFrame().to_csv(a.prefix+"_FUEL_COUNTS.csv",index=False)
    if status:
        df[status].value_counts(dropna=False).rename_axis("status").reset_index(name="records").to_csv(a.prefix+"_STATUS_COUNTS.csv",index=False)
    else:
        pd.DataFrame().to_csv(a.prefix+"_STATUS_COUNTS.csv",index=False)
    keep=[c for c in [name,country,lat,lon,fuel,status] if c]
    df.loc[valid,keep].head(1000).to_csv(a.prefix+"_SAMPLE.csv",index=False)
    print(json.dumps(summary,indent=2))
    if fuel: print("\nFuel counts\n",df[fuel].value_counts(dropna=False).head(30).to_string())
    if status: print("\nStatus counts\n",df[status].value_counts(dropna=False).head(30).to_string())
if __name__=="__main__":main()
