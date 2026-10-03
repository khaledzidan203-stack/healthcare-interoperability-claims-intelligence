from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import (
    load_settings,
)
from .fhir import (
    FetchResult,
    fetch_resource,
)
from .oauth import (
    authorize_interactively,
)
from .storage import (
    persist_run,
)


SCOPES = [
    "patient/Patient.rs",
    "patient/Coverage.rs",
    "patient/"
    "ExplanationOfBenefit.rs",
]


RESOURCE_TYPES = [
    "Patient",
    "Coverage",
    "ExplanationOfBenefit",
]


@dataclass(frozen=True)
class IngestionSummary:

    raw_run_directory: Path

    results: tuple[
        FetchResult,
        ...,
    ]

    token_expires_in: (
        int | None
    )


def run_ingestion(
    project_root: Path,
    *,
    user_label: str,
    page_size: int = 50,
) -> IngestionSummary:

    settings = load_settings(
        project_root
    )

    token = (
        authorize_interactively(
            settings,
            SCOPES,
        )
    )

    results = []

    for resource_type in (
        RESOURCE_TYPES
    ):

        results.append(
            fetch_resource(
                settings,
                token,
                resource_type,
                page_size=
                    page_size,
            )
        )

    raw_dir = persist_run(
        project_root,
        settings,
        token,
        results,
        user_label=
            user_label,
        page_size=
            page_size,
    )

    return IngestionSummary(
        raw_run_directory=
            raw_dir,

        results=
            tuple(results),

        token_expires_in=
            token.expires_in,
    )
