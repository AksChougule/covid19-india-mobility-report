The **internal object model** is what will determine whether SimCT stays elegant or turns into a tangled set of generators.

The goal is to make **everything flow through a few canonical structures**:

1. **Blueprint objects** — what is planned
2. **Simulation state objects** — what exists right now during simulation
3. **Event objects** — what happened over time
4. **Projection-ready views** — what artifact generators consume

The cleanest architecture is:

> **Blueprint → Initialized Study State → Event Timeline → Derived Subject/Study State → Projectors**

That gives you a stable foundation for SDTM, raw data, protocol, SAP, CRF, and later edit checks, query generation, QA scenarios, and more.

---

# 1. Design principles for the object model

The internal model should satisfy a few rules:

### A. Separate “planned” from “actual”

A visit in the protocol is not the same as a visit that actually happened.

So keep separate concepts for:

* planned schedule
* simulated actual conduct

### B. Events are append-only facts

Instead of mutating everything directly, record events like:

* subject enrolled
* randomized
* dose given
* visit missed
* AE started
* lab measured

Then derive state from those facts.

### C. Keep projectors dumb

The SDTM generator should not invent study behavior.
It should mostly **translate canonical state/events into rows**.

### D. Use IDs everywhere

Everything important should have stable IDs:

* study_id
* arm_id
* site_id
* subject_id
* visit_id
* planned_assessment_id
* event_id
* form_id
* field_id

### E. Make knowledge-pack influence explicit

Do not hide knowledge behavior everywhere.
Profiles and rules should be attached clearly to the study/arm/subject context.

---

# 2. Top-level canonical model

At the highest level, SimCT should revolve around these core objects:

```python
StudyBlueprint
StudyRunContext
StudyState
SubjectState
StudyEvent
KnowledgeRepository
ArtifactManifest
```

A simple mental model:

* **StudyBlueprint** = plan
* **StudyRunContext** = simulation settings and resolved knowledge
* **StudyState** = living simulation world
* **SubjectState** = one subject’s current state
* **StudyEvent** = facts over time
* **ArtifactManifest** = what was generated

---

# 3. Blueprint layer: canonical planned design objects

These are loaded from YAML and normalized into typed objects.

## 3.1 StudyBlueprint

This is the root object.

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class StudyBlueprint(BaseModel):
    study: "StudySpec"
    population: "PopulationSpec"
    arms: List["ArmSpec"]
    sites: "SitePlanSpec"
    schedule_template: str
    endpoints: List["EndpointSpec"] = Field(default_factory=list)
    assessments: List["AssessmentSpec"] = Field(default_factory=list)
    interventions: List["InterventionSpec"] = Field(default_factory=list)
    operational_rules: "OperationalRulesSpec"
    scenario: Optional["ScenarioSpec"] = None
    metadata: "BlueprintMetadata"
```

This should remain **normalized and explicit**, even if YAML is short.

---

## 3.2 StudySpec

```python
class StudySpec(BaseModel):
    study_id: str
    title: str
    indication: str
    phase: str
    design_type: str  # randomized_parallel, single_arm, crossover, etc.
    blinding: str     # open_label, double_blind, single_blind
    planned_subject_count: int
    planned_site_count: int
    therapeutic_area: Optional[str] = None
```

This gives all modules a stable header.

---

## 3.3 PopulationSpec

```python
class PopulationSpec(BaseModel):
    age_min: int
    age_max: int
    sex_strategy: str  # balanced, female_skewed, male_skewed, unrestricted
    baseline_severity_model: Optional[str] = None
    inclusion_tags: list[str] = Field(default_factory=list)
    exclusion_tags: list[str] = Field(default_factory=list)
    comorbidity_profile: Optional[str] = None
```

This informs subject generation.

---

## 3.4 ArmSpec

```python
class ArmSpec(BaseModel):
    arm_id: str
    name: str
    arm_type: str  # placebo, active, comparator, standard_of_care
    planned_ratio: float
    intervention_ids: list[str]
    epoch_sequence: list[str] = Field(default_factory=list)
```

Important: `arm_id` must be stable because it will appear everywhere.

---

## 3.5 InterventionSpec

```python
class InterventionSpec(BaseModel):
    intervention_id: str
    name: str
    drug_class: Optional[str] = None
    route: Optional[str] = None
    frequency: Optional[str] = None
    dose_level: Optional[str] = None
    start_rule: Optional[str] = None
    stop_rule: Optional[str] = None
```

This object is important because knowledge packs will often attach to **drug_class**.

---

## 3.6 EndpointSpec

```python
class EndpointSpec(BaseModel):
    endpoint_id: str
    name: str
    endpoint_type: str  # survival, binary, continuous, ordinal
    role: str           # primary, secondary, exploratory
    analysis_population: Optional[str] = None
    source_assessment_ids: list[str] = Field(default_factory=list)
    model_key: Optional[str] = None
```

This makes endpoint simulation and SAP generation much easier.

---

## 3.7 AssessmentSpec

```python
class AssessmentSpec(BaseModel):
    assessment_id: str
    name: str
    category: str   # lab, vital_sign, efficacy, questionnaire, imaging
    planned_form_id: Optional[str] = None
    timing_rule: Optional[str] = None
    result_model_key: Optional[str] = None
```

Assessments are the bridge between:

* protocol schedule
* CRF design
* raw datasets
* SDTM projectors

---

## 3.8 SitePlanSpec

```python
class SitePlanSpec(BaseModel):
    site_count: int
    regions: list[str] = Field(default_factory=list)
    enrollment_model: str = "uniform"
    site_profiles: list["SiteProfileSpec"] = Field(default_factory=list)
```

And site profile:

```python
class SiteProfileSpec(BaseModel):
    site_profile_id: str
    region: Optional[str] = None
    relative_enrollment_weight: float = 1.0
    screen_failure_rate: Optional[float] = None
    missed_visit_rate: Optional[float] = None
    protocol_deviation_rate: Optional[float] = None
```

---

## 3.9 OperationalRulesSpec

```python
class OperationalRulesSpec(BaseModel):
    enrollment_start_day: int = 0
    enrollment_window_days: int = 180
    screen_failure_enabled: bool = True
    withdrawal_enabled: bool = True
    missed_visit_enabled: bool = True
    protocol_deviation_enabled: bool = True
    rescheduling_enabled: bool = True
```

---

## 3.10 ScenarioSpec

This lets users quickly shift simulation behavior.

```python
class ScenarioSpec(BaseModel):
    enrollment_speed: Optional[str] = None   # slow, medium, fast
    dropout_rate: Optional[str] = None       # low, medium, high
    ae_rate_multiplier: float = 1.0
    deviation_rate: Optional[str] = None
    adherence_level: Optional[str] = None
```

---

## 3.11 BlueprintMetadata

```python
class BlueprintMetadata(BaseModel):
    blueprint_version: str
    author: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    source_template: Optional[str] = None
```

---

# 4. Knowledge layer objects

These should be resolved before simulation starts.

## 4.1 KnowledgeRepository

```python
class KnowledgeRepository(BaseModel):
    indication_profiles: Dict[str, "IndicationProfile"]
    drug_class_profiles: Dict[str, "DrugClassProfile"]
    visit_templates: Dict[str, "VisitTemplateProfile"]
    endpoint_models: Dict[str, "EndpointModelProfile"]
    assessment_models: Dict[str, "AssessmentModelProfile"]
```

This is the runtime-resolved knowledge bundle.

---

## 4.2 IndicationProfile

```python
class IndicationProfile(BaseModel):
    indication_key: str
    default_demographics_model: str
    common_comorbidities: list[str] = Field(default_factory=list)
    baseline_severity_distribution: dict = Field(default_factory=dict)
    common_endpoint_model_keys: list[str] = Field(default_factory=list)
```

---

## 4.3 DrugClassProfile

```python
class DrugClassProfile(BaseModel):
    drug_class_key: str
    common_ae_terms: list[str] = Field(default_factory=list)
    lab_effect_rules: list["LabEffectRule"] = Field(default_factory=list)
    discontinuation_risk: Optional[float] = None
    adherence_impact_model: Optional[str] = None
```

---

## 4.4 VisitTemplateProfile

```python
class VisitTemplateProfile(BaseModel):
    template_key: str
    visits: list["PlannedVisitSpec"] = Field(default_factory=list)
```

---

## 4.5 EndpointModelProfile

```python
class EndpointModelProfile(BaseModel):
    model_key: str
    endpoint_type: str
    parameters: dict = Field(default_factory=dict)
```

---

# 5. Initialization layer: resolved run context

Before simulation begins, YAML + knowledge packs should become a fully resolved context.

## 5.1 StudyRunContext

```python
class StudyRunContext(BaseModel):
    blueprint: StudyBlueprint
    knowledge: KnowledgeRepository
    simulation_settings: "SimulationSettings"
    resolved_schedule: list["PlannedVisitSpec"]
    resolved_forms: list["FormDefinition"]
    run_metadata: "RunMetadata"
```

This avoids repeated lookups during simulation.

---

## 5.2 SimulationSettings

```python
class SimulationSettings(BaseModel):
    random_seed: int
    max_subjects: int = 200
    validation_enabled: bool = True
    export_canonical_state: bool = True
    output_formats: list[str] = Field(default_factory=lambda: ["csv"])
```

---

## 5.3 RunMetadata

```python
class RunMetadata(BaseModel):
    simct_version: str
    blueprint_version: str
    knowledge_pack_versions: dict[str, str] = Field(default_factory=dict)
    run_id: str
```

---

# 6. Canonical study state objects

This is the most important part.

## 6.1 StudyState

This is the simulation “world.”

```python
class StudyState(BaseModel):
    study_id: str
    status: str  # initialized, enrolling, active, completed
    current_day: int = 0

    sites: Dict[str, "SiteState"] = Field(default_factory=dict)
    subjects: Dict[str, "SubjectState"] = Field(default_factory=dict)

    planned_visits: list["PlannedVisitSpec"] = Field(default_factory=list)
    events: list["StudyEvent"] = Field(default_factory=list)

    study_metrics: "StudyMetrics" = Field(default_factory=lambda: StudyMetrics())
```

Important: `StudyState` should contain both:

* entities
* global event log

---

## 6.2 SiteState

```python
class SiteState(BaseModel):
    site_id: str
    region: Optional[str] = None
    status: str = "active"

    target_enrollment: Optional[int] = None
    actual_enrollment: int = 0

    screen_failure_rate: float = 0.0
    missed_visit_rate: float = 0.0
    protocol_deviation_rate: float = 0.0

    subject_ids: list[str] = Field(default_factory=list)
```

---

## 6.3 SubjectState

This should be rich but not bloated.

```python
class SubjectState(BaseModel):
    subject_id: str
    site_id: str

    status: str  # screened, enrolled, randomized, active, discontinued, completed
    arm_id: Optional[str] = None

    demographics: "Demographics"
    baseline_profile: "BaselineProfile"

    consent_day: Optional[int] = None
    screen_day: Optional[int] = None
    randomization_day: Optional[int] = None
    treatment_start_day: Optional[int] = None
    treatment_end_day: Optional[int] = None
    discontinuation_day: Optional[int] = None
    study_end_day: Optional[int] = None

    scheduled_visits: list["SubjectPlannedVisit"] = Field(default_factory=list)
    actual_visits: list["ActualVisit"] = Field(default_factory=list)

    exposures: list["ExposureRecord"] = Field(default_factory=list)
    adverse_events: list["SubjectAE"] = Field(default_factory=list)
    concomitant_medications: list["SubjectCM"] = Field(default_factory=list)
    protocol_deviations: list["SubjectDeviation"] = Field(default_factory=list)
    endpoint_outcomes: list["EndpointOutcome"] = Field(default_factory=list)

    derived_flags: dict[str, bool] = Field(default_factory=dict)
```

This object becomes incredibly valuable later.

---

## 6.4 Demographics

```python
class Demographics(BaseModel):
    age: int
    sex: str
    race: Optional[str] = None
    ethnicity: Optional[str] = None
```

---

## 6.5 BaselineProfile

```python
class BaselineProfile(BaseModel):
    disease_severity: Optional[str] = None
    comorbidities: list[str] = Field(default_factory=list)
    baseline_labs: dict[str, float] = Field(default_factory=dict)
    risk_factors: dict[str, float] = Field(default_factory=dict)
```

---

## 6.6 StudyMetrics

```python
class StudyMetrics(BaseModel):
    enrolled_count: int = 0
    randomized_count: int = 0
    active_count: int = 0
    completed_count: int = 0
    discontinued_count: int = 0
    screen_failed_count: int = 0
```

---

# 7. Planned schedule vs actual conduct objects

This separation is critical.

## 7.1 PlannedVisitSpec

Blueprint-level schedule definition.

```python
class PlannedVisitSpec(BaseModel):
    visit_id: str
    name: str
    visit_number: int
    nominal_day: int
    window_min: Optional[int] = None
    window_max: Optional[int] = None
    required_assessment_ids: list[str] = Field(default_factory=list)
    optional_assessment_ids: list[str] = Field(default_factory=list)
    epoch: Optional[str] = None
```

---

## 7.2 SubjectPlannedVisit

Subject-specific expected visit.

```python
class SubjectPlannedVisit(BaseModel):
    subject_id: str
    visit_id: str
    nominal_day: int
    target_day: int
    status: str = "planned"  # planned, due, completed, missed, skipped
```

---

## 7.3 ActualVisit

What really happened.

```python
class ActualVisit(BaseModel):
    subject_id: str
    visit_id: str
    actual_day: int
    status: str  # completed, missed, partial, unscheduled
    performed_assessment_ids: list[str] = Field(default_factory=list)
```

That separation alone will save you a lot of pain.

---

# 8. Event model

This is the true canonical history.

## 8.1 Base StudyEvent

```python
from uuid import uuid4

class StudyEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    study_id: str
    subject_id: Optional[str] = None
    site_id: Optional[str] = None
    day: int
    event_type: str
    attributes: dict = Field(default_factory=dict)
```

This generic base is enough for storage and export.

You may also want typed subclasses for clarity.

---

## 8.2 Typed event subclasses

```python
class EnrollmentEvent(StudyEvent):
    event_type: str = "enrollment"

class RandomizationEvent(StudyEvent):
    event_type: str = "randomization"

class DoseEvent(StudyEvent):
    event_type: str = "dose"

class VisitCompletedEvent(StudyEvent):
    event_type: str = "visit_completed"

class VisitMissedEvent(StudyEvent):
    event_type: str = "visit_missed"

class AEStartedEvent(StudyEvent):
    event_type: str = "ae_started"

class AEEndedEvent(StudyEvent):
    event_type: str = "ae_ended"

class LabMeasurementEvent(StudyEvent):
    event_type: str = "lab_measurement"

class EndpointEvent(StudyEvent):
    event_type: str = "endpoint"

class ProtocolDeviationEvent(StudyEvent):
    event_type: str = "protocol_deviation"
```

My recommendation:

* store/export as generic `StudyEvent`
* use typed constructors internally for readability

---

# 9. Clinical data objects inside subject state

These are subject-level aggregates derived from events.

## 9.1 ExposureRecord

```python
class ExposureRecord(BaseModel):
    intervention_id: str
    start_day: int
    end_day: Optional[int] = None
    dose_level: Optional[str] = None
    frequency: Optional[str] = None
    status: str = "active"
```

---

## 9.2 SubjectAE

```python
class SubjectAE(BaseModel):
    ae_id: str
    term: str
    start_day: int
    end_day: Optional[int] = None
    severity: Optional[str] = None
    seriousness: Optional[bool] = None
    related_to_treatment: Optional[bool] = None
    action_taken: Optional[str] = None
    outcome: Optional[str] = None
```

---

## 9.3 SubjectCM

```python
class SubjectCM(BaseModel):
    cm_id: str
    medication_name: str
    indication: Optional[str] = None
    start_day: int
    end_day: Optional[int] = None
    linked_ae_id: Optional[str] = None
```

---

## 9.4 SubjectDeviation

```python
class SubjectDeviation(BaseModel):
    deviation_id: str
    category: str
    day: int
    severity: Optional[str] = None
    description: Optional[str] = None
```

---

## 9.5 EndpointOutcome

```python
class EndpointOutcome(BaseModel):
    endpoint_id: str
    status: str  # pending, observed, censored
    event_day: Optional[int] = None
    value: Optional[float] = None
    category: Optional[str] = None
```

---

# 10. CRF / raw data canonical objects

These are very important because CRF, raw datasets, and even edit checks can all use them.

## 10.1 FormDefinition

```python
class FormDefinition(BaseModel):
    form_id: str
    name: str
    category: str
    sections: list["FormSection"] = Field(default_factory=list)
```

## 10.2 FormSection

```python
class FormSection(BaseModel):
    section_id: str
    title: str
    fields: list["FieldDefinition"] = Field(default_factory=list)
```

## 10.3 FieldDefinition

```python
class FieldDefinition(BaseModel):
    field_id: str
    variable_name: str
    label: str
    data_type: str
    required: bool = False
    codelist_name: Optional[str] = None
    origin_assessment_id: Optional[str] = None
```

These definitions should come from:

* assessment specs
* schedule templates
* domain conventions

---

## 10.4 FormInstance

A filled form for a subject visit.

```python
class FormInstance(BaseModel):
    form_instance_id: str
    form_id: str
    subject_id: str
    visit_id: str
    day: int
    status: str = "completed"
    field_values: dict[str, object] = Field(default_factory=dict)
```

This becomes the basis for raw/EDC-like datasets.

---

# 11. Projection-friendly dataset abstractions

Before going straight to SDTM rows, introduce one small abstraction.

## 11.1 RecordBundle

```python
class RecordBundle(BaseModel):
    dataset_name: str
    records: list[dict] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
```

Each projector returns `RecordBundle`.

Examples:

* `DMProjector -> RecordBundle(dataset_name="DM")`
* `AEProjector -> RecordBundle(dataset_name="AE")`

This makes output writing much simpler.

---

## 11.2 ArtifactManifest

Track what was generated.

```python
class ArtifactManifest(BaseModel):
    generated_at: str
    run_id: str
    artifacts: list["ArtifactEntry"] = Field(default_factory=list)
```

```python
class ArtifactEntry(BaseModel):
    artifact_type: str   # sdtm, protocol, sap, crf, canonical_state
    artifact_name: str
    version_info: dict = Field(default_factory=dict)
    path: Optional[str] = None
```

---

# 12. Recommended relationships between objects

The most important links are:

* `StudyBlueprint` owns planned study design
* `StudyRunContext` resolves blueprint + knowledge + settings
* `StudyState` owns sites, subjects, planned visits, events
* `SubjectState` owns subject-level aggregates and actual visits
* `StudyEvent` is the canonical history
* `FormDefinition` / `FormInstance` support CRF and raw data
* `RecordBundle` supports projections

A simplified dependency map:

```text
StudyBlueprint
 ├── StudySpec
 ├── PopulationSpec
 ├── ArmSpec[]
 ├── EndpointSpec[]
 ├── AssessmentSpec[]
 ├── InterventionSpec[]
 └── OperationalRulesSpec

StudyRunContext
 ├── StudyBlueprint
 ├── KnowledgeRepository
 ├── SimulationSettings
 └── resolved_schedule[]

StudyState
 ├── SiteState[]
 ├── SubjectState[]
 ├── StudyEvent[]
 └── StudyMetrics

SubjectState
 ├── Demographics
 ├── BaselineProfile
 ├── SubjectPlannedVisit[]
 ├── ActualVisit[]
 ├── ExposureRecord[]
 ├── SubjectAE[]
 ├── SubjectCM[]
 ├── SubjectDeviation[]
 └── EndpointOutcome[]
```

---

# 13. What should be mutable vs immutable

This is a subtle but important design choice.

## Prefer immutable or mostly immutable:

* `StudyBlueprint`
* `KnowledgeRepository`
* `FormDefinition`
* `PlannedVisitSpec`

## Mutable during simulation:

* `StudyState`
* `SubjectState`
* `SiteState`
* `StudyMetrics`

## Append-only:

* `StudyEvent`

That gives you a very clean mental model.

---

# 14. Minimal canonical state export format

Since you want canonical state export, define a stable schema early.

A good export shape is:

```json
{
  "run_metadata": {},
  "study_blueprint_summary": {},
  "sites": [],
  "subjects": [],
  "events": [],
  "metrics": {}
}
```

For subjects, export:

* IDs
* assigned arm
* key dates
* actual visits
* AEs
* exposures
* outcomes

For events, export normalized rows:

* event_id
* subject_id
* day
* event_type
* attributes

This will make downstream reuse much easier.

---

# 15. Best implementation strategy: start smaller than the full model

You do not need to implement all classes on day 1.

Start with these **foundational canonical objects first**:

### Phase 1 core objects

* `StudyBlueprint`
* `StudyRunContext`
* `StudyState`
* `SiteState`
* `SubjectState`
* `PlannedVisitSpec`
* `ActualVisit`
* `StudyEvent`
* `ExposureRecord`
* `SubjectAE`
* `EndpointOutcome`
* `RecordBundle`

That is enough to build:

* enrollment
* randomization
* visits
* exposure
* AEs
* endpoints
* SDTM projection

### Phase 2 objects

* `FormDefinition`
* `FormInstance`
* `SubjectCM`
* `SubjectDeviation`
* `ArtifactManifest`

That unlocks:

* raw data
* CRF
* operational scenarios
* better summaries

---

# 16. Strong recommendation: split canonical model into 5 code files

To avoid one giant models file, organize like this:

```text
simct/core/models/
  blueprint.py
  knowledge.py
  state.py
  events.py
  artifacts.py
```

Suggested contents:

### `blueprint.py`

* StudyBlueprint
* StudySpec
* PopulationSpec
* ArmSpec
* EndpointSpec
* AssessmentSpec
* InterventionSpec
* OperationalRulesSpec
* ScenarioSpec

### `knowledge.py`

* KnowledgeRepository
* IndicationProfile
* DrugClassProfile
* VisitTemplateProfile
* EndpointModelProfile

### `state.py`

* StudyRunContext
* SimulationSettings
* RunMetadata
* StudyState
* SiteState
* SubjectState
* Demographics
* BaselineProfile
* StudyMetrics
* PlannedVisitSpec
* SubjectPlannedVisit
* ActualVisit
* ExposureRecord
* SubjectAE
* SubjectCM
* SubjectDeviation
* EndpointOutcome

### `events.py`

* StudyEvent
* typed event subclasses

### `artifacts.py`

* FormDefinition
* FormSection
* FieldDefinition
* FormInstance
* RecordBundle
* ArtifactManifest
* ArtifactEntry

---

# 17. The most important architectural payoff

Once these objects exist, almost every SimCT service becomes easier:

## SDTM generation

Project from:

* `StudyState.subjects`
* `StudyState.events`

## Raw dataset generation

Project from:

* `FormDefinition`
* `FormInstance`
* `ActualVisit`

## Protocol generation

Project from:

* `StudyBlueprint`
* `resolved_schedule`

## SAP generation

Project from:

* `EndpointSpec`
* `ArmSpec`
* `PopulationSpec`

## CRF generation

Project from:

* `AssessmentSpec`
* `FormDefinition`

## Validation

Validate across:

* planned schedule
* actual visits
* event order
* endpoint consistency

That is why the right object model makes implementation feel 10x cleaner.

---

# 18. My recommended “golden path” object flow

This is the flow I would design around:

```text
YAML
  ↓
StudyBlueprint
  ↓
Knowledge resolution
  ↓
StudyRunContext
  ↓
StudyState.initialize()
  ↓
Event-driven simulation
  ↓
StudyState + StudyEvent log
  ↓
Projectors
  ↓
Artifacts / datasets / summaries / exports
```

---

# 19. One extra refinement that will help a lot later

I recommend giving every subject a lightweight **SubjectDerivedState** or cached summary view, instead of forcing all projectors to re-scan the entire event log every time.

Example:

```python
class SubjectDerivedState(BaseModel):
    latest_status: str
    latest_visit_day: Optional[int] = None
    on_treatment: bool = False
    active_ae_count: int = 0
    primary_endpoint_status: Optional[str] = None
```

This should be:

* recomputed during simulation
* stored in `SubjectState` as a cached helper

That gives you the benefits of event sourcing without making every projection expensive or awkward.

---

# 20. Final recommendation

If you want the cleanest SimCT foundation, use this rule:

> **The canonical truth is the event timeline, but the practical working surface is StudyState + SubjectState aggregates.**

That gives you both:

* architectural purity
* implementation convenience

