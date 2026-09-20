# Final Generic Map Improvement / Infrastructure Roster V1 QA

Date: 2026-09-21  
Status: **PASS**

Authority:
- `tile_system/FINAL_GENERIC_MAP_IMPROVEMENT_INFRASTRUCTURE_ROSTER_V1.csv`
- `tile_system/validate_final_generic_map_roster_v1.py`
- workflow: `.github/workflows/civ-final-map-roster-qa.yml`

## GitHub Actions result

- Workflow: **Civ Final Map Roster QA**
- Run ID: **35527902714**
- Head SHA: `efd057e0042e04dd7c832369f5154f5518983cbd`
- Event: push
- Validator job: **success**

Run:
https://github.com/physical-geogrpahy-forever/academic_food_chain/actions/runs/35527902714

## Validator output

```text
map_roster_count=39
technology_master_map_entries=32
civic_or_special_entries=7
duplicate_item_names=0
forbidden_items_present=0
buildable_rows=28
rule_or_special_rows=11
PASS
```

## Structural checks passed

- expected normalized technology map entries: 32/32
- expected civic/special entries: 7/7
- total canonical records: 39
- duplicate ITEM_EN: 0
- duplicate MAP_ITEM_ID: 0
- unknown technology gates: 0
- unknown additional technology gates: 0
- unknown civic gates: 0
- missing map class/record kind: 0
- non-locked status rows: 0
- forbidden/nonbaseline items present: 0
- Canal cross-gate sanity: PASS
- Customs House cross-gate sanity: PASS
- Solar Farm Environmentalism cross-gate sanity: PASS
- Historic Landmark archaeology sanity: PASS
- National Park special-area sanity: PASS

## Explicitly excluded from the canonical baseline

- Citadel
- Trading Post
- Hydro Plant as a separate item
- Aerodrome district
- Preserve district

## Reconciliation correction included

The Ecology master text was synchronized so that both renewable improvements explicitly show the already-locked civic gate:

- Solar Farm -> Ecology + Environmentalism
- Geothermal Plant -> Ecology + Environmentalism

This is a text/gate synchronization with the existing Environmentalism civic decision, not a new design change.
