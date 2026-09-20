# Civic Tree Locked V1 — 72-node prerequisite DAG

Date: 2026-09-20  
Status: LOCKED GRAPH BASELINE

## Validation result

- Nodes: 72
- Root nodes: 1 — Code of Laws only
- Reachable from Code of Laws: 72/72
- Missing prerequisite references: 0
- Directed cycles: 0
- Era-backward prerequisite edges: 0
- Isolated civics (no prerequisite and no successor): 0
- Maximum prerequisite count on any node: 2
- Terminal branch nodes in the reference graph: Suffrage, Totalitarianism, Class Struggle, Future Civic

The four non-repeatable terminal branches — Suffrage, Totalitarianism, Class Struggle, Nuclear Program — are intentional unlock/end branches, not disconnected nodes. Future Civic is the repeatable terminal node.

## New-node insertion rules now locked

### Early Medieval to Renaissance
- Civil Service + Theology -> Written Culture
- Written Culture + Feudalism -> Court Culture
- Written Culture + Guilds -> Scholasticism
- Medieval Faires + Scholasticism -> Humanism
- Court Culture + Humanism -> Patronage
- Humanism -> Print Culture

This inserts the new civics without creating a second independent tree.

### Exploration
- Divine Right + Print Culture -> Reformed Church
- Humanism + Naval Tradition -> Mercantilism
- Mercantilism + Exploration -> Colonialism
- Print Culture + Exploration -> Scientific Revolution
- Diplomatic Service + Reformed Church -> Sovereignty

### Enlightenment
- Humanism + Diplomatic Service -> The Enlightenment
- The Enlightenment + Patronage -> Opera and Ballet
- Colonialism + Scientific Revolution -> Natural History
- The Enlightenment + Sovereignty -> Constitutionalism
- The Enlightenment + Print Culture -> Public Sphere

### Industrial and later
- Public Sphere -> Nationalism
- Opera and Ballet + Natural History -> Romanticism
- Capitalism -> Labor Movement
- Ideology + Constitutionalism -> Suffrage
- Ideology + Labor Movement -> Class Struggle
- Conservation + Romanticism -> Cultural Heritage
- Ideology + Nuclear Program -> Cold War

## Civilization VI preservation notes

Most Civilization VI prerequisite edges are retained exactly.

Where a new project civic was inserted, the old Civ VI dependency is preserved transitively rather than always directly. Examples:
- Guilds -> Humanism becomes Guilds -> Scholasticism -> Humanism.
- Guilds -> Reformed Church is represented through the expanded Renaissance/print branch while Divine Right remains an immediate prerequisite.
- The Enlightenment -> Nationalism becomes The Enlightenment -> Public Sphere -> Nationalism.

Other edges gain one historically useful extra prerequisite:
- Mercantilism additionally requires Naval Tradition.
- Colonialism additionally requires Exploration.
- Natural History additionally requires Scientific Revolution.
- Suffrage additionally requires Constitutionalism.
- Class Struggle additionally requires Labor Movement.
- Cultural Heritage additionally requires Romanticism.
- Cold War additionally requires Nuclear Program.

## Future-civic randomization

Gathering Storm randomizes the Future Era technology/civic progression each game. The project keeps that behavior even though those nodes are folded into the project's Information Era.

The CSV stores a **reference topology only** for QA.

Runtime random template:
- frontier F0-F3 = shuffled Near Future Governance / Venture Politics / Distributed Sovereignty / Optimization Imperative
- future A-E = shuffled Information Warfare / Global Warming Mitigation / Cultural Hegemony / Smart Power Doctrine / Exodus Imperative
- A requires F0 + F1
- B requires F2 + F3
- C requires A + F2
- D requires B + F1
- E requires C + D
- Future Civic requires E

This guarantees for every shuffle:
- all five future civics are connected;
- all four Information-era frontier civics participate;
- no cycle is possible;
- every future civic is required before Future Civic;
- no future branch is isolated;
- every node has at most two direct prerequisites.

## Era counts

- Ancient: 7
- Classical: 5
- Late Antiquity: 4
- Early Medieval: 4
- High Medieval: 4
- Renaissance: 4
- Exploration: 6
- Enlightenment: 5
- Industrial: 9
- Modern: 6
- Atomic: 6
- Information: 12

Total: 72.

## Next design stage

The roster and prerequisite graph are now locked enough to proceed to content assignment:
1. governments and government slots;
2. policy cards;
3. civic Inspirations;
4. buildings, wonders, units and diplomatic/religious unlocks;
5. Culture costs by era.

Do not add new civic nodes unless implementation exposes a concrete missing mechanic.
