# Semantic Layer Consumption Contract

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

6A ? Semantic Layer Consumption Contract

## Authority

The warehouse input is approved only because the current pipeline
run is:

`ANALYTICS_DQ_VALIDATED`

Validated pipeline run:

`run_20260930T084004Z_ingest_2db2ed86`

## Scope

This checkpoint defines the BI consumption contract.

It does **not** create:

- a PBIX/PBIP;
- Power Query queries;
- TMDL;
- DAX measures;
- report pages;
- visuals.

## Physical Source

Power BI must consume governed objects from the PostgreSQL
`analytics` schema.

Direct consumption of RAW or STAGING is not part of the approved
semantic design.

## Semantic Table Inventory

Physical Analytics tables:

**24**

Current semantic-release tables:

**22**

Load-gated / excluded objects:

- `DimCoverage`
- `BridgeClaimCoverage`

Coverage filtering is excluded because the current six claim
insurance associations contain display text without explicit
Coverage identity.

## Relationship Contract

Total semantic relationships:

**50**

Active relationships:

**45**

Inactive role-playing Date relationships:

**5**

Rules:

- dimension ? fact filtering is single-direction;
- fact ? fact relationships are forbidden;
- bidirectional relationships are not approved;
- Claim Created Date is the active Date role;
- alternate date roles remain inactive;
- Coverage is not connected in the current semantic release.

Inactive Date roles:

- Claim Billable Start Date;
- Claim Billable End Date;
- Item Service Date;
- Procedure Date;
- Supporting Info Timing Date.

## Metric Contract

Governed metric primitives:

**9**

### Approved base measures

- M001 ? Claim Count
- M002 ? Item Count
- M003 ? Diagnosis Occurrences
- M004 ? Procedure Occurrences
- M005 ? Care Team Occurrences
- M006 ? Supporting Info Occurrences

These metrics remain tied to their exact source fact grains.

### Restricted financial primitives

- M007 ? Claim Total Amount
- M008 ? Claim Adjudication Amount
- M009 ? Item Adjudication Amount

These are **not approved user-facing consolidated financial KPIs**.

For any future financial measure:

- preserve the physical fact grain;
- require one exact Financial Concept context;
- require one Currency context;
- never sum Claim Total + Claim Adjudication + Item Adjudication;
- never coerce source nulls to zero;
- do not label a restricted primitive as a business KPI.

## Current Semantic Gates

### SG-001 ? Financial KPIs

State:

`BLOCKED`

Approved consolidated financial KPIs:

**0**

### SG-002 ? Coverage Filtering

State:

`BLOCKED`

Current explicit Coverage links:

**0**

Display-only Claim/Coverage associations:

**6**

### SG-003 ? Non-Financial Terminology

State:

`MAPPING_GATED`

Pending governed terminology members:

**76**

Source coding may be retained structurally, but the report must not
present pending source labels as if they were completed
authoritative terminology mappings.

### SG-004 ? Analytical Snapshot

State:

`SINGLE_SNAPSHOT_ONLY`

Current analytical snapshot count:

**1**

Cross-run aggregation is forbidden.

`DimPipelineRun` should remain hidden from ordinary report users.

## Visibility Rules

Default-hide:

- surrogate keys;
- pipeline keys;
- raw/source hashes;
- technical lineage fields;
- SCD implementation fields;
- `DimPipelineRun`;
- financial fact tables;
- unresolved Coverage objects.

Business-facing coded dimensions must retain enough code/system
context to avoid presenting ambiguous labels.

## Patient Dimension

`DimPatient` participates as a conformed dimension but should be
hidden by default in the initial report.

Patient identifiers must not become accidental report KPIs or
summable numeric fields.

## Financial Null Semantics

Checkpoint 5E confirmed adjudication rows can legitimately retain
no typed numeric payload.

Therefore:

`NULL ? 0`

Power BI measures must not replace those source nulls with zero
unless a separately approved business rule explicitly requires it.

## Cross-Fact Policy

Cross-fact analysis may share conformed dimensions.

A measure must still aggregate from one governed fact grain unless
a separate explicit multi-fact KPI contract is approved.

Current approved cross-fact KPIs:

**0**

## Power BI Implementation Boundary

The next implementation may construct the semantic model only from
this contract.

It must not:

- reconnect Coverage prematurely;
- create bidirectional relationships to make visuals work;
- create direct Fact-to-Fact relationships;
- invent financial KPIs;
- merge financial fact grains;
- silently activate alternate Date relationships;
- expose multiple pipeline snapshots;
- bypass terminology gates.

## Contract Fingerprint

SHA-256:

`FC006081D6BDFC457230AA722085B0EC7EE9FCFB587A6C1453405626DBCB3A9F`

## Machine-Readable Artifacts

- `SEMANTIC_TABLE_CONTRACT.csv`
- `SEMANTIC_RELATIONSHIP_CONTRACT.csv`
- `SEMANTIC_MEASURE_CONTRACT.csv`
- `SEMANTIC_GATES.csv`

## Next Gate

Checkpoint 6B may implement the Power BI semantic model structure
from this contract.

Report-page design and KPI storytelling remain later checkpoints.
