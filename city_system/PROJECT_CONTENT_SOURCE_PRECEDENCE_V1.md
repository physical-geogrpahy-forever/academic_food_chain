# Project Content Source Precedence V1

Date: 2026-09-21
Status: **AUTHORITATIVE**

This file defines the source-precedence rule for all future balance work.

## Core rule

**Do not treat Civilization V Brave New World as the universal highest-priority source.**

When the project has explicitly adopted content or mechanics from a mod, Civilization VI, or Gathering Storm, that adopted source is authoritative for the affected content unless a later project decision explicitly overrides it.

## Precedence

For each individual content item or mechanic:

1. **Explicit project lock / project adaptation**
2. **The adopted source that actually supplied the content/mechanic**
3. Other adopted source used to reconcile a gap or conflict
4. Civilization V BNW fallback only where the adopted source does not define the relevant value/behavior
5. Minimal project interpolation only if all adopted sources are silent

This is evaluated **per field/effect**, not just per building or unit name.

Example:
- Hospital base production cost may still use Civ V BNW.
- Hospital Health effect must come from the adopted Health & Plague system.
- If the project later decides to reduce the BNW +5 Food to avoid double-growth, that is an explicit project override and must be documented as such.

## Adopted source families that must be checked

### Health & Plague for BNW
Authority for:
- Health yield
- plague risk/spread
- worked-resource Health effects
- building Health effects
- health/plague interaction with trade/roads
- health-sensitive population/growth behavior

Important:
The source mod deliberately minimizes changes to base-game assets for compatibility.
Therefore a vanilla building effect can coexist with added Health.
Never assume Health automatically replaces a BNW Food effect.

### Pouakai Enlightenment Era
Authority for content imported specifically from that mod, including adopted:
- Cloth Mill
- Gunsmith
- Drydock
- Enlightenment-era unit/building concepts and unlock relationships

Do not replace its actual effects with a generic BNW-style interpolation if the source effect is documented.

### Barathor's More Luxuries / project 47-resource roster
Authority for the added luxury-resource set and its placement/resource identity.

Project canonical resource set contains 47 resources:
- 7 strategic
- 10 bonus
- 30 luxury

The added More Luxuries-derived resources in the project include:
- Coffee
- Tea
- Tobacco
- Olives
- Perfume
- Amber
- Jade
- Lapis Lazuli
- Coral

Any resource-sensitive building or improvement audit must use the **project 47-resource roster**, never the vanilla Civ V resource list.

Do not invent building synergies merely because a resource exists.
If More Luxuries itself does not define a building interaction, use either:
- an explicitly adopted companion/rebalance rule, or
- a documented project adaptation.

### Civilization VI / Gathering Storm
Authority for content explicitly imported from Civ VI / Gathering Storm, including:
- Future Era structure
- GDR and Future modules
- Government Plaza building concepts
- district buildings converted to direct city buildings
- Power / climate / renewable-energy concepts
- Gathering Storm space-victory project chain
- GS-derived improvements/infrastructure

District, Governor and Builder-charge dependencies must be translated into the project's Civ V-style direct-building / persistent-Worker system rather than silently copied.

## Mixed-source content

A building can legitimately use different sources for different fields.

Example:
- Factory production cost/effect may use Civ V BNW numeric scale.
- Factory Power/pollution behavior may come from Gathering Storm adaptation.
- Factory Health/Disease externality may come from Health & Plague integration.

The balance table must record these as layered effects instead of pretending one source owns the entire row.

## Forbidden shortcuts

Do not:
- copy BNW Food/Gold/Science values and call the row complete when an adopted system changes the same gameplay domain;
- ignore Coffee/Tea/Tobacco/Olives/etc. when auditing resource-sensitive buildings/improvements;
- replace documented Enlightenment Era effects with arbitrary interpolation;
- use Civ VI district adjacency literally;
- use Governor-only effects when Governors are not in the project;
- use Builder-charge effects when the project uses persistent Workers;
- claim a source-exact value when it is actually project-scaled.

## Required audit labels

Future numeric tables should distinguish:
- SOURCE_EXACT
- SOURCE_ADAPTED
- PROJECT_OVERRIDE
- PROJECT_INTERPOLATED
- SOURCE_REAUDIT_REQUIRED

A row may be numerically locked while one external-system field remains pending, but the pending field must be explicit.

## Immediate consequence

The previously created `FINAL_GENERIC_BUILDING_NUMERIC_BALANCE_V1.csv` is retained as a working baseline, but its claim of universal finality is superseded.

A mod-aware V2 audit must review:
- Health/Disease-sensitive buildings
- Enlightenment Era imports
- resource-sensitive buildings against all 47 project resources
- Civ VI / Gathering Storm imports

BNW-only rows that are unaffected by adopted systems may remain unchanged.
