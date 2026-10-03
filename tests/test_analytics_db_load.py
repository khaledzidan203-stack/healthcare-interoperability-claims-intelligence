
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from healthcare_claims.analytics_db_load import (
    ENTITY_ORDER,
    render_transaction,
)


class AnalyticsDBLoadTests(unittest.TestCase):

    def _render(self):

        with TemporaryDirectory() as temp:

            root = Path(temp)

            paths = {}
            counts = {}

            for entity in ENTITY_ORDER:

                path = (
                    root
                    / f"{entity}.csv"
                )

                path.write_text(
                    "",
                    encoding="utf-8",
                )

                paths[entity] = path
                counts[entity] = 0

            return render_transaction(
                paths,
                "A" * 64,
                counts,
            )

    def test_loader_covers_all_24_entities(self):

        sql = self._render()

        self.assertEqual(
            sql.count(
                "CREATE TEMP TABLE load_"
            ),
            24,
        )

        self.assertEqual(
            sql.count(
                r"\copy load_"
            ),
            24,
        )

    def test_loader_is_atomic(self):

        sql = self._render()

        self.assertIn(
            "BEGIN;",
            sql,
        )

        self.assertIn(
            "COMMIT;",
            sql,
        )

        self.assertIn(
            "DO $analytics_reconcile$",
            sql,
        )

    def test_loader_is_non_destructive(self):

        sql = self._render().upper()

        for token in (
            "DELETE FROM",
            "TRUNCATE ",
            "DROP TABLE",
            "DROP SCHEMA",
            "UPDATE ANALYTICS.",
        ):

            self.assertNotIn(
                token,
                sql,
            )

    def test_coverage_identity_is_not_inferred(self):

        sql = self._render()

        self.assertIn(
            "coverage_key IS NOT NULL",
            sql,
        )

        self.assertIn(
            "DISPLAY_ONLY_NON_IDENTITY",
            sql,
        )

        self.assertIn(
            "coverage_id",
            sql,
        )

    def test_unknown_provider_is_explicit(self):

        sql = self._render()

        self.assertIn(
            "prov.is_unknown",
            sql,
        )

        self.assertIn(
            "Claims mapped to Unknown Provider",
            sql,
        )


if __name__ == "__main__":
    unittest.main()
