# Product Requirements Document (PRD)

# SimCT — Clinical Study Simulation Platform

## 1. Product Overview

SimCT is a **clinical study simulation platform** that allows users to design clinical trials, simulate their execution, and generate artifacts and datasets derived from the simulated study.

SimCT expands beyond synthetic SDTM data generation by introducing a **two-layer model**:

* **Study Blueprint** — structured representation of planned study design
* **Canonical Study State** — simulated execution of that design

All outputs (datasets, documents, metadata) are **projections of the design or simulation state**.

This architecture enables a wide range of artifacts including:

* synthetic clinical datasets
* study design documents
* CRF structures
* operational rules
* validation scenarios

Synthetic SDTM generation becomes **one projection among many**, making SimCT a broader and more defensible platform.

---

# 2. Target Users

### Primary Users

**Clinical platform vendors and software builders**

Examples:

* EDC vendors
* data pipeline developers
* analytics platforms
* AI product developers in clinical research
* QA teams testing clinical systems

These users need **realistic simulated clinical trials** to test systems.

---

### Secondary Users

**Study designers / clinical operations teams**

Use cases:

* exploring study designs
* prototyping protocol structures
* evaluating operational scenarios

---

# 3. Product Vision

SimCT acts as a **digital twin generator for clinical trials**.

Users describe a trial design and SimCT simulates:

* how the trial operates
* how subjects progress
* how data is generated
* how operational events occur

From that simulation SimCT can generate:

* clinical datasets
* protocol skeletons
* CRF designs
* SAP skeletons
* operational metadata

---

# 4. Core Concepts

## 4.1 Study Blueprint

Structured representation of **planned study design**.

Defined using **YAML configuration**.

Blueprint describes:

* study design
* population
* arms
* visit schedule
* endpoints
* interventions
* operational parameters

Example:

```yaml
study:
  indication: oncology
  phase: II
  subjects: 120

arms:
  - name: DrugA
  - name: Placebo

visit_schedule: oncology_phase2_standard

endpoints:
  - name: PFS
    type: survival
```

---

## 4.2 Canonical Study State

Represents **simulated execution of the study**.

Contains:

* subjects
* sites
* visits
* events
* treatment exposure
* outcomes

SimCT uses an **event timeline model**.

Example event timeline:

| Day | Event           |
| --- | --------------- |
| -14 | screening       |
| 0   | randomization   |
| 0   | dosing          |
| 10  | AE start        |
| 14  | lab abnormality |
| 30  | AE resolved     |
| 120 | endpoint        |

This canonical state becomes the **source of truth** for generating artifacts.

---

# 5. Artifact Layers

SimCT produces artifacts in three layers.

---

## Layer 1 — Design Artifacts

Generated from **Study Blueprint**

Examples:

* protocol skeleton
* SAP skeleton
* CRF structure
* arms tables
* schedule of assessments
* visit matrix

---

## Layer 2 — Operational Artifacts

Generated from **Blueprint + rules**

Examples:

* edit checks
* data collection logic
* EDC form definitions
* derivation specs
* SDTM mapping hints

---

## Layer 3 — Simulated Study Data

Generated from **Canonical Study State**

Examples:

* SDTM datasets
* raw datasets
* operational events
* protocol deviations
* listings
* study summaries

---

# 6. MVP Feature Scope

SimCT v1 supports generation of:

### Core Outputs

1. Synthetic SDTM datasets
2. Raw / EDC-like datasets
3. Protocol skeleton
4. SAP skeleton
5. CRF structure metadata

---

# 7. System Architecture

SimCT follows a **layered architecture**.

---

# 7.1 Config Layer

Responsibilities:

* load YAML blueprint
* validate schema
* normalize defaults
* resolve templates

Objects:

```
StudyBlueprint
ArmSpec
SiteSpec
SimulationSettings
ScenarioSettings
```

---

# 7.2 Knowledge Layer

Provides domain knowledge.

Knowledge packs include:

* indication models
* drug class effects
* visit templates
* event probabilities

Examples:

```
oncology_pack
diabetes_pack
checkpoint_inhibitor_pack
```

Knowledge packs are **separate installable packages**.

Example:

```
simct-oncology-pack
simct-cardiology-pack
```

Objects:

```
KnowledgeRepository
IndicationProfile
DrugClassProfile
VisitTemplateProfile
EndpointModel
```

---

# 7.3 Simulation Layer

Core simulation engine.

Responsibilities:

* initialize study
* create sites
* simulate enrollment
* assign treatment arms
* generate subject timelines
* simulate events

Objects:

```
StudySimulator
SubjectSimulator
SiteSimulator
EventEngine
RandomManager
```

Operational simulation includes:

* staggered enrollment
* screen failures
* missed visits
* treatment discontinuation
* protocol deviations

---

# 7.4 Canonical Event Model

Each subject maintains an **event timeline**.

Event types include:

```
EnrollmentEvent
VisitEvent
DoseEvent
LabEvent
AEEvent
CMEvent
EndpointEvent
ProtocolDeviationEvent
```

Events include:

```
subject_id
event_type
timestamp
attributes
```

---

# 7.5 Projection Layer

Transforms canonical state into artifacts.

Example projectors:

```
DMProjector
AEProjector
EXProjector
VSProjector
LBProjector
CMProjector
MHProjector
SVProjector
DSProjector
```

Additional projectors:

```
ProtocolProjector
SAPProjector
CRFProjector
RawDatasetProjector
```

Artifact modules are **plugin-based**.

---

# 7.6 Validation Layer

Ensures simulation realism and consistency.

Examples:

* AE cannot occur before enrollment
* lab measurements must align with visits
* dose precedes treatment-related AE
* visits match schedule windows

Validation engine can be **enabled or disabled**.

Objects:

```
StudyValidator
DomainValidator
CrossDomainValidator
```

---

# 7.7 Output Layer

Responsible for exports.

Supported outputs:

* CSV datasets
* Pandas DataFrames
* JSON canonical state
* summary reports

Objects:

```
OutputWriter
SummaryBuilder
StateExporter
```

---

# 8. Simulation Characteristics

### Maximum Study Size (MVP)

Up to:

```
200 subjects
5 arms
15 sites
```

Designed to run on a **standard laptop**.

---

### Deterministic Reproducibility

SimCT supports deterministic simulations.

```
same blueprint + same seed → identical study
```

Randomness controlled by **global seed**.

---

### Random Management

Single global seed controls all modules.

```
SimulationSettings:
  random_seed: 42
```

---

# 9. Study Sites Model

Sites include:

* region
* enrollment rate
* variability

Example:

```yaml
sites:
  count: 12
  enrollment_rate: medium
```

---

# 10. Study Scenarios

Users can adjust behavior using **scenario parameters**.

Example:

```yaml
scenario:
  enrollment_speed: fast
  dropout_rate: high
  ae_rate_multiplier: 1.3
  deviation_rate: medium
```

Allows simulation of:

* slow enrollment
* safety signals
* high dropout trials

---

# 11. Endpoint Simulation

Endpoints are defined in blueprint.

Example:

```yaml
endpoints:
  - name: PFS
    type: survival
```

Outcome models come from **knowledge packs**.

Example:

* oncology survival models
* diabetes biomarker response

---

# 12. CRF / eCRF Generation

SimCT generates **structured CRF metadata**.

Includes:

* forms
* sections
* fields
* variable definitions

Output format:

```
JSON / YAML
```

---

# 13. Protocol and SAP Generation

Protocol and SAP skeletons generated using **LLM-based templates**.

LLM input includes:

* blueprint
* endpoint definitions
* visit schedules
* arms

Outputs:

* protocol structure
* SAP sections
* statistical descriptions

---

# 14. Study Templates

SimCT ships with predefined templates.

Examples:

```
phase2_oncology_randomized
phase3_diabetes_superiority
single_arm_oncology
dose_escalation_trial
```

Users can override parameters.

---

# 15. Study Summary Reports

SimCT automatically generates study summaries.

Includes:

* subject counts
* enrollment timeline
* AE incidence
* endpoint outcomes
* operational metrics

Used for:

* debugging
* demos
* sanity checks

---

# 16. Interfaces

### MVP Interface

Primary interface:

**Python SDK**

Example usage:

```python
from simct import StudySimulator

sim = StudySimulator.from_yaml("study.yml", seed=42)

sim.run()

sdtm = sim.generate_sdtm()
protocol = sim.generate_protocol()
crf = sim.generate_crf()
```

---

### Future Interface

REST API:

```
POST /simulate-study
POST /generate-sdtm
POST /generate-protocol
```

---

# 17. Extensibility

SimCT supports plugin generators.

Example plugin modules:

```
simct-sdtm
simct-protocol
simct-crf
simct-rawdata
simct-adam
```

Knowledge packs also extensible.

---

# 18. Versioning

Outputs include version metadata.

Example:

```
simct_version
knowledge_pack_version
blueprint_version
simulation_seed
```

Ensures reproducibility across releases.

---

# 19. Non-Goals (MVP)

Not included in v1:

* pharmacokinetic modeling
* detailed disease progression models
* regulatory-grade datasets
* UI study designer

---

# 20. Future Expansion

SimCT can evolve into:

* **clinical trial digital twin platform**

Future modules:

* monitoring simulations
* query generation
* QA test case generation
* medical review workflows
* ADaM dataset simulation
* regulatory submission scenarios
* site performance analytics

---

# 21. Strategic Value

SimCT creates a **foundational simulation engine for clinical trials**.

Key differentiators:

1. Event-driven canonical study state
2. Multiple artifact projections
3. Domain knowledge packs
4. Deterministic reproducibility
5. Plugin architecture

This makes SimCT useful across:

* clinical software development
* QA testing
* AI training data generation
* study design experimentation
