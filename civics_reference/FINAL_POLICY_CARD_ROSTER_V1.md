# Final Policy Card Roster V1

Date: 2026-09-21
Status: **QUALITATIVE POLICY OWNERSHIP LOCKED**

Total final policy cards: **127**
Duplicate policy names: **0**

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

## Source mix

- CIV6: 115
- PROJECT_HISTORICAL: 7
- CIV5: 4
- OTHER: 1

## Source rule

**Civ V first -> historical/functional reconciliation -> Civ VI fallback -> minimal historical invention**

For policy cards specifically:
- direct Civ6 policies are retained when they fit;
- district conditions are translated to Civ V-style city buildings and tile infrastructure;
- Builder-charge effects become Worker construction effects;
- Governor-dependent policies are removed or adapted because baseline Governors are not used;
- obsolete/duplicate policies are not retained twice;
- exact percentages, yields, caps and thresholds remain for the numeric balance pass.

## Final duplicate cleanup

- Praetorium: removed because Governor-dependent.
- Native Conquest: final owner Colonialism, not Exploration.
- Patriotic War: removed because Gathering Storm folds its role into Defense of the Motherland.
- Five-Year Plan: final owner Class Struggle.
- Police State: final owner Totalitarianism.
- Economic Union: final owner Suffrage.
- Lightning Warfare: final owner Totalitarianism.
- Gunboat Diplomacy: one final instance at Ideology.
- Pamphleteering: final owner Public Sphere.

## Authority

`civics_reference/FINAL_POLICY_CARD_ROSTER_V1.csv`


## Gathering Storm Future split

The total remains 127 policy cards.

Policies owned by the six Future-era civics now use the Future era label. Eight policies move from Information to Future:
- Hallyu
- Non-State Actors
- Aerospace Contractors
- Space Tourism
- Integrated Attack Logistics
- Rabblerousing
- Diplomatic Capital
- Global Coalition

Authority:
- `policy_balance/INFORMATION_POLICY_EFFECTS_V1.csv`
- `policy_balance/FUTURE_POLICY_EFFECTS_V1.csv`
