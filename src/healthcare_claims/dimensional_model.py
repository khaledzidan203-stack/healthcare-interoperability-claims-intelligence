MODEL_TYPE = "GOVERNED_DIMENSIONAL_CONSTELLATION"


MODEL_POLICIES = {
    "direct_fact_to_fact_relationships":
        "FORBIDDEN",

    "cross_grain_financial_summation":
        "FORBIDDEN",

    "cross_currency_summation":
        "FORBIDDEN",

    "financial_alias_equivalence":
        "NOT_ASSUMED",

    "consolidated_financial_kpis":
        "NOT_APPROVED",

    "child_fact_parent_keys":
        "PROPAGATE_CONFORMED_DIMENSION_KEYS",

    "source_parent_ids":
        "RETAIN_AS_DEGENERATE_LINEAGE_NOT_RELATIONSHIPS",

    "coverage_filtering":
        "BRIDGE_REQUIRED_AND_LOAD_GATED",

    "analytics_tables":
        "NOT_YET_CREATED",
}


FACTS = (
    {
        "entity_id": "F01",
        "entity_type": "FACT",
        "entity_name": "FactClaim",
        "grain":
            "One governed FHIR ExplanationOfBenefit claim",
        "source":
            "staging.eob_claim",
        "natural_key":
            "pipeline_run_id + eob_id",
        "warehouse_key":
            "fact_claim_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "F02",
        "entity_type": "FACT",
        "entity_name": "FactItem",
        "grain":
            "One governed EOB item within one claim",
        "source":
            "staging.eob_item",
        "natural_key":
            "pipeline_run_id + eob_id + item_sequence",
        "warehouse_key":
            "fact_item_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "F03",
        "entity_type": "FACT",
        "entity_name": "FactClaimTotal",
        "grain":
            "One claim-total element at its exact source ordinal",
        "source":
            "staging.eob_total",
        "natural_key":
            "pipeline_run_id + eob_id + source_ordinal",
        "warehouse_key":
            "fact_claim_total_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "F04",
        "entity_type": "FACT",
        "entity_name": "FactClaimAdjudication",
        "grain":
            "One claim-level adjudication element at its exact source ordinal",
        "source":
            "staging.eob_adjudication",
        "natural_key":
            "pipeline_run_id + eob_id + source_ordinal",
        "warehouse_key":
            "fact_claim_adjudication_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "F05",
        "entity_type": "FACT",
        "entity_name": "FactItemAdjudication",
        "grain":
            "One item-level adjudication element at its exact source ordinal",
        "source":
            "staging.eob_item_adjudication",
        "natural_key":
            "pipeline_run_id + eob_id + item_sequence + source_ordinal",
        "warehouse_key":
            "fact_item_adjudication_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "F06",
        "entity_type": "FACT",
        "entity_name": "FactDiagnosisOccurrence",
        "grain":
            "One diagnosis occurrence attached to one claim",
        "source":
            "staging.eob_diagnosis",
        "natural_key":
            "pipeline_run_id + eob_id + diagnosis_sequence",
        "warehouse_key":
            "fact_diagnosis_occurrence_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "DIAGNOSIS_TERMINOLOGY_MAPPING_FOR_FULL_DIMENSION_ATTRIBUTES",
    },

    {
        "entity_id": "F07",
        "entity_type": "FACT",
        "entity_name": "FactProcedureOccurrence",
        "grain":
            "One procedure occurrence attached to one claim",
        "source":
            "staging.eob_procedure",
        "natural_key":
            "pipeline_run_id + eob_id + procedure_sequence",
        "warehouse_key":
            "fact_procedure_occurrence_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "PROCEDURE_TERMINOLOGY_MAPPING_FOR_FULL_DIMENSION_ATTRIBUTES",
    },

    {
        "entity_id": "F08",
        "entity_type": "FACT",
        "entity_name": "FactCareTeamOccurrence",
        "grain":
            "One care-team participation occurrence attached to one claim",
        "source":
            "staging.eob_care_team",
        "natural_key":
            "pipeline_run_id + eob_id + careteam_sequence",
        "warehouse_key":
            "fact_care_team_occurrence_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "PROVIDER_REFERENCE_NORMALIZATION",
    },

    {
        "entity_id": "F09",
        "entity_type": "FACT",
        "entity_name": "FactSupportingInfoOccurrence",
        "grain":
            "One supporting-information occurrence attached to one claim",
        "source":
            "staging.eob_supporting_info",
        "natural_key":
            "pipeline_run_id + eob_id + supporting_info_sequence",
        "warehouse_key":
            "fact_supporting_info_occurrence_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "SUPPORTING_INFO_TERMINOLOGY_FOR_FULL_DIMENSION_ATTRIBUTES",
    },

    {
        "entity_id": "F10",
        "entity_type": "FACT",
        "entity_name": "FactItemDetail",
        "grain":
            "One EOB item-detail element within one claim item",
        "source":
            "staging.eob_item_detail",
        "natural_key":
            "pipeline_run_id + eob_id + item_sequence + detail_sequence",
        "warehouse_key":
            "fact_item_detail_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "SERVICE_TERMINOLOGY_FOR_FULL_DIMENSION_ATTRIBUTES",
    },
)


DIMENSIONS = (
    {
        "entity_id": "D01",
        "entity_type": "DIMENSION",
        "entity_name": "DimDate",
        "grain":
            "One calendar date",
        "source":
            "Generated governed calendar",
        "natural_key":
            "calendar_date",
        "warehouse_key":
            "date_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "D02",
        "entity_type": "DIMENSION",
        "entity_name": "DimPipelineRun",
        "grain":
            "One governed pipeline run",
        "source":
            "governance.pipeline_run",
        "natural_key":
            "pipeline_run_id",
        "warehouse_key":
            "pipeline_run_key",
        "model_status":
            "APPROVED_DESIGN",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "D03",
        "entity_type": "DIMENSION",
        "entity_name": "DimPatient",
        "grain":
            "One governed patient dimension version",
        "source":
            "staging.patient",
        "natural_key":
            "source_system + patient_id + dimensional_version",
        "warehouse_key":
            "patient_key",
        "model_status":
            "APPROVED_DESIGN_SCD2",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "D04",
        "entity_type": "DIMENSION",
        "entity_name": "DimCoverage",
        "grain":
            "One governed coverage dimension version",
        "source":
            "staging.coverage",
        "natural_key":
            "source_system + coverage_id + dimensional_version",
        "warehouse_key":
            "coverage_key",
        "model_status":
            "APPROVED_DESIGN_SCD2",
        "load_gate":
            "CLAIM_INSURANCE_ARRAY_NORMALIZATION_FOR_RELATIONSHIP",
    },

    {
        "entity_id": "D05",
        "entity_type": "DIMENSION",
        "entity_name": "DimFinancialConcept",
        "grain":
            "One authoritative financial system/code concept version",
        "source":
            "AUTHORITATIVE_FINANCIAL_TERMINOLOGY.csv",
        "natural_key":
            "system_uri + code + authority_version",
        "warehouse_key":
            "financial_concept_key",
        "model_status":
            "APPROVED_DESIGN_REFERENCE",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "D06",
        "entity_type": "DIMENSION",
        "entity_name": "DimCurrency",
        "grain":
            "One currency code",
        "source":
            "FHIR Money.currency",
        "natural_key":
            "currency_code",
        "warehouse_key":
            "currency_key",
        "model_status":
            "APPROVED_DESIGN_REFERENCE",
        "load_gate":
            "NONE",
    },

    {
        "entity_id": "D07",
        "entity_type": "DIMENSION",
        "entity_name": "DimClaimType",
        "grain":
            "One claim-type system/code concept",
        "source":
            "staging.eob_claim",
        "natural_key":
            "system_uri + code",
        "warehouse_key":
            "claim_type_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "AUTHORITATIVE_NON_FINANCIAL_TERMINOLOGY",
    },

    {
        "entity_id": "D08",
        "entity_type": "DIMENSION",
        "entity_name": "DimServiceCode",
        "grain":
            "One service/product coding system/code concept",
        "source":
            "staging.eob_item + staging.eob_item_detail",
        "natural_key":
            "system_uri + code",
        "warehouse_key":
            "service_code_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "AUTHORITATIVE_SERVICE_TERMINOLOGY",
    },

    {
        "entity_id": "D09",
        "entity_type": "DIMENSION",
        "entity_name": "DimDiagnosis",
        "grain":
            "One diagnosis coding system/code concept",
        "source":
            "staging.eob_diagnosis",
        "natural_key":
            "system_uri + code",
        "warehouse_key":
            "diagnosis_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "AUTHORITATIVE_DIAGNOSIS_TERMINOLOGY",
    },

    {
        "entity_id": "D10",
        "entity_type": "DIMENSION",
        "entity_name": "DimProcedure",
        "grain":
            "One procedure coding system/code concept",
        "source":
            "staging.eob_procedure",
        "natural_key":
            "system_uri + code",
        "warehouse_key":
            "procedure_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "AUTHORITATIVE_PROCEDURE_TERMINOLOGY",
    },

    {
        "entity_id": "D11",
        "entity_type": "DIMENSION",
        "entity_name": "DimProvider",
        "grain":
            "One normalized provider identity/version",
        "source":
            "Claim/provider and care-team references/identifiers",
        "natural_key":
            "normalized provider identity",
        "warehouse_key":
            "provider_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "PROVIDER_REFERENCE_AND_IDENTIFIER_NORMALIZATION",
    },

    {
        "entity_id": "D12",
        "entity_type": "DIMENSION",
        "entity_name": "DimPayer",
        "grain":
            "One normalized payer/insurer identity/version",
        "source":
            "EOB insurer/reference structures",
        "natural_key":
            "normalized payer identity",
        "warehouse_key":
            "payer_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "PAYER_REFERENCE_NORMALIZATION",
    },

    {
        "entity_id": "D13",
        "entity_type": "DIMENSION",
        "entity_name": "DimSupportingInfoCategory",
        "grain":
            "One supporting-information system/code concept",
        "source":
            "staging.eob_supporting_info",
        "natural_key":
            "system_uri + code",
        "warehouse_key":
            "supporting_info_category_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "AUTHORITATIVE_SUPPORTING_INFO_TERMINOLOGY",
    },
)


BRIDGES = (
    {
        "entity_id": "B01",
        "entity_type": "BRIDGE",
        "entity_name": "BridgeClaimCoverage",
        "grain":
            "One claim-to-coverage association from EOB insurance[]",
        "source":
            "staging.eob_claim.insurance_json",
        "natural_key":
            "pipeline_run_id + eob_id + coverage_reference + source_ordinal",
        "warehouse_key":
            "bridge_claim_coverage_key",
        "model_status":
            "DESIGN_APPROVED_LOAD_GATED",
        "load_gate":
            "CLAIM_INSURANCE_ARRAY_NORMALIZATION_AND_CARDINALITY_VALIDATION",
    },
)


def _relationship(
    relationship_id,
    from_entity,
    to_entity,
    role,
    cardinality,
    key_rule,
    status,
    notes,
):
    return {
        "relationship_id": relationship_id,
        "from_entity": from_entity,
        "to_entity": to_entity,
        "relationship_role": role,
        "cardinality": cardinality,
        "filter_direction": "DIMENSION_TO_FACT",
        "key_rule": key_rule,
        "status": status,
        "notes": notes,
    }


_relationships = []
_counter = 1


def add_relationship(
    from_entity,
    to_entity,
    role,
    cardinality,
    key_rule,
    status="APPROVED_DESIGN",
    notes="",
):
    global _counter

    _relationships.append(
        _relationship(
            f"R{_counter:03d}",
            from_entity,
            to_entity,
            role,
            cardinality,
            key_rule,
            status,
            notes,
        )
    )

    _counter += 1


# Every fact receives the run and patient keys directly.
# Child facts inherit patient/run keys during ETL rather than
# relying on a fact-to-fact semantic relationship.

for fact in FACTS:

    name = fact["entity_name"]

    add_relationship(
        "DimPipelineRun",
        name,
        "Pipeline Run",
        "1:*",
        "pipeline_run_key",
        notes=
            "Technical/audit conformed dimension.",
    )

    add_relationship(
        "DimPatient",
        name,
        "Patient",
        "1:*",
        "patient_key",
        notes=
            "Patient key propagated from the governed claim context "
            "for child facts.",
    )

    add_relationship(
        "DimDate",
        name,
        "Claim Created Date",
        "1:*",
        "claim_created_date_key",
        notes=
            "Conformed claim-created date propagated to all facts.",
    )


# Additional role-playing dates.

add_relationship(
    "DimDate",
    "FactClaim",
    "Billable Start Date",
    "1:*",
    "billable_start_date_key",
)

add_relationship(
    "DimDate",
    "FactClaim",
    "Billable End Date",
    "1:*",
    "billable_end_date_key",
)

add_relationship(
    "DimDate",
    "FactItem",
    "Serviced Date",
    "1:*",
    "serviced_date_key",
)

add_relationship(
    "DimDate",
    "FactProcedureOccurrence",
    "Procedure Date",
    "1:*",
    "procedure_date_key",
)

add_relationship(
    "DimDate",
    "FactSupportingInfoOccurrence",
    "Timing Date",
    "1:*",
    "timing_date_key",
)


# Financial dimensions.

for fact in (
    "FactClaimTotal",
    "FactClaimAdjudication",
    "FactItemAdjudication",
):

    add_relationship(
        "DimFinancialConcept",
        fact,
        "Exact Financial Concept",
        "1:*",
        "financial_concept_key",
        notes=
            "Exact system/code only; no alias consolidation.",
    )

    add_relationship(
        "DimCurrency",
        fact,
        "Currency",
        "1:*",
        "currency_key",
        notes=
            "Cross-currency aggregation is forbidden.",
    )


# Coded and reference dimensions.

add_relationship(
    "DimClaimType",
    "FactClaim",
    "Claim Type",
    "1:*",
    "claim_type_key",
    "LOAD_GATED",
    "Requires broader authoritative terminology resolution.",
)

add_relationship(
    "DimServiceCode",
    "FactItem",
    "Service/Product",
    "1:*",
    "service_code_key",
    "LOAD_GATED",
    "Requires service terminology resolution.",
)

add_relationship(
    "DimServiceCode",
    "FactItemDetail",
    "Service/Product",
    "1:*",
    "service_code_key",
    "LOAD_GATED",
    "Requires service terminology resolution.",
)

add_relationship(
    "DimDiagnosis",
    "FactDiagnosisOccurrence",
    "Diagnosis",
    "1:*",
    "diagnosis_key",
    "LOAD_GATED",
    "Requires diagnosis terminology resolution.",
)

add_relationship(
    "DimProcedure",
    "FactProcedureOccurrence",
    "Procedure",
    "1:*",
    "procedure_key",
    "LOAD_GATED",
    "Requires procedure terminology resolution.",
)

add_relationship(
    "DimProvider",
    "FactClaim",
    "Claim Provider",
    "1:*",
    "provider_key",
    "LOAD_GATED",
    "Contained/relative provider references must be normalized.",
)

add_relationship(
    "DimProvider",
    "FactCareTeamOccurrence",
    "Care Team Provider",
    "1:*",
    "provider_key",
    "LOAD_GATED",
    "Provider identifiers/references require mastered identity rules.",
)

add_relationship(
    "DimPayer",
    "FactClaim",
    "Insurer/Payer",
    "1:*",
    "payer_key",
    "LOAD_GATED",
    "Payer reference normalization required.",
)

add_relationship(
    "DimSupportingInfoCategory",
    "FactSupportingInfoOccurrence",
    "Supporting Information Category",
    "1:*",
    "supporting_info_category_key",
    "LOAD_GATED",
    "Requires supporting-information terminology resolution.",
)


# Claim-to-coverage is explicitly modeled as a bridge because
# EOB insurance[] is repeating.

add_relationship(
    "DimPipelineRun",
    "BridgeClaimCoverage",
    "Pipeline Run",
    "1:*",
    "pipeline_run_key",
    notes=
        "Technical/audit conformed dimension for the "
        "run-scoped bridge.",
)


add_relationship(
    "DimCoverage",
    "BridgeClaimCoverage",
    "Coverage",
    "1:*",
    "coverage_key",
    "LOAD_GATED",
    "insurance[] normalization required before load.",
)

add_relationship(
    "BridgeClaimCoverage",
    "FactClaim",
    "Claim Coverage Association",
    "*:1",
    "claim business key association",
    "LOAD_GATED",
    "Bridge is not a fact; cardinality must be validated before semantic use.",
)


RELATIONSHIPS = tuple(
    _relationships
)


BUS_MATRIX = (
    {
        "fact": "FactClaim",
        "DimDate": "Created/Billable",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "BRIDGE_GATED",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "GATED",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "GATED",
        "DimPayer": "GATED",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactItem",
        "DimDate": "ClaimCreated/Serviced",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "GATED",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactClaimTotal",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "X",
        "DimCurrency": "X",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactClaimAdjudication",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "X",
        "DimCurrency": "X",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactItemAdjudication",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "X",
        "DimCurrency": "X",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactDiagnosisOccurrence",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "GATED",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactProcedureOccurrence",
        "DimDate": "ClaimCreated/Procedure",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "GATED",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactCareTeamOccurrence",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "GATED",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },

    {
        "fact": "FactSupportingInfoOccurrence",
        "DimDate": "ClaimCreated/Timing",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "GATED",
    },

    {
        "fact": "FactItemDetail",
        "DimDate": "ClaimCreated",
        "DimPipelineRun": "X",
        "DimPatient": "X",
        "DimCoverage": "",
        "DimFinancialConcept": "",
        "DimCurrency": "",
        "DimClaimType": "",
        "DimServiceCode": "GATED",
        "DimDiagnosis": "",
        "DimProcedure": "",
        "DimProvider": "",
        "DimPayer": "",
        "DimSupportingInfoCategory": "",
    },
)
