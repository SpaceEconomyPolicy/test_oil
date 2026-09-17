# Test Oil Reference Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `SpaceEconomyPolicy/test_oil` as a rigorous organizer-side reference repository for the case «Топливный космоконтур 2035», with machine-readable source data, canonical calculation rules, reproducible synthetic validation examples, scientific grounding, and a detailed participant-facing README, without providing a ready competition solution.

**Architecture:** The repository is documentation-and-data first. Official case inputs, scenario definitions, schemas, validation vectors, and explanatory documents are separated so teams can implement their own software stacks while sharing the same semantics and jury checks. No optimizer, dashboard, recommended supply mix, recommended investment schedule, or ready-to-submit solution is included.

**Tech Stack:** Markdown, CSV, YAML, JSON Schema Draft 2020-12, Mermaid diagrams, Python 3 only for maintainer-side validation commands in this plan, plus optional `PyYAML` and `jsonschema` for validating static artifacts during implementation.

**Spec:** `docs/superpowers/specs/2026-09-18-fuel-space-contour-reference-repository-design.md`

## Global Constraints

- Repository purpose: organizer reference framework, not a participant solution.
- Do not include a recommended procurement plan, optimal source mix, recommended investment timing, MCDA weights, ready optimizer, or ready dashboard.
- Preserve organizer case inputs exactly; do not silently reconcile ambiguous or missing source material.
- Every configurable parameter must be identifiable as `CASE_INPUT`, `TEAM_DECISION`, or `TEAM_ASSUMPTION` in documentation.
- BASE and mandatory STRESS must remain separate from team-defined research scenarios.
- Mandatory STRESS: +15% total and critical base demand in 2038-2040; +25% Earth-Core and Earth-Flex variable prices in 2038-2039 only; Lunar-ISRU actual delivery at 55% of plan in 2038 and 75% in 2039, returning to plan in 2040; `losses / throughput <= 2%` from 2038.
- Do not multiply mandatory-stress Lunar-ISRU delivery shares by reliability a second time.
- In BASE, reliability is not an automatic delivery multiplier.
- Critical demand is included in total demand and must not be added twice.
- Control material balance: `I_end = I_start + Q_delivered - Losses - Q_served`; shortage is separate from physical inventory.
- Control reserve rule: `R_y = D_y * 45 / 365` using total demand for the applicable year/scenario.
- Control losses use gross period inflow as throughput; do not apply the same modeled loss twice.
- Earth-New option cost is `90 + 270 = 360` mln units; do not add another 360.
- Emergency may not be treated as the base supply channel for more than two consecutive years.
- Scientific sources must be mapped as `source -> method/statement -> repository use -> limitation`; literature must not be used to justify synthetic case prices or capacities unless it actually contains those data.
- The source workbook `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx` is currently absent from the provided materials; document that gap in provenance and do not invent missing values.
- Russian copy should be technically precise and readable; use the provided humanizer guidance only as an editing-quality checklist, not as a detector-evasion guarantee and not as a reason to introduce mistakes.

---

## File Structure to Create

```text
README.md

data/
├── README.md
├── demand.csv
├── supply_sources.csv
├── storage_options.csv
├── investment_options.csv
└── constraints.csv

scenarios/
├── README.md
├── base.yaml
└── mandatory_stress.yaml

schemas/
├── demand.schema.json
├── supply_sources.schema.json
├── plan.schema.json
├── scenario.schema.json
└── export.schema.json

examples/
├── empty_plan.json
├── example_export_structure.csv
└── invalid_plan_examples/
    ├── negative_reservation.json
    ├── over_capacity.json
    └── malformed_scenario.json

validation/
├── README.md
├── control_cases.md
└── expected_checks.json

docs/
├── CASE_RULES.md
├── DATA_DICTIONARY.md
├── CALCULATION_RULES.md
├── STRESS_PROTOCOL.md
├── JURY_CHECKLIST.md
├── SCIENTIFIC_BASIS.md
├── SOURCES.md
├── ERRATA_AND_PROVENANCE.md
└── FAQ.md
```

The repository intentionally does **not** create `src/`, `app.py`, `optimizer.py`, a dashboard, or a finished participant codebase in this implementation phase.

---

### Task 1: Build the provenance and source-of-truth ledger

**Files:**
- Create: `docs/ERRATA_AND_PROVENANCE.md`

**Interfaces:**
- Consumes: approved design spec and the organizer documents used to formulate the case.
- Produces: a source ledger that every data and documentation task cites when transferring case values.

- [ ] **Step 1: Write the provenance rules at the top of the file**

Use this exact structure:

```markdown
# Происхождение данных, расхождения и границы исходного набора

Этот файл фиксирует, откуда перенесено каждое обязательное числовое условие стартового репозитория. Если исходные материалы расходятся или нужный файл отсутствует, репозиторий не подменяет это догадкой.

## Правила переноса

1. `CASE_INPUT` переносится без скрытого исправления смысла.
2. Если значение задано диапазоном, диапазон сохраняется.
3. Если одна и та же величина описана в нескольких материалах, фиксируются все источники и выбранная трактовка.
4. Если первичный файл отсутствует, это отмечается явно.
5. Научная публикация не заменяет синтетические цены, мощности и лимиты организатора.
```

- [ ] **Step 2: Add the missing-source-workbook note**

Add a section stating that the case documents refer to `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx`, sheet `Данные кейса 2`, but that workbook is not present in the provided material set currently used to build `test_oil`. State that machine-readable values in the repository are therefore transcribed from the case DOCX and jury note and must be reconciled if the original XLSX is later supplied.

- [ ] **Step 3: Add a parameter provenance table**

Create rows for at least all of the following values:

```text
Demand 2035: total 100, critical 80, low 80, high 110
Demand 2036: total 140, critical 105, low 112, high 154
Demand 2037: total 190, critical 135, low 152, high 209
Demand 2038: total 250, critical 170, low 200, high 312.5
Demand 2039: total 320, critical 210, low 256, high 400
Demand 2040: total 390, critical 250, low 312, high 487.5

Earth-Core: capacity 190, variable cost 6.2, reservation rate 0.45, take-or-pay 0.70, lead time 12 months, reliability 0.96
Earth-Flex: capacity 110, variable cost 8.9, reservation rate 0.15, take-or-pay 0, lead time 4 months, reliability 0.985
Earth-New: capacity 130, variable cost 7.1, reservation rate 0.30, take-or-pay 0.50, lead time 18-24 months, reliability 0.88 first year / 0.94 later
Lunar-ISRU: capacity 120, variable cost 3.0, reservation rate 0, take-or-pay 0, post-commissioning lead time 1-2 months, reliability 0.78/0.90/0.93 for 2038/2039/2040
Emergency: capacity 80, variable cost 13.8, reservation rate 0.35, lead time 6 weeks, reliability 0.995

Base storage: capacity 70, loss rate 0.045 of throughput, holding cost 0.72 mln units per t-year
ZBO option: CAPEX 180, capacity 120, loss rate 0.012 of throughput, additional OPEX 12/year, available as option from 2036
Lunar-ISRU pilot: CAPEX 1250, financing required before 2038, operation from 2038, fixed OPEX 70/year
Earth-New option: option fee 90, exercise cost 270, total 360

BASE service minimums: 0.99 critical, 0.97 total
CAPEX through end-2037 <= 1800
Cumulative CAPEX through 2040 <= 2800
Reserve = 45 days of applicable total demand or contractually equivalent emergency reserve
Emergency base-channel use <= 2 consecutive years
```

The table columns must be:

```text
parameter_id | value | unit | status | organizer_source | interpretation_note | unresolved_issue
```

Use `CASE_INPUT` for these organizer values.

- [ ] **Step 4: Add a separate section for mandatory stress provenance**

Document exactly:

```text
2038-2040 total and critical base demand multiplier = 1.15
2038-2039 Earth-Core variable price multiplier = 1.25
2038-2039 Earth-Flex variable price multiplier = 1.25
2040 Earth-Core and Earth-Flex price multiplier = 1.00 relative to base
2038 Lunar-ISRU actual delivery share = 0.55 of plan
2039 Lunar-ISRU actual delivery share = 0.75 of plan
2040 Lunar-ISRU actual delivery share = 1.00 of plan
2038 onward loss ceiling = 0.02 of throughput
```

Explicitly record that `0.55` and `0.75` are actual stress-delivery shares and are not multiplied by reliability again.

- [ ] **Step 5: Self-check the file for invented data**

Run a manual line-by-line check against the approved design and organizer materials. The file must contain no launcher names, market prices, post-2040 forecasts, or invented geopolitical probabilities.

- [ ] **Step 6: Commit**

```bash
git add docs/ERRATA_AND_PROVENANCE.md
git commit -m "docs: add case data provenance ledger"
```

---

### Task 2: Create normalized organizer input data

**Files:**
- Create: `data/demand.csv`
- Create: `data/supply_sources.csv`
- Create: `data/storage_options.csv`
- Create: `data/investment_options.csv`
- Create: `data/constraints.csv`
- Create: `data/README.md`

**Interfaces:**
- Consumes: provenance ledger from Task 1.
- Produces: machine-readable organizer inputs used by participant implementations and later schemas/docs.

- [ ] **Step 1: Create `data/demand.csv`**

Use exactly:

```csv
year,base_total_t,base_critical_t,low_total_t,high_total_t,status
2035,100,80,80,110,CASE_INPUT
2036,140,105,112,154,CASE_INPUT
2037,190,135,152,209,CASE_INPUT
2038,250,170,200,312.5,CASE_INPUT
2039,320,210,256,400,CASE_INPUT
2040,390,250,312,487.5,CASE_INPUT
```

- [ ] **Step 2: Verify critical demand never exceeds total demand**

Run:

```bash
python - <<'PY'
import csv
with open('data/demand.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 6
for r in rows:
    assert float(r['base_critical_t']) <= float(r['base_total_t'])
print('demand.csv OK')
PY
```

Expected output:

```text
demand.csv OK
```

- [ ] **Step 3: Create `data/supply_sources.csv` without flattening time-varying reliability incorrectly**

Use these columns:

```csv
source_id,name,capacity_t_per_year,variable_cost_mln_per_t,reservation_rate_mln_per_t_year_capacity,take_or_pay_share,lead_time_min_months,lead_time_max_months,reliability_profile,available_from_year,status,notes
```

Populate:

```csv
A,Earth-Core,190,6.2,0.45,0.70,12,12,"constant:0.96",2035,CASE_INPUT,"long-term Earth-to-orbit channel"
B,Earth-Flex,110,8.9,0.15,0.00,4,4,"constant:0.985",2035,CASE_INPUT,"flexible Earth-to-orbit channel"
C,Earth-New,130,7.1,0.30,0.50,18,24,"first_operating_year:0.88;later:0.94",,CASE_INPUT,"capacity available only after option exercise and preparation"
D,Lunar-ISRU,120,3.0,0.00,0.00,1,2,"2038:0.78;2039:0.90;2040:0.93",2038,CASE_INPUT,"available after required CAPEX financing and commissioning"
E,Emergency,80,13.8,0.35,0.00,1.5,1.5,"constant:0.995",2035,CASE_INPUT,"six-week lead time represented as 1.5 months for data interchange; authoritative wording remains six weeks"
```

The `available_from_year` cell for Earth-New remains blank because availability depends on the participant's option exercise timing plus 18-24 month preparation. Explain this in `data/README.md`; do not invent a fixed year.

- [ ] **Step 4: Verify capacity and take-or-pay ranges**

Run:

```bash
python - <<'PY'
import csv
with open('data/supply_sources.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert {r['source_id'] for r in rows} == {'A','B','C','D','E'}
for r in rows:
    assert float(r['capacity_t_per_year']) >= 0
    top = float(r['take_or_pay_share'])
    assert 0 <= top <= 1
print('supply_sources.csv OK')
PY
```

Expected output:

```text
supply_sources.csv OK
```

- [ ] **Step 5: Create `data/storage_options.csv`**

Use:

```csv
storage_id,name,capacity_t,loss_rate_on_throughput,holding_cost_mln_per_t_year,capex_mln,fixed_opex_mln_per_year,available_from_year,status,notes
BASE,Base storage,70,0.045,0.72,0,0,2035,CASE_INPUT,"existing storage"
ZBO,ZBO modernization,120,0.012,0.72,180,12,2036,CASE_INPUT,"case-model coefficient; not a universal real ZBO performance claim"
```

- [ ] **Step 6: Create `data/investment_options.csv`**

Use:

```csv
investment_id,name,option_fee_mln,exercise_cost_mln,total_capex_mln,commissioning_rule,fixed_opex_mln_per_year,status,notes
EARTH_NEW,Earth-New option,90,270,360,"18-24 months after exercise/preparation decision",0,CASE_INPUT,"do not add another 360 on top of 90+270"
LUNAR_ISRU,Lunar-ISRU pilot,0,1250,1250,"must be financed before 2038; available from 2038",70,CASE_INPUT,"capacity effect is defined in supply_sources.csv"
ZBO,ZBO modernization,0,180,180,"option available from 2036",12,CASE_INPUT,"capacity becomes 120 t; loss rate becomes 1.2% of throughput"
```

- [ ] **Step 7: Create `data/constraints.csv`**

Use these rows:

```csv
constraint_id,metric,operator,value,unit,period,scenario,severity,status,description
BASE_CRITICAL_SERVICE,critical_service_level,>=,0.99,share,annual,BASE,hard,CASE_INPUT,"critical demand service minimum"
BASE_TOTAL_SERVICE,total_service_level,>=,0.97,share,annual,BASE,hard,CASE_INPUT,"total demand service minimum"
CAPEX_2037,cumulative_capex,<=,1800,mln_units,through_2037,ALL,hard,CASE_INPUT,"CAPEX through end-2037"
CAPEX_2040,cumulative_capex,<=,2800,mln_units,through_2040,ALL,hard,CASE_INPUT,"total CAPEX through 2040"
RESERVE_45D,reserve_equivalent_days,>=,45,days,annual,ALL,hard,CASE_INPUT,"physical stock or demonstrably equivalent contracted emergency reserve"
EMERGENCY_BASE_STREAK,emergency_base_channel_consecutive_years,<=,2,years,2035_2040,ALL,hard,CASE_INPUT,"Emergency cannot serve as the base channel for more than two consecutive years"
STRESS_LOSS_LIMIT,losses_divided_by_throughput,<=,0.02,share,2038_2040,MANDATORY_STRESS,hard,CASE_INPUT,"applies from 2038 in mandatory stress only"
```

Do not encode the ISRU reliability statement as a hard generic numerical constraint that changes the organizer input; explain it in documentation as a bound on unsupported participant reinterpretation of first-year reliability.

- [ ] **Step 8: Create `data/README.md`**

It must explain:

- critical demand is nested within total demand;
- money is in mln conditional units in constant 2035 prices;
- Earth-New availability depends on the participant's exercise date and lead time;
- Emergency authoritative lead time is six weeks; the numeric 1.5 months is only an interchange approximation and must not override the written rule where timing precision matters;
- `reliability_profile` is descriptive input for risk analysis, not a BASE delivery multiplier;
- ZBO 1.2% is a case-model loss coefficient, not a physical claim about all ZBO systems;
- all values are transcribed from current organizer documents pending reconciliation with the absent source workbook.

- [ ] **Step 9: Run static data checks**

Run:

```bash
python - <<'PY'
import csv
for path in [
    'data/demand.csv',
    'data/supply_sources.csv',
    'data/storage_options.csv',
    'data/investment_options.csv',
    'data/constraints.csv',
]:
    with open(path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert rows, f'{path} is empty'
    assert all('status' in r for r in rows), f'{path} missing status'
print('all CSV files parse and contain status')
PY
```

Expected output:

```text
all CSV files parse and contain status
```

- [ ] **Step 10: Commit**

```bash
git add data
git commit -m "data: add normalized case inputs"
```

---

### Task 3: Encode BASE and mandatory STRESS as separate scenario data

**Files:**
- Create: `scenarios/base.yaml`
- Create: `scenarios/mandatory_stress.yaml`
- Create: `scenarios/README.md`

**Interfaces:**
- Consumes: normalized data from Task 2.
- Produces: scenario files that participant software can load without embedding scenario constants in UI code.

- [ ] **Step 1: Create `scenarios/base.yaml`**

Use:

```yaml
scenario_id: BASE
label_ru: "Стандартный сценарий"
status: CASE_INPUT
demand_multiplier:
  default: 1.0
variable_price_multiplier:
  default: 1.0
actual_delivery_share:
  default: 1.0
loss_ceiling:
  enabled: false
notes:
  - "BASE does not apply reliability as an automatic delivery multiplier."
```

- [ ] **Step 2: Create `scenarios/mandatory_stress.yaml`**

Use:

```yaml
scenario_id: MANDATORY_STRESS
label_ru: "Обязательный стрессовый сценарий"
status: CASE_INPUT
demand_multiplier:
  2035: 1.0
  2036: 1.0
  2037: 1.0
  2038: 1.15
  2039: 1.15
  2040: 1.15
critical_demand_multiplier:
  2035: 1.0
  2036: 1.0
  2037: 1.0
  2038: 1.15
  2039: 1.15
  2040: 1.15
variable_price_multiplier:
  Earth-Core:
    2035: 1.0
    2036: 1.0
    2037: 1.0
    2038: 1.25
    2039: 1.25
    2040: 1.0
  Earth-Flex:
    2035: 1.0
    2036: 1.0
    2037: 1.0
    2038: 1.25
    2039: 1.25
    2040: 1.0
actual_delivery_share:
  Lunar-ISRU:
    2038: 0.55
    2039: 0.75
    2040: 1.0
loss_ceiling:
  enabled: true
  from_year: 2038
  max_losses_divided_by_throughput: 0.02
notes:
  - "55% and 75% are actual delivery shares and must not be multiplied by reliability again."
  - "Reservation tariffs, CAPEX and other prices are not changed by the mandatory +25% price shock."
```

- [ ] **Step 3: Create `scenarios/README.md`**

Explain three namespaces:

```text
BASE                  organizer control scenario
MANDATORY_STRESS      organizer control stress
TEAM_*                optional participant research scenarios
```

State that `TEAM_*` scenarios must not silently overwrite `BASE` or `MANDATORY_STRESS` files.

- [ ] **Step 4: Parse the YAML files**

Run:

```bash
python -m pip install --quiet pyyaml
python - <<'PY'
from pathlib import Path
import yaml
for p in [Path('scenarios/base.yaml'), Path('scenarios/mandatory_stress.yaml')]:
    obj = yaml.safe_load(p.read_text(encoding='utf-8'))
    assert obj['scenario_id']
print('scenario YAML OK')
PY
```

Expected output:

```text
scenario YAML OK
```

- [ ] **Step 5: Assert the mandatory stress constants exactly**

Run:

```bash
python - <<'PY'
import yaml
s = yaml.safe_load(open('scenarios/mandatory_stress.yaml', encoding='utf-8'))
assert s['demand_multiplier'][2038] == 1.15
assert s['critical_demand_multiplier'][2040] == 1.15
assert s['variable_price_multiplier']['Earth-Core'][2038] == 1.25
assert s['variable_price_multiplier']['Earth-Core'][2040] == 1.0
assert s['actual_delivery_share']['Lunar-ISRU'][2038] == 0.55
assert s['actual_delivery_share']['Lunar-ISRU'][2039] == 0.75
assert s['loss_ceiling']['max_losses_divided_by_throughput'] == 0.02
print('mandatory stress constants OK')
PY
```

Expected output:

```text
mandatory stress constants OK
```

- [ ] **Step 6: Commit**

```bash
git add scenarios
git commit -m "data: encode base and mandatory stress scenarios"
```

---

### Task 4: Define portable schemas without defining a competition strategy

**Files:**
- Create: `schemas/demand.schema.json`
- Create: `schemas/supply_sources.schema.json`
- Create: `schemas/plan.schema.json`
- Create: `schemas/scenario.schema.json`
- Create: `schemas/export.schema.json`
- Create: `examples/empty_plan.json`
- Create: `examples/invalid_plan_examples/negative_reservation.json`
- Create: `examples/invalid_plan_examples/over_capacity.json`
- Create: `examples/invalid_plan_examples/malformed_scenario.json`
- Create: `examples/example_export_structure.csv`

**Interfaces:**
- Consumes: data/scenario field names from Tasks 2-3.
- Produces: language-neutral interchange contracts for participant systems.

- [ ] **Step 1: Create `schemas/demand.schema.json`**

The schema must use JSON Schema Draft 2020-12 and represent one logical demand row as:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/SpaceEconomyPolicy/test_oil/schemas/demand.schema.json",
  "title": "DemandRow",
  "type": "object",
  "required": ["year", "base_total_t", "base_critical_t", "low_total_t", "high_total_t", "status"],
  "properties": {
    "year": {"type": "integer", "minimum": 2035},
    "base_total_t": {"type": "number", "minimum": 0},
    "base_critical_t": {"type": "number", "minimum": 0},
    "low_total_t": {"type": "number", "minimum": 0},
    "high_total_t": {"type": "number", "minimum": 0},
    "status": {"const": "CASE_INPUT"}
  },
  "additionalProperties": false
}
```

Document in `DATA_DICTIONARY.md`, not the JSON Schema itself, that `base_critical_t <= base_total_t` is a cross-field semantic rule.

- [ ] **Step 2: Create `schemas/supply_sources.schema.json`**

Require the field names from `data/supply_sources.csv`. Use non-negative numbers for capacity/cost/reservation and `[0,1]` for `take_or_pay_share`. Keep `reliability_profile` as a non-empty string because organizer inputs include both constant and time-dependent profiles.

- [ ] **Step 3: Create `schemas/plan.schema.json`**

The plan schema must contain decisions but no recommended values. Use this shape:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/SpaceEconomyPolicy/test_oil/schemas/plan.schema.json",
  "title": "ParticipantPlan",
  "type": "object",
  "required": ["plan_id", "scenario_id", "decisions"],
  "properties": {
    "plan_id": {"type": "string", "minLength": 1},
    "scenario_id": {"type": "string", "minLength": 1},
    "decisions": {
      "type": "object",
      "required": ["supply_orders", "capacity_reservations", "investments", "inventory_policy"],
      "properties": {
        "supply_orders": {"type": "array", "items": {"type": "object"}},
        "capacity_reservations": {"type": "array", "items": {"type": "object"}},
        "investments": {"type": "array", "items": {"type": "object"}},
        "inventory_policy": {"type": "object"}
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": true
}
```

Keep the decision item schemas intentionally generic in the organizer reference repository; participant implementations may extend them. Do not add filled competition decisions.

- [ ] **Step 4: Create `schemas/scenario.schema.json`**

Require `scenario_id`, `status`, and optional mappings for demand, prices, delivery shares and loss ceiling. Allow `status` values `CASE_INPUT` or `TEAM_ASSUMPTION`.

- [ ] **Step 5: Create `schemas/export.schema.json`**

Require the export envelope fields:

```text
scenario_id
plan_id
units
assumptions_reference
yearly_balance
source_schedule
inventory_trace
financial_breakdown
constraint_checks
risk_register
```

Use arrays for the result blocks and strings/objects for identifiers and units.

- [ ] **Step 6: Create `examples/empty_plan.json`**

Use:

```json
{
  "plan_id": "example-empty-plan",
  "scenario_id": "BASE",
  "decisions": {
    "supply_orders": [],
    "capacity_reservations": [],
    "investments": [],
    "inventory_policy": {}
  }
}
```

- [ ] **Step 7: Create invalid examples**

`negative_reservation.json` must contain a synthetic `Source-X` with a negative reserved amount and a comment-free JSON structure that is syntactically valid but semantically invalid.

`over_capacity.json` must contain synthetic values such as `capacity=10`, `reserved=12`; do not use Earth-Core/Earth-Flex real competition numbers.

`malformed_scenario.json` must omit `scenario_id` so schema validation fails for a clear reason.

- [ ] **Step 8: Create `examples/example_export_structure.csv`**

Use only synthetic values and columns:

```csv
scenario_id,plan_id,year,metric,value,unit
SYNTHETIC,example,2035,total_demand,10,t
SYNTHETIC,example,2035,served_demand,9,t
SYNTHETIC,example,2035,shortage,1,t
```

- [ ] **Step 9: Validate all JSON files and schemas parse**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
paths = list(Path('schemas').glob('*.json')) + list(Path('examples').rglob('*.json'))
for p in paths:
    json.loads(p.read_text(encoding='utf-8'))
print(f'{len(paths)} JSON files parse')
PY
```

Expected: all JSON files parse without syntax errors.

- [ ] **Step 10: Validate `empty_plan.json` against `plan.schema.json`**

Run:

```bash
python -m pip install --quiet jsonschema
python - <<'PY'
import json
from jsonschema import validate
schema = json.load(open('schemas/plan.schema.json', encoding='utf-8'))
obj = json.load(open('examples/empty_plan.json', encoding='utf-8'))
validate(obj, schema)
print('empty plan schema OK')
PY
```

Expected output:

```text
empty plan schema OK
```

- [ ] **Step 11: Commit**

```bash
git add schemas examples
git commit -m "docs: add portable data and plan schemas"
```

---

### Task 5: Create synthetic control vectors and expected checks

**Files:**
- Create: `validation/README.md`
- Create: `validation/control_cases.md`
- Create: `validation/expected_checks.json`

**Interfaces:**
- Consumes: canonical rules in the approved design.
- Produces: arithmetic and semantic test vectors that validate implementations without solving the real competition case.

- [ ] **Step 1: Create `validation/control_cases.md` with explicit synthetic cases**

Include these cases with equations and expected outcomes.

#### Case V01: Material balance

```text
opening_inventory = 10 t
delivered = 30 t
losses = 2 t
served = 25 t
expected_closing_inventory = 13 t
```

Check: `10 + 30 - 2 - 25 = 13`.

#### Case V02: Shortage is not negative inventory

```text
opening_inventory = 0 t
delivered = 8 t
losses = 0 t
demand = 10 t
expected_served = 8 t
expected_shortage = 2 t
expected_closing_inventory = 0 t
```

#### Case V03: Take-or-pay minimum

```text
reserved_capacity_period = 100 t
order = 50 t
take_or_pay_share = 0.70
price = 2 mln units/t
expected_payable_volume = 70 t
expected_variable_payment = 140 mln units
```

#### Case V04: No double take-or-pay

Use the same V03 input and explicitly state that the correct payment remains 140; adding another `70 * 2` is wrong.

#### Case V05: Reservation proration

```text
annual_reserved_capacity = 100 t/year
reservation_rate = 0.4 mln units per t/year capacity
period_fraction = 0.5
expected_reservation_payment = 20 mln units
```

Calculation: `100 * 0.4 * 0.5 = 20`.

#### Case V06: Losses based on throughput once

```text
gross_inflow = 20 t
loss_rate = 0.05
expected_losses = 1 t
```

State that applying another 5% loss to closing stock for the same modeled mechanism is a failure.

#### Case V07: 45-day reserve

```text
annual_total_demand = 365 t
expected_45_day_reserve = 45 t
```

#### Case V08: Capacity violation

Use synthetic source capacity 10 and reservation 12; expected violation `CAPACITY_EXCEEDED`, excess 2.

#### Case V09: Critical demand nesting

```text
total_demand = 100
critical_demand = 60
```

Expected modeled total remains 100, not 160.

#### Case V10: Mandatory stress non-double-counting pattern

Use synthetic planned ISRU-like delivery 20 t and a stress actual-delivery share 0.50. Expected actual = 10 t. If a separate reliability 0.80 exists in the risk metadata, mandatory stress actual remains 10 t unless the test is explicitly a separate combined research scenario. This test is synthetic and illustrates the no-double-counting rule without using competition stress shares.

- [ ] **Step 2: Create `validation/expected_checks.json`**

Use an array with IDs V01-V10 and explicit expected values. Example:

```json
[
  {"case_id":"V01","expected":{"closing_inventory_t":13}},
  {"case_id":"V02","expected":{"served_t":8,"shortage_t":2,"closing_inventory_t":0}},
  {"case_id":"V03","expected":{"payable_volume_t":70,"variable_payment_mln":140}},
  {"case_id":"V04","expected":{"variable_payment_mln":140}},
  {"case_id":"V05","expected":{"reservation_payment_mln":20}},
  {"case_id":"V06","expected":{"losses_t":1}},
  {"case_id":"V07","expected":{"reserve_t":45}},
  {"case_id":"V08","expected":{"violation":"CAPACITY_EXCEEDED","excess_t":2}},
  {"case_id":"V09","expected":{"total_demand_t":100}},
  {"case_id":"V10","expected":{"actual_delivery_t":10}}
]
```

- [ ] **Step 3: Create `validation/README.md`**

State clearly:

- these are arithmetic/unit-test vectors, not a case solution;
- all source names and most values are synthetic;
- teams should reproduce expected outputs in their own technology stack;
- passing these tests does not prove the team has chosen a good strategy;
- teams must add their own boundary tests and mandatory-stress integration tests.

- [ ] **Step 4: Validate `expected_checks.json` parses and contains all case IDs**

Run:

```bash
python - <<'PY'
import json
obj = json.load(open('validation/expected_checks.json', encoding='utf-8'))
ids = {x['case_id'] for x in obj}
assert ids == {f'V{i:02d}' for i in range(1, 11)}
print('validation vectors OK')
PY
```

Expected output:

```text
validation vectors OK
```

- [ ] **Step 5: Commit**

```bash
git add validation
git commit -m "test: add synthetic control vectors"
```

---

### Task 6: Write canonical rules and data dictionary

**Files:**
- Create: `docs/CASE_RULES.md`
- Create: `docs/DATA_DICTIONARY.md`
- Create: `docs/CALCULATION_RULES.md`
- Create: `docs/STRESS_PROTOCOL.md`

**Interfaces:**
- Consumes: Tasks 1-5.
- Produces: authoritative participant-facing semantics referenced by the main README.

- [ ] **Step 1: Write `docs/CASE_RULES.md`**

Required sections:

```text
1. Что фиксирует организатор
2. Что выбирает команда
3. Что считается TEAM_ASSUMPTION
4. Что нельзя менять скрытно
5. Граница агрегированной модели
6. BASE, mandatory stress и research scenarios
7. Что не требуется проектировать
8. Что считается неисполнимым планом
```

Explicitly state that an infeasible plan must be shown as infeasible with reason/year/value and must not be repaired by silently changing capacities, budgets, deadlines or source data.

- [ ] **Step 2: Write `docs/DATA_DICTIONARY.md` as a field-by-field table**

For every field in `data/*.csv`, include:

```text
field | meaning | type | unit | status | allowed range | used in | common mistake
```

Mandatory semantic warnings:

```text
base_critical_t is included in base_total_t
reserved capacity is not inventory
ordered volume is not delivered volume
delivered volume is not served demand
reliability is not BASE delivery share
loss_rate_on_throughput is applied to gross inflow in the control model
```

- [ ] **Step 3: Write `docs/CALCULATION_RULES.md` with explicit formulas**

Include the following formulas and definitions exactly in meaning:

```text
I_end = I_start + Q_delivered - Losses - Q_served
Shortage = max(0, Demand - Q_served)
Losses = Throughput * loss_rate
R_y = D_y * 45 / 365
Q_pay = max(Q_order, take_or_pay_share * Q_reserved_period)
VariablePayment = price * Q_pay
ReservationPayment = reservation_rate * annual_capacity_value * period_fraction
SL_total = served_total / demand_total
SL_critical = served_critical / demand_critical
TotalCost = Procurement + Reservation + Holding + FixedOPEX + CAPEX
PV_t = CF_t / (1 + r)^(t - t0)   [only when a team uses discounting]
```

For each formula provide:

- unit check;
- when it applies;
- what it must not be confused with;
- one synthetic example if helpful;
- boundary condition.

- [ ] **Step 4: Add timing rules to `CALCULATION_RULES.md`**

State that the team may choose the internal time step, but it must detect within-year shortages and storage overflow and respect lead times. Use 365 days for the organizer control conversion of annual demand to days. State that annual take-or-pay is not duplicated into separate monthly minimum obligations unless the participant explicitly defines a separate research contract outside the control rules.

- [ ] **Step 5: Write `docs/STRESS_PROTOCOL.md`**

Required sections:

```text
BASE
MANDATORY_STRESS
Sensitivity analysis
Team-defined risk scenarios
Reverse stress / robust analysis / Monte Carlo as optional methods
Scenario isolation and reproducibility
```

Include the exact mandatory stress constants from Task 3 and a boxed warning against multiplying 55%/75% by reliability again.

- [ ] **Step 6: Cross-check terminology against data files**

Run a targeted manual consistency pass. The docs must use the exact identifiers `Earth-Core`, `Earth-Flex`, `Earth-New`, `Lunar-ISRU`, `Emergency`, `BASE`, and `MANDATORY_STRESS` where machine-readable identifiers are discussed.

- [ ] **Step 7: Commit**

```bash
git add docs/CASE_RULES.md docs/DATA_DICTIONARY.md docs/CALCULATION_RULES.md docs/STRESS_PROTOCOL.md
git commit -m "docs: define canonical case and calculation rules"
```

---

### Task 7: Write jury guidance, scientific basis, sources, and FAQ

**Files:**
- Create: `docs/JURY_CHECKLIST.md`
- Create: `docs/SCIENTIFIC_BASIS.md`
- Create: `docs/SOURCES.md`
- Create: `docs/FAQ.md`

**Interfaces:**
- Consumes: official criteria, jury explanatory note, organizer case, supplied scientific PDFs, and verified public primary sources.
- Produces: evaluation map and source-to-method traceability.

- [ ] **Step 1: Write `docs/JURY_CHECKLIST.md` as an action-based verification route**

Use these ordered checks:

```text
1. Start the participant system from its instructions.
2. Open BASE.
3. Pick one year and one source.
4. Trace input -> formula/algorithm -> result -> constraint.
5. Change an allowed decision without editing code.
6. Recalculate and confirm dependent outputs change.
7. Construct a knowingly infeasible plan.
8. Confirm the tool reports the violated condition, year and actual value.
9. Run MANDATORY_STRESS.
10. Compare cost, service, stock and shortage with BASE.
11. Export results.
12. Re-open a saved plan.
13. On a copy of the dataset, add a source or future period.
```

Add the scoring map:

```text
25 model correctness
20 architecture/strategy rationale
20 stress testing
15 risk register
10 stakeholders/adaptation
10 digital contour
+5 optional geopolitical block
```

- [ ] **Step 2: Write `docs/SCIENTIFIC_BASIS.md` using the four-column evidence model**

For each source use:

```text
Source
What it supports
How it is used in this case framework
What it does not support
```

At minimum cover:

1. NASA-STD-7009B — credibility, verification, validation, uncertainty and sensitivity practices.
2. Ho (2024), DOI `10.2514/1.A35982` — space logistics, inventory, infrastructure and uncertainty.
3. Simonini et al. (2024), DOI `10.1038/s41526-024-00377-5` — cryogenic propellant management challenges.
4. Sommariva et al. (2023), DOI `10.1016/j.actaastro.2023.01.004` — technical/economic analysis of Earth-vs-lunar propellant supply to an orbital depot under uncertainty.
5. Bertsimas & Sim (2004), DOI `10.1287/opre.1030.0065` — robust optimization/price of robustness as an optional method.
6. Linkov et al. (2006), DOI `10.1016/j.envint.2006.06.013` — MCDA and adaptive management framing.
7. Kenny et al. (2025), `Guidelines for In-Space Cryogenic Propellant Transfer` — engineering guidance for cryogenic transfer; distinguish the NTRS/CFM guideline context and the ASCEND publication rather than collapsing them into one bibliographic object.

- [ ] **Step 3: Write `docs/SOURCES.md` in two separate groups**

Group A: organizer materials.

```text
Кейс_2_Топливный_космоконтур_2035.docx
Критерии_оценки_Кейс_2_КЭП_upd.xlsx.docx
Пояснительная_записка_для_жюри_Кейс_2_КЭП.docx
52 признака AI-текста на русском_ полный список.pdf
humanizer-ru repository (editorial guidance only)
```

Group B: independent scientific/official sources.

For each scientific source include authors, title, year, journal/organization, DOI if available, and a primary or official link where possible.

Do not cite a secondary blog when the DOI publisher/NASA/NTRS source is available.

- [ ] **Step 4: Write `docs/FAQ.md` from foreseeable implementation confusion**

Include at least these questions with direct answers:

```text
Нужно ли использовать Python? -> Нет.
Нужен ли автоматический оптимизатор? -> Нет.
Можно ли сделать чат-бот? -> Да, если он запускает реальный расчёт, а не генерирует числа вместо модели.
Можно ли использовать Excel? -> Да для данных/проверки/экспорта, но не как единственный цифровой контур.
Нужно ли умножать BASE supply на reliability? -> Нет.
Нужно ли ещё раз умножать 55%/75% ISRU на reliability? -> Нет.
Критический спрос нужно прибавлять к общему? -> Нет.
Можно ли выбрать свой discount rate? -> Да как TEAM_ASSUMPTION, если организатор не задаёт его; раскрыть и не менять между сравниваемыми альтернативами.
Можно ли прогнозировать 2041+? -> Да только как отдельный research scenario с явными новыми входами.
Можно ли использовать реальные цены конкретных ракет? -> Только в отдельном исследовании; не подменять ими контрольные synthetic case inputs.
Должна ли стратегия обязательно включать Lunar-ISRU? -> Нет.
```

- [ ] **Step 5: Verify no scientific source is used to justify organizer synthetic values**

Search manually for phrases equivalent to "по данным NASA мощность Earth-Core 190" or "реальная ZBO имеет потери 1.2%" and remove them if present.

- [ ] **Step 6: Commit**

```bash
git add docs/JURY_CHECKLIST.md docs/SCIENTIFIC_BASIS.md docs/SOURCES.md docs/FAQ.md
git commit -m "docs: add jury, science, sources and FAQ guidance"
```

---

### Task 8: Write the complete participant-facing `README.md`

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: every artifact from Tasks 1-7.
- Produces: the primary entry point participants and jury can use without reading source DOCX files first.

- [ ] **Step 1: Write the opening section with the repository boundary**

The opening must say, in natural Russian, all of the following within the first screen:

```text
Case title and 2035-2040 horizon.
The participant builds a working digital planning tool for a conditional orbital propellant node.
The repository contains organizer data, control rules, formats and verification guidance.
The repository does not contain a ready competition strategy.
Teams choose their own source mix, procurement, investments, analysis method, stack and interface.
```

Do not start with generic phrases such as "В современном мире" or a history of space exploration.

- [ ] **Step 2: Add a clickable table of contents covering the approved README map**

At minimum include links to:

```text
Что нужно сделать
Что сдаёт команда
Что считается цифровым контуром
CASE_INPUT / TEAM_DECISION / TEAM_ASSUMPTION
Данные
Материальный баланс
Хранилище и потери
45-дневный резерв
Контракты
Инвестиции
Финансы
BASE / mandatory stress
Риски
Стейкхолдеры
Программная архитектура
Тесты
Проверка жюри
Критерии
Типовые ошибки
Научная база
```

- [ ] **Step 3: Add Mermaid diagram 1 — end-to-end case workflow**

Use:

```mermaid
flowchart LR
    A[Исходные данные] --> B[Решения команды]
    B --> C[Расчётное ядро]
    C --> D[BASE]
    D --> E[MANDATORY_STRESS]
    E --> F[Чувствительность и риски]
    F --> G[Сравнение альтернатив]
    G --> H[Записка, интерфейс, экспорт, защита]
```

- [ ] **Step 4: Add the deliverables section**

List the management note, one-page scenario comparison, working digital contour, source code/data/config, presentation, reproducible tests, calculated risk register and exports. Explain what the jury must be able to reproduce.

- [ ] **Step 5: Add the parameter-status section**

Explain `CASE_INPUT`, `TEAM_DECISION`, `TEAM_ASSUMPTION` with concrete non-prescriptive examples.

- [ ] **Step 6: Add the model-boundary section**

State that the organizer control model is aggregate supply/logistics, not a required tank thermodynamics or trajectory model. Explain that participants may add higher-fidelity research modules, but they must not replace or silently alter the control inputs.

- [ ] **Step 7: Add the demand and source tables from `data/`**

Show all organizer inputs in readable Markdown tables, including units and notes for time-varying reliability. Link each table to the corresponding CSV and provenance document.

- [ ] **Step 8: Add Mermaid diagram 2 — supply chain**

Use a diagram with all five sources feeding the orbital node, then storage, then critical/commercial demand. Show Emergency as a reserve/emergency path rather than visually implying it is always a normal base supplier.

- [ ] **Step 9: Add Mermaid diagram 3 — reserved vs ordered vs delivered vs served**

Use:

```mermaid
flowchart LR
    R[Reserved capacity] --> O[Ordered volume]
    O --> D[Delivered volume]
    D --> A[Available fuel]
    A --> S[Served demand]
```

Immediately below write:

```text
reserved != ordered != delivered != served
capacity != inventory
contractual emergency reserve != physical stock
```

- [ ] **Step 10: Add the material balance section with formula and shortage logic**

Use the exact control formula and state that negative inventory is not a physical state. Link to `docs/CALCULATION_RULES.md` and V01/V02 synthetic validation cases.

- [ ] **Step 11: Add Mermaid diagram 4 — material balance**

Use opening stock and delivered inflow into a storage node; show losses and served demand as outflows; show closing stock and shortage separately.

- [ ] **Step 12: Add the storage/loss section**

Explain throughput, one-time loss application, holding cost basis, base storage and ZBO organizer parameters. Include a prominent sentence that 1.2% is a case-model coefficient rather than a universal physical ZBO claim.

- [ ] **Step 13: Add the 45-day reserve section**

Show `R = annual total demand * 45 / 365`. Explain physical versus contracted emergency reserve and why annual Emergency capacity alone does not prove timely reserve availability.

- [ ] **Step 14: Add contracts and take-or-pay**

Show the payable-volume formula, variable payment, reservation payment, and the no-double-counting rule. Link to V03-V05.

- [ ] **Step 15: Add Mermaid diagram 5 — investment timing**

Use:

```mermaid
flowchart LR
    A[Decision] --> B[Payment / CAPEX]
    B --> C[Lead time]
    C --> D[Commissioning]
    D --> E[Available capacity / storage effect]
    E --> F[Operating OPEX]
```

- [ ] **Step 16: Add investment rules without recommendations**

Explain Earth-New `90+270=360`, ZBO parameters and Lunar-ISRU pilot parameters. Explicitly say the repository does not recommend whether or when to invest.

- [ ] **Step 17: Add financial metrics**

Explain cost components and optional discounting. Do not invent mission-failure penalties or revenues because the control inputs do not provide them.

- [ ] **Step 18: Add service-level section**

Show total and critical service formulas, BASE 97%/99% thresholds, and the rule that critical demand is nested in total demand.

- [ ] **Step 19: Add reliability section**

Put the wrong and right concepts side by side in prose:

```text
Wrong for BASE: delivered = planned * reliability.
Control rule: timely available planned volumes arrive as planned; reliability is analyzed separately as risk.
```

Also state that mandatory stress ISRU actual shares are not multiplied by reliability again.

- [ ] **Step 20: Add Mermaid diagram 6 — BASE vs mandatory stress**

Show which inputs change in stress: demand, Earth-Core/Earth-Flex variable prices, Lunar-ISRU actual delivery share, stress loss ceiling. Show reservation tariffs, CAPEX and unrelated prices as unchanged by that mandatory shock.

- [ ] **Step 21: Add the exact mandatory stress table**

Use:

| Parameter | 2035-2037 | 2038 | 2039 | 2040 |
|---|---:|---:|---:|---:|
| Base total demand | 100% | 115% | 115% | 115% |
| Base critical demand | 100% | 115% | 115% | 115% |
| Earth-Core variable price | 100% | 125% | 125% | 100% |
| Earth-Flex variable price | 100% | 125% | 125% | 100% |
| Lunar-ISRU actual delivery | plan | 55% plan | 75% plan | plan |
| Stress loss ceiling | n/a | <=2% | <=2% | <=2% |

- [ ] **Step 22: Add the stress-methodology section**

Differentiate mandatory stress, sensitivity, team-defined risks, reverse stress, robust analysis and Monte Carlo. State that sophistication is not a substitute for grounded inputs or reproducibility.

- [ ] **Step 23: Add risk and stakeholder sections**

Show the recommended risk-register fields and stakeholder groups. Do not give ready MCDA weights.

- [ ] **Step 24: Add the software architecture contract**

Include this recommended decomposition as a language-neutral example:

```text
load_case()
validate_case()
load_plan()
validate_plan()
apply_scenario()
calculate_deliveries()
calculate_inventory()
calculate_service()
calculate_costs()
check_constraints()
evaluate_risks()
compare_scenarios()
save_plan()
load_saved_plan()
export_results()
```

State explicitly that names are illustrative and teams may structure code differently if the required behavior remains testable.

- [ ] **Step 25: Add examples of useful error messages**

Use a synthetic example such as:

```text
CAPACITY_EXCEEDED
source=Source-X
year=2038
reserved=12
maximum=10
```

Do not use a real source/value combination that hints at a competition plan.

- [ ] **Step 26: Add extension tests**

Tell teams to add synthetic `Source-X` on a copy of the dataset and to add a research 2041 period with explicit `TEAM_ASSUMPTION` inputs. State that 2041 is not an organizer forecast.

- [ ] **Step 27: Add Mermaid diagram 7 — jury route**

Use:

```mermaid
flowchart LR
    A[Запуск] --> B[BASE]
    B --> C[Изменить решение]
    C --> D[Пересчитать]
    D --> E[Проверить нарушение]
    E --> F[MANDATORY_STRESS]
    F --> G[Сравнить]
    G --> H[Экспорт]
    H --> I[Повторно открыть план]
    I --> J[Расширить копию данных]
```

- [ ] **Step 28: Add the 100+5 scoring map**

Use the exact six primary criterion weights and +5 optional geopolitical block. Explain which repository artifact helps a team demonstrate each criterion, without saying how to "game" the score.

- [ ] **Step 29: Add the "Типовые ошибки" section**

At minimum include:

```text
adding critical demand to total demand again
multiplying BASE supply by reliability
multiplying mandatory stress ISRU share by reliability again
using negative inventory to represent shortage
counting the same losses twice
charging take-or-pay twice
adding another 360 on top of Earth-New 90+270
assuming Emergency annual capacity proves timely emergency reserve
silently changing source capacity, budget or lead time
calling a static screenshot a digital contour
presenting team assumptions as organizer facts
using real-company prices as replacements for organizer control values
inventing exact probabilities without data
```

- [ ] **Step 30: Add the science and source section**

Summarize the evidence map and link to `docs/SCIENTIFIC_BASIS.md`, `docs/SOURCES.md`, and `docs/ERRATA_AND_PROVENANCE.md`.

- [ ] **Step 31: Add a final pre-defense checklist**

Use checkbox items for:

```text
all numbers in note/dashboard/export agree
BASE reproducible
MANDATORY_STRESS reproducible
one invalid plan reports exact violation
one manual arithmetic control case matches
save/reopen works
export works
source/future-period extension tested on a copy
assumptions separated from organizer inputs
scientific claims have traceable sources
no secrets/API keys committed
```

- [ ] **Step 32: Run a human-readable style pass**

Search and revise unnecessary stock phrases, repetitive headings, excessive nominalizations and generic conclusions. Do not introduce spelling or factual errors. Keep formulas, legal/contract terms and scientific terminology exact even if that makes some passages formal.

- [ ] **Step 33: Commit**

```bash
git add README.md
git commit -m "docs: add complete participant guide"
```

---

### Task 9: Final repository integrity and anti-solution audit

**Files:**
- Modify as needed: `README.md`, `data/*`, `scenarios/*`, `schemas/*`, `examples/*`, `validation/*`, `docs/*`

**Interfaces:**
- Consumes: the complete starter repository.
- Produces: a release-ready reference repository whose files agree with one another and do not solve the case for participants.

- [ ] **Step 1: Validate all CSV and JSON files parse**

Run:

```bash
python - <<'PY'
import csv, json
from pathlib import Path
for p in Path('data').glob('*.csv'):
    with p.open(encoding='utf-8') as f:
        list(csv.DictReader(f))
for p in list(Path('schemas').glob('*.json')) + list(Path('examples').rglob('*.json')) + list(Path('validation').glob('*.json')):
    json.loads(p.read_text(encoding='utf-8'))
print('CSV/JSON syntax OK')
PY
```

Expected output:

```text
CSV/JSON syntax OK
```

- [ ] **Step 2: Validate YAML syntax**

Run:

```bash
python - <<'PY'
import yaml
from pathlib import Path
for p in Path('scenarios').glob('*.yaml'):
    yaml.safe_load(p.read_text(encoding='utf-8'))
print('YAML syntax OK')
PY
```

Expected output:

```text
YAML syntax OK
```

- [ ] **Step 3: Validate the approved stress constants in both YAML and README**

Run a small script that checks the YAML values programmatically, then manually compare the README stress table against them. Any mismatch blocks completion.

Programmatic part:

```bash
python - <<'PY'
import yaml
s = yaml.safe_load(open('scenarios/mandatory_stress.yaml', encoding='utf-8'))
expected = {
    'demand_2038': 1.15,
    'core_2038': 1.25,
    'flex_2039': 1.25,
    'isru_2038': 0.55,
    'isru_2039': 0.75,
    'loss': 0.02,
}
actual = {
    'demand_2038': s['demand_multiplier'][2038],
    'core_2038': s['variable_price_multiplier']['Earth-Core'][2038],
    'flex_2039': s['variable_price_multiplier']['Earth-Flex'][2039],
    'isru_2038': s['actual_delivery_share']['Lunar-ISRU'][2038],
    'isru_2039': s['actual_delivery_share']['Lunar-ISRU'][2039],
    'loss': s['loss_ceiling']['max_losses_divided_by_throughput'],
}
assert actual == expected, (actual, expected)
print('mandatory stress invariant OK')
PY
```

- [ ] **Step 4: Run the anti-solution content audit**

Search repository text for prescriptive phrases that would imply a ready competition strategy. Review every hit for terms such as:

```text
оптимальный план
рекомендуем купить
нужно выбрать Lunar-ISRU
лучший поставщик
оптимальный объём Earth-Core
инвестировать в 2036
победная стратегия
```

Do not blindly delete legitimate explanatory use of "optimal" in scientific-source titles or methodological discussion. Remove only organizer-authored prescriptions for the competition solution.

- [ ] **Step 5: Run the source-integrity audit**

Check every numerical `CASE_INPUT` shown in README against `data/*` and `ERRATA_AND_PROVENANCE.md`. If a number is not in the source ledger, either add a valid source or remove the unsupported number.

- [ ] **Step 6: Run the scoring-coverage audit**

For each official criterion confirm the README points to at least one concrete participant artifact/action:

```text
25 model correctness -> formulas + control tests + reproducibility
20 architecture -> data flow + assumptions + alternative strategies
20 stress -> mandatory stress + sensitivity protocol
15 risks -> calculated risk register
10 stakeholders -> stakeholder metrics/contracts/adaptation
10 digital contour -> change/recalculate/save/export/extend
+5 geopolitical -> optional separate scenario block
```

- [ ] **Step 7: Run the scientific traceability audit**

Every scientific source described in `SCIENTIFIC_BASIS.md` must have a corresponding bibliographic entry in `SOURCES.md`. Every methodological claim in README that relies on literature should link to `SCIENTIFIC_BASIS.md` rather than floating without support.

- [ ] **Step 8: Check internal Markdown links**

Use a script that extracts relative Markdown paths and verifies the target file exists. At minimum manually verify all links to `data/`, `scenarios/`, `validation/`, and `docs/`.

- [ ] **Step 9: Check there are no secret-like files or credentials**

Ensure the repository does not contain `.env`, API keys, tokens, passwords, or private service credentials. The starter repository should require no paid subscription or secret merely to understand the case materials.

- [ ] **Step 10: Final editorial pass in Russian**

Read README from the perspective of a developer who has never seen the three organizer DOCX files. Every unavoidable term such as take-or-pay, capacity reservation, throughput, ISRU and ZBO must either be defined inline or linked to a definition. Remove ambiguous pronouns and hidden prerequisites.

- [ ] **Step 11: Final commit**

```bash
git add README.md data scenarios schemas examples validation docs
git commit -m "chore: finalize test_oil reference repository"
```

- [ ] **Step 12: Record release evidence**

Capture the final commit SHA and list the repository tree. Confirm the repository contains documentation/data/schemas/validation only and no ready competition application or optimizer.

---

## Implementation Order Summary

1. Provenance before data.
2. Data before scenarios and schemas.
3. Schemas before examples.
4. Canonical rules before the main README.
5. Science/jury documents before the README source map.
6. README after all linked artifacts exist.
7. Final anti-solution and integrity audits last.

This order prevents the README from becoming a second, inconsistent source of truth.

## Completion Definition

The implementation is complete only when a participant can open `README.md` and determine, without organizer-side oral clarification, what must be built and how it will be checked, while still having to make their own supply, investment, risk, optimization and interface decisions.
