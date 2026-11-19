#!/usr/bin/env python3
"""Read-only check: all 116 source Europe lineages classified exactly once."""
from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EUROPE = ROOT / "civilizations"
SRC = EUROPE / "EUROPE_FULL_ERA_MATRIX_DRAFT_20261118.csv"
TGT = EUROPE / "EUROPE_116_LINEAGES_PLAYABILITY_TRIAGE_V1.csv"
ERAS = ["고대","고전","후기 고대","중세 초기","중세 성기","르네상스","탐험","계몽","산업","현대","원자력","정보화","미래"]

def load(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        rows = list(reader)
        assert not None in reader.fieldnames, f"invalid blank field name in {path}"
        assert all(None not in row for row in rows), f"unexpected overflow columns in {path}"
        return list(reader.fieldnames), rows

srcfields, source = load(SRC)
dstfields, triage = load(TGT)
assert srcfields == ["계보"]+ERAS, f"source era-header mismatch {srcfields}"
expected = ["SOURCE_ROW","LINEAGE","TIER","TIER_LABEL","ENTITY_KIND","REGION_GROUP",
            "FIRST_ERA_IN_MATRIX","LAST_ERA_IN_MATRIX","FILLED_ERA_COUNT",
            "CROSS_REGION_OR_MULTINATIONAL","OVERLAP_NOTE","REVIEW_URGENCY",
            "PROPOSED_GAME_ROLE","SOURCE_EXCERPT","USER_APPROVAL_STATUS"]
assert dstfields == expected, f"triage header mismatch {dstfields}"
assert len(source) == len(triage) == 116, f"row count: source={len(source)} triage={len(triage)}"
counts = Counter(x["TIER"] for x in triage)
assert counts == {"A": 41, "B": 59, "C": 16}, f"unexpected classification totals {counts}"
assert len({x["계보"] for x in source}) == 116, "duplicate source lineage"
assert len({x["LINEAGE"] for x in triage}) == 116, "duplicate target lineage"
assert all(x["USER_APPROVAL_STATUS"] == "PROPOSED_NOT_USER_LOCKED" for x in triage), "unexpected user-approval status"
urgent = Counter(x["REVIEW_URGENCY"] for x in triage)
assert urgent == {"HIGH": 22, "NORMAL": 94}, f"unexpected urgency totals {urgent}"
for index, (original, derived) in enumerate(zip(source, triage), start=2):
    assert derived["SOURCE_ROW"] == str(index), f"source row index mismatch at {index}"
    assert derived["LINEAGE"] == original["계보"], f"source name mismatch at {index}"
    assert derived["ENTITY_KIND"].strip(), f"empty entity kind {index}"
    assert derived["REGION_GROUP"].strip(), f"empty region {index}"
    assert derived["OVERLAP_NOTE"].strip(), f"empty overlap review {index}"
    assert derived["CROSS_REGION_OR_MULTINATIONAL"] in {"YES","NO"}, f"invalid cross-region {index}"
    populated = [era for era in ERAS if original[era].strip()]
    assert populated, f"source without any era entries: {index}"
    assert derived["FIRST_ERA_IN_MATRIX"] == populated[0], f"first-era mismatch {index}"
    assert derived["LAST_ERA_IN_MATRIX"] == populated[-1], f"last-era mismatch {index}"
    assert int(derived["FILLED_ERA_COUNT"]) == len(populated), f"era count mismatch {index}"
    assert derived["SOURCE_EXCERPT"] == original[populated[0]][:140], f"source excerpt changed {index}"
    assert derived["PROPOSED_GAME_ROLE"].strip(), f"missing role {index}"

print("PASS: 116 lineage rows mapped one-to-one (A=41 B=59 C=16); no missing, duplicate or user-locked entries; HIGH=22")
