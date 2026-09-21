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

Technology-era migration moves associated units with their gates.

Information-era late units include:
- Stealth Bomber
- Jet Fighter
- Mobile SAM
- Modern AT
- Modern Armor
- Guided Missile
- Missile Cruiser
- **Giant Death Robot**

Future:
- **XCOM Squad** -> Cybernetics + Rapid Deployment

### Giant Death Robot

GDR is restored to the baseline:
- Robotics -> Giant Death Robot
- Advanced AI -> Drone Air Defense
- Advanced Power Cells -> Particle Beam Siege Cannon
- Cybernetics -> Enhanced Mobility
- Smart Materials -> Reinforced Armor

The former optional GDR module is superseded.

Integrated Attack Logistics returns to its Gathering Storm-style baseline:
- +1 Movement to units beginning their turn in enemy territory
- +50% Production toward Giant Death Robots

## Infrastructure movement

Information:
- Wind Farm -> Composites + Environmentalism

Future:
- Grid Battery Storage -> Advanced Power Cells + Global Warming Mitigation
- Offshore Wind Farm -> Predictive Systems + Environmentalism
- Seastead -> Seasteads

## Policy split

Information: 6 policy cards  
Future: 8 policy cards

Future policy-effect authority:
- `civics_reference/policy_balance/FUTURE_POLICY_EFFECTS_V1.csv`

## Totals after realignment

- technologies: **109**
- civics: **72**
- generic non-Great-Person units: **89**
- policy cards: **127**
- generic buildings: **102**
- generic map improvement/infrastructure records: **39**

This file supersedes all earlier statements that:
- Gathering Storm Future technologies are folded into Information;
- Giant Death Robot is optional/nonbaseline;
- XCOM Squad unlocks at Nanotechnology;
- SS Engine / SS Stasis Chamber are part of the authoritative space-victory chain.
