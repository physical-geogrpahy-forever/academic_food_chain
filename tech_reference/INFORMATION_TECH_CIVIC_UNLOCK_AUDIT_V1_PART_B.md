# Information Technology + Civic Unlock Audit V1 — Part B

Date: 2026-09-21
Status: **PART B COMPLETE — Information era and the full era-by-era unlock audit are complete**

## Explicit source rule

The project now uses:

**Civ V first -> historical/functional reconciliation -> Civ VI fallback -> minimal historical invention**

This is especially important in the Information/Future layer where Civilization V has far fewer generic unlocks.

## Seasteads

Civ6 Gathering Storm directly unlocks the generic Seastead improvement at Seasteads.

Final:
- **Seasteads -> Seastead**
- water-tile Food/Housing/productive settlement support
- Fishing Boats adjacency synergy
- Reef Culture/Tourism synergy can require Environmentalism

This is kept as an ordinary tile improvement on the Civ V-style hex map.

The Civ6 Diplomatic Victory point for researching the technology is not retained.

## Offworld Mission

Civ6 Gathering Storm directly unlocks:
- Terrestrial Laser Station
- Lagrange Laser Station

Both are retained as city projects requiring:
**Offworld Mission + Exodus Imperative + Space Launch Center**

Previously deferred space projects are consolidated here:
- Mars Colony
- Mars Hydroponics
- Mars Habitation
- Mars Reactor
- Exoplanet Expedition

Supporting technologies such as Nanotechnology, Robotics, Nuclear Fusion and Smart Materials remain in the prerequisite chain, but the actual offworld program is centralized under the dedicated Offworld Mission technology.

## Future Tech

Civ6 Future Tech is repeatable and grants a cumulative city-project Production bonus.

Final:
- Repeatable Future Research
- repeatable city-project Production bonus

The Civ6 +5% per completion is a valid starting reference, but a cap or diminishing return may be needed.

Score Victory points are not retained unless the project later explicitly adopts a Score Victory system.

## Information Warfare

Civ6 provides:
- Integrated Attack Logistics
- Rabblerousing

Both are retained.

Because Giant Death Robot is only optional in this project, Integrated Attack Logistics is generalized into networked logistics/advanced robotic-unmanned unit support rather than remaining a GDR-only card.

Additional identity:
**Advanced AI + Information Warfare -> Cyber/Information Operations**

## Global Warming Mitigation

Civ6 directly provides:
- Carbon Recapture project
- +3 Envoys
- +1 Diplomatic Victory point.

Final:
- **Ecology + Global Warming Mitigation -> Carbon Recapture**
- carbon accounting/mitigation system
- +3 Envoys
- Grid Battery Storage support with Advanced Power Cells

Carbon Recapture's Civ6 Industrial Zone requirement is translated into a Factory/industrial-building requirement.

The Diplomatic Victory point is dropped unless that victory system is later adopted.

## Cultural Hegemony

Civ6 provides:
- Hallyu
- Non-State Actors

Both are retained.

Hallyu strengthens Rock Band promotion access.
Non-State Actors strengthens Spy promotion access.

The civic's broader role is Global Cultural Influence through music, media, Great Works and Tourism.

Rock Band is not re-unlocked here; it remains available from Cold War and is upgraded by Cultural Hegemony.

## Smart Power Doctrine

Civ6 provides:
- Diplomatic Capital
- Global Coalition

Both are retained.

The civic's general identity is:
**Smart Power Strategy**
mixing diplomacy, alliances, economic pressure and limited military power.

This is a strong example of Civ6 filling an otherwise sparse project civic without inventing an unnecessary building.

## Exodus Imperative

Civ6 provides:
- Aerospace Contractors
- Space Tourism

Both are retained/adapted.

Spaceport references become **Space Launch Center**.

Exodus Imperative is the institutional co-gate for all Offworld Mission projects.

## Future Civic

Civ6 Future Civic is repeatable.

Final:
- Repeatable Future Civic
- +50 Diplomatic Favor per completion if Diplomatic Favor is used.

Governor Title reward remains deferred because the project has not adopted the Governor system.

Score Victory points are not retained unless a Score Victory is explicitly designed.

## Full audit status

Era-by-era technology/civic unlock audit is now complete from:
Ancient
through
Information/Future.

Remaining work is no longer "which era has been researched?"

The next work should be:
1. consolidate all era files into master 109-technology and 72-civic unlock tables;
2. run duplicate/missing/unresolved-content QA;
3. resolve the deferred generic unit roster;
4. resolve numerical building/yield/Health values;
5. run separate Wonder/National Wonder audit.

## Authority files

- `tech_reference/information_tech_civic_unlock_audit_v1_part_b.csv`
- `tech_reference/technology_unlock_summary_information_v1_part_b.csv`
- `civics_reference/civic_unlock_summary_information_v1_part_b.csv`
