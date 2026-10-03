# Setup and reproducibility

Status: CURRENT / RELEASE. Commands reflect the implemented argparse interface.

## Prerequisites

Use Python 3.13, Git for eventual staging, and an approved PostgreSQL installation for database work. The historical database checkpoint records PostgreSQL 17.11; this audit did not reconnect or validate server compatibility. Power BI Desktop with PBIP/PBIR support is needed for interactive review. `powerbi-report-author` is a local validation tool, not a Python dependency.

Runtime imports are standard-library imports. `requirements.txt` has no active requirements. The project uses `PYTHONPATH=src`; no packaging installation is required.

## Source-only checks

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m healthcare_claims --help
python -B -m healthcare_claims validate-config --help
python -B -m healthcare_claims ingest --help
python -B -m unittest discover -s tests
python -B scripts/release/release_audit.py
python -B scripts/release/release_audit.py --inventory
```

On POSIX set `export PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1` first. Tests need no live OAuth or PostgreSQL. Existing tests use isolated system temporary directories; the auditor does not write source, bytecode, database state or report artifacts.

## Sandbox configuration

Create `.env` only if it does not already exist:

```powershell
if (-not (Test-Path -LiteralPath '.env')) {
    Copy-Item -LiteralPath '.env.example' -Destination '.env'
}
```

Populate client ID and secret privately. Keep `CMS_BLUEBUTTON_API_VERSION=v3`, the sandbox HTTPS base URL, and an HTTP loopback callback such as `http://localhost:8080/callback` registered with the application. The parser reads `KEY=value` directly: use unquoted values. Never print the file.

The application requests Patient, Coverage and ExplanationOfBenefit read/search scopes and fails if required scopes are absent. Follow [CMS sandbox registration](https://bluebutton.cms.gov/api-documentation/developer-sandbox/).

```powershell
python -B -m healthcare_claims validate-config --project-root .
python -B -m healthcare_claims ingest --project-root . --user-label portfolio-sandbox-user --page-size 50
```

`--user-label` is metadata, never a password. Page size is 1–50, default 50. The only commands are `validate-config` and `ingest`; no `validate` command exists. Ingestion opens interactive authorization and writes a new RAW run. It needs access to the sibling `output` directory used by `storage.py` before moving a completed run into RAW. No live ingestion was performed during this audit.

The CLI does not expose a complete staging-to-warehouse workflow. Transformation, normalization, bundle generation, transaction rendering and post-load checks are Python module APIs. Review their signatures in [source](../src/healthcare_claims) and [architecture](architecture/RELEASE_ARCHITECTURE.md). Historical execution records do not certify a new run.

## PostgreSQL sequence and gates

Review scripts in this order. Do not execute them blindly on an existing database.

| Order | Script | Preconditions and effect |
|---|---|---|
| 1 | `sql/01_create_foundation.sql` | Creates governance/STAGING structures and reserves analytics schema; DDL mutation. |
| 2 | `sql/02_harden_multirun_staging.sql` | Requires empty STAGING; hardens multirun keys before loading. |
| 3 | `sql/03_analytical_model_discovery.sql` | Read-only profiling of populated STAGING; requires psql variable `pipeline_run_id`. |
| 4 | `sql/04_create_analytics_model.sql` | Creates analytics tables/constraints; loading is a separate governed step. |
| 5 | `sql/05_promote_analytics_dq_validated.sql` | Historical mutating promotion for `run_20260930T084004Z_ingest_2db2ed86`, not a generic installer or promotion of the portfolio snapshot. Requires passed DQ and expected prior status. |

The loader renders a transaction with reconciliation. Post-load checks must pass before status promotion. Never combine runs or reuse historical counts to certify a new run. Do not execute script 5 for a new snapshot without an explicitly reviewed change.

`psql.exe` was previously blocked by Windows Application Control. This workflow does not launch it or bypass that control. Database deployment/recount needs an authorized environment under a separate task. No fresh database execution is claimed.

## Power BI

Open [HealthcareInteroperabilityClaims.pbip](../powerbi/HealthcareInteroperabilityClaims.pbip) in an approved Desktop environment. The model imports from PostgreSQL `localhost`, database `healthcare_interoperability_claims`; supply credentials locally, never in source. The public checkout omits caches and private datasets, so source alone cannot reproduce populated screenshots.

Preserve the hidden locked filter for `snapshot_20261001_portfolio_4patients_v1`, DAX guards, single-direction relationships and Coverage exclusion. Refresh only against the intended dataset. Review all pages, slicers, navigation and restricted measures after refresh.

Local validation command, where policy permits:

```powershell
powerbi-report-author validate "powerbi/HealthcareInteroperabilityClaims.Report"
```

The auditor also accepts `--pbir` to attempt this normal launcher and returns nonzero when the local gate is blocked or needs diagnostic review. It does not bypass execution policy.

This workstation rejected the PowerShell entry point because scripts are disabled. No alternate launcher or policy bypass was attempted. Fresh PBIR validation is blocked. Prior supplied evidence reports exit 0, zero errors and one `PBIR_SCHEMA_UNREACHABLE` warning; record it explicitly if it recurs. Static JSON checks do not validate remote schemas or Desktop runtime. For this release, the owner authorized carrying forward prior PBIR/Desktop validation after byte-identity verification. The permanent preservation manifest covers all 121 Power BI source files and seven screenshots; it identifies the original validation as owner-attested, not a fresh run.

CI runs source gates on Python 3.13 without credentials, database or Desktop. Consult the [workflow runs](https://github.com/khaledzidan203-stack/healthcare-interoperability-claims-intelligence/actions/workflows/ci.yml) and [release evidence](validation/RELEASE_VALIDATION_EVIDENCE.md) for hosted results and evidence boundaries.
