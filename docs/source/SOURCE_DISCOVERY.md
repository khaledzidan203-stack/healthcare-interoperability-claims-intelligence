# Source Discovery

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Scope

This document records source characteristics verified during Checkpoint 0B.

It does not define the final warehouse model.

## CMS Sample Resources

The CMS sample package contains:

- Patient
- Coverage
- ExplanationOfBenefit

Coverage and ExplanationOfBenefit are represented as FHIR Bundles because a
beneficiary can have multiple coverage records and claims.

## Patient

Observed resource type:
Patient

Observed CARIN profile:
http://hl7.org/fhir/us/carin-bb/StructureDefinition/C4BB-Patient

Observed top-level fields:

- address
- birthDate
- deceasedDateTime
- extension
- gender
- id
- identifier
- meta
- name
- resourceType

Observed sample counts:

- identifiers: 2
- names: 1
- addresses: 1
- telecom: 0
- communication: 0
- unique extension URLs: 18

No outbound FHIR references were detected in the Patient sample.

## Coverage

Observed Bundle:

- resourceType: Bundle
- type: searchset
- total: 4
- entries: 4

All four contained resources are Coverage.

All four have status = active.

Observed CARIN profile:
http://hl7.org/fhir/us/carin-bb/StructureDefinition/C4BB-Coverage

Observed fields include:

- id
- meta
- extension
- status
- type
- subscriberId
- beneficiary
- relationship
- payor
- class
- period

The period element appears in 2 of 4 sampled Coverage resources.

Coverage references Patient.

## ExplanationOfBenefit

Observed Bundle:

- resourceType: Bundle
- type: searchset
- reported total: 146
- entries present in downloaded sample: 10

All 10 resources are ExplanationOfBenefit.

Observed CARIN profile:
C4BB-ExplanationOfBenefit-Pharmacy

Observed values:

- use = claim for all 10
- outcome = complete for all 10
- item lines = 10 total
- diagnosis entries = 0
- procedure entries = 0
- careTeam entries = 10
- supportingInfo entries = 94
- insurance entries = 10

Each sampled EOB has one item.

Observed references:

- Patient
- Coverage

Observed coding systems include NDC, CARIN adjudication, CMS adjudication,
claim type, pharmacy service fields, drug-coverage fields, DAW fields,
brand/generic fields, prescription-origin fields, and plan identifiers.

## Mandatory Pagination Finding

EOB Bundle.total = 146

Downloaded sample entries = 10

Therefore a single Bundle cannot be assumed to represent the complete result
set.

Future ingestion must support pagination and reconciliation of retrieved
resource counts.

## Synthetic User Catalog

Observed nonblank rows:
10,001

Observed uniqueness:

- unique BENE_ID: 10,001
- unique FRONTEND_USER_NAME: 10,001
- duplicate BENE_ID rows: 0
- duplicate usernames: 0
- missing BENE_ID: 0
- missing usernames: 0

total_claim_count:

- minimum: 3
- median: 32
- maximum: 76
- aggregate: 325,915

total_claim_line_count:

- minimum: 3
- median: 55
- maximum: 214
- aggregate: 586,830

inpatient_claim_count:

- minimum: 0
- median: 0
- maximum: 7
- aggregate: 1,996
- zero-count users: 8,413

partd_event_count:

- minimum: 0
- median: 0
- maximum: 0
- aggregate: 0
- zero-count rows: 10,001

The synthetic-user CSV is a testing and user-selection aid.

Actual validated API payloads take precedence over this catalog.

## CMS v3 Data Dictionary

Observed rows:
345

Observed columns:
16

FHIR Resource distribution:

- ExplanationOfBenefit: 287
- Coverage: 34
- Patient: 18
- AuditEvent: 6

FHIRPath:

- populated: 345
- missing: 0

Documented claim or coverage categories include Pharmacy, Carrier, DME, HHA,
Hospice, Inpatient, Outpatient, SNF, Part A, Part B, Part C, Part D and
dual-related mappings.

The data dictionary is a governance and mapping reference.

It does not prove that every field appears in every API response.

## Blue Button System Listing

Observed rows:
317

Observed unique System URLs:
312

Observed unique CCW field names:
305

Observed duplicate CCW-field-name rows:
12

Missing System URLs:
0
