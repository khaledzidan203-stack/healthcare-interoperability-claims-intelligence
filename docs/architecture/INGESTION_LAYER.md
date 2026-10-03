# CMS Blue Button v3 Ingestion Layer

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Status

Checkpoint 1F introduces the first permanent reusable Python ingestion
implementation for the project.

## Package

src/healthcare_claims/

Modules:

- config.py
- oauth.py
- fhir.py
- storage.py
- ingest.py
- __main__.py

## Responsibilities

### config.py

Loads the local .env file and validates:

- Client ID presence
- Client Secret presence
- v3 API contract
- HTTPS CMS Sandbox base URL
- localhost OAuth callback

The Client Secret is excluded from dataclass repr output.

### oauth.py

Implements:

- OAuth 2.0 Authorization Code
- PKCE S256
- CSRF state validation
- localhost callback listener
- token exchange
- required-scope validation

Tokens remain in process memory only.

### fhir.py

Implements:

- Patient extraction
- Coverage extraction
- ExplanationOfBenefit extraction
- _count page sizing
- Bundle.link[next] traversal
- off-domain pagination rejection
- pagination-loop protection
- transient HTTP retry
- resource-key reconciliation
- cross-page duplicate rejection
- Bundle.total source-warning handling

## Completeness Contract

Completeness is defined by:

follow Bundle.link[next] until absent
? reconcile raw target-resource count
? reconcile unique resource keys
? reject duplicates

Bundle.total is retained as source metadata but is not the sole completeness
control because Checkpoint 1E reproduced a v3 Sandbox discrepancy.

## Retry Contract

Retryable HTTP statuses:

- 429
- 500
- 502
- 503
- 504

Retries use bounded exponential backoff and honor an integer Retry-After value
when present.

## Storage Contract

RAW API responses are persisted under:

data/raw/cms_bluebutton/v3/<run_id>/

Before final publication, page files and run_manifest.json are written to a
temporary staging directory outside the project root:

<project-parent>/output/

The completed run directory is then moved into the governed RAW path.

If persistence fails, the external staging directory is removed.

## Security Contract

The permanent code never intentionally persists:

- Client Secret
- access token
- refresh token
- authorization code
- PKCE verifier

The run manifest records only safe execution metadata.

## Test Contract

Permanent unit tests cover:

- secret-safe configuration representation
- invalid redirect rejection
- the observed Bundle.total warning pattern
- cross-page duplicate rejection
- off-domain pagination rejection
- token-free RAW manifest persistence

Live API behavior is validated separately in a controlled smoke-test
checkpoint.
