# Health and Plague Qualitative Integration V1

Date: 2026-09-21

## Adopted source structure
Based on Health & Plague for BNW:
- City Health depends on fresh water, local resources/features, population and buildings.
- Empire-level Health can be influenced by technologies/policies.
- negative Health increases plague risk.
- plagues spread more readily through roads, sea routes and international trade.
- plagued cities can lose population and nearby units can be affected.

## Project adaptation

### Early water and settlement health
- Fresh-water access: positive baseline Health factor.
- Aqueduct: improves water-supply Health.
- Granary remains primarily food/storage; any Health value is minor and numerical.
- Garden is not a primary plague-control building.

### Alchemy / Apothecary
**Alchemy -> Apothecary**

Role:
- early medical preparation and pharmaceutical processing;
- modest city Health support;
- reduces plague severity and/or recovery penalty;
- does **not** instantly cure all cities;
- no Great Scientist Academy tile is restored.

### Industrial sanitation
**Sanitation + Civil Engineering -> Sewer**
- major reduction in sanitation-related disease risk;
- lowers plague emergence pressure in dense cities.

**Sanitation + Urbanization -> Modern Public Health**
- citywide sanitary administration and prevention;
- counters the crowding/connectivity penalty of industrial urbanization.

### Biology / Hospital
**Biology + Urbanization -> Hospital**
- substantial Health and mortality/recovery support;
- broad medical institution rather than disease-specific cure.

### Penicillin / Medical Lab
**Penicillin + Urbanization -> Medical Lab**
- strong bacterial-disease treatment;
- improves recovery and lowers bacterial mortality;
- does not make viral/non-bacterial epidemics impossible.

### Cybernetics
**Cybernetics + Near Future Governance -> Advanced Assistive Medicine**
- medical-device, prosthetic, rehabilitation and monitoring support;
- improves Hospital/Medical Lab effectiveness and population productivity/recovery;
- not a direct plague-transmission blocker.

## Great Scientist plague cure
The source mod's Academy-built Great Scientist cure is **not** used because Great Person tile improvements are removed.

If a Great Scientist plague intervention is later retained, it must be an **active Great Scientist action or emergency medical research project**, never an Academy tile improvement.

## Numerical pass
No Health points, plague probabilities, transmission multipliers or immunity durations are locked here.
Those belong to the later quantitative Health balance pass.
