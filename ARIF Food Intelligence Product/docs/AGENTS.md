# ARIF-Net / ARIF Food Intelligence — AGENTS.md

**Document Version:** 0.1.0  
**Document Type:** AI Agent Engineering Governance & Implementation Guide  
**Project:** ARIF-Net / ARIF Food Intelligence  
**Research Model:** ARIF-Net  
**Product:** ARIF Food Intelligence  
**Status:** Working implementation contract  

> This file is the operational instruction layer for AI coding agents working on the ARIF-Net repository and the ARIF Food Intelligence product layer.

---

## 0. PURPOSE

The agent must treat this file as an implementation-governance document, not as a replacement for the research contract or source code.

The project has two connected but distinct layers:

```text
ARIF-Net
= research / modeling / experimentation layer

ARIF Food Intelligence
= product / application / visualization layer
```

The product exists to expose validated research outputs and contextual information through a public-first web application.

The research objective must remain centered on:

```text
supervised multimodal regression forecasting
+
historical price dynamics as mandatory input/backbone
+
climate/supply
+
news/sentiment
+
macro/logistics
+
calendar as supporting information
+
multi-horizon forecasting up to 365 days
```

Extreme movement / shock analysis is secondary. It is not the primary classification task.

---

# 1. SOURCE-OF-TRUTH HIERARCHY

When information conflicts, use this order:

1. Researcher-approved decisions and explicit decision gates.
2. Executable source code for what is actually implemented.
3. Versioned dataset / experiment / model artifacts for empirical numbers.
4. Official project documentation and implementation plans.
5. README and presentation-oriented documentation.
6. External literature / web research for theory, standards, and technology updates.

Rules:

- Do not trust README as proof of implementation.
- Do not treat an implementation as an approved methodology decision merely because the code exists.
- If code and documentation disagree, report the conflict and follow the source-of-truth hierarchy.
- If two documents conflict, do not silently reconcile them. Identify the conflict, determine authority, and document the decision.
- If the source does not support a claim, do not invent the missing information.

Primary project knowledge-base documents currently include:

- `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.1.0_PHASE0_SYNC.md`
- `ARIF-Net_Phase_0_Research_Contract_v2.0.0.md`
- `ARIF-Net_Implementation_Report_v2_Research_Realignment.pdf`
- `ARIF-Net_Proposal_BAB_1.pptx`

The exact version/name available in the repository must be checked before claiming a document is current.

---

# 2. NON-NEGOTIABLE RESEARCH RULES

## 2.1 Preserve the core research goal

Never silently turn the project into:

- a classification-first system;
- a shock detection product;
- a generic price prediction project;
- a causal inference system;
- a trading system;
- a policy-decision system.

The primary research task remains multimodal regression forecasting.

## 2.2 Historical price is mandatory

Historical price dynamics must remain explicit model input/backbone.

Do not design a final model that removes historical price dynamics while still calling it the canonical ARIF-Net research design.

## 2.3 Multi-horizon is part of the research contract

Supported standard horizons are:

```text
1
3
7
14
30
90
180
365 days
```

Do not introduce arbitrary horizons unless the model/data contract explicitly supports them.

## 2.4 Relative movement is the canonical modeling target

The research contract uses relative price movement / percentage change as the internal modeling target, with nominal price reconstructed for product presentation.

Do not silently replace the research target with direct-price regression.

## 2.5 Temporal integrity is mandatory

For forecast origin `t`, only information available by the cutoff/origin may be used.

The agent must prevent use of future realized values such as:

- future realized price;
- future realized weather/climate;
- future news;
- future realized fuel prices;
- future realized supply/logistics;
- any feature whose source was published/available after the forecast cutoff.

Future-known deterministic calendar information may be used when the research contract allows it.

## 2.6 Split integrity is mandatory

The final evaluation protocol is chronological:

```text
TRAIN → VALIDATION → TEST
```

The test set must not be used for:

- checkpoint selection;
- early stopping;
- hyperparameter tuning;
- threshold tuning;
- feature selection;
- architecture selection;
- any decision that changes the model before final evaluation.

Model selection happens on validation. Final test evaluation is blind/controlled.

## 2.7 Split-aware transformations

Any transformation requiring fitting must be fit on training data or handled split-aware, including:

- imputation parameters;
- scaling;
- normalization;
- anomaly baselines;
- quantile thresholds;
- target transformations;
- feature-selection statistics.

Never calculate full-period statistics and then feed them back into training/evaluation without a valid split-aware contract.

## 2.8 Shock definition

Shock is a secondary phenomenon.

Primary shock threshold is horizon-scaled and derived from the training distribution, with Q95 as the primary recommendation in the research contract.

The legacy fixed 3% threshold is only a comparison / sensitivity reference.

Do not silently turn shock into the main target.

## 2.9 No causal overclaim

These are not automatically causal evidence:

```text
correlation
SHAP
attention
learned gate weights
feature importance
predictive contribution
```

Use language such as:

- predictive contribution;
- association;
- model contribution;
- predictive information.

Do not claim that climate, sentiment, fuel, logistics, or another modality caused a price movement unless a valid causal methodology explicitly exists and is documented.

## 2.10 No fabricated evidence

Never invent:

- MAE;
- RMSE;
- R²;
- accuracy;
- shock recall;
- confidence intervals;
- significance tests;
- SHAP percentages;
- attention plots;
- gate activation statistics;
- forecast values;
- benchmark rankings;
- dataset counts;
- dates;
- source coverage;
- user counts.

If a value does not exist in an actual artifact/run, mark it as unavailable or unverified.

## 2.11 No fabricated literature

Never invent a paper title, DOI, author list, journal, indexing status, or study finding.

## 2.12 No synthetic research evidence

Synthetic/random/hardcoded/demo values are allowed only as explicit UI fixtures or development mocks.

They must never be presented as:

- actual research results;
- actual forecasts;
- actual benchmark values;
- actual residuals;
- actual sentiment data;
- actual climate evidence.

## 2.13 Model-specific explainability

Do not call XGBoost SHAP an ARIF-Net explanation.

If explanation artifacts are needed, use the explanation mechanism actually supported by the model and run.

## 2.14 Terminology accuracy

If an implemented loss is a weighted MSE variant, call it a weighted MSE / Shock-Weighted MSE as appropriate.

Do not relabel a method as focal loss, attention, causal weighting, or another technique merely because the label sounds stronger.

## 2.15 Candidate architecture remains candidate

Reliability-aware fusion and horizon-conditioned fusion are research candidates/hypotheses until validated through the agreed experimental protocol.

Do not write UI copy or academic documentation that treats candidate mechanisms as final validated contributions prematurely.

## 2.16 Novelty remains evidence-gated

Do not use unsupported wording such as:

- novel;
- first;
- state-of-the-art;
- best;
- proven superior;
- globally unique.

Use `candidate contribution` / `potential contribution` until evidence and literature validation justify stronger wording.

---

# 3. PRODUCT RULES — ARIF FOOD INTELLIGENCE

## 3.1 Product purpose

The product should help users understand:

```text
current price
→ historical dynamics
→ forecast
→ multimodal context
→ explanation
→ evidence
```

It is not an input-form-to-single-number application.

## 3.2 Public-first

The default public product should not require authentication for ordinary exploration.

Authentication, operator tools, or internal research controls must not be added to the public experience without a concrete requirement.

## 3.3 Commodity is the central product object

The main user experience should revolve around a commodity and its associated market, prices, forecasts, context, and evidence.

Keep these concepts separate:

```text
Commodity
Market
Supplier Region
```

Do not collapse supplier regions into market identity.

## 3.4 Forecast is an intelligence result, not a raw model dump

The product should expose:

- forecast origin;
- supported horizon;
- reference/current price;
- relative movement;
- reconstructed price when available;
- model version;
- dataset version;
- preprocessing version;
- data cutoff;
- availability state;
- limitations.

## 3.5 Product must consume versioned research artifacts

Frontend code must not silently reimplement research preprocessing.

Research transformation and product transformation are separate concerns.

If a transformation changes model semantics, update the appropriate contract and version.

## 3.6 No unversioned forecast

The UI must never display a forecast as a trustworthy research result unless its model/data/version metadata is present.

## 3.7 Explicit missing-data handling

Do not convert missing data into `0` unless zero is a semantically valid observed value defined by the contract.

Use explicit states such as:

```text
AVAILABLE
PARTIAL
MISSING
INSUFFICIENT_COVERAGE
TEMPORALLY_INVALID
SCHEMA_INVALID
```

## 3.8 Proxy labeling

If a value is a proxy, call it a proxy.

Example:

```text
distance × fuel_price
```

is a logistics cost proxy, not automatically actual logistics cost.

## 3.9 No causal UI wording

Do not build copy such as:

> Rainfall caused the price increase.

Prefer:

> Climate-related information used by the forecasting pipeline.

or, when validated:

> Climate-related features showed predictive contribution under the evaluated protocol.

## 3.10 Product limitations must remain visible

Do not hide data limitations, model limitations, missing modalities, or research status merely to make the product look stronger.

---

# 4. CURRENT STATE vs TARGET STATE

Always distinguish:

```text
CURRENT / OBSERVED
TARGET / PROPOSED
```

Examples:

- Existing repository architecture = observed state.
- Desired ARIF Food Intelligence architecture = target state.
- A candidate fusion mechanism = proposed state until experimentally validated.
- A published benchmark artifact = validated only if an actual run supports it.

Do not rewrite project history.

Known implementation problems should remain documented as historical/current issues until fixed and verified.

---

# 5. CHANGE CLASSIFICATION

Before modifying code, classify the change.

## Type A — Product/UI change

Examples:

- layout;
- styling;
- navigation;
- accessibility;
- chart interaction;
- loading/error states.

Can usually be implemented without changing research semantics.

## Type B — Product contract change

Examples:

- API response field;
- endpoint;
- data state;
- model metadata.

Requires contract review and compatibility analysis.

## Type C — Data/preprocessing change

Examples:

- feature definition;
- scaling;
- aggregation;
- temporal alignment;
- imputation;
- target creation.

Requires research impact analysis and versioning.

## Type D — Model/experiment change

Examples:

- encoder;
- fusion;
- loss;
- split;
- training protocol;
- metric;
- ablation.

Requires research-level review, experiment linkage, and validation.

---

# 6. REQUIRED WORKFLOW FOR CODE CHANGES

Before making a non-trivial change:

```text
1. Identify task
2. Read relevant source/documentation
3. Inspect actual repository code
4. Identify current behavior
5. Classify requested change
6. Check locked constraints
7. Identify affected contracts
8. Define acceptance criteria
9. Implement smallest coherent change
10. Run relevant tests/checks
11. Inspect resulting diff
12. Document important behavior changes
```

Do not begin by rewriting large portions of the repository unless the evidence shows that a larger refactor is necessary.

---

# 7. RESEARCH CODE CHANGE WORKFLOW

If changing data/model/experiment code:

```text
Current implementation
        ↓
Observed issue
        ↓
Impact on goal / RQ
        ↓
Candidate correction
        ↓
Required experiment / validation
        ↓
Implementation
        ↓
Tests / validation
        ↓
Artifact/version update
        ↓
Documentation update
```

Every research method must connect to an RQ or an explicit product requirement.

Do not add advanced techniques simply to increase apparent complexity.

---

# 8. PRODUCT CODE WORKFLOW

For product/frontend/backend changes:

```text
Requirement
   ↓
Relevant domain object
   ↓
API contract
   ↓
Type/schema
   ↓
Feature implementation
   ↓
UI state handling
   ↓
Tests
   ↓
Accessibility / responsive check
```

If an API field is missing from the contract, do not invent it silently.

Update the contract first or explicitly mark the field as a proposed extension.

---

# 9. FRONTEND ENGINEERING RULES

## 9.1 Separation of concerns

Preferred flow:

```text
Page
 ↓
Feature component
 ↓
Hook/query
 ↓
API client
 ↓
API
```

Avoid placing research calculations, data access, and page presentation in a single component.

## 9.2 Frontend must not train or run research experiments

Do not place:

- model training;
- feature engineering for experiments;
- data-fitting operations;
- evaluation logic;
- research metric generation

inside the web UI.

## 9.3 Frontend must not access secrets

Never expose database credentials, private API tokens, model credentials, or other secrets through client-side environment variables.

## 9.4 Use typed contracts

API data should be represented with TypeScript types/schema validation where appropriate.

Do not use `any` to bypass contract uncertainty without a documented reason.

## 9.5 Loading/error/empty states are required

Every data-driven page must consider at least:

```text
loading
success
empty
partial
error
```

## 9.6 Observed vs forecast must be visually distinguishable

Do not create charts where historical observed data and forecast data can be mistaken for the same signal.

## 9.7 Accessibility

Critical information must not depend solely on color.

Use labels, symbols, text, and semantic structure.

---

# 10. FRONTEND TARGET STRUCTURE

The following is the target organization for the product layer, not a claim about the current repository.

```text
product/web/
├── app/
├── components/
│   ├── ui/
│   ├── layout/
│   ├── data-display/
│   ├── charts/
│   ├── provenance/
│   └── states/
├── features/
│   ├── commodities/
│   ├── prices/
│   ├── forecasts/
│   ├── context/
│   ├── monitoring/
│   ├── education/
│   └── research/
├── lib/
│   ├── api/
│   ├── format/
│   ├── validation/
│   └── config/
├── hooks/
├── types/
├── mocks/
├── config/
├── styles/
└── public/
```

Do not force this structure onto the repository without first inspecting its current state.

---

# 11. API ENGINEERING RULES

## 11.1 API is the product boundary

Frontend should consume:

```text
/api/commodities
/api/markets
/api/prices
/api/forecasts
/api/context/*
/api/research/*
/api/metadata/*
```

Exact routes are contract proposals and must be checked against the current implementation before coding.

## 11.2 Standard response semantics

Preferred logical envelope:

```json
{
  "data": {},
  "meta": {},
  "provenance": {},
  "availability": {},
  "limitations": [],
  "error": null
}
```

Do not introduce this envelope into an existing production API blindly. Inspect the current API and preserve compatibility or perform a deliberate versioned migration.

## 11.3 Error responses should be structured

Prefer:

```json
{
  "error": {
    "code": "MODEL_VERSION_NOT_FOUND",
    "message": "Requested model version is unavailable.",
    "request_id": "req_xxx"
  }
}
```

Never leak stack traces or secrets to the client.

## 11.4 Version compatibility

A forecast request must be compatible with:

- model version;
- dataset version;
- preprocessing version;
- input schema;
- supported horizon;
- required modality contract.

## 11.5 Never use implicit “latest” research artifacts

Avoid unversioned production behavior such as:

```text
latest_model
latest_dataset
latest_preprocessor
```

unless the alias itself is explicitly version-controlled and auditable.

---

# 12. DATA ENGINEERING RULES

## 12.1 Provenance

Each meaningful research dataset must have source/provenance information.

## 12.2 Taxonomy

Do not leave commodity taxonomy ambiguous in final datasets.

At minimum, final data contracts should distinguish:

- commodity type;
- grade/type where relevant;
- unit;
- market definition.

## 12.3 Temporal fields

Where source behavior requires it, distinguish:

```text
observed_at
published_at
available_at
effective_at
```

Do not treat these timestamps as interchangeable.

## 12.4 Supplier-region handling

Supplier regions are external context, not automatically market identifiers.

Do not assign arbitrary contribution weights without evidence.

## 12.5 News features

If news/sentiment is implemented, preserve the actual model/pipeline provenance used in the run.

Do not claim a specific sentiment model was used if the actual run used a fallback or another method.

## 12.6 Fuel data

Fuel price is effective-date based. Do not backfill a future price into earlier dates.

## 12.7 Logistics distance

Static road distance is not historical travel time.

A derived `distance × fuel_price` feature must be documented as a proxy.

---

# 13. MODEL / INFERENCE RULES

## 13.1 Inference service must be model-aware

Inference must know which model version is being executed.

## 13.2 Input schema must be explicit

Each model artifact should have a compatible input/schema contract describing required feature groups and preprocessing expectations.

## 13.3 Output schema must be explicit

At minimum, a forecast result should identify:

```text
commodity
market
forecast_origin
horizon
reference_price
predicted_relative_movement
reconstructed_price (when available)
model_version
dataset_version
preprocessing_version
data_cutoff
availability
limitations
```

## 13.4 Do not silently alter preprocessing

If training uses one transformation and inference uses another, that is a correctness defect, not a harmless implementation detail.

## 13.5 No automatic causal/scenario semantics

Changing an input and rerunning the model is not automatically a causal counterfactual.

Do not expose an ordinary input perturbation UI as policy/intervention causality.

---

# 14. RESEARCH ARTIFACT RULES

Artifacts may include:

```text
dataset
model
forecast
benchmark
ablation
error_analysis
explainability
experiment
```

Every published artifact should be traceable to:

```text
source
version
experiment/run
```

When possible, maintain a clear lineage:

```text
Dataset
  ↓
Model
  ↓
Experiment
  ↓
Forecast / Benchmark / Ablation
```

---

# 15. MOCK DATA RULES

Mocks are allowed to unblock product development while research is being completed.

Requirements:

- clearly mark mock/demo/sample data;
- keep mock data out of research result paths;
- do not let mock data look like validated empirical output;
- use a repository/interface abstraction so real artifacts can replace mocks later.

Preferred architecture:

```text
UI
 ↓
Repository Interface
 ├── Mock Repository
 └── API Repository
```

---

# 16. TESTING RULES

## 16.1 Product tests

At minimum, cover where relevant:

- route rendering;
- component behavior;
- API contract handling;
- loading states;
- empty states;
- error states;
- partial-data states;
- responsive critical flows;
- accessibility-critical behavior.

## 16.2 API tests

Validate:

- request schema;
- invalid parameters;
- version compatibility;
- temporal constraints;
- missing modality behavior;
- error semantics.

## 16.3 Research tests

For research code, validate where relevant:

- chronological split;
- train-only fitting of transformations;
- test blindness;
- sequence boundary;
- target construction;
- temporal availability;
- reproducibility;
- artifact metadata.

## 16.4 Do not weaken tests to make code pass

If a new test exposes a research correctness issue, fix the issue or document the unresolved decision. Do not weaken the test merely to preserve the implementation.

---

# 17. GIT / CHANGE MANAGEMENT

Use small, coherent commits.

Recommended commit scopes:

```text
feat:
fix:
refactor:
test:
docs:
perf:
chore:
```

Examples:

```text
feat(product): add commodity intelligence page
fix(api): reject incompatible forecast schema
fix(research): enforce validation-only checkpoint selection
test(forecast): add temporal availability checks
docs(contract): update forecast response schema
```

Do not rewrite unrelated history or make broad formatting changes in a focused task unless necessary.

---

# 18. DEPENDENCY RULES

Before adding a dependency:

1. confirm the feature cannot reasonably be implemented with the current stack;
2. check project compatibility;
3. evaluate maintenance/security implications;
4. avoid overlapping libraries that solve the same problem;
5. document the reason for introducing the dependency.

Do not add advanced infrastructure just to make the architecture appear more sophisticated.

---

# 19. OVER-ENGINEERING GUARDRAIL

Do not add technologies or techniques such as:

- transformer variants;
- graph neural networks;
- reinforcement learning;
- causal modeling;
- multi-task learning;
- agent systems;
- microservices;
- event buses;
- complex real-time streaming

unless there is a concrete research question, product requirement, or validated engineering reason.

The project values reproducibility, correctness, and traceability over complexity.

---

# 20. DECISION GATE RULES

For an item marked `OPEN`, `PROPOSED`, or `CANDIDATE`:

- do not silently choose it as final;
- preserve alternatives where appropriate;
- identify trade-offs;
- state what evidence is required to close the gate;
- update the decision register when the project owner makes a decision.

If the requested task requires such a decision, stop short of pretending it is already locked.

---

# 21. METHODOLOGY IMPACT ANALYSIS

Any change to one of these requires impact analysis:

```text
target
horizon
feature definition
feature availability
preprocessing
train/validation/test split
loss
architecture
metric
shock definition
experiment protocol
```

Impact analysis must consider:

- research questions;
- benchmark comparability;
- ablation design;
- existing artifacts;
- report chapters;
- product API;
- UI semantics;
- reproducibility/versioning.

A change in one layer may require version updates in another.

---

# 22. DOCUMENTATION RULES

When code behavior changes materially, update the relevant documentation.

Maintain distinction between:

```text
FACT / OBSERVED
PROPOSED
OPEN
INFERENCE
EXTERNAL RESEARCH
DEPRECATED
```

Every official release should be traceable to relevant:

- repository commit/tag;
- dataset version;
- model version;
- experiment protocol version;
- known open decisions;
- known deprecated claims.

---

# 23. RESPONSE PROTOCOL FOR AI AGENTS

When asked for work on ARIF-Net, internally follow:

```text
IDENTIFY TASK
      ↓
LOAD AGENTS.md
      ↓
IDENTIFY RELEVANT SOURCE
      ↓
INSPECT ACTUAL CODE / ARTIFACT IF NEEDED
      ↓
CLASSIFY INFORMATION
      ↓
CHECK LOCKED GOAL
      ↓
CHECK TEMPORAL / RESEARCH VALIDITY
      ↓
CHECK PRODUCT CONTRACT
      ↓
MAKE CHANGE
      ↓
TEST / VALIDATE
      ↓
REVIEW DIFF
      ↓
DOCUMENT MATERIAL CHANGE
```

Do not answer from assumptions when repository evidence is required.

---

# 24. IF ASKED TO REVIEW CODE

Required flow:

```text
1. Locate actual implementation
2. Trace the relevant execution path
3. Identify the exact defect
4. Explain observed behavior
5. Explain why it matters
6. Define acceptance criteria
7. Patch/refactor
8. Run relevant tests
9. Inspect regression risk
10. Record the resulting behavior
```

Never claim that a code path works merely because it appears plausible from a filename or README.

---

# 25. IF ASKED TO BUILD A PRODUCT FEATURE

Required flow:

```text
Requirement
 ↓
Existing page / domain object
 ↓
Existing API contract
 ↓
Existing data source
 ↓
Required state cases
 ↓
Implementation
 ↓
Tests
```

Before creating a new domain concept, check whether an existing entity already represents it.

Do not duplicate `Commodity`, `Market`, `ForecastRun`, `ForecastPoint`, or provenance concepts under different names without a reason.

---

# 26. IF ASKED TO CHANGE THE MODEL

Do not immediately rewrite the model.

First report:

```text
Current architecture
↓
Observed problem
↓
Research impact
↓
Candidate alternatives
↓
Expected trade-offs
↓
Experiment required
↓
Decision gate
```

Then implement only after the requested decision is clear or the project owner has authorized the candidate direction.

---

# 27. IF ASKED TO WRITE ACADEMIC CONTENT

The agent must:

- follow the requested academic template;
- preserve research terminology;
- distinguish evidence from interpretation;
- never fabricate results;
- mark unavailable information as unverified/placeholder;
- use the documented project source hierarchy;
- avoid causal overclaim;
- avoid claiming novelty beyond the evidence state.

---

# 28. PRODUCT ROUTE CONTRACT — TARGET

The target public information architecture currently includes:

```text
/
/prices
/commodities
/commodities/[slug]
/commodities/[slug]/forecast
/forecast
/context
/context/climate
/context/news
/context/macro-logistics
/monitoring
/learn
/learn/food-price
/learn/forecasting
/learn/data
/research
/research/model
/research/methodology
/research/data
/research/experiments
/research/benchmark
/research/ablation
/research/limitations
```

These are target routes from the product planning work. Inspect the current repository before adding or renaming them.

---

# 29. CORE PRODUCT UX CONTRACT

Public user journey:

```text
Landing
 ↓
Choose Commodity
 ↓
Current Price
 ↓
Historical Trend
 ↓
Forecast
 ↓
Climate / News / Macro Context
 ↓
Model Explanation
 ↓
Evidence
 ↓
Limitations
```

The interface should progressively disclose technical depth rather than forcing research detail onto the first screen.

---

# 30. FORECAST UI CONTRACT

A forecast view should make these dimensions explicit:

```text
Commodity
Market
Forecast Origin
Horizon
Reference Price
Predicted Relative Movement
Reconstructed Price
Observed vs Forecast boundary
Model Version
Dataset Version
Preprocessing Version
Data Cutoff
Context Availability
Limitations
```

Do not display a forecast as an unqualified single number.

---

# 31. RESEARCH UI CONTRACT

Research pages should allow a visitor to understand:

```text
Problem
Goal
Data
Temporal Rules
Model
Experiment Protocol
Benchmark
Ablation
Limitations
```

Benchmark and ablation pages must only render actual experiment artifacts.

---

# 32. DEFINITION OF DONE — PRODUCT

A product change is complete only when, where relevant:

- the requested behavior is implemented;
- types/contracts are updated;
- loading/empty/error states exist;
- responsive behavior is checked;
- critical accessibility behavior is checked;
- no research semantics were silently changed;
- no secrets are exposed;
- tests/checks pass;
- material behavior changes are documented.

---

# 33. DEFINITION OF DONE — RESEARCH

A research change is complete only when, where relevant:

- the goal/RQ impact is understood;
- temporal integrity remains valid;
- test blindness is preserved;
- transformations remain split-aware;
- actual code matches the stated method;
- experiments use the correct protocol;
- artifacts are versioned;
- results are reproducible;
- documentation reflects the actual state.

---

# 34. RELEASE / PUBLISHING GATE

Before publishing a research-derived result to the public product, verify:

```text
[ ] Artifact exists
[ ] Artifact version exists
[ ] Dataset version exists
[ ] Model version exists
[ ] Preprocessing version exists
[ ] Forecast origin/cutoff is known
[ ] Temporal integrity is satisfied
[ ] Result is from an actual run
[ ] Result status is valid for publication
[ ] Limitations are represented
[ ] UI wording does not overclaim
```

If any critical item is missing, do not present the result as validated research evidence.

---

# 35. DO NOT DO THESE THINGS

Never:

1. invent research numbers;
2. invent papers or sources;
3. fabricate API behavior;
4. silently change the research target;
5. remove historical price dynamics from the canonical model design;
6. use future information in forecast inputs;
7. use the test set for selection/tuning;
8. call predictive explanation causal;
9. call baseline SHAP an ARIF-Net explanation;
10. present mock data as empirical evidence;
11. silently choose an OPEN decision;
12. expose secrets in frontend code;
13. hide limitations;
14. rename a proxy as an observed real-world measurement;
15. introduce unnecessary architecture complexity.

---

# 36. WORKING PROJECT POSITIONING

```text
Research Theme
Multimodal Food Price Forecasting and Intelligence

Research Task
Supervised Multimodal Regression Forecasting

Primary Inputs
Historical Price Dynamics
Climate / Supply
News / Sentiment
Macro / Logistics
Calendar Support

Secondary Capability
Extreme-Movement / Shock Monitoring

Research Model
ARIF-Net
(candidate until validated)

Product
ARIF Food Intelligence
(web productization layer)
```

---

# 37. IMMEDIATE PRODUCT IMPLEMENTATION ORDER

For product development in parallel with research:

```text
1. App Shell
2. Design Tokens
3. Foundation Components
4. Domain Types
5. API Contract Layer
6. Mock / Fixture Repository
7. Commodity Explorer
8. Price Explorer
9. Commodity Intelligence Page
10. Forecast UI
11. Context UI
12. Research UI
13. Education UI
14. Monitoring UI
15. Real API Integration
16. Versioned Research Artifact Integration
17. Product Testing
```

Build the product shell and contracts before treating the final model integration as complete.

---

# 38. RESEARCH IMPLEMENTATION PRIORITY

When research work is the task, follow the current canonical research roadmap as applicable:

```text
P1 Data / Temporal Audit
↓
P2 Explicit Price Dynamics
↓
P3 Train / Validation / Test Repair
↓
P4 Rebuild Baselines
↓
P5 ARIF-Net
↓
P6 Ablation
↓
P7 Explainability / Error Analysis
↓
P8 Research Evidence Freeze
↓
P9 Product Integration
```

The project implementation plan identifies these as the immediate implementation priorities and requires product inference to be built on a valid research foundation.

---

# 39. FINAL AGENT PRINCIPLE

> **Make the smallest technically correct change that preserves research validity, product integrity, reproducibility, and traceability.**

When uncertain:

```text
VERIFY > ASSUME

TRACE > GUESS

VERSION > IMPLICITLY MUTATE

TEST > CLAIM

EVIDENCE > APPEARANCE

USER DECISION > AGENT DECISION
```

---

# 40. SOURCE BASIS

This AGENTS.md is derived from the current project planning and research-contract materials supplied for ARIF-Net, especially:

- `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.1.0_PHASE0_SYNC.md`
- `ARIF-Net_Phase_0_Research_Contract_v2.0.0.md`
- `ARIF-Net_Implementation_Report_v2_Research_Realignment.pdf`
- `ARIF-Net_Proposal_BAB_1.pptx`

This file is an operational implementation layer. It does not override a later researcher-approved decision or a validated research artifact.

---

**End of AGENTS.md**
