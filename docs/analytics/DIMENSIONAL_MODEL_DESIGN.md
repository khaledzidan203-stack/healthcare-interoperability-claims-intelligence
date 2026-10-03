# Dimensional Model Design

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

4E ? Dimensional Model Design

## Model Type

**Governed Dimensional Fact Constellation**

The source contains multiple valid analytical grains, therefore the correct model is a fact constellation rather than one flattened claim table.

No physical analytics tables are created by this checkpoint.

## Design Baseline

- Validated STAGING rows: 678
- Approved facts: 10
- Designed dimensions: 13
- Designed bridges: 1
- Designed relationships: 53
- Financial alias groups still NOT_ASSUMED: 11

## Facts

| Fact | Grain | Source | Load Gate |
|---|---|---|---|
| FactClaim | One governed FHIR ExplanationOfBenefit claim | staging.eob_claim | NONE |
| FactItem | One governed EOB item within one claim | staging.eob_item | NONE |
| FactClaimTotal | One claim-total element at its exact source ordinal | staging.eob_total | NONE |
| FactClaimAdjudication | One claim-level adjudication element at its exact source ordinal | staging.eob_adjudication | NONE |
| FactItemAdjudication | One item-level adjudication element at its exact source ordinal | staging.eob_item_adjudication | NONE |
| FactDiagnosisOccurrence | One diagnosis occurrence attached to one claim | staging.eob_diagnosis | DIAGNOSIS_TERMINOLOGY_MAPPING_FOR_FULL_DIMENSION_ATTRIBUTES |
| FactProcedureOccurrence | One procedure occurrence attached to one claim | staging.eob_procedure | PROCEDURE_TERMINOLOGY_MAPPING_FOR_FULL_DIMENSION_ATTRIBUTES |
| FactCareTeamOccurrence | One care-team participation occurrence attached to one claim | staging.eob_care_team | PROVIDER_REFERENCE_NORMALIZATION |
| FactSupportingInfoOccurrence | One supporting-information occurrence attached to one claim | staging.eob_supporting_info | SUPPORTING_INFO_TERMINOLOGY_FOR_FULL_DIMENSION_ATTRIBUTES |
| FactItemDetail | One EOB item-detail element within one claim item | staging.eob_item_detail | SERVICE_TERMINOLOGY_FOR_FULL_DIMENSION_ATTRIBUTES |

## Conformed and Candidate Dimensions

| Dimension | Grain | Status | Load Gate |
|---|---|---|---|
| DimDate | One calendar date | APPROVED_DESIGN | NONE |
| DimPipelineRun | One governed pipeline run | APPROVED_DESIGN | NONE |
| DimPatient | One governed patient dimension version | APPROVED_DESIGN_SCD2 | NONE |
| DimCoverage | One governed coverage dimension version | APPROVED_DESIGN_SCD2 | CLAIM_INSURANCE_ARRAY_NORMALIZATION_FOR_RELATIONSHIP |
| DimFinancialConcept | One authoritative financial system/code concept version | APPROVED_DESIGN_REFERENCE | NONE |
| DimCurrency | One currency code | APPROVED_DESIGN_REFERENCE | NONE |
| DimClaimType | One claim-type system/code concept | DESIGN_APPROVED_LOAD_GATED | AUTHORITATIVE_NON_FINANCIAL_TERMINOLOGY |
| DimServiceCode | One service/product coding system/code concept | DESIGN_APPROVED_LOAD_GATED | AUTHORITATIVE_SERVICE_TERMINOLOGY |
| DimDiagnosis | One diagnosis coding system/code concept | DESIGN_APPROVED_LOAD_GATED | AUTHORITATIVE_DIAGNOSIS_TERMINOLOGY |
| DimProcedure | One procedure coding system/code concept | DESIGN_APPROVED_LOAD_GATED | AUTHORITATIVE_PROCEDURE_TERMINOLOGY |
| DimProvider | One normalized provider identity/version | DESIGN_APPROVED_LOAD_GATED | PROVIDER_REFERENCE_AND_IDENTIFIER_NORMALIZATION |
| DimPayer | One normalized payer/insurer identity/version | DESIGN_APPROVED_LOAD_GATED | PAYER_REFERENCE_NORMALIZATION |
| DimSupportingInfoCategory | One supporting-information system/code concept | DESIGN_APPROVED_LOAD_GATED | AUTHORITATIVE_SUPPORTING_INFO_TERMINOLOGY |

## Bridge

`BridgeClaimCoverage` is required because FHIR EOB `insurance[]` is repeating. A claim is therefore not assumed to have exactly one coverage.

The bridge remains load-gated until the insurance array is promoted from preserved JSON into a governed relational association and its cardinality is validated.

## Conformed Dimension Strategy

`DimPipelineRun`, `DimPatient`, and claim-created `DimDate` keys are propagated directly into child facts during analytics ETL.

This allows common filtering without creating FactClaim ? FactItem or other direct fact-to-fact relationships.

Parent source identifiers such as `eob_id` and `item_sequence` remain available for lineage and reconciliation but are not used as semantic fact-to-fact relationships.

## Date Strategy

A single conformed `DimDate` is role-played for:

- Claim Created Date
- Billable Start Date
- Billable End Date
- Item Serviced Date
- Procedure Date
- Supporting Information Timing Date

Power BI active/inactive date relationship decisions are deferred to the semantic-model checkpoint.

## Financial Model

`FactClaimTotal`, `FactClaimAdjudication`, and `FactItemAdjudication` remain physically and semantically separate.

All three use the conformed:

- `DimFinancialConcept`
- `DimCurrency`

but this does not authorize cross-fact summation.

Financial aliases remain `NOT_ASSUMED` even where authoritative display labels are identical.

## Patient Dimension

`DimPatient` is designed as a governed SCD Type 2 dimension so that future source changes can be represented without overwriting historical analytical context.

The current sandbox has only one validated run, so SCD behavior will be implementation-tested later.

## Coverage Dimension

`DimCoverage` is also designed for governed versioning, but claim coverage filtering is not enabled yet because `insurance[]` requires explicit bridge normalization.

## Load-Gated Dimensions

The following designs exist but must not be treated as fully resolved business dimensions yet:

- DimClaimType
- DimServiceCode
- DimDiagnosis
- DimProcedure
- DimProvider
- DimPayer
- DimSupportingInfoCategory

Their source keys can be retained, but authoritative terminology or reference/master-data normalization must be completed before enriched business attributes are loaded.

## Relationship Rules

- Direct fact-to-fact relationships: FORBIDDEN
- Default many-to-many fact relationships: FORBIDDEN
- Cross-grain financial summation: FORBIDDEN
- Cross-currency financial summation: FORBIDDEN
- Financial display-name equivalence: NOT ASSUMED
- NULL-to-zero conversion: not allowed by default

## User-Facing KPI State

Consolidated financial KPIs remain **NOT APPROVED**.

This model establishes safe dimensional structure only.

## Next Gate

Before physical analytics DDL is built, normalize the remaining repeating/reference structures required by the dimensional model, starting with claim insurance/coverage and provider/payer identities.


## Relationship Reconciliation

The physical bridge is explicitly run-scoped.

The approved model therefore includes:

`DimPipelineRun ? BridgeClaimCoverage`

This is a technical/audit conformed-dimension relationship.
It is not a fact-to-fact relationship and does not change
the analytical grain or financial safety rules.

The corrected total relationship count is **53**.
