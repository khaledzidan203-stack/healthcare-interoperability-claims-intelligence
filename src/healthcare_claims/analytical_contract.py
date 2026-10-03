MODEL_POLICIES = {
    "direct_fact_to_fact_relationships":
        "FORBIDDEN",

    "cross_grain_financial_summation":
        "FORBIDDEN",

    "cross_currency_summation":
        "FORBIDDEN",

    "cross_system_semantic_aliasing":
        "REQUIRES_EXPLICIT_APPROVAL",

    "null_to_zero_conversion":
        "FORBIDDEN_BY_DEFAULT",

    "unknown_member_policy":
        "EXPLICIT_ONLY",

    "user_facing_financial_kpis":
        "NOT_YET_APPROVED",
}


GRAIN_CONTRACTS = (
    {
        "grain_id": "G01",
        "proposed_entity": "FactClaim",
        "row_definition":
            "One row = one FHIR ExplanationOfBenefit claim "
            "within one pipeline run.",
        "source_staging":
            "staging.eob_claim",
        "business_key":
            "pipeline_run_id + eob_id",
        "parent_grain":
            "",
        "analytical_role":
            "CORE_FACT",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G02",
        "proposed_entity": "FactItem",
        "row_definition":
            "One row = one EOB item within one claim "
            "and pipeline run.",
        "source_staging":
            "staging.eob_item",
        "business_key":
            "pipeline_run_id + eob_id + item_sequence",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "CORE_FACT",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G03",
        "proposed_entity": "FactClaimTotal",
        "row_definition":
            "One row = one claim-level EOB total element "
            "at its exact source ordinal.",
        "source_staging":
            "staging.eob_total",
        "business_key":
            "pipeline_run_id + eob_id + source_ordinal",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "CLAIM_FINANCIAL_FACT",
        "financial_grain":
            "CLAIM_TOTAL",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G04",
        "proposed_entity": "FactClaimAdjudication",
        "row_definition":
            "One row = one claim-level adjudication element "
            "at its exact source ordinal.",
        "source_staging":
            "staging.eob_adjudication",
        "business_key":
            "pipeline_run_id + eob_id + source_ordinal",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "CLAIM_ADJUDICATION_FACT",
        "financial_grain":
            "CLAIM_ADJUDICATION",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G05",
        "proposed_entity": "FactItemAdjudication",
        "row_definition":
            "One row = one adjudication element for one "
            "EOB item at its exact source ordinal.",
        "source_staging":
            "staging.eob_item_adjudication",
        "business_key":
            "pipeline_run_id + eob_id + item_sequence "
            "+ source_ordinal",
        "parent_grain":
            "FactItem",
        "analytical_role":
            "ITEM_ADJUDICATION_FACT",
        "financial_grain":
            "ITEM_ADJUDICATION",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G06",
        "proposed_entity": "FactDiagnosisOccurrence",
        "row_definition":
            "One row = one diagnosis occurrence attached "
            "to one claim.",
        "source_staging":
            "staging.eob_diagnosis",
        "business_key":
            "pipeline_run_id + eob_id + diagnosis_sequence",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "FACTLESS_OCCURRENCE",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G07",
        "proposed_entity": "FactProcedureOccurrence",
        "row_definition":
            "One row = one procedure occurrence attached "
            "to one claim.",
        "source_staging":
            "staging.eob_procedure",
        "business_key":
            "pipeline_run_id + eob_id + procedure_sequence",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "FACTLESS_OCCURRENCE",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G08",
        "proposed_entity": "FactCareTeamOccurrence",
        "row_definition":
            "One row = one care-team participation "
            "occurrence attached to one claim.",
        "source_staging":
            "staging.eob_care_team",
        "business_key":
            "pipeline_run_id + eob_id + careteam_sequence",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "FACTLESS_OCCURRENCE",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G09",
        "proposed_entity": "FactSupportingInfoOccurrence",
        "row_definition":
            "One row = one supporting-information "
            "occurrence attached to one claim.",
        "source_staging":
            "staging.eob_supporting_info",
        "business_key":
            "pipeline_run_id + eob_id "
            "+ supporting_info_sequence",
        "parent_grain":
            "FactClaim",
        "analytical_role":
            "FACTLESS_OCCURRENCE",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },

    {
        "grain_id": "G10",
        "proposed_entity": "FactItemDetail",
        "row_definition":
            "One row = one EOB item detail element "
            "within one claim item.",
        "source_staging":
            "staging.eob_item_detail",
        "business_key":
            "pipeline_run_id + eob_id + item_sequence "
            "+ detail_sequence",
        "parent_grain":
            "FactItem",
        "analytical_role":
            "SECONDARY_CHILD_FACT",
        "financial_grain":
            "NO",
        "status":
            "APPROVED_GRAIN",
    },
)


METRIC_CONTRACTS = (
    {
        "metric_id": "M001",
        "business_name": "Claim Count",
        "business_definition":
            "Number of governed EOB claims.",
        "formula":
            "SUM(claim_row_count)",
        "numerator":
            "1 per FactClaim row",
        "denominator":
            "",
        "source_fact":
            "FactClaim",
        "grain":
            "Claim",
        "eligible_population":
            "Validated EOB claims",
        "inclusions_exclusions":
            "One governed EOB per pipeline run",
        "time_logic":
            "Use approved claim date role",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "N/A",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_claim row count",
        "known_limitations":
            "Sandbox population is not representative",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M002",
        "business_name": "Item Count",
        "business_definition":
            "Number of governed EOB claim items.",
        "formula":
            "SUM(item_row_count)",
        "numerator":
            "1 per FactItem row",
        "denominator":
            "",
        "source_fact":
            "FactItem",
        "grain":
            "Claim Item",
        "eligible_population":
            "Validated EOB items",
        "inclusions_exclusions":
            "One governed item sequence per claim",
        "time_logic":
            "Inherited from parent claim or serviced date",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "N/A",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_item row count",
        "known_limitations":
            "Not equivalent to number of claims",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M003",
        "business_name": "Diagnosis Occurrence Count",
        "business_definition":
            "Number of diagnosis occurrences across claims.",
        "formula":
            "SUM(diagnosis_row_count)",
        "numerator":
            "1 per FactDiagnosisOccurrence row",
        "denominator":
            "",
        "source_fact":
            "FactDiagnosisOccurrence",
        "grain":
            "Claim Diagnosis",
        "eligible_population":
            "Validated diagnosis occurrences",
        "inclusions_exclusions":
            "Source diagnosis sequences only",
        "time_logic":
            "Inherited from parent claim",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "Missing optional diagnoses remain absent",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_diagnosis row count",
        "known_limitations":
            "Occurrence count is not distinct-patient count",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M004",
        "business_name": "Procedure Occurrence Count",
        "business_definition":
            "Number of procedure occurrences across claims.",
        "formula":
            "SUM(procedure_row_count)",
        "numerator":
            "1 per FactProcedureOccurrence row",
        "denominator":
            "",
        "source_fact":
            "FactProcedureOccurrence",
        "grain":
            "Claim Procedure",
        "eligible_population":
            "Validated procedure occurrences",
        "inclusions_exclusions":
            "Source procedure sequences only",
        "time_logic":
            "Procedure date when populated; otherwise claim context",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "Missing optional procedures remain absent",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_procedure row count",
        "known_limitations":
            "Occurrence count is not distinct-patient count",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M005",
        "business_name": "Care Team Occurrence Count",
        "business_definition":
            "Number of care-team participation occurrences.",
        "formula":
            "SUM(care_team_row_count)",
        "numerator":
            "1 per FactCareTeamOccurrence row",
        "denominator":
            "",
        "source_fact":
            "FactCareTeamOccurrence",
        "grain":
            "Claim Care Team",
        "eligible_population":
            "Validated care-team occurrences",
        "inclusions_exclusions":
            "Source care-team sequences only",
        "time_logic":
            "Inherited from parent claim",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "Missing optional care-team rows remain absent",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_care_team row count",
        "known_limitations":
            "Not a distinct-provider count",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M006",
        "business_name": "Supporting Information Occurrence Count",
        "business_definition":
            "Number of supporting-information occurrences.",
        "formula":
            "SUM(supporting_info_row_count)",
        "numerator":
            "1 per FactSupportingInfoOccurrence row",
        "denominator":
            "",
        "source_fact":
            "FactSupportingInfoOccurrence",
        "grain":
            "Claim Supporting Information",
        "eligible_population":
            "Validated supporting-information rows",
        "inclusions_exclusions":
            "Source supporting-information sequences only",
        "time_logic":
            "Timing date/period when semantically applicable",
        "unit_format":
            "Count",
        "valuation_basis":
            "N/A",
        "total_behavior":
            "SUM",
        "null_rule":
            "Optional structures remain NULL/absent",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_supporting_info row count",
        "known_limitations":
            "Categories require terminology interpretation",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M007",
        "business_name":
            "Claim Total Amount ? Exact Financial Concept",
        "business_definition":
            "Sum of claim-total monetary values only when "
            "financial domain, system URI, code and currency "
            "are identical.",
        "formula":
            "SUM(amount)",
        "numerator":
            "FactClaimTotal.amount",
        "denominator":
            "",
        "source_fact":
            "FactClaimTotal",
        "grain":
            "Claim Total Element",
        "eligible_population":
            "semantic_role = MONETARY_AMOUNT",
        "inclusions_exclusions":
            "Exact domain/system/code/currency only; "
            "no claim-adjudication or item-adjudication mixing",
        "time_logic":
            "Inherited from parent claim",
        "unit_format":
            "Currency",
        "valuation_basis":
            "Authoritative exact financial concept",
        "total_behavior":
            "SUM only within exact concept and currency",
        "null_rule":
            "NULL amount excluded; never converted to zero",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_total exact concept reconciliation",
        "known_limitations":
            "Not a consolidated Paid/Allowed/Submitted KPI",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M008",
        "business_name":
            "Claim Adjudication Amount ? Exact Financial Concept",
        "business_definition":
            "Sum of claim-level adjudication monetary values "
            "only when domain, system URI, code and currency "
            "are identical.",
        "formula":
            "SUM(amount)",
        "numerator":
            "FactClaimAdjudication.amount",
        "denominator":
            "",
        "source_fact":
            "FactClaimAdjudication",
        "grain":
            "Claim Adjudication Element",
        "eligible_population":
            "semantic_role = MONETARY_AMOUNT",
        "inclusions_exclusions":
            "Exclude NON_MONETARY_VALUE and "
            "STATUS_DISCRIMINATOR; no ClaimTotal mixing",
        "time_logic":
            "Inherited from parent claim",
        "unit_format":
            "Currency",
        "valuation_basis":
            "Authoritative exact financial concept",
        "total_behavior":
            "SUM only within exact concept and currency",
        "null_rule":
            "NULL amount excluded; never converted to zero",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_adjudication exact concept reconciliation",
        "known_limitations":
            "Claim adjudication may contain non-money values",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },

    {
        "metric_id": "M009",
        "business_name":
            "Item Adjudication Amount ? Exact Financial Concept",
        "business_definition":
            "Sum of item-level adjudication monetary amounts "
            "only for one exact system URI, code and currency.",
        "formula":
            "SUM(amount)",
        "numerator":
            "FactItemAdjudication.amount",
        "denominator":
            "",
        "source_fact":
            "FactItemAdjudication",
        "grain":
            "Claim Item Adjudication Element",
        "eligible_population":
            "semantic_role = MONETARY_AMOUNT",
        "inclusions_exclusions":
            "No claim-level financial rows; exact concept only",
        "time_logic":
            "Inherited from item/claim service context",
        "unit_format":
            "Currency",
        "valuation_basis":
            "Authoritative exact financial concept",
        "total_behavior":
            "SUM only within exact concept and currency",
        "null_rule":
            "NULL amount excluded; never converted to zero",
        "directionality":
            "Contextual",
        "validation_baseline":
            "staging.eob_item_adjudication exact concept reconciliation",
        "known_limitations":
            "Must never be blindly added to claim-level totals",
        "approval_status":
            "APPROVED_ANALYTICAL_PRIMITIVE",
    },
)


REQUIRED_METRIC_FIELDS = (
    "metric_id",
    "business_name",
    "business_definition",
    "formula",
    "numerator",
    "denominator",
    "source_fact",
    "grain",
    "eligible_population",
    "inclusions_exclusions",
    "time_logic",
    "unit_format",
    "valuation_basis",
    "total_behavior",
    "null_rule",
    "directionality",
    "validation_baseline",
    "known_limitations",
    "approval_status",
)
