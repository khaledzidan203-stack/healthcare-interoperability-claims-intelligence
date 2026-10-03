import copy
import unittest

from healthcare_claims.reference_normalization import (
    normalize_reference,
    normalize_resources,
)


class ReferenceNormalizationTests(unittest.TestCase):

    def test_display_only_coverage_is_preserved_but_not_inferred(self):

        resource = {
            "resourceType":
                "ExplanationOfBenefit",

            "id":
                "e1",

            "insurance": [
                {
                    "focal": True,
                    "coverage": {
                        "display":
                            "Source Coverage Display"
                    },
                }
            ],
        }

        result = normalize_resources(
            [resource],
            "run1",
        )

        row = result[
            "bridge_claim_coverage"
        ][0]

        self.assertEqual(
            row[
                "coverage_resolution_status"
            ],
            "DISPLAY_ONLY_NON_IDENTITY",
        )

        self.assertIsNone(
            row[
                "coverage_identity_key_sha256"
            ]
        )

        self.assertIsNotNone(
            row[
                "association_key_sha256"
            ]
        )

    def test_empty_provider_does_not_fabricate_identity(self):

        resource = {
            "resourceType":
                "ExplanationOfBenefit",

            "id":
                "e1",

            "provider": {},
        }

        result = normalize_resources(
            [resource],
            "run1",
        )

        row = result[
            "provider_reference"
        ][0]

        self.assertEqual(
            row[
                "resolution_status"
            ],
            "SOURCE_IDENTITY_NOT_EXPLICIT",
        )

        self.assertIsNone(
            row[
                "identity_key_sha256"
            ]
        )

    def test_identifier_only_reference_is_key_ready(self):

        result = normalize_reference(
            {
                "identifier": {
                    "system":
                        "http://example.org/id",

                    "value":
                        "123",
                }
            },
            "Coverage",
            "c1",
            {},
        )

        self.assertEqual(
            result[
                "resolution_status"
            ],
            "IDENTIFIER_KEY_READY",
        )

        self.assertIsNotNone(
            result[
                "identity_key_sha256"
            ]
        )

    def test_contained_reference_resolves(self):

        resource = {
            "resourceType":
                "ExplanationOfBenefit",

            "id":
                "e1",

            "contained": [
                {
                    "resourceType":
                        "Practitioner",

                    "id":
                        "p1",
                }
            ],

            "provider": {
                "reference":
                    "#p1"
            },
        }

        result = normalize_resources(
            [resource],
            "run1",
        )

        row = result[
            "provider_reference"
        ][0]

        self.assertEqual(
            row[
                "resolution_status"
            ],
            "CONTAINED_RESOLVED",
        )

        self.assertEqual(
            row[
                "target_resource_type"
            ],
            "Practitioner",
        )

    def test_reference_value_becomes_deterministic_identity(self):

        result = normalize_reference(
            {
                "reference":
                    "Organization/o1"
            },
            "ExplanationOfBenefit",
            "e1",
            {},
        )

        self.assertEqual(
            result[
                "resolution_status"
            ],
            "REFERENCE_KEY_READY",
        )

        self.assertIsNotNone(
            result[
                "identity_key_sha256"
            ]
        )

    def test_source_is_not_mutated(self):

        resource = {
            "resourceType":
                "Coverage",

            "id":
                "c1",

            "payor": [
                {
                    "reference":
                        "Organization/o1"
                }
            ],
        }

        original = copy.deepcopy(
            resource
        )

        normalize_resources(
            [resource],
            "run1",
        )

        self.assertEqual(
            resource,
            original,
        )


if __name__ == "__main__":
    unittest.main()
