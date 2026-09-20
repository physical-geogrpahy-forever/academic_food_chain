# Civ V era-mod gap-fill crosswalk V1

Date: 2026-09-20  
Status: review baseline

## Scope

Era-expansion/mod sources checked after the Civ VI and Civ V BNW crosswalk:

1. Pouakai et al. — **Enlightenment Era**
2. zwei833 — **Renaissance Era Revised (RER)**
3. BlouBlou — **Eras: Medieval Age**
4. MoreTech — broad expanded-tech-tree reference

The project precedence rule remains:

**Civ VI Gathering Storm > Civ V BNW > Civ V era-mod content > original new design**

If a mod item is already a Civ VI civic, government, or policy concept, Civ VI wins.

## Enlightenment Era findings

The original Enlightenment Era mod adds a complete new Enlightenment era with 11 new technologies, 11 units, 12 buildings and 9 wonders. Its technology structure includes the new/reworked nodes:

- Exploration
- Sovereignty
- Flintlock
- Humanism
- Imperialism
- Warships
- Fortification
- Manufacturing
- Natural History
- Armor Plating
- Romanticism

The important result is that these do **not** all belong in the civic tree.

### Strong civic candidates

#### 1. Sovereignty

Original mod role:
- requires Banking + Printing Press
- unlocks Manor, Summer Palace, Topkapi Palace and Versailles
- founds the World Congress
- feeds into Humanism, Economics and Flintlock

Civ VI comparison:
- no exact civic named Sovereignty
- Diplomatic Service covers diplomacy but not the full state-sovereignty concept
- Nationalism is later and concerns national political identity rather than the early-modern doctrine of sovereign state authority
- The Enlightenment is broader intellectual change

Project verdict:
**strong new civic candidate**

Best era:
**Exploration, 16–17C**

Possible insertion without breaking the Civ VI skeleton:

```
Guilds -> Diplomatic Service
Humanism ------------------\
                           -> Sovereignty -> The Enlightenment
Diplomatic Service --------/
```

A lighter option is:

```
Diplomatic Service -> Sovereignty -> The Enlightenment
Humanism -------------------------> The Enlightenment
```

The exact prerequisite pattern should be chosen only after graph QA.

Useful imported content:
- Manor
- Summer Palace
- Topkapi Palace
- Versailles
- World-Congress/diplomatic-system unlock concept

These can substantially reduce new content design work even if individual buildings/wonders are later reassigned.

#### 2. Romanticism

Original mod role:
- follows Scientific Theory
- unlocks Surveyor, Menagerie, Gallery and Crystal Palace

Civ VI comparison:
- no exact Romanticism civic
- Humanism is earlier
- Opera and Ballet covers performing arts, not the broader Romantic movement
- Natural History covers museums/science
- Mass Media is much later

Project verdict:
**strong new civic candidate**

Best era:
**Industrial, 19C**  
or a very late Enlightenment transition if the graph needs it.

Possible function:
- bridge cultural development from Opera and Ballet / Natural History toward later cultural heritage and mass society
- unlock cultural buildings and policies rather than duplicate science

### Civ VI exact duplicates: do not add

- Exploration -> Civ VI Exploration
- Humanism -> Civ VI Humanism
- Natural History -> Civ VI Natural History

Their Enlightenment Era buildings/wonders may still be reused as unlock content.

### Keep as science/technology nodes, not civics

- Flintlock
- Warships
- Fortification
- Manufacturing
- Armor Plating

These are technical/military-production concepts.

### Imperialism: hold, not immediate civic

The mod's Imperialism node is primarily an 18C military/trade technology package:
- Cuirassier
- Weigh House
- extra trade route
- plantation gold
- Torre Del Oro

Its function overlaps strongly with Civ VI Mercantilism and Colonialism.

Therefore do not add an 18C Imperialism civic now.

However, a **19C Imperialism civic** may still be historically distinct from Colonialism and Nationalism. That question should be revisited only after the Industrial-era graph is assembled.

## Enlightenment Era content worth reusing

Even where the mod technology is rejected as a civic, its content can be reassigned.

- Humanism -> Academy, Salon, Wat Phra Kaew
- Sovereignty -> Manor, Summer Palace, Topkapi Palace, Versailles
- Natural History -> Museum, Smithsonian Institution
- Romanticism -> Menagerie, Gallery, Crystal Palace
- Imperialism/Mercantilism/Colonialism area -> Weigh House, Torre Del Oro
- Fortification -> Bastion, Fasil Ghebbi
- Manufacturing -> Cloth Mill
- Warships/Armor Plating -> Kronborg, Drydock
- Flintlock -> Gunsmith

This is exactly the kind of content reuse that reduces work without inflating the civic count.

## Renaissance Era Revised findings

RER mainly improves the Renaissance military technology/unit line.

Relevant additions:
- Large Cold Arms
- Pike and Shot
- Reiter
- Two-handed Swordsman
- Tercio
- Free Company

Verdict:
- Large Cold Arms -> science/technology candidate
- Pike and Shot -> science/technology candidate
- Free Company -> attach to existing Civ VI **Mercenaries** civic/unit content
- no strong new civic candidate

RER is therefore useful mainly for the **technology and unit tree**, not for adding social civics.

## BlouBlou Eras: Medieval Age findings

This mod does not meaningfully expand the historical medieval civic/tech vocabulary. It mainly:
- caps the game at the Medieval Era
- moves later functionality earlier so a full game can end there
- introduces a repeatable end-cap technology called Mentoring

Verdict:
- useful as a pacing/end-era design reference
- **not** a source of new medieval civic nodes

Therefore it does not solve the project's Early Medieval gap.

## MoreTech findings

MoreTech expands Civ V to 166 technologies and 16 eras. It independently includes several names also present in Enlightenment Era, including:
- Sovereignty
- Exploration
- Humanism
- Flintlock
- Scientific Theory
- Manufacturing
- Warships
- Fortification
- Romanticism

It also contains later concepts such as Corporations, Cinematography, Environmentalism, Globalization, Mass Media and Digital Society.

Under the Civ VI-priority rule:
- Environmentalism -> Civ VI Environmentalism
- Globalization -> Civ VI Globalization
- Mass Media -> Civ VI Mass Media
- Digital Society -> largely contained by Social Media / Near Future Governance
- Corporations -> mostly contained by Capitalism unless a separate corporate mechanic later requires it
- Cinematography -> better as a Mass Media unlock/technology
- Sovereignty and Romanticism remain the strongest genuinely non-overlapping civic candidates

## Combined candidate status after all sources so far

### Strong candidates

| Candidate | Source | Project era | Why it survives Civ VI priority |
|---|---|---|---|
| Scholasticism | Civ V BNW Patronage | High Medieval | no direct Civ VI civic for medieval scholastic intellectual institutions |
| Scientific Revolution | Civ V BNW Rationalism | Exploration | distinct 16–17C transformation between Humanism and 18C Enlightenment |
| Sovereignty | Enlightenment Era / MoreTech | Exploration | early-modern sovereign-state concept not equivalent to Diplomatic Service or Nationalism |
| Romanticism | Enlightenment Era / MoreTech | Industrial | distinct cultural movement absent from Civ VI civic tree |

### Hold for later review

- 19C Imperialism
- Corporations

### Rejected as duplicate civic

- Humanism
- Exploration
- Natural History
- Environmentalism
- Globalization
- Mass Media
- Monarchy
- Oligarchy
- Theocracy
- Mercantilism
- Nationalism
- Urbanization
- Mobilization
- and the other duplicates already listed in the BNW crosswalk

## Gap status now

Using the 61 imported Civ VI civics plus only strong candidates:

- Early Medieval: Civ VI 2 + **0** strong candidate
- High Medieval: Civ VI 3 + **Scholasticism**
- Renaissance: Civ VI 2 + **0** strong candidate
- Exploration: Civ VI 4 + **Scientific Revolution + Sovereignty**
- Enlightenment: Civ VI 3 + **0 necessary**
- Industrial: Civ VI 7 + **Romanticism** if desired

The unresolved gaps therefore remain mainly:
- **Early Medieval**
- **Renaissance**

These should not be filled by forcing Enlightenment-mod technology names into the civic tree.

## Source references

Enlightenment Era Steam Workshop:
https://steamcommunity.com/workshop/filedetails/?id=544452801

Enlightenment Era CivFanatics thread:
https://forums.civfanatics.com/threads/the-enlightenment-era.551446/

Enlightenment Era content table:
https://civ5customization-archive.fandom.com/wiki/Pouakai%27s_Enlightenment_Era

Renaissance Era Revised:
https://forums.civfanatics.com/resources/v-4-renaissance-era-revised.24663/

BlouBlou Medieval Age:
https://steamcommunity.com/sharedfiles/filedetails/?id=85949525

MoreTech:
https://forums.civfanatics.com/threads/moretech.656168/
