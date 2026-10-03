# Release checklist

Status: RELEASE. Review date: 2026-10-03. Source PASS is not publication approval.

- [x] Inspect Python, SQL, tests, TMDL, PBIR, references and seven screenshots.
- [x] Re-run 94 tests and check syntax/imports without bytecode writes.
- [x] Verify five SQL files; document prerequisites and historical promotion scope.
- [x] Preserve 22 business tables, 9 measures, 50 relationships, 7 pages and 77 visuals.
- [x] Preserve report filter, financial restrictions and Coverage exclusion.
- [x] Verify six curated fixture SHA-256 values against the manifest.
- [x] Label historical documentation and remove personal absolute paths.
- [x] Complete final auditor with zero static failures: 94 pipeline tests and 7 auditor tests pass; 266 public candidates inventoried after five authorized release additions.
- [x] Carry forward owner-attested PBIR validation after proving complete baseline byte identity; preserve `PBIR_SCHEMA_UNREACHABLE` and document that fresh rerun is blocked by policy.
- [x] Carry forward the owner-approved Desktop baseline after verifying all report/model source and screenshots unchanged; no fresh Desktop session claimed.
- [x] Owner selected MIT; LICENSE and separate third-party notices are present.
- [x] Initialize main, verify actual ignore behavior, inspect all 266 staged paths and blob bytes, and re-run audit.
- [x] Authorized push and hosted source CI passed: run 37140006407. Final tag target must also have green CI.
- [x] Owner explicitly authorized public repository creation, push, CI fixes, tagging and GitHub Release under the specified account.

No database mutation or security-control bypass is part of these gates. If private data cannot be recounted, retain the screenshot qualification. The inclusion inventory has been checked against actual Git and the remote tree. The final tag/release process requires a clean worktree, matching local/remote main and a green run for the exact tag target.
