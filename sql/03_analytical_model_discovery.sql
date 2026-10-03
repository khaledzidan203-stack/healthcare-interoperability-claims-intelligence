-- Healthcare Interoperability & Claims Intelligence Platform
-- Checkpoint 4A
-- Analytical Model Discovery
--
-- Required psql variable:
--   pipeline_run_id
--
-- Read-only discovery only.

SELECT
    status,
    use,
    outcome,
    claim_type_system,
    claim_type_code,
    COUNT(*) AS claim_count
FROM staging.eob_claim
WHERE pipeline_run_id = :'pipeline_run_id'
GROUP BY
    status,
    use,
    outcome,
    claim_type_system,
    claim_type_code
ORDER BY claim_count DESC;

WITH coded AS (

    SELECT
        'claim_type' AS domain,
        claim_type_system AS system,
        claim_type_code AS code
    FROM staging.eob_claim
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'item_product_service',
        product_service_system,
        product_service_code
    FROM staging.eob_item
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'diagnosis',
        diagnosis_system,
        diagnosis_code
    FROM staging.eob_diagnosis
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'procedure',
        procedure_system,
        procedure_code
    FROM staging.eob_procedure
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'supporting_info_category',
        category_system,
        category_code
    FROM staging.eob_supporting_info
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'claim_adjudication_category',
        category_system,
        category_code
    FROM staging.eob_adjudication
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'claim_total_category',
        category_system,
        category_code
    FROM staging.eob_total
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'item_adjudication_category',
        category_system,
        category_code
    FROM staging.eob_item_adjudication
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'item_detail_product_service',
        product_service_system,
        product_service_code
    FROM staging.eob_item_detail
    WHERE pipeline_run_id = :'pipeline_run_id'
)

SELECT
    domain,
    system,
    COUNT(*) AS row_count,
    COUNT(code) AS coded_row_count,
    COUNT(DISTINCT code) AS distinct_code_count
FROM coded
GROUP BY domain, system
ORDER BY domain, system;

WITH financial AS (

    SELECT
        'claim_adjudication' AS domain,
        category_system,
        category_code,
        currency,
        amount,
        value
    FROM staging.eob_adjudication
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'claim_total',
        category_system,
        category_code,
        currency,
        amount,
        NULL::NUMERIC
    FROM staging.eob_total
    WHERE pipeline_run_id = :'pipeline_run_id'

    UNION ALL

    SELECT
        'item_adjudication',
        category_system,
        category_code,
        currency,
        amount,
        NULL::NUMERIC
    FROM staging.eob_item_adjudication
    WHERE pipeline_run_id = :'pipeline_run_id'
)

SELECT
    domain,
    category_system,
    category_code,
    currency,
    COUNT(*) AS row_count,
    COUNT(amount) AS amount_row_count,
    SUM(amount) AS raw_amount_sum,
    COUNT(value) AS value_row_count,
    SUM(value) AS raw_value_sum
FROM financial
GROUP BY
    domain,
    category_system,
    category_code,
    currency
ORDER BY domain, category_system, category_code, currency;
