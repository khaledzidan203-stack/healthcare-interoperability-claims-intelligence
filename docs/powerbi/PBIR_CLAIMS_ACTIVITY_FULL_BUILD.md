# Claims Activity Full PBIR Build

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Checkpoint

6C.10a ? Corrected Full Claims Activity Build

## State

STATIC PASS ? POWER BI DESKTOP VALIDATION REQUIRED

## Story

Filters
? Claim Count
? Claim Trend
? Status
? Use
? Outcome
? Claim Type Detail
? Governance

## Governance Correction

Governance validation inspects semantic query bindings only.

Narrative text is not treated as a semantic binding.

Claim Type Detail exposes only:

- source_display
- Claim Count

Authoritative terminology remains excluded until mapped and approved.

## Runtime Requirement

The Claim Type table is based on a native PBIR 2.12 tableEx donor.
The current report is PBIR 2.13.

Power BI Desktop runtime/render/save validation is mandatory.
