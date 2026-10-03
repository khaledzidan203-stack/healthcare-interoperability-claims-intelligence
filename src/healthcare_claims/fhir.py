from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from urllib.error import (
    HTTPError,
    URLError,
)
from urllib.parse import urlparse
from urllib.request import (
    Request,
    urlopen,
)

import json
import time

from .config import Settings
from .oauth import TokenSet


class FHIRIngestionError(
    RuntimeError
):
    pass


@dataclass(frozen=True)
class PageData:

    page_number: int
    raw: bytes
    bundle_total: int | None
    entry_count: int
    target_resource_count: int
    resource_keys: tuple[str, ...]
    missing_resource_id_count: int
    next_url: str | None
    self_present: bool

    @property
    def sha256(self) -> str:

        return (
            sha256(self.raw)
            .hexdigest()
            .upper()
        )


@dataclass(frozen=True)
class FetchResult:

    resource_type: str
    pages: tuple[
        PageData,
        ...,
    ]
    unique_resource_count: int
    duplicate_resource_count: int
    missing_resource_id_count: int
    bundle_total_values: tuple[
        int | None,
        ...,
    ]
    warnings: tuple[str, ...]

    @property
    def raw_resource_count(
        self,
    ) -> int:

        return sum(
            page.target_resource_count
            for page in self.pages
        )


def _find_link(
    bundle: dict,
    relation: str,
) -> str | None:

    for link in (
        bundle.get(
            "link",
            [],
        )
        or []
    ):

        if (
            isinstance(
                link,
                dict,
            )
            and
            link.get(
                "relation"
            )
            == relation
            and
            link.get(
                "url"
            )
        ):
            return str(
                link["url"]
            )

    return None


def validate_next_url(
    settings: Settings,
    url: str,
) -> None:

    base = urlparse(
        settings.base_url
    )

    candidate = urlparse(
        url
    )

    if (
        candidate.scheme
        != "https"
        or
        candidate.netloc
        != base.netloc
    ):
        raise FHIRIngestionError(
            "FHIR pagination link "
            "points outside the "
            "configured CMS host."
        )

    required_prefix = (
        f"/{settings.api_version}"
        "/fhir/"
    )

    if not candidate.path.startswith(
        required_prefix
    ):
        raise FHIRIngestionError(
            "FHIR pagination link "
            "points outside the "
            "configured FHIR path."
        )


def parse_bundle_page(
    raw: bytes,
    expected_resource_type: str,
    page_number: int,
) -> PageData:

    try:
        bundle = json.loads(
            raw.decode("utf-8")
        )

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:

        raise FHIRIngestionError(
            f"Page {page_number} "
            "returned invalid JSON."
        ) from exc

    if (
        bundle.get(
            "resourceType"
        )
        != "Bundle"
    ):
        raise FHIRIngestionError(
            f"Page {page_number} "
            "is not a FHIR Bundle."
        )

    entries = (
        bundle.get(
            "entry"
        )
        or []
    )

    keys: list[str] = []

    missing_ids = 0
    target_count = 0

    for entry in entries:

        resource = (
            entry.get(
                "resource"
            )
            if isinstance(
                entry,
                dict,
            )
            else None
        )

        if (
            not isinstance(
                resource,
                dict,
            )
            or
            resource.get(
                "resourceType"
            )
            != expected_resource_type
        ):
            continue

        target_count += 1

        resource_id = (
            resource.get(
                "id"
            )
        )

        if resource_id:

            keys.append(
                f"id:{resource_id}"
            )

        else:

            missing_ids += 1

            canonical = (
                json.dumps(
                    resource,
                    sort_keys=True,
                    separators=(
                        ",",
                        ":",
                    ),
                    ensure_ascii=False,
                )
                .encode("utf-8")
            )

            keys.append(
                "hash:"
                + sha256(
                    canonical
                )
                .hexdigest()
                .upper()
            )

    total = bundle.get(
        "total"
    )

    if (
        total is not None
        and not isinstance(
            total,
            int,
        )
    ):
        total = None

    return PageData(
        page_number=
            page_number,

        raw=
            raw,

        bundle_total=
            total,

        entry_count=
            len(entries),

        target_resource_count=
            target_count,

        resource_keys=
            tuple(keys),

        missing_resource_id_count=
            missing_ids,

        next_url=
            _find_link(
                bundle,
                "next",
            ),

        self_present=
            bool(
                _find_link(
                    bundle,
                    "self",
                )
            ),
    )


def summarize_pages(
    resource_type: str,
    pages: list[PageData],
) -> FetchResult:

    seen: set[str] = set()

    duplicates = 0
    missing_ids = 0

    for page in pages:

        missing_ids += (
            page
            .missing_resource_id_count
        )

        for key in (
            page.resource_keys
        ):

            if key in seen:
                duplicates += 1

            else:
                seen.add(
                    key
                )

    if duplicates:

        raise FHIRIngestionError(
            f"Duplicate "
            f"{resource_type} "
            "resources were detected "
            "across paginated pages."
        )

    raw_count = sum(
        page.target_resource_count
        for page in pages
    )

    if raw_count != len(seen):

        raise FHIRIngestionError(
            f"Raw and unique "
            f"{resource_type} "
            "counts do not reconcile."
        )

    totals = tuple(
        page.bundle_total
        for page in pages
    )

    warnings: list[str] = []

    non_null_totals = [
        value
        for value in totals
        if value is not None
    ]

    if (
        non_null_totals
        and
        any(
            value != len(seen)
            for value
            in non_null_totals
        )
    ):

        warnings.append(
            "Bundle.total does not "
            "reconcile to the full "
            "paginated result set; "
            "completeness is controlled "
            "by following "
            "Bundle.link[next] until "
            "absent plus resource-key "
            "reconciliation."
        )

    if missing_ids:

        warnings.append(
            f"{missing_ids} "
            f"{resource_type} "
            "resource(s) had no id; "
            "canonical content hashes "
            "were used as fallback "
            "resource keys."
        )

    return FetchResult(
        resource_type=
            resource_type,

        pages=
            tuple(pages),

        unique_resource_count=
            len(seen),

        duplicate_resource_count=
            duplicates,

        missing_resource_id_count=
            missing_ids,

        bundle_total_values=
            totals,

        warnings=
            tuple(warnings),
    )


def _read_with_retry(
    request: Request,
    *,
    retries: int = 3,
    timeout_seconds: int = 120,
) -> bytes:

    retryable = {
        429,
        500,
        502,
        503,
        504,
    }

    for attempt in range(
        retries + 1
    ):

        try:

            with urlopen(
                request,
                timeout=
                    timeout_seconds,
            ) as response:

                return (
                    response.read()
                )

        except HTTPError as exc:

            if (
                exc.code
                not in retryable
                or
                attempt >= retries
            ):

                raise (
                    FHIRIngestionError(
                        "FHIR request "
                        "failed with "
                        f"HTTP {exc.code}."
                    )
                ) from exc

            retry_after = (
                exc.headers.get(
                    "Retry-After"
                )
                if exc.headers
                else None
            )

            delay = (
                float(retry_after)
                if (
                    retry_after
                    and
                    retry_after.isdigit()
                )
                else 2 ** attempt
            )

            time.sleep(
                min(
                    delay,
                    30,
                )
            )

        except URLError as exc:

            if attempt >= retries:

                raise (
                    FHIRIngestionError(
                        "FHIR connection "
                        "failed: "
                        f"{exc.reason}"
                    )
                ) from exc

            time.sleep(
                min(
                    2 ** attempt,
                    30,
                )
            )

    raise FHIRIngestionError(
        "FHIR request retry loop "
        "ended unexpectedly."
    )


def fetch_resource(
    settings: Settings,
    token: TokenSet,
    resource_type: str,
    *,
    page_size: int = 50,
    max_pages: int = 1000,
) -> FetchResult:

    if not 1 <= page_size <= 50:

        raise ValueError(
            "page_size must be "
            "between 1 and 50."
        )

    current_url = (
        f"{settings.fhir_base_url}/"
        f"{resource_type}/"
        f"?_count={page_size}"
    )

    seen_urls: set[str] = set()

    pages: list[
        PageData
    ] = []

    while current_url:

        if current_url in seen_urls:

            raise FHIRIngestionError(
                "FHIR pagination "
                "loop detected."
            )

        if len(pages) >= max_pages:

            raise FHIRIngestionError(
                "FHIR pagination "
                "safety limit exceeded."
            )

        if pages:

            validate_next_url(
                settings,
                current_url,
            )

        seen_urls.add(
            current_url
        )

        request = Request(
            current_url,
            method="GET",
            headers={
                "Authorization":
                    "Bearer "
                    f"{token.access_token}",

                "Accept":
                    "application/json",
            },
        )

        raw = _read_with_retry(
            request
        )

        page = parse_bundle_page(
            raw,
            resource_type,
            len(pages) + 1,
        )

        pages.append(
            page
        )

        current_url = (
            page.next_url
        )

    if not pages:

        raise FHIRIngestionError(
            "No FHIR pages were "
            "returned for "
            f"{resource_type}."
        )

    if pages[-1].next_url:

        raise FHIRIngestionError(
            "Final pagination page "
            "unexpectedly retained "
            "a next link."
        )

    return summarize_pages(
        resource_type,
        pages,
    )
