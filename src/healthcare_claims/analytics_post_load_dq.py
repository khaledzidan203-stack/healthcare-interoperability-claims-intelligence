
FACT_SOURCE_MAP = {
    "fact_claim": "eob_claim",
    "fact_item": "eob_item",
    "fact_claim_total": "eob_total",
    "fact_claim_adjudication": "eob_adjudication",
    "fact_item_adjudication": "eob_item_adjudication",
    "fact_diagnosis_occurrence": "eob_diagnosis",
    "fact_procedure_occurrence": "eob_procedure",
    "fact_care_team_occurrence": "eob_care_team",
    "fact_supporting_info_occurrence": "eob_supporting_info",
    "fact_item_detail": "eob_item_detail",
}


FACT_BUSINESS_KEYS = {
    "fact_claim":
        ("pipeline_run_key", "eob_id"),

    "fact_item":
        ("pipeline_run_key", "eob_id", "item_sequence"),

    "fact_claim_total":
        ("pipeline_run_key", "eob_id", "source_ordinal"),

    "fact_claim_adjudication":
        ("pipeline_run_key", "eob_id", "source_ordinal"),

    "fact_item_adjudication":
        (
            "pipeline_run_key",
            "eob_id",
            "item_sequence",
            "source_ordinal",
        ),

    "fact_diagnosis_occurrence":
        (
            "pipeline_run_key",
            "eob_id",
            "diagnosis_sequence",
        ),

    "fact_procedure_occurrence":
        (
            "pipeline_run_key",
            "eob_id",
            "procedure_sequence",
        ),

    "fact_care_team_occurrence":
        (
            "pipeline_run_key",
            "eob_id",
            "careteam_sequence",
        ),

    "fact_supporting_info_occurrence":
        (
            "pipeline_run_key",
            "eob_id",
            "supporting_info_sequence",
        ),

    "fact_item_detail":
        (
            "pipeline_run_key",
            "eob_id",
            "item_sequence",
            "detail_sequence",
        ),
}


def hash_multiset_sql(
    staging_table,
    analytics_table,
    pipeline_run_id,
):

    return f'''
WITH source_hashes AS (
    SELECT
        raw_record_hash AS record_hash,
        COUNT(*) AS row_count
    FROM staging.{staging_table}
    WHERE pipeline_run_id='{pipeline_run_id}'
    GROUP BY raw_record_hash
),
analytics_hashes AS (
    SELECT
        f.source_record_hash AS record_hash,
        COUNT(*) AS row_count
    FROM analytics.{analytics_table} f
    JOIN analytics.dim_pipeline_run pr
      ON pr.pipeline_run_key=f.pipeline_run_key
    WHERE pr.pipeline_run_id='{pipeline_run_id}'
    GROUP BY f.source_record_hash
)
SELECT COUNT(*)
FROM source_hashes s
FULL OUTER JOIN analytics_hashes a
  ON a.record_hash=s.record_hash
WHERE COALESCE(s.row_count,0)
   <> COALESCE(a.row_count,0);
'''


def duplicate_key_sql(
    analytics_table,
    keys,
):

    key_expression = ", ".join(keys)

    return f'''
SELECT COUNT(*)
FROM (
    SELECT
        {key_expression},
        COUNT(*) AS row_count
    FROM analytics.{analytics_table}
    GROUP BY {key_expression}
    HAVING COUNT(*) > 1
) x;
'''


def wrong_run_sql(
    analytics_table,
    pipeline_run_id,
):

    return f'''
SELECT COUNT(*)
FROM analytics.{analytics_table} f
JOIN analytics.dim_pipeline_run pr
  ON pr.pipeline_run_key=f.pipeline_run_key
WHERE pr.pipeline_run_id <> '{pipeline_run_id}';
'''
