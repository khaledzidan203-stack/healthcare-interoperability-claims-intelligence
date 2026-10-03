
TABLES = (
    {
        "semantic_name": "DimDate",
        "physical_table": "dim_date",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Governed continuous calendar dimension.",
    },
    {
        "semantic_name": "DimPipelineRun",
        "physical_table": "dim_pipeline_run",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "HIDDEN",
        "business_status": "TECHNICAL",
        "notes": "Lineage and snapshot control only.",
    },
    {
        "semantic_name": "DimPatient",
        "physical_table": "dim_patient",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "HIDDEN",
        "business_status": "TECHNICAL",
        "notes": "Conformed patient dimension; identifiers not intended as default report fields.",
    },
    {
        "semantic_name": "DimCoverage",
        "physical_table": "dim_coverage",
        "entity_type": "DIMENSION",
        "inclusion": "EXCLUDED_CURRENT_RELEASE",
        "visibility": "HIDDEN",
        "business_status": "LOAD_GATED",
        "notes": "Current claim associations contain display-only Coverage identity.",
    },
    {
        "semantic_name": "DimFinancialConcept",
        "physical_table": "dim_financial_concept",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "GOVERNED_RESTRICTED",
        "notes": "Required for exact financial-concept context.",
    },
    {
        "semantic_name": "DimCurrency",
        "physical_table": "dim_currency",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "GOVERNED_RESTRICTED",
        "notes": "Required for financial aggregation safety.",
    },
    {
        "semantic_name": "DimClaimType",
        "physical_table": "dim_claim_type",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "MAPPING_GATED",
        "notes": "Structural coding retained; authoritative mapping pending.",
    },
    {
        "semantic_name": "DimServiceCode",
        "physical_table": "dim_service_code",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "MAPPING_GATED",
        "notes": "Structural coding retained; authoritative mapping pending.",
    },
    {
        "semantic_name": "DimDiagnosis",
        "physical_table": "dim_diagnosis",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "MAPPING_GATED",
        "notes": "Structural coding retained; authoritative mapping pending.",
    },
    {
        "semantic_name": "DimProcedure",
        "physical_table": "dim_procedure",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "MAPPING_GATED",
        "notes": "Structural coding retained; authoritative mapping pending.",
    },
    {
        "semantic_name": "DimProvider",
        "physical_table": "dim_provider",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED_WITH_UNKNOWN",
        "notes": "One governed Unknown Provider member is valid.",
    },
    {
        "semantic_name": "DimPayer",
        "physical_table": "dim_payer",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Current payer identities are explicitly resolved.",
    },
    {
        "semantic_name": "DimSupportingInfoCategory",
        "physical_table": "dim_supporting_info_category",
        "entity_type": "DIMENSION",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "MAPPING_GATED",
        "notes": "Structural coding retained; authoritative mapping pending.",
    },

    {
        "semantic_name": "FactClaim",
        "physical_table": "fact_claim",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "One row per governed EOB claim.",
    },
    {
        "semantic_name": "FactItem",
        "physical_table": "fact_item",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "One row per governed EOB item.",
    },
    {
        "semantic_name": "FactClaimTotal",
        "physical_table": "fact_claim_total",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "HIDDEN",
        "business_status": "FINANCIAL_RESTRICTED",
        "notes": "Exact-concept financial primitive only.",
    },
    {
        "semantic_name": "FactClaimAdjudication",
        "physical_table": "fact_claim_adjudication",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "HIDDEN",
        "business_status": "FINANCIAL_RESTRICTED",
        "notes": "Must remain separate from other financial grains.",
    },
    {
        "semantic_name": "FactItemAdjudication",
        "physical_table": "fact_item_adjudication",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "HIDDEN",
        "business_status": "FINANCIAL_RESTRICTED",
        "notes": "Must remain separate from other financial grains.",
    },
    {
        "semantic_name": "FactDiagnosisOccurrence",
        "physical_table": "fact_diagnosis_occurrence",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Occurrence grain; not distinct-patient count.",
    },
    {
        "semantic_name": "FactProcedureOccurrence",
        "physical_table": "fact_procedure_occurrence",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Occurrence grain.",
    },
    {
        "semantic_name": "FactCareTeamOccurrence",
        "physical_table": "fact_care_team_occurrence",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Care-team occurrence grain.",
    },
    {
        "semantic_name": "FactSupportingInfoOccurrence",
        "physical_table": "fact_supporting_info_occurrence",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Supporting-information occurrence grain.",
    },
    {
        "semantic_name": "FactItemDetail",
        "physical_table": "fact_item_detail",
        "entity_type": "FACT",
        "inclusion": "INCLUDED",
        "visibility": "VISIBLE",
        "business_status": "APPROVED",
        "notes": "Nested item-detail grain.",
    },
    {
        "semantic_name": "BridgeClaimCoverage",
        "physical_table": "bridge_claim_coverage",
        "entity_type": "BRIDGE",
        "inclusion": "EXCLUDED_CURRENT_RELEASE",
        "visibility": "HIDDEN",
        "business_status": "LOAD_GATED",
        "notes": "Association preserved physically but current Coverage identity is unresolved.",
    },
)


MEASURES = (
    {
        "metric_id": "M001",
        "name": "Claim Count",
        "source_fact": "FactClaim",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Claim",
        "unit": "Count",
        "notes": "Count of governed claim rows.",
    },
    {
        "metric_id": "M002",
        "name": "Item Count",
        "source_fact": "FactItem",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Item",
        "unit": "Count",
        "notes": "Count of governed EOB item rows.",
    },
    {
        "metric_id": "M003",
        "name": "Diagnosis Occurrences",
        "source_fact": "FactDiagnosisOccurrence",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Diagnosis occurrence",
        "unit": "Count",
        "notes": "Occurrence count, not unique diagnoses or patients.",
    },
    {
        "metric_id": "M004",
        "name": "Procedure Occurrences",
        "source_fact": "FactProcedureOccurrence",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Procedure occurrence",
        "unit": "Count",
        "notes": "Occurrence count.",
    },
    {
        "metric_id": "M005",
        "name": "Care Team Occurrences",
        "source_fact": "FactCareTeamOccurrence",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Care-team occurrence",
        "unit": "Count",
        "notes": "Occurrence count.",
    },
    {
        "metric_id": "M006",
        "name": "Supporting Info Occurrences",
        "source_fact": "FactSupportingInfoOccurrence",
        "status": "APPROVED_BASE_MEASURE",
        "aggregation": "COUNTROWS",
        "grain": "Supporting-info occurrence",
        "unit": "Count",
        "notes": "Occurrence count.",
    },
    {
        "metric_id": "M007",
        "name": "Claim Total Amount",
        "source_fact": "FactClaimTotal",
        "status": "RESTRICTED_FINANCIAL_PRIMITIVE",
        "aggregation": "SUM_AMOUNT_EXACT_CONCEPT_AND_CURRENCY_ONLY",
        "grain": "Claim total concept occurrence",
        "unit": "Currency",
        "notes": "Not a user-facing consolidated KPI. One financial concept and one currency context required.",
    },
    {
        "metric_id": "M008",
        "name": "Claim Adjudication Amount",
        "source_fact": "FactClaimAdjudication",
        "status": "RESTRICTED_FINANCIAL_PRIMITIVE",
        "aggregation": "SUM_AMOUNT_EXACT_CONCEPT_AND_CURRENCY_ONLY",
        "grain": "Claim adjudication concept occurrence",
        "unit": "Currency",
        "notes": "Do not combine with Claim Total or Item Adjudication.",
    },
    {
        "metric_id": "M009",
        "name": "Item Adjudication Amount",
        "source_fact": "FactItemAdjudication",
        "status": "RESTRICTED_FINANCIAL_PRIMITIVE",
        "aggregation": "SUM_AMOUNT_EXACT_CONCEPT_AND_CURRENCY_ONLY",
        "grain": "Item adjudication concept occurrence",
        "unit": "Currency",
        "notes": "Do not combine with other financial grains.",
    },
)


GATES = (
    {
        "gate_id": "SG-001",
        "subject": "Financial KPIs",
        "state": "BLOCKED",
        "rule": "No consolidated or cross-grain financial KPI may be published.",
    },
    {
        "gate_id": "SG-002",
        "subject": "Coverage filtering",
        "state": "BLOCKED",
        "rule": "DimCoverage and BridgeClaimCoverage are excluded from the current semantic release.",
    },
    {
        "gate_id": "SG-003",
        "subject": "Non-financial terminology",
        "state": "MAPPING_GATED",
        "rule": "Source code/display may be shown with limitation; authoritative semantic labels are not yet approved.",
    },
    {
        "gate_id": "SG-004",
        "subject": "Pipeline snapshots",
        "state": "MULTI_RUN_WAREHOUSE_SINGLE_RUN_CONTEXT",
        "rule": "Multiple validated pipeline runs may coexist in the warehouse; each semantic analytical context must resolve to exactly one pipeline run, and cross-run aggregation remains forbidden.",
    },
)


def relationship(
    relationship_id,
    from_table,
    from_column,
    to_table,
    to_column,
    active=True,
    role="STANDARD",
):
    return {
        "relationship_id": relationship_id,
        "from_table": from_table,
        "from_column": from_column,
        "to_table": to_table,
        "to_column": to_column,
        "cardinality": "1:*",
        "filter_direction": "SINGLE_DIMENSION_TO_FACT",
        "active": active,
        "role": role,
        "status": "APPROVED",
    }


_relationships = []
_counter = 1


def add(
    from_table,
    from_column,
    to_table,
    to_column,
    active=True,
    role="STANDARD",
):
    global _counter

    _relationships.append(
        relationship(
            f"SR-{_counter:03d}",
            from_table,
            from_column,
            to_table,
            to_column,
            active,
            role,
        )
    )

    _counter += 1


FACTS = (
    "FactClaim",
    "FactItem",
    "FactClaimTotal",
    "FactClaimAdjudication",
    "FactItemAdjudication",
    "FactDiagnosisOccurrence",
    "FactProcedureOccurrence",
    "FactCareTeamOccurrence",
    "FactSupportingInfoOccurrence",
    "FactItemDetail",
)


# Core conformed dimensions.
for fact in FACTS:
    add(
        "DimPipelineRun",
        "pipeline_run_key",
        fact,
        "pipeline_run_key",
    )

    add(
        "DimPatient",
        "patient_key",
        fact,
        "patient_key",
    )

    add(
        "DimDate",
        "date_key",
        fact,
        "claim_created_date_key",
        True,
        "CLAIM_CREATED_DATE",
    )


# Alternate Date roles.
add(
    "DimDate",
    "date_key",
    "FactClaim",
    "billable_start_date_key",
    False,
    "BILLABLE_START_DATE",
)

add(
    "DimDate",
    "date_key",
    "FactClaim",
    "billable_end_date_key",
    False,
    "BILLABLE_END_DATE",
)

add(
    "DimDate",
    "date_key",
    "FactItem",
    "serviced_date_key",
    False,
    "SERVICE_DATE",
)

add(
    "DimDate",
    "date_key",
    "FactProcedureOccurrence",
    "procedure_date_key",
    False,
    "PROCEDURE_DATE",
)

add(
    "DimDate",
    "date_key",
    "FactSupportingInfoOccurrence",
    "timing_date_key",
    False,
    "SUPPORTING_INFO_TIMING_DATE",
)


# Fact-specific conformed dimensions.
add(
    "DimClaimType",
    "claim_type_key",
    "FactClaim",
    "claim_type_key",
)

add(
    "DimProvider",
    "provider_key",
    "FactClaim",
    "provider_key",
)

add(
    "DimPayer",
    "payer_key",
    "FactClaim",
    "payer_key",
)

add(
    "DimServiceCode",
    "service_code_key",
    "FactItem",
    "service_code_key",
)

add(
    "DimFinancialConcept",
    "financial_concept_key",
    "FactClaimTotal",
    "financial_concept_key",
)

add(
    "DimCurrency",
    "currency_key",
    "FactClaimTotal",
    "currency_key",
)

add(
    "DimFinancialConcept",
    "financial_concept_key",
    "FactClaimAdjudication",
    "financial_concept_key",
)

add(
    "DimCurrency",
    "currency_key",
    "FactClaimAdjudication",
    "currency_key",
)

add(
    "DimFinancialConcept",
    "financial_concept_key",
    "FactItemAdjudication",
    "financial_concept_key",
)

add(
    "DimCurrency",
    "currency_key",
    "FactItemAdjudication",
    "currency_key",
)

add(
    "DimDiagnosis",
    "diagnosis_key",
    "FactDiagnosisOccurrence",
    "diagnosis_key",
)

add(
    "DimProcedure",
    "procedure_key",
    "FactProcedureOccurrence",
    "procedure_key",
)

add(
    "DimProvider",
    "provider_key",
    "FactCareTeamOccurrence",
    "provider_key",
)

add(
    "DimSupportingInfoCategory",
    "supporting_info_category_key",
    "FactSupportingInfoOccurrence",
    "supporting_info_category_key",
)

add(
    "DimServiceCode",
    "service_code_key",
    "FactItemDetail",
    "service_code_key",
)


RELATIONSHIPS = tuple(_relationships)
