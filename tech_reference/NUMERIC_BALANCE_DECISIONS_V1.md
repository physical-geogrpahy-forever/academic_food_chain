# Numeric Balance Decisions V1

Date: 2026-09-21
Status: **LOCKED FOR CURRENT BASELINE**

This file resolves the remaining 13 deferred numeric/system items from the technology+civic unlock audit.

## Agricultural stacking

Pasture progression is now:

- Horse Collar: **no Pasture Food bonus**
- Fertilizer: **Pasture +1 Food**
- Replaceable Parts: **Pasture +1 Production**
- Robotics: **Pasture +1 Food**

This avoids a three-step early Food stack while preserving distinct industrial and late automation roles.

## Scholarship and bureaucracy

- Papermaking + Recorded History:
  - Paper Workshop +1 Science
  - Paper Workshop +1 Culture
- Block Printing + Written Culture:
  - each Great Work of Writing in a city with Woodblock Printing House +1 Culture
- Algebra + Written Culture:
  - Library +1 Science
  - Scriptorium +1 Science
  - Paper Workshop +1 Science
- Algebra + Code of Laws:
  - Courthouse +1 Gold
  - Market +1 Gold
- Education + Scholasticism:
  - each University +1 Great Scientist Point per turn
- Education + Scientific Revolution:
  - cities with University +10% Science

## Mercenaries

Eligible land combat units purchased in a city with Barracks:
- Gold purchase cost -15%
- +1 Gold maintenance for the first 20 turns

This creates a real contract-recruitment tradeoff rather than a permanent cheap-army exploit.

## Court Culture

Palace gains:
- +1 Great Work of Writing slot
- +1 Great Work of Art slot

## Public Sphere

War legitimacy becomes visible to public opinion:
- justified / Casus Belli wars: diplomatic grievance or reputation penalty -20%
- Surprise / unjustified wars: diplomatic grievance or reputation penalty +20%

## Advanced AI and Information Warfare

With both Advanced AI and Information Warfare:
- offensive Spy mission duration -10%
- enemy Spy detection chance +10%

## Predictive Systems and Synthetic Technocracy

With Predictive Systems researched and Synthetic Technocracy adopted:
- +30% Production toward city projects

This retains the Civ6 Synthetic Technocracy project-production identity.

## Authority

- `tech_reference/NUMERIC_BALANCE_DECISIONS_V1.csv`
