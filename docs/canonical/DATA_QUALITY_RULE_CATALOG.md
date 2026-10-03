# Data Quality Rule Catalog

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project
Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint
2C ? Data Quality Rule Catalog

## Status Model

- PASS ? expected condition satisfied.
- WARNING ? suspicious or incomplete condition requiring review.
- FAIL ? project/data-integrity condition that blocks canonical publication.
- SOURCE_WARNING ? reproducible source behavior preserved without rewriting source data.

---

## DQ-001 ? RAW Immutability
RAW FHIR responses must never be modified during canonical processing.

Severity: FAIL

## DQ-002 ? Expected Resource Type
Patient files must contain Patient resources, Coverage files Coverage resources,
and EOB files ExplanationOfBenefit resources.

Severity: FAIL

## DQ-003 ? Resource Identity
Patient, Coverage and ExplanationOfBenefit canonical parent resources must
retain their original FHIR resource id.

Severity: FAIL

## DQ-004 ? Resource Uniqueness
The same FHIR resource id must not appear more than once in the same governed
extraction population unless later source evidence proves versioned duplication.

Severity: FAIL

## DQ-005 ? Parent Reference Integrity
Where an explicit parent reference is supplied, it must be retained and its
format validated.

Examples:
- Coverage.beneficiary.reference
- ExplanationOfBenefit.patient.reference

Unresolvable references must remain visible as DQ evidence.

Severity: FAIL or WARNING according to reference type and source contract.

## DQ-006 ? Child Sequence Presence
For repeating structures where FHIR supplies sequence, retain it.

Applies to:
- item.sequence
- diagnosis.sequence
- procedure.sequence
- careTeam.sequence
- supportingInfo.sequence
- detail.sequence

Missing sequence on an observed child requiring sequence is a DQ exception.

Severity: FAIL

## DQ-007 ? Child Sequence Uniqueness
Sequence values must be unique within their correct parent grain.

Examples:
- eob_id + item_sequence
- eob_id + diagnosis_sequence
- eob_id + procedure_sequence
- eob_id + careteam_sequence
- eob_id + supporting_info_sequence
- eob_id + item_sequence + detail_sequence

Severity: FAIL

## DQ-008 ? Ordinal-Based Structures
Where the source has no business sequence, preserve deterministic source array
ordinal.

Applies currently to:
- claim-level adjudication
- claim totals
- item-level adjudication

Ordinal must never be interpreted as business rank or meaning.

Severity: FAIL if ordinal cannot be reproduced deterministically.

## DQ-009 ? Optional FHIR Structures
Missing optional structures are not automatically errors.

Examples observed as optional:
- diagnosis
- procedure
- insurer
- subType
- payment amount/date

Do not invent missing values.

Severity: PASS / not applicable unless a later contract makes the field required.

## DQ-010 ? Coding Integrity
FHIR coding must preserve code and coding system together when supplied.

Display text is descriptive and may be absent.

Severity:
- missing code/system pair needed for interpretation ? WARNING/FAIL
- missing display only ? allowed

## DQ-011 ? Financial Value Integrity
Financial amount values must remain numeric.

Currency must be preserved when supplied and must not be silently defaulted.

Severity: FAIL for invalid numeric amount; WARNING for unexpected missing currency.

## DQ-012 ? Date Validity
Date/date-time values must be parseable.

For periods:
start <= end

Do not silently correct reversed or malformed dates.

Severity: FAIL

## DQ-013 ? Internal Contained References
References beginning with # must resolve to the matching contained resource id
inside the same parent FHIR resource when such references are used.

Severity: FAIL

## DQ-014 ? Bundle.total Source Exception
Bundle.total is retained as source metadata.

The validated CMS Blue Button v3 Sandbox behavior showed that Bundle.total may
not equal the complete multi-page result population.

Completeness is therefore controlled by:

Bundle.link[next] traversal
? raw target-resource count
? unique resource-key reconciliation
? duplicate detection

Severity: SOURCE_WARNING

## DQ-015 ? RAW-to-Canonical Count Reconciliation
Every canonical entity produced from a repeating FHIR structure must reconcile
to the corresponding source structure count unless a documented eligibility or
mapping rule explains the difference.

Severity: FAIL

## DQ-016 ? Parent/Child Reconciliation
Every canonical child row must retain its parent key.

No orphan canonical rows are allowed unless explicitly classified as an
unresolved source-reference exception.

Severity: FAIL

## DQ-017 ? Type Drift
Observed field types must be checked against the approved canonical contract.

Compatible numeric representations such as integer and decimal may be
standardized only under an explicit numeric rule.

Unexpected structural/type drift must be surfaced.

Severity: WARNING or FAIL according to materiality.

## DQ-018 ? Repeating Structure Preservation
Repeated structures must not be silently discarded.

Structures currently requiring explicit disposition include:
- identifiers
- codings
- extensions
- modifiers
- contained resources
- diagnosisSequence
- informationSequence
- type codings
- revenue codings

Each must later be classified as:
1. canonical child entity;
2. selected canonical attributes;
3. governed mapping/reference data;
4. preserved source JSON/lineage.

Severity: FAIL if silently lost.

## DQ-019 ? Lineage
Every canonical row must be traceable back to its RAW source.

Required lineage design must include, as applicable:
- pipeline run id
- source resource type
- source resource id
- source page/file
- child sequence or source ordinal

Severity: FAIL

## DQ-020 ? Security
Canonical data, manifests, documentation and logs must never contain:
- Client Secret
- access token
- refresh token
- authorization code
- PKCE verifier

Severity: FAIL

---

# Governance Rule

Data-quality detection does not automatically mean deletion.

Invalid, unusual or unresolved records must remain traceable until an approved
business/source rule determines their treatment.

# Modeling Boundary

This catalog defines DQ expectations only.

It does not yet define:
- SQL physical tables;
- final data types;
- surrogate keys;
- warehouse/star schema;
- KPIs;
- Power BI model.
