
import unittest

from healthcare_claims.analytics_post_load_dq import (
    FACT_BUSINESS_KEYS,
    FACT_SOURCE_MAP,
    duplicate_key_sql,
    hash_multiset_sql,
    wrong_run_sql,
)


class AnalyticsPostLoadDQTests(unittest.TestCase):

    def test_physical_staging_names_have_no_stg_prefix(self):

        self.assertEqual(
            len(FACT_SOURCE_MAP),
            10,
        )

        for table in FACT_SOURCE_MAP.values():

            self.assertFalse(
                table.startswith("stg_")
            )

    def test_fact_grain_contract_has_10_facts(self):

        self.assertEqual(
            len(FACT_BUSINESS_KEYS),
            10,
        )

    def test_hash_reconciliation_uses_multiset_logic(self):

        sql = hash_multiset_sql(
            "eob_item",
            "fact_item",
            "run1",
        ).upper()

        self.assertIn(
            "FULL OUTER JOIN",
            sql,
        )

        self.assertIn(
            "RAW_RECORD_HASH",
            sql,
        )

        self.assertIn(
            "SOURCE_RECORD_HASH",
            sql,
        )

    def test_duplicate_check_uses_grouping(self):

        sql = duplicate_key_sql(
            "fact_item",
            (
                "pipeline_run_key",
                "eob_id",
                "item_sequence",
            ),
        ).upper()

        self.assertIn(
            "HAVING COUNT(*) > 1",
            sql,
        )

    def test_validation_queries_are_read_only(self):

        sql = (
            hash_multiset_sql(
                "eob_item",
                "fact_item",
                "run1",
            )
            + duplicate_key_sql(
                "fact_item",
                (
                    "pipeline_run_key",
                    "eob_id",
                    "item_sequence",
                ),
            )
            + wrong_run_sql(
                "fact_item",
                "run1",
            )
        ).upper()

        for token in (
            "INSERT INTO",
            "UPDATE ",
            "DELETE FROM",
            "TRUNCATE ",
            "DROP TABLE",
            "DROP SCHEMA",
        ):

            self.assertNotIn(
                token,
                sql,
            )


if __name__ == "__main__":
    unittest.main()
