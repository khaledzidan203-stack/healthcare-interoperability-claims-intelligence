# Analytics Snapshot Policy

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Current State

The Analytics warehouse currently contains one governed
analytical snapshot.

Pipeline run:

`run_20260930T084004Z_ingest_2db2ed86`

## Current Rule

Facts from multiple pipeline runs must not be aggregated together
implicitly.

The current warehouse therefore requires:

- exactly one `DimPipelineRun` member;
- all facts and bridge rows to belong to the same governed run;
- no cross-run aggregation.

## Future Multi-Run Design

Before multiple snapshots are retained simultaneously, the project
must explicitly design and validate one of:

- active analytical snapshot selection;
- snapshot-version filtering;
- temporal analytical history;
- governed partition/mart strategy.

Power BI must not expose multiple pipeline snapshots without an
explicit semantic filtering contract that prevents duplicate
business events.
