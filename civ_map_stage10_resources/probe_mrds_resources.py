#!/usr/bin/env python3
"""
Stage 10A source audit: inspect USGS MRDS for Civ-style mineral resources.

This is a source audit, not final placement. It reports field names, commodity
tokens, record counts, coordinate validity, and duplicate coordinates for a
transparent mapping decision.
"""
import argparse, json, re, zipfile
from pathlib import Path
import pandas as pd

GROUPS={
 "IRON":[r"\biron\b",r"\bfe\b"],
 "ALUMINUM_BAUXITE":[r"bauxite",r"alumin"],
 "URANIUM":[r"uranium",r"\bu\b"],
 "COAL":[r"\bcoal\b"],
 "GOLD":[r"\bgold\b",r"\bau\b"],
 "SILVER":[r"\bsilver\b",r"\bag\b"],
 "COPPER":[r"\bcopper\b",r"\bcu\b"],
 "SALT":[r"\bsalt\b",r"halite"],
 "MARBLE":[r"marble"],
 "GEMS":[r"diamond",r"gem",r"emerald",r"ruby",r"sapphire"],
}

def detect_cols(df):
    low={c.lower():c for c in df.columns}
    lat=next((low[k] for k in low if k in ["latitude","lat"]),None)
    lon=next((low[k] for k in low if k in ["longitude","long","lon"]),None)
    commodity=[c for c in df.columns if any(x in c.lower() for x in ["commod","material","mineral"])]
    status=[c for c in df.columns if any(x in c.lower() for x in ["dev_stat","status","production"])]
    return lat,lon,commodity,status

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--prefix",default="CIV_GAME_MAP_STAGE10A_MRDS_PROBE")
    a=ap.parse_args()
    z=zipfile.ZipFile(a.zip)
    names=z.namelist()
    csvs=[n for n in names if n.lower().endswith(".csv")]
    if not csvs: raise SystemExit("no CSV in archive")
    name=max(csvs,key=lambda n:z.getinfo(n).file_size)
    with z.open(name) as f:
        df=pd.read_csv(f,low_memory=False,encoding_errors="replace")
    lat,lon,ccols,scols=detect_cols(df)
    if lat is None or lon is None:
        raise SystemExit(f"coordinate columns not detected: {list(df.columns)}")
    latv=pd.to_numeric(df[lat],errors="coerce")
    lonv=pd.to_numeric(df[lon],errors="coerce")
    valid=latv.between(-90,90)&lonv.between(-180,180)
    text=df[ccols].fillna("").astype(str).agg(" | ".join,axis=1) if ccols else pd.Series([""]*len(df))
    text=text.str.lower()

    rows=[]
    matched_union=pd.Series(False,index=df.index)
    for group,pats in GROUPS.items():
        pat="|".join(f"(?:{p})" for p in pats)
        m=text.str.contains(pat,regex=True,na=False)&valid
        matched_union|=m
        coords=pd.DataFrame({"lat":latv[m].round(5),"lon":lonv[m].round(5)})
        rows.append({
          "group":group,
          "records":int(m.sum()),
          "unique_coords":int(len(coords.drop_duplicates())),
          "duplicate_coord_records":int(len(coords)-len(coords.drop_duplicates())),
        })
    counts=pd.DataFrame(rows).sort_values("records",ascending=False)
    counts.to_csv(a.prefix+"_GROUP_COUNTS.csv",index=False)

    # Top raw commodity strings are useful for refining exact mappings.
    top=text[text.ne("")].value_counts().head(300).rename_axis("commodity_text").reset_index(name="records")
    top.to_csv(a.prefix+"_TOP_COMMODITY_STRINGS.csv",index=False)

    sample_cols=[c for c in [lat,lon]+ccols+scols if c]
    sample=df.loc[matched_union,sample_cols].copy()
    sample.insert(0,"ROW_INDEX",sample.index)
    sample.to_csv(a.prefix+"_MATCHED_SAMPLE.csv",index=False)

    summary={
      "source":"USGS Mineral Resources Data System (MRDS) bulk CSV",
      "archive_member":name,
      "rows":int(len(df)),
      "columns":list(df.columns),
      "latitude_column":lat,
      "longitude_column":lon,
      "commodity_columns":ccols,
      "status_columns":scols,
      "valid_coordinate_rows":int(valid.sum()),
      "matched_any_target_group":int(matched_union.sum()),
      "note":"MRDS stopped systematic updating in 2011; use as deposit/occurrence evidence, not as a modern production-weight dataset.",
      "Stage1A_1deg_used":False
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print(counts.to_string(index=False))
    print("\nTop commodity strings:\n",top.head(80).to_string(index=False))

if __name__=="__main__":main()
