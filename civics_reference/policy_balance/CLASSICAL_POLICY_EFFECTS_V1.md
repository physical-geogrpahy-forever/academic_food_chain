# Classical Policy Effects V1

Date: 2026-09-21
Status: **LOCKED**

## Direct Civ6 values retained
- Charismatic Leader: +2 Influence/turn toward Envoys
- Diplomatic League: first Envoy to each city-state counts as 2
- Literary Tradition: +2 Great Writer Points/turn
- Raid: pillage/coastal-raid yields +50%
- Equestrian Orders: improved Horses and Iron each yield +1 strategic resource/turn

## Civ V-style structural translations

### Insulae
Civ6 requires 2 specialty districts.

Project:
**+1 Housing in cities with at least 2 institutional building chains.**

For this threshold, the city must have buildings from at least two different functional chains, such as:
- religion: Shrine/Temple
- science: Library/University
- commerce: Market/Bank
- military: Barracks/Armory
- culture: Amphitheater/Opera House/Museum
- port: Harbor/Lighthouse/Seaport
- industry: Workshop/Factory

Multiple buildings from one chain count as one chain.

### Veterancy
Civ6 boosts Encampment and Harbor construction.

Project:
**+30% Production toward Barracks, Armory, Military Academy, Harbor, Lighthouse, and Seaport.**

### Natural Philosophy
Campus adjacency does not exist.

Project:
**Library and University each +1 Science while the policy is active.**

This is intentionally modest because Algebra, Scholasticism, Scientific Revolution, Rationalism and later science policies can also stack.

Authority:
`civics_reference/policy_balance/CLASSICAL_POLICY_EFFECTS_V1.csv`
