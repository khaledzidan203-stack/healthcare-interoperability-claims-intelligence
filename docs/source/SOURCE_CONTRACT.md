# Source Contract

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Source

CMS Blue Button FHIR API and official CMS Blue Button reference artifacts.

## Current Primary Resource Scope

- Patient
- Coverage
- ExplanationOfBenefit

AuditEvent is present in the CMS v3 data dictionary as an additional documented
FHIR resource.

Live API scope will be locked only after sandbox validation.

## Format

Primary API payload:
FHIR JSON

Current reference formats:

- JSON
- CSV
- TXT

## Source Reference Policy

Everything under:

data/source_reference

is treated as immutable.

Source-reference files must not be cleaned, manually corrected, reformatted,
or overwritten.

Required transformations must occur in derived layers.

## RAW Policy

Future API responses will be stored under:

data/raw

The RAW layer must preserve source fidelity and traceability.

Planned ingestion metadata includes:

- pipeline_run_id
- extraction timestamp
- endpoint
- resource type
- synthetic beneficiary identifier
- HTTP status
- page information
- source/API version
- extraction status
- content hash

Exact metadata implementation is gated by the API ingestion checkpoint.

## Pagination Contract

Pagination is mandatory.

Evidence:

- EOB Bundle total: 146
- downloaded sample entries: 10

The ingestion implementation must:

1. detect pagination continuation;
2. retrieve intended pages;
3. prevent duplicate resource ingestion;
4. capture page-level failures;
5. reconcile retrieved counts;
6. support controlled retry.

## Source Integrity

Checkpoint 0A created SHA256 fingerprints for all seven initial reference
files.

Checkpoint 0B confirmed those hashes were unchanged.

Unexpected reference-file hash changes are governance exceptions.

## Schema Drift

FHIR JSON must not be treated as a fixed flat schema.

The pipeline must account for:

- optional elements
- different cardinalities
- nested arrays
- newly observed extensions
- different EOB profiles
- different claim types
- new coding systems
- API/source-version changes

## Authority Order

1. validated API payload
2. official CMS/FHIR documentation
3. validated source-reference artifacts
4. documented project mappings
5. analytical structures

Assumptions do not override observed source behavior.

## Analytical Limitation

Synthetic CMS data is used for engineering and analytical demonstration.

Synthetic results must not be represented as real Medicare population
findings.
