# Power BI Report Architecture

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Report Contract State

**FROZEN FOR PBIR CONSTRUCTION**

## Page Architecture

1. INDEX
2. Executive Overview
3. Claims Activity
4. Clinical & Coding
5. Provider & Payer
6. Terminology & Governance
7. Methodology & Validation

## Navigation Contract

- INDEX is the opening/navigation page.
- INDEX contains six destination tiles.
- Every destination page contains a Home action back to INDEX.
- No circular analytical navigation is required in V1.

## Global Analytical Filter Contract

Analytical pages P01?P05 use:

- DimDate[calendar_year]
- DimDate[calendar_quarter]

These are the only common page slicers in V1.

## Measure Contract

User-facing measures:

- Claim Count
- Item Count
- Diagnosis Occurrences
- Procedure Occurrences
- Care Team Occurrences
- Supporting Info Occurrences

Restricted financial primitives are not bound to report visuals.

## Governance Boundaries

### Financial

No consolidated or cross-grain financial KPI is published.

### Coverage

DimCoverage and BridgeClaimCoverage remain excluded.

### Terminology

Source code/display may be used with an explicit mapping limitation.
`authoritative_display` is not used in V1 report bindings.

### Snapshot

The report represents one governed pipeline snapshot.
Cross-run aggregation is forbidden.

## Build Boundary

This checkpoint creates documentation contracts only.

No PBIR page, visual, navigation or interaction artifact is modified.

The next checkpoint may begin controlled PBIR construction only after
this architecture contract is validated.
