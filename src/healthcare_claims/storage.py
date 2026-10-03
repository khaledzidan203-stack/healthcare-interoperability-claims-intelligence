from __future__ import annotations

from datetime import (
    datetime,
    timezone,
)
from hashlib import sha256
from pathlib import Path

import json
import os
import secrets
import shutil
import tempfile

from .config import Settings
from .fhir import FetchResult
from .oauth import TokenSet


class StorageError(
    RuntimeError
):
    pass


def _sha256(
    data: bytes,
) -> str:

    return (
        sha256(data)
        .hexdigest()
        .upper()
    )


def persist_run(
    project_root: Path,
    settings: Settings,
    token: TokenSet,
    results: list[FetchResult],
    *,
    user_label: str,
    page_size: int,
) -> Path:

    stamp = (
        datetime.now(
            timezone.utc
        )
        .strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    run_id = (
        f"run_{stamp}_ingest_"
        f"{secrets.token_hex(4)}"
    )

    final_parent = (
        project_root
        / "data"
        / "raw"
        / "cms_bluebutton"
        / settings.api_version
    )

    final_parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_dir = (
        final_parent
        / run_id
    )

    if final_dir.exists():

        raise StorageError(
            "RAW run directory "
            "already exists: "
            f"{final_dir}"
        )

    # Staging is deliberately outside
    # the project root so temporary
    # execution artifacts never become
    # repository content.

    staging_base = (
        project_root.parent
        / "output"
    )

    staging_base.mkdir(
        parents=True,
        exist_ok=True,
    )

    staging_dir = Path(
        tempfile.mkdtemp(
            prefix=".hc_ingest_",
            dir=str(
                staging_base
            ),
        )
    )

    try:

        resource_manifest = {}

        all_warnings = []

        for result in results:

            prefix = (
                result.resource_type
                .lower()
            )

            page_records = []

            for page in (
                result.pages
            ):

                filename = (
                    f"{prefix}_bundle_"
                    f"page_"
                    f"{page.page_number:03d}"
                    ".json"
                )

                target = (
                    staging_dir
                    / filename
                )

                target.write_bytes(
                    page.raw
                )

                page_records.append(
                    {
                        "page":
                            page.page_number,

                        "filename":
                            filename,

                        "bundle_total":
                            page.bundle_total,

                        "entry_count":
                            page.entry_count,

                        "target_resource_count":
                            page
                            .target_resource_count,

                        "next_present":
                            bool(
                                page.next_url
                            ),

                        "self_present":
                            page.self_present,

                        "sha256":
                            page.sha256,

                        "bytes":
                            len(
                                page.raw
                            ),
                    }
                )

            resource_manifest[
                result.resource_type
            ] = {
                "page_count":
                    len(
                        result.pages
                    ),

                "raw_resource_count":
                    result
                    .raw_resource_count,

                "unique_resource_count":
                    result
                    .unique_resource_count,

                "duplicate_resource_count":
                    result
                    .duplicate_resource_count,

                "missing_resource_id_count":
                    result
                    .missing_resource_id_count,

                "bundle_total_values":
                    list(
                        result
                        .bundle_total_values
                    ),

                "warnings":
                    list(
                        result.warnings
                    ),

                "pages":
                    page_records,
            }

            for warning in (
                result.warnings
            ):

                all_warnings.append(
                    {
                        "resource_type":
                            result.resource_type,

                        "warning":
                            warning,
                    }
                )

        manifest = {
            "run_id":
                run_id,

            "extracted_at_utc":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "environment":
                "CMS Blue Button "
                "Sandbox",

            "api_version":
                settings.api_version,

            "authorization_flow":
                "OAuth 2.0 "
                "Authorization Code "
                "+ PKCE S256",

            "synthetic_test_user_label":
                user_label,

            "requested_page_size":
                page_size,

            "requested_scopes": [
                "patient/Patient.rs",
                "patient/Coverage.rs",
                "patient/"
                "ExplanationOfBenefit.rs",
            ],

            "granted_scopes":
                sorted(
                    token
                    .granted_scopes
                ),

            "patient_context_present":
                bool(
                    token.patient
                ),

            "token_values_persisted":
                False,

            "completeness_strategy":
                "follow_bundle_next_"
                "until_absent_and_"
                "reconcile_resource_keys",

            "source_warnings":
                all_warnings,

            "resources":
                resource_manifest,
        }

        manifest_bytes = (
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
            )
            .encode("utf-8")
        )

        (
            staging_dir
            / "run_manifest.json"
        ).write_bytes(
            manifest_bytes
        )

        # Move only after every page and
        # the manifest are complete.
        #
        # Temporary staging remains
        # outside the repository.

        os.replace(
            staging_dir,
            final_dir,
        )

        return final_dir

    except Exception:

        shutil.rmtree(
            staging_dir,
            ignore_errors=True,
        )

        raise
