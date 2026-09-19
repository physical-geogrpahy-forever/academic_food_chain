#!/usr/bin/env python3
import requests, json
ARTICLE=28519994
u=f"https://api.figshare.com/v2/articles/{ARTICLE}/files"
r=requests.get(u,timeout=60); r.raise_for_status()
files=r.json()
for f in files:
    print(json.dumps({k:f.get(k) for k in ["id","name","size","download_url","supplied_md5"]},ensure_ascii=False))
