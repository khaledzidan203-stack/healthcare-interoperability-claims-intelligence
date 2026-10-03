# Power BI Semantic Model Hardening

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

6B.3c ? Final Semantic Model Hardening

## State

STATIC HARDENING PASSED

## Governed Semantic State

- Analytics source tables: 22
- Coverage objects excluded/load-gated: 2
- Auto Date/Time: disabled
- Auto-generated Date tables: 0
- Auto-Date variation/defaultHierarchy references: 0
- Semantic relationships: 50
- Active relationships: 45
- Inactive role-playing Date relationships: 5
- Bidirectional relationships: 0
- Fact-to-Fact relationships: 0
- Relationship cardinality: many-to-one
- Cross-filter direction: single direction
- Unsafe implicit column summarization: 0
- Raw financial amount/value fields exposed: 0
- Hidden governed tables: 5
- Source calculated columns: 0
- Explicit DAX measures: 0

## Date Governance

DimDate is the governed semantic Date table.

`calendar_date` is the Date key.

Power BI automatic Date/Time objects are not part of the governed model.

## Financial Governance

Raw monetary/value columns remain available to governed explicit
measures but are hidden from report authors.

No user-facing financial KPI has been approved or created.

## Coverage Governance

DimCoverage and BridgeClaimCoverage remain excluded from the current
semantic release because Coverage identity remains load-gated.

## Runtime Boundary

This checkpoint validates the PBIP/TMDL source statically.

Power BI Desktop runtime validation is required before governed
measure implementation begins.
