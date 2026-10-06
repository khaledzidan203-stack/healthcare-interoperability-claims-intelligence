# Portfolio Demo Walkthrough — 60–90 seconds

This script is designed for recruiter screens, interviews and LinkedIn/GitHub walkthroughs. It is presentation-only documentation and does not change the validated project implementation.

## 0–10 sec — What the project is

This is a production-style healthcare interoperability and claims analytics project built on CMS Blue Button synthetic FHIR data. The goal is to convert nested healthcare resources into governed, traceable analytical facts that can be validated and consumed in Power BI.

## 10–25 sec — Why the problem is hard

FHIR claims are not naturally analytics-ready. Claims, items, diagnoses, procedures, care-team participants, supporting information and financial elements live at different grains. Flattening them carelessly can create duplicate counts, invalid joins and misleading totals.

## 25–45 sec — Architecture

The pipeline uses OAuth 2.0 with PKCE to retrieve Patient, Coverage and ExplanationOfBenefit resources. Data is persisted with run identity and hashes, transformed into canonical staging structures, normalized, validated and promoted into a PostgreSQL analytical model. The semantic model is defined in TMDL and consumed through a source-controlled PBIR Power BI report.

## 45–65 sec — Dashboard

Start on Executive Overview to show governed claim activity for one selected run. Move to Claims Activity for trends and source categories, then Clinical & Coding to show diagnosis/procedure occurrences and terminology-mapping state. Provider & Payer demonstrates how source identity and missing display information are handled without inventing data. Terminology & Governance shows unresolved mapping states and review controls.

## 65–80 sec — Engineering quality

The project includes 94 regression tests, a release auditor and GitHub Actions validation. It also preserves lineage, run isolation, source uncertainty and explicit evidence boundaries so analytical claims remain reviewable.

## 80–90 sec — Close

The main value of the project is not just the dashboard. It demonstrates end-to-end analytics engineering across interoperability, dimensional modeling, data quality, governance, PostgreSQL, Power BI and CI while keeping the analytical logic reproducible and source-controlled.

## Suggested recording order

1. Repository README title and recruiter quick scan.
2. Mermaid architecture diagram.
3. Executive Overview screenshot/report page.
4. Claims Activity.
5. Clinical & Coding.
6. Provider & Payer.
7. Terminology & Governance.
8. GitHub Actions badge / validation section.

## Recording notes

- Keep the final video between 60 and 90 seconds.
- Do not present sandbox/synthetic data as real patient or production CMS data.
- Do not describe restricted financial primitives as consolidated financial KPIs.
- Avoid showing private `.env`, runtime data, credentials or local caches.
- Prefer one concise sentence per screen; the GitHub repository contains the detailed evidence for technical reviewers.
