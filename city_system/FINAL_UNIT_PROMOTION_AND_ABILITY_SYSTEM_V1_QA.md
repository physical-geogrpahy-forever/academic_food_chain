# Final Unit Promotion and Ability System V1 QA

Date: 2026-09-21
Status: **PASS — current repository structural validation**

Authorities:
- `city_system/FINAL_UNIT_PROMOTION_SYSTEM_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_PROFILE_ASSIGNMENT_V1.csv`
- `city_system/FINAL_UNIT_INNATE_ABILITIES_V1.csv`
- `city_system/FINAL_UNIT_PROMOTION_INHERITANCE_V1.csv`
- `city_system/validate_final_unit_promotion_ability_v1.py`

Current result:
- canonical units: 89
- promotion-profile assignments: 89
- promotion definitions: 70
- innate ability rules: 60
- promotion inheritance rules: 15
- duplicate promotion IDs: 0
- duplicate innate-rule IDs: 0
- unknown target units/roles: 0
- inheritance rules pointing to nonexistent upgrade edges: 0
- result: **PASS**

Promotion profiles after Gathering Storm correction:
- LAND_MELEE: 27
- LAND_RANGED: 13
- RECON: 4
- NAVAL_MELEE: 6
- NAVAL_RANGED: 7
- NAVAL_RAIDER: 2
- CARRIER: 1
- AIR_FIGHTER: 3
- AIR_BOMBER: 3
- NONE: 23

Important locked exception:
- Giant Death Robot -> profile NONE
- GDR cannot gain normal XP/promotions
- GDR uses Future-tech modules only

Privateer remains the other major profile exception:
- canonical role NAVAL_RAIDER
- promotion profile NAVAL_MELEE while it is a surface raider
- on upgrade to Submarine, highest Coastal Raider/Boarding Party rank converts to corresponding Wolfpack rank

No GitHub Actions run ID is claimed until an actual completed run is retrieved.
