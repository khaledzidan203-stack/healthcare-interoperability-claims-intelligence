# Analytics Governance Status Promotion

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

5F ? Analytics Governance Status Promotion

## Validated Pipeline Run

`run_20260930T084004Z_ingest_2db2ed86`

## Promotion

Previous state:

`STAGING_DQ_VALIDATED`

Approved state:

`ANALYTICS_DQ_VALIDATED`

The following records were promoted atomically:

- `governance.pipeline_run`
- `analytics.dim_pipeline_run`

## Promotion Authority

Checkpoint 5E independently validated:

- 33 DQ rules;
- 30 PASS;
- 0 fatal failures;
- 3 governed warnings;
- exact STAGING-to-Analytics fact counts;
- exact source-hash multiset reconciliation;
- zero analytical business-key duplicates;
- exact financial field-level reconciliation;
- one analytical snapshot;
- preserved Coverage identity limitation;
- preserved terminology mapping gate.

## Governed Warnings Retained

### A-DQ-027

Adjudication rows without typed numeric payload remain preserved
and are not coerced to zero.

### A-DQ-030

Non-financial terminology remains mapping-gated.

### A-DQ-031

Six Claim/Coverage associations remain display-only and unlinked.

These warnings do not authorize fabricated semantic mappings.

## Data Preservation

The promotion changed only the two governed `run_status` values.

Validated after promotion:

- Analytics rows: 3245
- Fact rows: 676
- Bridge rows: 6
- Fact source-record fingerprint unchanged: YES
- Bridge association fingerprint unchanged: YES
- 5E DQ evidence unchanged: YES
- STAGING manifest unchanged: YES
- Reference-normalization manifest unchanged: YES
- Analytics package manifest unchanged: YES

## SQL Evidence

`sql/05_promote_analytics_dq_validated.sql`

SHA-256:

`3F4E97EBA2F7EE2FFBA0BA112EB4D5C01C5DB5ED71DA5F3EF57EB69882D1443E`

## Current Warehouse State

**ANALYTICS_DQ_VALIDATED**

The warehouse is now approved as the governed input for the
semantic-layer contract.

This approval does not remove the following gates:

- consolidated financial KPI approval;
- Coverage identity resolution;
- authoritative non-financial terminology mapping;
- explicit single-snapshot filtering policy.

## Next Gate

Define the BI / semantic consumption contract before creating
Power BI measures or report pages.
