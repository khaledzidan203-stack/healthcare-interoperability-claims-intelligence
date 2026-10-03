from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys

from .config import (
    ConfigError,
    load_settings,
)
from .fhir import (
    FHIRIngestionError,
)
from .ingest import (
    run_ingestion,
)
from .oauth import (
    OAuthError,
)
from .storage import (
    StorageError,
)


def _parser(
) -> ArgumentParser:

    parser = ArgumentParser(
        prog="healthcare_claims",

        description=(
            "CMS Blue Button v3 "
            "synthetic FHIR ingestion "
            "for the Healthcare "
            "Interoperability & Claims "
            "Intelligence Platform."
        ),
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    validate = sub.add_parser(
        "validate-config",

        help=(
            "Validate local .env "
            "configuration without "
            "printing secrets."
        ),
    )

    validate.add_argument(
        "--project-root",
        default=".",
    )

    ingest = sub.add_parser(
        "ingest",

        help=(
            "Run interactive OAuth "
            "and ingest Patient, "
            "Coverage and "
            "ExplanationOfBenefit."
        ),
    )

    ingest.add_argument(
        "--project-root",
        default=".",
    )

    ingest.add_argument(
        "--user-label",
        required=True,

        help=(
            "Synthetic CMS frontend "
            "user label for run "
            "metadata only. "
            "Never pass a password."
        ),
    )

    ingest.add_argument(
        "--page-size",
        type=int,
        default=50,
        choices=range(
            1,
            51,
        ),
        metavar="1..50",
    )

    return parser


def main(
) -> int:

    args = (
        _parser()
        .parse_args()
    )

    root = Path(
        args.project_root
    ).resolve()

    try:

        if (
            args.command
            == "validate-config"
        ):

            settings = (
                load_settings(
                    root
                )
            )

            print(
                "CONFIG_VALIDATION: PASS"
            )

            print(
                "API_VERSION: "
                f"{settings.api_version}"
            )

            print(
                "CLIENT_ID_PRESENT: YES"
            )

            print(
                "CLIENT_SECRET_PRESENT: YES"
            )

            print(
                "REDIRECT_URI: "
                f"{settings.redirect_uri}"
            )

            print(
                "SANDBOX_BASE_URL: "
                f"{settings.base_url}"
            )

            print(
                "SECRET_VALUES_PRINTED: NO"
            )

            return 0

        print(
            "INGESTION_START"
        )

        print(
            "OAuth browser "
            "authorization will open."
        )

        print(
            "Credentials and tokens "
            "are not printed or "
            "persisted."
        )

        summary = run_ingestion(
            root,
            user_label=
                args.user_label,
            page_size=
                args.page_size,
        )

        for result in (
            summary.results
        ):

            print(
                "RESOURCE | "
                f"{result.resource_type}"
                " | "
                f"pages="
                f"{len(result.pages)}"
                " | "
                f"raw="
                f"{result.raw_resource_count}"
                " | "
                f"unique="
                f"{result.unique_resource_count}"
                " | "
                f"duplicates="
                f"{result.duplicate_resource_count}"
                " | "
                f"missing_ids="
                f"{result.missing_resource_id_count}"
            )

            for warning in (
                result.warnings
            ):

                print(
                    "SOURCE_WARNING | "
                    f"{result.resource_type}"
                    " | "
                    f"{warning}"
                )

        print(
            "TOKEN_EXPIRES_IN: "
            f"{summary.token_expires_in}"
        )

        print(
            "RAW_RUN_DIRECTORY: "
            + str(
                summary
                .raw_run_directory
                .relative_to(root)
            )
        )

        print(
            "TOKEN_VALUES_PERSISTED: NO"
        )

        print(
            "INGESTION_STATUS: PASS"
        )

        return 0

    except (
        ConfigError,
        OAuthError,
        FHIRIngestionError,
        StorageError,
        ValueError,
    ) as exc:

        print(
            "INGESTION_STATUS: "
            f"FAIL | {exc}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(
        main()
    )
