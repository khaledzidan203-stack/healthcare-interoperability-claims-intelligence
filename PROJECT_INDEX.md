# Healthcare Interoperability & Claims Intelligence Platform

> Status: HISTORICAL build record. For the current implementation, start with [README](README.md) and [release evidence](docs/validation/RELEASE_VALIDATION_EVIDENCE.md). Historical approval/pending statements do not redefine the release.

## Project Identity

Project:
Healthcare Interoperability & Claims Intelligence Platform

Repository target:
healthcare-fhir-claims-intelligence-platform

Local project root:
<project-root>

## Purpose

Build an end-to-end healthcare interoperability and claims intelligence
platform using CMS Blue Button FHIR resources.

Target flow:

CMS Blue Button
? OAuth / API
? FHIR JSON
? Immutable RAW
? Validation
? Normalized STAGING
? Governed Analytical Warehouse
? SQL / Python Reconciliation
? Semantic Model
? Power BI
? GitHub Portfolio Release

No analytical warehouse schema, dimensional model, KPI contract, or semantic
model is approved yet.

## Governance Principle

Validated implementation and observed source behavior take precedence over
assumptions.

Business Question
? Source Evidence
? Data Contract
? Grain
? Data Quality
? Transformation
? Reconciliation
? Analytical Model
? KPI
? Visualization

## Checkpoint Status

### Checkpoint 0A ? Local Bootstrap & Source Validation
Status: APPROVED

Validated:
- project root
- directory structure
- seven source-reference files
- JSON syntax
- CSV structure
- SHA256 source fingerprints
- project cleanliness
- absence of temporary execution artifacts

### Checkpoint 0B ? Deep Source Discovery & Profiling
Status: APPROVED

Profiled:
- Patient
- Coverage
- ExplanationOfBenefit
- synthetic-user catalog
- CMS v3 data dictionary
- Blue Button system listing

Important discovery:
The EOB sample Bundle reports total = 146 while only 10 entries are contained
in the downloaded sample page.

Pagination is therefore a mandatory ingestion requirement.

### Checkpoint 0C ? Governance Documentation
Status: IN PROGRESS

## Current Source Inventory

1. patient_bbuser29999.json
2. coverage_bundle_bbuser29999.json
3. eob_bundle_bbuser29999.json
4. readme.txt
5. synthetic_users_by_claim_count_full.csv
6. v3-data-dictionary-2.248.0.csv
7. bluebutton_system_listing.csv

All source-reference files are immutable.

## Current Modeling Boundary

No analytical warehouse schema is approved.

No star schema is approved.

No warehouse grain is approved.

No KPI set is approved.

No Power BI semantic model is approved.

These decisions remain gated by live API profiling.

### Checkpoint 1E ? Live Pagination Validation

**Status:** APPROVED

Validated on CMS Blue Button v3:

- OAuth Authorization Code + PKCE
- live multi-page ExplanationOfBenefit extraction
- Bundle.link[next] traversal
- 3-page forced pagination test
- 6 unique EOB resources
- zero cross-page duplicates
- RAW pagination evidence
- token-free persistence

Governed source exception:

Bundle.total did not reconcile to the full cross-page EOB population during
the validated v3 Sandbox pagination test.

The project therefore uses Bundle.link[next] traversal plus unique resource-key
reconciliation as the extraction completeness control.

### Checkpoint 1F ? Final Reusable Ingestion Layer

**Status:** IN PROGRESS

Purpose:

Convert validated discovery behavior into permanent reusable source-controlled
Python ingestion code with unit tests and documented security/completeness
contracts.
