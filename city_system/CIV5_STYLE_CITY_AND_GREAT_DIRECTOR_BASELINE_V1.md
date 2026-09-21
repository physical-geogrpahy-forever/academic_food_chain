# Civ V-style City System + Great Director Baseline V1

Date: 2026-09-20
Status: LOCKED DESIGN DIRECTION

## City system

The project uses a Civilization V-style city system rather than Civilization VI district placement.

Core rules:
- no map-placed Campus / Commercial Hub / Industrial Zone / Theater Square district puzzle;
- normal buildings are constructed directly inside the city;
- citizens work surrounding tiles or specialist slots;
- tile improvements remain on the map;
- technology/civic unlocks attach to city buildings, specialists, tile improvements, resources, units and systems rather than district adjacency.

Civilization VI content can still be reused, but district-dependent unlocks must be translated into Civ V-style city buildings or infrastructure.

Examples:
- Campus -> removed as a placed district; Library -> University -> Research Lab remain city buildings.
- Commercial Hub -> removed; Market -> Bank -> Stock Exchange remain city buildings.
- Industrial Zone -> removed; Workshop -> Factory -> Power Plant remain city buildings.
- Theater Square -> removed; Amphitheater / Museum / Broadcast-type buildings remain city buildings.
- Encampment -> removed as a placed district; Barracks -> Armory -> Military Academy remain city buildings.

## Great Director / Great Works of Film

The project will include the Civilization V Great Director / Great Works of Film concept.

Reference behavior from JFD's Great Works of Film:
- Great Director is a cultural Great Person.
- Citizens assigned as Directors at a Director's Guild generate Great Director points.
- Great Directors create Great Works of Film.
- Great Works of Film use dedicated Film slots.
- Cinema provides Film slots.
- World-wonder-specific Film slots are NOT automatically imported; all world wonders remain subject to separate wonder-quality audit.

## Project implementation direction

### Great Person
Great Director

Primary action:
- create a Great Work of Film.

Possible secondary action:
- culture / tourism burst or Golden Age-style cultural ability.
- exact secondary ability is not locked yet.

### Specialist
Director specialist

Generated/hosted by:
- Director's Guild or later film-industry building.

Purpose:
- yields Culture and/or Tourism;
- generates Great Director points.

### Building chain

Provisional Civ V-style city chain:
- Theater / Amphitheater cultural line
- Cinema
- Director's Guild or Film School / Studio-type institution
- later Broadcast / Media buildings

Exact prerequisite order and mutual exclusivity will be decided during building-tree design.

### Great Work type
Great Work of Film

Use:
- dedicated Film slots;
- Culture and Tourism;
- theming/collection bonuses can be considered later.

Great Works of Film should NOT simply make Great Works of Music obsolete. Film and Music need differentiated slot/building bonuses.

## Technology integration — FINAL

The project keeps the locked **109-technology V2 tree**.

**Photography and Cinematography are not added as separate technology nodes.**

For implementation:
- **Electricity** absorbs the late-19th-century photography / motion-picture production technology package.
- **Electricity unlocks the Great Director system, Cinema, Director specialist infrastructure, and Great Works of Film.**
- **Radio** is the later upgrade gate for broadcast/media expansion and later film/media corporate effects.

This preserves the 109-tech lock while giving film a historically usable late-Industrial entry point and keeping Radio for the later mass-media phase.

MoreTech remains a design reference for the Great Director / Cinematography concept, but the project does not copy its standalone Cinematography node.

## Wonder policy

Hollywood and any other film-related World Wonder are NOT automatically imported.

Wonder candidates will later be evaluated separately for:
- global historical significance;
- uniqueness;
- architectural/cultural recognizability;
- whether it is truly comparable to a world wonder rather than merely famous;
- gameplay distinctiveness.

This prevents source mods from determining the project's wonder roster automatically.

## Source references

- JFD — Great Works of Film (Civilization V mod)
- MoreTech — integrates Great Works of Film and unlocks Great Directors at Cinematography


## Former Great Person tile improvements — UPDATED

The earlier design assumption that Great Person tile improvements should be removed is superseded.

The project now keeps five former Civ V Great Person improvements as **nerfed ordinary Worker-built tile improvements**:

- Academy — Education
- Manufactory — Manufacturing
- Customs House — Economics + Mercantilism
- Holy Site — Theology
- Landmark — Humanism

Great People are not required or consumed.

The Great General **Citadel is the sole excluded former Great Person improvement**.

Military tile defense instead follows:
Fort -> Bastion Fort -> Advanced Fortification.

Natural History may also create archaeological Historic Landmarks from Antiquity Sites, distinct from the generic Humanism Landmark.

Authority:
`tile_system/FORMER_GREAT_PERSON_TILE_IMPROVEMENTS_V1.md`


## Great Person class scope — FINAL

The project will **not add any further Great Person classes** beyond the already adopted Great Director.

Baseline Great Person classes therefore remain:
- Great General
- Great Admiral
- Great Scientist
- Great Engineer
- Great Merchant
- Great Prophet
- Great Writer
- Great Artist
- Great Musician
- Great Director

Candidate mod classes such as Great Diplomat, Great Explorer, Great Doctor, Great Architect, Great Philosopher, Great Sculptor, Great Dignitary, Great Performer and related variants are **not adopted as separate Great Person classes**.

Their useful gameplay functions, if ever needed, should be represented through existing units, specialists, buildings, policies, projects or existing Great Person abilities rather than by expanding the Great Person-class roster.
