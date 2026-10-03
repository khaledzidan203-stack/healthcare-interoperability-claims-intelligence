# Physical Database Design

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project
Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint
3A ? Physical Database Design

## Database Engine

PostgreSQL

## Purpose

The database will receive validated canonical STAGING data.

RAW FHIR JSON remains immutable in the governed filesystem and is not replaced
by the relational database.

---

# Database Schemas

## staging

Validated relational representation of FHIR source structures.

## governance

Pipeline runs, reconciliation evidence, data-quality exceptions and lineage
metadata.

## analytics

Reserved for the governed analytical model.

No analytics facts or dimensions are defined yet.

---

# Physical STAGING Tables

## staging.patient

Primary business key:
- patient_id TEXT

Important types:
- birth_date DATE
- gender TEXT
- JSON-preserved structures JSONB
- raw_record_hash CHAR(64)

---

## staging.coverage

Primary business key:
- coverage_id TEXT

Important types:
- status TEXT
- subscriber_id TEXT
- beneficiary_reference TEXT
- period_start DATE
- period_end DATE
- preserved structures JSONB

---

## staging.eob_claim

Primary business key:
- eob_id TEXT

Important types:
- patient_reference TEXT
- status TEXT
- use TEXT
- outcome TEXT
- claim_type_code TEXT
- claim_type_system TEXT
- created TIMESTAMPTZ
- billable_period_start TIMESTAMPTZ
- billable_period_end TIMESTAMPTZ
- provider_reference TEXT
- insurer_reference TEXT
- preserved structures JSONB

---

## staging.eob_item

Composite primary key:
- eob_id
- item_sequence

Types:
- item_sequence INTEGER
- source_ordinal INTEGER
- product/service codes TEXT
- preserved structures JSONB

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_diagnosis

Composite primary key:
- eob_id
- diagnosis_sequence

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_procedure

Composite primary key:
- eob_id
- procedure_sequence

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_care_team

Composite primary key:
- eob_id
- careteam_sequence

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_supporting_info

Composite primary key:
- eob_id
- supporting_info_sequence

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_adjudication

Composite primary key:
- eob_id
- source_ordinal

Financial types:
- amount NUMERIC
- currency TEXT

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_total

Composite primary key:
- eob_id
- source_ordinal

Financial types:
- amount NUMERIC
- currency TEXT

Foreign key:
- eob_id ? staging.eob_claim

---

## staging.eob_item_adjudication

Composite primary key:
- eob_id
- item_sequence
- source_ordinal

Financial types:
- amount NUMERIC
- currency TEXT

Foreign key:
- eob_id + item_sequence ? staging.eob_item

---

## staging.eob_item_detail

Composite primary key:
- eob_id
- item_sequence
- detail_sequence

Foreign key:
- eob_id + item_sequence ? staging.eob_item

---

# Common Lineage Columns

All applicable STAGING tables retain:

- pipeline_run_id TEXT
- source_file TEXT
- source_page_number INTEGER
- source_resource_type TEXT
- source_resource_id TEXT
- parent_resource_id TEXT
- source_sequence INTEGER
- source_ordinal INTEGER
- raw_record_hash CHAR(64)
- source_fragment_json JSONB

---

# Governance Tables Planned

## governance.pipeline_run

One row per governed ingestion/transformation run.

## governance.data_quality_result

One row per evaluated DQ rule/result.

## governance.source_exception

Approved source anomalies such as the CMS Bundle.total discrepancy.

## governance.reconciliation_result

RAW ? STAGING and later STAGING ? ANALYTICS reconciliation evidence.

---

# Physical Design Rules

1. RAW files remain immutable outside PostgreSQL.
2. PostgreSQL STAGING is reproducible from RAW.
3. No surrogate keys are required in STAGING.
4. Natural/source composite keys are preserved.
5. Foreign keys enforce approved parent-child grain.
6. JSONB preserves secondary FHIR structures not yet normalized.
7. Monetary values use NUMERIC, never FLOAT.
8. Dates and timestamps remain typed.
9. NULL is preserved; NULL is not automatically converted to zero.
10. Analytics/star-schema design remains a later checkpoint.

---

# Boundary

This checkpoint defines physical design only.

It does not yet:
- create PostgreSQL objects;
- load data;
- create facts/dimensions;
- define KPIs;
- build Power BI.
