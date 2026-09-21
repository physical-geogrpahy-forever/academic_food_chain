# Gathering Storm Future Era Realignment V1

Date: 2026-09-21  
Status: **LOCKED / AUTHORITATIVE LATE-ERA OVERRIDE**

The project restores Civilization VI: Gathering Storm's separate **Future Era** while retaining the existing totals of 109 technologies and 72 civics.

## Technology era split

Atomic: **5**
- Computers
- Nuclear Fission
- Synthetic Materials
- Ecology
- Particle Physics

Information: **9**
- Telecommunications
- Satellites
- Guidance Systems
- Lasers
- Composites
- Stealth Technology
- Robotics
- Nuclear Fusion
- Nanotechnology

Future: **8**
- Advanced AI
- Advanced Power Cells
- Cybernetics
- Smart Materials
- Predictive Systems
- Seasteads
- Offworld Mission
- Future Tech

## Civic era split

Atomic: **5**
- Nuclear Program
- Cultural Heritage
- Cold War
- Rapid Deployment
- Space Race

Information: **7**
- Globalization
- Social Media
- Near Future Governance
- Venture Politics
- Distributed Sovereignty
- Optimization Imperative
- Environmentalism

Future: **6**
- Information Warfare
- Global Warming Mitigation
- Cultural Hegemony
- Smart Power Doctrine
- Exodus Imperative
- Future Civic

## Science-victory / space-project chain

The project removes the old mixed Civ V spaceship-part abstraction and uses a Gathering Storm-style project sequence:

1. Rocketry + Space Race -> **Launch Earth Satellite**
2. Satellites + Space Race -> **Moon Landing**
3. Nanotechnology + Space Race -> **Launch Mars Colony**
4. Smart Materials + Exodus Imperative -> **Exoplanet Expedition**
5. Offworld Mission + Exodus Imperative -> **Terrestrial Laser Station / Lagrange Laser Station**
6. Future Tech remains repeatable.

Old authoritative references to **SS Engine** and **SS Stasis Chamber** are superseded.

## Late military realignment

Information-era late units:
- Stealth Bomber
- Jet Fighter
- Mobile SAM
- Modern AT
- Modern Armor
- Guided Missile
- Missile Cruiser
- Giant Death Robot

Atomic:
- Spec Ops -> Radar + Rapid Deployment

Future:
- XCOM Squad -> Cybernetics + Rapid Deployment

### Giant Death Robot

GDR is restored to the baseline:
- Robotics -> Giant Death Robot
- Advanced AI -> Drone Air Defense
- Advanced Power Cells -> Particle Beam Siege Cannon
- Cybernetics -> Enhanced Mobility
- Smart Materials -> Reinforced Armor

The former optional GDR module is superseded.

Integrated Attack Logistics restores its Gathering Storm-style baseline:
- +1 Movement to units beginning their turn in enemy territory
- +50% Production toward Giant Death Robots

## Infrastructure movement

Information:
- Wind Farm -> Composites + Environmentalism
- Solar Farm -> Ecology + Environmentalism
- Geothermal Plant -> Ecology + Environmentalism
- Flood Barrier -> Ecology + Environmentalism
- Recycling Center -> Ecology + Environmentalism
- Solar Plant -> Ecology + Environmentalism

Future:
- Grid Battery Storage -> Advanced Power Cells + Global Warming Mitigation
- Offshore Wind Farm -> Predictive Systems + Environmentalism
- Seastead -> Seasteads

The era label follows the latest required technology/civic gate.

## Policy split

Information: **6 policy cards**  
Future: **8 policy cards**

Future:
- Integrated Attack Logistics
- Rabblerousing
- Hallyu
- Non-State Actors
- Diplomatic Capital
- Global Coalition
- Aerospace Contractors
- Space Tourism

## Totals after realignment

- technologies: **109**
- civics: **72**
- generic non-Great-Person units: **89**
- policy cards: **127**
- generic buildings: **102**
- generic map improvement/infrastructure records: **39**

Unit era counts:
- Ancient 14
- Classical 6
- Late Antiquity 3
- Early Medieval 1
- High Medieval 4
- Renaissance 5
- Exploration 10
- Enlightenment 2
- Industrial 12
- Modern 18
- Atomic 5
- Information 8
- Future 1

## Validation

Cross-system validation: **PASS**

Checked:
- technology nodes: 109
- civic nodes: 72
- unit rows: 89
- policy rows: 127
- map/infrastructure rows: 39
- building rows: 102
- missing technology/civic references: 0
- backward-era prerequisite edges: 0
- content placed earlier than its latest unlock gate: 0

Additional cleanup found during validation:
- Spec Ops era corrected from Modern to Atomic because Rapid Deployment is Atomic.
- Coal Power Plant and Steelworks no longer misuse Industrialization as a civic gate; Industrialization is inherited through their Factory / Power Plant prerequisite chain.

This file supersedes all earlier statements that:
- Gathering Storm Future technologies are folded into Information;
- Giant Death Robot is optional/nonbaseline;
- XCOM Squad unlocks at Nanotechnology;
- SS Engine / SS Stasis Chamber are part of the authoritative space-victory chain.
