> **SUPERSEDED — DO NOT IMPLEMENT THIS VERSION.** Current reviewed baseline: `civ_map_stage10_resources/contact_dynamic_resource_system_v2.md`\n\n# Contact-Based Dynamic Resource System V1

Date: 2026-09-20
Project: CIV game world map resource system
Status: design baseline for implementation

## 1. Core principle

Resource geography must not be controlled by a fixed historical year alone.
The game must allow alternate-history transfer when civilizations make contact earlier than in real history.

Example:
- In real history, horses and cattle reached the Americas through post-1492 trans-Atlantic contact.
- In the game, if a Korean civilization reaches South America in 1000 CE and establishes a settlement, resources already known and carried by Korea may be introduced there centuries earlier.
- Therefore a hard rule such as `HORSES_IN_AMERICAS = false before 1492` is not acceptable for gameplay.

The system must distinguish:
1. where a resource is naturally present,
2. where a resource has been domesticated or developed,
3. which civilizations know the resource,
4. which regions have been contacted,
5. whether transfer actually occurred,
6. whether the local environment can sustain the transferred resource,
7. whether the required technology exists to exploit it.

## 2. Resource-state model

Each map resource should use several independent state layers rather than one static present/absent layer.

### 2.1 Native layer
`native_presence[resource, hex]`

Meaning:
- Natural mineral deposit, wild species range, or original domestication/source area.
- This layer does not depend on player contact.
- Geological resources normally remain spatially fixed.
- Biological ranges may depend on era/climate if later paleogeographic support is added.

### 2.2 Known-resource layer
`civ_knows_resource[civ, resource]`

Meaning:
- The civilization recognizes the resource and knows how to use, cultivate, breed, trade, or extract it at the current technological level.

A civilization can acquire this through:
- starting knowledge,
- technological development,
- direct contact with another civilization,
- trade,
- conquest,
- exploration and discovery,
- settlement in a source region.

### 2.3 Introduction layer
`introduced_presence[resource, hex]`

Meaning:
- The resource is not native to the hex but has been introduced through human action.

Examples:
- Horses introduced into the Americas
- Cattle introduced into the Americas
- Maize introduced into Eurasia
- Tobacco introduced into East Asia
- Cotton introduced into Korea
- Coffee introduced outside its original African range

### 2.4 Exploitable layer
`resource_active[resource, hex, civ]`

Activation can require:
- deposit or introduced population exists,
- civilization knows the resource,
- required extraction/cultivation technology is available,
- environmental conditions are suitable,
- optional minimum infrastructure threshold is met.

## 3. Event routes that can transfer resources

### 3.1 Direct civilization contact
Meaningful contact can transfer knowledge of selected resources.
Contact alone does not automatically create the resource everywhere.

### 3.2 Trade
Sustained trade can transfer crop seed, livestock, domestication knowledge, processing knowledge, and luxury-resource knowledge.
Transfer can depend on trade duration, volume, transportability, environmental suitability, and technology.

### 3.3 Settlement and colonization
Settlement is the strongest introduction mechanism.

Example:
- Korea reaches South America in 1000 CE.
- Korea already knows and maintains horses, cattle, rice, and other transferable resources.
- A Korean settlement is founded.
- Horses and cattle can become introduced resources in environmentally suitable nearby cells.
- This can happen even though the historical Columbian Exchange has not occurred.

### 3.4 Exploration and discovery
Exploration may discover a native resource without formal contact with a local civilization.
Discovery can create `civ_knows_resource = true` without immediately creating introduced presence elsewhere.

### 3.5 Conquest or occupation
Conquest can transfer local resource knowledge to the conqueror and introduced resources from the conqueror into the occupied region.

## 4. Transferability classes

### Class A. Geological fixed resources
Examples: IRON, COAL, OIL, ALUMINUM, URANIUM, COPPER, GOLD, SILVER, MARBLE, SALT, GEMS, JADE, LAPIS_LAZULI, AMBER, STONE.

Rules:
- Cannot be introduced by trade or settlement.
- Location comes from geological evidence.
- Contact can reveal knowledge or extraction methods.
- Technology activates exploitation.

### Class B. Transferable domesticated plants
Examples: WHEAT, RICE, MAIZE, BANANAS, CITRUS, COTTON, SUGAR, COFFEE, TEA, TOBACCO, OLIVES, WINE/grape basis, transportable SPICES components.

Rules:
- Native/source region exists independently.
- Can be transferred after contact, trade, or settlement.
- Introduction requires environmental suitability.

### Class C. Transferable domesticated animals
Examples: HORSES, CATTLE, SHEEP.

Rules:
- Can move through migration, trade, conquest, or colonization.
- Introduced populations may spread from settlement cells into suitable neighboring cells.

### Class D. Wild biological resources
Examples: BISON, DEER, FURS, IVORY, FISH, CRAB, PEARLS, WHALES, CORAL, TRUFFLES.

Rules:
- Normally tied to natural range.
- Contact does not automatically create them elsewhere.
- Exploitation can begin after discovery and technology acquisition.

### Class E. Processed-display resources
Examples:
- COCOA displayed as Chocolate
- PERFUME displayed as Perfume

Rules:
- Internal geography remains tied to source ingredients or production inputs.
- Player-facing label may be the finished luxury good.
- Activation may require source resource plus processing technology.

## 5. Environmental suitability

Transferred biological resources should not appear automatically in every contacted region.

Use:

`S = climate_suitability × terrain_suitability × biome_suitability × technology_modifier`

An introduction succeeds only if `S >= threshold_resource`.

Example:
- Korean horses introduced to temperate South America: plausible if suitable.
- Bananas introduced to arctic tundra: fail.

## 6. Spatial spread after introduction

Suggested simple rule:

`P(spread to neighbor) = base_spread × suitability × connectivity × human_support`

Where:
- suitability = environmental suitability of target cell,
- connectivity is reduced by mountains, deserts, sea barriers, and distance,
- human_support is larger near settlements, roads, farms, ports, and trade routes.

Use discrete turns for a low-cost implementation.

## 7. Contact graph implementation

For each civilization pair:
- unknown
- encountered
- diplomatic contact
- trade contact
- sustained exchange
- political control / settlement

Implementation-test coefficients only:
- encountered: 0.05
- diplomatic contact: 0.15
- trade contact: 0.35
- sustained exchange: 0.60
- settlement/conquest: 0.90

These are gameplay parameters, not historical facts.

## 8. Resource transfer event

```text
for each contact event A -> B:
    for each transferable resource R known by A:
        if B does not know R:
            test knowledge transfer

for each settlement/trade node in region H:
    for each transferable resource R known by owner/trader:
        if R is not native in H:
            if suitability(R, H) >= threshold:
                test introduction
                if success:
                    introduced_presence[R,H] = true
```

## 9. Historical reality as default path, not hard-coded destiny

Historical introduction dates are default historical priors, not absolute locks.

Examples:
- Korean cotton becomes important after the late Goryeo introduction associated with 1363.
- Tobacco reaches Korea around the late 16th to early 17th century in the historical path.
- Horses and cattle reach the post-Columbian Americas through European contact in the historical path.

Alternate contact can move these dates.

## 10. Minimal data schema

```yaml
id: HORSES
transfer_class: domesticated_animal
native_source_layer: horses_native_v1
requires_knowledge: true
requires_technology: ANIMAL_HUSBANDRY
transferable_by:
  - trade
  - migration
  - settlement
  - conquest
environmental_suitability_model: horses_suitability_v1
spread_model: neighbor_human_assisted_v1
```

Per civilization:

```text
civ_id
resource_id
known
first_known_turn
knowledge_source_civ
knowledge_source_event
```

Per hex:

```text
hex_id
resource_id
native_presence
introduced_presence
first_introduction_turn
introduced_by_civ
introduction_event_id
active
```

## 11. Easy game-integration version

For the first implementation, use four checks:
1. Does the civilization know the resource?
2. Is the resource transferable?
3. Is the target hex suitable?
4. Was there a valid transfer event such as trade, settlement, conquest, or expedition?

If all four pass, add the resource to an introduction queue.
After a fixed delay, activate the resource in the target cell and optionally spread to adjacent suitable cells.

## 12. Important design lock

Do NOT implement a single global date switch such as:

```text
if year >= 1492: horses appear in Americas
```

Instead use:

```text
if valid_contact_or_settlement_event
and source_civ_knows_horses
and destination_is_suitable:
    horses_can_be_introduced
```

Historical dates validate the default historical path, while contact and transfer events control the actual game state.
