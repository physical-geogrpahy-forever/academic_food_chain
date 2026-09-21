# Civic Tree Historical Flow V3 — full 72-node audit

Date: 2026-09-20
Status: ACTIVE SOCIAL-FLOW BASELINE — supersedes Historical V2

## Scope

The 72 civic names and era assignments remain locked.

V3 asks one question for every social edge:

> Does the later civic plausibly require the earlier **social/institutional** development, rather than merely being adjacent in Civilization VI?

Technological necessities are deliberately excluded here and will be added as cross-tree gates afterward.

## Automated QA

- Nodes: 72
- Root: Code of Laws
- Reachable from Code of Laws: 72/72
- Missing prerequisite references: 0
- Directed cycles: 0
- Backward-era edges: 0
- Maximum direct social prerequisites: 2
- Terminal/optional branches: Games and Recreation, Mercenaries, Divine Right, Reformed Church, Colonialism, Scorched Earth, Suffrage, Totalitarianism, Class Struggle, Professional Sports, Cultural Heritage, Rapid Deployment, Space Race, Future Civic

## V3 changes after the full era-by-era audit

### Ancient

Opening structure is retained from Civilization VI for game readability:

Code of Laws -> Craftsmanship / Foreign Trade.

This is explicitly a **structural game abstraction**, not a claim that historical craftsmanship or foreign trade originated after written law codes.

The rest of the Ancient opening is retained.

### Classical

Changed:
- Mysticism + Early Empire -> Drama and Poetry
- Military Tradition + State Workforce -> Military Training
- Early Empire + Political Philosophy -> Recorded History

Removed as hard causal links:
- Games and Recreation -> Military Training
- Drama and Poetry -> Recorded History

Reason:
organized military training depends more plausibly on martial institutions and state manpower than on public entertainment.
Recorded historical traditions depend on literate states and political-historical reflection; writing itself will later be a technology gate.

Drama and Poetry remains connected forward through Court Culture rather than being treated as a prerequisite of historiography.

### Late Antiquity

Retained from V2:
- Military Training + Political Philosophy -> Defensive Tactics
- Mysticism + Recorded History -> Theology
- Military Tradition + Foreign Trade -> Naval Tradition
- Early Empire + Recorded History -> Civil Service

These are broad conceptual dependencies, not claims of a single universal historical sequence.

### Early Medieval

- Defensive Tactics -> Feudalism
- Military Training + Foreign Trade -> Mercenaries
- Civil Service -> Written Culture
- Written Culture + Drama and Poetry -> Court Culture

Important:
- Feudalism is NOT required for Court Culture.
- Theology is NOT required for Written Culture.
- Mercenaries becomes an optional military-economic branch and is not forced into Exploration.

### High Medieval

- Feudalism + Foreign Trade -> Medieval Faires
- Medieval Faires + Written Culture -> Guilds
- Theology + Court Culture -> Divine Right
- Theology + Written Culture -> Scholasticism

Guilds no longer requires Civil Service directly; the written-charter/legal infrastructure is represented by Written Culture.

### Renaissance

- Scholasticism + Court Culture -> Humanism
- Court Culture -> Diplomatic Service
- Humanism + Guilds -> Patronage
- Humanism -> Print Culture

This makes the major branches clearer:
- intellectual: Scholasticism -> Humanism -> Print Culture
- court/state: Court Culture -> Diplomatic Service
- urban cultural support: Guilds + Humanism -> Patronage

### Exploration

- Naval Tradition + Medieval Faires -> Exploration
- Theology + Print Culture -> Reformed Church
- Print Culture -> Scientific Revolution
- Diplomatic Service + Humanism -> Sovereignty
- Exploration + Sovereignty -> Mercantilism
- Mercantilism -> Colonialism

Removed:
- Mercenaries -> Exploration

Mercenary institutions were important in early-modern warfare but are not a universal prerequisite for overseas exploration.

### Enlightenment

Retained:
- Scientific Revolution + Sovereignty -> The Enlightenment
- Patronage -> Opera and Ballet
- Scientific Revolution + Exploration -> Natural History
- Print Culture + The Enlightenment -> Public Sphere
- Public Sphere + Sovereignty -> Constitutionalism

These links deliberately separate intellectual, cultural, communicative and constitutional developments.

### Industrial

- Mercantilism -> Capitalism
- Civil Service + Sovereignty -> Civil Engineering
- Sovereignty + Public Sphere -> Nationalism
- Opera and Ballet + The Enlightenment -> Romanticism
- Civil Engineering + Capitalism -> Urbanization
- Defensive Tactics + Nationalism -> Scorched Earth
- Natural History + Romanticism -> Conservation
- Public Sphere + Urbanization -> Mass Media
- Capitalism + Urbanization -> Labor Movement

Scorched Earth is retained only as an **optional military branch**. It is no longer allowed to cause Mobilization.

### Modern

Changed:
- Nationalism + Urbanization -> Mobilization
- Nationalism + Mass Media -> Ideology
- Constitutionalism -> Suffrage
- Ideology -> Totalitarianism
- Ideology + Labor Movement -> Class Struggle
- Games and Recreation + Urbanization -> Professional Sports

Critical fixes:
- Scorched Earth no longer causes Mobilization.
- Mobilization no longer causes Ideology.
- Labor Movement is no longer a mandatory prerequisite for Suffrage.
- Professional Sports has no ideological prerequisite; it now continues the older public-recreation branch through urban mass society.

Labor movements historically contributed to franchise expansion in many societies, but because they were not universally necessary they belong better as an Inspiration/boost for Suffrage than as a hard prerequisite.

### Atomic

Changed:
- Mobilization -> Nuclear Program
- Conservation -> Cultural Heritage
- Ideology + Nuclear Program -> Cold War
- Cold War -> Rapid Deployment / Space Race
Nuclear Program is no longer caused by Ideology.
Its real material requirement — nuclear physics/fission — will be a technology gate.
Mobilization represents the social/state-capacity side of large strategic programs.

Environmentalism is socially derived from Conservation + Mass Media but is now placed in the Information era under the Gathering Storm late-era split.

### Information

- Capitalism + Mass Media -> Globalization
- Mass Media + Public Sphere -> Social Media
- Conservation + Mass Media -> Environmentalism
- Environmentalism + Globalization -> Near Future Governance
- Globalization + Social Media -> Venture Politics / Distributed Sovereignty / Optimization Imperative

Critical fix:
Professional Sports no longer causes Social Media.

The social link Public Sphere -> Social Media is supported conceptually by scholarship that treats social media as a transformed digital public sphere. Internet/telecommunications/computing will be technology gates, not social predecessors.

Cold War is no longer a mandatory prerequisite for Globalization. The Information-era placement supplies chronology; Capitalism + Mass Media supplies the social/economic communication lineage.


### Future

The Gathering Storm Future civic layer is restored as a separate project era:

- Near Future Governance + Venture Politics -> Information Warfare
- Distributed Sovereignty + Optimization Imperative -> Global Warming Mitigation
- Information Warfare + Distributed Sovereignty -> Cultural Hegemony
- Global Warming Mitigation + Venture Politics -> Smart Power Doctrine
- Cultural Hegemony + Smart Power Doctrine -> Exodus Imperative
- Exodus Imperative -> Future Civic

Future Civic remains the repeatable terminal node.

## Remaining intentional abstractions

### Code of Laws as the sole root
Kept because the project deliberately follows the Civ VI opening structure.
Historically, craftsmanship and foreign exchange long predate formal written law codes.

### Feudalism
Kept as a broad project civic despite the fact that "feudalism" is a contested and regionally specific historical category.

### Divine Right
Kept in the High Medieval roster for Civ VI continuity, although the strict doctrine associated with the phrase is especially prominent in early-modern Europe. It is interpreted broadly in gameplay as sacral/legitimist monarchy.

### Scorched Earth
A tactic/doctrine more than a general social institution. It remains an optional military civic because the roster is locked.

### Nuclear Program / Rapid Deployment / Space Race
These are state-strategic programs rather than ordinary civics. They remain for Civ VI continuity and will receive strong technology gates.

## Cross-tree gates expected next

Examples, NOT yet implemented in this file:

- Recorded History <- Writing technology
- Written Culture <- Writing / manuscript-production technologies
- Print Culture <- Printing technology
- Scientific Revolution <- astronomy/optics/scientific-instrument technology
- Exploration <- navigation/cartography/seafaring technology
- Mass Media <- industrial printing / telegraph / radio chain
- Nuclear Program <- Nuclear Fission
- Rapid Deployment <- aviation/logistics technology
- Space Race <- Rocketry
- Social Media <- Internet / telecommunications / computing
- Optimization Imperative <- Robotics / AI-related technology

## Decision rule going forward

A missing technology should never be replaced by an unrelated civic prerequisite merely to keep the graph connected.

The social tree may have optional terminal branches. "Connected" means every node is reachable from the root, not that every civic must be a mandatory step toward a later civic.

That distinction prevents artificial links such as Mercenaries -> Exploration or Professional Sports -> Social Media.


### Public recreation continuity

Post-QA cleanup:
- Professional Sports now requires **Games and Recreation + Urbanization**, not Capitalism + Urbanization.
- This preserves a long cultural line from organized public recreation to urban mass spectator sport without making capitalism a universal hard prerequisite.


### Cross-tree inheritance correction

After linking the civic tree to the technology tree, Cold War -> Globalization was removed as a hard social edge.

Reason:
Cold War inherits the Nuclear Program's hard Nuclear Fission gate. If Globalization required Cold War, all globalization and much of the later Information civic branch would incorrectly inherit Nuclear Fission as a material prerequisite.

V3.1 therefore uses:
**Capitalism + Mass Media -> Globalization**

Cold War remains a separate Atomic-era geopolitical branch.
