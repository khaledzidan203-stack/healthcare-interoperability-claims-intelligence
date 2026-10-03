# Governed Analytics Transactional Load

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5D ? Governed Analytics Transactional Load

## State

**DATABASE LOADED / TRANSACTION COMMITTED / RECONCILED**

## Source Package

`data/processed/analytics_load/v1/run_20260930T084004Z_ingest_2db2ed86`

Package rows:

**3245**

## PostgreSQL

- Server version: 17.11
- Database: `healthcare_interoperability_claims`
- Schema: `analytics`

## Loaded Population

- Dimension rows: 2563
- Fact rows: 676
- Bridge rows: 6
- Total Analytics rows: 3245

## Transaction Safety

All 24 target entities were loaded inside one PostgreSQL
transaction.

The transaction contained a pre-COMMIT reconciliation block.
Any entity-count mismatch would have raised an exception and
rolled back the complete load.

## Provider Governance

- Governed Unknown Provider members: 1
- Claims mapped to Unknown Provider: 2

No Provider identity was fabricated.

## Coverage Governance

- Claim/Coverage bridge rows: 6
- Explicit Coverage links: 0
- Display-only unlinked associations: 6

The current-run `DimCoverage` linkage remains load-gated.

No Coverage identity was inferred from display text.

## Financial Governance

- Financial structural fact rows: 450
- Authoritative financial concepts: 74
- Financial KPIs approved: 0

Claim Total, Claim Adjudication, and Item Adjudication remain
separate fact grains.

No cross-grain financial aggregation was performed.

## Reconciliation

`docs/analytics/ANALYTICS_LOAD_RECONCILIATION.csv`

All 24 package entity counts are reconciled to PostgreSQL.

## Governance Run Status

The authoritative governance column is:

`governance.pipeline_run.run_status`

After this load it intentionally remains:

`STAGING_DQ_VALIDATED`

It will not advance until independent Analytics post-load
data-quality validation succeeds in Checkpoint 5E.

## Immutable Inputs

The following remained unchanged:

- Governed STAGING manifest
- Reference-normalization v2 manifest
- Analytics dry-run package manifest

## Next Gate

Checkpoint 5E must independently validate the loaded Analytics
warehouse against STAGING, the dry-run package, dimensional
relationships, source limitations, and financial grain rules
before any business KPI or Power BI semantic model is approved.
