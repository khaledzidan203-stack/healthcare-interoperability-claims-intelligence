# Security policy

Status: CURRENT / RELEASE.

This repository is limited to CMS sandbox/synthetic engineering examples. Do not ingest, commit, attach or screenshot real patient data for this portfolio. Synthetic fixtures are not real Medicare beneficiary records.

## Credentials and OAuth

Keep credentials only in local `.env`; use `.env.example` for empty credential fields and public configuration. Never place credentials in code, CLI arguments, screenshots, logs or issue reports. Do not force-add `.env`. Test secrets must be unmistakable dummy values.

The OAuth implementation generates PKCE S256 and state values, validates returned state and scopes, and suppresses callback request logging. Token fields are excluded from dataclass representations. Access and refresh tokens are held in memory; persistence records scope and expiry metadata rather than token values. This boundary does not establish that arbitrary OS memory or third-party exception output is secret-proof. Redact diagnostics before sharing.

Use only the configured CMS sandbox host for portfolio ingestion. Configuration validates HTTPS but does not enforce a sandbox hostname allowlist; verify the base URL. No production credentials belong here.

## Publication boundary

`.gitignore` excludes `.env` variants, credentials/key files, OAuth artifacts, RAW/STAGING/processed data, Power BI `.pbi` state, ABF/PBIX/PBIT caches, Python bytecode, environments and logs. Empty `.gitkeep` placeholders may be public. The full synthetic username/password matrix remains local. See [publication inventory](docs/validation/PUBLICATION_INVENTORY.csv).

Only the six curated files in the [source manifest](docs/source/PUBLIC_SOURCE_MANIFEST.md) are intended public data inputs. Hashes establish artifact identity; they do not independently prove redistribution rights or absence of all sensitive content.

Run `python -B scripts/release/release_audit.py` before staging. It reads public candidates only and reports finding locations without credential values. Pattern scans and screenshot review cannot prove absence of every possible secret. Ignore rules do not remove tracked files: inspect the index before committing.

## Reporting and response

Do not put secrets or patient details in public issues. Send a minimal redacted report through an owner-approved private channel; use GitHub private vulnerability reporting if enabled after publication. No monitored mailbox or response-time guarantee is configured. Non-sensitive reproduction steps may be shared only after removing identifiers and credentials.

If a credential is exposed, stop publication, revoke/rotate it at the issuer, inspect exposure and history, and obtain approval for any history rewrite. Deleting a line does not invalidate a leaked credential. Windows security restrictions remain enabled; blocked execution is an unresolved gate, not a reason to use a bypass.
