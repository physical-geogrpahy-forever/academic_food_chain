# Industrial Technology + Civic Unlock Audit V1 — Part A

Date: 2026-09-21
Status: **PART A COMPLETE — 8 technologies + 4 civics**

This part covers:
Industrialization, Steam Power, Sanitation, Rifling, Replaceable Parts, Steel, Refining, Electricity;
Civil Engineering, Nationalism, Scorched Earth, Urbanization.

## Key decisions

- Factory stays at Industrialization.
- Coal reveal stays at earlier Manufacturing, avoiding a duplicate Industrialization reveal.
- Steam Power gives Ironclad and transport/logging improvements; Railroad is reserved for the dedicated Railroad technology.
- Sanitation is fully integrated with the Health & Plague concept: Sewer, public-health system and plague-risk reduction.
- Rifleman is placed at Rifling.
- Replaceable Parts gives mechanized agriculture and cross-gates Infantry with Nationalism.
- Steel provides Steelworks, Artillery with Military Science, and urban-defense modernization with Civil Engineering.
- Refining reveals Oil and unlocks Oil Well.
- Electricity provides electric power infrastructure and remains the locked Great Director / Film gate.

## Health & Plague integration

The adopted Health & Plague source makes city health depend on fresh water, resources/features, population, buildings and technologies, while negative health raises plague risk and road/sea connections accelerate spread.

Industrial implementation:
- **Sanitation + Civil Engineering -> Sewer**
- **Sanitation + Urbanization -> Modern Public Health**
- Sanitation sharply reduces plague risk, exact coefficient deferred.
- Urbanization raises connectivity/crowding disease risk unless offset by health infrastructure.
- Medic moves from Military Science to **Sanitation + Military Training**.
- Hospital remains deferred to Biology.

The source mod's Academy plague cure is still rejected because Great Scientist Academy tile improvements do not exist in this project.

## Power and industry

Coal was already revealed at Manufacturing.

Industrialization:
- Factory
- Mine production upgrade

Electricity:
- Power Plant + Civil Engineering
- Coal Power Plant + Industrialization
- existing Dam -> Hydroelectric Dam upgrade with Civil Engineering

This prevents Coal Power Plant from appearing before the Electricity technology.

## Corporation integration

Imported unchanged from the corporation map:
- Industrialization + Capitalism -> Construction Materials
- Industrialization + Capitalism -> Trading Houses & Industrial Investment
- Steam Power + Capitalism -> Shipping & Logistics
- Replaceable Parts + Capitalism -> Machinery & Precision Components
- Steel + Capitalism -> Steel & Heavy Materials
- Steel -> Construction Materials sector upgrade
- Refining + Capitalism -> Petroleum Refining
- Electricity + Capitalism -> Electrical Equipment & Power Systems
- Electricity + Capitalism -> Film, Media & Entertainment

## Authority files

- `tech_reference/industrial_tech_civic_unlock_audit_v1_part_a.csv`
- `tech_reference/technology_unlock_summary_industrial_v1_part_a.csv`
- `civics_reference/civic_unlock_summary_industrial_v1_part_a.csv`

Part B will cover:
Mass Production, Fertilizer, Biology, Dynamite, Railroad, Refrigeration, Telegraph, Armor Plating;
Conservation, Mass Media, Capitalism, Romanticism, Labor Movement.
