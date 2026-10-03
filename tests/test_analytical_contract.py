import unittest

from healthcare_claims.analytical_contract import (
    GRAIN_CONTRACTS,
    METRIC_CONTRACTS,
    MODEL_POLICIES,
    REQUIRED_METRIC_FIELDS,
)


class AnalyticalContractTests(unittest.TestCase):

    def test_grain_ids_are_unique(self):

        ids = [
            row["grain_id"]
            for row in GRAIN_CONTRACTS
        ]

        self.assertEqual(
            len(ids),
            len(set(ids)),
        )

    def test_metric_ids_are_unique(self):

        ids = [
            row["metric_id"]
            for row in METRIC_CONTRACTS
        ]

        self.assertEqual(
            len(ids),
            len(set(ids)),
        )

    def test_metric_contract_is_complete(self):

        required = set(
            REQUIRED_METRIC_FIELDS
        )

        for metric in METRIC_CONTRACTS:

            self.assertEqual(
                set(metric),
                required,
            )

    def test_claim_and_item_financial_grains_are_separate(self):

        facts = {
            row["proposed_entity"]
            for row in GRAIN_CONTRACTS
        }

        self.assertIn(
            "FactClaimTotal",
            facts,
        )

        self.assertIn(
            "FactClaimAdjudication",
            facts,
        )

        self.assertIn(
            "FactItemAdjudication",
            facts,
        )

    def test_cross_grain_financial_summation_is_forbidden(self):

        self.assertEqual(
            MODEL_POLICIES[
                "cross_grain_financial_summation"
            ],
            "FORBIDDEN",
        )

    def test_fact_to_fact_relationships_are_forbidden(self):

        self.assertEqual(
            MODEL_POLICIES[
                "direct_fact_to_fact_relationships"
            ],
            "FORBIDDEN",
        )

    def test_financial_metrics_are_exact_concept_only(self):

        financial = [
            metric
            for metric in METRIC_CONTRACTS
            if metric["metric_id"]
            in ("M007", "M008", "M009")
        ]

        self.assertEqual(
            len(financial),
            3,
        )

        for metric in financial:

            text = (
                metric["business_definition"]
                + " "
                + metric["inclusions_exclusions"]
                + " "
                + metric["total_behavior"]
            ).lower()

            self.assertIn(
                "exact",
                text,
            )

            self.assertIn(
                "currency",
                text,
            )

    def test_no_user_facing_financial_kpi_is_approved(self):

        self.assertEqual(
            MODEL_POLICIES[
                "user_facing_financial_kpis"
            ],
            "NOT_YET_APPROVED",
        )


if __name__ == "__main__":
    unittest.main()
