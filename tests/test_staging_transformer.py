from __future__ import annotations

from copy import deepcopy
import unittest

from healthcare_claims.staging import (
    TransformError,
    transform_resource,
)


def coded(system, code):

    return {
        "coding": [{
            "system": system,
            "code": code,
        }]
    }


class StagingTransformerTests(unittest.TestCase):

    def test_eob_splits_into_expected_grains(self):

        source = {
            "resourceType": "ExplanationOfBenefit",
            "id": "e1",
            "status": "active",
            "use": "claim",
            "outcome": "complete",
            "patient": {
                "reference": "Patient/p1"
            },
            "type": coded(
                "sys:type",
                "pharmacy",
            ),
            "item": [{
                "sequence": 1,
                "productOrService": coded(
                    "sys:drug",
                    "D1",
                ),
                "adjudication": [{
                    "category": coded(
                        "sys:adj",
                        "allowed",
                    ),
                    "amount": {
                        "value": 10.0,
                        "currency": "USD",
                    },
                }],
                "detail": [{
                    "sequence": 1,
                    "productOrService": coded(
                        "sys:detail",
                        "X1",
                    ),
                }],
            }],
            "diagnosis": [{
                "sequence": 1,
                "diagnosisCodeableConcept": coded(
                    "sys:icd",
                    "A01",
                ),
            }],
            "procedure": [{
                "sequence": 1,
                "procedureCodeableConcept": coded(
                    "sys:cpt",
                    "99213",
                ),
            }],
            "careTeam": [{
                "sequence": 1,
                "provider": {
                    "identifier": {
                        "system": "sys:npi",
                        "value": "999",
                    }
                },
            }],
            "supportingInfo": [{
                "sequence": 1,
                "category": coded(
                    "sys:info",
                    "x",
                ),
            }],
            "adjudication": [{
                "category": coded(
                    "sys:adj",
                    "paid",
                ),
                "amount": {
                    "value": 5.0,
                    "currency": "USD",
                },
            }],
            "total": [{
                "category": coded(
                    "sys:total",
                    "submitted",
                ),
                "amount": {
                    "value": 20.0,
                    "currency": "USD",
                },
            }],
        }

        original = deepcopy(source)

        rows = transform_resource(
            source,
            run_id="run_test",
            source_file="eob_bundle_page_001.json",
        )

        self.assertEqual(
            source,
            original,
        )

        expected = {
            "stg_eob_claim": 1,
            "stg_eob_item": 1,
            "stg_eob_diagnosis": 1,
            "stg_eob_procedure": 1,
            "stg_eob_care_team": 1,
            "stg_eob_supporting_info": 1,
            "stg_eob_adjudication": 1,
            "stg_eob_total": 1,
            "stg_eob_item_adjudication": 1,
            "stg_eob_item_detail": 1,
        }

        for entity, count in expected.items():

            self.assertEqual(
                len(rows[entity]),
                count,
            )

        item = rows["stg_eob_item"][0]

        self.assertEqual(
            item["eob_id"],
            "e1",
        )

        self.assertEqual(
            item["item_sequence"],
            1,
        )

        self.assertEqual(
            item["source_page_number"],
            1,
        )

        self.assertEqual(
            item["product_service_code"],
            "D1",
        )

        self.assertTrue(
            item["raw_record_hash"]
        )

        self.assertTrue(
            item["source_fragment_json"]
        )

    def test_optional_children_can_be_absent(self):

        rows = transform_resource(
            {
                "resourceType":
                    "ExplanationOfBenefit",
                "id": "e2",
            },
            run_id="run_test",
            source_file="eob_bundle_page_001.json",
        )

        self.assertEqual(
            len(rows["stg_eob_claim"]),
            1,
        )

        self.assertEqual(
            len(rows["stg_eob_item"]),
            0,
        )

    def test_duplicate_sequence_fails(self):

        source = {
            "resourceType": "ExplanationOfBenefit",
            "id": "e3",
            "item": [
                {"sequence": 1},
                {"sequence": 1},
            ],
        }

        with self.assertRaises(
            TransformError
        ):

            transform_resource(
                source,
                run_id="run_test",
                source_file="eob_bundle_page_001.json",
            )

    def test_missing_sequence_fails(self):

        source = {
            "resourceType": "ExplanationOfBenefit",
            "id": "e4",
            "diagnosis": [{
                "diagnosisCodeableConcept":
                    coded("sys", "A")
            }],
        }

        with self.assertRaises(
            TransformError
        ):

            transform_resource(
                source,
                run_id="run_test",
                source_file="eob_bundle_page_001.json",
            )


if __name__ == "__main__":
    unittest.main()
