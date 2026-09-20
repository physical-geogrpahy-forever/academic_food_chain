# Civilization V BNW -> Civilization VI civic gap crosswalk V1

Date: 2026-09-20
Status: review baseline

## Purpose

Use Civilization V: Brave New World only to fill real gaps left after importing Civilization VI: Gathering Storm.

Locked precedence:
1. Civ VI civic / government / policy card
2. Civ V BNW social-policy concept
3. Civ V BNW technology concept
4. newly invented civic

If a Civ V name or function is already present in Civ VI, Civ VI wins.

## Sources checked

Civ V BNW social-policy trees include Tradition, Liberty, Honor, Piety, Patronage, Commerce, Rationalism, Aesthetics and Exploration. BNW also converts Freedom, Order and Autocracy into ideology systems.

The policy crosswalk includes all 45 regular BNW policy nodes and the 48 BNW ideology-tenet slots.

The technology crosswalk includes all 74 Civ V technologies from Ancient through Future as listed in the CivFanatics technology reference.

## Main result

Applying the Civ VI-priority rule removes almost all apparent "new civic" candidates.

### Strong new civic candidates surviving the comparison

1. **Scholasticism**
   - source: Civ V Patronage policy
   - best project era: High Medieval, 11-13C
   - why it survives: Civ VI has no civic directly representing medieval scholasticism; it is historically distinct from Civil Service, Theology, Guilds and Humanism.
   - proposed role: bridge the Theology/Civil Service intellectual branch toward later Humanism.
   - possible insertion:
     `Theology + Civil Service -> Scholasticism -> Humanism`
   - this would preserve the Civ VI graph's logic while adding one historically useful high-medieval node.

2. **Scientific Revolution**
   - source: Civ V Rationalism policy
   - best project era: Exploration, 16-17C
   - why it survives: Civ VI The Enlightenment is broader and belongs naturally to the project's 18C Enlightenment era. Scientific Revolution is a distinct 16-17C intellectual transformation.
   - proposed insertion:
     `Humanism -> Scientific Revolution -> The Enlightenment`
   - Diplomatic Service can remain the second Civ VI prerequisite for The Enlightenment unless later testing suggests a three-prerequisite node is too restrictive.

These are candidates, not yet committed into the actual civic graph.

## Concepts rejected as new civics because Civ VI already covers them

Examples:

- Monarchy -> Civ VI Divine Right unlocks Monarchy.
- Oligarchy / Republic -> Political Philosophy governments.
- Military Tradition -> exact Civ VI civic.
- Professional Army -> exact Civ VI policy card.
- Theocracy -> Reformed Church unlocks Theocracy.
- Reformation -> Reformed Church.
- Mercantilism -> exact Civ VI civic.
- Humanism -> exact Civ VI civic.
- Naval Tradition -> exact Civ VI civic.
- Capitalism -> exact Civ VI civic.
- Urbanization -> exact Civ VI civic.
- Mobilization -> exact Civ VI civic.
- Nationalism -> exact Civ VI civic.
- Universal Suffrage -> Civ VI Suffrage.
- Discipline, New Deal, Five-Year Plan, Lightning Warfare, Police State, Third Alternative, Total War and Gunboat Diplomacy already exist as Civ VI policy cards.

Therefore they should not be converted into duplicate civics.

## Concepts better reused as policy cards/effects

The following types are useful, but not as additional civic nodes:

- Aristocracy
- Landed Elite
- Legalism
- Citizenship
- Collective Rule
- Meritocracy
- Representation
- Warrior Code
- Military Caste
- Organized Religion
- Religious Tolerance
- Philanthropy
- Consulates
- Cultural Diplomacy
- Wagon Trains
- Entrepreneurship
- Protectionism
- Secularism
- Free Thought
- Sovereignty
- Fine Arts
- Cultural Exchange
- Maritime Infrastructure
- Navigation School
- Merchant Navy
- Treasure Fleets

They can supply policy-card names, effects, building/unlock concepts or Inspiration ideas.

## What Civ V technologies contribute to the civic tree

Very little, once Civ VI precedence is applied.

Direct conflicts:
- Theology -> keep Civ VI Theology civic; do not duplicate as a technology for this project unless deliberately renamed/re-scoped later.
- Civil Service -> keep Civ VI Civil Service civic.
- Mass Media -> keep Civ VI Mass Media civic.
- Globalization -> keep Civ VI Globalization civic.
- Archaeology -> Civ VI Natural History already carries the archaeology gameplay function.
- Chivalry -> Civ VI already uses Chivalry as a policy-card concept; do not create a new civic from the Civ V technology.

Most other Civ V technologies remain useful for the future science/technology-tree phase rather than for filling civic gaps.

## Gap result after Civ V comparison

Current imported Civ VI counts before adding anything:
- Early Medieval: 2
- High Medieval: 3
- Renaissance: 2
- Exploration: 4
- Enlightenment: 3

Civ V provides:
- Early Medieval: **no strong non-overlapping new civic**
- High Medieval: **Scholasticism** is a strong candidate
- Renaissance: **no strong non-overlapping new civic**
- Exploration: **Scientific Revolution** is a strong candidate
- Enlightenment: most Civ V Rationalism concepts are already contained by Civ VI The Enlightenment

This is useful because it prevents artificial node inflation. The remaining Early Medieval and Renaissance gaps should next be checked against:
1. Civ V's actual unlock/content functions,
2. the Civ V Enlightenment Era mod where chronologically relevant,
3. historical concepts only after the game sources are exhausted.

## Important design implication

Do not use Civ V just because a name sounds historically useful.

For example:
- Landed Elite sounds medieval, but Feudalism already contains that social relation.
- Organized Religion sounds useful for Late Antiquity, but Theology already fills it.
- Navigation School sounds suitable for the Exploration era, but its gameplay role fits better as an Exploration unlock/building/policy.
- Secularism and Free Thought are core Enlightenment themes, but Civ VI already deliberately packages them under The Enlightenment.

The user-defined rule therefore substantially reduces duplicated civics and leaves a cleaner Civ VI-shaped tree.

## Reference files

- `civ5_bnw_policy_civ6_crosswalk_v1.csv`
- `civ5_tech_civic_crosswalk_v1.csv`
- `civ6_gs_civics_reference.csv`
- `civ6_to_project_12era_remap_v1.csv`

Web reference basis:
- CivFanatics Civilization V technology table
- Civilization Wiki BNW social-policy and ideology entries
