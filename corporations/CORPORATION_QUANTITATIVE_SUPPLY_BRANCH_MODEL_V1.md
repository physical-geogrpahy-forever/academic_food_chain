# Corporation Quantitative Supply & Branch Model V1

Date: 2026-09-20  
Status: **IMPLEMENTATION BASELINE / balance values tunable after simulation**

This file converts the corporation concept into a compact model that can actually be coded and simulated.

Machine-readable sector effects:
`corporations/corporation_sector_effects_v1.csv`

## 1. One normalized unit: Supply Unit (SU)

A Supply Unit is a game abstraction, not one tonne/barrel/item.

Physical corporate goods use SU per turn.

Default city demand:

```
Functional Good demand = ceil(city_population / 5) SU/turn
Manufactured Luxury demand = ceil(city_population / 8) SU/turn
Hybrid physical-product demand = ceil(city_population / 6) SU/turn
```

This prevents one headquarters from granting an empire-wide permanent bonus.

A normal corporate plant produces about 4 SU/turn, with sector values between 3 and 5.

Therefore one ordinary plant can fully supply roughly:
- 20 population of Functional Goods;
- 32 population of Manufactured Luxury;
- 24 population of Hybrid physical goods.

Large empires need multiple plants or imports.

## 2. Physical-good coverage

For a city and product:

```
coverage = min(1.0, allocated_SU / demand_SU)
```

Percentage effects scale linearly:

```
effective_bonus = full_bonus × coverage
```

Example:

A city needs 4 SU of Refined Petroleum Products but receives 2.

```
coverage = 2 / 4 = 0.5
Production bonus = 10% × 0.5 = 5%
```

Discrete Amenities do not scale linearly.

Default Manufactured Luxury threshold:
- coverage < 0.75 -> no Amenity from the category
- coverage >= 0.75 -> +1 Amenity from the category

## 3. Brand anti-stacking

A city can receive Ford, Toyota, Honda and Hyundai, but all belong to the **Automobiles** category.

The city receives the main Automobile Amenity only once.

Additional brands can contribute:
- corporate revenue;
- market share;
- export demand;
- Gold;
- brand Tourism where appropriate.

Default repeated-brand rule:

```
+2% city Gold per additional supplied brand in same category
cap = +6%
extra Amenity = 0
```

This rule applies only where the sector file says a branded category exists.

## 4. Plant capacity and inputs

Default corporate plant:
- 4 SU/turn

Sector exceptions:
- high-volume consumer/food goods: 5 SU/turn
- heavy/bulk or aircraft/petroleum: 3 SU/turn

If a sector requires a map-resource input, one active plant normally consumes one normalized input unit per turn at full capacity.

The existing strategic/luxury/bonus resource accounting remains authoritative. SU does **not** replace Oil, Iron, Wheat, Cocoa, etc.

Instead:

```
map/raw resource -> corporate plant -> corporate SU
```

No plant can produce full output without its required input.

## 5. Domestic allocation

Physical corporate output enters that firm's national product pool for the turn.

A city may draw from the pool if:
- it belongs to the firm's home civilization and is connected to the economic network; or
- it has an eligible foreign trade/branch connection.

This deliberately avoids expensive tile-by-tile freight simulation.

The game still cares about logistics because disconnected cities cannot draw product and foreign allocation requires an economic connection.

## 6. Foreign physical-goods trade

Default maximum foreign allocation per active trade connection:

**4 SU/turn**

With full Shipping/Logistics corporate service:

**5 SU/turn**

This is a throughput bonus, not resource creation.

## 7. Services use coverage, not stock

Services such as finance, hotels, insurance, software and digital platforms do not create SU.

Default service coverage:

| State | Coverage |
|---|---:|
| no access | 0.0 |
| connected national network, no local branch | 0.5 |
| local branch/network node | 1.0 |
| foreign city with explicit branch/network access | 1.0 |

Percentage effects are multiplied by this coverage.

Sector exceptions are allowed.

Example:
Hospitality Tourism requires an actual local hotel branch; remote network presence alone does not generate Tourism.

## 8. Hybrid sectors

Hybrid sectors use both physical and network logic when appropriate.

### Automotive
Physical Automobiles generate:
- category Amenity;
- land-logistics benefit.

Dealer/branch network mainly determines market reach and Gold.

### Telecommunications
Equipment can be physically produced, but the main economic effect comes from network coverage.

### Consumer electronics / computing
Physical products must be supplied.
Their Science/consumer effects scale with physical coverage.

## 9. Corporate diversification

The historical founder's primary sector never changes.

A named corporation may enter another sector only through a **Diversification Project**.

Requirements:
1. target sector technology is researched;
2. corporation has at least 3 operating branches/plants outside its HQ;
3. target sector has its required input/network access;
4. a headquarters Diversification Project is completed.

Default limits:
- maximum **2 secondary sectors** per corporation;
- secondary sectors never change the founder attribution;
- a secondary sector does not block other corporations from that sector.

This handles historical conglomerates cleanly.

Examples:
- Samsung can begin as a trading house and later diversify into electronics.
- Tata can begin as a trading/industrial-investment firm and later enter heavy industry.
- Reliance can begin with textiles and later enter petrochemicals/refining.

## 10. Named firm uniqueness vs sector competition

- named historical firm: unique globally
- canonical sector: never unique
- generic corporation: always available if normal founding rules are met

If a signature founder is not used to create the named firm, another Great Merchant/Engineer can still create a generic corporation in that sector.

## 11. Sector quantitative baseline

| Sector | Channel | Plant SU | Pop/SU | Full supplied effect |
|---|---|---:|---:|---|
| TEXTILES_APPAREL_SPORTING | PHYSICAL_LUXURY | 5 | 8 | +1 Amenity for category at >=75% coverage; +5% Gold |
| COSMETICS_PERSONAL_CARE | PHYSICAL_LUXURY | 5 | 8 | +1 Amenity at >=75% coverage; +5% Gold; +5% Tourism for iconic brand |
| FOOD_PROCESSING | PHYSICAL_HYBRID | 5 | 5 | Functional line: up to +10% Food and +5% Growth; luxury subline: +1 Amenity by category |
| FOOD_SERVICE | SERVICE | 0 | - | Local branch: +5% Gold, +5% Growth; +5% Tourism in cities with foreign visitors |
| FURNITURE_HOUSEHOLD | PHYSICAL_LUXURY | 5 | 8 | +1 Amenity at >=75% coverage; +5% Growth/housing efficiency |
| RETAIL_DISTRIBUTION | SERVICE | 0 | - | Local branch: +10% Gold and +25% received Manufactured Luxury distribution capacity |
| HOSPITALITY_TRAVEL | SERVICE | 0 | - | Local branch: +15% Tourism, +5% Culture, +5% Gold |
| FINANCE_BANKING | SERVICE | 0 | - | Local branch: +10% Gold; -15% corporate branch/plant investment cost in city |
| INSURANCE | SERVICE | 0 | - | Local branch: +5% Gold; -25% disaster/business-loss magnitude |
| TRADING_HOUSES | SERVICE | 0 | - | Local branch/HQ: +10% international trade Gold; +15% corporate import/export allocation capacity |
| PETROLEUM_REFINING | PHYSICAL_FUNCTIONAL | 3 | 5 | At full coverage: +10% Production; +20% corporate/logistics throughput for oil-dependent modern systems |
| CHEMICALS_MATERIALS | PHYSICAL_FUNCTIONAL | 4 | 5 | Industrial Chemicals: +8% Production; Fertilizer subline: +10% Food from worked farms |
| PHARMACEUTICALS | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +10% Growth/Health; +5 HP unit healing per turn in city territory |
| STEEL_HEAVY_MATERIALS | PHYSICAL_FUNCTIONAL | 3 | 5 | At full coverage: +10% Production toward buildings and industrial/military units |
| CONSTRUCTION_MATERIALS | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +15% Production toward buildings and infrastructure only |
| MINING_EXTRACTIVES | PHYSICAL_FUNCTIONAL | 4 | 5 | Supplied mining city: +15% improved mineral extraction and +5% Production |
| MACHINERY_COMPONENTS | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +10% Production; +10% factory/workshop efficiency or vehicle/component efficiency |
| AUTOMOTIVE | PHYSICAL_HYBRID | 4 | 6 | At >=75% coverage: +1 Automobile-category Amenity; at full coverage: +10% land trade/logistics efficiency |
| BATTERIES_ELECTRIFIED_MOBILITY | PHYSICAL_HYBRID | 4 | 6 | At full coverage: +5% Science, +5% Production; mature electric-vehicle line may grant Automobile-category Amenity |
| ELECTRICAL_EQUIPMENT | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +10% Production and +5% Science |
| ELECTRONICS_MANUFACTURING | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +10% Production toward electronics/advanced buildings and +5% Science |
| CONSUMER_ELECTRONICS | PHYSICAL_HYBRID | 5 | 6 | At >=75% coverage: +1 Consumer-Electronics-category Amenity; at full coverage: +5% Science and +5% Gold |
| COMPUTING_HARDWARE | PHYSICAL_HYBRID | 4 | 6 | At full coverage: +10% Science and +5% Production; consumer line may grant +1 category Amenity at >=75% |
| SEMICONDUCTORS | PHYSICAL_FUNCTIONAL | 4 | 5 | At full coverage: +10% Science and +10% Production toward advanced units/buildings |
| TELECOMMUNICATIONS | HYBRID_NETWORK | 3 | - | Local full network: +10% Science, +5% Gold, +10% trade/network efficiency |
| SOFTWARE_IT | SERVICE | 0 | - | Local/full network: +10% Science, +5% Production, +5% Gold |
| DIGITAL_PLATFORMS | SERVICE | 0 | - | Local/full network: +10% Gold, +5% Science, +10% internal trade/service efficiency |
| SHIPPING_LOGISTICS | SERVICE | 0 | - | Local/full network: +10% trade-route Gold and +25% physical-goods distribution/export capacity |
| AEROSPACE | PHYSICAL_FUNCTIONAL | 3 | 5 | At full coverage: +15% Production toward air units/aviation infrastructure; +10% long-distance logistics capacity |
| CULTURAL_GOODS | PHYSICAL_LUXURY | 5 | 8 | At >=75% coverage: +1 Amenity; at full coverage: +5% Culture |
| MEDIA_FILM_ENTERTAINMENT | SERVICE | 0 | - | PROVISIONAL EFFECT ONLY: local branch +10% Culture, +15% Tourism; HQ +1 Great Director point/turn |
| AIRLINES_TRAVEL | SERVICE | 0 | - | Local route/branch: +15% Tourism, +10% international trade Gold, +25% intercontinental service connectivity |

## 12. Film exception remains unresolved

`MEDIA_FILM_ENTERTAINMENT` has only a provisional effect envelope.

Its technology gate remains unresolved because Photography/Cinematography is still an explicit project decision.

Do not treat the provisional sector row as permission to silently add or remap the technology.

## 13. What is now fixed vs tunable

### Fixed system behavior
- Functional/Manufactured physical goods use supply quantities.
- Services use branch/network coverage.
- same product category does not stack Amenities infinitely.
- foreign physical-goods allocation needs economic connection.
- sectors are non-exclusive.
- named firms are unique.
- diversification does not rewrite founder history.

### Initial balance values, tunable after simulation
- 3-5 SU plant capacities;
- population-per-SU demand;
- +5/+10/+15% yield magnitudes;
- 4 SU foreign connection throughput;
- 0.5 remote service coverage.

These should be stress-tested once city population, trade-route and yield scales are implemented.
