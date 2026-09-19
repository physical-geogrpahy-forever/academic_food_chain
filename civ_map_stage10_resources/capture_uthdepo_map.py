#!/usr/bin/env python3
"""
Capture the IAEA UThDEPO map payload from its Blazor Server WebSocket.

The public map sends a large initializeMap JS invocation containing a JSON
string with depositMapDtos. This script stores that payload as ordinary JSON
without attempting to automate spreadsheet downloads.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

def extract_outer_json(payload: bytes):
    marker=b"initializeMap"
    if marker not in payload or b"depositMapDtos" not in payload:
        return None
    # The JS interop argument is a one-element JSON array whose element itself
    # is an escaped JSON string: ["{\u0022commodityId...}"].
    start=payload.find(b'["{', payload.find(marker))
    if start < 0:
        return None
    end=payload.rfind(b'}"]')
    if end < start:
        return None
    outer=payload[start:end+3].decode("utf-8","strict")
    wrapped=json.loads(outer)
    if not isinstance(wrapped,list) or not wrapped:
        return None
    inner=wrapped[0]
    obj=json.loads(inner)
    if not isinstance(obj,dict) or "depositMapDtos" not in obj:
        return None
    return obj

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default="https://infcis.iaea.org/UTHDEPO/Deposits/Map")
    ap.add_argument("--out",default="UTHDEPO_MAP_DATA.json")
    ap.add_argument("--summary",default="UTHDEPO_MAP_DATA_SUMMARY.json")
    a=ap.parse_args()

    captured={"obj":None,"frame_bytes":0}

    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        ctx=browser.new_context()
        page=ctx.new_page()

        def on_ws(ws):
            def recv(payload):
                if captured["obj"] is not None or not isinstance(payload,(bytes,bytearray)):
                    return
                try:
                    obj=extract_outer_json(bytes(payload))
                except Exception:
                    obj=None
                if obj is not None:
                    captured["obj"]=obj
                    captured["frame_bytes"]=len(payload)
            ws.on("framereceived",recv)

        page.on("websocket",on_ws)
        page.goto(a.url,wait_until="domcontentloaded",timeout=60000)
        for _ in range(90):
            if captured["obj"] is not None:
                break
            page.wait_for_timeout(1000)
        browser.close()

    obj=captured["obj"]
    if obj is None:
        raise RuntimeError("initializeMap depositMapDtos payload not captured")

    deps=obj.get("depositMapDtos",[])
    Path(a.out).write_text(json.dumps(obj,ensure_ascii=False),encoding="utf-8")

    commodity={}
    ranges={}
    valid=0
    for d in deps:
        k=str(d.get("commodityId"))
        commodity[k]=commodity.get(k,0)+1
        rr=str(d.get("resourceRange") or "")
        ranges[rr]=ranges.get(rr,0)+1
        try:
            lat=float(d["latitude"]); lon=float(d["longitude"])
            if -90<=lat<=90 and -180<=lon<=180:
                valid+=1
        except Exception:
            pass

    summary={
        "source":"IAEA UThDEPO public map",
        "url":a.url,
        "websocket_frame_bytes":captured["frame_bytes"],
        "commodityId":obj.get("commodityId"),
        "deposit_count":len(deps),
        "valid_coordinate_count":valid,
        "commodity_id_counts":commodity,
        "resource_range_counts":dict(sorted(ranges.items(),key=lambda kv:(kv[0]=="",kv[0]))),
    }
    Path(a.summary).write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
