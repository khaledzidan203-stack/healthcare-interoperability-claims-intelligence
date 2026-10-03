BEGIN;

-- Database must still be empty before key hardening.
DO $$
DECLARE
    total_rows BIGINT;
BEGIN
    SELECT
          (SELECT COUNT(*) FROM staging.patient)
        + (SELECT COUNT(*) FROM staging.coverage)
        + (SELECT COUNT(*) FROM staging.eob_claim)
        + (SELECT COUNT(*) FROM staging.eob_item)
        + (SELECT COUNT(*) FROM staging.eob_diagnosis)
        + (SELECT COUNT(*) FROM staging.eob_procedure)
        + (SELECT COUNT(*) FROM staging.eob_care_team)
        + (SELECT COUNT(*) FROM staging.eob_supporting_info)
        + (SELECT COUNT(*) FROM staging.eob_adjudication)
        + (SELECT COUNT(*) FROM staging.eob_total)
        + (SELECT COUNT(*) FROM staging.eob_item_adjudication)
        + (SELECT COUNT(*) FROM staging.eob_item_detail)
    INTO total_rows;

    IF total_rows <> 0 THEN
        RAISE EXCEPTION
            'STAGING must be empty before multi-run key migration. Rows=%',
            total_rows;
    END IF;
END
$$;

-- Drop only STAGING parent-child FKs.
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT
            c.conrelid::regclass AS table_name,
            c.conname
        FROM pg_constraint c
        JOIN pg_namespace n
          ON n.oid = c.connamespace
        WHERE c.contype = 'f'
          AND n.nspname = 'staging'
          AND c.confrelid IN (
              'staging.eob_claim'::regclass,
              'staging.eob_item'::regclass
          )
    LOOP
        EXECUTE format(
            'ALTER TABLE %s DROP CONSTRAINT %I',
            r.table_name,
            r.conname
        );
    END LOOP;
END
$$;

-- Drop current STAGING primary keys.
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT
            c.conrelid::regclass AS table_name,
            c.conname
        FROM pg_constraint c
        JOIN pg_namespace n
          ON n.oid = c.connamespace
        WHERE c.contype = 'p'
          AND n.nspname = 'staging'
    LOOP
        EXECUTE format(
            'ALTER TABLE %s DROP CONSTRAINT %I',
            r.table_name,
            r.conname
        );
    END LOOP;
END
$$;

ALTER TABLE staging.patient
    ADD PRIMARY KEY (
        pipeline_run_id,
        patient_id
    );

ALTER TABLE staging.coverage
    ADD PRIMARY KEY (
        pipeline_run_id,
        coverage_id
    );

ALTER TABLE staging.eob_claim
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id
    );

ALTER TABLE staging.eob_item
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        item_sequence
    );

ALTER TABLE staging.eob_diagnosis
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        diagnosis_sequence
    );

ALTER TABLE staging.eob_procedure
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        procedure_sequence
    );

ALTER TABLE staging.eob_care_team
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        careteam_sequence
    );

ALTER TABLE staging.eob_supporting_info
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        supporting_info_sequence
    );

ALTER TABLE staging.eob_adjudication
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        source_ordinal
    );

ALTER TABLE staging.eob_total
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        source_ordinal
    );

ALTER TABLE staging.eob_item_adjudication
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        item_sequence,
        source_ordinal
    );

ALTER TABLE staging.eob_item_detail
    ADD PRIMARY KEY (
        pipeline_run_id,
        eob_id,
        item_sequence,
        detail_sequence
    );

ALTER TABLE staging.eob_item
    ADD CONSTRAINT fk_eob_item_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_diagnosis
    ADD CONSTRAINT fk_eob_diagnosis_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_procedure
    ADD CONSTRAINT fk_eob_procedure_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_care_team
    ADD CONSTRAINT fk_eob_care_team_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_supporting_info
    ADD CONSTRAINT fk_eob_supporting_info_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_adjudication
    ADD CONSTRAINT fk_eob_adjudication_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_total
    ADD CONSTRAINT fk_eob_total_claim_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id
    )
    REFERENCES staging.eob_claim (
        pipeline_run_id,
        eob_id
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_item_adjudication
    ADD CONSTRAINT fk_eob_item_adjudication_item_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id,
        item_sequence
    )
    REFERENCES staging.eob_item (
        pipeline_run_id,
        eob_id,
        item_sequence
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_item_detail
    ADD CONSTRAINT fk_eob_item_detail_item_run
    FOREIGN KEY (
        pipeline_run_id,
        eob_id,
        item_sequence
    )
    REFERENCES staging.eob_item (
        pipeline_run_id,
        eob_id,
        item_sequence
    )
    ON DELETE RESTRICT;

ALTER TABLE staging.eob_supporting_info
    ALTER COLUMN timing_date TYPE DATE
    USING timing_date::date;

COMMIT;
