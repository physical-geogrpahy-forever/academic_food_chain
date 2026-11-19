#!/usr/bin/env python3
"""Read-only full tracked-file integrity audit + authoritative Civ cross-file QA."""
import collections
import csv
import io
import json
import pathlib
import re
import subprocess
import sys
import traceback
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit-output"
ERRORS, WARNINGS, STATS, VALIDATORS = [], [], {}, []
TEXT_EXT = {".py", ".csv", ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".svg", ".geojson"}
SKIP_EXT = {".pyc"}
VALIDATE = [
    "city_system/test_build_final_building_master_v1.py",
    "city_system/test_calculate_city_happiness_v1.py",
    "city_system/test_validate_cross_system_v1.py",
    "city_system/test_validate_final_building_master_v1.py",
    "city_system/test_validate_happiness_building_links_v1.py",
    "city_system/validate_cross_system_v1.py",
    "city_system/validate_final_air_gdr_rules_v1.py",
    "city_system/validate_final_building_master_v1.py",
    "city_system/validate_final_generic_building_numeric_balance_v1.py",
    "city_system/validate_final_generic_unit_roster_v1.py",
    "city_system/validate_final_unit_numeric_balance_v1.py",
    "city_system/validate_final_unit_operational_rules_v1.py",
    "city_system/validate_final_unit_promotion_ability_v1.py",
    "city_system/validate_final_unit_upgrade_graph_v1.py",
    "city_system/validate_happiness_building_links_v1.py",
    "city_system/validate_settler_progression_v1.py",
    "city_system/validate_standard_speed_pre_autoplay_v1.py",
    "civics_reference/validate_civic_tech_crosslinks_v1.py",
    "civics_reference/validate_civic_tree_historical_v3.py",
    "tech_reference/validate_gathering_storm_future_era_v1.py",
    "tech_reference/validate_technology_tree_historical_v2.py",
    "tile_system/validate_final_generic_map_numeric_balance_v1.py",
    "tile_system/validate_final_generic_map_roster_v1.py",
    "tools/validate_europe_classification_v1.py",
]

def fail(msg):
    ERRORS.append(msg)

def warn(msg):
    WARNINGS.append(msg)

def check(cond, msg):
    if not cond:
        fail(msg)

def csvrows(path):
    p = ROOT / path
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def names(rows, key):
    return [r[key].strip() for r in rows]

def uniqueness(rows, key, label):
    v = names(rows, key)
    bad = [x for x, n in collections.Counter(v).items() if n > 1]
    if bad:
        fail(f"{label}: duplicate {key}: {bad[:15]}")
    if "" in v:
        fail(f"{label}: empty {key}")
    return set(v)

def same(a, b, label):
    if a != b:
        fail(f"{label}: only-left={sorted(a-b)[:15]}, only-right={sorted(b-a)[:15]}")

def gates(rows, col, canonical, label, extra=()):
    missing = []
    for r in rows:
        for g in str(r.get(col, "")).split(";"):
            g = g.strip()
            if g and g not in canonical and g not in extra:
                missing.append((r.get("UNIT_EN") or r.get("BUILDING_EN") or r.get("ITEM_EN"), g))
    if missing:
        fail(f"{label} {col}: unresolved {len(missing)} gates; sample {missing[:12]}")

def graph(rows, key, prereq, label):
    d = {r[key]: r for r in rows}
    adj = {}
    for name, row in d.items():
        parts = [v.strip() for v in row[prereq].split(";") if v.strip()]
        adj[name] = parts
        for p in parts:
            if p not in d:
                fail(f"{label}: missing predecessor {p} for {name}")
            elif int(d[p]["ERA_INDEX"]) > int(row["ERA_INDEX"]):
                fail(f"{label}: future-era predecessor {p} -> {name}")
    state, cycles = {}, []
    def dfs(node):
        if state.get(node) == 1:
            cycles.append(node)
            return
        if state.get(node) == 2:
            return
        state[node] = 1
        for p in adj[node]:
            if p in d:
                dfs(p)
        state[node] = 2
    for n in d:
        dfs(n)
    if cycles:
        fail(f"{label}: cycle {cycles[:12]}")
    STATS[label+"_nodes"] = len(d)
    STATS[label+"_roots"] = [n for n, prereqs in adj.items() if not prereqs]

def markdown_roster(subdir, prefix, count):
    root = ROOT / "city_system" / subdir
    expected = ["ANCIENT", "CLASSICAL", "LATE_ANTIQUITY", "EARLY_MEDIEVAL", "HIGH_MEDIEVAL", "RENAISSANCE", "EXPLORATION", "ENLIGHTENMENT", "INDUSTRIAL", "MODERN", "ATOMIC", "INFORMATION"]
    result = []
    per_era = {}
    for era in expected:
        name = f"{prefix}_{era}_V1.md"
        p = root / name
        s = p.read_text(encoding="utf-8-sig")
        people = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", s, flags=re.M)
        people = [x.strip() for x in people]
        per_era[era] = len(people)
        result.extend(people)
    check(len(result) == count, f"{subdir}: {count} expected people, got {len(result)}")
    duplicated = [x for x, n in collections.Counter(result).items() if n > 1]
    if duplicated:
        fail(f"{subdir}: duplicate persons {duplicated[:15]}")
    STATS[subdir] = {"count": len(result), "per_era": per_era, "duplicates": duplicated}
    return result

def audit_tracked_files():
    p = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    paths = [pathlib.Path(s.decode("utf-8")) for s in p.stdout.split(b"\x00") if s]
    extcounts = collections.Counter()
    bytes_scanned = 0
    files_text = 0
    csv_data_rows = 0
    for rel in paths:
        name = str(rel).replace("\\", "/")
        ext = rel.suffix.lower()
        extcounts[ext or "<no extension>"] += 1
        full = ROOT / rel
        if not full.is_file():
            fail(f"tracked file absent: {name}")
            continue
        data = full.read_bytes()
        bytes_scanned += len(data)
        if ext in SKIP_EXT:
            continue
        if ext not in TEXT_EXT:
            warn(f"unknown extension not parsed: {name}")
            continue
        files_text += 1
        try:
            text = data.decode("utf-8-sig")
            if "\x00" in text:
                fail(f"NUL found in text file: {name}")
            if ext == ".py":
                compile(text, name, "exec")
            elif ext in {".json", ".geojson"}:
                json.loads(text)
            elif ext == ".svg":
                ET.fromstring(text)
            elif ext in {".yml", ".yaml"}:
                import yaml
                yaml.safe_load(text)
            elif ext == ".csv":
                rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
                nonempty = [row for row in rows if row]
                if nonempty:
                    width = len(nonempty[0])
                    bad = [i + 1 for i, row in enumerate(nonempty[1:], 1) if len(row) != width]
                    if bad:
                        fail(f"csv inconsistent columns: {name}; header {width}, rows {bad[:12]}")
                    csv_data_rows += len(nonempty) - 1
        except Exception as ex:
            fail(f"parse/decode failed {name}: {type(ex).__name__} {ex}")
    STATS["tracked_files"] = len(paths)
    STATS["parsed_text_files"] = files_text
    STATS["bytes_scanned"] = bytes_scanned
    STATS["total_csv_data_rows_all_files"] = csv_data_rows
    STATS["extension_counts"] = dict(sorted(extcounts.items()))
    STATS["binary_and_unparsed_files"] = len(paths) - files_text

def audit_authorities():
    tr = csvrows("tech_reference/technology_roster_locked_v2.csv")
    tt = csvrows("tech_reference/technology_tree_historical_v2.csv")
    tm = csvrows("tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv")
    cr = csvrows("civics_reference/civic_roster_locked_v1.csv")
    ct = csvrows("civics_reference/civic_tree_historical_v3.csv")
    cm = csvrows("civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv")
    pc = csvrows("civics_reference/FINAL_POLICY_CARD_ROSTER_V1.csv")
    un = csvrows("city_system/FINAL_GENERIC_UNIT_ROSTER_V1.csv")
    br = csvrows("city_system/FINAL_GENERIC_BUILDING_ROSTER_V1.csv")
    bo = csvrows("city_system/FINAL_GENERIC_BUILDING_ROSTER_V3_OVERRIDE.csv")
    bm = csvrows("city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv")
    mp = csvrows("tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv")
    founder = csvrows("corporations/signature_corporate_founder_roster_v1.csv")
    sector = csvrows("corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.csv")
    placement = csvrows("civ_map_stage10_resources/resource_fix_v1/CIV_GAME_MAP_STAGE10Y_RESOURCE_PLACEMENT_PREVIEW_PLACED_FIXED_V1.csv")

    tech = uniqueness(tr,"TECH_EN","technology roster")
    civ = uniqueness(ct,"CIVIC_EN","civic tree")
    same(tech, uniqueness(tt,"TECH","technology tree"),"technology roster↔tree")
    same(tech, uniqueness(tm,"TECH_EN","technology unlock master"),"technology roster↔unlocks")
    same(civ, uniqueness(cm,"CIVIC_EN","civic unlock master"),"civic tree↔unlocks")
    count_by_era = {r["ERA"]: int(r["COUNT"]) for r in cr if r["ERA"] != "TOTAL"}
    check(sum(count_by_era.values()) == 72, "civic era aggregate must total 72")
    check(len(ct) == 72, "civic tree count 72")
    if any(sum(1 for r in ct if r["PROJECT_ERA"] == era) != count for era, count in count_by_era.items()):
        fail("civic era aggregates do not match civic tree era counts")
    graph(tt, "TECH", "PREREQUISITES_AND", "technology DAG")
    graph(ct, "CIVIC_EN", "SOCIAL_PREREQUISITES_AND", "civic DAG")
    check(len(pc) == 127, "policy cards count !=127")
    uniqueness(pc, "POLICY_EN", "policy cards")
    check(len(un) == 89, "units count !=89")
    uniqueness(un, "UNIT_ID", "unit roster")
    check(len(br) == 102, "base buildings count !=102")
    check(len(bo) == 2, "building V3 override rows !=2")
    check(len(bm) == 104, "building master count !=104")
    uniqueness(bm, "BUILDING_EN", "building master")
    same(set(names(bm,"BUILDING_EN")),set(names(br,"BUILDING_EN")) | {r["BUILDING_EN"] for r in bo if r["ACTION"] == "ADD"}, "buildings base+override↔master")
    check(len(mp) == 39, "map item count !=39")
    uniqueness(mp, "MAP_ITEM_ID", "map items")
    for label, rows in [("units",un),("buildings",br),("building overrides",bo),("map items",mp)]:
        gates(rows,"TECH_GATE",tech,label)
        gates(rows,"ADDITIONAL_TECH_GATE",tech,label)
        gates(rows,"CIVIC_GATE",civ,label,extra={"Tier-2 government adoption","Tier-3 government adoption"})
    for r in pc:
        if r["CIVIC_EN"] not in civ:
            fail(f"policy {r['POLICY_EN']}: unknown civic {r['CIVIC_EN']}")

    check(len(founder) == 98, "signature founders count !=98")
    uniqueness(founder,"FOUNDER","signature founder")
    check(len(sector) == 32, "sectors count !=32")
    sector_ids = uniqueness(sector,"SECTOR_ID","corporation sectors")
    gates(founder,"TECH_GATE",tech,"founder")
    gates(founder,"CIVIC_GATE",civ,"founder")
    for r in founder:
        if r["CANONICAL_SECTOR_ID"] not in sector_ids:
            fail(f"founder {r['FOUNDER']}: unknown sector {r['CANONICAL_SECTOR_ID']}")
    discrepancy=[]
    for r in sector:
        actual = sum(1 for f in founder if f["CANONICAL_SECTOR_ID"] == r["SECTOR_ID"])
        if int(r["FOUNDER_COUNT"]) != actual:
            discrepancy.append({"sector":r["SECTOR_ID"],"claimed":int(r["FOUNDER_COUNT"]),"playable_roster":actual,"claimed_names":r["FOUNDERS"]})
    if discrepancy:
        warn(f"sector founder-count semantics differ from 98-person playable roster: {discrepancy}")
    STATS["sector_founder_discrepancies"] = discrepancy

    check(len(placement)==12500, "resource placement count !=12500")
    uniqueness(placement, "id", "resource placement")
    resources = {r["RESOURCE_ID"] for r in placement}
    check(len(resources) == 47,"resource placement unique types !=47")
    classes = collections.Counter(r["RESOURCE_CLASS"] for r in placement)
    check(set(classes)=={"strategic","bonus","luxury"},"resource category has unexpected values")
    for r in placement:
        try:
            check(float(r["RESOURCE_QTY"]) > 0, f"nonpositive resource quantity {r['id']}")
            check(float(r["RESOURCE_STRENGTH"]) >= 0, f"negative resource strength {r['id']}")
        except ValueError:
            fail(f"non-numeric resource value {r['id']}")

    scientists = markdown_roster("great_scientists","GREAT_SCIENTIST",319)
    phils = markdown_roster("great_philosophers","GREAT_PHILOSOPHER",220)
    scientific_summary = (ROOT/"city_system/great_scientists/GREAT_SCIENTIST_CURRENT_SUMMARY.md").read_text(encoding="utf-8-sig")
    science_names = [x.strip() for x in re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", scientific_summary, flags=re.M)]
    same(set(scientists),set(science_names),"scientist per-era roster↔current summary")
    check(len(science_names)==319,"scientist summary count !=319")
    workstate = (ROOT/"city_system/great_scientists/WORK_STATE.md").read_text(encoding="utf-8")
    if "332 unique people" in workstate:
        warn("scientist WORK_STATE.md stale 332 vs active 319")
    philsummary = (ROOT/"city_system/great_philosophers/GREAT_PHILOSOPHER_CURRENT_SUMMARY.md").read_text(encoding="utf-8")
    if "227" in philsummary:
        warn("philosopher CURRENT_SUMMARY.md stale 227 vs active 220")

    STATS["canonical_counts"] = {
        "technologies":len(tech),"civics":len(civ),"policies":len(pc),"units":len(un),
        "buildings":len(bm),"map_items":len(mp),"signature_founders":len(founder),
        "sectors":len(sector),"resource_rows":len(placement),"resource_types":len(resources),
        "scientists":len(scientists),"philosophers":len(phils),
    }

def run_existing_validators():
    for script in VALIDATE:
        target = ROOT/script
        if not target.is_file():
            fail(f"validator script missing: {script}")
            continue
        try:
            p = subprocess.run([sys.executable,script],cwd=ROOT,capture_output=True,text=True,timeout=120)
            msg = ((p.stdout or "")+"\n"+(p.stderr or "")).strip()
            VALIDATORS.append({"script":script,"returncode":p.returncode,"output_tail":msg[-1300:]})
            if p.returncode:
                fail(f"validator failed {script}: {msg[-450:]}")
        except Exception as exc:
            VALIDATORS.append({"script":script,"exception":str(exc)})
            fail(f"validator error {script}: {exc}")

def write_reports():
    AUDIT_DIR.mkdir(parents=True,exist_ok=True)
    result = {"status":"PASS" if not ERRORS else "FAIL","stats":STATS,"errors":ERRORS,"warnings":WARNINGS,"validators":VALIDATORS}
    (AUDIT_DIR/"full_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    lines = ["# Civ project full tracked-file + authority audit","",
        f"- Status: **{result['status']}**",f"- Tracked files: {STATS.get('tracked_files')}",
        f"- Text files parsed: {STATS.get('parsed_text_files')}",
        f"- Bytes scanned: {STATS.get('bytes_scanned')}",
        f"- Existing validator executions: {len(VALIDATORS)}",
        f"- Errors: {len(ERRORS)}",f"- Warnings: {len(WARNINGS)}","","## Canonical counts",""]
    for k,v in STATS.get("canonical_counts",{}).items():
        lines.append(f"- {k}: {v}")
    for label,seq in [("Errors",ERRORS),("Warnings",WARNINGS)]:
        lines.extend(["",f"## {label}",""])
        lines.extend(f"- {item}" for item in seq[:100])
    lines.extend(["","## Validator runs",""])
    for r in VALIDATORS:
        lines.append(f"- {'PASS' if r.get('returncode')==0 else 'FAIL'} — {r['script']} : {r.get('output_tail','')[-120:].replace(chr(10),' | ')}")
    (AUDIT_DIR/"full_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("AUDIT_STATUS",result["status"],"TRACKED",STATS.get("tracked_files"),"CHECKED",STATS.get("parsed_text_files"),"ERRORS",len(ERRORS),"WARNINGS",len(WARNINGS),"VALIDATORS",len(VALIDATORS))
    for x in ERRORS[:25]:
        print("ERROR:",x)
    for x in WARNINGS[:15]:
        print("WARNING:",x)

if __name__ == "__main__":
    try:
        audit_tracked_files()
        audit_authorities()
        run_existing_validators()
    except Exception as exc:
        fail(f"unhandled audit error: {type(exc).__name__}: {exc}")
        traceback.print_exc()
    finally:
        write_reports()
    sys.exit(1 if ERRORS else 0)
