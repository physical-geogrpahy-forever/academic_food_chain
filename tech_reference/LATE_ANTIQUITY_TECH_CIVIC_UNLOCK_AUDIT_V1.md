# Late Antiquity Technology + Civic Unlock Audit V1

Date: 2026-09-21
Status: **LATE ANTIQUITY COMPLETE — 5 technologies + 4 civics**

## Final technologies

| Technology | Main result |
|---|---|
| Military Tactics | Pikeman |
| Military Engineering | Military Engineer + Military Training; Armory + Military Training; Niter reveal; military roads |
| Stirrups | Knight |
| Horse Collar | Draft Animal Labor; Farm +1 Production; provisional Pasture +1 Food |
| Alchemy | Apothecary; early chemical/medicinal processing |

## Final civics

| Civic | Main result |
|---|---|
| Defensive Tactics | Reconquest/Protectorate War; Bastions/Limes policy candidates |
| Theology | Temple; advanced organized-religion layer |
| Naval Tradition | Great Admiral/naval-infrastructure policy layer |
| Civil Service | Alliances; Defensive Pact; administrative policy layer |

## Major reconciliations

### Pikeman
Civ V places Pikeman at Civil Service, while Civ VI places Pikeman at Military Tactics.

Final:
**Military Tactics -> Pikeman**

This is both the cleaner functional fit and a direct use of the project's dedicated Military Tactics technology.

### Military Engineering
Civ VI Military Engineering provides Military Engineer, Armory, Trebuchet and Niter reveal.

Final:
- **Military Engineering + Military Training -> Armory**
- **Military Engineering + Military Training -> Military Engineer**
- **Military Engineering -> Niter reveal**
- Military Engineer may build/upgrade strategic roads and construct Forts efficiently.

The full Trebuchet is **not** kept here. The project already has a later Physics node and Civ V associates Trebuchet with Physics, so the final trebuchet placement is deferred to that audit.

### Niter
Niter is revealed at Military Engineering, following Civ VI.

Mining remains the extraction method once a Niter tile is visible.

Alchemy does not reveal Niter, avoiding a duplicate resource reveal.

### Stirrups
Civ VI Stirrups unlocks Knight and gives Pastures +1 Food.

Final:
**Stirrups -> Knight**

The Pasture agricultural bonus is moved away from Stirrups because stirrups are a mounted-combat technology, not an agricultural productivity technology.

### Horse Collar
Horse Collar is a project-added historical technology.

Final baseline:
- Draft Animal Labor system
- Farm +1 Production
- provisional Pasture +1 Food

The Production effect represents the much greater usable traction of properly harnessed horses in plowing and hauling. Exact resource requirements and yield numbers can be tuned after simulation.

### Alchemy
Alchemy is a project-added bridge toward Gunpowder, Metallurgy and Chemistry.

Final:
**Alchemy -> Apothecary**

The Apothecary becomes an early medical/material-processing city building. It can later interact with the Health & Plague system, but no arbitrary Health coefficient or plague-cure probability is invented here.

The removed Great Scientist Academy improvement is not restored as a plague-cure mechanism.

### Defensive Tactics
Civ VI gives this civic Bastions, Limes, Reconquest War and Protectorate War.

These remain institutional/policy content.

No Castle is moved here because the project has a separate **Castles** technology in the next era.

### Theology
Civ VI Theology unlocks Temple, and Civ V Theology also carries multiple religion-oriented buildings/wonders.

Final:
**Theology -> Temple**

Grand Temple and major religious wonders are deferred to the National/World Wonder audit.

Civ V's Garden is moved away from Theology.

### Garden
Final candidate:
**Irrigation + Civil Service -> Garden**

Reason:
the building's horticultural/fresh-water basis is technological, while a public/elite urban garden also fits organized civic administration better than religious theology.

Its Great Person/Health effect is tuned later.

### Naval Tradition
Civ VI Naval Tradition unlocks Naval Infrastructure and Navigation policies.

Final:
- keep those as policy candidates;
- retain a Great Admiral generation bonus;
- combine **Celestial Navigation + Naval Tradition** for later port/naval institutional efficiency.

Civ VI Harbor district adjacency effects must be translated into bonuses for the project's Harbor/Lighthouse/port buildings because districts are absent.

### Civil Service
Civ VI Civil Service allows Alliances and unlocks Meritocracy, Retainers and Civil Prestige.

Final:
- **Civil Service -> Alliances**
- **Civil Service -> Defensive Pact**
- retain the three policies as adaptation candidates.

Civ V Civil Service content is split:
- Pikeman -> Military Tactics
- fresh-water Farm +1 Food -> Irrigation
- Open Borders -> Early Empire
- therefore Civil Service remains genuinely institutional rather than a catch-all technology.

## Health-system note

Late Antiquity now has two explicit health-related candidates:
- Apothecary from Alchemy
- Garden from Irrigation + Civil Service

Temple is not treated as a generic Health building.

Exact health values remain deferred to the Health & Plague quantitative pass.

## Authority files

- `tech_reference/late_antiquity_tech_civic_unlock_audit_v1.csv`
- `tech_reference/technology_unlock_summary_late_antiquity_v1.csv`
- `civics_reference/civic_unlock_summary_late_antiquity_v1.csv`
