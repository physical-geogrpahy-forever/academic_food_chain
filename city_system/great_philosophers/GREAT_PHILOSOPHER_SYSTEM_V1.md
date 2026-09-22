# Great Philosopher System V1

Date: 2026-09-22
Status: DESIGN LOCK V1

## 1. Class identity

Official class name:

`Great Philosopher / 위대한 철학가`

Scope includes:
- natural philosophy
- epistemology and philosophy of science
- metaphysics
- ethics
- religious philosophy and theology
- political philosophy and philosophy of law
- economic philosophy and political economy
- social philosophy
- aesthetics

The class is intentionally broader than modern academic philosophy.
Political philosophy and economic philosophy remain inside Great Philosopher rather than creating separate Great Person classes.

## 2. Core gameplay identity

Great Philosopher is the **cross-system Great Person class**.

Scientists mainly improve science and research.
Prophets found or strengthen religion.
Writers, Artists and Musicians mainly support culture.
Merchants mainly support commerce.

Great Philosophers instead connect systems that normally operate separately.

Typical links:
- Science <-> Culture
- Faith <-> Science
- Faith <-> Culture
- Government / civics <-> Culture
- Government / civics <-> Science
- Gold / Trade <-> Science
- Gold / Trade <-> Culture
- Happiness / Health <-> Culture or Science
- specialists / population <-> Culture or Science

A Philosopher ability should normally change a rule, create a conditional conversion, connect two systems, or create a limited-duration intellectual effect.

Avoid making the class a generic:
`Science + X, Culture + Y, Faith + Z`
bundle.

## 3. Recruitment model

Great Philosopher uses the project's worldwide named-person recruitment system.

- one named Great Philosopher candidate is globally available at a time;
- civilizations accumulate Great Philosopher Points (GPhP);
- the first eligible civilization to meet the current candidate requirement may recruit that Philosopher;
- the individual is removed globally after recruitment;
- the next eligible candidate appears;
- overflow GPhP is retained.

Great Philosopher is **not** a Faith-purchase class.
Great Prophet remains the project's direct-Faith-purchase religious Great Person.

Great Philosopher does **not** found a religion and does not replace Great Prophet.

## 4. No Philosopher specialist

There is no dedicated Philosopher specialist.

Reason:
- the city system already contains Scientist, Engineer, Merchant, Writer, Artist, Musician and Director specialist structures;
- another specialist would add city-management clutter;
- historically, philosophy emerged from several institutional settings rather than one specialized urban occupation.

Great Philosopher Points instead come from **institutional diversity**.

## 5. Thought-chain system

Each city can activate up to five distinct philosophical institution chains.

A chain is active if the city contains at least one qualifying building in that family.

Multiple buildings in the same family do **not** stack.

For example:
`Library + University + Public School`
still counts as only one `KNOWLEDGE` chain.

### A. KNOWLEDGE

Qualifying buildings:
- Library
- Paper Workshop
- University
- Observatory
- Chemical Laboratory
- Public School
- Research Lab

Represents:
- natural philosophy
- epistemology
- mathematics
- philosophy of science

### B. RELIGION_NATURE

Qualifying buildings:
- Grove
- Shrine
- Garden
- Temple
- Sanctuary

Represents:
- theology
- religious philosophy
- metaphysics
- natural philosophy and moral traditions

### C. CULTURE_MEDIA

Qualifying buildings:
- Amphitheater
- Scriptorium
- Woodblock Printing House
- Printing Press
- Opera House
- Art Museum
- Archaeological Museum
- Newspaper Office
- Cinema
- Broadcast Center
- Film Studio
- Writers' Guild
- Artists' Guild
- Musicians' Guild
- Director's Guild

`Monument` alone does **not** activate the chain.

Represents:
- rhetoric
- aesthetics
- humanities
- public discourse
- social criticism

### D. GOVERNMENT_DIPLOMACY

Qualifying buildings:
- Government Plaza
- Ancestral Hall
- Audience Chamber
- Warlord's Throne
- Consulate
- Court
- Chancery
- Foreign Ministry
- Grand Master's Chapel
- Intelligence Agency
- National History Museum
- Royal Society
- War Department

The following administrative/security buildings do not activate the philosophical chain by themselves:
- Courthouse
- Constabulary
- Telegraph Office

Represents:
- political philosophy
- philosophy of law
- statecraft
- constitutional and diplomatic thought

### E. COMMERCE_TRADE

Qualifying buildings:
- Market
- Bank
- Customs Office
- Stock Exchange

The following do not activate the chain by themselves:
- Caravansary
- Mint
- Shopping Mall

Represents:
- economic philosophy
- political economy
- theories of trade, value and wealth

## 6. Great Philosopher Point formula

For each city, let:

`N = number of distinct active thought chains`

Then:

`City GPhP per turn = max(0, N - 1)`

Therefore:

| Active thought chains | GPhP / turn |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |

This is calculated per city and summed civilization-wide.

Examples:

- Library only -> 0 GPhP
- Library + Shrine -> 1 GPhP
- Library + Shrine + Amphitheater -> 2 GPhP
- Library + Temple + Amphitheater + Market -> 3 GPhP
- Library + Temple + Amphitheater + Government Plaza + Market -> 4 GPhP

The system therefore rewards **institutional diversity**, not building spam.

## 7. Why no within-chain stacking

Without the non-stacking rule, a late-game city containing:
Library -> University -> Public School -> Research Lab
would generate several Philosopher points from the same intellectual tradition.

That would make Great Philosopher effectively another Scientist class.

The diversity formula instead makes philosophy strongest in cities where scientific, religious, cultural, political and economic institutions coexist.

## 8. Candidate eligibility

Historical activity period determines the Philosopher's era label.

Use the same chronology already locked for Great Scientist activity audits:
- Ancient: before 500 BCE
- Classical: 500 BCE–299 CE
- Late Antiquity: 300–599
- Early Medieval: 600–999
- High Medieval: 1000–1299
- Renaissance: 1300–1499
- Exploration: 1500–1699
- Enlightenment: 1700–1799
- Industrial: 1800–1899
- Modern: 1900–1944
- Atomic: 1945–1989
- Information: 1990–present
- Future: no historical-person roster

Class assignment is based on the historical work represented by the candidate.

A person belongs to Great Philosopher when the representative achievement is a systematic account of knowledge, ethics, religion, politics, economics, society, law, aesthetics or related philosophical questions.

A person remains Great Scientist when the representative achievement is primarily mathematical, observational, experimental or theoretical investigation of natural phenomena.

Do not classify solely from period terminology such as "natural philosopher."

## 9. Boundary with other Great Person classes

### Philosopher vs Scientist

Use Philosopher when:
- the representative work concerns knowledge, method, metaphysics, ethics, society, politics, economics or religion as a conceptual system.

Use Scientist when:
- the representative work is primarily a scientific discovery, mathematical theory, experiment, observation, empirical classification or physical/biological model.

### Philosopher vs Prophet

Use Prophet when:
- the representative identity is founding, revealing, institutionalizing or reforming a religion.

Use Philosopher when:
- the representative identity is theological or religious-philosophical argument.

A Philosopher may affect Faith but cannot found a religion.

### Philosopher vs Writer

Use Writer when:
- literary production itself is the representative achievement.

Use Philosopher when:
- the text is primarily a systematic philosophical, political, economic, ethical or social argument.

### Philosopher vs Merchant

Use Merchant when:
- the representative achievement is commerce, enterprise, finance or business operation.

Use Philosopher when:
- the representative achievement is a theory of value, trade, markets, political economy or economic order.

## 10. Ability design rules

Each named Great Philosopher receives one individual ability.

Preferred mechanics:
- connect Science and Culture;
- connect Faith and Science or Culture;
- connect Gold/Trade and Culture or Science;
- connect government/civics and intellectual yields;
- convert one system's success into another system's progress;
- temporary empire-wide intellectual movements;
- city-specific schools of thought;
- conditional Eureka + Inspiration combinations;
- specialist interactions across different specialist classes.

Avoid:
- repeated flat `Science + Culture + Faith` packages;
- simple permanent `building +1 yield` as the default pattern;
- religion founding;
- generic Great Works of Philosophy in V1;
- a generic Philosopher tile improvement.

## 11. Ability duration mix

The roster should mix:
- one-time active effects;
- charge-based abilities;
- 10–20 turn intellectual movements;
- one-city permanent institutional effects;
- conditional civilization-wide effects;
- limited technology/civic acceleration.

Not every Philosopher should create a permanent empire modifier.

## 12. Great Work policy

V1 does not introduce a separate Great Work of Philosophy system.

Reason:
- Great Writers already own the Great Work of Writing space;
- duplicating that system would blur class identity;
- Philosopher identity is better expressed through cross-system rules.

A philosophy-work subsystem can be reconsidered only if later culture-system testing shows a clear need.

## 13. Patronage

Default recruitment is GPhP competition.

If Civ VI-style patronage is later enabled for specialist-GPP classes:
- Gold patronage may apply to Great Philosopher;
- Faith patronage should remain disabled by default to preserve Great Prophet's distinct Faith-purchase identity.

This remains provisional until the global patronage formula is locked.

## 14. Initial implementation rule

Implementation can be handled without a new specialist table.

For each city each turn:
1. test the five thought-chain flags;
2. count active flags;
3. calculate `max(0, flags - 1)`;
4. add that amount to civilization-wide Great Philosopher Points.

This requires only five boolean chain flags per city and one integer accumulation.

## 15. Next content pass

Before building the Philosopher roster:
1. audit existing Great Scientists for class transfer candidates;
2. later audit Writers, Merchants and Prophets for cross-class candidates;
3. build a broad Philosopher candidate pool by activity period;
4. give every candidate an individual cross-system ability;
5. do not quota-balance eras or regions artificially.

Likely Scientist-to-Philosopher review cases include:
- Aristotle
- Francis Bacon
- René Descartes
- Ibn Khaldun
- Gottfried Wilhelm Leibniz

These are review candidates only, not automatic transfers.
