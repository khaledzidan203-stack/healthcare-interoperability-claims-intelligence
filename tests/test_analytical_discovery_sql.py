from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / "sql" / "03_analytical_model_discovery.sql"


class AnalyticalDiscoverySQLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = SQL.read_text(
            encoding="utf-8"
        )
        cls.upper = cls.text.upper()

    def test_discovery_sql_is_read_only(self):
        for token in (
            "CREATE TABLE",
            "ALTER TABLE",
            "DROP TABLE",
            "TRUNCATE ",
            "INSERT INTO",
            "UPDATE ",
            "DELETE FROM",
        ):
            self.assertNotIn(
                token,
                self.upper,
            )

    def test_core_staging_domains_are_referenced(self):
        for table in (
            "staging.eob_claim",
            "staging.eob_item",
            "staging.eob_diagnosis",
            "staging.eob_procedure",
            "staging.eob_supporting_info",
            "staging.eob_adjudication",
            "staging.eob_total",
            "staging.eob_item_adjudication",
            "staging.eob_item_detail",
        ):
            self.assertIn(
                table,
                self.text,
            )

    def test_no_analytics_tables_are_created(self):
        self.assertNotIn(
            "CREATE TABLE analytics.",
            self.upper,
        )


if __name__ == "__main__":
    unittest.main()
