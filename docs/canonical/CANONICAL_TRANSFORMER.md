# Canonical / STAGING Transformer

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Checkpoint
2E ? Canonical Transformer Build

## Purpose

This module transforms immutable FHIR RAW resources into the twelve approved
logical staging grains.

It does not create SQL tables.

## Safety

- RAW files are read-only.
- Source FHIR resource ids are preserved.
- Child sequence values are preserved.
- Array ordinal is preserved where required.
- Duplicate sequence values fail transformation.
- Missing required child sequences fail transformation.
- Every output row contains lineage metadata.
- Every output row contains a SHA256 hash of its source fragment.
- Every output row retains the complete source fragment as canonical JSON.

The retained source fragment prevents secondary FHIR structures from being
silently lost while later typed field mappings are refined.

## Current Boundary

Checkpoint 2E builds and unit-tests the transformer only.

Checkpoint 2F will execute it against the validated live RAW run and reconcile
RAW structure counts against transformed staging counts.
