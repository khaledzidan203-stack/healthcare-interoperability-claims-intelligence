
from pathlib import Path
import re


ENTITY_ORDER = (
    "dim_date",
    "dim_pipeline_run",
    "dim_patient",
    "dim_coverage",
    "dim_financial_concept",
    "dim_currency",
    "dim_claim_type",
    "dim_service_code",
    "dim_diagnosis",
    "dim_procedure",
    "dim_provider",
    "dim_payer",
    "dim_supporting_info_category",
    "fact_claim",
    "fact_item",
    "fact_claim_total",
    "fact_claim_adjudication",
    "fact_item_adjudication",
    "fact_diagnosis_occurrence",
    "fact_procedure_occurrence",
    "fact_care_team_occurrence",
    "fact_supporting_info_occurrence",
    "fact_item_detail",
    "bridge_claim_coverage",
)


def _validated_hash(value):

    value = str(value).upper()

    if not re.fullmatch(
        r"[0-9A-F]{64}",
        value,
    ):
        raise ValueError(
            "Invalid SHA256"
        )

    return value


def _copy_path(path):

    value = (
        Path(path)
        .resolve()
        .as_posix()
        .replace(
            "'",
            "''",
        )
    )

    return value


def render_transaction(
    csv_paths,
    staging_manifest_sha256,
    expected_counts,
):

    if set(csv_paths) != set(ENTITY_ORDER):
        raise ValueError(
            "CSV entity inventory mismatch"
        )

    if set(expected_counts) != set(ENTITY_ORDER):
        raise ValueError(
            "Expected-count inventory mismatch"
        )

    staging_hash = _validated_hash(
        staging_manifest_sha256
    )

    parts = [
        r"\set ON_ERROR_STOP on",
        "",
        "BEGIN;",
        "",
    ]

    for entity in ENTITY_ORDER:

        path = _copy_path(
            csv_paths[entity]
        )

        parts += [
            (
                f"CREATE TEMP TABLE "
                f"load_{entity} ("
                f"payload JSONB NOT NULL"
                f") ON COMMIT DROP;"
            ),
            (
                rf"\copy load_{entity}(payload) "
                rf"FROM '{path}' "
                rf"WITH (FORMAT csv, ENCODING 'UTF8');"
            ),
            "",
        ]

    parts.append(
r'''
INSERT INTO analytics.dim_date (
    date_key,
    calendar_date,
    calendar_year,
    calendar_quarter,
    month_number,
    month_name,
    day_of_month,
    day_of_week,
    day_name,
    is_weekend
)
SELECT
    (payload->>'date_key')::INTEGER,
    (payload->>'calendar_date')::DATE,
    (payload->>'calendar_year')::SMALLINT,
    (payload->>'calendar_quarter')::SMALLINT,
    (payload->>'month_number')::SMALLINT,
    payload->>'month_name',
    (payload->>'day_of_month')::SMALLINT,
    (payload->>'day_of_week')::SMALLINT,
    payload->>'day_name',
    (payload->>'is_weekend')::BOOLEAN
FROM load_dim_date;


INSERT INTO analytics.dim_pipeline_run (
    pipeline_run_id,
    run_status,
    raw_manifest_sha256,
    staging_manifest_sha256
)
SELECT
    payload->>'pipeline_run_id',
    payload->>'run_status',
    NULLIF(
        payload->>'raw_manifest_sha256',
        ''
    ),
    COALESCE(
        NULLIF(
            payload->>'staging_manifest_sha256',
            ''
        ),
        '__STAGING_HASH__'
    )
FROM load_dim_pipeline_run;


INSERT INTO analytics.dim_patient (
    source_system,
    patient_id,
    birth_date,
    gender,
    valid_from_pipeline_run_id,
    valid_to_pipeline_run_id,
    is_current,
    row_hash,
    attributes_json
)
SELECT
    payload->>'source_system',
    payload->>'patient_id',
    NULLIF(
        payload->>'birth_date',
        ''
    )::DATE,
    NULLIF(
        payload->>'gender',
        ''
    ),
    payload->>'valid_from_pipeline_run_id',
    NULLIF(
        payload->>'valid_to_pipeline_run_id',
        ''
    ),
    (payload->>'is_current')::BOOLEAN,
    payload->>'row_hash',
    NULLIF(
        payload->>'attributes_json',
        ''
    )::JSONB
FROM load_dim_patient;


INSERT INTO analytics.dim_coverage (
    source_system,
    coverage_id,
    coverage_status,
    subscriber_id,
    period_start,
    period_end,
    valid_from_pipeline_run_id,
    valid_to_pipeline_run_id,
    is_current,
    row_hash,
    attributes_json
)
SELECT
    payload->>'source_system',
    payload->>'coverage_id',
    NULLIF(
        payload->>'coverage_status',
        ''
    ),
    NULLIF(
        payload->>'subscriber_id',
        ''
    ),
    NULLIF(
        payload->>'period_start',
        ''
    )::DATE,
    NULLIF(
        payload->>'period_end',
        ''
    )::DATE,
    payload->>'valid_from_pipeline_run_id',
    NULLIF(
        payload->>'valid_to_pipeline_run_id',
        ''
    ),
    (payload->>'is_current')::BOOLEAN,
    payload->>'row_hash',
    NULLIF(
        payload->>'attributes_json',
        ''
    )::JSONB
FROM load_dim_coverage;


INSERT INTO analytics.dim_financial_concept (
    system_uri,
    code,
    authority_version,
    authoritative_display,
    semantic_role,
    aggregation_rule,
    authority,
    authority_url,
    resolution_status,
    kpi_status
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    payload->>'authority_version',
    payload->>'authoritative_display',
    payload->>'semantic_role',
    payload->>'aggregation_rule',
    payload->>'authority',
    payload->>'authority_url',
    payload->>'resolution_status',
    payload->>'kpi_status'
FROM load_dim_financial_concept;


INSERT INTO analytics.dim_currency (
    currency_code,
    currency_name
)
SELECT
    payload->>'currency_code',
    NULLIF(
        payload->>'currency_name',
        ''
    )
FROM load_dim_currency;


INSERT INTO analytics.dim_claim_type (
    system_uri,
    code,
    source_display,
    authoritative_display,
    mapping_status,
    authority,
    authority_version
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    NULLIF(
        payload->>'source_display',
        ''
    ),
    NULLIF(
        payload->>'authoritative_display',
        ''
    ),
    payload->>'mapping_status',
    NULLIF(
        payload->>'authority',
        ''
    ),
    NULLIF(
        payload->>'authority_version',
        ''
    )
FROM load_dim_claim_type;


INSERT INTO analytics.dim_service_code (
    system_uri,
    code,
    source_display,
    authoritative_display,
    mapping_status,
    authority,
    authority_version
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    NULLIF(
        payload->>'source_display',
        ''
    ),
    NULLIF(
        payload->>'authoritative_display',
        ''
    ),
    payload->>'mapping_status',
    NULLIF(
        payload->>'authority',
        ''
    ),
    NULLIF(
        payload->>'authority_version',
        ''
    )
FROM load_dim_service_code;


INSERT INTO analytics.dim_diagnosis (
    system_uri,
    code,
    source_display,
    authoritative_display,
    mapping_status,
    authority,
    authority_version
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    NULLIF(
        payload->>'source_display',
        ''
    ),
    NULLIF(
        payload->>'authoritative_display',
        ''
    ),
    payload->>'mapping_status',
    NULLIF(
        payload->>'authority',
        ''
    ),
    NULLIF(
        payload->>'authority_version',
        ''
    )
FROM load_dim_diagnosis;


INSERT INTO analytics.dim_procedure (
    system_uri,
    code,
    source_display,
    authoritative_display,
    mapping_status,
    authority,
    authority_version
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    NULLIF(
        payload->>'source_display',
        ''
    ),
    NULLIF(
        payload->>'authoritative_display',
        ''
    ),
    payload->>'mapping_status',
    NULLIF(
        payload->>'authority',
        ''
    ),
    NULLIF(
        payload->>'authority_version',
        ''
    )
FROM load_dim_procedure;


INSERT INTO analytics.dim_provider (
    identity_key_sha256,
    identity_status,
    target_resource_type,
    identifier_system,
    identifier_value,
    display,
    is_unknown,
    attributes_json
)
SELECT
    NULLIF(
        payload->>'identity_key_sha256',
        ''
    ),
    payload->>'identity_status',
    NULLIF(
        payload->>'target_resource_type',
        ''
    ),
    NULLIF(
        payload->>'identifier_system',
        ''
    ),
    NULLIF(
        payload->>'identifier_value',
        ''
    ),
    NULLIF(
        payload->>'display',
        ''
    ),
    (payload->>'is_unknown')::BOOLEAN,
    NULLIF(
        payload->>'attributes_json',
        ''
    )::JSONB
FROM load_dim_provider;


INSERT INTO analytics.dim_payer (
    identity_key_sha256,
    identity_status,
    target_resource_type,
    identifier_system,
    identifier_value,
    display,
    is_unknown,
    attributes_json
)
SELECT
    NULLIF(
        payload->>'identity_key_sha256',
        ''
    ),
    payload->>'identity_status',
    NULLIF(
        payload->>'target_resource_type',
        ''
    ),
    NULLIF(
        payload->>'identifier_system',
        ''
    ),
    NULLIF(
        payload->>'identifier_value',
        ''
    ),
    NULLIF(
        payload->>'display',
        ''
    ),
    (payload->>'is_unknown')::BOOLEAN,
    NULLIF(
        payload->>'attributes_json',
        ''
    )::JSONB
FROM load_dim_payer;


INSERT INTO analytics.dim_supporting_info_category (
    system_uri,
    code,
    source_display,
    authoritative_display,
    mapping_status,
    authority,
    authority_version
)
SELECT
    payload->>'system_uri',
    payload->>'code',
    NULLIF(
        payload->>'source_display',
        ''
    ),
    NULLIF(
        payload->>'authoritative_display',
        ''
    ),
    payload->>'mapping_status',
    NULLIF(
        payload->>'authority',
        ''
    ),
    NULLIF(
        payload->>'authority_version',
        ''
    )
FROM load_dim_supporting_info_category;


INSERT INTO analytics.fact_claim (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    billable_start_date_key,
    billable_end_date_key,
    claim_type_key,
    provider_key,
    payer_key,
    eob_id,
    claim_status,
    claim_use,
    claim_outcome,
    claim_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    NULLIF(
        s.payload->>'billable_start_date_key',
        ''
    )::INTEGER,
    NULLIF(
        s.payload->>'billable_end_date_key',
        ''
    )::INTEGER,
    ct.claim_type_key,
    prov.provider_key,
    pay.payer_key,
    s.payload->>'eob_id',
    NULLIF(
        s.payload->>'claim_status',
        ''
    ),
    NULLIF(
        s.payload->>'claim_use',
        ''
    ),
    NULLIF(
        s.payload->>'claim_outcome',
        ''
    ),
    (s.payload->>'claim_row_count')::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_claim s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_claim_type ct
  ON ct.system_uri =
     NULLIF(
         s.payload->>'claim_type_system_uri',
         ''
     )
 AND ct.code =
     NULLIF(
         s.payload->>'claim_type_code',
         ''
     )
JOIN analytics.dim_provider prov
  ON (
       (
         (s.payload->>'provider_is_unknown')::BOOLEAN
         AND prov.is_unknown
       )
       OR
       (
         NOT (
             s.payload->>'provider_is_unknown'
         )::BOOLEAN
         AND prov.identity_key_sha256 =
             s.payload->>'provider_identity_key_sha256'
       )
     )
LEFT JOIN analytics.dim_payer pay
  ON pay.identity_key_sha256 =
     NULLIF(
         s.payload->>'payer_identity_key_sha256',
         ''
     );


INSERT INTO analytics.fact_item (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    serviced_date_key,
    service_code_key,
    eob_id,
    item_sequence,
    quantity_value,
    quantity_unit,
    item_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    NULLIF(
        s.payload->>'serviced_date_key',
        ''
    )::INTEGER,
    svc.service_code_key,
    s.payload->>'eob_id',
    (s.payload->>'item_sequence')::INTEGER,
    NULLIF(
        s.payload->>'quantity_value',
        ''
    )::NUMERIC(24,6),
    NULLIF(
        s.payload->>'quantity_unit',
        ''
    ),
    (s.payload->>'item_row_count')::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_item s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_service_code svc
  ON svc.system_uri =
     NULLIF(
         s.payload->>'service_system_uri',
         ''
     )
 AND svc.code =
     NULLIF(
         s.payload->>'service_code',
         ''
     );


INSERT INTO analytics.fact_claim_total (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    financial_concept_key,
    currency_key,
    eob_id,
    source_ordinal,
    amount,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    fin.financial_concept_key,
    cur.currency_key,
    s.payload->>'eob_id',
    (s.payload->>'source_ordinal')::INTEGER,
    NULLIF(
        s.payload->>'amount',
        ''
    )::NUMERIC(24,6),
    s.payload->>'source_record_hash'
FROM load_fact_claim_total s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_financial_concept fin
  ON fin.system_uri =
     s.payload->>'financial_system_uri'
 AND fin.code =
     s.payload->>'financial_code'
 AND fin.authority_version =
     s.payload->>'financial_authority_version'
LEFT JOIN analytics.dim_currency cur
  ON cur.currency_code =
     NULLIF(
         s.payload->>'currency_code',
         ''
     );


INSERT INTO analytics.fact_claim_adjudication (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    financial_concept_key,
    currency_key,
    eob_id,
    source_ordinal,
    amount,
    value,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    fin.financial_concept_key,
    cur.currency_key,
    s.payload->>'eob_id',
    (s.payload->>'source_ordinal')::INTEGER,
    NULLIF(
        s.payload->>'amount',
        ''
    )::NUMERIC(24,6),
    NULLIF(
        s.payload->>'value',
        ''
    )::NUMERIC(24,6),
    s.payload->>'source_record_hash'
FROM load_fact_claim_adjudication s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_financial_concept fin
  ON fin.system_uri =
     s.payload->>'financial_system_uri'
 AND fin.code =
     s.payload->>'financial_code'
 AND fin.authority_version =
     s.payload->>'financial_authority_version'
LEFT JOIN analytics.dim_currency cur
  ON cur.currency_code =
     NULLIF(
         s.payload->>'currency_code',
         ''
     );


INSERT INTO analytics.fact_item_adjudication (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    financial_concept_key,
    currency_key,
    eob_id,
    item_sequence,
    source_ordinal,
    amount,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    fin.financial_concept_key,
    cur.currency_key,
    s.payload->>'eob_id',
    (s.payload->>'item_sequence')::INTEGER,
    (s.payload->>'source_ordinal')::INTEGER,
    NULLIF(
        s.payload->>'amount',
        ''
    )::NUMERIC(24,6),
    s.payload->>'source_record_hash'
FROM load_fact_item_adjudication s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_financial_concept fin
  ON fin.system_uri =
     s.payload->>'financial_system_uri'
 AND fin.code =
     s.payload->>'financial_code'
 AND fin.authority_version =
     s.payload->>'financial_authority_version'
LEFT JOIN analytics.dim_currency cur
  ON cur.currency_code =
     NULLIF(
         s.payload->>'currency_code',
         ''
     );


INSERT INTO analytics.fact_diagnosis_occurrence (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    diagnosis_key,
    eob_id,
    diagnosis_sequence,
    diagnosis_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    dx.diagnosis_key,
    s.payload->>'eob_id',
    (s.payload->>'diagnosis_sequence')::INTEGER,
    (s.payload->>'diagnosis_row_count')::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_diagnosis_occurrence s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_diagnosis dx
  ON dx.system_uri =
     NULLIF(
         s.payload->>'diagnosis_system_uri',
         ''
     )
 AND dx.code =
     NULLIF(
         s.payload->>'diagnosis_code',
         ''
     );


INSERT INTO analytics.fact_procedure_occurrence (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    procedure_date_key,
    procedure_key,
    eob_id,
    procedure_sequence,
    procedure_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    NULLIF(
        s.payload->>'procedure_date_key',
        ''
    )::INTEGER,
    proc.procedure_key,
    s.payload->>'eob_id',
    (s.payload->>'procedure_sequence')::INTEGER,
    (s.payload->>'procedure_row_count')::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_procedure_occurrence s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_procedure proc
  ON proc.system_uri =
     NULLIF(
         s.payload->>'procedure_system_uri',
         ''
     )
 AND proc.code =
     NULLIF(
         s.payload->>'procedure_code',
         ''
     );


INSERT INTO analytics.fact_care_team_occurrence (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    provider_key,
    eob_id,
    careteam_sequence,
    role_json,
    qualification_json,
    care_team_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    prov.provider_key,
    s.payload->>'eob_id',
    (s.payload->>'careteam_sequence')::INTEGER,
    NULLIF(
        s.payload->>'role_json',
        ''
    )::JSONB,
    NULLIF(
        s.payload->>'qualification_json',
        ''
    )::JSONB,
    (s.payload->>'care_team_row_count')::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_care_team_occurrence s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_provider prov
  ON prov.identity_key_sha256 =
     s.payload->>'provider_identity_key_sha256'
 AND prov.is_unknown = FALSE;


INSERT INTO analytics.fact_supporting_info_occurrence (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    timing_date_key,
    supporting_info_category_key,
    eob_id,
    supporting_info_sequence,
    value_string,
    code_json,
    value_quantity_json,
    supporting_info_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    NULLIF(
        s.payload->>'timing_date_key',
        ''
    )::INTEGER,
    cat.supporting_info_category_key,
    s.payload->>'eob_id',
    (s.payload->>'supporting_info_sequence')::INTEGER,
    NULLIF(
        s.payload->>'value_string',
        ''
    ),
    NULLIF(
        s.payload->>'code_json',
        ''
    )::JSONB,
    NULLIF(
        s.payload->>'value_quantity_json',
        ''
    )::JSONB,
    (
        s.payload->>'supporting_info_row_count'
    )::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_supporting_info_occurrence s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_supporting_info_category cat
  ON cat.system_uri =
     NULLIF(
         s.payload->>'supporting_info_system_uri',
         ''
     )
 AND cat.code =
     NULLIF(
         s.payload->>'supporting_info_code',
         ''
     );


INSERT INTO analytics.fact_item_detail (
    pipeline_run_key,
    patient_key,
    claim_created_date_key,
    service_code_key,
    eob_id,
    item_sequence,
    detail_sequence,
    quantity_value,
    quantity_unit,
    item_detail_row_count,
    source_record_hash
)
SELECT
    pr.pipeline_run_key,
    pat.patient_key,
    (s.payload->>'claim_created_date_key')::INTEGER,
    svc.service_code_key,
    s.payload->>'eob_id',
    (s.payload->>'item_sequence')::INTEGER,
    (s.payload->>'detail_sequence')::INTEGER,
    NULLIF(
        s.payload->>'quantity_value',
        ''
    )::NUMERIC(24,6),
    NULLIF(
        s.payload->>'quantity_unit',
        ''
    ),
    (
        s.payload->>'item_detail_row_count'
    )::SMALLINT,
    s.payload->>'source_record_hash'
FROM load_fact_item_detail s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.dim_patient pat
  ON pat.source_system =
     s.payload->>'patient_source_system'
 AND pat.patient_id =
     s.payload->>'patient_id'
 AND pat.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id'
LEFT JOIN analytics.dim_service_code svc
  ON svc.system_uri =
     NULLIF(
         s.payload->>'service_system_uri',
         ''
     )
 AND svc.code =
     NULLIF(
         s.payload->>'service_code',
         ''
     );


INSERT INTO analytics.bridge_claim_coverage (
    association_key_sha256,
    pipeline_run_key,
    fact_claim_key,
    coverage_key,
    insurance_ordinal,
    focal,
    coverage_reference_form,
    coverage_resolution_status,
    coverage_display,
    source_record_hash
)
SELECT
    s.payload->>'association_key_sha256',
    pr.pipeline_run_key,
    claim.fact_claim_key,
    cov.coverage_key,
    (s.payload->>'insurance_ordinal')::INTEGER,
    NULLIF(
        s.payload->>'focal',
        ''
    )::BOOLEAN,
    s.payload->>'coverage_reference_form',
    s.payload->>'coverage_resolution_status',
    NULLIF(
        s.payload->>'coverage_display',
        ''
    ),
    s.payload->>'source_record_hash'
FROM load_bridge_claim_coverage s
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_id =
     s.payload->>'pipeline_run_id'
JOIN analytics.fact_claim claim
  ON claim.pipeline_run_key =
     pr.pipeline_run_key
 AND claim.eob_id =
     s.payload->>'eob_id'
LEFT JOIN analytics.dim_coverage cov
  ON NULLIF(
         s.payload->>'coverage_id',
         ''
     ) IS NOT NULL
 AND cov.source_system =
     s.payload->>'coverage_source_system'
 AND cov.coverage_id =
     s.payload->>'coverage_id'
 AND cov.valid_from_pipeline_run_id =
     s.payload->>'pipeline_run_id';
'''
    )

    parts[-1] = parts[-1].replace(
        "__STAGING_HASH__",
        staging_hash,
    )

    check_lines = [
        "DO $analytics_reconcile$",
        "DECLARE",
        "    actual_count BIGINT;",
        "BEGIN",
    ]

    for entity in ENTITY_ORDER:

        expected = int(
            expected_counts[entity]
        )

        check_lines += [
            (
                f"    SELECT COUNT(*) "
                f"INTO actual_count "
                f"FROM analytics.{entity};"
            ),
            (
                f"    IF actual_count <> {expected} THEN"
            ),
            (
                "        RAISE EXCEPTION "
                f"'Analytics count mismatch: {entity} "
                f"expected={expected} actual=%', "
                "actual_count;"
            ),
            "    END IF;",
        ]

    check_lines += [
r'''
    SELECT COUNT(*)
    INTO actual_count
    FROM analytics.dim_provider
    WHERE is_unknown = TRUE;

    IF actual_count <> 1 THEN
        RAISE EXCEPTION
        'Unknown Provider member count expected=1 actual=%',
        actual_count;
    END IF;


    SELECT COUNT(*)
    INTO actual_count
    FROM analytics.fact_claim fc
    JOIN analytics.dim_provider dp
      ON dp.provider_key =
         fc.provider_key
    WHERE dp.is_unknown = TRUE;

    IF actual_count <> 2 THEN
        RAISE EXCEPTION
        'Claims mapped to Unknown Provider expected=2 actual=%',
        actual_count;
    END IF;


    SELECT COUNT(*)
    INTO actual_count
    FROM analytics.bridge_claim_coverage
    WHERE coverage_key IS NOT NULL;

    IF actual_count <> 0 THEN
        RAISE EXCEPTION
        'Explicit current-run Coverage links expected=0 actual=%',
        actual_count;
    END IF;


    SELECT COUNT(*)
    INTO actual_count
    FROM analytics.bridge_claim_coverage
    WHERE coverage_key IS NULL
      AND coverage_resolution_status =
          'DISPLAY_ONLY_NON_IDENTITY';

    IF actual_count <> 6 THEN
        RAISE EXCEPTION
        'Display-only Coverage bridge rows expected=6 actual=%',
        actual_count;
    END IF;

END
$analytics_reconcile$;

COMMIT;
'''
    ]

    parts.extend(
        check_lines
    )

    return "\n".join(
        parts
    ) + "\n"
