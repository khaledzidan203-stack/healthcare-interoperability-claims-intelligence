# Secrets and Credential Policy

## Purpose

Protect CMS Blue Button OAuth credentials, access tokens, refresh tokens,
and other security-sensitive material throughout the project lifecycle.

## Classification

The following are classified as SECRET:

- CMS Blue Button Client Secret
- OAuth access token
- OAuth refresh token
- authorization codes
- private keys
- passwords
- credential-bearing environment variables

Client ID is not treated as a password, but it should still be managed
through project configuration rather than hard-coded throughout source files.

## Storage Rule

Real credentials must exist only in local secret configuration such as:

`.env`

The real `.env` file is excluded from Git.

Only:

`.env.example`

may be committed.

`.env.example` must never contain real credentials or tokens.

## Output Rule

Validation scripts must never print:

- Client Secret
- access token
- refresh token
- authorization code
- beneficiary password

Validation output may report only safe states such as:

- credential variable present: YES / NO
- token request status
- HTTP status
- token expiration metadata
- granted scopes

## Git Rule

Before every GitHub release or major commit, the repository must be checked
for accidental credentials.

No secret may be committed even if it is later deleted from the working tree,
because Git history may retain it.

## Screenshot Rule

Credentials and tokens must never appear in:

- screenshots
- README images
- portfolio documentation
- Power BI screenshots
- terminal captures

## Raw Data Rule

Future live Sandbox API responses are synthetic, but RAW extracts remain
local by default until publication suitability is explicitly reviewed.

## OAuth Design

The project will use CMS-supported OAuth authorization behavior and PKCE
where applicable.

The final API version and endpoint configuration will be locked only after
live Sandbox validation.

## Incident Rule

If a Client Secret or token is accidentally exposed:

1. stop using the exposed credential;
2. rotate or regenerate it in the CMS Sandbox;
3. remove it from the working tree;
4. inspect Git history;
5. document the security exception without recording the secret itself.
