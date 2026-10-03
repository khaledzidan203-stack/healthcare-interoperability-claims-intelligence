from collections import Counter
from pathlib import Path
import json


class TerminologyError(RuntimeError):
    pass


def source_family(system):

    if not system:
        return "NO_SYSTEM"

    value = system.lower()

    if "bluebutton.cms.gov" in value:
        return "CMS_BLUE_BUTTON"

    if "cms.gov" in value:
        return "CMS"

    if "terminology.hl7.org" in value:
        return "HL7_TERMINOLOGY"

    if "hl7.org/fhir" in value:
        return "HL7_FHIR"

    if "snomed.info" in value:
        return "SNOMED_CT"

    if "loinc.org" in value:
        return "LOINC"

    if "ama-assn.org" in value:
        return "AMA_CPT"

    if "cdc.gov" in value:
        return "CDC"

    if value.startswith("urn:oid:"):
        return "OID"

    return "EXTERNAL_OR_UNKNOWN"


def reference_form(reference):

    if not reference:
        return "NULL"

    if reference.startswith("#"):
        return "CONTAINED"

    if reference.startswith("urn:"):
        return "URN"

    if (
        reference.startswith("http://")
        or reference.startswith("https://")
    ):
        return "ABSOLUTE"

    if "/" in reference:
        return "RELATIVE"

    return "OTHER"


def reference_target_type(
    reference,
    contained_types=None,
):

    if not reference:
        return "UNKNOWN"

    contained_types = (
        contained_types
        if isinstance(contained_types, dict)
        else {}
    )

    if reference.startswith("#"):

        return contained_types.get(
            reference[1:],
            "UNRESOLVED_CONTAINED_TYPE",
        )

    value = reference.rstrip("/")

    if value.startswith(
        ("http://", "https://")
    ):

        parts = value.split("/")

        if len(parts) >= 2:
            return parts[-2]

        return "UNKNOWN"

    if "/" in value:
        return value.split("/", 1)[0]

    return "UNKNOWN"


def iter_resources(run_dir):

    run_dir = Path(run_dir)

    if not run_dir.is_dir():
        raise TerminologyError(
            f"RAW run missing: {run_dir}"
        )

    seen = set()

    for path in sorted(
        run_dir.glob("*_bundle_page_*.json")
    ):

        bundle = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if bundle.get("resourceType") != "Bundle":
            raise TerminologyError(
                f"Expected Bundle: {path.name}"
            )

        for entry in (
            bundle.get("entry", [])
            or []
        ):

            if not isinstance(entry, dict):
                continue

            resource = entry.get("resource")

            if not isinstance(
                resource,
                dict,
            ):
                continue

            resource_type = resource.get(
                "resourceType"
            )

            resource_id = resource.get("id")

            if not resource_type or not resource_id:
                raise TerminologyError(
                    "FHIR resource missing type or id"
                )

            key = (
                resource_type,
                resource_id,
            )

            if key in seen:
                raise TerminologyError(
                    f"Duplicate resource: {key}"
                )

            seen.add(key)

            yield resource


def _walk(
    value,
    resource_type,
    path,
    contained_types,
    coding_counter,
    reference_counter,
):

    if isinstance(value, dict):

        code = value.get("code")
        system = value.get("system")
        display = value.get("display")

        if isinstance(code, str):

            coding_counter[
                (
                    resource_type,
                    path,
                    system or "",
                    code,
                    display or "",
                    source_family(system),
                )
            ] += 1

        for key, child in value.items():

            child_path = (
                f"{path}.{key}"
            )

            if (
                key == "reference"
                and isinstance(child, str)
            ):

                reference_counter[
                    (
                        resource_type,
                        path,
                        reference_form(child),
                        reference_target_type(
                            child,
                            contained_types,
                        ),
                    )
                ] += 1

            _walk(
                child,
                resource_type,
                child_path,
                contained_types,
                coding_counter,
                reference_counter,
            )

    elif isinstance(value, list):

        for index, child in enumerate(value):

            _walk(
                child,
                resource_type,
                f"{path}[{index}]",
                contained_types,
                coding_counter,
                reference_counter,
            )


def inventory_run(run_dir):

    coding_counter = Counter()
    reference_counter = Counter()
    profile_counter = Counter()
    contained_counter = Counter()

    resources = list(
        iter_resources(run_dir)
    )

    for resource in resources:

        resource_type = resource[
            "resourceType"
        ]

        contained_types = {}

        for item in (
            resource.get("contained", [])
            or []
        ):

            if not isinstance(item, dict):
                continue

            contained_id = item.get("id")
            contained_type = item.get(
                "resourceType"
            )

            if (
                contained_id
                and contained_type
            ):

                contained_types[
                    contained_id
                ] = contained_type

                contained_counter[
                    (
                        resource_type,
                        contained_type,
                    )
                ] += 1

        profiles = (
            (resource.get("meta") or {})
            .get("profile", [])
            or []
        )

        for profile in profiles:

            if isinstance(profile, str):

                profile_counter[
                    (
                        resource_type,
                        profile,
                    )
                ] += 1

        _walk(
            resource,
            resource_type,
            "$",
            contained_types,
            coding_counter,
            reference_counter,
        )

    return {
        "resource_count": len(resources),
        "coding_counter":
            coding_counter,
        "reference_counter":
            reference_counter,
        "profile_counter":
            profile_counter,
        "contained_counter":
            contained_counter,
    }


def financial_category_inventory(
    run_dir,
):

    counter = Counter()

    for resource in iter_resources(
        run_dir
    ):

        if (
            resource.get("resourceType")
            != "ExplanationOfBenefit"
        ):
            continue

        for adjudication in (
            resource.get(
                "adjudication",
                [],
            )
            or []
        ):

            for coding in (
                (
                    adjudication.get(
                        "category"
                    )
                    or {}
                ).get(
                    "coding",
                    [],
                )
                or []
            ):

                counter[
                    (
                        "CLAIM_ADJUDICATION",
                        coding.get(
                            "system",
                            "",
                        ),
                        coding.get(
                            "code",
                            "",
                        ),
                        coding.get(
                            "display",
                            "",
                        ),
                    )
                ] += 1

        for total in (
            resource.get(
                "total",
                [],
            )
            or []
        ):

            for coding in (
                (
                    total.get(
                        "category"
                    )
                    or {}
                ).get(
                    "coding",
                    [],
                )
                or []
            ):

                counter[
                    (
                        "CLAIM_TOTAL",
                        coding.get(
                            "system",
                            "",
                        ),
                        coding.get(
                            "code",
                            "",
                        ),
                        coding.get(
                            "display",
                            "",
                        ),
                    )
                ] += 1

        for item in (
            resource.get(
                "item",
                [],
            )
            or []
        ):

            for adjudication in (
                item.get(
                    "adjudication",
                    [],
                )
                or []
            ):

                for coding in (
                    (
                        adjudication.get(
                            "category"
                        )
                        or {}
                    ).get(
                        "coding",
                        [],
                    )
                    or []
                ):

                    counter[
                        (
                            "ITEM_ADJUDICATION",
                            coding.get(
                                "system",
                                "",
                            ),
                            coding.get(
                                "code",
                                "",
                            ),
                            coding.get(
                                "display",
                                "",
                            ),
                        )
                    ] += 1

    return counter
