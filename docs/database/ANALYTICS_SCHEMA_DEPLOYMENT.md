# Analytics Schema Deployment

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5B ? Analytics Schema Deployment

## Deployment State

**DEPLOYED / EMPTY / VALIDATED**

The approved Analytics DDL was deployed atomically into PostgreSQL.

No Analytics data was loaded by this checkpoint.

## PostgreSQL

- Server version: 17.11
- Database: `healthcare_interoperability_claims`
- Schema: `analytics`

## Approved DDL

Artifact:

`sql/04_create_analytics_model.sql`

SHA256:

`E4D853D06ED2EC057FF2E9F1AAC9D0B5BB170BAD528634F6BD2B286C4C353958`

## Physical Inventory

- Dimensions: 13
- Facts: 10
- Bridges: 1
- Total Analytics tables: 24
- Primary keys: 24

## Foreign-Key Inventory

- Analytics ? Analytics relationships: 53
- Analytics ? Governance lineage foreign keys: 5
- Total foreign keys owned by Analytics tables: 58

The 53-dimensional-model relationship contract counts only
Analytics-to-Analytics physical relationships.

The five additional foreign keys point to governed pipeline-run
lineage and are not semantic-model relationships.

## Relationship Safety

- Direct Fact ? Fact foreign keys: 0
- BridgeClaimCoverage ? FactClaim foreign keys: 1
- Bridge coverage key nullable: YES
- Direct FactClaim coverage key columns: 0

## Source-Limitation Governance

The current source run contains six display-only Coverage
associations and no explicit Coverage identity.

Therefore `BridgeClaimCoverage.coverage_key` remains nullable and
no Coverage identity has been inferred.

`FactClaim.provider_key` is mandatory because unresolved provider
occurrences must later map to an explicit governed Unknown member,
not to a fabricated provider identity.

## Data Load State

- Analytics data rows: 0
- User-facing financial KPIs loaded: 0
- Consolidated financial metrics approved: 0

## Decision

The Analytics physical schema is deployed and structurally
validated.

The next checkpoint may design and build the governed
STAGING/processed ? Analytics loading layer.
