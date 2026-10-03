# Analytical Grain & Metric Contract

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

4D ? Analytical Grain & Metric Contract

## Governing Principle

Every analytical fact must have an explicit grain before aggregation, relationships, KPIs, or Power BI measures are built.

Different fact grains must remain separate and must not be joined or summed blindly.

## Approved Analytical Grains

| ID | Proposed Entity | One Row Means | Source | Role |
|---|---|---|---|---|
| G01 | FactClaim | One row = one FHIR ExplanationOfBenefit claim within one pipeline run. | staging.eob_claim | CORE_FACT |
| G02 | FactItem | One row = one EOB item within one claim and pipeline run. | staging.eob_item | CORE_FACT |
| G03 | FactClaimTotal | One row = one claim-level EOB total element at its exact source ordinal. | staging.eob_total | CLAIM_FINANCIAL_FACT |
| G04 | FactClaimAdjudication | One row = one claim-level adjudication element at its exact source ordinal. | staging.eob_adjudication | CLAIM_ADJUDICATION_FACT |
| G05 | FactItemAdjudication | One row = one adjudication element for one EOB item at its exact source ordinal. | staging.eob_item_adjudication | ITEM_ADJUDICATION_FACT |
| G06 | FactDiagnosisOccurrence | One row = one diagnosis occurrence attached to one claim. | staging.eob_diagnosis | FACTLESS_OCCURRENCE |
| G07 | FactProcedureOccurrence | One row = one procedure occurrence attached to one claim. | staging.eob_procedure | FACTLESS_OCCURRENCE |
| G08 | FactCareTeamOccurrence | One row = one care-team participation occurrence attached to one claim. | staging.eob_care_team | FACTLESS_OCCURRENCE |
| G09 | FactSupportingInfoOccurrence | One row = one supporting-information occurrence attached to one claim. | staging.eob_supporting_info | FACTLESS_OCCURRENCE |
| G10 | FactItemDetail | One row = one EOB item detail element within one claim item. | staging.eob_item_detail | SECONDARY_CHILD_FACT |

## Financial Grain Separation

Three financial source grains are explicitly separate:

1. Claim Total
2. Claim Adjudication
3. Item Adjudication

They must never be blindly combined into one total.

A value may only be summed when all of the following match:

- approved analytical fact;
- financial domain;
- terminology system URI;
- code;
- currency;
- compatible analytical grain.

## Approved Analytical Metric Primitives

| Metric | Name | Source Fact | Grain | Total Behavior | Status |
|---|---|---|---|---|---|
| M001 | Claim Count | FactClaim | Claim | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M002 | Item Count | FactItem | Claim Item | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M003 | Diagnosis Occurrence Count | FactDiagnosisOccurrence | Claim Diagnosis | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M004 | Procedure Occurrence Count | FactProcedureOccurrence | Claim Procedure | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M005 | Care Team Occurrence Count | FactCareTeamOccurrence | Claim Care Team | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M006 | Supporting Information Occurrence Count | FactSupportingInfoOccurrence | Claim Supporting Information | SUM | APPROVED_ANALYTICAL_PRIMITIVE |
| M007 | Claim Total Amount ? Exact Financial Concept | FactClaimTotal | Claim Total Element | SUM only within exact concept and currency | APPROVED_ANALYTICAL_PRIMITIVE |
| M008 | Claim Adjudication Amount ? Exact Financial Concept | FactClaimAdjudication | Claim Adjudication Element | SUM only within exact concept and currency | APPROVED_ANALYTICAL_PRIMITIVE |
| M009 | Item Adjudication Amount ? Exact Financial Concept | FactItemAdjudication | Claim Item Adjudication Element | SUM only within exact concept and currency | APPROVED_ANALYTICAL_PRIMITIVE |

## Important Distinction

`APPROVED_ANALYTICAL_PRIMITIVE` does not mean that a user-facing business KPI has been approved.

The financial primitives only permit safe aggregation of an exact authoritative concept at an exact grain and currency.

Consolidated business metrics such as:

- Total Paid
- Total Allowed
- Total Patient Responsibility
- Total Submitted

remain unapproved until source precedence and alias rules are explicitly decided.

## Non-Monetary Adjudication Values

The six CMS count/weight concepts remain in `FactClaimAdjudication` but are not currency measures.

`benefitpaymentstatus` remains a non-summable status discriminator.

## Relationship Policy

- No direct fact-to-fact relationships.
- No default many-to-many relationships.
- Shared analysis must occur through conformed dimensions or explicit bridges.
- Parent-child source relationships do not automatically become Power BI fact-to-fact relationships.

## Candidate Conformed Dimensions

| Dimension | Current State |
|---|---|
| Date | Candidate ? multiple governed date roles required |
| Patient | Candidate ? source identity available |
| Coverage | Candidate ? coverage context available |
| Financial Concept | Approved candidate from authoritative mapping |
| Currency | Approved candidate |
| Claim Type | Candidate ? terminology mapping still broader than financial mapping |
| Service / Product Code | Candidate ? terminology resolution pending |
| Diagnosis | Candidate ? terminology resolution pending |
| Procedure | Candidate ? terminology resolution pending |
| Provider | Pending reference/master-data normalization |
| Payer / Insurer | Pending reference/master-data normalization |

## Double-Counting Guard

The artifact `FINANCIAL_ALIAS_REVIEW.csv` identifies labels that appear across more than one source context.

These are review candidates only. Equality of display text does not prove semantic equivalence.

## KPI Governance State

- Analytical primitives approved: 9
- User-facing consolidated financial KPIs approved: 0
- Cross-grain financial summation allowed: NO
- Cross-currency summation allowed: NO

## Next Gate

Design the dimensional model using these fixed grains and relationship rules before any analytics tables are created.
