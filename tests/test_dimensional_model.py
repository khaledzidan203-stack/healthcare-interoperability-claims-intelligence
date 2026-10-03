import unittest

from healthcare_claims.dimensional_model import (
    BRIDGES,
    BUS_MATRIX,
    DIMENSIONS,
    FACTS,
    MODEL_POLICIES,
    MODEL_TYPE,
    RELATIONSHIPS,
)


class DimensionalModelTests(unittest.TestCase):

    def test_model_is_constellation(self):

        self.assertEqual(
            MODEL_TYPE,
            "GOVERNED_DIMENSIONAL_CONSTELLATION",
        )

    def test_entity_counts(self):

        self.assertEqual(len(FACTS), 10)
        self.assertEqual(len(DIMENSIONS), 13)
        self.assertEqual(len(BRIDGES), 1)

    def test_entity_names_are_unique(self):

        entities = (
            list(FACTS)
            + list(DIMENSIONS)
            + list(BRIDGES)
        )

        names = [
            row["entity_name"]
            for row in entities
        ]

        ids = [
            row["entity_id"]
            for row in entities
        ]

        self.assertEqual(
            len(names),
            len(set(names)),
        )

        self.assertEqual(
            len(ids),
            len(set(ids)),
        )

    def test_no_fact_to_fact_relationships(self):

        facts = {
            row["entity_name"]
            for row in FACTS
        }

        for relationship in RELATIONSHIPS:

            self.assertFalse(
                relationship["from_entity"] in facts
                and relationship["to_entity"] in facts
            )

    def test_every_fact_has_pipeline_and_patient_dimensions(self):

        for fact in FACTS:

            name = fact["entity_name"]

            targets = {
                relationship["from_entity"]
                for relationship in RELATIONSHIPS
                if relationship["to_entity"] == name
            }

            self.assertIn(
                "DimPipelineRun",
                targets,
            )

            self.assertIn(
                "DimPatient",
                targets,
            )

    def test_financial_facts_use_conformed_financial_dimensions(self):

        for fact in (
            "FactClaimTotal",
            "FactClaimAdjudication",
            "FactItemAdjudication",
        ):

            dimensions = {
                r["from_entity"]
                for r in RELATIONSHIPS
                if r["to_entity"] == fact
            }

            self.assertIn(
                "DimFinancialConcept",
                dimensions,
            )

            self.assertIn(
                "DimCurrency",
                dimensions,
            )

    def test_coverage_is_bridge_gated(self):

        self.assertEqual(
            BRIDGES[0]["entity_name"],
            "BridgeClaimCoverage",
        )

        self.assertIn(
            "LOAD_GATED",
            BRIDGES[0]["model_status"],
        )

        self.assertEqual(
            MODEL_POLICIES[
                "coverage_filtering"
            ],
            "BRIDGE_REQUIRED_AND_LOAD_GATED",
        )

    def test_financial_safety_policies(self):

        self.assertEqual(
            MODEL_POLICIES[
                "direct_fact_to_fact_relationships"
            ],
            "FORBIDDEN",
        )

        self.assertEqual(
            MODEL_POLICIES[
                "cross_grain_financial_summation"
            ],
            "FORBIDDEN",
        )

        self.assertEqual(
            MODEL_POLICIES[
                "cross_currency_summation"
            ],
            "FORBIDDEN",
        )

        self.assertEqual(
            MODEL_POLICIES[
                "financial_alias_equivalence"
            ],
            "NOT_ASSUMED",
        )

        self.assertEqual(
            MODEL_POLICIES[
                "consolidated_financial_kpis"
            ],
            "NOT_APPROVED",
        )

    def test_bridge_has_pipeline_run_dimension(self):

        bridge_dimensions = {
            relationship["from_entity"]
            for relationship in RELATIONSHIPS
            if relationship["to_entity"]
            == "BridgeClaimCoverage"
        }

        self.assertIn(
            "DimPipelineRun",
            bridge_dimensions,
        )

        self.assertIn(
            "DimCoverage",
            bridge_dimensions,
        )

    def test_bus_matrix_has_all_facts(self):

        self.assertEqual(
            {
                row["fact"]
                for row in BUS_MATRIX
            },
            {
                row["entity_name"]
                for row in FACTS
            },
        )


if __name__ == "__main__":
    unittest.main()
