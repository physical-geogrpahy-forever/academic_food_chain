# Corporation Sector and Output Catalogue V2

Date: 2026-09-20  
Status: **CANONICAL SECTOR CATALOGUE — founder-linked design baseline**

## 1. Purpose

This catalogue normalizes the free-form industries in the 99-founder V2 pool into reusable game sectors.

- canonical sectors defined: **32**
- sectors currently represented by at least one audited founder: **30**
- deliberately retained future sectors without a locked founder: **MEDIA_FILM_ENTERTAINMENT, AIRLINES_TRAVEL**

Machine-readable file:
`corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.csv`

The founder matrix now contains a `CANONICAL_SECTOR_ID` column linking every founder to this catalogue.

## 2. Core rule

Corporation founding remains:

**Capitalism + sector technology**

However, a sector can have:
- a base technology for the earliest historically plausible form;
- a later upgrade technology for mature network/production mechanics;
- founder-specific later gates when the historical company belongs to a mature form of the sector.

Example:
- Telecommunications base sector can exist at **Telegraph**;
- modern telecom founders can still require **Telecommunications**;
- this lets Ericsson and late-20C mobile-network founders coexist without inventing separate duplicate sectors.

## 3. Supply models

### Physical product supply
Used for Manufactured Luxury and Functional Corporate Goods.

A corporation produces quantities. Cities only receive the effect when supplied.

### Branch/network coverage
Used for Services.

A local branch, route, or network provides service access. There is no artificial stockpile token for banking, hotels, software, telecom service, etc.

### Hybrid
Some sectors intentionally combine both:
- Automotive
- Consumer Electronics
- Computing Hardware
- Telecommunications

This follows the previously locked rule that cars/electronics can have both consumer-brand value and functional economic effects.

## 4. Canonical sector list

| Sector | Base gate | Upgrade | Output | Founders |
|---|---|---|---|---:|
| Textiles, Apparel & Sporting Goods | Mass Production | - | Manufactured Luxury | 6 |
| Cosmetics & Personal Care | Chemistry | - | Manufactured Luxury | 5 |
| Processed Food & Confectionery | Refrigeration | - | Hybrid: Functional Corporate Good + Manufactured Luxury | 7 |
| Food Service | Refrigeration | - | Service | 1 |
| Furniture & Household Goods | Mass Production | - | Manufactured Luxury | 1 |
| Retail & Distribution | Mass Production | - | Service | 1 |
| Hospitality & Hotels | Railroad | Advanced Flight | Service | 2 |
| Finance & Banking | Banking | Computers | Service | 4 |
| Insurance | Banking | Computers | Service | 1 |
| Trading Houses & Industrial Investment | Industrialization | Telegraph | Service | 2 |
| Petroleum Refining | Refining | - | Functional Corporate Good | 1 |
| Chemicals & Industrial Materials | Chemistry | Fertilizer | Functional Corporate Good | 5 |
| Pharmaceuticals | Biology | Penicillin | Functional Corporate Good | 2 |
| Steel & Heavy Materials | Steel | - | Functional Corporate Good | 1 |
| Construction Materials | Industrialization | Steel | Functional Corporate Good | 1 |
| Mining & Extractive Materials | Dynamite | Railroad | Functional Corporate Good | 1 |
| Machinery & Precision Components | Replaceable Parts | Electronics | Functional Corporate Good | 3 |
| Automotive Manufacturing | Combustion | Mass Production | Hybrid: Manufactured Luxury + Functional Corporate Good | 7 |
| Batteries & Electrified Mobility | Electronics | Advanced Power Cells | Functional Corporate Good | 1 |
| Electrical Equipment & Power Systems | Electricity | - | Functional Corporate Good | 5 |
| Electronics Manufacturing | Electronics | Robotics | Functional Corporate Good | 1 |
| Consumer Electronics | Electronics | Computers | Hybrid: Manufactured Luxury + Functional Corporate Good | 6 |
| Computing Hardware | Computers | Robotics | Hybrid: Manufactured Luxury + Functional Corporate Good | 2 |
| Semiconductors | Electronics | Computers | Functional Corporate Good | 4 |
| Telecommunications | Telegraph | Telecommunications | Hybrid: Functional Corporate Good + Service | 4 |
| Software & IT Services | Computers | - | Service | 5 |
| Digital Platforms & E-commerce | Telecommunications | Computers | Service | 12 |
| Shipping & Logistics | Steam Power | Advanced Flight | Service | 5 |
| Aerospace Manufacturing | Flight | Advanced Flight | Functional Corporate Good | 2 |
| Cultural Manufactured Goods | Acoustics | - | Manufactured Luxury | 1 |
| Film, Media & Entertainment | PENDING_FILM_TECH_DECISION | Radio | Service | 0 |
| Airlines & Travel | Advanced Flight | - | Service | 0 |

## 5. Film/media exception

`MEDIA_FILM_ENTERTAINMENT` is deliberately **not** given a fake current gate.

The project still has the unresolved 109-tech vs 111-tech decision:
- keep 109 technologies and map Film/Great Director to an existing technology; or
- add Photography and Cinematography.

Therefore its base technology is recorded as:
`PENDING_FILM_TECH_DECISION`

Do not silently convert this to Radio or another technology until that earlier project decision is made.

## 6. Conglomerate handling

A conglomerate is not itself a gameplay sector.

Examples:
- Samsung founder Lee Byung-chul is mapped to **TRADING_HOUSES** for the founder-era corporate form instead of falsely claiming he founded Samsung Electronics.
- Tata founder Jamsetji Tata is also mapped to **TRADING_HOUSES / industrial investment** rather than retroactively assigning later group companies to him.
- Reliance founder Dhirubhai Ambani is mapped to **TEXTILES_APPAREL_SPORTING** at founding stage, with later petrochemical diversification available through company development.
- Hyundai founder Chung Ju-yung is mapped to **AUTOMOTIVE** for the signature industrial line while retaining qualified lineage wording.

Named firms may later diversify into additional sectors through gameplay. Diversification does not rewrite the historical founder attribution.

## 7. Next implementation step

Before the 109-tech unit/building table:
1. reconcile founder-specific gate exceptions against this catalogue;
2. assign quantitative production/branch effects by sector;
3. define corporate diversification rules;
4. resolve the Film/Cinematography technology decision;
5. freeze the signature-founder subset.


## 8. Historical gate reconciliation note

- **Carl Benz** uses `Mass Production` as the earliest Industrial-era automotive-sector gate because the locked `Combustion` technology sits in the project Modern Era. Later automotive founders use `Combustion`.
- **J. C. Mahindra** and **K. C. Mahindra** are mapped to `STEEL_HEAVY_MATERIALS` at founding because Mahindra began as a steel-trading company before later automotive diversification.
- `SHIPPING_LOGISTICS` uses a progression of `Steam Power -> Railroad -> Advanced Flight`, allowing shipping, parcel delivery and express-air logistics founders to enter at historically appropriate stages.
