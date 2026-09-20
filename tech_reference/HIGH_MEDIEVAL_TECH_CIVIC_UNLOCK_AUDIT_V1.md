# High Medieval Technology + Civic Unlock Audit V1

Date: 2026-09-21
Status: **HIGH MEDIEVAL COMPLETE — 6 technologies + 4 civics**

## Final technologies

| Technology | Main result |
|---|---|
| Apprenticeship | Workshop; Mine +1 Production; Man-at-Arms with Military Training |
| Machinery | Crossbowman; improved Road movement; Lumber Mill production upgrade |
| Buttress | Dam as river-linked tile infrastructure; Buttressed Masonry |
| Education | University; Production to Science; Research Agreement with Scholasticism |
| Compass | Galleass; Harbor/trade-range upgrade; Fishing Boats +1 Gold |
| Physics | Trebuchet; siege-mechanics upgrade |

## Final civics

| Civic | Main result |
|---|---|
| Medieval Faires | Medieval Fair system; Aesthetics; Medina Quarter; Merchant Confederation |
| Guilds | Artists' Guild; Great Artist generation; craft-guild organization |
| Divine Right | Monarchy; Chivalry; Gothic Architecture |
| Scholasticism | Scholastic Exchange; allied city-state Science share; Research Agreements with Education |

## Major reconciliations

### Apprenticeship
Civilization VI unlocks Workshop, Industrial Zone, Man-at-Arms and +1 Production on Mines at Apprenticeship.

Final:
- **Apprenticeship -> Workshop**
- **Apprenticeship -> Mine +1 Production**
- **Apprenticeship + Military Training -> Man-at-Arms**

Industrial Zone is removed.

Workshop is a direct Civ V-style city building.

### Machinery
Civ V and Civ VI both associate Machinery with Crossbowman.

Final:
- **Machinery -> Crossbowman**
- **Machinery -> improved Road movement**
- **Machinery -> Lumber Mill production upgrade**

Lumber Mill itself remains at Construction from Classical V1, avoiding duplicate unlocks.

Civ V Ironworks remains deferred to the National Wonder audit.

### Buttress
Civ VI Gathering Storm unlocks the Dam district at Buttress.

The district form is removed.

Final:
**Buttress -> Dam as river-linked tile infrastructure**

The Dam is part of the normal map infrastructure system rather than a specialty district. Flood-control, irrigation, water-supply and eventual power-generation effects can be split across later technologies instead of all appearing immediately.

Buttress also establishes a **Buttressed Masonry** structural system for large masonry construction.

A generic universal Cathedral is not automatically introduced because that would over-generalize one religious architectural tradition. Monumental religious buildings can use religion-specific names and forms if added later.

### Education
Both Civ V and Civ VI unlock University at Education.

Final:
**Education -> University**

Campus is absent; University is built directly in the city and requires Library.

Civ V's ability to convert Production to Science is retained in concept.

Research Agreements are changed to:
**Education + Scholasticism -> Research Agreement**

This separates technical higher education from the institutional culture of scholarly exchange.

The Great Scientist **Academy tile improvement remains removed**.

### Compass
Civ V Compass unlocks Harbor, Galleass, longer sea trade routes, another trade route and +1 Gold on Fishing Boats.

Harbor is already an earlier city building under Celestial Navigation.

Final:
- **Compass -> Galleass**
- **Compass -> Fishing Boats +1 Gold**
- **Compass + Foreign Trade -> Harbor maritime trade-range upgrade**
- **Compass + Foreign Trade -> additional maritime trade capacity candidate**

Ocean crossing remains later at Astronomy.

### Physics
Civ V Physics unlocks Trebuchet.

Late Antiquity V1 deliberately deferred Trebuchet from Military Engineering.

Final:
**Physics -> Trebuchet**

Notre Dame remains a World Wonder candidate.

## Medieval Faires
Civilization VI Medieval Faires unlocks:
- Aesthetics
- Medina Quarter
- Merchant Confederation

These are retained but adapted to the Civ V-style city structure.

Aesthetics:
- no Theater Square adjacency;
- later translated into cultural-building efficiency.

Medina Quarter:
- no specialty-district-count requirement;
- replace with a developed-city/building threshold.

Merchant Confederation transfers cleanly.

The civic also receives a **Medieval Fair** system:
- requires an existing Market/trade economy;
- represents periodic fairs rather than a permanent district;
- exact project/event implementation and yields remain open.

## Guilds
Civilization V BNW has an Artists' Guild unlocked by the Guilds technology. The project has moved Guilds to the civic tree.

Final:
**Guilds -> Artists' Guild**

Artists' Guild remains one per civilization and generates Great Artist points/specialists.

Civilization VI Guilds provides:
- Craftsmen
- Town Charters
- Traveling Merchants

These are retained as adapted policy candidates.

Craft Guild Organization becomes a cross-tree concept:
**Apprenticeship + Guilds**

This may later improve Workshops and Great Engineer/Merchant generation without adding a redundant generic Guild Hall building.

## Divine Right
Civilization VI Divine Right directly unlocks:
- **Monarchy**
- Chivalry policy
- Gothic Architecture policy

All three are retained.

Tier-2 Government Plaza buildings are not assigned solely to Divine Right because Merchant Republic and Theocracy will appear through other civic paths. They must be audited together after all Tier-2 governments are available.

## Scholasticism
Scholasticism is a project civic, but Civilization V already has a Patronage policy of the same name.

Civ V Scholasticism causes allied city-states to contribute Science.

That concept is retained as:
**Scholastic Exchange / Allied City-State Science Share**

The original Civ V 25% coefficient is not locked yet.

Scholasticism also cross-gates:
**Education + Scholasticism -> Research Agreement**

No extra generic 'Scholastic Academy' building is created because University already occupies that role.

## Great Person tile improvements

No Great Person tile improvement is restored.

In particular:
- Academy remains removed.
- Artists' Guild generates Great Artists without creating an Artist super-tile.
- Great Scientists continue to use non-tile active/system abilities.

## Authority files

- `tech_reference/high_medieval_tech_civic_unlock_audit_v1.csv`
- `tech_reference/technology_unlock_summary_high_medieval_v1.csv`
- `civics_reference/civic_unlock_summary_high_medieval_v1.csv`
