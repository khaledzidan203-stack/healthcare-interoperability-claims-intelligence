import unittest

from healthcare_claims.analytics_load import (
    FACT_SOURCE_MAP,
    TARGET_ENTITIES,
    build_date_rows,
    build_identity_dimension,
    date_key,
    reference_target_id,
)


class AnalyticsLoadTests(unittest.TestCase):

    def test_target_inventory_contains_24_entities(self):

        self.assertEqual(
            len(TARGET_ENTITIES),
            24,
        )

        self.assertEqual(
            len(set(TARGET_ENTITIES)),
            24,
        )

    def test_fact_inventory_contains_10_facts(self):

        self.assertEqual(
            len(FACT_SOURCE_MAP),
            10,
        )

    def test_date_key_is_deterministic(self):

        self.assertEqual(
            date_key(
                "2026-09-30"
            ),
            20260930,
        )

        self.assertEqual(
            date_key(
                "2026-09-30T12:00:00Z"
            ),
            20260930,
        )

    def test_date_dimension_is_continuous(self):

        rows = build_date_rows([
            "2026-01-01",
            "2026-01-03",
        ])

        self.assertEqual(
            len(rows),
            3,
        )

        self.assertEqual(
            rows[1]["date_key"],
            20260102,
        )

    def test_relative_reference_target_id(self):

        self.assertEqual(
            reference_target_id(
                "Patient/123"
            ),
            "123",
        )

    def test_provider_unknown_member_is_explicit(self):

        rows = build_identity_dimension(
            [],
            unknown_required=True,
        )

        self.assertEqual(
            len(rows),
            1,
        )

        self.assertTrue(
            rows[0]["is_unknown"]
        )

        self.assertIsNone(
            rows[0][
                "identity_key_sha256"
            ]
        )

    def test_display_text_does_not_create_identity(self):

        rows = build_identity_dimension(
            [
                {
                    "identity_key_sha256":
                        None,

                    "display":
                        "Example Provider",
                }
            ],
            unknown_required=False,
        )

        self.assertEqual(
            rows,
            [],
        )


if __name__ == "__main__":
    unittest.main()
