# Third-party notices

The [MIT License](LICENSE), copyright 2026 Khaled Zidan, applies to this project's original code and documentation. It does not relicense third-party material beyond the rights available from its original source.

## CMS Blue Button references and synthetic samples

The six approved reference/sample artifacts retain CMS Blue Button source attribution and provenance. Their exact paths and SHA-256 values appear in the [public source manifest](docs/source/PUBLIC_SOURCE_MANIFEST.md); the [fixture provenance record](docs/source/CMS_SAMPLE_FHIR_PROVENANCE.md) explains their synthetic/sample context.

- `data/source_reference/cms_reference/bluebutton_system_listing.csv`
- `data/source_reference/cms_reference/v3-data-dictionary-2.248.0.csv`
- `data/source_reference/cms_sample_fhir/patient_bbuser29999.json`
- `data/source_reference/cms_sample_fhir/coverage_bundle_bbuser29999.json`
- `data/source_reference/cms_sample_fhir/eob_bundle_bbuser29999.json`
- `data/source_reference/cms_sample_fhir/readme.txt`

These FHIR fixtures support reproducibility and engineering demonstration. They are CMS synthetic/sample data, not real Medicare beneficiary data. The dictionary is pinned to historical build `2.248.0`; it is not represented as the latest version. Inclusion does not imply CMS endorsement or ownership of CMS material by this project.

Sources: [CMS Explore the API](https://bluebutton.cms.gov/api-documentation/explore-the-api/), [Developer Sandbox](https://bluebutton.cms.gov/api-documentation/developer-sandbox/), [Calling the API](https://bluebutton.cms.gov/api-documentation/calling-the-api/) and [Understanding the Data](https://bluebutton.cms.gov/data/understanding-the-data/).

The local provenance evidence does not identify a specific third-party software license for these artifacts. This notice therefore records attribution without inventing a license or expanding redistribution rights. Consult the original source for applicable terms.

## Power BI generated resources

The report includes a Power BI generated Fluent base-theme resource under `powerbi/HealthcareInteroperabilityClaims.Report/StaticResources/SharedResources/BaseThemes/`. It is retained as part of the existing report definition, without claiming original authorship or a separate MIT grant over Microsoft material. Microsoft and Power BI names identify the tools/formats used; no endorsement is implied.

## CI tooling

The CI workflow references `actions/checkout` and `actions/setup-python`. Those external tools are downloaded by GitHub Actions under their own terms; their code is not bundled into this repository. Python, PostgreSQL and Power BI are separate prerequisites, not relicensed by the project.
