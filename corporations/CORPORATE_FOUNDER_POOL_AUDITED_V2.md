# Corporate Founder Pool Audited V2

Date: 2026-09-20  
Status: **AUDITED CANDIDATE POOL — 99 candidates; not yet final Great Person lock**

## 1. Purpose

This file supersedes the candidate-count target in `CORPORATE_FOUNDER_POOL_RESEARCH_V1.md` while preserving V1 as the source-audit archive for the original 61 entries.

V2 contains **99 founder candidates**:
- 61 inherited from the V1 primary-source audit
- 38 newly added or previously deferred candidates
- every row now has a project era, Great Person class, signature firm, founder-status wording, sector, output class, product/service, exact technology gate from the locked 109-tech V2 tree, and civic gate

Machine-readable authority:
`corporations/CORPORATE_FOUNDER_POOL_AUDITED_V2.csv`

## 2. Gate rule

General corporation founding gate remains:

**Capitalism + sector-specific technology**

All technology names in V2 are taken from the locked 109-tech roster. No new technology was invented merely to fit a company.

Examples:
- finance -> Banking
- petroleum -> Refining
- automotive -> Combustion
- electrical equipment -> Electricity
- chemicals/cosmetics -> Chemistry
- pharmaceuticals -> Biology
- semiconductors/electronics -> Electronics
- software -> Computers
- modern telecommunications/digital networks -> Telecommunications
- aerospace -> Flight
- steel -> Steel
- retail/apparel -> Mass Production
- shipping -> Steam Power
- logistics -> Railroad or Advanced Flight according to business model

## 3. Counts

### Region
- Europe/North America: 44
- East Asia: 23
- Southeast Asia: 9
- South Asia: 7
- Latin America: 6
- Middle East: 5
- Africa: 4
- Oceania: 1

### Great Person class
- Great Merchant: 53
- Great Engineer: 46

### Project era
- Industrial: 23
- Atomic: 43
- Modern: 20
- Information: 13

## 4. Newly added / resolved candidates

The 38 additions include:
- Thomas Edison
- George Westinghouse
- Steve Jobs
- Steve Wozniak
- Bill Gates
- Paul Allen
- Morris Chang
- Wang Chuanfu
- Dhirubhai Ambani
- Sam Walton
- Phil Knight
- Bill Bowerman
- Frederick W. Smith
- A.P. Møller
- William Boeing
- Cornelius Vander Starr
- Marcos Galperin
- David Vélez
- Cristina Junqueira
- Melanie Perkins
- Nadiem Makarim
- Tony Tan Caktiong
- Suh Sung-whan
- Shin Kyuk-ho
- Lee Hae-jin
- Kim Beom-su
- Chung Ju-yung
- Miguel Krigsner
- Patrice Motsepe
- Gil Shwed
- Forrest Li
- William Tanuwijaya
- Min-Liang Tan
- Anita Roddick
- Cher Wang
- Huda Kattan
- Lakshmi Mittal
- Jim Casey

This resolves most of the V1 deferred list while deliberately avoiding candidate inflation from listing every member of a large founding team.

## 5. Important founder-status rules

- `Founder` does **not** imply sole founder.
- Where corporate history clearly identifies a co-founder, V2 says `Co-founder`.
- Conglomerate or merger lineages use `Founder-lineage` or similarly qualified wording.
- Lee Byung-chul remains tied to the Samsung group lineage, not falsely labeled sole founder of Samsung Electronics.
- Thomas Edison is tied to Edison electric-company / GE lineage, not labeled sole founder of modern General Electric.
- Lakshmi Mittal is tied to Mittal Steel / ArcelorMittal lineage.
- Ozires Silva remains a special case: key creator and first managing director of state-created Embraer, **not a strict private-company founder**.

## 6. Remaining flagged cases

- **Liu Chuanzhi** — LOCK_CANDIDATE: treated as representative founding-team leader / co-founder; not as sole founder
- **Ozires Silva** — REFERENCE_ONLY_INSTITUTIONAL_CREATOR: state-created Embraer key creator / first managing director; excluded from ordinary signature-founder roster

These flagged cases may remain in the research pool but should not be promoted to an unqualified signature-founder lock until wording is settled.

## 7. Design implications

The expanded pool now covers:
- finance and insurance
- retail and distribution
- apparel, cosmetics, food and hospitality
- petroleum, chemicals and pharmaceuticals
- steel, mining and construction materials
- automobiles, machinery and aerospace
- electrical equipment and electronics
- semiconductors, computers and software
- telecommunications and cybersecurity
- shipping, parcel delivery and express logistics
- e-commerce, fintech and digital platforms

The next design task is therefore **not further indiscriminate founder collection**. It is:

1. finalize the sector/output catalogue;
2. reconcile duplicate or overlapping sectors;
3. define quantitative supply/branch effects;
4. review the small number of flagged founder-status edge cases;
5. then freeze the signature-founder subset used by the game.

Do not move to the 109-tech building/unit unlock table until the corporation sector/output catalogue and gates are reconciled.


## 8. Final V2 integrity QA

Result after canonical-sector reconciliation:

- founder rows: **99**
- canonical sectors: **32**
- sectors populated by current founders: **30**
- Great Merchant: **53**
- Great Engineer: **46**
- LOCK_CANDIDATE: **98**
- Liu Chuanzhi: **promoted to LOCK_CANDIDATE**
- REFERENCE_ONLY_INSTITUTIONAL_CREATOR: **1** — Ozires Silva
- missing technology references: **0**
- missing civic references: **0**
- technology gates later than founder project era: **0**
- missing canonical-sector references: **0**
- sector/gate mismatches: **0**
- non-hybrid output-class mismatches: **0**
- duplicate founders: **0**
- missing source fields: **0**

Canonical sector authority:
- `corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.csv`
- `corporations/CORPORATION_SECTOR_OUTPUT_CATALOGUE_V2.md`


## 9. Edge-case resolution

The two remaining founder-status edge cases are now resolved for gameplay purposes:

- **Liu Chuanzhi**: keep as a normal signature-founder candidate. Use the wording **Founding-team leader / co-founder**. Do not present him as a sole founder.
- **Ozires Silva**: keep in the 99-row historical research pool, but **exclude from the ordinary signature-founder roster**. His role is recorded as **Institutional creator / first managing director** because Embraer was state-created.

Therefore:
- historical research pool = **99**
- ordinary signature-founder eligible pool = **98**
- institutional reference-only = **1**
