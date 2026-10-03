# Analytical Model Discovery

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project

Healthcare Interoperability & Claims Intelligence Platform

## Checkpoint

4A ? Analytical Model Discovery

## Governance State

- Pipeline run: `run_20260930T084004Z_ingest_2db2ed86`
- STAGING status: `STAGING_DQ_VALIDATED`
- Data quality rules: 20
- Data quality failures: 0
- Analytics physical tables: 0

This checkpoint performs discovery only. It does not define the final star schema, KPIs, facts, dimensions, or Power BI model.

## Validated Grain Inventory

| Canonical Grain | Rows |
|---|---|
| Patient | 1 |
| Coverage | 1 |
| EOB Claim | 6 |
| EOB Item | 29 |
| Diagnosis | 29 |
| Procedure | 2 |
| Care Team | 35 |
| Supporting Info | 112 |
| Claim Adjudication | 31 |
| Claim Total | 26 |
| Item Adjudication | 393 |
| Item Detail | 13 |

## Temporal Coverage

- Earliest EOB created: `2026-01-29 03:00:00+03`
- Latest EOB created: `2026-03-05 03:00:00+03`
- Earliest billable period start: `2019-08-21 00:00:00+03`
- Latest billable period end: `2025-09-09 00:00:00+03`

## Claim Header Profiles

| Status | Use | Outcome | Type System | Type Code | Claims |
|---|---|---|---|---|---|
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 1 | 1 |
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 3 | 1 |
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 4 | 1 |
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 50 | 1 |
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 72 | 1 |
| active | claim | complete | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 81 | 1 |

## Child Cardinality per Claim

| Structure | Minimum | Average | Maximum |
|---|---|---|---|
| Items | 1 | 4.83 | 13 |
| Diagnoses | 0 | 4.83 | 19 |
| Procedures | 0 | 0.33 | 2 |
| Care Team | 1 | 5.83 | 19 |
| Supporting Info | 13 | 18.67 | 22 |
| Claim Adjudication | 1 | 5.17 | 24 |
| Claim Totals | 3 | 4.33 | 7 |

## Code-System Inventory

| Domain | Code System | Rows | Rows With Code | Distinct Codes |
|---|---|---|---|---|
| Claim Adjudication Category | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudicationDiscriminator | 6 | 6 | 1 |
| Claim Adjudication Category | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | 25 | 25 | 24 |
| Claim Total Category | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | 14 | 14 | 6 |
| Claim Total Category | http://terminology.hl7.org/CodeSystem/adjudication | 12 | 12 | 3 |
| Claim Type | https://bluebutton.cms.gov/fhir/CodeSystem/CLM-TYPE-CD | 6 | 6 | 6 |
| Diagnosis | http://hl7.org/fhir/sid/icd-10-cm | 29 | 29 | 13 |
| Item Adjudication Category | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | 143 | 143 | 7 |
| Item Adjudication Category | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudicationDiscriminator | 13 | 13 | 1 |
| Item Adjudication Category | http://terminology.hl7.org/CodeSystem/adjudication | 94 | 94 | 4 |
| Item Adjudication Category | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | 143 | 143 | 15 |
| Item Detail Product/Service | http://hl7.org/fhir/sid/ndc | 13 | 13 | 8 |
| Item Product/Service | http://hl7.org/fhir/sid/ndc | 2 | 2 | 2 |
| Item Product/Service | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBCompoundLiteral | 1 | 1 | 1 |
| Item Product/Service | http://www.ama-assn.org/go/cpt | 18 | 18 | 2 |
| Item Product/Service | https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets | 8 | 8 | 1 |
| Procedure | http://www.cms.gov/Medicare/Coding/ICD10 | 2 | 2 | 2 |
| Supporting Info Category | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType | 30 | 30 | 13 |
| Supporting Info Category | https://bluebutton.cms.gov/fhir/CodeSystem/Supporting-Information | 82 | 82 | 30 |

## Financial Structure Inventory

The sums below are raw structural observations only. They are not approved business KPIs because the financial category semantics have not yet been mapped.

| Domain | Category System | Category Code | Currency | Rows | Amount Rows | Raw Amount Sum | Value Rows | Raw Value Sum |
|---|---|---|---|---|---|---|---|---|
| Claim Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudicationDiscriminator | benefitpaymentstatus | <NULL> | 6 | 0 | 0 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_BLOOD_CHRG_AMT | USD | 1 | 1 | 37.11 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_BLOOD_LBLTY_AMT | USD | 1 | 1 | 3.98 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_BLOOD_NCVRD_CHRG_AMT | USD | 1 | 1 | 101.21 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_HIPPS_UNCOMPD_CARE_AMT | USD | 1 | 1 | 95.11 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_INSTNL_CVRD_DAY_CNT | <NULL> | 1 | 0 | 0 | 1 | 8 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_INSTNL_DRG_OUTLIER_AMT | USD | 1 | 1 | 1057.17 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_INSTNL_MDCR_COINS_DAY_CNT | <NULL> | 1 | 0 | 0 | 1 | 3 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_INSTNL_NCVRD_DAY_CNT | <NULL> | 1 | 0 | 0 | 1 | 1 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_INSTNL_PER_DIEM_AMT | USD | 1 | 1 | 228.6 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_HOSPC_PRD_CNT | <NULL> | 1 | 0 | 0 | 1 | 3 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_INSTNL_PRMRY_PYR_AMT | USD | 1 | 1 | 2439.2 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_BENE_DDCTBL_AMT | USD | 1 | 1 | 16.61 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_LRD_USE_CNT | <NULL> | 1 | 0 | 0 | 1 | 7 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_CPTL_FSP_AMT | USD | 1 | 1 | 12.71 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_CPTL_HRMLS_AMT | USD | 1 | 1 | 20.2 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_CPTL_IME_AMT | USD | 1 | 1 | 14.81 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_CPTL_TOT_AMT | USD | 1 | 1 | 24.55 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_DRG_WT_NUM | <NULL> | 1 | 0 | 0 | 1 | 1.29 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_DSPRPRTNT_AMT | USD | 1 | 1 | 1782.66 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_EXCPTN_AMT | USD | 1 | 1 | 21.09 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_IP_PPS_OUTLIER_AMT | USD | 1 | 1 | 7.85 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_PRFNL_PRMRY_PYR_AMT | USD | 2 | 2 | 1277.0 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_OPRTNL_DSPRTNT_AMT | USD | 1 | 1 | 0.0 | 0 | 0 |
| Claim Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_OPRTNL_IME_AMT | USD | 1 | 1 | 0.0 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | coinsurance | USD | 1 | 1 | 17.43 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | noncovered | USD | 1 | 1 | 31123.95 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidbypatient | USD | 5 | 5 | 817521.09 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidtopatient | USD | 1 | 1 | 0 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidtoprovider | USD | 3 | 3 | 31.0 | 0 | 0 |
| Claim Total | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | priorpayerpaid | USD | 3 | 3 | 1615.18 | 0 | 0 |
| Claim Total | http://terminology.hl7.org/CodeSystem/adjudication | deductible | USD | 3 | 3 | 4164.73 | 0 | 0 |
| Claim Total | http://terminology.hl7.org/CodeSystem/adjudication | eligible | USD | 3 | 3 | 1385678.0 | 0 | 0 |
| Claim Total | http://terminology.hl7.org/CodeSystem/adjudication | submitted | USD | 6 | 6 | 5820347.43 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | coinsurance | USD | 13 | 13 | 28.0 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | discount | USD | 13 | 13 | 38919.0 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | noncovered | USD | 13 | 13 | 10307.03 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidbypatient | USD | 13 | 13 | 26.70 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidtopatient | USD | 26 | 26 | 60.37 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | paidtoprovider | USD | 26 | 26 | 19963.11 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication | priorpayerpaid | USD | 39 | 39 | 46517.16 | 0 | 0 |
| Item Adjudication | http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudicationDiscriminator | benefitpaymentstatus | <NULL> | 13 | 0 | 0 | 0 | 0 |
| Item Adjudication | http://terminology.hl7.org/CodeSystem/adjudication | benefit | USD | 26 | 26 | 60.81 | 0 | 0 |
| Item Adjudication | http://terminology.hl7.org/CodeSystem/adjudication | deductible | USD | 26 | 26 | 79.33 | 0 | 0 |
| Item Adjudication | http://terminology.hl7.org/CodeSystem/adjudication | eligible | USD | 13 | 13 | 27.0 | 0 | 0 |
| Item Adjudication | http://terminology.hl7.org/CodeSystem/adjudication | submitted | USD | 29 | 29 | 4140645.44 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_ADD_ON_PYMT_AMT | USD | 13 | 13 | 73429.94 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_BLOOD_DDCTBL_AMT | USD | 13 | 13 | 102.49 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_CARR_PSYCH_OT_LMT_AMT | USD | 13 | 13 | 65570.0 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_GRS_ABOVE_THRSHLD_AMT | USD | 3 | 3 | 1730988.21 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_GRS_BLW_THRSHLD_AMT | USD | 3 | 3 | 1143547.8 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_INSTNL_ADJSTD_AMT | USD | 13 | 13 | 8233.54 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_INSTNL_RATE_AMT | USD | 13 | 13 | 116.40 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_INSTNL_RDCD_AMT | USD | 13 | 13 | 9616.58 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_LIS_AMT | USD | 3 | 3 | 2007361.89 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_PLRO_AMT | USD | 3 | 3 | 1387516.78 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_PRFNL_DME_PRICE_AMT | USD | 11 | 11 | 54018.0 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_PRFNL_INTRST_AMT | USD | 13 | 13 | 53751.0 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_LINE_RPTD_GAP_DSCNT_AMT | USD | 3 | 3 | 1789790.71 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_MDCR_PRMRY_PYR_ALOWD_AMT | USD | 13 | 13 | 61649.0 | 0 | 0 |
| Item Adjudication | https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication | CLM_REV_CNTR_TDAPA_AMT | USD | 13 | 13 | 69584.38 | 0 | 0 |

## Reference Patterns

| Reference Domain | Reference Form | Rows |
|---|---|---|
| Claim Insurer | CONTAINED | 3 |
| Claim Insurer | NULL | 3 |
| Claim Patient | RELATIVE | 6 |
| Claim Provider | CONTAINED | 4 |
| Claim Provider | NULL | 2 |
| Coverage Beneficiary | RELATIVE | 1 |

## Analytical Field Population

| Field | Rows | Populated | Population % |
|---|---|---|---|
| Claim.PatientReference | 6 | 6 | 100.00% |
| Claim.TypeCode | 6 | 6 | 100.00% |
| Claim.ProviderReference | 6 | 4 | 66.67% |
| Claim.InsurerReference | 6 | 3 | 50.00% |
| Item.ProductServiceCode | 29 | 29 | 100.00% |
| Diagnosis.Code | 29 | 29 | 100.00% |
| Procedure.Code | 2 | 2 | 100.00% |
| ClaimAdjudication.Amount | 31 | 19 | 61.29% |
| ClaimTotal.Amount | 26 | 26 | 100.00% |
| ItemAdjudication.Amount | 393 | 380 | 96.69% |

## Candidate Analytical Subject Areas

The validated source currently supports investigation of:

- claim-header activity and temporal patterns;
- service/item utilization;
- diagnosis and procedure occurrences;
- care-team/provider participation;
- claim-level and item-level adjudication structures;
- claim total structures;
- coverage context;
- supporting-information structures;
- source lineage, reconciliation, and data-quality monitoring.

These are candidate analytical subject areas, not approved facts or dimensions.

## Semantic Blockers Before Final Analytical Modeling

1. FHIR/CMS code systems must be mapped to human-readable business meanings before KPI definitions are approved.
2. Adjudication and total category codes must be interpreted before financial metrics such as paid, allowed, beneficiary liability, or submitted amount are defined.
3. Provider, insurer, and contained-resource references require reference/master-data treatment before dimension design.
4. Repeating structures retained in JSONB must be reviewed for possible promotion into governed relational entities.
5. The current CMS Sandbox population is suitable for structural and engineering validation, not population-level business conclusions.

## Decision

Do not create the final analytical star schema yet.

The next checkpoint must establish terminology and reference-data mapping for the discovered FHIR/CMS code systems.
