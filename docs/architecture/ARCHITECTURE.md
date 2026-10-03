# Architecture

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Current Status

The architecture below is the target architecture.

Detailed physical implementation is not yet locked.

## Target Flow

CMS Blue Button Developer Source
        |
        v
OAuth / Authorized Access
        |
        v
FHIR REST API
        |
        v
Python Ingestion
        |
        +-- HTTP handling
        +-- Pagination
        +-- Retry logic
        +-- Error handling
        +-- Logging
        +-- Run metadata
        |
        v
Immutable RAW FHIR JSON
        |
        v
FHIR / Structural Validation
        |
        v
Data Quality & Governance
        |
        +-- Completeness
        +-- Duplicate detection
        +-- Referential checks
        +-- Coding-system checks
        +-- Schema-drift detection
        +-- Exception handling
        +-- Lineage
        |
        v
Normalized STAGING
        |
        v
Governed Analytical Warehouse
        |
        v
SQL / Python Reconciliation
        |
        v
Semantic Model
        |
        v
Power BI PBIP / PBIR / TMDL

## Observed Resource Relationships

Coverage references Patient.

ExplanationOfBenefit references:

- Patient
- Coverage

Final key strategy is not approved yet.

## Pagination Requirement

Observed:

Bundle.total = 146

Downloaded EOB entries = 10

Pagination is therefore a first-class pipeline requirement.

## Layer Responsibilities

### Source Reference

Official downloaded examples and reference dictionaries.

Immutable.

### RAW

Faithfully preserved API responses plus ingestion metadata.

### STAGING

Normalized relational representation of FHIR structures.

### Warehouse

Governed analytical structures with explicit grain.

### Semantic Model

Business-facing governed measures and dimensions.

### Presentation

Power BI analytical application.

## Modeling Rule

The final star schema will be derived from:

- business questions
- actual API payloads
- resource profiles
- cardinality
- grain
- data-quality behavior
- reconciliation requirements

It will not be copied from a generic healthcare schema.
