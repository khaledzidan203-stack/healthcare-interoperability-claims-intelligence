# PostgreSQL DDL Build

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Checkpoint
3B ? PostgreSQL DDL Build

## Purpose

Defines the physical PostgreSQL foundation for:

- governance schema;
- staging schema;
- reserved analytics schema.

## Scope

The DDL creates:

- 12 staging tables;
- 4 governance tables;
- primary keys;
- parent-child foreign keys;
- pipeline lineage foreign keys;
- type and integrity checks;
- supporting indexes.

## Safety

The script is non-destructive.

It does not contain:

- DROP TABLE;
- TRUNCATE;
- DELETE FROM.

Checkpoint 3B builds and statically validates the SQL only.

Checkpoint 3C will execute the DDL against PostgreSQL and inspect the
created database objects before any STAGING data is loaded.
