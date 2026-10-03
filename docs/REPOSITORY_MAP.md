# Repository map

Status: CURRENT / RELEASE.

| Location | Classification | Interpretation |
|---|---|---|
| `src/healthcare_claims/` | CURRENT | Executable pipeline and analytical contracts. |
| `sql/` | CURRENT source; script 05 HISTORICAL run scope | Foundation, hardening, discovery, DDL and run-specific promotion; read setup preconditions. |
| `tests/` | TESTING | 14 regression modules; dummy credentials only. |
| `powerbi/` excluding caches | POWER BI SOURCE | PBIP/PBIR and semantic TMDL. |
| `screen_shot/` | PORTFOLIO | Seven original supplied screenshots. |
| `scripts/release/`, `.github/workflows/` | RELEASE | Auditor and source CI; no live-data or Desktop gate. |
| `data/source_reference/cms_reference/` | PUBLIC SOURCE REFERENCE | Attributed CMS listing and pinned dictionary. |
| `data/source_reference/cms_sample_fhir/` | PUBLIC SOURCE REFERENCE | Synthetic/sample fixtures and original source note. |
| `.env`, runtime data, logs, caches | LOCAL ONLY / LOCAL-EVIDENCE | Excluded; no deletion performed. |
| `docs/source/PUBLIC_SOURCE_MANIFEST.md`, `CMS_SAMPLE_FHIR_PROVENANCE.md` | CURRENT | Source boundaries and attribution. |
| `docs/security/`, `docs/governance/`, `SECURITY.md` | CURRENT policy | Data and credential policy. |
| New `RELEASE_*`, `PUBLICATION_*`, setup/map/decisions/gallery/case study | RELEASE / PORTFOLIO | Current entry points and bounded audit evidence. |
| Earlier checkpoint/design Markdown and CSV in `docs/` | HISTORICAL | Original design and run-specific evidence; may describe earlier states/populations. |
| `PROJECT_INDEX.md`, `CHANGELOG.md` | HISTORICAL / SUPERSEDED as landing pages | Checkpoint history retained with notices; start at README. |
| `config/` | CURRENT reserved folder | No active configuration contract; `.env.example` and `config.py` define it. |

Historical current/pending/approved labels apply to their original checkpoint. CSV contracts inform review, but current source and validation take precedence. The old snapshot policy names an earlier run and cannot override the current report filter.

[Publication inventory](validation/PUBLICATION_INVENTORY.csv) lists every eligible file and excluded boundary. Excluded directories are wildcard groups because access restrictions prevent reliable enumeration. No file is selected for removal. Preexisting ignored caches remain local; no new backup or sidecar artifact is part of this release.
