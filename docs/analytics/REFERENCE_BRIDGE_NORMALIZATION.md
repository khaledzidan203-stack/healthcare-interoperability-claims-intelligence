# Reference & Bridge Normalization

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Current Version

**v2 ? source-aware normalization contract**

## Correction Rationale

The first normalization package correctly preserved the source structures but incorrectly treated absence of explicit source identity material as a pipeline failure.

Diagnosis established that all six claim insurance coverage objects contain display text but no reference or identifier. Therefore no Coverage identity may be inferred.

Two claim-provider occurrences likewise contain no explicit identity material. They remain governed source-limited occurrences rather than fabricated provider identities.

## Governed Result

- Claim/Coverage associations preserved: 6
- Coverage identities explicitly resolved: 0
- Display-only Coverage associations: 6
- Provider identities resolved: 39
- Provider source-identity-not-explicit occurrences: 2
- Payer identities resolved: 4
- Contained resources normalized: 8
- Unresolved contained references: 0

## Critical Governance Rule

**Absence of source identity is not a pipeline defect and is not permission to infer identity.**

A display value is descriptive source text only. It must not be used as a master-data key.

## Claim / Coverage Bridge State

`BridgeClaimCoverage` is structurally ready because every source `insurance[]` association is preserved with a deterministic association key.

However, the `DimCoverage` relationship remains **LOAD_GATED** for this run because the source does not provide an explicit Coverage reference or identifier in those six associations.

The existence of one fetched Coverage resource is not sufficient evidence to infer that all six associations refer to it.

## Provider State

Thirty-nine provider occurrences have deterministic source-based identity candidates. Two claim-provider occurrences remain `SOURCE_IDENTITY_NOT_EXPLICIT` and require explicit Unknown/Unresolved warehouse treatment rather than fabricated identity.

## Payer State

All four payer occurrences have deterministic source-based identity.

## Versioning

The original v1 processed package is retained unchanged as audit evidence. v2 supersedes it for future analytical loading.

## Analytics DDL Gate

Analytics DDL may now be designed with:

- nullable or explicit Unknown/Unresolved dimension handling;
- a structurally available Claim/Coverage bridge;
- the Coverage dimension relationship kept load-gated;
- no identity inference from display values;
- no modification to governed STAGING.
