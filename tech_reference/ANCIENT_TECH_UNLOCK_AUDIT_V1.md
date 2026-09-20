# Ancient Technology Unlock Audit V1

Date: 2026-09-21  
Status: **ANCIENT 14 COMPLETE — content baseline**

This pass audits the project's 14 Ancient technologies against Civ V BNW, relevant Civ VI GS content, and the adopted mod/system rules.

## Final Ancient mapping

| Technology | Main final unlocks |
|---|---|
| Agriculture | Worker, Farm, starting core units |
| Pottery | Granary |
| Animal Husbandry | Pasture, Horses reveal, Caravan with Foreign Trade civic |
| Mining | Mine, forest clearing, mineral exploitation |
| Sailing | Work Boat, Trireme, Fishing Boats, Cargo Ship with Foreign Trade civic |
| Astrology | Shrine; early religion/Great Prophet access with Mysticism |
| Irrigation | Plantation; marsh clearing; fresh-water Farm +1 Food |
| Archery | Archer |
| Writing | Library |
| Masonry | Quarry, Walls, Stone Works, Battering Ram |
| Bronze Working | Spearman, Barracks, Iron reveal, jungle/rainforest clearing |
| Wheel | Road, Water Mill, Chariot Archer |
| Calendar | calendar/agricultural knowledge; no exclusive tile improvement |
| Trapping | Camp; Circus with Games and Recreation civic |

## Key reconciliation decisions

### Plantation
Civ V BNW places Plantation at Calendar, while Civ VI places it at Irrigation.

Final:
**Irrigation -> Plantation**

Reason:
Civ V remains the structural baseline for the city/tile model, but source-game unlock placement is not binding. Plantation establishment is more naturally grouped with managed water, cultivated perennial/cash crops and agricultural intensification. The project therefore follows functional and historical fit rather than mechanically copying Civ V's Calendar placement.

Calendar remains useful as a knowledge prerequisite/node in the technology tree without needing to own Plantation.

### Irrigation
The project has a dedicated Irrigation technology while Civ V put the fresh-water Farm bonus on Civil Service.

But project Civil Service is a civic.

Final:
**Irrigation -> marsh clearing + fresh-water Farms receive +1 Food**

This preserves the familiar Civ V fresh-water farm logic while putting the material technology on the science tree.

### Quarry
Civ VI places Quarry at Mining; Civ V places it at Masonry.

Final:
**Masonry -> Quarry**

### Stone Works
Civ V oddly attaches Stone Works to Calendar.

Final:
**Masonry -> Stone Works**

### Shrine / Astrology
Civ V places Shrine at Pottery; Civ VI places Shrine at Astrology.

Final:
**Astrology -> Shrine**

Full early religion access is cross-gated with the Ancient civic **Mysticism**.

### Trade routes
Civ V BNW attaches Caravan/trade access to Animal Husbandry and Cargo Ship/trade capacity to Sailing.

The project has a parallel civic tree.

Final:
- Animal Husbandry provides the physical **Caravan** capability.
- Sailing provides the physical **Cargo Ship** capability.
- actual organized trade access requires **Foreign Trade** civic.

### Circus
Civ V puts Circus at Trapping.

Final:
**Trapping + Games and Recreation civic -> Circus**

### Districts
Removed:
- Holy Site
- Campus
- Encampment

Their useful buildings survive directly in cities:
- Shrine
- Library
- Barracks

### Great Person improvements
No Academy, Manufactory, Customs House, Citadel or Holy Site tile improvement is introduced in this pass.

## Health & Plague integration note

Health & Plague for BNW was checked as an adopted system source.

Its public mechanics make city Health depend on fresh water, local resources/features, population and buildings, while low Health raises plague risk and roads/sea routes accelerate spread.

For Ancient:
- the Health system should already recognize **fresh water and local environmental/resource conditions**;
- **Granary** is flagged for later health-value tuning;
- no unsupported exact Health coefficient is invented in this pass.

The mod's BNW rule that an Academy can cure plagues will **not** preserve the Academy tile improvement, because Great-Person tile improvements are removed in this project. That cure function must later be remapped to a Great Scientist action, medical project, or medical technology during the Health-system audit.

## Deferred rather than forgotten

World Wonders are recorded in the long-form audit but remain deferred:
- Great Bath
- Stonehenge
- Hanging Gardens
- Temple of Artemis
- Great Library
- Pyramids/Mausoleum family
- Statue of Zeus

Heavy Chariot is retained only as a unit-roster candidate because it overlaps the Civ V Chariot Archer role.

Open Borders is deferred to civic-tech reconciliation rather than automatically remaining at Writing.

## Files

- long-form authority: `tech_reference/technology_unlock_audit_v1.csv`
- Ancient summary: `tech_reference/technology_unlock_summary_ancient_v1.csv`
