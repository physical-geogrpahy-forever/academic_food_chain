# Final Air Combat and GDR Rules V1 QA

Date: 2026-09-21
Status: **PASS — current repository structural validation**

Authorities:
- `city_system/FINAL_GDR_MODULE_BALANCE_V1.csv`
- `city_system/FINAL_AIR_INTERCEPTION_UNIT_RULES_V1.csv`
- `city_system/FINAL_AIR_COMBAT_GLOBAL_RULES_V1.csv`
- `city_system/FINAL_AIR_COMBAT_AND_GDR_RULES_V1.md`
- `city_system/validate_final_air_gdr_rules_v1.py`

Current result:
- GDR module rows: 6
- air-unit rule rows: 10
- global air-combat rules: 15
- GDR ordinary promotion profile: NONE
- missing required GDR innate rules: 0
- GDR module value mismatches: 0
- interceptor chance/range mismatches: 0
- Stealth Bomber / Guided Missile evasion mismatches: 0
- result: **PASS**

Locked GDR module values:
- Advanced AI -> AA Defense Strength 130
- Advanced Power Cells -> city ranged strength 100 -> 130 and full city-defense effectiveness
- Cybernetics -> Moves 5 -> 8 + Mountain Jump
- Smart Materials -> +10 defense vs land/naval

Locked Civ V air-interception chances:
- Triplane 50%
- Fighter 100%
- Jet Fighter 100%
- Anti-Air Gun 100%
- Mobile SAM 100%
- Destroyer 40%
- Missile Cruiser 100%

Innate 100% evasion:
- Stealth Bomber
- Guided Missile

No GitHub Actions run ID is claimed until an actual completed run is retrieved.
