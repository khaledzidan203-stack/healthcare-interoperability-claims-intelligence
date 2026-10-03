# Analytics Physical Model DDL

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5A ? Analytics Physical DDL Build

## State

**DDL BUILT / NOT DEPLOYED**

No analytics physical table is created in PostgreSQL by this checkpoint.

## Physical Model

- Dimensions: 13
- Facts: 10
- Bridges: 1
- Total analytics tables: 24
- Designed analytics relationships: 53
- Direct fact-to-fact foreign keys: 0

## Model Pattern

The physical warehouse implements the approved **Governed Dimensional Fact Constellation**.

Child facts carry conformed dimension keys directly rather than depending on semantic fact-to-fact joins.

## Core Conformed Dimensions

- DimDate
- DimPipelineRun
- DimPatient
- DimFinancialConcept
- DimCurrency

## SCD Strategy

`DimPatient` and `DimCoverage` physically support SCD Type 2 versioning through:

- valid-from pipeline run;
- valid-to pipeline run;
- current-row indicator;
- row hash.

## Provider Source Limitation

The current normalized v2 source contains:

- 39 provider identity-ready occurrences;
- 2 claim-provider occurrences where source identity is not explicit.

`DimProvider` therefore supports one explicit governed Unknown member.

Those two occurrences may map to that Unknown member during the later warehouse-load checkpoint.

This does not fabricate source identity.

## Coverage Source Limitation

All six claim insurance associations are structurally preserved, but they contain display text only and no explicit Coverage reference or identifier.

Therefore:

- `BridgeClaimCoverage` is physically defined;
- each association can have a deterministic bridge key;
- `coverage_key` is nullable;
- no direct `coverage_key` exists on `FactClaim`;
- current-run Coverage dimension linkage remains load-gated.

The existence of one fetched Coverage resource is not treated as evidence that the six claim associations point to it.

## Financial Safety

`FactClaimTotal`, `FactClaimAdjudication`, and `FactItemAdjudication` remain separate physical facts.

Each uses:

- `DimFinancialConcept`;
- `DimCurrency`.

This does not permit cross-fact or cross-grain aggregation.

## DDL Safety

The build file contains no:

- DROP TABLE;
- DROP SCHEMA;
- TRUNCATE;
- DELETE;
- UPDATE;
- INSERT.

Checkpoint 5A only defines and validates the DDL.

## DDL Artifact

`sql/04_create_analytics_model.sql`

SHA256:

`E4D853D06ED2EC057FF2E9F1AAC9D0B5BB170BAD528634F6BD2B286C4C353958`

## Next Gate

Deploy this validated DDL into the currently empty `analytics` schema, then verify the physical database metadata before loading any analytics data.
