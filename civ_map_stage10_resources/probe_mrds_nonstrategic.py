#!/usr/bin/env python3
"""
Probe USGS MRDS commodity labels for Civ non-strategic mineral resources.
This is a source audit only.
"""
from __future__ import annotations
import argparse,zipfile,re,json
from pathlib import Path
import pandas as pd

GROUPS={
 "COPPER":["copper"],
 "GOLD":["gold"],
 "SILVER":["silver"],
 "SALT":["salt","halite"],
 "MARBLE":["marble"],
 "STONE":["stone","limestone","granite","sandstone","basalt","dimension stone"],
 "GEMS":["diamond","emerald","ruby","sapphire","opal","topaz","tourmaline","garnet","aquamarine","beryl","amethyst","gemstone"],
 "AMBER":["amber"],
 "JADE":["jade","jadeite","nephrite"],
 "LAPIS_LAZULI":["lapis","lazuli"],
}

def norm(s): return s.fillna("").astype(str).str.lower().str.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--prefix",default="CIV_STAGE10P_MRDS_NONSTRATEGIC_PROBE")
    a=ap.parse_args()

    z=zipfile.ZipFile(a.zip)
    member=max((n for n in z.namelist() if n.lower().endswith(".csv")),
               key=lambda n:z.getinfo(n).file_size)
    with z.open(member) as f:
        df=pd.read_csv(f,low_memory=False,encoding_errors="replace")

    for c in ["commod1","commod2","commod3"]:
        if c not in df.columns: raise RuntimeError(f"missing {c}")
        df[c+"_N"]=norm(df[c])
    lat=pd.to_numeric(df.latitude,errors="coerce")
    lon=pd.to_numeric(df.longitude,errors="coerce")
    valid=lat.between(-90,90)&lon.between(-180,180)

    rows=[]; samples=[]
    for group,keys in GROUPS.items():
        pat="|".join(re.escape(k) for k in keys)
        per=[]
        union=pd.Series(False,index=df.index)
        for c in ["commod1_N","commod2_N","commod3_N"]:
            m=df[c].str.contains(pat,regex=True,na=False)&valid
            per.append(int(m.sum())); union|=m
        raw=pd.concat([df.loc[union,["commod1","commod2","commod3"]]],ignore_index=True)
        vals=pd.concat([raw.commod1,raw.commod2,raw.commod3]).dropna().astype(str)
        vals=vals[vals.str.lower().str.contains(pat,regex=True,na=False)]
        top=vals.value_counts().head(30).to_dict()
        coords=pd.DataFrame({"lat":lat[union].round(5),"lon":lon[union].round(5)})
        rows.append({
          "group":group,
          "primary":per[0],"secondary":per[1],"tertiary":per[2],
          "records_any":int(union.sum()),
          "unique_coords":int(len(coords.drop_duplicates())),
          "top_matching_labels":json.dumps(top,ensure_ascii=False),
        })
        if union.any():
            s=df.loc[union,["latitude","longitude","commod1","commod2","commod3"]].copy()
            s.insert(0,"GROUP",group)
            samples.append(s.head(200))

    out=pd.DataFrame(rows)
    out.to_csv(a.prefix+"_COUNTS.csv",index=False)
    if samples: pd.concat(samples,ignore_index=True).to_csv(a.prefix+"_SAMPLES.csv",index=False)
    summary={
      "source":"USGS MRDS bulk CSV",
      "archive_member":member,
      "rows":int(len(df)),
      "groups":rows,
    }
    Path(a.prefix+"_SUMMARY.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(out.to_string(index=False))

if __name__=="__main__":main()
