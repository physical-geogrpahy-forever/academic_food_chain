# Long-form Unlock Audit Structural QA V1

Date: 2026-09-21

- Audit files checked: 16
- Total audit rows: 948
- Malformed era/type rows: 3
- Duplicate record IDs within a source file: 0
- Generic DEFER/DEFER_SYSTEM rows: 83

## Malformed rows
- tech_reference/industrial_tech_civic_unlock_audit_v1_part_b.csv :: ICB013 :: era=POLICY :: type=Industrial :: Laissez-Faire
- tech_reference/industrial_tech_civic_unlock_audit_v1_part_b.csv :: ICB014 :: era=POLICY :: type=Industrial :: Market Economy
- tech_reference/atomic_tech_civic_unlock_audit_v1_part_b.csv :: AB013 :: era=SYSTEM :: type=Atomic :: Industrial Robotics

## Duplicate IDs
- none

## Deferred generic content
DEFER/DEFER_SYSTEM is not automatically an error. These rows are candidates for later unit, system, numerical, or government balancing.

- A043 [UNIT] Heavy Chariot (DEFER_SYSTEM)
- C003 [POLICY] Discipline; God King; Survey; Urban Planning (DEFER_SYSTEM)
- C005 [POLICY] Ilkum; Agoge (DEFER_SYSTEM)
- C009 [POLICY] Caravansaries; Maritime Industries (DEFER_SYSTEM)
- C010 [DIPLOMACY] Joint War / Join Ongoing War (DEFER_SYSTEM)
- C014 [POLICY] Maneuver; Strategos (DEFER_SYSTEM)
- C016 [POLICY] Corvée; Conscription (DEFER_SYSTEM)
- C017 [SYSTEM] Governor Title (DEFER_SYSTEM)
- C020 [POLICY] Colonization; Land Surveyors; Limitanei (DEFER_SYSTEM)
- C021 [SYSTEM] Governor Title (DEFER_SYSTEM)
- C025 [POLICY] Inspiration; Revelation (DEFER_SYSTEM)
- C026 [SYSTEM] Envoy +1 (DEFER_SYSTEM)
- C028 [CITY_BUILDING] Grove (DEFER_SYSTEM)
- CC003 [POLICY] Insulae (DEFER_SYSTEM)
- CC010 [POLICY] Charismatic Leader; Diplomatic League (DEFER_SYSTEM)
- CC019 [POLICY] Literary Tradition (DEFER_SYSTEM)
- CC023 [POLICY] Raid; Veterancy; Equestrian Orders (DEFER_SYSTEM)
- CC024 [SYSTEM] Envoy +1 (DEFER_SYSTEM)
- CC027 [POLICY] Natural Philosophy; Praetorium (DEFER_SYSTEM)
- CC028 [SYSTEM] Governor Title (DEFER_SYSTEM)
- CC030 [SYSTEM] Paper-record synergy (DEFER_SYSTEM)
- LA020 [SYSTEM] Plague treatment support (DEFER_SYSTEM)
- LC001 [POLICY] Bastions (DEFER_SYSTEM)
- LC002 [POLICY] Limes (DEFER_SYSTEM)
- LC009 [POLICY] Scripture (DEFER_SYSTEM)
- LC012 [POLICY] Naval Infrastructure (DEFER_SYSTEM)
- LC013 [POLICY] Navigation (DEFER_SYSTEM)
- LC019 [POLICY] Meritocracy (DEFER_SYSTEM)
- LC020 [POLICY] Retainers (DEFER_SYSTEM)
- LC021 [POLICY] Civil Prestige (DEFER_SYSTEM)
- EM012 [SYSTEM] Great Work of Writing copying/distribution bonus (DEFER_SYSTEM)
- EM015 [YIELD_UPGRADE] Library / Scriptorium / Paper Workshop science upgrade (DEFER_SYSTEM)
- EM016 [SYSTEM] Administrative and commercial calculation (DEFER_SYSTEM)
- EM019 [CITY_BUILDING] Harbor/Lighthouse navigation upgrade (DEFER_SYSTEM)
- EC002 [POLICY] Feudal Contract (DEFER_SYSTEM)
- EC004 [CITY_BUILDING] Estate / Manor (DEFER_SYSTEM)
- EC010 [SYSTEM] Mercenary Recruitment (DEFER_SYSTEM)
- EC016 [POLICY] Manuscript Patronage (DEFER_SYSTEM)
- EC019 [GREAT_PERSON_SYSTEM] Court Great Writer/Artist support (DEFER_SYSTEM)
- EC020 [SYSTEM] Palace Great Work slot upgrade (DEFER_SYSTEM)
- EC021 [POLICY] Court Patronage policy (DEFER_SYSTEM)
- HM014 [CITY_BUILDING] Major Religious Complex (DEFER_SYSTEM)
- HC019 [CITY_BUILDING] Tier-2 Government Building choice (DEFER_SYSTEM)
- HC024 [YIELD_UPGRADE] University Scholasticism Bonus (DEFER_SYSTEM)
- RC020 [SYSTEM] City-State Great Person gifts (DEFER_SYSTEM)
- RC023 [POLICY] Vernacular Print (DEFER_SYSTEM)
- RC024 [POLICY] Pamphleteering (DEFER_SYSTEM)
- XC007 [POLICY] Native Conquest (DEFER_SYSTEM)
- XC031 [YIELD_UPGRADE] University scientific-method bonus (DEFER_SYSTEM)
- EC019 [POLICY] Separation of Powers (DEFER_SYSTEM)
- EC020 [POLICY] Bill of Rights (DEFER_SYSTEM)
- EC021 [GOVERNMENT] Constitutional Monarchy / Constitutional Republic variants (DEFER_SYSTEM)
- EC025 [POLICY] Coffeehouse Debate (DEFER_SYSTEM)
- EC026 [DIPLOMACY] Public diplomatic opinion effects (DEFER_SYSTEM)
- IA005 [CITY_BUILDING] Coal Power Plant (DEFER_SYSTEM)
- IA020 [UNIT] Ranger (DEFER_SYSTEM)
- IA043 [UNIT] Submarine (DEFER_SYSTEM)
- IC013 [POLICY] Expropriation (DEFER_SYSTEM)
- IB010 [YIELD_UPGRADE] Pasture +1 Food (DEFER_SYSTEM)
- ICB022 [CITY_BUILDING] Labor Union Hall (DEFER_SYSTEM)
- ICB025 [SYSTEM] Strike / Labor Dispute pressure (DEFER_SYSTEM)
- MC013 [CITY_BUILDING] Tier-3 Government Building choice (DEFER_SYSTEM)
- MB036 [UNIT] Spec Ops (DEFER_SYSTEM)
- MCB011 [POLICY] Patriotic War (DEFER_SYSTEM)
- AA020 [SYSTEM] Long-distance digital communications capacity (DEFER_SYSTEM)
- AA034 [UNIT] Nuclear Missile (DEFER_SYSTEM)
- AB015 [UNIT] Giant Death Robot (DEFER_SYSTEM)
- AB017 [YIELD_UPGRADE] Pasture automation bonus (DEFER_SYSTEM)
- AB033 [CITY_BUILDING] Particle Accelerator (DEFER_SYSTEM)
- IN007 [UNIT] Giant Death Robot Drone Air Defense upgrade (DEFER_SYSTEM)
- IN008 [SYSTEM] AI-assisted intelligence analysis (DEFER_SYSTEM)
- IN011 [UNIT] Giant Death Robot Particle Beam Siege Cannon upgrade (DEFER_SYSTEM)
- IN016 [UNIT] Giant Death Robot Enhanced Mobility upgrade (DEFER_SYSTEM)
- IN017 [SYSTEM] Cybernetic medical/assistive systems (DEFER_SYSTEM)
- IN020 [UNIT] Giant Death Robot Reinforced Armor upgrade (DEFER_SYSTEM)
- IN025 [SYSTEM] City-project forecasting bonus (DEFER_SYSTEM)
- ICA006 [SYSTEM] Governor Title (DEFER_SYSTEM)
- ICA011 [SYSTEM] Governor Title (DEFER_SYSTEM)
- ICA014 [SYSTEM] Governor Title (DEFER_SYSTEM)
- ICA018 [SYSTEM] Science penalty (DEFER_SYSTEM)
- ICA021 [SYSTEM] Military-strength tradeoff (DEFER_SYSTEM)
- ICA025 [SYSTEM] Tourism tradeoff (DEFER_SYSTEM)
- ICB024 [SYSTEM] Governor Title +1 per completion (DEFER_SYSTEM)
