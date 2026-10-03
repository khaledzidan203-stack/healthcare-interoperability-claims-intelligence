# Healthcare Interoperability & Claims Intelligence Platform v1.0.0

This is a portfolio-scale, production-style engineering implementation using CMS synthetic/sandbox data. It is not a production Medicare claims-processing system and does not use real Medicare beneficiary data.

- CMS Blue Button FHIR ingestion for Patient, Coverage and ExplanationOfBenefit using OAuth 2.0 Authorization Code + PKCE S256.
- Governed RAW/STAGING architecture with pagination checks, source hashes, reference normalization and terminology/financial-grain controls.
- PostgreSQL analytical model and transactional load/post-load reconciliation contracts.
- 94-test pipeline suite, seven release-auditor tests and reproducible GitHub Actions source checks.
- Power BI semantic source: 22 business tables, nine governed measures and 50 relationships.
- Seven-page, 77-visual PBIR report with seven original Desktop screenshots and a preserved governed-run filter.
- MIT-licensed original work, separate third-party notices and a curated synthetic-source publication boundary.

PBIR validation and Desktop visual review are carried forward from the owner-attested approved baseline after complete source/screenshot SHA-256 identity verification. They are not fresh runtime sessions. The prior PBIR result was exit 0, zero errors and one `PBIR_SCHEMA_UNREACHABLE` warning; fresh rerun remains blocked by local security policy.

The bounded snapshot shows four patients, 24 claims, 87 items, 98 diagnosis occurrences, 12 procedure occurrences, 72 care-team occurrences and 460 supporting-info occurrences. These are preserved snapshot evidence, not a fresh database recount or population statistics.

Limitations: private runtime data and caches are excluded; clinical mappings may remain pending; Coverage is excluded from semantic relationships; financial measures are restricted primitives, not consolidated financial KPIs. Source CI does not execute PostgreSQL, Power BI Desktop or fresh PBIR validation.
