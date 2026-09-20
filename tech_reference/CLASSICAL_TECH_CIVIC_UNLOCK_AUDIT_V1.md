# Classical Technology + Civic Unlock Audit V1

Date: 2026-09-21
Status: **CLASSICAL COMPLETE — 10 technologies + 5 civics**

## Method

Civ V BNW remains the baseline for city/tile form and first-pass placement.

When Civ V, Civ VI technologies, Civ VI civics, or project-added nodes conflict:
1. historical and functional fit;
2. coherence with the locked 109-tech + 72-civic structure;
3. duplicate avoidance;
4. gameplay progression;
5. source placement.

## Final Classical technologies

| Technology | Main final unlocks |
|---|---|
| Celestial Navigation | Harbor city building; +1 naval movement |
| Currency | Market; Mint with Code of Laws; Wealth process |
| Horseback Riding | Horseman; Stable; Caravansary with Foreign Trade |
| Iron Working | Swordsman |
| Shipbuilding | Quadrireme; general land-unit embarkation |
| Mathematics | Catapult |
| Construction | Composite Bowman; Lumber Mill; Siege Tower; Arena with Games and Recreation |
| Engineering | Aqueduct; Fort; road bridges; provisional extra trade capacity with Foreign Trade |
| Optics | Lighthouse |
| Papermaking | Paper Workshop; paper-supported scholarship/administration |

## Final Classical civics

| Civic | Main final unlocks |
|---|---|
| Games and Recreation | Arena with Construction; Circus with Trapping |
| Political Philosophy | Autocracy, Oligarchy, Classical Republic; Tier-1 government buildings; Consulate |
| Drama and Poetry | Amphitheater; Writers' Guild; Great Writer system |
| Military Training | military-training policy layer |
| Recorded History | Natural Philosophy/Praetorium policy layer; recorded-history administration |

## Major reconciliations

### Arena / Colosseum
Civ V generic Colosseum and Civ VI Arena are merged into:
**Arena**

Gate:
**Construction + Games and Recreation**

This avoids having every city construct a building named after Rome's specific Colosseum while preserving Civ V's gameplay role.

The actual Colosseum remains a World Wonder candidate.

### Circus
Ancient V2 moved Circus away from Trapping-only.

Final:
**Trapping + Games and Recreation -> Circus**

### Market and Mint
Market remains:
**Currency -> Market**

Mint becomes:
**Currency + Code of Laws -> Mint**

Reason:
coin manufacture requires currency technology but also state/legal authority over standardized coinage.

### Caravansary
Final:
**Horseback Riding + Foreign Trade -> Caravansary**

The physical pack-animal/roadside transport side and the trade institution are both represented.

### Consulate
Civ VI places Diplomatic Quarter and Consulate at Mathematics.

The district is removed.

Final:
**Political Philosophy -> Consulate**

The Consulate becomes a one-per-civilization city building.
Its later upgrade, Chancery, remains naturally associated with the later Diplomatic Service civic.

### Catapult
Civ V places Catapult at Mathematics while Civ VI places it at Engineering.

Final:
**Mathematics -> Catapult**

Civ V gets priority here and the relationship through calculation, geometry and trajectory is acceptable. Engineering already has Aqueduct, Fort and bridge infrastructure.

### Construction
Construction keeps:
- Composite Bowman
- Lumber Mill
- Siege Tower

Civ VI and Civ V both provide useful construction-related content here.

### Engineering
Engineering keeps the Civ V-style infrastructure identity:
- Aqueduct
- Fort
- road bridges across rivers

Aqueduct is a normal city building, not a Civ VI district.

It is also flagged for the later Health & Plague pass.

### Shipbuilding vs Optics
Civ V puts general embarkation at Optics.
Civ VI puts it at Shipbuilding.

Final:
**Shipbuilding -> general land-unit embarkation**

Optics keeps:
**Lighthouse**

This is a stronger functional split.

### Celestial Navigation
Civ VI Harbor district is converted into:
**Harbor city building**

The later Civ V Harbor placement is not binding because the project has an explicit Celestial Navigation node.

Civ VI's +1 naval movement from Mathematics is moved here because navigation is the stronger functional fit.

### Papermaking
Papermaking is a project-added historical technology.

Final:
**Papermaking -> Paper Workshop**

The generic Paper Workshop is inspired by the historical paper-production function and Civ V China's Paper Maker concept, but it does not copy China's unique yields.

China's Paper Maker remains civilization-specific.

## Political Philosophy government buildings

The Government Plaza itself was converted in Ancient V2 into a one-per-civilization national city building.

After adopting a Tier-1 government at Political Philosophy, choose one mutually exclusive building:
- Ancestral Hall
- Audience Chamber
- Warlord's Throne

This preserves the Civ VI government choice without using a map district. Civ VI itself requires a Tier-1 government for these buildings. 

## Drama and Poetry

Because the project node is a civic, Civ V's technology unlocks migrate naturally here:
- Amphitheater
- Writers' Guild
- Great Writer generation

The Theater Square district is removed.

## Health & disease note

Aqueduct is flagged as an early Health-supporting city building.

Harbor, Caravansary, expanded trade routes and embarkation may later increase disease transmission connectivity in the Health & Plague model. No transmission coefficients are assigned in this pass.

## Wonders and civilization uniques

All World/National Wonders remain deferred.

Civilization-specific units, buildings and improvements remain unique and are not promoted into the generic roster.

## Authority files

- `tech_reference/classical_tech_civic_unlock_audit_v1.csv`
- `tech_reference/technology_unlock_summary_classical_v1.csv`
- `civics_reference/civic_unlock_summary_classical_v1.csv`

