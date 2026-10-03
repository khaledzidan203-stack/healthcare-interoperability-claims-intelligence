from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DDL = ROOT / "sql" / "01_create_foundation.sql"


class DatabaseDDLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sql = DDL.read_text(encoding="utf-8")

    def test_expected_schemas(self):
        for schema in (
            "governance",
            "staging",
            "analytics",
        ):
            self.assertIn(
                f"CREATE SCHEMA IF NOT EXISTS {schema};",
                self.sql,
            )

    def test_expected_table_count(self):
        tables = re.findall(
            r"CREATE TABLE IF NOT EXISTS\s+"
            r"([a-z_]+\.[a-z_]+)",
            self.sql,
            flags=re.IGNORECASE,
        )

        self.assertEqual(len(tables), 16)
        self.assertEqual(len(set(tables)), 16)

    def test_required_tables(self):
        required = {
            "governance.pipeline_run",
            "governance.data_quality_result",
            "governance.source_exception",
            "governance.reconciliation_result",
            "staging.patient",
            "staging.coverage",
            "staging.eob_claim",
            "staging.eob_item",
            "staging.eob_diagnosis",
            "staging.eob_procedure",
            "staging.eob_care_team",
            "staging.eob_supporting_info",
            "staging.eob_adjudication",
            "staging.eob_total",
            "staging.eob_item_adjudication",
            "staging.eob_item_detail",
        }

        for table in required:
            self.assertIn(
                f"CREATE TABLE IF NOT EXISTS {table}",
                self.sql,
            )

    def test_financial_values_are_numeric(self):
        self.assertRegex(
            self.sql,
            r"\bamount\s+NUMERIC\b",
        )

        self.assertNotRegex(
            self.sql,
            r"\bamount\s+(FLOAT|REAL|DOUBLE)",
        )

    def test_jsonb_lineage_is_preserved(self):
        self.assertIn(
            "source_fragment_json JSONB NOT NULL",
            self.sql,
        )

        self.assertIn(
            "raw_record_hash CHAR(64) NOT NULL",
            self.sql,
        )

    def test_parent_foreign_keys_exist(self):
        self.assertIn(
            "REFERENCES staging.eob_claim (pipeline_run_id, eob_id)",
            self.sql,
        )

        self.assertRegex(
            self.sql,
            r"REFERENCES\s+staging\.eob_item\s*\(\s*"
            r"pipeline_run_id,\s*eob_id,\s*item_sequence\s*\)",
        )

    def test_pipeline_lineage_fk_exists(self):
        self.assertIn(
            "REFERENCES governance.pipeline_run (pipeline_run_id)",
            self.sql,
        )

    def test_analytics_schema_has_no_tables_yet(self):
        self.assertNotIn(
            "CREATE TABLE IF NOT EXISTS analytics.",
            self.sql,
        )

    def test_non_destructive_ddl(self):
        upper = self.sql.upper()

        self.assertNotIn("DROP TABLE", upper)
        self.assertNotIn("TRUNCATE ", upper)
        self.assertNotIn("DELETE FROM", upper)


if __name__ == "__main__":
    unittest.main()
