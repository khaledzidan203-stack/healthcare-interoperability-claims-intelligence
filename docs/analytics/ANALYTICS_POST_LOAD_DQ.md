# Analytics Post-Load Data Quality & Reconciliation

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5E ? Corrected Analytics Post-Load Data Quality & Reconciliation

## Validation State

Fatal failures:

**0**

Warnings:

**3**

## Validated Population

- STAGING rows: 678
- Analytics dimensions: 2563
- Analytics facts: 676
- Analytics bridges: 6
- Analytics total rows: 3245

## Independent Reconciliation

Validation includes:

- immutable package ? PostgreSQL counts;
- physical STAGING ? Analytics fact counts;
- STAGING raw-record hash ? Analytics source-record hash multisets;
- analytical business-key uniqueness;
- single-snapshot/run scope;
- date-dimension continuity and role coverage;
- SCD current-member uniqueness;
- Provider/Payer governance;
- Claim/Coverage source limitation;
- financial terminology resolution;
- field-level financial amount/value/currency reconciliation;
- dimensional referential integrity;
- source/package immutability.

## Physical STAGING Contract

PostgreSQL physical STAGING tables use names such as:

- `staging.eob_claim`
- `staging.eob_item`
- `staging.eob_total`
- `staging.eob_adjudication`
- `staging.eob_item_adjudication`

The earlier `stg_*` identifiers are logical/canonical entity names,
not PostgreSQL physical table names.

## Financial Payload Contract

Current physical STAGING supports:

### Claim Total

- amount
- currency

### Claim Adjudication

- amount
- currency
- numeric value

### Item Adjudication

- amount
- currency

No `value` column exists in physical
`staging.eob_item_adjudication`.

Therefore the post-load validation reconciles only fields actually
present in the governed physical source contract and does not invent
an unsupported item-adjudication value field.

Rows with no typed numeric adjudication payload are preserved as
source structural records and are not coerced to zero.

## Financial KPI Gate

- financial structural rows: 450
- financial concepts: 74
- consolidated financial KPIs approved: 0

No cross-grain financial aggregation is approved.

## Coverage Limitation

- bridge rows: 6
- explicit Coverage links: 0
- display-only unlinked associations: 6

No Coverage identity is inferred from display text.

## Terminology Limitation

Non-financial terminology mappings remain pending for
76 dimension members.

This is a documented semantic gate, not a structural load failure.

## Database Mutation

Checkpoint 5E performs no INSERT, UPDATE, DELETE, TRUNCATE or
schema mutation.

Both run-status fields remain:

`STAGING_DQ_VALIDATED`

Status promotion is deliberately deferred to the next checkpoint
after this independent DQ evidence is reviewed.

## Machine-Readable Evidence

`docs/analytics/ANALYTICS_POST_LOAD_DQ_RESULTS.csv`

## Snapshot Governance

`docs/analytics/ANALYTICS_SNAPSHOT_POLICY.md`
