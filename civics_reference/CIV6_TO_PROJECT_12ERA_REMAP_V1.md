# Civilization VI civics -> 12-era remap V1

Date: 2026-09-20
Status: review baseline

## Rule

Use Civilization VI: Gathering Storm as the skeleton.

For the imported 61 normal civics:
- keep the original civic identity;
- keep original prerequisite links unless an explicit later design decision changes them;
- keep policy-card, government and major unlock content as the default;
- keep the original Inspiration as a placeholder;
- after the science/technology tree is finalized, review Inspirations that refer to specific technologies, units, buildings or districts;
- change the era assignment where the project's 12-era chronology is finer than Civ VI;
- do not add new civics until this remap has exposed real gaps.

The project's eras are:
Ancient -> Classical -> Late Antiquity -> Early Medieval -> High Medieval -> Renaissance -> Exploration -> Enlightenment -> Industrial -> Modern -> Atomic -> Information.

## Mapping result

All 61 Civ VI Gathering Storm reference civics are retained.

| Project era | Civ VI civics assigned |
|---|---:|
| Ancient | 7 |
| Classical | 5 |
| Late Antiquity | 4 |
| Early Medieval | 2 |
| High Medieval | 3 |
| Renaissance | 2 |
| Exploration | 4 |
| Enlightenment | 3 |
| Industrial | 7 |
| Modern | 6 |
| Atomic | 6 |
| Information | 12 |
| **Total** | **61** |

The low counts in Early Medieval, High Medieval and Renaissance are intentional audit signals. They show where genuinely new civics may be needed; do not fill them yet by inventing content.

## Exact Civ VI graph preserved through the remap

### Opening
Code of Laws
-> Craftsmanship -> Military Tradition / State Workforce
-> Foreign Trade -> Early Empire / Mysticism

Political Philosophy requires State Workforce + Early Empire.
Military Training requires Military Tradition + Games and Recreation.
Defensive Tactics requires Games and Recreation + Political Philosophy.
Recorded History requires Political Philosophy + Drama and Poetry.
Theology requires Mysticism + Drama and Poetry.

### Late Antiquity / Medieval redistribution
Defensive Tactics -> Naval Tradition / Feudalism / Civil Service
Recorded History + Defensive Tactics -> Civil Service
Military Training + Feudalism -> Mercenaries
Feudalism -> Medieval Faires
Feudalism + Civil Service -> Guilds
Theology + Civil Service -> Divine Right

Only their era labels move. Their prerequisite graph remains the Civ VI graph.

### Renaissance / Exploration / Enlightenment redistribution
Mercenaries + Medieval Faires -> Exploration
Medieval Faires + Guilds -> Humanism
Guilds -> Diplomatic Service
Guilds + Divine Right -> Reformed Church
Humanism -> Mercantilism
Humanism + Diplomatic Service -> The Enlightenment
Mercantilism -> Colonialism / Civil Engineering
The Enlightenment -> Nationalism / Opera and Ballet
Colonialism -> Natural History

This is why Exploration, Mercantilism, Reformed Church and Colonialism can be moved into the project's 16-17C Exploration Era without rebuilding the tree.

### Industrial / Modern
Civil Engineering + Nationalism -> Urbanization
Nationalism -> Scorched Earth
Natural History -> Conservation
Natural History + Urbanization -> Mass Media
Urbanization + Scorched Earth -> Mobilization
Mass Media -> Capitalism
Mass Media + Mobilization -> Ideology
Ideology -> Suffrage / Totalitarianism / Class Struggle / Nuclear Program / Cold War / Professional Sports

Mass Media is placed in the project's 19C Industrial Era so that the Civ VI link Mass Media -> Capitalism is not reversed. This is also compatible with Civ VI Civilopedia's description of mass media as fundamentally an industrial-era phenomenon.

### Atomic / Information
Conservation -> Cultural Heritage
Ideology -> Cold War
Cold War -> Rapid Deployment / Space Race
Cultural Heritage + Rapid Deployment -> Environmentalism
Rapid Deployment + Space Race -> Globalization
Space Race + Professional Sports -> Social Media
Environmentalism + Globalization -> Near Future Governance
Globalization + Social Media -> Venture Politics / Distributed Sovereignty / Optimization Imperative

The five speculative Future-era branches and Future Civic are absorbed into the late Information Era because this project has no separate Future Era. Their randomized-future-tree character is retained rather than replaced by invented fixed links at this stage.

## Content-reuse rule

For now, every row is KEEP_ALL.

That means the following Civ VI content remains attached to the civic:
- policy cards;
- governments;
- diplomatic rules and Casus Belli;
- districts/buildings/wonders;
- unit or formation mechanics;
- governor/envoy/spy effects;
- Inspiration condition.

This is a labor-saving baseline, not a claim that every unlock will survive final design unchanged.

The technology tree comes next, so Inspirations or unlocks that refer to a Civ VI technology must be checked after that tree is imported/remapped.

## Government spine retained

Code of Laws -> Chiefdom

Political Philosophy ->
Autocracy / Oligarchy / Classical Republic

Divine Right -> Monarchy
Exploration -> Merchant Republic
Reformed Church -> Theocracy

Suffrage -> Democracy
Totalitarianism -> Fascism
Class Struggle -> Communism

Venture Politics -> Corporate Libertarianism
Distributed Sovereignty -> Digital Democracy
Optimization Imperative -> Synthetic Technocracy

## Important gap audit

The remap shows three historically expanded eras that are sparse:
- Early Medieval: 2 existing Civ VI civics
- High Medieval: 3
- Renaissance: 2

Late Antiquity already receives 4 existing Civ VI civics and therefore may need fewer additions than originally assumed.

The next civic-design task should therefore be:
1. inspect the actual functions already supplied by the 61 Civ VI civics;
2. list only functions missing from the sparse eras;
3. add the minimum number of new civics needed to bridge those gaps;
4. attach them by inserting them into existing Civ VI edges instead of rewriting the whole graph.

## Files

- `civ6_gs_civics_reference.csv`: imported Civ VI content reference
- `civ6_to_project_12era_remap_v1.csv`: exact 61-row era mapping
- this file: design/audit explanation

## Source precedence rule

When filling gaps with Civilization V material, use this precedence:

1. Civilization VI Gathering Storm civic takes priority whenever a Civ V policy/technology has the same name, substantially overlapping function, or is a narrower concept already contained inside the Civ VI civic.
2. Civilization V BNW social policies are used only for genuinely missing social/institutional concepts.
3. Civilization V BNW technologies are primarily technology-tree references and should become civics only when the concept is clearly institutional/social rather than scientific/technical.
4. If a Civ V candidate duplicates a Civ VI unlock or civic function, do not add a second civic. Keep the Civ VI civic and, if useful, reuse the Civ V idea as a policy card, Inspiration condition, flavor text, or unlock detail.
5. New original civics are added only after both Civ VI and Civ V reference pools have been checked.

Examples:
- Civ V Rationalism should not replace or duplicate Civ VI The Enlightenment if the intended function is already represented there; Rationalism can instead inform policy-card or content design.
- Civ V Monarchy should not create a duplicate civic if the government role is already handled by Civ VI Divine Right -> Monarchy.
- Civ V Legalism should not become a separate civic if its intended role is adequately contained by Code of Laws / Civil Service; it may be reused as a policy-card concept.
- Civ V Merchant Confederacy/merchant-oriented ideas should be checked against Guilds, Mercantilism, Exploration and Merchant Republic before any new civic is created.
