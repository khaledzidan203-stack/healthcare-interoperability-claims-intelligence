from __future__ import annotations

from pathlib import Path
from tempfile import (
    TemporaryDirectory,
)

import json
import sys
import unittest


sys.path.insert(
    0,
    str(
        Path(__file__)
        .resolve()
        .parents[1]
        / "src"
    ),
)


from healthcare_claims.config import (
    ConfigError,
    Settings,
    load_settings,
)
from healthcare_claims.fhir import (
    FHIRIngestionError,
    parse_bundle_page,
    summarize_pages,
    validate_next_url,
)
from healthcare_claims.oauth import (
    TokenSet,
)
from healthcare_claims.storage import (
    persist_run,
)


def bundle_bytes(
    ids,
    *,
    total=2,
    next_url=None,
):

    links = [
        {
            "relation":
                "self",

            "url":
                "https://sandbox."
                "bluebutton.cms.gov/"
                "v3/fhir/"
                "ExplanationOfBenefit/"
                "?_count=2",
        }
    ]

    if next_url:

        links.append(
            {
                "relation":
                    "next",

                "url":
                    next_url,
            }
        )

    obj = {
        "resourceType":
            "Bundle",

        "type":
            "searchset",

        "total":
            total,

        "link":
            links,

        "entry": [
            {
                "resource": {
                    "resourceType":
                        "ExplanationOfBenefit",

                    "id":
                        value,
                }
            }
            for value in ids
        ],
    }

    return (
        json.dumps(obj)
        .encode("utf-8")
    )


class IngestionCoreTests(
    unittest.TestCase
):

    def test_settings_repr_does_not_leak_secret(
        self,
    ):

        settings = Settings(
            client_id="client",
            client_secret=
                "test-client-secret",
            redirect_uri=
                "http://localhost:"
                "8080/callback",
            api_version="v3",
            base_url=
                "https://sandbox."
                "bluebutton.cms.gov",
        )

        self.assertNotIn(
            "super-secret",
            repr(settings),
        )

    def test_load_settings_rejects_nonlocal_redirect(
        self,
    ):

        with TemporaryDirectory() as tmp:

            root = Path(tmp)

            (
                root / ".env"
            ).write_text(
                "CMS_BLUEBUTTON_CLIENT_ID=x\n"
                "CMS_BLUEBUTTON_CLIENT_SECRET=y\n"
                "CMS_BLUEBUTTON_REDIRECT_URI="
                "https://example.com/callback\n"
                "CMS_BLUEBUTTON_API_VERSION=v3\n"
                "CMS_BLUEBUTTON_SANDBOX_BASE_URL="
                "https://sandbox.bluebutton.cms.gov\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                ConfigError
            ):

                load_settings(
                    root
                )

    def test_live_source_exception_pattern_is_warning_not_failure(
        self,
    ):

        p1 = parse_bundle_page(
            bundle_bytes(
                ["A", "B"],
                total=2,
                next_url=
                    "https://sandbox."
                    "bluebutton.cms.gov/"
                    "v3/fhir/"
                    "ExplanationOfBenefit/"
                    "?page=2",
            ),
            "ExplanationOfBenefit",
            1,
        )

        p2 = parse_bundle_page(
            bundle_bytes(
                ["C", "D"],
                total=2,
                next_url=
                    "https://sandbox."
                    "bluebutton.cms.gov/"
                    "v3/fhir/"
                    "ExplanationOfBenefit/"
                    "?page=3",
            ),
            "ExplanationOfBenefit",
            2,
        )

        p3 = parse_bundle_page(
            bundle_bytes(
                ["E", "F"],
                total=2,
            ),
            "ExplanationOfBenefit",
            3,
        )

        result = summarize_pages(
            "ExplanationOfBenefit",
            [p1, p2, p3],
        )

        self.assertEqual(
            result
            .unique_resource_count,
            6,
        )

        self.assertEqual(
            result
            .duplicate_resource_count,
            0,
        )

        self.assertEqual(
            result
            .bundle_total_values,
            (2, 2, 2),
        )

        self.assertTrue(
            any(
                "Bundle.total"
                in warning
                for warning
                in result.warnings
            )
        )

    def test_duplicate_across_pages_is_failure(
        self,
    ):

        p1 = parse_bundle_page(
            bundle_bytes(
                ["A", "B"]
            ),
            "ExplanationOfBenefit",
            1,
        )

        p2 = parse_bundle_page(
            bundle_bytes(
                ["B", "C"]
            ),
            "ExplanationOfBenefit",
            2,
        )

        with self.assertRaises(
            FHIRIngestionError
        ):

            summarize_pages(
                "ExplanationOfBenefit",
                [p1, p2],
            )

    def test_off_domain_pagination_is_rejected(
        self,
    ):

        settings = Settings(
            client_id="client",
            client_secret="test-client-secret",
            redirect_uri=
                "http://localhost:"
                "8080/callback",
            api_version="v3",
            base_url=
                "https://sandbox."
                "bluebutton.cms.gov",
        )

        with self.assertRaises(
            FHIRIngestionError
        ):

            validate_next_url(
                settings,
                "https://evil.example/"
                "v3/fhir/"
                "ExplanationOfBenefit/"
                "?page=2",
            )

    def test_persist_run_does_not_persist_tokens(
        self,
    ):

        with TemporaryDirectory() as tmp:

            base = Path(tmp)

            root = (
                base
                / "HealthcareInteroperabilityClaims"
            )

            root.mkdir()

            (
                base / "output"
            ).mkdir()

            settings = Settings(
                client_id="client",
                client_secret="test-client-secret",
                redirect_uri=
                    "http://localhost:"
                    "8080/callback",
                api_version="v3",
                base_url=
                    "https://sandbox."
                    "bluebutton.cms.gov",
            )

            token = TokenSet(
                access_token=
                    "access-secret",
                refresh_token=
                    "refresh-secret",
                scope=
                    "patient/Patient.rs "
                    "patient/Coverage.rs "
                    "patient/"
                    "ExplanationOfBenefit.rs",
                expires_in=3600,
                patient=
                    "synthetic-patient",
            )

            page = parse_bundle_page(
                json.dumps(
                    {
                        "resourceType":
                            "Bundle",

                        "type":
                            "searchset",

                        "total":
                            1,

                        "entry": [
                            {
                                "resource": {
                                    "resourceType":
                                        "Patient",

                                    "id":
                                        "P1",
                                }
                            }
                        ],
                    }
                ).encode("utf-8"),
                "Patient",
                1,
            )

            result = summarize_pages(
                "Patient",
                [page],
            )

            final_dir = persist_run(
                root,
                settings,
                token,
                [result],
                user_label=
                    "BBUserTEST",
                page_size=
                    50,
            )

            manifest_text = (
                final_dir
                / "run_manifest.json"
            ).read_text(
                encoding="utf-8"
            )

            self.assertNotIn(
                "access-secret",
                manifest_text,
            )

            self.assertNotIn(
                "refresh-secret",
                manifest_text,
            )

            self.assertIn(
                '"token_values_persisted": false',
                manifest_text,
            )

            leftovers = list(
                (
                    base / "output"
                ).glob(
                    ".hc_ingest_*"
                )
            )

            self.assertEqual(
                leftovers,
                [],
            )


if __name__ == "__main__":
    unittest.main()
