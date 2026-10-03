# Portfolio case study: making claims analytics traceable

Status: PORTFOLIO / RELEASE.

## Problem and constraints

FHIR claims are nested interoperability resources, not ready-made analytical rows. Repeated diagnoses, items, care-team participants, financial elements and references have distinct grains and identity semantics. Flattening them into one table can make counts and sums depend on accidental joins.

The project uses bounded CMS synthetic sandbox inputs. It cannot claim population representativeness, clinical truth or financial outcomes. Credentials and runtime extracts must stay private, while validated transformations and report behavior must survive release preparation unchanged.

## Architecture and decisions

The pipeline establishes extraction integrity through PKCE, state/scope checks, next-link traversal, unique resource accounting and hashed persistence. It transforms nested structures into canonical grains, normalizes references, then builds dimensions and separate facts. Transactional loading and reconciliation separate a generated bundle from an accepted analytical load.

Preserving grain is the key decision. Diagnosis occurrences answer a different question from claim counts. Missing payer display does not prove missing identity. Claim totals, claim adjudications and item adjudications cannot form a trusted KPI merely because each contains an amount.

## Difficult problems

**Pagination:** observed Bundle totals did not reliably reconcile with retrieved resources. The code follows validated next links and checks resource keys; discrepancies stay documented as source warnings.

**Identity:** contained, external and display-only references need different handling. Normalization preserves identity where supported and exposes unresolved cases. Coverage relationships remain gated rather than inferred from labels.

**Run isolation:** retained runs can duplicate business events if combined implicitly. Keys and DQ preserve lineage; the report adds a locked filter and measures return blank without one run selected.

**Terminology and money:** retained source codes and mapping status allow analysis without claiming complete clinical enrichment. Hidden financial primitives require single run/concept/currency context and remain outside consolidated KPI claims.

## Delivery and testing

The Power BI source includes seven pages and 77 visuals over 22 business tables, nine measures and 50 relationships. Supplied screenshots demonstrate navigation, activity analysis, mapping status and methodology. Source blanks and pending mappings remain visible.

Release work re-ran 94 tests and independently checked source inventories. A reusable auditor checks publication boundaries, syntax/imports, fixture identity, JSON, local links and model/report contracts. CI applies source gates without secrets. [Release evidence](validation/RELEASE_VALIDATION_EVIDENCE.md) distinguishes observed results from unresolved local gates.

## Lessons and limitations

A screenshot supports a displayed count, not a fresh database recount. JSON parsing is not full PBIR schema validation. Historical checkpoints do not establish current deployment state. The release records these boundaries, including blocked fresh PBIR validation and unavailable private-data recount.

Useful future work includes a reviewed orchestration CLI for staging through post-load DQ and a sanitized machine-readable run attestation. Independent terminology validation and a reviewed Coverage identity contract remain separately gated work. They are more valuable than extra dependencies or unsupported production claims.
