# Publication plan

Status: RELEASE / explicitly authorized by the owner. Publication results are recorded in [release evidence](RELEASE_VALIDATION_EVIDENCE.md).

## Authorized target

- Owner: `khaledzidan203-stack`; never use the inactive account.
- Repository: `healthcare-interoperability-claims-intelligence`.
- Visibility: public; default branch: `main`.
- [Repository](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence).
- Original work: [MIT License](../../LICENSE), copyright 2026 Khaled Zidan.
- External material: [third-party notices](../../THIRD_PARTY_NOTICES.md); no speculative third-party license grant.

## Inclusion and preservation

[PUBLICATION_INVENTORY.csv](PUBLICATION_INVENTORY.csv) contains 266 public candidates, five more than the preceding release-preparation inventory: license, notices, Git byte-preservation attributes, protected baseline hashes and release notes. Print the current set with `python -B scripts/release/release_audit.py --inventory`.

Public: source/tests, SQL, curated attributed CMS inputs, Power BI source, seven screenshots, historical records with notices, release docs, auditor and CI. Excluded: `.env`, credentials, full synthetic-user matrix, RAW/STAGING/processed data, logs, `.pbi`, ABF/PBIX/PBIT, environments and bytecode. Restricted directory contents are grouped, not enumerated. No deletion is proposed.

## Execution sequence

1. Confirm GitHub identity and target-repository absence; never replace an unrelated repository.
2. Pass source audit and owner-authorized preserved PBIR/Desktop gates. Verify all 170 protected hashes.
3. Initialize `main`, check actual Git ignore results against the inventory, then stage.
4. Re-audit the index: exact paths, modes and blob bytes must match scanned public files.
5. Commit: `feat: publish healthcare interoperability claims intelligence platform`.
6. Create the authorized public repository, configure only its `origin`, set factual topics and push `main`.
7. Inspect actual remote tree, README/images, license/notices, exclusions and hosted CI. Correct only demonstrated release/CI defects.
8. Confirm clean matching local/remote main, repeat final tests/audit, create and push annotated `v1.0.0`.
9. Publish the non-draft, non-prerelease [release](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence/releases/tag/v1.0.0) using [reviewed notes](RELEASE_NOTES_v1.0.0.md); verify remote metadata/tag/release.

Description: Production-style healthcare interoperability and claims analytics engineering portfolio using CMS Blue Button synthetic FHIR data, PostgreSQL, data governance, and Power BI PBIR.

Topics cover healthcare, FHIR, OAuth/PKCE, claims analytics, data/analytics engineering, governance/DQ, PostgreSQL, Power BI/DAX/TMDL/PBIR, Python and portfolio work. No production or real-patient claims are authorized.

PBIR validation is carried forward only from the owner-attested successful baseline with complete byte identity. Fresh rerun remains blocked by local security policy. No bypass, database mutation, source redesign or private-data publication is part of this process.
