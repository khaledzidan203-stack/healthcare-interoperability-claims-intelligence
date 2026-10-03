
import unittest

from healthcare_claims.semantic_contract import (
    GATES,
    MEASURES,
    RELATIONSHIPS,
    TABLES,
)


class SemanticContractTests(unittest.TestCase):

    def test_physical_source_inventory_is_24(self):

        self.assertEqual(
            len(TABLES),
            24,
        )

    def test_current_semantic_release_includes_22_tables(self):

        included = [
            row
            for row in TABLES
            if row["inclusion"] == "INCLUDED"
        ]

        excluded = [
            row
            for row in TABLES
            if row["inclusion"]
            == "EXCLUDED_CURRENT_RELEASE"
        ]

        self.assertEqual(
            len(included),
            22,
        )

        self.assertEqual(
            len(excluded),
            2,
        )

    def test_coverage_objects_are_load_gated(self):

        gated = {
            row["semantic_name"]
            for row in TABLES
            if row["business_status"]
            == "LOAD_GATED"
        }

        self.assertEqual(
            gated,
            {
                "DimCoverage",
                "BridgeClaimCoverage",
            },
        )

    def test_semantic_relationship_count(self):

        self.assertEqual(
            len(RELATIONSHIPS),
            50,
        )

    def test_role_playing_date_relationships_are_inactive(self):

        inactive = [
            row
            for row in RELATIONSHIPS
            if not row["active"]
        ]

        self.assertEqual(
            len(inactive),
            5,
        )

        self.assertTrue(
            all(
                row["from_table"] == "DimDate"
                for row in inactive
            )
        )

    def test_all_relationships_are_single_direction(self):

        self.assertTrue(
            all(
                row["filter_direction"]
                == "SINGLE_DIMENSION_TO_FACT"
                for row in RELATIONSHIPS
            )
        )

    def test_no_fact_to_fact_relationships(self):

        fact_names = {
            row["semantic_name"]
            for row in TABLES
            if row["entity_type"] == "FACT"
        }

        for row in RELATIONSHIPS:

            self.assertFalse(
                row["from_table"] in fact_names
                and row["to_table"] in fact_names
            )

    def test_coverage_not_in_semantic_relationships(self):

        relationship_tables = {
            row["from_table"]
            for row in RELATIONSHIPS
        } | {
            row["to_table"]
            for row in RELATIONSHIPS
        }

        self.assertNotIn(
            "DimCoverage",
            relationship_tables,
        )

        self.assertNotIn(
            "BridgeClaimCoverage",
            relationship_tables,
        )

    def test_measure_inventory(self):

        self.assertEqual(
            len(MEASURES),
            9,
        )

        base = [
            row
            for row in MEASURES
            if row["status"]
            == "APPROVED_BASE_MEASURE"
        ]

        restricted = [
            row
            for row in MEASURES
            if row["status"]
            == "RESTRICTED_FINANCIAL_PRIMITIVE"
        ]

        self.assertEqual(
            len(base),
            6,
        )

        self.assertEqual(
            len(restricted),
            3,
        )

    def test_financial_measures_are_not_user_facing_kpis(self):

        for row in MEASURES:

            if row["metric_id"] in {
                "M007",
                "M008",
                "M009",
            }:

                self.assertEqual(
                    row["status"],
                    "RESTRICTED_FINANCIAL_PRIMITIVE",
                )

    def test_four_governance_gates_exist(self):

        self.assertEqual(
            len(GATES),
            4,
        )


    def test_multirun_warehouse_requires_single_run_semantic_context(self):

        from healthcare_claims.semantic_contract import GATES

        gate = next(
            gate
            for gate in GATES
            if gate["gate_id"] == "SG-004"
        )

        self.assertEqual(
            gate["state"],
            "MULTI_RUN_WAREHOUSE_SINGLE_RUN_CONTEXT",
        )

        self.assertEqual(
            gate["rule"],
            "Multiple validated pipeline runs may coexist in the warehouse; each semantic analytical context must resolve to exactly one pipeline run, and cross-run aggregation remains forbidden.",
        )

        self.assertIn(
            "exactly one pipeline run",
            gate["rule"],
        )

        self.assertIn(
            "cross-run aggregation remains forbidden",
            gate["rule"],
        )


if __name__ == "__main__":
    unittest.main()
