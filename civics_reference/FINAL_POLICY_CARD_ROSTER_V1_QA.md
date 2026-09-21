# Final Policy Card Roster V1 QA

Date: 2026-09-21
Status: **PASS**

## Coverage

- Final policy cards: **127**
- Policy names duplicated: **0**
- Missing policy slots: **0**
- Missing final effects: **0**
- Numeric status other than `LOCKED_V1`: **0**

## Era counts

- Ancient: 17
- Classical: 8
- Late Antiquity: 7
- Early Medieval: 7
- High Medieval: 8
- Renaissance: 8
- Exploration: 9
- Enlightenment: 9
- Industrial: 14
- Modern: 14
- Atomic: 12
- Information: 6
- Future: 8

## Slot counts

- Military: 35
- Economic: 46
- Wildcard: 26
- Diplomatic: 20

Total: **127**

## Structural rules applied

- Civ V first, then historical/functional reconciliation, then Civ VI fallback.
- Civ VI district conditions are translated into Civ V-style building-chain conditions.
- Builder-charge effects are translated to persistent Worker effects.
- Governor-dependent effects are removed or adapted because baseline Governors are not adopted.
- Giant Death Robot is restored to baseline; Gathering Storm GDR-linked policy clauses may apply to the baseline unit where appropriate.
- Policy ownership is unique: each final policy has one civic owner.
- Exact policy effects are locked in `FINAL_POLICY_CARD_ROSTER_V1.csv`.

## Era effect files

- `policy_balance/ANCIENT_POLICY_EFFECTS_V1.csv`
- `policy_balance/CLASSICAL_POLICY_EFFECTS_V1.csv`
- `policy_balance/LATE_ANTIQUITY_POLICY_EFFECTS_V1.csv`
- `policy_balance/EARLY_MEDIEVAL_POLICY_EFFECTS_V1.csv`
- `policy_balance/HIGH_MEDIEVAL_POLICY_EFFECTS_V1.csv`
- `policy_balance/RENAISSANCE_POLICY_EFFECTS_V1.csv`
- `policy_balance/EXPLORATION_POLICY_EFFECTS_V1.csv`
- `policy_balance/ENLIGHTENMENT_POLICY_EFFECTS_V1.csv`
- `policy_balance/INDUSTRIAL_POLICY_EFFECTS_V1.csv`
- `policy_balance/MODERN_POLICY_EFFECTS_V1.csv`
- `policy_balance/ATOMIC_POLICY_EFFECTS_V1.csv`
- `policy_balance/INFORMATION_POLICY_EFFECTS_V1.csv`
- `policy_balance/FUTURE_POLICY_EFFECTS_V1.csv`
