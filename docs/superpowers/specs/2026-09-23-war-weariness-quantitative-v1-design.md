# War Weariness Quantitative V1 Design

Date: 2026-09-23
Branch: `civ-game-map-stage1b-etopo2022`
Status: WRITTEN SPEC AWAITING USER REVIEW

## 1. Purpose

Quantify the already-adopted War Weariness system so that long wars create visible domestic and military costs without duplicating City Happiness, Occupation, Colonial burden, Health, or State Stability.

The system must support the project's world-scale map, simultaneous multi-front wars, overseas wars, colonial wars and repeated wars. It should preserve the useful Vox Populi idea of opponent-specific war weariness while adapting the final aggregation for a game where a civilization may be fighting several meaningful wars at once.

War Weariness V1 produces three direct outputs:

- `war_weariness_unhappiness` for the existing City Happiness interface
- military unit production and purchase cost modifier
- Military Capacity modifier

State Stability does not receive a direct numerical penalty in this pass. Stability will later read War Weariness and City Happiness as separate inputs so the same burden is not double-counted.

## 2. Existing authorities preserved

This design extends rather than replaces:

- `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`
- `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`
- `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`
- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `city_system/STABILITY_BUILDING_SUPPORT_V1.md`

Vox Populi source structure retained conceptually:

- War Weariness is tracked by opponent rather than as one undifferentiated global counter.
- War duration and war damage contribute to weariness.
- Damage inflicted on the enemy contributes less than damage suffered.
- War Weariness can increase Unhappiness.
- War Weariness can reduce military supply.
- War Weariness can increase military unit costs.
- Peace strongly reduces the burden.
- Liberating cities can reduce the burden.

Relevant VP implementation interfaces include:

- `GetWarWearinessPercent(PlayerTypes ePlayer)`
- `GetHighestWarWearinessPercent()`
- `GetHighestWarWearinessPlayer()`
- `GetSupplyReductionFromWarWeariness()`
- `GetUnitCostIncreaseFromWarWeariness()`
- `GetUnhappinessFromWarWeariness()`

The exact VP numerical formula is not copied. All numerical coefficients below are project-native V1 balance values.

## 3. State representation

Maintain one War Weariness state per opponent:

```text
W_i ∈ [0, 100]
```

where `i` is another civilization or war participant against whom the player has a weariness history.

The state persists after peace until it decays to zero. This is necessary so repeated wars against the same opponent have historical continuity rather than resetting instantly.

Each opponent state should expose at minimum:

- current `W_i`
- whether currently at war
- consecutive current-war turns
- turns since peace
- whether the current war is offensive, defensive, liberation or overseas
- whether this opponent was fought recently enough to trigger repeat-war pressure

## 4. Per-turn weariness accumulation

For an active war against opponent `i`, first compute positive accumulation only:

```text
ΔW_i_raw_positive
=
  Duration
+ CombatLoss
+ EnemyDamage
+ CivilianCityDamage
+ Conscription
+ PositiveStrategicShock
```

Then apply one bounded war-context multiplier and the per-turn gain cap:

```text
ΔW_i_positive
=
clamp(
  ΔW_i_raw_positive × WarContextMultiplier,
  0,
  TurnGainCap
)
```

Relief events are calculated separately:

```text
Relief_i >= 0
```

Final active-war update:

```text
W_i_next
=
clamp(
  W_i + ΔW_i_positive - Relief_i,
  0,
  100
)
```

For V1:

```text
TurnGainCap = 20
```

This separation is mandatory. Negative liberation relief must never disappear merely because positive accumulation is clamped at zero.

A per-turn positive-gain cap prevents one pathological combat event or malformed input from jumping directly from calm to maximum weariness. Relief is not counted against the positive-gain cap because it moves weariness downward.

## 5. Duration term

Short wars should not be punished heavily merely for existing.

```text
if current_war_turns <= 5:
    Duration = 0
else:
    Duration = 0.35
```

The five-turn grace period means a short punitive expedition or quickly resolved defensive war can end with little duration burden. Combat losses and strategic shocks can still generate weariness during those first five turns.

The duration value is deliberately constant after the grace period rather than accelerating quadratically. Attrition is already represented through the damage and loss terms.

## 6. Military damage terms

### 6.1 Own military damage

Define per-turn own military damage value as:

```text
OwnDamageValue
=
Σ(unit_production_cost × hp_lost / max_hp)
```

Destroyed units naturally contribute their remaining lost HP through the same accounting. A unit already damaged before the turn contributes only newly lost HP in the current update.

Normalize by military value at the start of the turn:

```text
OwnDamageRatio
=
OwnDamageValue / max(StartTurnOwnMilitaryValue, MilitaryValueFloor)
```

V1 coefficient:

```text
CombatLoss = 30 × OwnDamageRatio
```

`MilitaryValueFloor` prevents tiny early armies from producing undefined or absurd ratios. V1 uses:

```text
MilitaryValueFloor = 100 production-value units
```

This is a denominator floor, not extra military power.

### 6.2 Damage inflicted on the opponent

The enemy-damage term models the social cost of sustained fighting even during a successful offensive, but at one fifth the weight of losses suffered.

```text
EnemyDamageValue
=
Σ(enemy_unit_production_cost × hp_lost / max_hp)

EnemyDamageRatio
=
EnemyDamageValue / max(StartTurnEnemyMilitaryValue, MilitaryValueFloor)

EnemyDamage = 6 × EnemyDamageRatio
```

This term must never be interpreted as a reward or victory bonus. It is a small additional burden from continued combat activity.

## 7. Civilian and city damage

Civilian and urban losses are handled separately from military HP loss.

V1 event additions before context multiplier:

- civilian unit lost: `+2`
- non-capital city lost: `+10`
- capital lost: `+25` total for the city-loss event, not `+10 + +25`
- city population lost directly to a war event: `+0.5` per population, maximum `+5` per city per turn
- city razed by the opponent: additional `+5`

Capital loss may still coexist with direct wartime population loss or razing because those represent distinct harms. Only the normal city-loss `+10` is replaced by the capital-loss `+25`.

The city-loss values are intentionally large because territorial collapse should create a sharper political shock than routine battlefield attrition.

## 8. Conscription

If a mechanic creates military units through forced or emergency conscription, add:

```text
Conscription = min(5, conscripted_units_this_turn × 1)
```

Ordinary Gold purchase, normal Production and free units from non-conscription effects do not count.

This term should be fed only by mechanics explicitly tagged as conscription or emergency levy.

## 9. Strategic shock and relief

Strategic events are sparse event modifiers, not a generic catch-all.

Positive strategic shocks contributing to `ΔW_i_raw_positive`:

- loss of a designated core city other than the capital: `+4`
- first enemy occupation of the player's original core region in the current war: `+5`

Relief contributing to `Relief_i` after positive accumulation is calculated:

- liberation of one of the player's cities by self or ally: `4`
- liberation of another civilization's city by the player: `8`

Relief is subtracted after the context-adjusted positive gain and then the final opponent weariness state is clamped to `[0,100]`.

Do not create a separate generic 'losing war' flat shock here. Losing status is handled by the war-context multiplier using War Score.

## 10. War-context multiplier

Only one combined multiplier is applied to positive raw per-turn accumulation. Relief is not multiplied.

Base:

```text
1.00
```

Context factors:

| Condition | Factor |
|---|---:|
| homeland defensive war | 0.75 |
| liberation-war objective | 0.85 |
| overseas offensive war | 1.25 |
| repeat war against same opponent | 1.20 |
| clearly winning by War Score | 0.85 |
| clearly losing by War Score | 1.30 |

Definitions:

- `homeland defensive war`: opponent declared or invaded and the player is not currently pursuing a primary offensive war goal outside its pre-war sovereign/recognized territory.
- `liberation-war objective`: the active primary war goal is liberation and the player has not converted the war into territorial annexation beyond liberated/returned territory.
- `overseas offensive war`: the main combat theater is not connected to the player's capital landmass by owned contiguous land and is being prosecuted offensively.
- `repeat war`: a new war against the same opponent begins 30 or fewer turns after the previous peace.
- `clearly winning`: War Score at or above the project's positive threshold.
- `clearly losing`: War Score at or below the symmetric negative threshold.

Final multiplier:

```text
WarContextMultiplier
=
clamp(product_of_active_factors, 0.60, 1.50)
```

Offensive/defensive/liberation classification must be supplied by the diplomacy/war-goal layer. The weariness calculator must not guess intent from unit positions.

## 11. Multi-war empire aggregation

VP's highest-opponent concept is retained as the dominant term, but the project adds partial contribution from secondary wars.

Let all nonzero opponent weariness values be sorted descending:

```text
W_max = max(W_i)
W_secondary = sum(W_i for all other opponents)
```

If there are no nonzero states, `W_empire = 0` and there is no dominant opponent.

Otherwise:

```text
W_empire
=
clamp(
  W_max + 0.20 × W_secondary,
  0,
  100
)
```

Properties:

- one severe war dominates
- several small wars matter
- five simultaneous wars do not simply quintuple the penalty
- inactive historical opponent states can still contribute until they decay to zero

For V1, all nonzero opponent states participate in aggregation, including recently concluded wars. Their contribution falls naturally as peace decay reduces `W_i`.

## 12. Peace and recovery

On a newly signed peace with opponent `i`:

```text
W_i = 0.50 × W_i
```

Apply the halving exactly once per peace transition, never once per peaceful turn.

Additional settlement relief:

```text
if final war result is clearly favorable:
    W_i = max(0, W_i - 10)
```

`clearly favorable` uses the same positive War Score threshold used by the war-context layer at settlement time. Do not stack multiple victory labels for the same treaty.

During each subsequent peaceful turn with that opponent:

```text
W_i_next = max(0, W_i - 4)
```

If war resumes before `W_i` reaches zero, the existing value becomes the starting burden of the new war. The repeat-war context factor also applies when the new declaration occurs 30 or fewer turns after the previous peace.

A city liberation event during war may additionally reduce weariness through `Relief_i` as specified above.

## 13. City Happiness output

War Weariness enters the already-defined City Happiness interface exactly once through:

```text
war_weariness_unhappiness
```

V1 mapping:

```text
war_weariness_unhappiness
=
clamp(
  ceil((W_empire - 10) / 20),
  0,
  5
)
```

Equivalent ranges:

| W_empire | War Weariness Unhappiness |
|---:|---:|
| 0-10 | 0 |
| >10-30 | 1 |
| >30-50 | 2 |
| >50-70 | 3 |
| >70-90 | 4 |
| >90-100 | 5 |

This value is supplied to every city by default as the empire-wide war burden.

Future policies, governments or city-specific effects may modify the city-local received penalty, but V1 does not invent such modifiers.

The War Weariness module does not recalculate City Happiness. It only supplies this named input to `calculate_city_happiness_v1.py`.

## 14. Military unit cost output

War Weariness increases the cost of producing and purchasing new military units.

To avoid programming-language differences in half-value rounding, V1 defines integer rounding explicitly:

```text
military_unit_cost_increase_percent
=
floor(0.75 × W_empire + 0.5)
```

Bound:

```text
0 to 75 percent
```

The modifier applies to:

- military unit Production cost
- military unit Gold purchase cost

It does not apply to civilian units, buildings, Wonders or projects.

Faith-purchased religious units and Great People are not military units for this rule unless an explicit later system overrides that classification.

## 15. Military Capacity output

War Weariness reduces national Military Capacity but does not directly simulate operational logistics.

V1:

```text
military_capacity_reduction_percent
=
floor(0.30 × W_empire + 0.5)
```

Bound:

```text
0 to 30 percent
```

The reduction is applied to the final national Military Capacity after ordinary population/building/policy/technology capacity sources are combined, but before determining whether the player is over capacity.

Operational Supply remains a separate logistics/front-line system.

## 16. No direct State Stability penalty in V1

War Weariness is a future State Stability input, but this module does not output a direct `stability_penalty` number.

Reason:

- War Weariness already lowers City Happiness.
- City Happiness will itself be an input to State Stability.
- A direct Stability penalty assigned here would risk counting the same domestic burden twice before the State Stability equation is designed.

The later State Stability pass may intentionally use both:

- `W_empire` as a direct political-war-stress signal
- aggregate City Happiness as a social satisfaction signal

but their weights must be calibrated together in that later pass.

## 17. Separation from Occupation and Colonial burden

War Weariness does not include:

- occupied-city unrest
- resistance from annexed populations
- colonial administration burden
- overseas territorial distance by itself

The only overseas effect here is the `1.25` context multiplier for an offensive war whose main theater is overseas.

Occupation and Colonial burden remain separate City Happiness inputs and future Stability inputs.

## 18. Required calculator inputs

A pure per-opponent active-war update function should accept at minimum:

- current opponent weariness
- current-war turn count
- own damage value or the raw data necessary to compute it
- start-turn own military value
- enemy damage value or raw data
- start-turn enemy military value
- civilians lost this turn
- city-loss events
- war-related city population loss
- razing events
- conscripted units this turn
- positive strategic-shock events
- relief events
- war-context flags
- War Score state

A separate empire aggregation function should accept all opponent states and return:

- `W_empire`
- dominant opponent identifier, or none if all states are zero
- secondary contribution
- City Happiness penalty
- military unit cost increase percent
- Military Capacity reduction percent

A peace update function should accept:

- current `W_i`
- whether peace was newly signed this update
- whether the state was already peaceful
- favorable-settlement flag

The interface must make one-time events explicit so the same city loss, liberation relief or peace halving cannot be applied twice.

## 19. Error handling

Reject:

- negative weariness
- weariness above 100 as an input state
- negative military values
- non-finite numeric values
- negative unit/city/civilian event counts
- negative current-war turn count
- contradictory mutually exclusive war classifications when they cannot coexist by definition
- malformed opponent-state collections

Allow:

- military value of zero, handled through `MilitaryValueFloor`
- no active wars with residual postwar weariness
- one or many opponent states
- fractional `W_i` and `W_empire` values internally

All final percentages and weariness states are explicitly clamped to their documented ranges.

## 20. Required static QA scenarios

At minimum implementation tests must cover:

1. no wars, all weariness zero
2. first five turns with no combat produces no duration weariness
3. sixth turn adds duration burden
4. 10 percent own military-value damage produces `CombatLoss = 3`
5. same relative enemy damage produces one fifth the own-loss burden
6. homeland defensive multiplier lowers otherwise identical accumulation
7. overseas offensive multiplier raises otherwise identical accumulation
8. repeat-war multiplier activates only at 30 or fewer turns since previous peace
9. combined context multiplier clamps at 0.60 and 1.50
10. one severe war dominates empire aggregation
11. two secondary wars contribute at 20 percent each
12. empire aggregation caps at 100
13. peace halves opponent weariness exactly once
14. favorable peace removes an additional 10 after halving
15. peaceful decay removes 4 per turn without crossing below zero
16. resumed war inherits residual weariness
17. `W_empire <= 10` gives zero City Happiness penalty
18. high weariness reaches but never exceeds 5 City Happiness penalty
19. `W_empire = 100` gives 75 percent military unit cost increase
20. `W_empire = 100` gives 30 percent Military Capacity reduction
21. capital loss uses the capital event value rather than double-counting normal city loss
22. conscription contribution caps at 5 per turn
23. positive per-turn weariness gain caps at 20
24. liberation relief reduces weariness even on a turn with zero positive accumulation and cannot reduce `W_i` below zero
25. NaN and Infinity inputs are rejected
26. no nonzero opponent states returns `W_empire=0` and no dominant opponent
27. half-value military-effect rounding follows the explicit `floor(x + 0.5)` rule

These are pre-runtime arithmetic tests. They are not autoplay or actual game telemetry.

## 21. Expected implementation artifacts

After the written design and implementation plan are approved, implementation should create:

- `city_system/WAR_WEARINESS_NUMERIC_RULES_V1.csv`
- `city_system/calculate_war_weariness_v1.py`
- `city_system/test_calculate_war_weariness_v1.py`
- `city_system/generate_war_weariness_static_qa_v1.py`
- `city_system/WAR_WEARINESS_STATIC_QA_V1.md`
- `city_system/WAR_WEARINESS_QUANTITATIVE_V1.md`
- `.github/workflows/war-weariness-qa.yml`

The implementation should update the relevant VP system implementation index only after the full static suite passes.

## 22. Authority order after implementation

For War Weariness conflicts after implementation, use:

1. future `city_system/WAR_WEARINESS_QUANTITATIVE_V1.md`
2. future `city_system/WAR_WEARINESS_NUMERIC_RULES_V1.csv`
3. future `city_system/calculate_war_weariness_v1.py`
4. `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md` for how the resulting city penalty is consumed
5. `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`
6. `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`

## 23. Final design verdict

War Weariness V1 is an opponent-specific persistent 0-100 burden with project-native accumulation and recovery rules.

The design keeps the VP principle that one major war should dominate while adding a bounded 20 percent contribution from secondary wars for world-scale multi-front conflict. Military losses are normalized by current military value, short wars receive a five-turn duration grace period, overseas and repeated offensive wars are more tiring, and peace creates strong but non-instant recovery.

The system exports exactly three direct gameplay effects in V1: City Happiness penalty, military unit cost increase and Military Capacity reduction. It deliberately does not directly reduce State Stability, Occupation Happiness or Colonial Happiness in order to preserve clean system boundaries and prevent double counting.
