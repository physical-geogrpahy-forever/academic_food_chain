# Civic–Technology Crosslinks V1

Date: 2026-09-20
Status: PROVISIONAL CROSS-TREE BASELINE

This file is layered on top of:
- `CIVIC_TREE_HISTORICAL_V3.md`
- `civic_tree_historical_v3.csv`

The 72 civic names, eras and V3 social prerequisites are unchanged.

## Core rule

The science/technology tree and civic tree remain parallel.

A civic can have one of three **direct** technology relations:

- **HARD**: the civic cannot be completed until the listed technology is known.
- **BOOST**: the civic can be researched without the technology, but the technology gives a civic research boost / Inspiration-type bonus.
- **NONE**: no new direct technology condition is added.

A civic also inherits HARD gates from its prerequisite civics. The CSV calculates those inherited gates separately so they are not redundantly attached to every downstream node.

Current direct classification:
- HARD: 11
- BOOST: 31
- NONE: 30
- TOTAL: 72

## Hard gates are intentionally rare

Only developments where the material technology is close to indispensable receive a direct HARD gate.

- Recorded History <- **Writing**
- Naval Tradition <- **Sailing**
- Print Culture <- **Printing**
- Exploration <- **Cartography**
- Civil Engineering <- **Engineering**
- Nuclear Program <- **Nuclear Fission**
- Rapid Deployment <- **Flight**
- Space Race <- **Rocketry**
- Social Media <- **Telecommunications**
- Optimization Imperative <- **Robotics**
- Exodus Imperative <- **Satellites**

Examples:
- Recorded History needs Writing.
- Print Culture needs Printing.
- Exploration, as the project's 16th-17th century oceanic exploration civic, needs Cartography.
- Nuclear Program needs Nuclear Fission.
- Rapid Deployment needs Flight.
- Space Race needs Rocketry.
- Social Media needs Telecommunications.
- Optimization Imperative needs Robotics.
- Exodus Imperative needs mature space infrastructure represented provisionally by Satellites.

## Technology boosts

Technology is much more often a catalyst than an absolute prerequisite.

- Code of Laws <- Writing boost
- Craftsmanship <- Mining boost
- Foreign Trade <- Sailing boost
- State Workforce <- Masonry boost
- Early Empire <- Writing boost
- Political Philosophy <- Writing boost
- Military Training <- Bronze Working boost
- Defensive Tactics <- Engineering boost
- Mercenaries <- Currency boost
- Medieval Faires <- Currency boost
- Guilds <- Currency boost
- Scholasticism <- Education boost
- Humanism <- Education boost
- Scientific Revolution <- Astronomy boost
- Mercantilism <- Banking boost
- The Enlightenment <- Scientific Theory boost
- Natural History <- Scientific Theory boost
- Capitalism <- Banking boost
- Urbanization <- Industrialization boost
- Scorched Earth <- Military Science boost
- Conservation <- Biology boost
- Mass Media <- Radio boost
- Labor Movement <- Industrialization boost
- Mobilization <- Steam Power boost
- Ideology <- Radio boost
- Totalitarianism <- Radio boost
- Professional Sports <- Radio boost
- Environmentalism <- Ecology boost
- Globalization <- Telecommunications boost
- Near Future Governance <- Computers boost
- Global Warming Mitigation <- Satellites boost

This avoids deterministic technological history. For example:
- industrialization strongly accelerates Urbanization and Labor Movement but neither human settlement nor worker organization is literally impossible before industrial machinery;
- radio strongly expands Mass Media, Ideology, Totalitarianism and Professional Sports but is not treated as their single cause;
- telecommunications accelerates modern Globalization but earlier global exchange existed without electronic communication.

## Important inherited examples

Because hard gates propagate through the social prerequisite graph:

- Civil Service and Written Culture inherit **Writing** through Recorded History.
- Reformed Church, Scientific Revolution, Public Sphere and much of the later political-cultural branch inherit **Printing** through Print Culture.
- Mercantilism and Colonialism inherit **Sailing + Cartography** through Exploration.
- Urbanization, Mass Media and Labor Movement inherit **Engineering** through Civil Engineering where that branch is required.
- Cold War inherits **Nuclear Fission** through Nuclear Program.
- Venture Politics and Distributed Sovereignty inherit **Telecommunications** through Social Media.
- late Future branches inherit the hard gates accumulated by their randomized predecessors.

This is why the CSV does not repeat the same hard technology on every downstream civic.

## Technology names are provisional until the science tree is locked

The current labels deliberately reuse Civilization VI technology names where practical:
Writing, Mining, Sailing, Masonry, Bronze Working, Engineering, Currency, Education, Printing, Cartography, Astronomy, Banking, Scientific Theory, Industrialization, Military Science, Biology, Radio, Steam Power, Nuclear Fission, Flight, Rocketry, Ecology, Telecommunications, Computers, Robotics, Satellites.

The **relation strength** (HARD / BOOST / NONE) is the important design decision here.

Exact technology names may later be remapped when the project's own science tree is finalized.

Examples:
- if the final science tree contains an explicit Internet technology, Social Media should use Internet instead of the broader Telecommunications label;
- if it contains Oceanic Navigation rather than Cartography, Exploration can be remapped without altering the civic graph;
- if it separates rail logistics from Steam Power, Mobilization can use that more specific technology as its boost.

## Historical support for the strongest crosslinks

### Writing
Civilization VI's own historical description of Writing emphasizes that writing enabled organized government, economy, religion and the preservation of knowledge. Recorded History is therefore a strong hard-gate case.

### Printing
Civilization VI explicitly describes Printing as promoting the Reformation and Scientific Revolution. Historical scholarship on the printing revolution likewise treats print as a major agent in the Renaissance, Reformation and rise of modern science.

### Exploration / Cartography
Civilization VI's Cartography entry explicitly links advances in mapping to the Age of Exploration and enables ocean navigation in gameplay.

### Industrialization
Civilization VI's Industrialization entry explicitly associates industrialization with urbanization, capitalism, social upheaval and the reorganization of labor. It is therefore used as a boost rather than a universal hard cause for Urbanization and Labor Movement.

### Nuclear Program
Civilization VI's Nuclear Fission entry directly connects fission research with the Manhattan Project and the first atomic weapons. This is a true HARD gate.

### Space Race
NASA's historical account describes the Cold War space race as depending on postwar rocketry and upper-atmosphere research. Rocketry is therefore a HARD gate.

### Telecommunications and globalization
Historical research on telegraphy and telecommunications describes long-distance communications as central to the transformation of global economic networks. Telecommunications is therefore a strong boost for Globalization.

### Social Media
Civilization VI's Telecommunications entry explicitly treats Internet and related communication systems as part of telecommunications. Social Media therefore receives a HARD Telecommunications gate for now.

## Design safeguards

1. A HARD technology gate must represent a near-material impossibility, not merely correlation.
2. Do not make a technology HARD just because it appeared around the same time.
3. Social prerequisites continue to model institutions, ideas and cultural continuity.
4. Technology boosts represent enabling or accelerating effects.
5. If a hard prerequisite is already inherited from a prerequisite civic, do not duplicate it directly.
6. Final hard-gate validation must be repeated after the science tree itself is locked.

## Next step

Build/remap the science tree, then:
1. map each provisional technology name to an exact project technology node;
2. verify no civic requires a technology from a later project era;
3. verify no technology requires a civic that would create a cross-tree cycle;
4. replace generic technology boosts with actual Inspiration values/conditions.
