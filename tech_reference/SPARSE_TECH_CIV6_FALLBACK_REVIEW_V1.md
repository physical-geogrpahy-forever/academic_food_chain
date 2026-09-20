# Sparse Technology Civ VI Fallback Review V1

Date: 2026-09-21
Status: COMPLETE

Rule:
**Civ V first -> historical/functional reconciliation -> Civ VI fallback -> minimal historical invention**

The 109-tech master QA found 15 technologies with only a systems-note field and no separate unit/building/improvement/resource column.

This review checks every one against Civilization VI before adding any new historical content.

| Technology | Civ VI status | Civ VI generic content checked | Project resolution | Result |
|---|---|---|---|---|
| Astrology | CIV6_DIRECT | Shrine; Holy Site; Stonehenge | Shrine -> Mysticism; Holy Site removed; Stonehenge deferred | REVIEWED_NO_DUPLICATE |
| Calendar | NO_DIRECT_CIV6_NODE | - | Civ5 node retained for seasonal agriculture | REVIEWED_HISTORICAL/CIV5 |
| Horse Collar | NO_DIRECT_CIV6_NODE | - | Historical node; draft-animal labor role retained | REVIEWED_HISTORICAL |
| Algebra | NO_DIRECT_CIV6_NODE | - | Historical node; advanced calculation system retained | REVIEWED_HISTORICAL |
| Astrolabe | NO_DIRECT_CIV6_NODE | - | Historical node; navigation instrument system retained | REVIEWED_HISTORICAL |
| Square Rigging | CIV6_DIRECT | Frigate; +1 embarked movement; De Zeven Provinciën | Movement retained; Frigate -> Warships; unique unit remains unique | REVIEWED_NO_DUPLICATE |
| Ballistics | CIV6_DIRECT | Field Cannon; Cuirassier; Rough Rider | Field Gun -> Fortification; Cuirassier -> Military Science; unique unit remains unique | REVIEWED_NO_DUPLICATE |
| Fertilizer | NO_DIRECT_CIV6_NODE | - | Civ5 agricultural node retained | REVIEWED_CIV5 |
| Satellites | CIV6_DIRECT | Mechanized Infantry; Solar Farm; Moon Landing | Mechanized Infantry -> Combined Arms; Solar Farm -> Ecology+Environmentalism; Moon Landing retained with Space Race | REVIEWED_NO_DUPLICATE |
| Nuclear Fusion | CIV6_DIRECT | Operation Ivy; Thermonuclear Device; Mars Reactor | Ivy/device retained with Nuclear Program; Mars Reactor -> Offworld Mission | REVIEWED_NO_DUPLICATE |
| Advanced AI | CIV6_DIRECT | GDR Drone Air Defense upgrade | GDR optional; general Advanced AI decision system added instead | REVIEWED_CIV6_OPTIONAL |
| Cybernetics | CIV6_DIRECT | GDR Enhanced Mobility; Lumber Mill +1 Production | GDR optional; lumber bonus rejected as weak; Human-Machine Interface retained | REVIEWED_CIV6_OPTIONAL |
| Smart Materials | CIV6_DIRECT | GDR armor; Exoplanet Expedition; Mine production bonus | GDR optional; Exoplanet -> Offworld Mission; Mine bonus retained in systems note | REVIEWED_NO_DUPLICATE |
| Offworld Mission | CIV6_DIRECT | Terrestrial Laser Station; Lagrange Laser Station | Both retained; Mars/Exoplanet project family consolidated here | REVIEWED_CIV6_FILLED |
| Future Tech | CIV6_DIRECT | Repeatable +5% city project Production | Repeatable project-production bonus retained; score-victory reward dropped | REVIEWED_CIV6_FILLED |

## Result

- Materially empty technologies after consolidation: **0**
- Sparse technologies reviewed: **15/15**
- Sparse technologies requiring a new invented building/unit after Civ VI fallback: **0**
- Duplicate unlocks deliberately not restored.

Important examples:
- Astrology: Civ6 Shrine was consciously moved to Mysticism; Holy Site district is removed.
- Square Rigging: Civ6 Frigate is consciously owned by Warships because the adopted Enlightenment Era mod has a dedicated Warships node.
- Ballistics: Civ6 Field Cannon/Cuirassier already have project owners at Fortification/Military Science.
- Satellites: Civ6 content is distributed by function rather than duplicated.
- Advanced AI/Cybernetics: Civ6 mostly provides Giant Death Robot upgrades; because GDR is optional, the project uses broader general-purpose systems.
- Offworld Mission and Future Tech use Civ6 directly and are no longer content-empty.


## Additional sparse nodes created by cleanup

After removing moved/deferred placeholders from live unlock columns, three additional technologies became correctly classified as system-only sparse nodes.

| Technology | Source status | Source content checked | Project resolution | Result |
|---|---|---|---|---|
| Telecommunications | CIV6_DIRECT | Nuclear Submarine | Nuclear Submarine -> Nuclear Fission + Cold War; telecommunications retains network/system role | REVIEWED_NO_DUPLICATE |
| Robotics | CIV6_DIRECT | Giant Death Robot; Mars Habitation; Pasture yield | GDR optional; Mars Habitation -> Offworld Mission; automation role retained | REVIEWED_NO_DUPLICATE |
| Particle Physics | CIV5_DIRECT / NO SAME CIV6 NODE | SS Engine | SS Engine retained with Space Race; particle-physics system remains general scientific role | REVIEWED_CIV5 |

Current sparse reviewed set: **18 technologies**.
All are reviewed against Civ VI where a same or adjacent node exists, otherwise against the adopted Civ V source hierarchy.
