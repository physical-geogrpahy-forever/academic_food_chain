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

## Technology integration

JFD's base Great Works of Film mod does not require the project to copy a specific tech name, but MoreTech explicitly unlocks the Great Director / Great Works of Film system at **Cinematography**.

This creates a concrete implementation gap in the current technology tree.

Therefore:
- Cinematography is now a **strong technology-addition candidate**.
- It should be evaluated together with Photography before inserting it into the locked technology DAG.
- likely placement: late Industrial / early Modern boundary.
- Great Director availability should begin only after the film-production technology gate is reached.

No technology is added in this document yet; the technology tree must be updated in a separate audited step.

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
