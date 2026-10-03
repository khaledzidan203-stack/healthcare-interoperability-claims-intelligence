# Source Exceptions

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## EXC-SRC-001 ? CMS Blue Button v3 Bundle.total Pagination Discrepancy

**State:** CURRENT / SOURCE_WARNING

**Observed:** 2026-09-30

**Environment:** CMS Blue Button Developer Sandbox

**API Version:** v3

**Resource:** ExplanationOfBenefit

**Synthetic test user:** BBUser09338

**Requested page size:** 2

## Reproduced Behavior

Live pagination returned:

- Page 1: Bundle.total = 2, EOB = 2, next = YES
- Page 2: Bundle.total = 2, EOB = 2, next = YES
- Page 3: Bundle.total = 2, EOB = 2, next = NO

Cross-page result:

- pages retrieved: 3
- raw EOB resources: 6
- unique EOB resources: 6
- duplicate EOB resources: 0

The live source therefore exposed six unique EOB resources while each page
reported Bundle.total = 2.

## Evidence

Validated RAW evidence:

data/raw/cms_bluebutton/v3/run_20260930T082250Z_pagination_final_c1b42fb2

Checkpoint result:

CHECKPOINT_1E_LIVE_PAGINATION = PASS

BUNDLE_TOTAL_RECONCILIATION = WARNING

## Governance Decision

Bundle.total is preserved as source metadata.

It is not used as the sole extraction-completeness control.

Complete extraction is governed by:

1. follow Bundle.link[next] exactly as supplied by CMS;
2. continue until no next link remains;
3. reconcile raw target-resource count to unique resource keys;
4. reject unexplained cross-page duplicates;
5. retain source warnings in the run manifest.

## Data Treatment

No source value is rewritten to force Bundle.total to equal the cross-page
resource count.

The discrepancy remains visible as governed source evidence.

## Downstream Impact

Warehouse and analytical layers must use the actual successfully ingested
resource population.

They must not infer missing records merely from this observed Bundle.total
behavior.

This exception must be re-reviewed if CMS changes the v3 Sandbox pagination
behavior or authoritative documentation.
