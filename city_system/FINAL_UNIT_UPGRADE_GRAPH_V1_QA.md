# Final Unit Upgrade Graph V1 QA

Date: 2026-09-21  
Status: **PASS — current repository structural validation**

Authority:
- `city_system/FINAL_UNIT_UPGRADE_GRAPH_V1.csv`
- `city_system/validate_final_unit_upgrade_graph_v1.py`

Current validation:
- roster units: 89
- upgrade graph rows: 89
- missing graph rows: 0
- duplicate source-unit rows: 0
- unknown successors: 0
- era-regressing upgrade edges: 0
- directed cycles: 0
- explicit branch-choice rows: 1
- founding-unit production replacements: 3
- GDR successor-unit edge: 0
- result: **PASS**

Locked special checks:
- Settler -> Pioneer -> Colonist -> Urban Planner is production replacement only
- Privateer -> Submarine
- Paratrooper -> XCOM Squad
- Marine terminal
- GDR module upgrades rather than unit successor
- Frigate branch = Ship of the Line / Cruiser

The GitHub Actions workflow is:
`.github/workflows/civ-final-unit-upgrade-graph-qa.yml`

No Actions run ID is claimed here until a completed run is actually retrieved.
