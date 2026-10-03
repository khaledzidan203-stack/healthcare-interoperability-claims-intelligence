from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

DDL = (
    ROOT
    / "sql"
    / "04_create_analytics_model.sql"
)


FACT_TABLES = (
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
)


DIMENSION_TABLES = (
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
)


class AnalyticsDDLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.text = DDL.read_text(
            encoding="utf-8"
        )

        cls.upper = cls.text.upper()

        pattern = re.compile(
            r"CREATE TABLE IF NOT EXISTS "
            r"analytics\.(\w+)\s*\((.*?)\n\);",
            re.IGNORECASE
            | re.DOTALL,
        )

        cls.bodies = {
            name.lower(): body
            for name, body
            in pattern.findall(
                cls.text
            )
        }

    def test_table_inventory(self):

        expected = (
            set(FACT_TABLES)
            | set(DIMENSION_TABLES)
            | {"bridge_claim_coverage"}
        )

        self.assertEqual(
            set(self.bodies),
            expected,
        )

        self.assertEqual(
            len(self.bodies),
            24,
        )

    def test_relationship_count_matches_design(self):

        count = len(
            re.findall(
                r"REFERENCES\s+analytics\.",
                self.text,
                flags=re.IGNORECASE,
            )
        )

        self.assertEqual(
            count,
            53,
        )

    def test_no_direct_fact_to_fact_foreign_keys(self):

        for fact in FACT_TABLES:

            body = self.bodies[
                fact
            ]

            self.assertNotRegex(
                body,
                r"REFERENCES\s+analytics\.fact_",
            )

    def test_bridge_is_only_physical_fact_reference(self):

        body = self.bodies[
            "bridge_claim_coverage"
        ]

        self.assertIn(
            "REFERENCES analytics.fact_claim",
            body,
        )

    def test_all_facts_use_core_conformed_dimensions(self):

        for fact in FACT_TABLES:

            body = self.bodies[
                fact
            ]

            for dimension in (
                "dim_pipeline_run",
                "dim_patient",
                "dim_date",
            ):

                self.assertIn(
                    (
                        "REFERENCES "
                        f"analytics.{dimension}"
                    ),
                    body,
                )

    def test_financial_facts_use_financial_dimensions(self):

        for fact in (
            "fact_claim_total",
            "fact_claim_adjudication",
            "fact_item_adjudication",
        ):

            body = self.bodies[
                fact
            ]

            self.assertIn(
                "REFERENCES analytics.dim_financial_concept",
                body,
            )

            self.assertIn(
                "REFERENCES analytics.dim_currency",
                body,
            )

    def test_coverage_bridge_is_nullable_and_load_gated(self):

        body = self.bodies[
            "bridge_claim_coverage"
        ]

        self.assertRegex(
            body,
            r"coverage_key\s+BIGINT\s+NULL",
        )

        self.assertIn(
            "REFERENCES analytics.dim_coverage",
            body,
        )

        self.assertIn(
            "coverage_resolution_status",
            body,
        )

    def test_provider_unknown_member_is_explicitly_supported(self):

        body = self.bodies[
            "dim_provider"
        ]

        self.assertIn(
            "is_unknown BOOLEAN",
            body,
        )

        self.assertIn(
            "identity_status TEXT NOT NULL",
            body,
        )

        claim = self.bodies[
            "fact_claim"
        ]

        self.assertRegex(
            claim,
            r"provider_key\s+BIGINT\s+NOT NULL",
        )

    def test_patient_and_coverage_support_scd2(self):

        for dimension in (
            "dim_patient",
            "dim_coverage",
        ):

            body = self.bodies[
                dimension
            ]

            self.assertIn(
                "valid_from_pipeline_run_id",
                body,
            )

            self.assertIn(
                "valid_to_pipeline_run_id",
                body,
            )

            self.assertIn(
                "is_current BOOLEAN NOT NULL",
                body,
            )

    def test_ddl_is_non_destructive(self):

        for token in (
            "DROP TABLE",
            "DROP SCHEMA",
            "TRUNCATE ",
            "DELETE FROM",
            "UPDATE ",
            "INSERT INTO",
        ):

            self.assertNotIn(
                token,
                self.upper,
            )


if __name__ == "__main__":
    unittest.main()
