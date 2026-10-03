from hashlib import sha256
from pathlib import Path
from urllib.parse import urlparse
import json


class ReferenceNormalizationError(RuntimeError):
    pass


OUTPUT_ENTITIES = (
    "bridge_claim_coverage",
    "provider_reference",
    "payer_reference",
    "contained_resource",
)


NORMALIZATION_VERSION = "v2"


def canonical_json(value):

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def fragment_hash(value):

    return sha256(
        canonical_json(value).encode(
            "utf-8"
        )
    ).hexdigest().upper()


def identity_hash(material):

    if material is None:
        return None

    return sha256(
        material.encode(
            "utf-8"
        )
    ).hexdigest().upper()


def load_jsonl(path):

    return [
        json.loads(line)
        for line in Path(path).read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def load_source_resources(staging_run):

    staging_run = Path(staging_run)

    resources = []
    seen = set()

    for entity in (
        "stg_patient",
        "stg_coverage",
        "stg_eob_claim",
    ):

        path = (
            staging_run
            / f"{entity}.jsonl"
        )

        if not path.is_file():

            raise ReferenceNormalizationError(
                f"Missing staging source: {path}"
            )

        for row in load_jsonl(path):

            fragment = row.get(
                "source_fragment_json"
            )

            if not isinstance(
                fragment,
                str,
            ):

                raise ReferenceNormalizationError(
                    "Missing source fragment"
                )

            resource = json.loads(
                fragment
            )

            resource_type = (
                resource.get(
                    "resourceType"
                )
            )

            resource_id = (
                resource.get("id")
            )

            if (
                not resource_type
                or not resource_id
            ):

                raise ReferenceNormalizationError(
                    "FHIR resource missing type/id"
                )

            key = (
                resource_type,
                resource_id,
            )

            if key in seen:

                raise ReferenceNormalizationError(
                    f"Duplicate resource: {key}"
                )

            seen.add(key)
            resources.append(resource)

    return resources


def contained_index(resource):

    result = {}

    for item in (
        resource.get(
            "contained",
            [],
        )
        or []
    ):

        if not isinstance(item, dict):
            continue

        contained_id = item.get("id")

        if not contained_id:
            continue

        if contained_id in result:

            raise ReferenceNormalizationError(
                "Duplicate contained id "
                f"within parent: {contained_id}"
            )

        result[contained_id] = item

    return result


def normalize_reference(
    reference_object,
    parent_resource_type,
    parent_resource_id,
    contained,
):

    if not isinstance(
        reference_object,
        dict,
    ):
        reference_object = {}

    reference = (
        reference_object.get(
            "reference"
        )
    )

    identifier = (
        reference_object.get(
            "identifier"
        )
    )

    if not isinstance(
        identifier,
        dict,
    ):
        identifier = {}

    identifier_system = (
        identifier.get(
            "system"
        )
    )

    identifier_value = (
        identifier.get(
            "value"
        )
    )

    display = (
        reference_object.get(
            "display"
        )
    )

    result = {
        "reference_value":
            reference,

        "reference_form":
            "NULL",

        "target_resource_type":
            None,

        "target_id":
            None,

        "contained_id":
            None,

        "identifier_system":
            identifier_system,

        "identifier_value":
            identifier_value,

        "display":
            display,

        "identity_key_sha256":
            None,

        "resolution_status":
            "SOURCE_IDENTITY_NOT_EXPLICIT",
    }

    if (
        isinstance(reference, str)
        and reference.strip()
    ):

        value = reference.strip()

        if value.startswith("#"):

            contained_id = value[1:]

            target = contained.get(
                contained_id
            )

            result[
                "reference_form"
            ] = "CONTAINED"

            result[
                "contained_id"
            ] = contained_id

            result[
                "target_id"
            ] = contained_id

            if isinstance(
                target,
                dict,
            ):

                result[
                    "target_resource_type"
                ] = target.get(
                    "resourceType"
                )

                result[
                    "resolution_status"
                ] = "CONTAINED_RESOLVED"

                material = (
                    "CONTAINED|"
                    f"{parent_resource_type}|"
                    f"{parent_resource_id}|"
                    f"{contained_id}"
                )

                result[
                    "identity_key_sha256"
                ] = identity_hash(
                    material
                )

            else:

                result[
                    "resolution_status"
                ] = "CONTAINED_UNRESOLVED"

            return result

        if value.startswith(
            (
                "http://",
                "https://",
            )
        ):

            segments = [
                segment
                for segment
                in urlparse(
                    value
                ).path.split("/")
                if segment
            ]

            result[
                "reference_form"
            ] = "ABSOLUTE"

            if len(segments) >= 2:

                result[
                    "target_resource_type"
                ] = segments[-2]

                result[
                    "target_id"
                ] = segments[-1]

            result[
                "resolution_status"
            ] = "REFERENCE_KEY_READY"

            result[
                "identity_key_sha256"
            ] = identity_hash(
                "REFERENCE|" + value
            )

            return result

        if "/" in value:

            target_type, target_id = (
                value.split("/", 1)
            )

            result[
                "reference_form"
            ] = "RELATIVE"

            result[
                "target_resource_type"
            ] = target_type or None

            result[
                "target_id"
            ] = target_id or None

            result[
                "resolution_status"
            ] = "REFERENCE_KEY_READY"

            result[
                "identity_key_sha256"
            ] = identity_hash(
                "REFERENCE|" + value
            )

            return result

        result[
            "reference_form"
        ] = "OTHER"

        result[
            "target_id"
        ] = value

        result[
            "resolution_status"
        ] = "REFERENCE_KEY_READY"

        result[
            "identity_key_sha256"
        ] = identity_hash(
            "REFERENCE|" + value
        )

        return result

    if identifier_value:

        result[
            "reference_form"
        ] = "IDENTIFIER"

        result[
            "resolution_status"
        ] = "IDENTIFIER_KEY_READY"

        result[
            "identity_key_sha256"
        ] = identity_hash(
            "IDENTIFIER|"
            f"{identifier_system or ''}|"
            f"{identifier_value}"
        )

        return result

    if display:

        result[
            "reference_form"
        ] = "DISPLAY_ONLY"

        result[
            "resolution_status"
        ] = "DISPLAY_ONLY_NON_IDENTITY"

        # Deliberately DO NOT generate an identity
        # from display text. Display equality is not
        # evidence of real-world identity.

        return result

    # Source object may exist but contain no usable
    # identity material. Preserve the occurrence,
    # but do not fabricate an identity.

    result[
        "resolution_status"
    ] = "SOURCE_IDENTITY_NOT_EXPLICIT"

    return result


def _reference_row(
    pipeline_run_id,
    source_context,
    parent_resource_type,
    parent_resource_id,
    parent_sequence,
    occurrence_ordinal,
    reference_object,
    contained,
):

    normalized = (
        normalize_reference(
            reference_object,
            parent_resource_type,
            parent_resource_id,
            contained,
        )
    )

    fragment = (
        reference_object
        if isinstance(
            reference_object,
            dict,
        )
        else {}
    )

    return {
        "pipeline_run_id":
            pipeline_run_id,

        "source_context":
            source_context,

        "parent_resource_type":
            parent_resource_type,

        "parent_resource_id":
            parent_resource_id,

        "parent_sequence":
            parent_sequence,

        "occurrence_ordinal":
            occurrence_ordinal,

        **normalized,

        "reference_fragment_json":
            canonical_json(
                fragment
            ),

        "raw_record_hash":
            fragment_hash(
                fragment
            ),
    }


def normalize_resources(
    resources,
    pipeline_run_id,
):

    output = {
        entity: []
        for entity
        in OUTPUT_ENTITIES
    }

    for resource in resources:

        resource_type = (
            resource[
                "resourceType"
            ]
        )

        resource_id = (
            resource["id"]
        )

        contained = (
            contained_index(
                resource
            )
        )

        for ordinal, item in enumerate(
            (
                resource.get(
                    "contained",
                    [],
                )
                or []
            ),
            start=1,
        ):

            if not isinstance(
                item,
                dict,
            ):
                continue

            contained_id = item.get(
                "id"
            )

            contained_type = item.get(
                "resourceType"
            )

            if (
                not contained_id
                or not contained_type
            ):

                raise ReferenceNormalizationError(
                    "Contained resource "
                    "missing id/type"
                )

            output[
                "contained_resource"
            ].append({
                "pipeline_run_id":
                    pipeline_run_id,

                "parent_resource_type":
                    resource_type,

                "parent_resource_id":
                    resource_id,

                "source_ordinal":
                    ordinal,

                "contained_id":
                    contained_id,

                "contained_resource_type":
                    contained_type,

                "identifiers_json":
                    canonical_json(
                        item.get(
                            "identifier",
                            [],
                        )
                    ),

                "name_json":
                    canonical_json(
                        item.get("name")
                    ),

                "source_fragment_json":
                    canonical_json(item),

                "raw_record_hash":
                    fragment_hash(item),
            })

        if (
            resource_type
            == "ExplanationOfBenefit"
        ):

            for ordinal, insurance in enumerate(
                (
                    resource.get(
                        "insurance",
                        [],
                    )
                    or []
                ),
                start=1,
            ):

                if not isinstance(
                    insurance,
                    dict,
                ):

                    raise ReferenceNormalizationError(
                        "EOB insurance element "
                        "is not an object"
                    )

                coverage = (
                    insurance.get(
                        "coverage"
                    )
                )

                if not isinstance(
                    coverage,
                    dict,
                ):

                    raise ReferenceNormalizationError(
                        "EOB insurance.coverage "
                        "missing"
                    )

                normalized = (
                    normalize_reference(
                        coverage,
                        resource_type,
                        resource_id,
                        contained,
                    )
                )

                association_material = (
                    "CLAIM_COVERAGE_ASSOCIATION|"
                    f"{pipeline_run_id}|"
                    f"{resource_id}|"
                    f"{ordinal}"
                )

                output[
                    "bridge_claim_coverage"
                ].append({
                    "pipeline_run_id":
                        pipeline_run_id,

                    "eob_id":
                        resource_id,

                    "insurance_ordinal":
                        ordinal,

                    "association_key_sha256":
                        identity_hash(
                            association_material
                        ),

                    "focal":
                        insurance.get(
                            "focal"
                        ),

                    "coverage_reference":
                        normalized[
                            "reference_value"
                        ],

                    "coverage_reference_form":
                        normalized[
                            "reference_form"
                        ],

                    "coverage_target_resource_type":
                        normalized[
                            "target_resource_type"
                        ],

                    "coverage_target_id":
                        normalized[
                            "target_id"
                        ],

                    "coverage_display":
                        normalized[
                            "display"
                        ],

                    "coverage_identity_key_sha256":
                        normalized[
                            "identity_key_sha256"
                        ],

                    "coverage_resolution_status":
                        normalized[
                            "resolution_status"
                        ],

                    "preauth_json":
                        canonical_json(
                            insurance.get(
                                "preAuthRef",
                                [],
                            )
                        ),

                    "source_fragment_json":
                        canonical_json(
                            insurance
                        ),

                    "raw_record_hash":
                        fragment_hash(
                            insurance
                        ),
                })

            provider = resource.get(
                "provider"
            )

            if isinstance(
                provider,
                dict,
            ):

                output[
                    "provider_reference"
                ].append(
                    _reference_row(
                        pipeline_run_id,
                        "CLAIM_PROVIDER",
                        resource_type,
                        resource_id,
                        None,
                        1,
                        provider,
                        contained,
                    )
                )

            insurer = resource.get(
                "insurer"
            )

            if isinstance(
                insurer,
                dict,
            ):

                output[
                    "payer_reference"
                ].append(
                    _reference_row(
                        pipeline_run_id,
                        "CLAIM_INSURER",
                        resource_type,
                        resource_id,
                        None,
                        1,
                        insurer,
                        contained,
                    )
                )

            for ordinal, care_team in enumerate(
                (
                    resource.get(
                        "careTeam",
                        [],
                    )
                    or []
                ),
                start=1,
            ):

                if not isinstance(
                    care_team,
                    dict,
                ):
                    continue

                provider = (
                    care_team.get(
                        "provider"
                    )
                )

                if not isinstance(
                    provider,
                    dict,
                ):
                    continue

                output[
                    "provider_reference"
                ].append(
                    _reference_row(
                        pipeline_run_id,
                        "CARE_TEAM_PROVIDER",
                        resource_type,
                        resource_id,
                        care_team.get(
                            "sequence"
                        ),
                        ordinal,
                        provider,
                        contained,
                    )
                )

        elif (
            resource_type
            == "Coverage"
        ):

            for ordinal, payor in enumerate(
                (
                    resource.get(
                        "payor",
                        [],
                    )
                    or []
                ),
                start=1,
            ):

                if not isinstance(
                    payor,
                    dict,
                ):
                    continue

                output[
                    "payer_reference"
                ].append(
                    _reference_row(
                        pipeline_run_id,
                        "COVERAGE_PAYOR",
                        resource_type,
                        resource_id,
                        None,
                        ordinal,
                        payor,
                        contained,
                    )
                )

    return output


def normalize_staging_run(
    staging_run,
    pipeline_run_id,
):

    return normalize_resources(
        load_source_resources(
            staging_run
        ),
        pipeline_run_id,
    )
