# Governed DAX Measures

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Checkpoint

6B.6 ? Measure Host + Governed DAX Build

## State

**STATIC DAX BUILD PASSED**

## Measure Host

`_Measures` is a zero-business-row, disconnected semantic organization table.

- Hidden placeholder column: `Placeholder`
- M partition returns zero rows
- Relationships: 0
- Explicit measures owned: 9

## Governance

All nine measures enforce the single-snapshot gate.

The three restricted financial primitives additionally require exactly one Financial Concept and one Currency in the current filter context.

No financial grains are combined.

Restricted financial measures remain hidden from ordinary report-author field browsing.

## Measures

### M001 ? Claim Count

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_claim`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_claim'), BLANK())
```

### M002 ? Item Count

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_item`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_item'), BLANK())
```

### M003 ? Diagnosis Occurrences

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_diagnosis_occurrence`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_diagnosis_occurrence'), BLANK())
```

### M004 ? Procedure Occurrences

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_procedure_occurrence`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_procedure_occurrence'), BLANK())
```

### M005 ? Care Team Occurrences

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_care_team_occurrence`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_care_team_occurrence'), BLANK())
```

### M006 ? Supporting Info Occurrences

- Status: `APPROVED_BASE_MEASURE`
- Source fact: `fact_supporting_info_occurrence`
- Display folder: `01 Approved Base Measures`
- Hidden: `False`
- Format: `#,##0`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_supporting_info_occurrence'), BLANK())
```

### M007 ? Claim Total Amount

- Status: `RESTRICTED_FINANCIAL_PRIMITIVE`
- Source fact: `fact_claim_total`
- Display folder: `90 Restricted Financial Primitives`
- Hidden: `True`
- Format: `#,##0.00`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_claim_total'[amount]), BLANK())
```

### M008 ? Claim Adjudication Amount

- Status: `RESTRICTED_FINANCIAL_PRIMITIVE`
- Source fact: `fact_claim_adjudication`
- Display folder: `90 Restricted Financial Primitives`
- Hidden: `True`
- Format: `#,##0.00`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_claim_adjudication'[amount]), BLANK())
```

### M009 ? Item Adjudication Amount

- Status: `RESTRICTED_FINANCIAL_PRIMITIVE`
- Source fact: `fact_item_adjudication`
- Display folder: `90 Restricted Financial Primitives`
- Hidden: `True`
- Format: `#,##0.00`

```DAX
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_item_adjudication'[amount]), BLANK())
```

## Runtime Boundary

This checkpoint validates TMDL/DAX structure offline.

Power BI Desktop must reopen, save, and execute representative DAX queries successfully before the measures are approved for report-page construction.
