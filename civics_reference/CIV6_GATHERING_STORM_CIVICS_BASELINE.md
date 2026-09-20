# Civilization VI: Gathering Storm — Civic Tree reference baseline

Date collected: 2026-09-20

## Scope

This is a reference import for the Civilization-style game project.

Baseline:
- Civilization VI with Rise and Fall / Gathering Storm rules
- normal game civics
- no scenario-only civics
- no Tech and Civic Shuffle Mode
- civilization/leader-specific unique unlocks are retained only as notes, not as core shared mechanics

The project should use this file as the starting point instead of rebuilding the civic system from zero.

## Core Civ VI mechanics retained as reference

- Civics are researched with Culture.
- Each civic has prerequisite civic links.
- Inspirations are gameplay objectives that immediately add civic progress. In Rise and Fall / Gathering Storm the normal boost is 40% of civic cost; Near Future Governance is a special 90% case.
- Civics unlock policy cards, governments, units, buildings, districts, wonders, diplomatic rules and other game systems.
- Policy cards can be re-slotted, with free reselection when a new government or policy is unlocked.
- The tree repeatedly branches and reconverges. It is not a set of isolated thematic branches.
- Future Era prerequisites in Gathering Storm are randomized; Future Civic is always the final repeatable civic.

## Full standard civic roster

Ancient:
Code of Laws; Craftsmanship; Foreign Trade; Military Tradition; State Workforce; Early Empire; Mysticism.

Classical:
Games and Recreation; Political Philosophy; Drama and Poetry; Military Training; Defensive Tactics; Recorded History; Theology.

Medieval:
Naval Tradition; Feudalism; Civil Service; Mercenaries; Medieval Faires; Guilds; Divine Right.

Renaissance:
Exploration; Humanism; Diplomatic Service; Reformed Church; Mercantilism; The Enlightenment.

Industrial:
Colonialism; Civil Engineering; Nationalism; Opera and Ballet; Natural History; Scorched Earth; Urbanization.

Modern:
Conservation; Mass Media; Mobilization; Capitalism; Ideology; Nuclear Program; Suffrage; Totalitarianism; Class Struggle.

Atomic:
Cultural Heritage; Cold War; Professional Sports; Rapid Deployment; Space Race.

Information:
Environmentalism; Globalization; Social Media; Near Future Governance; Venture Politics; Distributed Sovereignty; Optimization Imperative.

Future:
Information Warfare; Global Warming Mitigation; Cultural Hegemony; Smart Power Doctrine; Exodus Imperative; Future Civic.

Total normal Gathering Storm reference civics: 61.

## Exact structural spine to preserve where possible

Ancient/Classical opening:
Code of Laws
-> Craftsmanship -> Military Tradition / State Workforce
-> Foreign Trade -> Early Empire / Mysticism

Political Philosophy requires BOTH State Workforce and Early Empire.
Military Training requires BOTH Military Tradition and Games and Recreation.
Defensive Tactics requires BOTH Games and Recreation and Political Philosophy.
Recorded History requires BOTH Political Philosophy and Drama and Poetry.
Theology requires BOTH Mysticism and Drama and Poetry.

Medieval/Renaissance:
Defensive Tactics -> Naval Tradition / Feudalism
Defensive Tactics + Recorded History -> Civil Service
Military Training + Feudalism -> Mercenaries
Feudalism -> Medieval Faires
Feudalism + Civil Service -> Guilds
Theology + Civil Service -> Divine Right
Mercenaries + Medieval Faires -> Exploration
Medieval Faires -> Humanism
Guilds -> Diplomatic Service
Guilds + Divine Right -> Reformed Church
Humanism -> Mercantilism
Humanism + Diplomatic Service -> The Enlightenment

Industrial/Modern:
Mercantilism -> Colonialism / Civil Engineering
The Enlightenment -> Nationalism / Opera and Ballet
Colonialism -> Natural History
Nationalism -> Scorched Earth
Civil Engineering + Nationalism -> Urbanization
Natural History -> Conservation
Natural History + Urbanization -> Mass Media
Urbanization + Scorched Earth -> Mobilization
Mass Media -> Capitalism
Mass Media + Mobilization -> Ideology
Ideology -> Nuclear Program / Suffrage / Totalitarianism / Class Struggle / Cold War / Professional Sports

Atomic/Information:
Conservation -> Cultural Heritage
Cold War -> Rapid Deployment / Space Race
Professional Sports + Space Race -> Social Media
Rapid Deployment + Space Race -> Globalization
Cultural Heritage + Rapid Deployment -> Environmentalism
Environmentalism + Globalization -> Near Future Governance
Globalization + Social Media -> Venture Politics / Distributed Sovereignty / Optimization Imperative

## Government unlock spine

Code of Laws -> Chiefdom

Political Philosophy ->
- Autocracy
- Oligarchy
- Classical Republic

Divine Right -> Monarchy
Exploration -> Merchant Republic
Reformed Church -> Theocracy

Suffrage -> Democracy
Totalitarianism -> Fascism
Class Struggle -> Communism

Venture Politics -> Corporate Libertarianism
Distributed Sovereignty -> Digital Democracy
Optimization Imperative -> Synthetic Technocracy

## How this should be used in our 12-era project

Do NOT redesign the whole social system first.

Preferred procedure:
1. preserve every useful Civ VI civic and its original prerequisite relationship;
2. move the civic into one of our 12 historical eras when Civ VI's era is too coarse;
3. insert new civics only where our extra eras create a real historical gap;
4. keep Civ VI policy cards and major unlocks unless there is a clear reason to replace them;
5. rescale Culture costs only after the 12-era tree is final;
6. adapt Inspiration conditions only when the original condition conflicts with our map, units, tech tree or historical timing.

Our eras:
Ancient -> Classical -> Late Antiquity -> Early Medieval -> High Medieval -> Renaissance -> Exploration -> Enlightenment -> Industrial -> Modern -> Atomic -> Information.

The biggest Civ VI decompositions will therefore occur between:
- Classical and Medieval: insert Late Antiquity + Early Medieval + High Medieval
- Renaissance and Industrial: separate Renaissance + Exploration + Enlightenment
- Industrial/Modern: redistribute Civ VI Industrial/Modern civics across our Industrial and Modern eras

## Source basis

Primary game-data/reference sources used:
- Civilopedia.net Gathering Storm civic pages and government/policy pages
- Civilization Wiki Gathering Storm civic/era data tables
- CivFanatics Civilization VI Civics tree reference for the original prerequisite graph
- Civilization VI official/manual descriptions for civic-tree mechanics

Reference URLs:
https://www.civilopedia.net/en-US/gathering-storm/civics/intro/
https://www.civilopedia.net/en-US/gathering-storm/concepts/culture_4/
https://www.civilopedia.net/en-US/gathering-storm/concepts/govt_1
https://civilization.fandom.com/wiki/List_of_civics_in_Civ6
https://civilization.fandom.com/wiki/Module:Data/Civ6/GS/Civics
https://civfanatics.com/civ6/info/civic/

See civ6_gs_civics_reference.csv for row-level content.
