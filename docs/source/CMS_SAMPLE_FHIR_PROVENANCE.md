# CMS Blue Button Synthetic FHIR Fixture Provenance

## Purpose

The FHIR files in `data/source_reference/cms_sample_fhir/` are retained as small source-reference fixtures for ingestion, schema, terminology and transformation validation.

They are **not real Medicare beneficiary data** and must never be described as such.

## Local evidence

The validated local fixtures contain the expected FHIR resource families:

- `Patient`
- `Coverage`
- `ExplanationOfBenefit`

The Patient fixture uses a negative numeric resource identifier. CMS documentation explicitly identifies negative Patient IDs as a synthetic-data behavior.

The Coverage and ExplanationOfBenefit fixtures contain references to the CMS Blue Button sandbox domain.

The project validation record also identifies `bbuser29999` as the sample source context used for these local fixtures.

## CMS provenance

Current CMS Blue Button documentation states that:

- the developer sandbox provides synthetic Medicare enrollee data;
- developers authenticate with synthetic sandbox users;
- downloadable sample data contain a Patient resource, an ExplanationOfBenefit bundle and a Coverage bundle;
- synthetic records are realistic-but-not-real data and are not tied to real patients.

Authoritative CMS references:

- https://bluebutton.cms.gov/api-documentation/explore-the-api/
- https://bluebutton.cms.gov/api-documentation/developer-sandbox/
- https://bluebutton.cms.gov/api-documentation/calling-the-api/
- https://bluebutton.cms.gov/data/understanding-the-data/

Historical CMS sample-client material also used `BBUser29999` as a sample beneficiary account. That historical account reference is supporting provenance evidence only; it is not treated as a current credential contract.

## Security boundary

The public fixtures do not contain this project's OAuth client secret, access token, refresh token or private `.env` values.

The full synthetic-user credential matrix is intentionally excluded from the public repository even though the accounts are synthetic.

## Analytical boundary

These fixtures are used only for reproducible engineering demonstrations.

They do not represent:

- real patients;
- real clinical histories;
- real Medicare beneficiary outcomes;
- a representative population sample;
- production claims volume;
- production OAuth credentials.

The governed portfolio analytical snapshot remains separately identified by its pipeline-run contract.
