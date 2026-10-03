# STAGING Logical Model

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project
Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint
2D ? STAGING Logical Model

## Purpose

STAGING converts nested FHIR JSON into structured, testable rows while
preserving source meaning and lineage.

STAGING is not yet the final analytical warehouse.

---

# Common Lineage Columns

Every staging entity must retain, where applicable:

- pipeline_run_id
- source_file
- source_page_number
- source_resource_type
- source_resource_id
- parent_resource_id
- source_sequence
- source_ordinal
- raw_record_hash

---

# Logical Entities

## 1. stg_patient

One row = one FHIR Patient resource.

Business/source key:
- patient_id

Selected logical content:
- patient identifiers
- birth date
- gender
- address
- communication
- profile metadata

---

## 2. stg_coverage

One row = one FHIR Coverage resource.

Business/source key:
- coverage_id

Parent/reference:
- patient_id / beneficiary reference

Selected logical content:
- status
- subscriber id
- relationship
- period
- coverage type
- payor reference
- class information

---

## 3. stg_eob_claim

One row = one ExplanationOfBenefit resource.

Business/source key:
- eob_id

References:
- patient
- coverage
- provider
- insurer

Selected logical content:
- status
- use
- outcome
- type
- subtype
- created date
- billable period
- payment information
- profile/source metadata

---

## 4. stg_eob_item

One row = one item within one EOB.

Business/source key:
- eob_id
- item_sequence

Parent:
- stg_eob_claim

Selected logical content:
- product/service code
- quantity
- service date/period
- location
- revenue coding
- modifier information

---

## 5. stg_eob_diagnosis

One row = one diagnosis within one EOB.

Business/source key:
- eob_id
- diagnosis_sequence

Parent:
- stg_eob_claim

Selected logical content:
- diagnosis code/system
- diagnosis type
- on-admission status

---

## 6. stg_eob_procedure

One row = one procedure within one EOB.

Business/source key:
- eob_id
- procedure_sequence

Parent:
- stg_eob_claim

Selected logical content:
- procedure code/system
- procedure type
- procedure date

---

## 7. stg_eob_care_team

One row = one care-team element within one EOB.

Business/source key:
- eob_id
- careteam_sequence

Parent:
- stg_eob_claim

Selected logical content:
- provider identifier
- provider identifier system
- provider display
- provider type
- role
- qualification

---

## 8. stg_eob_supporting_info

One row = one supportingInfo element within one EOB.

Business/source key:
- eob_id
- supporting_info_sequence

Parent:
- stg_eob_claim

Selected logical content:
- category coding
- code coding
- timing date/period
- value quantity
- value string

---

## 9. stg_eob_adjudication

One row = one claim-level adjudication element.

Business/source key:
- eob_id
- source_ordinal

Parent:
- stg_eob_claim

Selected logical content:
- category code/system
- amount
- currency
- value
- reason

---

## 10. stg_eob_total

One row = one claim total element.

Business/source key:
- eob_id
- source_ordinal

Parent:
- stg_eob_claim

Selected logical content:
- total category code/system
- amount
- currency

---

## 11. stg_eob_item_adjudication

One row = one adjudication element within one EOB item.

Business/source key:
- eob_id
- item_sequence
- source_ordinal

Parent:
- stg_eob_item

Selected logical content:
- adjudication category
- amount
- currency
- reason

---

## 12. stg_eob_item_detail

One row = one detail element within one EOB item.

Business/source key:
- eob_id
- item_sequence
- detail_sequence

Parent:
- stg_eob_item

Selected logical content:
- product/service coding
- quantity

---

# Secondary FHIR Structures

The following structures remain preserved but are not promoted to independent
staging entities yet:

- identifiers
- extensions
- modifiers
- contained resources
- diagnosisSequence
- informationSequence
- additional codings

Treatment at this stage:

1. selected analytically useful values may become staging columns;
2. source system + code must stay together;
3. original structure remains available in RAW;
4. no structure may be silently discarded;
5. later profiling may promote a structure to its own child entity.

---

# Relationship Map

Patient
  ?
Coverage

Patient
  ?
EOB Claim
  ??? EOB Item
  ?    ??? Item Adjudication
  ?    ??? Item Detail
  ??? Diagnosis
  ??? Procedure
  ??? Care Team
  ??? Supporting Info
  ??? Claim Adjudication
  ??? Claim Total

---

# STAGING Rules

1. RAW remains immutable.
2. STAGING rows must reconcile to RAW structures.
3. Parent keys must be retained.
4. Source sequence must be retained where available.
5. Source ordinal is used only when no FHIR sequence exists.
6. No unexplained duplicate business keys.
7. No silent row deletion.
8. No automatic replacement of NULL with zero.
9. Invalid values must be flagged, not silently corrected.
10. Every row must retain lineage to its RAW source.

---

# Modeling Boundary

This model defines logical STAGING entities only.

It does not yet define:

- physical SQL tables;
- SQL data types;
- indexes;
- surrogate keys;
- final dimensions/facts;
- star schema;
- KPIs;
- Power BI relationships.
