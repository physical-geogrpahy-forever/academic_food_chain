# Great Person Recruitment System V1

Date: 2026-09-21
Status: **LOCKED DESIGN DIRECTION**

## Core hybrid rule

The project combines:
- Civilization V-style **generation sources**
- Civilization VI-style **worldwide named Great Person recruitment**

The generation source depends on Great Person class, but the recruited person is always a unique historical individual who can be recruited only once worldwide.

## 1. Specialist / building GPP classes

Classes:
- Great Scientist
- Great Engineer
- Great Merchant
- Great Writer
- Great Artist
- Great Musician
- Great Director

Generation:
- city specialists and eligible buildings generate class-specific Great Person Points
- city contributions are summed into a civilization-wide class pool
- city-level contribution is still tracked for birthplace / source-city attribution

Recruitment:
- one named historical candidate is currently available globally for each class
- civilizations compete with their accumulated class GPP
- first civilization to reach the candidate requirement may recruit that person
- the recruited historical individual is removed from the world pool
- the next eligible candidate appears
- unspent / overflow class GPP remains with the civilization for the next candidate unless a later balance pass explicitly changes carryover

This preserves Civ V specialist city management while using Civ VI-style named-person competition.

## 2. Great Prophet

Great Prophet does **not** use Prophet GPP.

Generation currency:
- **Faith**

Recruitment:
- the current named Great Prophet candidate is globally unique
- civilizations do not accumulate Great Prophet Points
- instead, any eligible civilization with enough Faith may purchase/recruit the current candidate
- the first civilization to purchase that candidate receives the named Great Prophet
- all other civilizations keep their Faith
- the recruited individual is removed globally and the next named candidate becomes available

Thus:
`Faith generation -> Faith purchase -> globally unique named Great Prophet`

This preserves the project's Civ V-style Faith purchase for prophets while applying the same named-person competition used for other Great People.

Important:
- do not convert Great Prophet into a specialist-GPP class
- Shrine/Temple Faith remains relevant because it funds prophet recruitment rather than Prophet Points
- no Great Prophet specialist is required

Great Prophet uses remain part of the religion system.
The old Great Prophet Holy Site consumption is already superseded by the worker-built Holy Site improvement and must not be reintroduced automatically.

## 3. Great General

Great General does **not** use city specialist GPP.

Generation source:
- land combat

Land combat experience / military action also contributes to a civilization-wide Great General recruitment pool.

Recruitment:
- current named Great General candidate is globally unique
- civilizations compete with accumulated Great General combat points
- first civilization to reach the current candidate threshold recruits that individual
- overflow is retained for the next candidate unless later balance testing changes this

Thus:
`land combat -> Great General points -> globally unique named Great General`

## 4. Great Admiral

Great Admiral mirrors Great General but uses naval combat.

Thus:
`naval combat -> Great Admiral points -> globally unique named Great Admiral`

No Admiral specialist is required.

## 5. Final class acquisition model

| Great Person class | Generation / purchase source | Recruitment competition |
|---|---|---|
| Great Scientist | Scientist specialist/building GPP | Global named candidate |
| Great Engineer | Engineer specialist/building GPP | Global named candidate |
| Great Merchant | Merchant specialist/building GPP | Global named candidate |
| Great Writer | Writer specialist/building GPP | Global named candidate |
| Great Artist | Artist specialist/building GPP | Global named candidate |
| Great Musician | Musician specialist/building GPP | Global named candidate |
| Great Director | Director specialist/building GPP | Global named candidate |
| Great Prophet | **Faith purchase** | Global named candidate |
| Great General | **Land-combat points** | Global named candidate |
| Great Admiral | **Naval-combat points** | Global named candidate |

## 6. Historical identity rule

A named historical Great Person is globally unique.

Once recruited:
- that individual can never be recruited by another civilization in the same game
- the class advances to the next eligible historical candidate

Great Scientist content now has a separate draft roster:
- `city_system/great_scientists/README.md`
- 279 first-pass candidates across Ancient through Future
- each candidate has an individual ability draft
- candidate count is deliberately not quota-balanced by era or region
- recruitment eligibility is gated by a minimum technology/building/system condition so a Scientist does not depend on an institution that does not yet exist
- `CROSS_CLASS_REVIEW` preserves ambiguous figures until Engineer/Merchant/Writer/Prophet/etc. rosters are available for final de-duplication

The 279-person Scientist roster is **not yet a locked final roster**. Historical-period QA, cross-class de-duplication and numerical balance remain pending.

Other Great Person classes still require their own content passes.

## 7. Pass and patronage

For specialist-GPP classes:
- Civ VI-style Pass may be used
- exact Pass penalty / cooldown remains for numerical balance

For Great Prophet:
- no GPP Pass mechanic is required
- a player simply chooses not to spend Faith on the current candidate
- Faith continues accumulating

For Great General / Great Admiral:
- candidate skipping behavior will follow the same named-person queue principle
- exact pass mechanics remain to be numerically tested

## 8. Gold / Faith patronage

Specialist-GPP classes may later allow Civ VI-style Gold/Faith patronage to cover missing GPP, but the cost formula is not yet locked.

Great Prophet is different:
- Faith is already the primary recruitment currency
- therefore Great Prophet does not use a second Faith-patronage layer

## 9. Design consequence

The project now has three generation models but one recruitment identity model:

1. specialist/building GPP
2. combat GPP
3. direct Faith purchase

All three resolve to:
**globally unique named historical Great People.**
