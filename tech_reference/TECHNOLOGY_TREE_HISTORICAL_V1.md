# Technology Tree Historical V1 — 103-node DAG

Date: 2026-09-20
Status: ACTIVE TECHNOLOGY-TREE BASELINE

## Scope

This graph uses the locked 103-technology roster:
- Civilization VI: Gathering Storm as the primary skeleton,
- non-duplicating Civilization V technologies,
- five technical nodes from the Civilization V Enlightenment Era mod.

The prerequisite graph itself is **not** a mechanical copy of either game. It is rebuilt so that a prerequisite represents a plausible technical/material predecessor.

## Automated QA

- Technologies: 103
- Root technologies: Agriculture, Pottery, Animal Husbandry, Mining, Sailing, Archery
- Reachable from a root: 103/103
- Missing prerequisite references: 0
- Directed cycles: 0
- Backward-era prerequisite edges: 0
- Maximum direct prerequisites: 2
- Terminal technologies: Archery, Irrigation, Trapping, Stirrups, Buttress, Cartography, Fortification, Economics, Sanitation, Mass Production, Fertilizer, Dynamite, Railroad, Refrigeration, Telegraph, Armor Plating, Advanced Ballistics, Combined Arms, Penicillin, Satellites, Guidance Systems, Lasers, Stealth Technology, Ecology, Future Tech

Multiple roots are intentional. Unlike the civic tree, the technology tree does not pretend that all early technologies descended from one invention.

## Era counts

- Ancient: 14
- Classical: 9
- Late Antiquity: 2
- Early Medieval: 2
- High Medieval: 6
- Renaissance: 5
- Exploration: 9
- Enlightenment: 6
- Industrial: 16
- Modern: 12
- Atomic: 13
- Information: 9
- Total: 103

## Major historical/technical chains

### Food and settlement
Agriculture -> Irrigation  
Agriculture -> Calendar -> Astrology  
Animal Husbandry -> Trapping / Horseback Riding  
Mining -> Masonry / Bronze Working  
Agriculture + Mining -> Wheel

### Writing, mathematics and administration technologies
Pottery -> Writing  
Writing + Calendar -> Currency / Mathematics  
Construction + Mathematics -> Engineering

Writing is therefore not a universal root. Agriculture, pastoralism, mining, sailing and archery can all exist independently.

### Metals and military engineering
Mining -> Bronze Working -> Iron Working  
Engineering + Military Tactics -> Military Engineering  
Military Engineering + Education -> Gunpowder  
Apprenticeship + Machinery -> Metal Casting  
Gunpowder + Metal Casting -> Metallurgy  
Gunpowder + Metallurgy -> Flintlock  
Flintlock + Ballistics -> Rifling

### Navigation and the oceanic expansion branch
Sailing + Astrology -> Celestial Navigation  
Celestial Navigation + Iron Working -> Compass  
Optics + Education -> Astronomy  
Compass + Astronomy -> Navigation  
Printing + Navigation -> Cartography  
Shipbuilding + Navigation -> Square Rigging  
Square Rigging + Metallurgy -> Warships

This separates:
- Navigation = practical positional/oceanic navigation,
- Cartography = systematic mapped representation,
- Square Rigging = sailing-rig technology,
- Warships = large early-modern naval military technology.

### Knowledge, printing and early modern science
Engineering + Apprenticeship -> Machinery  
Machinery + Education -> Printing  
Optics + Education -> Astronomy  
Mathematics + Engineering -> Physics  
Astronomy + Physics -> Scientific Theory  
Gunpowder + Scientific Theory -> Chemistry

The civic **Scientific Revolution** will later use these science technologies as cross-tree boosts/gates without duplicating them as civics.

### Production to industrialization
Apprenticeship + Banking -> Manufacturing  
Manufacturing + Scientific Theory -> Steam Power  
Steam Power + Manufacturing -> Industrialization  
Manufacturing + Machinery -> Replaceable Parts  
Replaceable Parts + Industrialization -> Mass Production

This fixes the chronology problem in Civilization VI where Mass Production sits in the Renaissance era. Here it is a 19th-century industrial technology.

### Industrial infrastructure
Scientific Theory + Physics -> Electricity  
Electricity + Printing -> Telegraph  
Steam Power + Steel -> Railroad  
Chemistry + Industrialization -> Refrigeration  
Chemistry + Biology -> Fertilizer  
Steel + Warships -> Armor Plating

### Early 20th century
Refining + Engineering -> Combustion  
Combustion + Physics -> Flight  
Electricity + Acoustics -> Radio  
Flight + Radio -> Advanced Flight  
Ballistics + Chemistry -> Rocketry  
Electricity + Radio -> Electronics  
Radio + Electronics -> Radar  
Scientific Theory + Physics -> Atomic Theory

### Atomic and late-20th century
Atomic Theory + Chemistry -> Nuclear Fission  
Electronics + Mathematics -> Computers  
Electronics + Computers -> Telecommunications  
Rocketry + Electronics -> Satellites / Guidance Systems  
Atomic Theory + Electronics -> Lasers  
Plastics + Chemistry -> Synthetic Materials  
Synthetic Materials + Advanced Flight -> Composites  
Radar + Composites -> Stealth Technology  
Computers + Electronics -> Robotics  
Atomic Theory + Electronics -> Particle Physics  
Nuclear Fission + Particle Physics -> Nuclear Fusion  
Biology + Computers -> Ecology

### Information and future
Composites + Particle Physics -> Nanotechnology  
Robotics + Telecommunications -> Advanced AI  
Nuclear Fusion + Nanotechnology -> Advanced Power Cells  
Robotics + Advanced AI -> Cybernetics  
Nanotechnology + Cybernetics -> Smart Materials  
Advanced AI + Telecommunications -> Predictive Systems  
Smart Materials + Advanced Power Cells -> Seasteads  
Advanced Power Cells + Predictive Systems -> Offworld Mission  
Seasteads + Offworld Mission -> Future Tech

This is a fixed QA/reference topology. If the project later preserves Gathering Storm-style random Future technology ordering, the Information-era future names can be shuffled through a fixed acyclic template without changing the locked roster.

## Deliberate departures from Civilization VI

- Agriculture is restored from Civ V instead of treating Pottery/Animal Husbandry/Mining as the whole opening.
- Chemistry is placed in the 18th-century Enlightenment era.
- Mass Production is placed in the 19th-century Industrial era.
- Electricity, Steel, Replaceable Parts and Refining are 19th-century Industrial technologies.
- Rocketry and Advanced Flight are early-20th-century Modern technologies.
- Telecommunications, Satellites, Lasers, Robotics and related technologies are mid-late-20th-century Atomic technologies.
- Future Era technologies are folded into Information because the project has no separate Future era.

## Known abstractions to review later

- Astrology is retained because it is a Civ VI technology, but in this project it should be treated as early systematic celestial/religious observation rather than modern science.
- Apprenticeship is institution-like in name but retained as a technology because Civ VI uses it as the craft-production branch; its gameplay content should focus on production technique and skilled craft organization.
- Education likewise borders the civic/technology divide. It remains in technology because both Civ V and Civ VI use it there; the civic tree's Scholasticism/Humanism represents the social-intellectual institution.
- Economics remains a technology because Civ VI uses it in the technology tree; Capitalism/Mercantilism remain civics.

## Next step

Reconcile `civic_tech_crosslinks_v1.csv` with this exact tree:
- confirm every HARD/BOOST technology exists;
- ensure no civic requires a technology from a later project era;
- replace generic crosslinks where a more exact locked technology now exists;
- check for cross-tree cycles once any technology begins to require civic conditions.
