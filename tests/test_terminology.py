from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from healthcare_claims.terminology import (
    TerminologyError,
    inventory_run,
    reference_form,
    reference_target_type,
    source_family,
)


class TerminologyTests(unittest.TestCase):

    def test_source_family_classification(self):

        self.assertEqual(
            source_family(
                "https://bluebutton.cms.gov/resources/codesystem/test"
            ),
            "CMS_BLUE_BUTTON",
        )

        self.assertEqual(
            source_family(
                "http://hl7.org/fhir/test"
            ),
            "HL7_FHIR",
        )

    def test_reference_classification(self):

        self.assertEqual(
            reference_form(
                "Patient/123"
            ),
            "RELATIVE",
        )

        self.assertEqual(
            reference_target_type(
                "Patient/123"
            ),
            "Patient",
        )

        self.assertEqual(
            reference_target_type(
                "#provider1",
                {
                    "provider1":
                        "Practitioner"
                },
            ),
            "Practitioner",
        )

    def test_inventory_reads_coding_and_reference(self):

        with TemporaryDirectory() as temp:

            root = Path(temp)

            bundle = {
                "resourceType": "Bundle",
                "entry": [
                    {
                        "resource": {
                            "resourceType":
                                "Patient",
                            "id": "p1",
                            "meta": {
                                "profile": [
                                    "http://example/profile"
                                ]
                            },
                            "gender": "male",
                            "extension": [
                                {
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "system":
                                                    "http://example/system",
                                                "code":
                                                    "ABC",
                                                "display":
                                                    "Example",
                                            }
                                        ]
                                    }
                                }
                            ],
                            "managingOrganization": {
                                "reference":
                                    "Organization/o1"
                            },
                        }
                    }
                ],
            }

            (
                root
                / "patient_bundle_page_001.json"
            ).write_text(
                json.dumps(bundle),
                encoding="utf-8",
            )

            result = inventory_run(root)

            self.assertEqual(
                result["resource_count"],
                1,
            )

            self.assertEqual(
                sum(
                    result[
                        "coding_counter"
                    ].values()
                ),
                1,
            )

            self.assertEqual(
                sum(
                    result[
                        "reference_counter"
                    ].values()
                ),
                1,
            )

    def test_duplicate_resource_is_rejected(self):

        with TemporaryDirectory() as temp:

            root = Path(temp)

            bundle = {
                "resourceType": "Bundle",
                "entry": [
                    {
                        "resource": {
                            "resourceType":
                                "Patient",
                            "id": "p1",
                        }
                    }
                ],
            }

            for number in (1, 2):

                (
                    root
                    / (
                        "patient_bundle_page_"
                        f"{number:03d}.json"
                    )
                ).write_text(
                    json.dumps(bundle),
                    encoding="utf-8",
                )

            with self.assertRaises(
                TerminologyError
            ):

                inventory_run(root)


if __name__ == "__main__":
    unittest.main()
