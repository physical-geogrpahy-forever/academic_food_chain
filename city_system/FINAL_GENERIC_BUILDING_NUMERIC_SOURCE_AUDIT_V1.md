# Final Generic Building Numeric Source Audit V1

Date: 2026-09-21

This file distinguishes source-game values from project adaptations.

## Primary Civ V data authority

Civilization V BNW building data:
https://civilization.fandom.com/wiki/Module:Data/Civ5/BNW/Buildings

Direct anchor examples used in V1:
- Palace
- Walls
- Monument
- Granary
- Water Mill
- Stone Works
- Barracks
- Shrine
- Library
- Caravansary
- Market
- Mint
- Amphitheater
- Writers' Guild
- Circus
- Aqueduct
- Lighthouse
- Stable
- Armory
- Garden
- Temple
- Castle
- Artists' Guild
- Windmill
- Workshop
- University
- Bank
- Constabulary
- Arsenal
- Musicians' Guild
- Opera House
- Seaport
- Observatory
- Stock Exchange
- Zoo
- Military Academy
- Public School
- Military Base
- Factory
- Hospital
- Airport
- Stadium
- Medical Lab
- Research Lab
- Solar Plant

These rows are labeled `A_CIV5_BNW_EXACT`.

## Civ VI adaptation references

Government Plaza:
https://civilization.fandom.com/wiki/Government_Plaza_(Civ6)

Ancestral Hall:
https://civilization.fandom.com/wiki/Ancestral_Hall_(Civ6)

Audience Chamber:
https://civilization.fandom.com/wiki/Audience_Chamber_(Civ6)

Warlord's Throne:
https://civilization.fandom.com/wiki/Warlord%27s_Throne_(Civ6)

Foreign Ministry:
https://civilization.fandom.com/wiki/Foreign_Ministry_(Civ6)

Grand Master's Chapel:
https://civilization.fandom.com/wiki/Grand_Master%27s_Chapel_(Civ6)

Intelligence Agency:
https://civilization.fandom.com/wiki/Intelligence_Agency_(Civ6)

National History Museum / Royal Society / War Department source data:
https://civilization.fandom.com/wiki/Module:Data/Civ6/GS/Buildings

Consulate / Chancery source data:
https://civilization.fandom.com/wiki/Module:Data/Civ6/RF/Buildings

Food Market / Shopping Mall:
https://civilization.fandom.com/wiki/Food_Market_(Civ6)
https://civilization.fandom.com/wiki/Shopping_Mall_(Civ6)

Ferris Wheel / Aquarium / Aquatics Center:
https://civilization.fandom.com/wiki/Ferris_Wheel_(Civ6)
https://civilization.fandom.com/wiki/Aquarium_(Civ6)
https://civilization.fandom.com/wiki/Aquatics_Center_(Civ6)

## Important source-to-project translations

- no districts
- no Governors
- no Builder charges
- no free Worker from Ancestral Hall
- Civ VI regional entertainment auras are converted to local city-building values unless explicitly represented as a special effect
- project uses Civ V-style direct buildings and maintenance scale
- Food Market / Shopping Mall are not mutually exclusive in V1 because the project already placed both in the generic direct-building roster
- Royal Society cannot consume Workers, so it becomes a city-project Production modifier
- Recycling Center does not generate Aluminum
- district-specific adjacency is translated or omitted rather than recreated invisibly

## Pouakai / project rows

Pouakai-based rows are labeled `B_EE_ADAPTED`:
- Star Fort
- Gunsmith
- Cloth Mill
- Drydock

Historical/project rows are labeled `B_PROJECT_INTERPOLATED`.

Their numeric values are project balance decisions and must not be cited as original Civ V/Civ VI values.
