# CIVIC ROSTER LOCKED V1 — 72 civics

Date: 2026-09-20
Status: LOCKED ROSTER BASELINE

## Design rule

Civilization VI: Gathering Storm remains the primary skeleton.
Civilization V BNW, Civ V era-expansion mods and historical additions are used only where Civ VI leaves a real gap.

Priority:
1. Civ VI civic / government / policy content
2. Civ V BNW
3. Civ V era-mod content
4. historical original additions

Do not add a new civic when the same name, function, or a broader containing concept already exists in Civ VI.

## Locked era counts

| Project era | Count |
|---|---:|
| Ancient | 7 |
| Classical | 5 |
| Late Antiquity | 4 |
| Early Medieval | 4 |
| High Medieval | 4 |
| Renaissance | 4 |
| Exploration | 6 |
| Enlightenment | 5 |
| Industrial | 9 |
| Modern | 6 |
| Atomic | 6 |
| Information | 12 |
| **Total** | **72** |

## Locked additions beyond the imported Civ VI roster

Early Medieval:
- Written Culture
- Court Culture

High Medieval:
- Scholasticism

Renaissance:
- Patronage
- Print Culture

Exploration:
- Scientific Revolution
- Sovereignty

Enlightenment:
- Constitutionalism
- Public Sphere

Industrial:
- Romanticism
- Labor Movement

Total additions to the 61 imported Civ VI civics: 11.
61 + 11 = 72.

## Industrial Era locked roster

- Civil Engineering
- Nationalism
- Scorched Earth
- Urbanization
- Conservation
- Mass Media
- Capitalism
- Romanticism
- Labor Movement

### Labor Movement

Status: ADOPTED / LOCKED.

Reason:
- no exact Civilization VI civic duplicates it;
- it represents nineteenth-century organized labor, trade-union development and collective worker politics;
- it gives a historically coherent precursor to Civilization VI's later Class Struggle civic.

Provisional graph role:
Urbanization + Capitalism -> Labor Movement
Ideology + Labor Movement -> Class Struggle

## No further civic additions recommended at roster stage

The remaining apparent gaps are better handled by:
- policy cards,
- governments,
- buildings,
- units,
- wonders,
- religion mechanics,
- diplomacy mechanics,
- or the technology tree.

Examples that should NOT become new civic nodes now:
- Imperialism: overlaps substantially with Colonialism / Nationalism and may be expressed as policy or later-era content.
- Absolutism: better as government/policy configuration.
- Social Contract: contained within Civ VI The Enlightenment.
- Rationalism, Liberalism, Free Market: existing Civ VI policy-card concepts.
- Monasticism, Serfdom, Chivalry: already represented in Civ VI policy content or broader civics.
- Corporations: mostly contained by Capitalism unless a separate corporation system later requires an explicit mechanic.

## Next task

Do not add more civic names before graph validation.

Next:
1. assemble all 72 nodes into one prerequisite DAG;
2. preserve Civ VI edges wherever possible;
3. insert the 11 added nodes into existing edges rather than rewriting the tree;
4. ensure every non-root civic has at least one prerequisite;
5. ensure every node is reachable from Code of Laws;
6. detect era-backward edges;
7. detect cycles;
8. detect accidental dead ends;
9. review prerequisite burden for nodes with two or more prerequisites;
10. only after graph QA, assign/revise Inspirations and unlock content.

This file is the roster baseline for that graph work.
