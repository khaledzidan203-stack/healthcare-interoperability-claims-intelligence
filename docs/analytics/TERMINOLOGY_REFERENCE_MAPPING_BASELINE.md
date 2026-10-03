# Terminology & Reference Mapping Baseline

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

4B ? Terminology & Reference Mapping Baseline

## Purpose

Create a complete source-faithful inventory of FHIR/CMS terminology, profiles, contained resource types, and reference patterns before assigning business meanings.

## Governance Rules

1. Exact source system URI and code are preserved.
2. Source display text is preserved when supplied.
3. Missing display text is not invented.
4. Human-readable code meanings are not guessed.
5. Reference inventories are aggregated and do not emit resource IDs.
6. Financial code semantics remain unapproved until authoritative mapping.
7. RAW remains immutable.

## Inventory Summary

- Validated parent FHIR resources: 8
- Coding occurrences: 1569
- Unique terminology systems: 92
- Unique system/code pairs: 408
- Reference occurrences: 15
- Profile occurrences: 10
- Contained-resource occurrences: 8
- Financial category combinations: 85

## Mapping State

All terminology is currently classified as `AUTHORITATIVE_MAPPING_PENDING` unless the source itself supplied a display value.

A source display is evidence from the source payload; it does not by itself constitute an approved analytical KPI definition.

## Mapping Priority

1. Claim and item adjudication categories.
2. Claim total categories.
3. Claim type and subtype terminology.
4. Product/service coding systems.
5. Diagnosis and procedure coding systems.
6. Supporting-information terminology.
7. Profiles, contained resources, and reference targets.

## Next Gate

Resolve discovered terminology against authoritative CMS/HL7 or code-system documentation before analytical facts, dimensions, financial KPIs, or Power BI measures are approved.
