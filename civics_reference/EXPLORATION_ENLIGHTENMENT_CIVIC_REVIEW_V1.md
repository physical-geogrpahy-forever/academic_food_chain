# Exploration and Enlightenment civic review V1

Date: 2026-09-20
Status: LOCKED

## Locked source precedence

1. Civilization VI Gathering Storm
2. Civilization V BNW
3. older Civilization V policy material and Civ V era-expansion mods
4. original historical additions only where the above leave a real gap

If a name or function is already represented by a Civ VI civic, government or policy card, the Civ VI implementation takes priority.

## Corrected Civ VI spine

Important correction found during this audit:
- Humanism requires BOTH Medieval Faires and Guilds in Gathering Storm.
- Diplomatic Service requires Guilds.
- Exploration requires Mercenaries + Medieval Faires.
- Reformed Church requires Guilds + Divine Right.
- Mercantilism requires Humanism.
- The Enlightenment requires Humanism + Diplomatic Service.
- Colonialism requires Mercantilism.
- The Enlightenment leads to Nationalism and Opera and Ballet.

The earlier local reference that listed Humanism as requiring Medieval Faires only has been corrected.

## Exploration Era, 16th-17th centuries

### Existing Civ VI nodes retained

- Exploration
- Reformed Church
- Mercantilism
- Colonialism

These already cover:
- oceanic exploration and merchant-republic government
- Reformation-era organized religious change and Theocracy
- state-directed mercantile economy
- overseas colonial systems

### Candidate 1 — Scientific Revolution

Source:
- Civilization V Rationalism policy
- Civ V Civilopedia explicitly describes the European scientific revolution beginning in the 16th century with Copernicus and Vesalius

Verdict:
STRONG CANDIDATE

Reason:
- not an exact Civ VI civic
- Civ VI The Enlightenment is a broader 18th-century civic
- gives the project's 16th-17th century Exploration Era its intellectual/scientific branch
- Print Culture already adopted in the Renaissance provides a natural predecessor

Preferred project edge:
Humanism + Print Culture -> Scientific Revolution

Possible successor:
Scientific Revolution -> The Enlightenment

### Candidate 2 — Sovereignty

Sources:
- Civilization V Rationalism policy
- Pouakai Enlightenment Era technology
- later VP Enlightenment Era revisions retain Sovereignty in the early-modern progression

Verdict:
STRONG CANDIDATE

Reason:
- Civ VI Diplomatic Service covers professional diplomacy, not sovereign state authority itself
- Civ VI Nationalism is later and represents nation-based political identity
- Enlightenment Era uses Sovereignty as a major early-modern state-development node and attaches state institutions/world diplomacy to it

Preferred project edge:
Diplomatic Service + Print Culture -> Sovereignty

Possible successor:
Sovereignty -> The Enlightenment

This keeps Sovereignty distinct from:
- Diplomatic Service = professional interstate relations
- Sovereignty = locus and institutionalization of state authority
- Nationalism = political identification of nation and people

### Rejected/held Exploration-era candidates

Absolutism:
- historically fits the 17th century
- but best treated as a government/policy configuration derived from Monarchy/Divine Right/Sovereignty rather than another mandatory universal civic
- HOLD for government-system design

Free Thought / Secularism:
- Civ V Rationalism policies
- conceptually contained by Civ VI The Enlightenment and its Rationalism/Liberalism policy content
- do not add separate civics

Imperialism:
- Pouakai Enlightenment Era uses it as a technology
- current 16th-17th century gameplay role overlaps Mercantilism + Colonialism
- HOLD for a possible distinct 19th-century Industrial civic, not Exploration

### Locked Exploration-era roster

1. Exploration — Civ VI
2. Reformed Church — Civ VI
3. Mercantilism — Civ VI
4. Colonialism — Civ VI, era moved
5. Scientific Revolution — Civ V import candidate
6. Sovereignty — Civ V / era-mod import candidate

## Enlightenment Era, 18th century

### Existing Civ VI nodes retained

- The Enlightenment
- Opera and Ballet
- Natural History

The Enlightenment already contains many ideas that should NOT become duplicate civics:
- rationalism
- religious/political skepticism
- social-contract thinking
- individual rights
- representative government

Civ VI also unlocks policy content such as Liberalism, Rationalism and Free Market around this part of the tree, so those should remain policy concepts instead of new civics.

### Candidate 1 — Constitutionalism

Sources:
- Civilization V originally had Constitution as a Freedom social policy
- Constitution was removed when BNW converted Freedom into an Ideology, so it is a lower-priority Civ V source than BNW
- JFD Cultural Diversity also uses Constitutionalism as a later cultural-development concept

Verdict:
STRONG CANDIDATE FOR REVIEW

Reason:
- a constitution/constitutional order is an institution, not identical to the broader Enlightenment movement
- does not duplicate Civ VI Suffrage, which is placed much later and unlocks Democracy
- can represent codification and limitation/organization of political authority without forcing the Democracy government to appear in the 18th century

Preferred edge:
The Enlightenment + Sovereignty -> Constitutionalism

Possible later continuation:
Constitutionalism -> an Industrial/Modern representative-politics branch, ultimately connecting toward Suffrage

Do not use Civ V's old policy effect directly; only reuse the concept/name.

### Candidate 2 — Public Sphere

Source:
- historical addition after game-source audit
- Oxford and Cambridge scholarship treats the public sphere as a major social dimension of the Enlightenment, involving new reading publics, salons, coffeehouses, clubs, print circulation and public opinion
- Civ VI's own National Identity historical entry explicitly refers to the emergence of a public sphere in 18th-century Europe

Verdict:
STRONG ORIGINAL CANDIDATE

Reason:
- Print Culture represents the technological/social diffusion of printed material in the Renaissance
- The Enlightenment represents the intellectual movement
- Public Sphere represents the social institutions and audiences through which debate and opinion circulate
- therefore it fills a different gameplay/social role without duplicating either node

Preferred edge:
Print Culture + The Enlightenment -> Public Sphere

Possible successors:
Public Sphere -> Mass Media
Public Sphere -> Nationalism

This gives Print Culture a meaningful downstream connection and creates a long-term communication/civil-society line.

### Rejected/held Enlightenment candidates

Social Contract:
- historically central, but Civ VI The Enlightenment's own Civilopedia explicitly includes social-contract thinkers and representative government
- therefore it is contained by The Enlightenment under the Civ VI-priority rule

Liberalism:
- Civ VI already uses Liberalism as a policy card unlocked by The Enlightenment
- do not create duplicate civic

Rationalism:
- Civ VI already uses Rationalism as a policy card unlocked by The Enlightenment
- do not create duplicate civic

Free Market:
- Civ VI already uses Free Market as a policy card unlocked by The Enlightenment
- do not create duplicate civic

Free Speech:
- older Civ V Freedom policy, but its social function can be attached to Constitutionalism/Public Sphere as a policy card or effect
- do not add as a separate civic at this stage

Enlightened Absolutism:
- better handled as a government/policy configuration, not a universal civic

### Locked Enlightenment-era roster

1. The Enlightenment — Civ VI
2. Opera and Ballet — Civ VI
3. Natural History — Civ VI
4. Constitutionalism — Civ V-derived candidate
5. Public Sphere — historical candidate after game-source audit

## Proposed cross-era skeleton

Renaissance:
Humanism
Diplomatic Service
Patronage
Print Culture

Exploration:
Exploration
Reformed Church
Mercantilism
Colonialism
Scientific Revolution
Sovereignty

Enlightenment:
The Enlightenment
Opera and Ballet
Natural History
Constitutionalism
Public Sphere

Suggested new-node flow:

Humanism + Print Culture -> Scientific Revolution ----\
                                                       -> The Enlightenment
Diplomatic Service + Print Culture -> Sovereignty ----/

The Enlightenment + Sovereignty -> Constitutionalism
Print Culture + The Enlightenment -> Public Sphere

The Enlightenment -> Opera and Ballet
Colonialism -> Natural History

Public Sphere -> Mass Media / Nationalism
Constitutionalism -> later representative-politics line toward Suffrage

## Current recommendation

Locked additions:
- Scientific Revolution
- Sovereignty
- Constitutionalism
- Public Sphere

Do NOT add:
- Social Contract
- Rationalism
- Liberalism
- Free Market
- Free Speech
- Absolutism

as separate civic nodes at this stage, because they are either already represented by Civ VI civic content/policy cards or are better reserved for government/policy mechanics.


## Locked total civic counts by project era

- Ancient: 7
- Classical: 5
- Late Antiquity: 4
- Early Medieval: 4
- High Medieval: 4
- Renaissance: 4
- Exploration: 6
- Enlightenment: 5
- Industrial: 7
- Modern: 6
- Atomic: 6
- Information: 12
- Total: 70

Romanticism remains an unadopted Industrial-era candidate and is not included in the 70.
