# Great Person Recruitment System V2

Date: 2026-09-24
Status: LOCKED DESIGN DIRECTION

Supersedes:
- `city_system/FINAL_GREAT_PERSON_RECRUITMENT_SYSTEM_V1.md`

## 1. Core hybrid principle

The project preserves Civilization V-style generation sources where they fit, while recruitment uses named historical individuals who are globally unique.

The generation source differs by Great Person class. A historical person may be recruited only once worldwide.

## 2. Final class acquisition model

| Great Person class | Generation / purchase source | Recruitment model |
|---|---|---|
| Great Scientist | Scientist specialist/building GPP | Global named candidate competition |
| Great Philosopher | Institution-diversity GPhP, no dedicated specialist | Global named candidate competition |
| Great Engineer | Engineer specialist/building GPP | Global named candidate competition |
| Great Merchant | Merchant specialist/building GPP | Global named candidate competition |
| Great Writer | Writer specialist/building GPP | Global named candidate competition |
| Great Artist | Artist specialist/building GPP | Global named candidate competition |
| Great Musician | Musician specialist/building GPP | Global named candidate competition |
| Great Director | Director specialist/building GPP | Global named candidate competition |
| Great Prophet | Faith purchase | Globally unique named Prophet candidate |
| Great General | Land-combat points | Global named candidate competition |
| Great Admiral | Naval-combat points | Global named candidate competition |
| Great Revolutionary | Political-event GReP held by political unit | Context-filtered globally unique candidate pool |

## 3. Five generation models

The project therefore has five Great Person generation models:

1. specialist/building GPP;
2. institution-diversity GPhP;
3. combat GPP;
4. direct Faith purchase;
5. political-event / political-condition GReP.

All resolve to globally unique named historical people, but Great Revolutionary uses a context-filtered candidate pool rather than a single unconditional queue.

## 4. Specialist/building GPP classes

Great Scientist, Engineer, Merchant, Writer, Artist, Musician and Director retain class-specific specialist/building point generation.

City contributions sum to a civilization-wide class pool. Birth/source city may still be tracked.

Overflow is retained unless a later class-specific balance rule explicitly supersedes it.

## 5. Great Philosopher

No Philosopher specialist exists.

Each city activates philosophical institution chains. City GPhP is:

```text
max(0, number_of_distinct_active_thought_chains - 1)
```

Same-chain buildings do not stack for generation.

Authority:
- `city_system/great_philosophers/GREAT_PHILOSOPHER_SYSTEM_V1.md`

## 6. Great Prophet

Great Prophet does not use Prophet GPP.

```text
Faith generation -> Faith purchase -> globally unique named Great Prophet
```

Prophet remains distinct from Great Philosopher.

The old Prophet-only Holy Site consumption model is not restored; Holy Site is already a worker-built improvement in this project.

## 7. Great General and Great Admiral

Great General:

```text
land combat -> Great General points -> named candidate competition
```

Great Admiral:

```text
naval combat -> Great Admiral points -> named candidate competition
```

Neither requires a city specialist.

## 8. Great Revolutionary

Great Revolutionary does not use a generic specialist.

```text
political organization / ideology
+
grievance / political crisis
+
major political events
-> political-unit GReP
-> context-filtered named Great Revolutionary recruitment
```

Important distinctions:
- sovereign states and colonial governments may have separate GReP pools;
- low Happiness alone does not generate GReP;
- ordinary voluntary government switching does not generate GReP;
- historical candidates are globally unique;
- candidate availability depends on era, movement type and political context;
- default Great Revolutionary is a political-person entity rather than a roaming civilian unit.

Quantitative authority:
- `city_system/great_revolutionaries/GREAT_REVOLUTIONARY_SYSTEM_V2.md`
- `city_system/great_revolutionaries/GREP_EVENT_VALUES_V1.csv`
- `city_system/great_revolutionaries/GREP_RECRUITMENT_THRESHOLDS_V1.csv`

## 9. Great Philosopher / Great Revolutionary boundary

A thinker is not moved into Great Revolutionary merely because later movements used that person's ideas.

Use Great Philosopher when the representative historical achievement is theory, political philosophy, social philosophy, economics, ethics or related conceptual work.

Use Great Revolutionary when the representative historical achievement is practical political organization, mobilization, independence struggle, revolutionary government or direct social transformation.

A Great Philosopher may generate or modify GReP without being duplicated in the Revolutionary roster.

## 10. Historical identity and de-duplication

A named historical person may appear in only one primary Great Person class.

Cross-class audits are required among at least:
- Great Scientist;
- Great Philosopher;
- Great Engineer;
- Great Merchant;
- Great Writer;
- Great Prophet;
- Great General;
- Great Revolutionary;
- civilization leaders where the same person would create an identity conflict.

Historical uniqueness is global within a single game.

## 11. Pass and patronage

Specialist/building GPP classes may use Civ VI-style Pass mechanics after numerical balance is locked.

Great Prophet does not require a GPP Pass because the player can simply retain Faith.

Great General and Great Admiral follow their named-candidate queues; exact pass rules remain a later numerical decision.

Great Revolutionary does not use a generic Pass button. If the offered historical candidates are poor fits, the political unit may hold GReP and wait for the political context or candidate pool to change.

## 12. Gold / Faith patronage

Gold/Faith patronage for normal GPP classes remains a later balance option.

Exceptions:
- Great Prophet already uses Faith as the primary recruitment currency and therefore has no second Faith-patronage layer.
- Great Revolutionary does not use Gold/Faith patronage by default; political events and GReP are intended to remain the acquisition route.

## 13. Current content state

Great Philosopher:
- system design locked;
- current active roster 220 according to `great_philosophers/WORK_STATE.md`;
- consolidated summary regeneration and later cross-class review remain.

Great Revolutionary:
- system V2 and Standard-speed GReP values locked;
- historical roster not yet built;
- candidate tags and unique abilities remain the next content pass.

Other classes retain their existing work-state documents and require later cross-class de-duplication.
