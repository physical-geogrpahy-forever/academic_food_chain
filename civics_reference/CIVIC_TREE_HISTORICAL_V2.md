# Civic Tree Historical Flow V2 — 72-node social prerequisite DAG

Date: 2026-09-20
Status: ACTIVE REVIEW BASELINE — supersedes V1 for social-to-social prerequisite design

## What changed

V1 was deliberately close to Civilization VI. V2 keeps the 72 locked civic names and era assignments but removes social prerequisite links that are difficult to defend historically.

The guiding distinction is now:

- this file stores **social/institutional prerequisites only**;
- material/technical necessities will be added later as cross-tree technology gates;
- a social prerequisite should represent a plausible institutional/intellectual predecessor, not merely a convenient Civ VI path.

## Automated QA

- nodes: 72
- roots: Code of Laws
- reachable from Code of Laws: 72/72
- missing prerequisite references: 0
- directed cycles: 0
- backward-era edges: 0
- maximum direct social prerequisites: 2
- terminal nodes: Mercenaries, Guilds, Divine Right, Reformed Church, Colonialism, Suffrage, Totalitarianism, Class Struggle, Rapid Deployment, Space Race, Future Civic

## Major corrections from V1

### Late Antiquity

Old game-shaped links:
- Games and Recreation + Political Philosophy -> Defensive Tactics
- Mysticism + Drama and Poetry -> Theology
- Defensive Tactics -> Naval Tradition
- Defensive Tactics + Recorded History -> Civil Service

V2:
- Military Training + Political Philosophy -> Defensive Tactics
- Mysticism + Recorded History -> Theology
- Military Tradition + Foreign Trade -> Naval Tradition
- Early Empire + Recorded History -> Civil Service

Rationale:
military doctrine, religious textual/systematic traditions, maritime trade/warfare, and record-based administration are separated instead of being routed through entertainment or defensive warfare.

### Early Medieval / High Medieval

V2:
- Civil Service -> Written Culture
- Written Culture -> Court Culture
- Feudalism + Foreign Trade -> Medieval Faires
- Medieval Faires + Civil Service -> Guilds
- Theology + Court Culture -> Divine Right
- Theology + Written Culture -> Scholasticism

The old requirement Feudalism -> Court Culture is removed. Court-centered administration and intellectual life existed in Byzantine, Abbasid and other non-feudal settings.

### Renaissance

V2:
- Scholasticism + Guilds -> Humanism
- Court Culture -> Diplomatic Service
- Court Culture + Humanism -> Patronage
- Humanism -> Print Culture

Diplomatic Service is no longer derived from Guilds. Renaissance permanent diplomacy is instead tied to court/state institutions.

### Exploration

V2:
- Naval Tradition + Mercenaries -> Exploration
- Theology + Print Culture -> Reformed Church
- Print Culture -> Scientific Revolution
- Diplomatic Service + Humanism -> Sovereignty
- Exploration + Sovereignty -> Mercantilism
- Mercantilism -> Colonialism

Removed:
- Reformed Church as a hard prerequisite of Sovereignty
- Exploration as a hard prerequisite of Scientific Revolution
- Naval Tradition as a hard prerequisite of Mercantilism

This avoids making Christian Reformation mandatory for sovereign-state development or overseas exploration mandatory for scientific change.

### Enlightenment

V2:
- Scientific Revolution + Sovereignty -> The Enlightenment
- Patronage -> Opera and Ballet
- Scientific Revolution + Exploration -> Natural History
- Print Culture + The Enlightenment -> Public Sphere
- Public Sphere + Sovereignty -> Constitutionalism

The Enlightenment is therefore reached through an intellectual-scientific branch plus an early-modern state/political branch rather than directly through Diplomatic Service alone.

### Industrial

V2:
- Mercantilism -> Capitalism
- Sovereignty -> Civil Engineering
- Sovereignty + Public Sphere -> Nationalism
- Opera and Ballet + The Enlightenment -> Romanticism
- Civil Engineering + Capitalism -> Urbanization
- Nationalism + Military Training -> Scorched Earth
- Natural History + Romanticism -> Conservation
- Public Sphere + Urbanization -> Mass Media
- Capitalism + Urbanization -> Labor Movement

Critical correction:
**Mass Media -> Capitalism is removed.**
Capitalism now grows from the earlier mercantile-commercial line. Britannica's economic-history overview likewise describes a transition from mercantilism/commercial capitalism toward industrial capitalism.

### Modern

V2:
- Scorched Earth -> Mobilization
- Mass Media + Mobilization -> Ideology
- Constitutionalism + Labor Movement -> Suffrage
- Ideology -> Totalitarianism
- Ideology + Labor Movement -> Class Struggle
- Urbanization + Capitalism -> Professional Sports

Critical corrections:
- Ideology is no longer required for Professional Sports.
- Suffrage is no longer downstream of Ideology; it is connected to constitutional politics and organized mass society.

### Atomic

V2:
- Ideology -> Nuclear Program
- Conservation -> Cultural Heritage
- Ideology + Nuclear Program -> Cold War
- Cold War -> Rapid Deployment / Space Race
- Cultural Heritage + Mass Media -> Environmentalism

Critical correction:
**Rapid Deployment -> Environmentalism is removed.**

Nuclear Program, Rapid Deployment and Space Race will later receive technology gates; this social graph alone does not claim those developments are possible without nuclear physics, aviation or rocketry.

### Information

V2:
- Cold War + Capitalism -> Globalization
- Mass Media + Professional Sports -> Social Media
- Environmentalism + Globalization -> Near Future Governance
- Globalization + Social Media -> Venture Politics / Distributed Sovereignty / Optimization Imperative

Critical corrections:
- Space Race is no longer a hard social prerequisite of Social Media.
- Rapid Deployment and Space Race are no longer the social causes of Globalization.

Telecommunications, computing and Internet technologies will later be hard technology gates where appropriate.

## Historical basis for the main corrections

- Early medieval literacy was integral to government and written administration, not dependent on theology alone.
- Byzantine court culture retained a secular administrative elite, showing that court culture cannot be made dependent on feudalism.
- Renaissance permanent diplomacy developed together with territorial states, central chanceries and court/state administration.
- Print culture materially aided Reformation movements and expanded later reading publics.
- Seventeenth- and eighteenth-century public spheres grew through print, coffeehouses, salons and other spaces of sociability.
- Mercantilism is conventionally treated as an early stage of commercial capitalism, followed by industrial capitalism.
- Nineteenth-century professional spectator sport was strongly linked to urbanization, rising incomes and commercialization.
- Modern environmental movements have depended heavily on mass media for mobilization and public visibility.

## Remaining deliberate game abstractions

Some imported Civ VI civics remain imperfect as universal historical stages:
- Scorched Earth
- Professional Sports
- Nuclear Program
- Rapid Deployment
- Space Race

They remain because the roster is locked and they provide useful gameplay unlock branches.

Their historical plausibility should be improved with:
1. technology gates;
2. policy-card effects;
3. optional/branch positioning;
rather than by adding more civics.

## Next step

Do not yet attach technologies.

First review V2's social-only relationships. After approval:
- mark which social civics need hard technology gates;
- mark which only receive technology-based Inspiration/boost;
- keep the two trees parallel but cross-linked.


## Guilds and Mercenaries successor cleanup

After the first V2 QA pass:
- Humanism was changed from Scholasticism + Medieval Faires to **Scholasticism + Guilds**.
- Exploration was changed from Naval Tradition + Medieval Faires to **Naval Tradition + Mercenaries**.

This removes two unnecessary dead-end branches while remaining close to Civilization VI's original structure.
