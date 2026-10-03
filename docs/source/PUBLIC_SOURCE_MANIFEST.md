# Public Source Manifest

This document defines the source-reference artifacts intentionally eligible for the public portfolio release.

## Publication boundary

- Real OAuth credentials, access tokens, refresh tokens and the local `.env` are excluded.
- Runtime RAW, STAGING and generated processed data are excluded from the public repository.
- The complete CMS synthetic-user username/password matrix is retained locally but excluded from publication.
- Published FHIR fixtures are treated strictly as CMS synthetic/sample data and must not be described as real Medicare beneficiary data.

## Public source-reference artifacts

| Artifact | Release classification | SHA-256 | Purpose |
|---|---|---|---|
| `data/source_reference/cms_reference/bluebutton_system_listing.csv` | `KEEP_WITH_ATTRIBUTION` | `d1025a09a5127730d1dd93a25e4309e291d5757797396c8d555a28a7394260b1` | CMS Blue Button reference metadata used during source discovery. |
| `data/source_reference/cms_reference/v3-data-dictionary-2.248.0.csv` | `KEEP_PINNED_BUILD_REFERENCE` | `6fe00eda96bb4a47e7b091be110be9c7b5d0ca1582e1017426004ecfac675445` | Pinned Blue Button v3 data-dictionary reference used by the validated build; not claimed as the latest CMS dictionary. |
| `data/source_reference/cms_sample_fhir/patient_bbuser29999.json` | `KEEP_SYNTHETIC_FIXTURE` | `c3fc6a235b019561ef84390667a579e3d17af95123a02ccd63ac3e32bb4107f4` | CMS Blue Button synthetic/sample Patient fixture used for schema and ingestion validation. |
| `data/source_reference/cms_sample_fhir/coverage_bundle_bbuser29999.json` | `KEEP_SYNTHETIC_FIXTURE` | `71ea316470bd2ebb70589252edec905260b37cac76bec953670afb862bff955d` | CMS Blue Button synthetic/sample Coverage bundle used for schema and ingestion validation. |
| `data/source_reference/cms_sample_fhir/eob_bundle_bbuser29999.json` | `KEEP_SYNTHETIC_FIXTURE` | `d94d0bce4e77593d22173c6516c08be787358ec8325cbdfff2750c61ef92cd81` | CMS Blue Button synthetic/sample ExplanationOfBenefit bundle used for schema and ingestion validation. |
| `data/source_reference/cms_sample_fhir/readme.txt` | `KEEP_ORIGINAL_SOURCE_NOTE` | `3e298c973e731bdf8e49032f931c10008ad2ec2d4a268f7e48c4de9095a137b7` | Original local source-reference note retained alongside the curated provenance documentation. |

## Excluded local source reference

- `data/source_reference/synthetic_users/synthetic_users_by_claim_count_full.csv` ? CMS synthetic sandbox credential matrix. It is synthetic, but publishing the complete username/password list adds no analytical value and creates unnecessary credential-like material in the repository.

## Authoritative external provenance

- CMS Blue Button API ? Explore the API: https://bluebutton.cms.gov/api-documentation/explore-the-api/
- CMS Blue Button API ? Developer Sandbox: https://bluebutton.cms.gov/api-documentation/developer-sandbox/
- CMS Blue Button API ? Calling the API: https://bluebutton.cms.gov/api-documentation/calling-the-api/
- CMS Blue Button API ? Understanding the Data: https://bluebutton.cms.gov/data/understanding-the-data/

CMS documentation describes the sandbox/sample dataset as synthetic Medicare enrollee data and documents Patient, ExplanationOfBenefit and Coverage resources for testing.

## Evidence boundary

These artifacts support reproducibility and schema understanding only. They do not establish production deployment, real-beneficiary analytics, clinical truth, population estimates or real financial outcomes.
