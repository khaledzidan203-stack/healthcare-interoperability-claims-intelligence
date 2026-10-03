BEGIN;

CREATE SCHEMA IF NOT EXISTS governance;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- ============================================================
-- GOVERNANCE
-- ============================================================

CREATE TABLE IF NOT EXISTS governance.pipeline_run (
    pipeline_run_id TEXT PRIMARY KEY,
    source_raw_run TEXT NOT NULL,
    staging_run_path TEXT,
    api_version TEXT,
    run_status TEXT NOT NULL,
    raw_manifest_sha256 CHAR(64),
    staging_manifest_sha256 CHAR(64),
    total_raw_resources INTEGER CHECK (total_raw_resources >= 0),
    total_staging_rows INTEGER CHECK (total_staging_rows >= 0),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS governance.data_quality_result (
    dq_result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_run_id TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    entity_name TEXT,
    severity TEXT NOT NULL,
    result_status TEXT NOT NULL,
    observed_value TEXT,
    expected_value TEXT,
    message TEXT,
    source_file TEXT,
    source_resource_id TEXT,
    evidence_json JSONB,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_dq_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS governance.source_exception (
    source_exception_code TEXT PRIMARY KEY,
    first_observed_pipeline_run_id TEXT,
    source_system TEXT NOT NULL,
    resource_type TEXT,
    severity TEXT NOT NULL DEFAULT 'SOURCE_WARNING',
    status TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_source_exception_pipeline
        FOREIGN KEY (first_observed_pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS governance.reconciliation_result (
    reconciliation_result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_run_id TEXT NOT NULL,
    layer_from TEXT NOT NULL,
    layer_to TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    source_count BIGINT NOT NULL,
    target_count BIGINT NOT NULL,
    difference BIGINT NOT NULL,
    result_status TEXT NOT NULL,
    evidence_json JSONB,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_reconciliation_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT
);

-- ============================================================
-- STAGING.PATIENT
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.patient (
    patient_id TEXT NOT NULL,

    birth_date DATE,
    gender TEXT,

    identifiers_json JSONB NOT NULL,
    address_json JSONB NOT NULL,
    communication_json JSONB NOT NULL,
    profiles_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, patient_id),

    CONSTRAINT fk_patient_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_patient_resource_type
        CHECK (source_resource_type = 'Patient'),

    CONSTRAINT ck_patient_source_id
        CHECK (source_resource_id = patient_id),

    CONSTRAINT ck_patient_hash
        CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

-- ============================================================
-- STAGING.COVERAGE
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.coverage (
    coverage_id TEXT NOT NULL,

    status TEXT,
    subscriber_id TEXT,
    beneficiary_reference TEXT,

    relationship_json JSONB NOT NULL,
    period_start DATE,
    period_end DATE,
    coverage_type_json JSONB NOT NULL,
    payor_json JSONB NOT NULL,
    class_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, coverage_id),

    CONSTRAINT fk_coverage_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_coverage_resource_type
        CHECK (source_resource_type = 'Coverage'),

    CONSTRAINT ck_coverage_source_id
        CHECK (source_resource_id = coverage_id),

    CONSTRAINT ck_coverage_period
        CHECK (
            period_start IS NULL
            OR period_end IS NULL
            OR period_start <= period_end
        ),

    CONSTRAINT ck_coverage_hash
        CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

-- ============================================================
-- STAGING.EOB CLAIM
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.eob_claim (
    eob_id TEXT NOT NULL,

    patient_reference TEXT,
    status TEXT,
    use TEXT,
    outcome TEXT,

    claim_type_code TEXT,
    claim_type_system TEXT,

    created TIMESTAMPTZ,

    subtype_json JSONB NOT NULL,

    billable_period_start TIMESTAMPTZ,
    billable_period_end TIMESTAMPTZ,

    provider_reference TEXT,
    insurer_reference TEXT,

    insurance_json JSONB NOT NULL,
    payment_json JSONB NOT NULL,
    profiles_json JSONB NOT NULL,

    meta_source TEXT,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id),

    CONSTRAINT fk_eob_claim_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_eob_claim_resource_type
        CHECK (source_resource_type = 'ExplanationOfBenefit'),

    CONSTRAINT ck_eob_claim_source_id
        CHECK (source_resource_id = eob_id),

    CONSTRAINT ck_eob_claim_period
        CHECK (
            billable_period_start IS NULL
            OR billable_period_end IS NULL
            OR billable_period_start <= billable_period_end
        ),

    CONSTRAINT ck_eob_claim_hash
        CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

-- ============================================================
-- STAGING.EOB ITEM
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.eob_item (
    eob_id TEXT NOT NULL,
    item_sequence INTEGER NOT NULL,

    product_service_code TEXT,
    product_service_system TEXT,

    quantity_json JSONB NOT NULL,
    serviced_date DATE,
    serviced_period_json JSONB NOT NULL,
    location_json JSONB NOT NULL,
    revenue_json JSONB NOT NULL,
    modifier_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, item_sequence),

    CONSTRAINT fk_eob_item_claim
        FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_eob_item_pipeline
        FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_eob_item_sequence
        CHECK (item_sequence > 0),

    CONSTRAINT ck_eob_item_ordinal
        CHECK (source_ordinal > 0),

    CONSTRAINT ck_eob_item_source_id
        CHECK (source_resource_id = eob_id),

    CONSTRAINT ck_eob_item_hash
        CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_diagnosis (
    eob_id TEXT NOT NULL,
    diagnosis_sequence INTEGER NOT NULL,

    diagnosis_code TEXT,
    diagnosis_system TEXT,
    diagnosis_type_json JSONB NOT NULL,
    on_admission_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, diagnosis_sequence),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (diagnosis_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_procedure (
    eob_id TEXT NOT NULL,
    procedure_sequence INTEGER NOT NULL,

    procedure_code TEXT,
    procedure_system TEXT,
    procedure_date TIMESTAMPTZ,
    procedure_type_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, procedure_sequence),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (procedure_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_care_team (
    eob_id TEXT NOT NULL,
    careteam_sequence INTEGER NOT NULL,

    provider_identifier TEXT,
    provider_identifier_system TEXT,
    provider_display TEXT,
    provider_type TEXT,

    role_json JSONB NOT NULL,
    qualification_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, careteam_sequence),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (careteam_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_supporting_info (
    eob_id TEXT NOT NULL,
    supporting_info_sequence INTEGER NOT NULL,

    category_code TEXT,
    category_system TEXT,

    code_json JSONB NOT NULL,
    timing_date DATE,
    timing_period_json JSONB NOT NULL,
    value_quantity_json JSONB NOT NULL,
    value_string TEXT,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, supporting_info_sequence),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (supporting_info_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_adjudication (
    eob_id TEXT NOT NULL,
    source_ordinal INTEGER NOT NULL,

    category_code TEXT,
    category_system TEXT,
    amount NUMERIC,
    currency TEXT,
    value NUMERIC,
    reason_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, source_ordinal),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_total (
    eob_id TEXT NOT NULL,
    source_ordinal INTEGER NOT NULL,

    category_code TEXT,
    category_system TEXT,
    amount NUMERIC,
    currency TEXT,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (pipeline_run_id, eob_id, source_ordinal),

    FOREIGN KEY (pipeline_run_id, eob_id)
        REFERENCES staging.eob_claim (pipeline_run_id, eob_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_item_adjudication (
    eob_id TEXT NOT NULL,
    item_sequence INTEGER NOT NULL,
    source_ordinal INTEGER NOT NULL,

    category_code TEXT,
    category_system TEXT,
    amount NUMERIC,
    currency TEXT,
    reason_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        item_sequence,
        source_ordinal
    ),

    FOREIGN KEY (pipeline_run_id, eob_id, item_sequence)
        REFERENCES staging.eob_item (
            pipeline_run_id,
            eob_id,
            item_sequence
        )
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (item_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE TABLE IF NOT EXISTS staging.eob_item_detail (
    eob_id TEXT NOT NULL,
    item_sequence INTEGER NOT NULL,
    detail_sequence INTEGER NOT NULL,

    product_service_code TEXT,
    product_service_system TEXT,
    quantity_json JSONB NOT NULL,

    pipeline_run_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_page_number INTEGER,
    source_resource_type TEXT NOT NULL,
    source_resource_id TEXT NOT NULL,
    parent_resource_id TEXT,
    source_sequence INTEGER,
    source_ordinal INTEGER NOT NULL,
    raw_record_hash CHAR(64) NOT NULL,
    source_fragment_json JSONB NOT NULL,

    PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        item_sequence,
        detail_sequence
    ),

    FOREIGN KEY (pipeline_run_id, eob_id, item_sequence)
        REFERENCES staging.eob_item (
            pipeline_run_id,
            eob_id,
            item_sequence
        )
        ON DELETE RESTRICT,

    FOREIGN KEY (pipeline_run_id)
        REFERENCES governance.pipeline_run (pipeline_run_id)
        ON DELETE RESTRICT,

    CHECK (item_sequence > 0),
    CHECK (detail_sequence > 0),
    CHECK (source_ordinal > 0),
    CHECK (source_resource_id = eob_id),
    CHECK (raw_record_hash ~ '^[0-9A-F]{64}$')
);

CREATE INDEX IF NOT EXISTS ix_dq_pipeline
    ON governance.data_quality_result (pipeline_run_id);

CREATE INDEX IF NOT EXISTS ix_reconciliation_pipeline
    ON governance.reconciliation_result (pipeline_run_id);

CREATE INDEX IF NOT EXISTS ix_coverage_pipeline
    ON staging.coverage (pipeline_run_id);

CREATE INDEX IF NOT EXISTS ix_eob_claim_pipeline
    ON staging.eob_claim (pipeline_run_id);

CREATE INDEX IF NOT EXISTS ix_eob_item_claim
    ON staging.eob_item (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_diagnosis_claim
    ON staging.eob_diagnosis (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_procedure_claim
    ON staging.eob_procedure (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_care_team_claim
    ON staging.eob_care_team (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_supporting_info_claim
    ON staging.eob_supporting_info (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_adjudication_claim
    ON staging.eob_adjudication (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_total_claim
    ON staging.eob_total (eob_id);

CREATE INDEX IF NOT EXISTS ix_eob_item_adjudication_item
    ON staging.eob_item_adjudication (
        eob_id,
        item_sequence
    );

CREATE INDEX IF NOT EXISTS ix_eob_item_detail_item
    ON staging.eob_item_detail (
        eob_id,
        item_sequence
    );

COMMIT;
