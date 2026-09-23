# Health-Power Cross-System QA V1

Date: 2026-09-23
Status: STATIC CROSS-SYSTEM QA COMPLETE / ONE NUMERIC BRIDGE DEFERRED

Inputs:

- `health_system/HEALTH_AND_PLAGUE_QUANTITATIVE_V1.md`
- `health_system/HEALTH_BUILDING_VALUES_V1.csv`
- `health_system/HEALTH_PLAGUE_NUMERIC_RULES_V1.csv`
- `city_system/POWER_SYSTEM_V1.md`
- `city_system/POWER_DEMAND_BUILDING_V1.csv`
- `city_system/FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V2_VP.csv`

## 1. Direct Health versus Pollution

PASS structurally.

Factory, Coal Power Plant and generic Oil-role Power Plant do not receive an additional hard-coded direct negative Health value in Health V1.

Their intended route is:

`industrial/power source -> Pollution -> city Health penalty`

This avoids applying both direct `-Health` and Pollution-derived `-Health` for the same industrial externality.

### Deferred numeric bridge

Power V1 currently records fuel-source emissions only as classes:

- Coal: HEAVY
- Oil: MODERATE
- Nuclear: MINUSCULE
- renewables: ZERO

Power V1 explicitly did not assign exact local Pollution/CO2 points.

Health V1 already defines:

`Health pollution penalty = -floor(city_pollution / 10)`, capped at -5.

Therefore the formula contract exists, but fossil/nuclear power does not yet inject a numeric city-pollution value into it.

Verdict:

`DEFERRED_POWER_EMISSION_TO_LOCAL_POLLUTION_BRIDGE`

This bridge must be resolved before claiming a full Health-Power runtime balance pass.

## 2. Power demand versus Health buildings

PASS.

Hospital, Sewer, Apothecary and Medical Lab do not receive invented Power loads merely because they are medical buildings.

Food Market does have a Power load of 1 because it comes from the adopted Gathering Storm Power structure.

Thus medical Health progression is not accidentally gated behind electricity unless the source/project building already has a Power role.

## 3. Food Market overlap

WATCH, not an error.

Food Market currently has:

- base Food +4
- Health +1
- Power load 1
- powered Food +2

A healthy Powered city can therefore obtain both the direct Food bonus and an indirect Food contribution through total city Health.

These effects are mechanically distinct:

- direct/powered Food is building output;
- Health-derived Food is a city-state conversion affected by population, water, resources, pollution and plague.

Do not remove either before runtime data exists.

Runtime watch: Industrial urban growth acceleration.

## 4. Hospital overlap

WATCH, not an error.

Hospital currently retains Civ V-style base Food +5 while Health V1 adds Health +4 and plague-duration -1.

A sufficiently healthy city can therefore receive substantial direct Food plus indirect Health-derived Food.

This is intentional source-layer separation, but it is one of the strongest potential growth accelerators in the system.

Do not reduce Hospital Food or Health from static arithmetic alone.

Runtime watch:

- city growth immediately after Hospital completion;
- whether Population -1 Health per citizen naturally absorbs the temporary Health surplus;
- whether Hospital + Sewer together erase the Industrial disease challenge too abruptly.

## 5. Aqueduct duplicate counting

PASS after Health V1 override.

The old building V2 table contains provisional `Aqueduct Health +2` as if it were a flat building value.

Health V1 supersedes that interpretation:

- natural fresh water -> water Health 2
- Aqueduct -> water Health floor 2
- they do not stack

This removes a potential +4 river-city double count.

## 6. International trade double-effect

PASS structurally, runtime watch quantitatively.

International trade affects Health in two different ways:

1. every four active international routes impose -1 Empire Health, capped at -2;
2. an active international trade link from an infected city has plague network multiplier x2.0.

These are not the same event:

- the Empire Health effect is a mild persistent connectivity/crowding cost;
- the transmission multiplier applies only when there is an actual infected source city.

Therefore this is not a literal duplicate penalty.

Runtime watch: highly trade-oriented civilizations during the High Medieval plague peak.

## 7. Dynamic resource system compatibility

PASS.

Health from resources requires the resource copy to be worked locally.

Discovery, contact or trade can reveal/use a resource under the dynamic-resource system, but mere visibility or import does not create automatic Health.

This preserves the existing contact-based resource-discovery rules and prevents global trade networks from creating free city Health.

## 8. Strategic-resource Health tradeoff

WATCH.

The original Health & Plague design explicitly used Coal, Iron and Oil as additive worked Health maluses. Health V1 preserves -1 per worked copy.

For the project this creates a meaningful but potentially strong interaction:

- Iron may impose an early Health cost before the Pollution system is important;
- Coal/Oil can later have both worked-tile Health malus and city Pollution externality from industrial use.

These are different mechanisms: extraction-site local Health versus citywide pollution from consumption.

Autoplay must check whether the combined Coal/Oil burden is excessive.

## 9. Late disease suppression

WATCH.

The late stack can include:

- Sewer +4 Health and x0.75 spontaneous risk
- Hospital +4 Health and duration -1
- Medical Lab +5 Health and duration -2
- Recycling Center +2 Health plus Pollution -25%

This is intentionally powerful but may make post-Modern plague nearly irrelevant before the era multiplier itself declines.

No static nerf is applied. Runtime outbreak frequency will decide.

## Final verdict

Cross-system structure is coherent and no direct duplicate Health/Power bonus or penalty requires immediate removal.

One implementation dependency remains before full runtime integration:

**Power emission class -> numeric local Pollution points.**

All other identified interactions are runtime balance watches rather than structural errors.