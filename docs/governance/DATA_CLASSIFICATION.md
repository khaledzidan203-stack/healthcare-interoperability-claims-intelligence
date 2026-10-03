# Data Classification

## PUBLIC_REFERENCE

Official public technical reference material.

Examples:

- CMS v3 data dictionary
- Blue Button system listing
- official CMS sample files

## SYNTHETIC_TEST_DATA

Synthetic beneficiary-like and claims-like developer data.

Examples:

- synthetic-user catalog
- Patient sample
- Coverage sample
- ExplanationOfBenefit sample
- future Sandbox API extracts

Rules:

- never describe as real patient data
- maintain source traceability
- publish only after repository review

## SECRET

Authentication and credential material.

Examples:

- client secret
- access token
- refresh token
- private key
- password
- credential-bearing .env values

Rules:

- never commit to Git
- never place in documentation
- never print in validation output
- never include in screenshots
- never persist in public logs

## DERIVED_ANALYTICAL_DATA

Data produced from source resources.

Examples:

- staging tables
- normalized relational structures
- warehouse facts and dimensions
- reconciliation extracts
- semantic-model outputs

Derived data must retain lineage to the source layer.

## Current Privacy Position

Only synthetic CMS developer data is approved for this portfolio project.

No real beneficiary health information is approved.
