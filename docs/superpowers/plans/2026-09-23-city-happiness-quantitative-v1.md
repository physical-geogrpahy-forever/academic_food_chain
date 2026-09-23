# City Happiness Quantitative V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved City Happiness quantitative core with era-based Needs expectations, bounded relative adjustment, Health separation, Building-master integration, static QA, and reproducible CI validation.

**Architecture:** The system is split into four small units. A CSV stores the 13-era per-capita expectations. A pure Python calculator loads that table and returns a cause-by-cause City Happiness breakdown. A separate validator checks that the current 104-row Building master exposes valid Needs and Local Happiness fields without mixing Health or Stability. A static QA generator runs fixed scenarios and writes a Markdown report. Existing Building, Health, Power and Stability authorities remain unchanged.

**Tech Stack:** Python 3.12 standard library only (`csv`, `math`, `dataclasses` or plain dictionaries, `pathlib`, `argparse`); GitHub Actions; existing repository CSV/Markdown conventions.

**Spec:** `docs/superpowers/specs/2026-09-23-city-happiness-quantitative-v1-design.md`

## Global Constraints

- Do not call static calculation or CI validation “runtime autoplay”. The game engine does not exist yet.
- Preserve the existing final Building authority at `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`; Happiness reads it but does not rewrite it.
- Keep `HEALTH_POINTS_FINAL`, `STABILITY_POINTS_FINAL`, Power fields and Happiness/Needs fields distinct.
- `gross_food_pre_health` excludes `Food_from_Health` so negative Health is not double-counted through Distress.
- Citizen Needs Unhappiness is capped at city population.
- Relative adjustment is optional and clamped to `[0.90, 1.10]` for every Needs category.
- External War Weariness, Occupation, Colonial and Policy Burden inputs remain named inputs with default 0.
- Use only Python standard library; no new dependencies.
- Apply TDD: failing test first, observe RED, implement minimal code, observe GREEN, then refactor if needed.

## Review Focus

1. **Zero-population transitional city:** must return zero Needs and zero Local Happiness while still passing through explicit external penalties exactly once.
2. **Relative-median edge values:** `None`, missing category, zero, negative or non-numeric medians must never silently corrupt expectations; invalid supplied values are rejected while an omitted relative layer means factor 1.00.
3. **Floating-point boundary behavior:** supported population uses `floor(yield / expectation)` deterministically; a value infinitesimally below a threshold must not round upward.
4. **Building-master schema drift:** validator must fail if any of the five Needs-reduction fields or `LOCAL_HAPPINESS` disappears or becomes non-numeric/negative.
5. **Cross-system contamination:** validator must explicitly reject any implementation path that treats `HEALTH_POINTS_FINAL` or `STABILITY_POINTS_FINAL` as a Needs reduction or Local Happiness field.

---

### Task 1: Add authoritative era expectation data and loader

**Files:**
- Create: `city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv`
- Create: `city_system/test_calculate_city_happiness_v1.py`
- Create: `city_system/calculate_city_happiness_v1.py`

**Interfaces:**
- Consumes: `HAPPINESS_ERA_EXPECTATIONS_V1.csv`
- Produces:
  - `load_expectations(path: Path) -> dict[str, dict[str, float]]`
  - `get_effective_expectations(era: str, expectations: dict, global_medians: dict[str, float] | None = None) -> dict[str, float]`

- [ ] **Step 1: Create the 13-era CSV**

Write exactly these columns and values:

```csv
ERA,BASIC_NEED,GOLD_NEED,SCIENCE_NEED,CULTURE_NEED
Ancient,2.00,0.75,0.75,0.40
Classical,2.20,1.00,1.00,0.50
Late Antiquity,2.40,1.10,1.20,0.60
Early Medieval,2.60,1.25,1.40,0.70
High Medieval,2.80,1.40,1.60,0.80
Renaissance,3.00,1.60,1.90,1.00
Exploration,3.20,1.80,2.20,1.20
Enlightenment,3.40,2.00,2.60,1.40
Industrial,3.60,2.30,3.00,1.60
Modern,3.80,2.60,3.50,1.90
Atomic,4.00,3.00,4.00,2.20
Information,4.20,3.40,4.60,2.60
Future,4.40,3.80,5.20,3.00
```

- [ ] **Step 2: Write failing loader and clamp tests**

Add tests equivalent to:

```python
def test_load_expectations_has_13_eras():
    data = module.load_expectations(EXPECTATIONS)
    assert len(data) == 13
    assert data["Ancient"]["basic"] == 2.0
    assert data["Future"]["science"] == 5.2


def test_relative_adjustment_clamps_to_ten_percent():
    data = module.load_expectations(EXPECTATIONS)
    hi = module.get_effective_expectations(
        "Ancient", data,
        {"basic": 3.0, "gold": 2.0, "science": 2.0, "culture": 1.0},
    )
    lo = module.get_effective_expectations(
        "Ancient", data,
        {"basic": 0.5, "gold": 0.1, "science": 0.1, "culture": 0.1},
    )
    assert hi["basic"] == 2.2
    assert lo["basic"] == 1.8


def test_unknown_era_rejected():
    data = module.load_expectations(EXPECTATIONS)
    with pytest.raises(ValueError, match="Unknown era"):
        module.get_effective_expectations("Stone Age", data)
```

Use plain `assert` plus a local helper if avoiding pytest; if repository CI has no pytest dependency, implement tests as executable Python scripts using `try/except` and explicit assertions.

- [ ] **Step 3: Run test and verify RED**

Run:

```bash
python city_system/test_calculate_city_happiness_v1.py
```

Expected: failure because loader/effective-expectation functions do not yet exist.

- [ ] **Step 4: Implement minimal loader and relative adjustment**

Implement:

```python
NEED_KEYS = {
    "BASIC_NEED": "basic",
    "GOLD_NEED": "gold",
    "SCIENCE_NEED": "science",
    "CULTURE_NEED": "culture",
}


def clamp(value, low, high):
    return max(low, min(high, value))


def load_expectations(path):
    ...


def get_effective_expectations(era, expectations, global_medians=None):
    ...
```

Rules:
- every expectation must be positive numeric;
- unknown era raises `ValueError`;
- omitted `global_medians` gives all factors 1.00;
- when supplied, all four categories must be present and strictly positive numeric;
- `factor = clamp(median / base, 0.90, 1.10)`;
- return exact float expectations by category.

- [ ] **Step 5: Run tests and verify GREEN**

Run the same command. Expected: expectation tests pass.

- [ ] **Step 6: Commit**

```bash
git add city_system/HAPPINESS_ERA_EXPECTATIONS_V1.csv city_system/calculate_city_happiness_v1.py city_system/test_calculate_city_happiness_v1.py
git commit -m "feat: add happiness era expectations"
```

---

### Task 2: Implement the pure City Happiness calculator

**Files:**
- Modify: `city_system/calculate_city_happiness_v1.py`
- Modify: `city_system/test_calculate_city_happiness_v1.py`

**Interfaces:**
- Consumes:
  - expectation table from Task 1
  - city yield/Health/reduction inputs
- Produces:
  - `calculate_city_happiness(...) -> dict[str, object]`
  - helper `health_unhappiness(health: int | float) -> int`

The calculator signature must remain explicit rather than accepting an opaque arbitrary dictionary:

```python
def calculate_city_happiness(
    *,
    era,
    population,
    gross_food_pre_health,
    production,
    gold,
    science,
    culture,
    city_health,
    minority_followers=0,
    religion_active=True,
    local_happiness_sources=0,
    distress_reduction=0,
    poverty_reduction=0,
    illiteracy_reduction=0,
    boredom_reduction=0,
    religious_unrest_reduction=0,
    global_medians=None,
    war_weariness_unhappiness=0,
    occupation_unhappiness=0,
    colonial_unhappiness=0,
    policy_burden_unhappiness=0,
    expectations_path=DEFAULT_EXPECTATIONS,
):
    ...
```

- [ ] **Step 1: Write RED tests for approved scenarios A-H**

Cover all eight design scenarios and the five Review Focus cases. Core assertions include:

```python
assert balanced["citizen_needs_unhappiness"] == 0
assert balanced["city_happiness"] == 0

assert underdeveloped["citizen_needs_pre_cap"] > 4
assert underdeveloped["citizen_needs_unhappiness"] == 4

assert reduced["illiteracy"] == max(0, baseline["illiteracy"] - 1)

assert health_case["health_unhappiness"] == 2
assert health_case["supported_basic"] == baseline_same_food["supported_basic"]

assert religion_case["religious_unrest_raw"] == 2

assert local_case["local_happiness_positive"] == 3

assert relative_hi["effective_expectations"]["science"] == 0.75 * 1.10

assert passthrough["external_penalties"]["war_weariness"] == 2
assert passthrough["city_happiness"] == expected_total
```

Also test:
- `population=0` with external penalties;
- negative population rejected;
- every yield input below zero rejected;
- reduction below zero rejected;
- minority followers > population rejected;
- global medians with missing category, zero, negative or string values rejected;
- a yield at `expectation * 3 - 1e-9` supports only 2 citizens.

- [ ] **Step 2: Run full calculator test and verify RED**

```bash
python city_system/test_calculate_city_happiness_v1.py
```

Expected: failure at missing `calculate_city_happiness` or missing returned fields.

- [ ] **Step 3: Implement validation and Needs arithmetic**

Use exactly:

```python
supported_basic = math.floor((gross_food_pre_health + production) / effective["basic"])
supported_gold = math.floor(gold / effective["gold"])
supported_science = math.floor(science / effective["science"])
supported_culture = math.floor(culture / effective["culture"])
```

For `population > 0`:

```python
distress_raw = max(0, population - supported_basic)
poverty_raw = max(0, population - supported_gold)
illiteracy_raw = max(0, population - supported_science)
boredom_raw = max(0, population - supported_culture)
```

Religious Unrest:

```python
if religion_active and population > 0:
    religious_unrest_raw = minority_followers // 2
else:
    religious_unrest_raw = 0
```

Post-reduction values use `max(0, raw - reduction)`.

Citizen cap:

```python
pre_cap = distress + poverty + illiteracy + boredom + religious_unrest
citizen_needs = min(population, pre_cap)
```

- [ ] **Step 4: Implement Health, Local Happiness and external penalties**

```python
def health_unhappiness(health):
    if health >= 0:
        return 0
    if health >= -2:
        return 1
    if health >= -4:
        return 2
    return 3
```

Local Happiness:

```python
local_positive = min(population, max(0, local_happiness_sources))
```

Final:

```python
external_total = (
    war_weariness_unhappiness
    + occupation_unhappiness
    + colonial_unhappiness
    + policy_burden_unhappiness
)
city_happiness = local_positive - citizen_needs - health_penalty - external_total
```

For population 0, Needs, Religious Unrest, Health Unhappiness and Local Happiness are forced to 0; explicit external penalties still pass through.

- [ ] **Step 5: Return a complete structured breakdown**

Return at least:

```python
{
    "era": era,
    "population": population,
    "effective_expectations": {...},
    "supported_basic": ...,
    "supported_gold": ...,
    "supported_science": ...,
    "supported_culture": ...,
    "distress_raw": ...,
    "poverty_raw": ...,
    "illiteracy_raw": ...,
    "boredom_raw": ...,
    "religious_unrest_raw": ...,
    "distress": ...,
    "poverty": ...,
    "illiteracy": ...,
    "boredom": ...,
    "religious_unrest": ...,
    "citizen_needs_pre_cap": ...,
    "citizen_needs_unhappiness": ...,
    "health_unhappiness": ...,
    "local_happiness_positive": ...,
    "external_penalties": {
        "war_weariness": ...,
        "occupation": ...,
        "colonial": ...,
        "policy_burden": ...,
    },
    "city_happiness": ...,
}
```

- [ ] **Step 6: Run tests and verify GREEN**

```bash
python city_system/test_calculate_city_happiness_v1.py
```

Expected final line:

```text
CITY_HAPPINESS_CALCULATOR_TEST: PASS
```

- [ ] **Step 7: Commit**

```bash
git add city_system/calculate_city_happiness_v1.py city_system/test_calculate_city_happiness_v1.py
git commit -m "feat: implement city happiness calculator"
```

---

### Task 3: Validate all 104 Building-master Happiness links

**Files:**
- Create: `city_system/validate_happiness_building_links_v1.py`
- Create: `city_system/test_validate_happiness_building_links_v1.py`

**Interfaces:**
- Consumes: `city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv`
- Produces:
  - `validate_building_links(path: Path) -> dict[str, object]`
  - command output summarizing rows and counts of reduction sources

- [ ] **Step 1: Write failing fixture test**

Fixture must include one valid row for each Needs category plus a row with Health and Stability final fields. Assert:

```python
result = module.validate_building_links(master)
assert result["rows"] == 5
assert result["distress_sources"] >= 1
assert result["poverty_sources"] >= 1
assert result["illiteracy_sources"] >= 1
assert result["boredom_sources"] >= 1
```

Then make malformed fixture variants and require failure for:
- missing `VP_DISTRESS_REDUCTION` column;
- negative `LOCAL_HAPPINESS`;
- non-numeric `VP_ILLITERACY_REDUCTION`;
- missing `HEALTH_POINTS_FINAL` or `STABILITY_POINTS_FINAL` cross-system guard columns.

- [ ] **Step 2: Run test and verify RED**

```bash
python city_system/test_validate_happiness_building_links_v1.py
```

Expected: missing validator module/function failure.

- [ ] **Step 3: Implement strict schema and numeric validation**

Required fields:

```python
REQUIRED = [
    "BUILDING_EN",
    "LOCAL_HAPPINESS",
    "VP_DISTRESS_REDUCTION",
    "VP_POVERTY_REDUCTION",
    "VP_ILLITERACY_REDUCTION",
    "VP_BOREDOM_REDUCTION",
    "VP_RELIGIOUS_UNREST_REDUCTION",
    "HEALTH_POINTS_FINAL",
    "STABILITY_POINTS_FINAL",
]
```

Rules:
- every required field exists;
- all Happiness/Needs values parse as numeric and are `>= 0`;
- Health/Stability are checked only for schema presence and numeric parse, never added to Happiness source counts;
- there must be at least one positive source for Distress, Poverty, Illiteracy and Boredom;
- Religious Unrest may be zero-source and is reported rather than failed.

- [ ] **Step 4: Run fixture test and verify GREEN**

Expected final line:

```text
HAPPINESS_BUILDING_LINK_TEST: PASS
```

- [ ] **Step 5: Run validator on the actual 104-row master**

```bash
python city_system/validate_happiness_building_links_v1.py
```

Expected format:

```text
HAPPINESS_BUILDING_LINK_QA: PASS rows=104 distress_sources=<n> poverty_sources=<n> illiteracy_sources=<n> boredom_sources=<n> religious_sources=<n>
```

If it fails, fix source data only when the failure is a real data defect; do not weaken the validator to hide missing or malformed fields.

- [ ] **Step 6: Commit**

```bash
git add city_system/validate_happiness_building_links_v1.py city_system/test_validate_happiness_building_links_v1.py
git commit -m "test: validate building happiness links"
```

---

### Task 4: Generate static QA report and quantitative authority document

**Files:**
- Create: `city_system/generate_city_happiness_static_qa_v1.py`
- Create: `city_system/CITY_HAPPINESS_STATIC_QA_V1.md`
- Create: `city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md`

**Interfaces:**
- Consumes: calculator and expectation CSV
- Produces: reproducible Markdown QA plus human-readable quantitative authority

- [ ] **Step 1: Write the QA generator using named scenarios**

Encode scenarios A-H from the design as data dictionaries, call `calculate_city_happiness`, and write a Markdown table with at least:
- scenario name;
- population;
- Needs pre-cap;
- Needs final;
- Health penalty;
- Local Happiness;
- external penalty total;
- final City Happiness;
- PASS/FAIL assertion summary.

The generator must exit nonzero if any scenario assertion fails.

- [ ] **Step 2: Add arithmetic sanity assertions**

In addition to A-H, include:
- population 0 passthrough;
- relative clamp high/low;
- floating threshold floor case;
- all four external penalties nonzero simultaneously to detect double-application.

- [ ] **Step 3: Run the generator**

```bash
python city_system/generate_city_happiness_static_qa_v1.py
```

Expected:

```text
CITY_HAPPINESS_STATIC_QA: PASS scenarios=12
```

- [ ] **Step 4: Write `CITY_HAPPINESS_QUANTITATIVE_V1.md`**

The authority document must state:
- the four Needs formulas;
- era expectation table source file;
- optional relative adjustment clamp;
- Religious Unrest formula;
- population cap;
- Health tiers;
- Local Happiness cap;
- full City Happiness equation;
- external penalty interface status;
- explicit statement that empire luxury Happiness is not silently distributed into city Local Happiness;
- explicit statement that this is pre-runtime static balance, not autoplay evidence;
- source/provenance distinction: VP structure, project-native numeric values.

- [ ] **Step 5: Commit**

```bash
git add city_system/generate_city_happiness_static_qa_v1.py city_system/CITY_HAPPINESS_STATIC_QA_V1.md city_system/CITY_HAPPINESS_QUANTITATIVE_V1.md
git commit -m "docs: lock city happiness quantitative v1"
```

---

### Task 5: Add CI and update the system authority index

**Files:**
- Create: `.github/workflows/city-happiness-qa.yml`
- Create: `city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V8.md`

**Interfaces:**
- Consumes: all Tasks 1-4 artifacts
- Produces: branch-level reproducible QA and new authority index

- [ ] **Step 1: Create CI workflow**

Workflow triggers on changes to:
- expectation CSV;
- calculator/test;
- Building master;
- Building validator/test;
- QA generator;
- quantitative Happiness authority.

Run, in this order:

```bash
python city_system/test_calculate_city_happiness_v1.py
python city_system/test_validate_happiness_building_links_v1.py
python city_system/validate_happiness_building_links_v1.py
python city_system/generate_city_happiness_static_qa_v1.py
```

Do not auto-edit the Building master in this workflow.

- [ ] **Step 2: Trigger CI and inspect every step**

Confirm all four commands exit 0. A green Actions wrapper without inspecting failed/skipped steps is not enough.

- [ ] **Step 3: Create `VP_SYSTEM_IMPLEMENTATION_INDEX_V8.md`**

Record:
- V7 remains historical predecessor;
- `CITY_HAPPINESS_QUANTITATIVE_V1.md` is the City Happiness numeric authority;
- `HAPPINESS_ERA_EXPECTATIONS_V1.csv` is the era-expectation numeric authority;
- final Building master remains Building numeric authority;
- Health and Stability remain independent fields;
- War Weariness is the next quantitative subsystem;
- runtime/autoplay remains deferred until an engine exists.

- [ ] **Step 4: Fresh final verification**

Re-run all four commands after the index/workflow commit or inspect the workflow run triggered by the final commit. Required evidence:

```text
CITY_HAPPINESS_CALCULATOR_TEST: PASS
HAPPINESS_BUILDING_LINK_TEST: PASS
HAPPINESS_BUILDING_LINK_QA: PASS rows=104 ...
CITY_HAPPINESS_STATIC_QA: PASS scenarios=12
```

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/city-happiness-qa.yml city_system/VP_SYSTEM_IMPLEMENTATION_INDEX_V8.md
git commit -m "ci: validate city happiness quantitative v1"
```

---

## Plan Self-Review

### Spec coverage

- 13-era expectation table: Task 1.
- Relative expectation adjustment capped at plus/minus 10 percent: Tasks 1-2.
- Distress/Poverty/Illiteracy/Boredom formulas: Task 2.
- Religious Unrest: Task 2.
- Citizen Needs population cap: Task 2.
- Health Unhappiness and Health/Distress double-count protection: Task 2.
- Local Happiness cap: Task 2.
- Named external penalty inputs: Task 2.
- Complete cause breakdown for UI/AI: Task 2.
- Building-master link audit: Task 3.
- Static scenarios and report: Task 4.
- Quantitative authority document: Task 4.
- Reproducible CI and authority index: Task 5.
- Runtime/autoplay boundary: Tasks 4-5.

No spec requirement is left without an owning task.

### Placeholder scan

The plan contains no implementation placeholder such as TBD/TODO. Later subsystems are named external interfaces by design rather than hidden unfinished work.

### Type and interface consistency

- Expectation categories are consistently `basic`, `gold`, `science`, `culture`.
- Building source columns use the existing exact master names.
- Calculator returns explicit named components used by the QA generator.
- Health and Stability are read only as separate system fields and never reused as Happiness reductions.

### Review-focus coverage

All five Review Focus risks have explicit tests in Tasks 2 or 3.
