# Governed Analytics Load Build

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5C ? Governed Analytics Load Build

## State

**ETL BUILT / DRY-RUN PACKAGE VALIDATED / DATABASE NOT LOADED**

## Purpose

Build the permanent transformation layer that converts governed
STAGING plus reference-normalization v2 into load-ready Analytics
structures.

The package uses natural-key references. PostgreSQL surrogate keys
are resolved only during the later transactional load checkpoint.

## Sources

- Governed STAGING
- Reference normalization v2
- Authoritative financial terminology mapping
- Approved Analytics dimensional model

## Target Model

- Dimensions: 13
- Facts: 10
- Bridges: 1
- Total target entities: 24

## Fact Reconciliation

Total analytical fact rows prepared:

**676**

This equals the complete ten approved analytical source grains:

- FactClaim: 6
- FactItem: 29
- FactClaimTotal: 26
- FactClaimAdjudication: 31
- FactItemAdjudication: 393
- FactDiagnosisOccurrence: 29
- FactProcedureOccurrence: 2
- FactCareTeamOccurrence: 35
- FactSupportingInfoOccurrence: 112
- FactItemDetail: 13

## Provider Governance

Two claim-provider occurrences lack explicit source identity.

They map to one explicit governed Unknown Provider member.

No provider identity is fabricated.

Care-team provider occurrences require explicit deterministic source
identity and are not mapped to Unknown silently.

## Coverage Governance

Six Claim/Coverage associations are preserved.

Current-run linkage state:

- explicit Coverage links: 0
- display-only unlinked associations: 6

The bridge is load-ready structurally, but the Coverage dimension
foreign key remains NULL for those source-limited associations.

## Financial Governance

Financial physical facts remain separate:

- Claim Total
- Claim Adjudication
- Item Adjudication

All 450 financial structural rows resolve to one
of the 74 authoritative financial concepts.

No cross-grain aggregation is performed.

No consolidated financial KPI is created.

## Dry-Run Package

`data/processed/analytics_load/v1/run_20260930T084004Z_ingest_2db2ed86`

Package type:

`NATURAL_KEY_REFERENCE_DRY_RUN`

The package is an immutable pre-load artifact.

## Database State

This checkpoint performs **no PostgreSQL INSERT, UPDATE, DELETE,
TRUNCATE or Analytics data load**.

The deployed Analytics schema remains empty until the governed
transactional load checkpoint.

## Next Gate

Resolve natural-key package references to PostgreSQL surrogate keys,
load all dimensions/facts/bridge in one governed transaction, and
reconcile every loaded grain back to this dry-run package.
