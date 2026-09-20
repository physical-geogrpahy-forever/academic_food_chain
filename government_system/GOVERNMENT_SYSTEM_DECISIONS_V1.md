# Government System Decisions V1

Date: 2026-09-21

## Baseline decision: no Civilization VI Governor system

The project does **not** import the Civ6 Governor/Title system into the baseline rules.

Reasons:
- the project structurally prioritizes a Civ V-style city system;
- all affected civics already have meaningful non-Governor content;
- importing Governors would create a large parallel character/promotion system not needed to fill a content gap.

Therefore Governor Title rewards at:
State Workforce, Early Empire, Recorded History, Globalization, Social Media, Near Future Governance, Future Civic
are omitted.

Civil Prestige is also omitted because it is Governor-dependent.

## Government building system retained

The Civ6 Government Plaza **district** is removed, but its building-choice structure is retained as one-per-civilization city buildings.

See:
`government_system/GOVERNMENT_BUILDING_CHOICES_V1.md`

## Government tiers

Tier 1:
- Autocracy
- Oligarchy
- Classical Republic

Tier 2:
- Monarchy
- Theocracy
- Merchant Republic

Tier 3:
- Democracy
- Fascism
- Communism

Tier 4:
- Corporate Libertarianism
- Digital Democracy
- Synthetic Technocracy

## Constitutionalism

Constitutionalism does not create duplicate government forms named Constitutional Monarchy / Constitutional Republic.

Instead it unlocks/represents:
- Constitutional Government
- Separation of Powers
- Bill of Rights

and can modify compatible existing governments.

## Tier-4 tradeoffs

Civ6 government identities are retained qualitatively:
- Corporate Libertarianism: **Science penalty**
- Digital Democracy: **military-strength penalty**
- Synthetic Technocracy: **Tourism penalty**

Exact numeric values are not locked here and belong to the government balance pass.
