# Authoritative Financial Terminology

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

4C ? Authoritative Financial Terminology Resolution

## Scope

- Pipeline run: `run_20260930T084004Z_ingest_2db2ed86`
- Financial source combinations: 68
- Unique financial system/code pairs: 58
- Monetary concepts: 51
- Non-monetary count/weight concepts: 6
- Status discriminator concepts: 1
- Unresolved financial combinations: 0
## Authoritative Sources

- CMS Blue Button v3 CodeSystem: Adjudication
- HL7 Terminology CodeSystem: adjudication
- CARIN Blue Button IG 2.1.0: C4BBAdjudication
- CARIN Blue Button IG 2.1.0: C4BBAdjudicationDiscriminator

## Critical Semantic Finding

Not every value located in an FHIR adjudication structure is money.

The following CMS concepts in the validated source are explicitly classified as non-monetary values:

- Claim Medicare Utilization Day Count
- Beneficiary Total Coinsurance Days Count
- Claim Medicare Non Utilization Days Count
- Hospice Period Count
- Beneficiary Medicare Lifetime Reserve Days Used Count
- PPS DRG Weight Number

`benefitpaymentstatus` is a CARIN adjudication discriminator and is not an amount.

## Aggregation Guard

A monetary concept may only be considered for aggregation when:

1. system URI and code are identical;
2. currency is identical;
3. analytical grain is identical;
4. claim-level and item-level values are not combined blindly;
5. the final analytical model explicitly approves the measure.

Therefore, resolving a code as a monetary amount does not automatically make it a KPI.

## KPI Governance State

All mapped concepts remain `NOT_APPROVED` for KPI use.

No financial KPI, fact table, measure, or Power BI calculation is created by this checkpoint.

## Decision

Financial terminology semantics are sufficiently resolved to begin analytical grain and metric-contract design, while preserving strict controls against cross-grain double counting.
