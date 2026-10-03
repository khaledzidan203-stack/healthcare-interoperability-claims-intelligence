# Release validation evidence

Status: RELEASE. Review date: **2026-10-03 (Asia/Riyadh)**.

## Evidence hierarchy

Latest validated implementation > current source artifacts > current validation evidence > release documentation > historical checkpoints. Historical CSV/Markdown reports refer to their recorded runs; none is reused as a current-run database attestation.

## Independently observed source checks

| Check | Result / evidence |
|---|---|
| Regression | PASS: 94/94 tests in 14 modules, Python 3.13; no live services required. |
| Python | PASS: syntax and import checks; 17 modules, 70 top-level functions, 13 classes. No external runtime imports. |
| CLI | `validate-config` and `ingest` only. Requested `validate --help` failed as an invalid command; setup corrected to real interface. |
| SQL | Five canonical scripts. 40 CREATE TABLE, 4 CREATE SCHEMA, 27 CREATE INDEX and 2 CREATE UNIQUE INDEX statements. SQL execution/database state not revalidated. |
| Semantic source | 22 business tables plus `_Measures`, 9 governed measures, 50 relationships; 45 active/default and 5 explicitly inactive. Coverage excluded. |
| Report source | 7 pages, 77 visuals, every page 1920 × 1080 / FitToPage. |
| Run filter | Hidden and locked report filter selects exactly `snapshot_20261001_portfolio_4patients_v1`; nine measures require one run. |
| Financial measures | Three restricted primitives retain run/concept/currency guards; no consolidated financial KPI claim. |
| Curated sources | All six SHA-256 values match the existing public source manifest; fixture JSON parses. |
| Screenshots | All seven PNG files inspected visually and retained unchanged. Screenshot pixel sizes differ from the report canvas size, as expected for captures. |
| Security | Public-candidate scan and ignore-policy probes; private `.env` and excluded credential matrix contents not opened. Exact existing dummy test sentinels are narrowly allowlisted by hash/file. |
| Documentation | Release entry points created; old checkpoint prose marked HISTORICAL; one personal absolute path replaced with a project-relative description. |

## Page inventory

| Page | Page ID | Visuals |
|---|---|---:|
| INDEX | `6d04c910ec0a42270c1a` | 8 |
| Executive Overview | `e470b425b32f9bdc7a16` | 14 |
| Claims Activity | `93a77f48dcca84f1a64d` | 11 |
| Clinical & Coding | `363f4c4b16ab4c25de1d` | 10 |
| Provider & Payer | `45f44dd944255de928e4` | 10 |
| Terminology & Governance | `20908086e6ada0788299` | 10 |
| Methodology & Validation | `5966bf7edfc1090b40fb` | 14 |

## Bounded snapshot evidence

The Executive Overview screenshot displays 24 claims, 87 items, 98 diagnosis occurrences, 12 procedure occurrences, 72 care-team occurrences and 460 supporting-info occurrences. Its narrative and the Methodology screenshot state 4 patients. Methodology identifies the same governed run as the current report filter.

These counts are verified as displayed presentation evidence, not freshly recomputed from PostgreSQL. Private RAW/STAGING/processed directories denied access. No attempt was made to alter permissions, combine older runs, read cached ABF contents or query/mutate PostgreSQL. Historical DQ CSV files describe earlier runs and cannot independently certify this snapshot. Screenshot DQ narratives are retained as prior evidence, not republished as new database-test results.

## PBIR and Desktop boundary

The attempted command was `powerbi-report-author validate "powerbi/HealthcareInteroperabilityClaims.Report"`. PowerShell returned exit 1 and `PSSecurityException` because script execution is disabled. The validator itself did not run. **Fresh PBIR validation: BLOCKED.** No security-policy bypass or alternate launcher was attempted.

The supplied prior validation contract reports exit 0, zero errors and one `PBIR_SCHEMA_UNREACHABLE` warning. The screenshot also records prior zero structural errors. That history is not fresh verification. The warning means the remote schema endpoint was unreachable; it is not a structural error and limits schema coverage. Preserve it explicitly in future evidence if it recurs.

No fresh Desktop opening, refresh or interaction check was performed. The owner explicitly attests the approved Desktop baseline and authorizes carry-forward only after byte-identity proof.

The prior turn's actual in-session SHA-256 inventory was retained and compared again before publication. All **170 protected files** match, including the complete **121-file Power BI source tree** and **seven screenshots**, with no added or removed protected artifacts. The original hashes are now persisted in [RELEASE_PRESERVATION_BASELINE.json](RELEASE_PRESERVATION_BASELINE.json), and the auditor compares both path sets and hashes on every run. `.gitattributes` disables newline conversion so Git checkout preserves those exact bytes.

Evidence provenance: the original successful PBIR execution and Desktop approval are owner-attested; their execution was not independently observed in these release turns. Byte identity from the release-entry baseline through publication is independently verified. The hash inventory was captured during release preparation, not emitted by the earlier validator. No claim is made that hashes alone prove runtime behavior.

```text
PBIR_VALIDATION_STATE=CARRIED_FORWARD_FROM_BYTE_IDENTICAL_VALIDATED_BASELINE
PBIR_FRESH_RERUN=BLOCKED_BY_LOCAL_POLICY
PBIR_RELEASE_GATE=PASS_WITH_PRESERVED_VALIDATION_EVIDENCE
DESKTOP_VISUAL_VALIDATION=CARRIED_FORWARD_FROM_APPROVED_BASELINE
```

These gates use the owner's explicit carry-forward authorization plus the preserved baseline; they do not suppress the prior schema-reachability warning. Any protected-source change invalidates this preservation gate.

## Publication and preservation

No `.env` values, credentials, database state, source transformations, SQL, tests, DAX, relationships, filters, visuals, curated fixture bytes or screenshot bytes were intentionally changed. Final SHA-256 comparison confirmed all 170 protected source/test/SQL/Power BI/fixture/screenshot artifacts are byte-for-byte unchanged; no protected artifacts were added. Historical documentation was retained, not deleted. No new backup or temporary sidecar files were created inside the repository.

Runtime RAW/STAGING/processed data, the full synthetic-user matrix, `.pbi`, ABF and bytecode remain local via ignore rules. Public source scan is heuristic, not a proof against every possible secret. Markdown checks validate local file/image destinations; external URL uptime and heading anchors are not comprehensively validated.

## Final audit record

Final source auditor: **PASS**, exit 0, zero failing checks. It ran **94/94 pipeline regression tests plus 7/7 auditor boundary tests**. Python syntax/imports, public JSON, source hashes, report/model counts, publication probes and all local Markdown/image destinations passed. No secret-pattern findings, personal absolute paths or unwanted public backup/sidecar artifacts were found. The synchronized publication inventory contains **266 eligible public files** and **11 observed excluded boundaries (including Git metadata)**. Ignored directory contents are grouped, not individually counted.

The optional `--pbir` audit returned exit 1 with static PASS and PBIR BLOCKED; this is the expected fail-closed local gate when execution policy rejects the normal launcher. No remote-schema warning was generated in this attempt because the validator never ran.

GitHub Actions **PASS**: [run 37140006407](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence/actions/runs/37140006407) ran the source auditor successfully on Ubuntu/Python 3.13 for initial commit `0322bb2f56290a875d32c69628a7662b1b4e438e`. This includes the 94 pipeline and seven auditor tests. Later documentation commits are separately validated by the [live workflow](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence/actions/workflows/ci.yml); the release process requires green CI at the exact tag target.

Git is initialized on `main`, with **266 tracked public files**. Actual ignore probes, inventory parity and index-mode/blob comparisons pass. Staged bytes match the scanned working tree, including every protected baseline hash. MIT licensing and separate third-party notices are present.

**RELEASE VALIDATION STATUS: PASS - preserved runtime evidence, fresh source/index checks and successful hosted CI.**

`READY_FOR_GITHUB_PUBLICATION=YES`

The owner explicitly authorized Git initialization, public repository creation under `khaledzidan203-stack`, pushing, CI remediation, tagging and the v1.0.0 release. The active account was independently confirmed; the target repository was absent before creation. Git inclusion/index checks and initial hosted/remote verification passed. Final tag and release metadata are verified after the last documentation commit; consult the actual GitHub release for its immutable commit target. See [checklist](RELEASE_CHECKLIST.md) and [publication plan](PUBLICATION_PLAN.md).


## Publication inventory delta

The original 261 candidates increase to **266**: `LICENSE`, `THIRD_PARTY_NOTICES.md`, `.gitattributes`, `docs/validation/RELEASE_PRESERVATION_BASELINE.json` and `docs/validation/RELEASE_NOTES_v1.0.0.md`. No runtime dataset was added. Git metadata is never a public file. The auditor now checks actual index blob bytes against the scanned working tree whenever the index is populated.


## Release-only portability correction

Real Git inspection found Windows text-mode stdin translated newline-delimited ignore probes to CRLF, causing Git to interpret carriage returns as part of filenames. The auditor now uses NUL-delimited binary input/output with `git check-ignore -z --stdin`. The existing boundary test also verifies actual Git results when a repository is present. All 94 pipeline and seven auditor tests pass; no validated pipeline or Power BI source changed.


## Remote publication evidence

- [Repository](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence): owner `khaledzidan203-stack`, public, default branch `main`, requested description and 19 factual topics.
- Initial push succeeded; remote recursive tree contains exactly the 266 paths and Git blob IDs from the audited local commit. This establishes that no excluded runtime/credential artifact appeared remotely. Empty `.gitkeep` placeholders are the only public entries under local runtime/log directories.
- GitHub's rendered README HTML was inspected: headings, documentation links and seven screenshot references are present. All seven PNGs fetched from GitHub match the preserved SHA-256 values. Primary relative destinations are verified against the same remote tree.
- LICENSE, SECURITY, THIRD_PARTY_NOTICES and setup documentation are present remotely; source references are exactly the approved six files.
- Browser inventory was empty, so this is server-rendered HTML/API verification, not a new browser visual-layout session. The original screenshot visual review remains preserved evidence.
- The original hosted workflow passed without CI failures. The only portability fix was the pre-push Windows Git stdin correction documented above.
- [v1.0.0 release notes](RELEASE_NOTES_v1.0.0.md) explicitly retain the synthetic-data, financial, terminology, Coverage and runtime-evidence limits. The annotated tag/release are created only after final clean-tree and matching-main checks.
