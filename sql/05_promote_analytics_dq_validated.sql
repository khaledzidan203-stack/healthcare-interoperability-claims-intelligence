\set ON_ERROR_STOP on

BEGIN;

DO $analytics_promotion$
DECLARE
    governance_updated INTEGER;
    analytics_updated INTEGER;
BEGIN

    UPDATE governance.pipeline_run
    SET run_status='ANALYTICS_DQ_VALIDATED'
    WHERE pipeline_run_id='run_20260930T084004Z_ingest_2db2ed86'
      AND run_status='STAGING_DQ_VALIDATED';

    GET DIAGNOSTICS governance_updated = ROW_COUNT;

    IF governance_updated <> 1 THEN
        RAISE EXCEPTION
            'Governance promotion expected 1 row; actual=%',
            governance_updated;
    END IF;


    UPDATE analytics.dim_pipeline_run
    SET run_status='ANALYTICS_DQ_VALIDATED'
    WHERE pipeline_run_id='run_20260930T084004Z_ingest_2db2ed86'
      AND run_status='STAGING_DQ_VALIDATED';

    GET DIAGNOSTICS analytics_updated = ROW_COUNT;

    IF analytics_updated <> 1 THEN
        RAISE EXCEPTION
            'Analytics promotion expected 1 row; actual=%',
            analytics_updated;
    END IF;

END
$analytics_promotion$;

COMMIT;
