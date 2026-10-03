from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
import csv
import json


SOURCE_SYSTEM = "CMS_BLUE_BUTTON_SANDBOX_V3"


TARGET_ENTITIES = (
    "dim_date",
    "dim_pipeline_run",
    "dim_patient",
    "dim_coverage",
    "dim_financial_concept",
    "dim_currency",
    "dim_claim_type",
    "dim_service_code",
    "dim_diagnosis",
    "dim_procedure",
    "dim_provider",
    "dim_payer",
    "dim_supporting_info_category",
    "fact_claim",
    "fact_item",
    "fact_claim_total",
    "fact_claim_adjudication",
    "fact_item_adjudication",
    "fact_diagnosis_occurrence",
    "fact_procedure_occurrence",
    "fact_care_team_occurrence",
    "fact_supporting_info_occurrence",
    "fact_item_detail",
    "bridge_claim_coverage",
)


FACT_SOURCE_MAP = {
    "fact_claim":
        "stg_eob_claim",

    "fact_item":
        "stg_eob_item",

    "fact_claim_total":
        "stg_eob_total",

    "fact_claim_adjudication":
        "stg_eob_adjudication",

    "fact_item_adjudication":
        "stg_eob_item_adjudication",

    "fact_diagnosis_occurrence":
        "stg_eob_diagnosis",

    "fact_procedure_occurrence":
        "stg_eob_procedure",

    "fact_care_team_occurrence":
        "stg_eob_care_team",

    "fact_supporting_info_occurrence":
        "stg_eob_supporting_info",

    "fact_item_detail":
        "stg_eob_item_detail",
}


class AnalyticsLoadError(RuntimeError):
    pass


def canonical_json(value):

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def read_jsonl(path):

    path = Path(path)

    if not path.is_file():

        raise AnalyticsLoadError(
            f"Missing source file: {path}"
        )

    return [
        json.loads(line)
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def parse_fragment(row):

    value = row.get(
        "source_fragment_json"
    )

    if isinstance(value, dict):
        return value

    if isinstance(value, str):

        try:
            return json.loads(value)

        except json.JSONDecodeError as exc:

            raise AnalyticsLoadError(
                "Invalid source_fragment_json"
            ) from exc

    return {}


def parse_json_value(value, default=None):

    if value is None:
        return default

    if isinstance(
        value,
        (
            dict,
            list,
            int,
            float,
            bool,
        ),
    ):
        return value

    if isinstance(value, str):

        stripped = value.strip()

        if not stripped:
            return default

        try:
            return json.loads(
                stripped
            )

        except json.JSONDecodeError:
            return value

    return value


def iso_date(value):

    if value in (
        None,
        "",
    ):
        return None

    if isinstance(
        value,
        datetime,
    ):
        return value.date()

    if isinstance(
        value,
        date,
    ):
        return value

    text = str(value).strip()

    if not text:
        return None

    try:
        return date.fromisoformat(
            text[:10]
        )

    except ValueError as exc:

        raise AnalyticsLoadError(
            f"Invalid date value: {text}"
        ) from exc


def date_key(value):

    parsed = iso_date(value)

    if parsed is None:
        return None

    return int(
        parsed.strftime(
            "%Y%m%d"
        )
    )


def build_date_rows(values):

    parsed = sorted(
        {
            iso_date(value)
            for value in values
            if iso_date(value)
            is not None
        }
    )

    if not parsed:
        raise AnalyticsLoadError(
            "No analytical dates found"
        )

    start = parsed[0]
    end = parsed[-1]

    span = (
        end - start
    ).days

    if span > 50000:
        raise AnalyticsLoadError(
            "Unexpected analytical calendar span"
        )

    rows = []

    current = start

    while current <= end:

        rows.append({
            "date_key":
                int(
                    current.strftime(
                        "%Y%m%d"
                    )
                ),

            "calendar_date":
                current.isoformat(),

            "calendar_year":
                current.year,

            "calendar_quarter":
                (
                    (
                        current.month
                        - 1
                    )
                    // 3
                )
                + 1,

            "month_number":
                current.month,

            "month_name":
                current.strftime(
                    "%B"
                ),

            "day_of_month":
                current.day,

            "day_of_week":
                current.isoweekday(),

            "day_name":
                current.strftime(
                    "%A"
                ),

            "is_weekend":
                current.isoweekday()
                in (6, 7),
        })

        current += timedelta(
            days=1
        )

    return rows


def reference_target_id(reference):

    if not isinstance(
        reference,
        str,
    ):
        return None

    value = reference.strip()

    if not value:
        return None

    if value.startswith("#"):
        return None

    if value.startswith(
        (
            "http://",
            "https://",
        )
    ):

        segments = [
            segment
            for segment in (
                urlparse(
                    value
                ).path.split("/")
            )
            if segment
        ]

        if len(segments) >= 1:
            return segments[-1]

        return None

    if "/" in value:
        return value.split("/", 1)[1]

    return value


def reference_target_type(reference):

    if not isinstance(
        reference,
        str,
    ):
        return None

    value = reference.strip()

    if not value:
        return None

    if value.startswith("#"):
        return None

    if value.startswith(
        (
            "http://",
            "https://",
        )
    ):

        segments = [
            segment
            for segment in (
                urlparse(
                    value
                ).path.split("/")
            )
            if segment
        ]

        if len(segments) >= 2:
            return segments[-2]

        return None

    if "/" in value:
        return value.split("/", 1)[0]

    return None


def coding_display(
    concept,
    system,
    code,
):

    if not isinstance(
        concept,
        dict,
    ):
        return None

    for coding in (
        concept.get(
            "coding",
            [],
        )
        or []
    ):

        if not isinstance(
            coding,
            dict,
        ):
            continue

        if (
            coding.get("system")
            == system
            and coding.get("code")
            == code
        ):

            return coding.get(
                "display"
            )

    return None


def quantity_parts(value):

    value = parse_json_value(
        value,
        {},
    )

    if not isinstance(
        value,
        dict,
    ):
        return (
            None,
            None,
        )

    return (
        value.get("value"),
        value.get("unit")
        or value.get("code"),
    )


def build_identity_dimension(
    rows,
    unknown_required=False,
):

    grouped = defaultdict(
        list
    )

    for row in rows:

        identity = row.get(
            "identity_key_sha256"
        )

        if identity:

            grouped[
                identity
            ].append(row)

    result = []

    if unknown_required:

        result.append({
            "identity_key_sha256":
                None,

            "identity_status":
                "UNKNOWN_SOURCE_IDENTITY_NOT_EXPLICIT",

            "target_resource_type":
                None,

            "identifier_system":
                None,

            "identifier_value":
                None,

            "display":
                "Unknown / Source Identity Not Explicit",

            "is_unknown":
                True,

            "attributes_json":
                canonical_json({
                    "governance":
                        "Explicit warehouse unknown member"
                }),
        })

    for identity in sorted(
        grouped
    ):

        group = grouped[
            identity
        ]

        def first_nonempty(field):

            values = sorted({
                str(row[field])
                for row in group
                if row.get(field)
                not in (
                    None,
                    "",
                )
            })

            return (
                values[0]
                if values
                else None
            )

        result.append({
            "identity_key_sha256":
                identity,

            "identity_status":
                "SOURCE_IDENTITY_READY",

            "target_resource_type":
                first_nonempty(
                    "target_resource_type"
                ),

            "identifier_system":
                first_nonempty(
                    "identifier_system"
                ),

            "identifier_value":
                first_nonempty(
                    "identifier_value"
                ),

            "display":
                first_nonempty(
                    "display"
                ),

            "is_unknown":
                False,

            "attributes_json":
                canonical_json({
                    "source_contexts":
                        sorted({
                            row.get(
                                "source_context"
                            )
                            for row
                            in group
                            if row.get(
                                "source_context"
                            )
                        }),

                    "occurrence_count":
                        len(group),
                }),
        })

    return result


def _dimension_from_pairs(
    pairs,
    dimension_type,
):

    rows = []

    for (
        system,
        code,
        source_display,
    ) in sorted(
        pairs
    ):

        if not system or not code:
            continue

        row = {
            "system_uri":
                system,

            "code":
                code,

            "source_display":
                source_display,

            "authoritative_display":
                None,

            "mapping_status":
                "AUTHORITATIVE_MAPPING_PENDING",

            "authority":
                None,

            "authority_version":
                None,
        }

        rows.append(row)

    return rows


def build_analytics_bundle(
    staging_run,
    reference_run,
    financial_mapping_csv,
    pipeline_run_id,
    pipeline_run_status,
    source_system=SOURCE_SYSTEM,
):

    staging_run = Path(
        staging_run
    )

    reference_run = Path(
        reference_run
    )

    staging = {}

    for entity in (
        "stg_patient",
        "stg_coverage",
        "stg_eob_claim",
        "stg_eob_item",
        "stg_eob_diagnosis",
        "stg_eob_procedure",
        "stg_eob_care_team",
        "stg_eob_supporting_info",
        "stg_eob_adjudication",
        "stg_eob_total",
        "stg_eob_item_adjudication",
        "stg_eob_item_detail",
    ):

        staging[
            entity
        ] = read_jsonl(
            staging_run
            / f"{entity}.jsonl"
        )

    references = {}

    for entity in (
        "bridge_claim_coverage",
        "provider_reference",
        "payer_reference",
        "contained_resource",
    ):

        references[
            entity
        ] = read_jsonl(
            reference_run
            / f"{entity}.jsonl"
        )

    with Path(
        financial_mapping_csv
    ).open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:

        financial_mapping_rows = list(
            csv.DictReader(handle)
        )

    bundle = {
        entity: []
        for entity
        in TARGET_ENTITIES
    }

    # ------------------------------------------------------
    # Pipeline run dimension seed.
    # Manifest hashes are populated by the physical loader.
    # ------------------------------------------------------

    bundle[
        "dim_pipeline_run"
    ] = [{
        "pipeline_run_id":
            pipeline_run_id,

        "run_status":
            pipeline_run_status,

        "raw_manifest_sha256":
            None,

        "staging_manifest_sha256":
            None,
    }]

    # ------------------------------------------------------
    # Patient
    # ------------------------------------------------------

    patient_ids = set()

    for row in staging[
        "stg_patient"
    ]:

        patient_id = row.get(
            "patient_id"
        )

        if not patient_id:

            raise AnalyticsLoadError(
                "Patient row missing patient_id"
            )

        patient_ids.add(
            patient_id
        )

        fragment = parse_fragment(
            row
        )

        bundle[
            "dim_patient"
        ].append({
            "source_system":
                source_system,

            "patient_id":
                patient_id,

            "birth_date":
                fragment.get(
                    "birthDate"
                ),

            "gender":
                fragment.get(
                    "gender"
                ),

            "valid_from_pipeline_run_id":
                pipeline_run_id,

            "valid_to_pipeline_run_id":
                None,

            "is_current":
                True,

            "row_hash":
                row[
                    "raw_record_hash"
                ],

            "attributes_json":
                canonical_json({
                    "active":
                        fragment.get(
                            "active"
                        )
                }),
        })

    # ------------------------------------------------------
    # Coverage
    # ------------------------------------------------------

    coverage_ids = set()

    for row in staging[
        "stg_coverage"
    ]:

        coverage_id = row.get(
            "coverage_id"
        )

        if not coverage_id:

            raise AnalyticsLoadError(
                "Coverage row missing coverage_id"
            )

        coverage_ids.add(
            coverage_id
        )

        fragment = parse_fragment(
            row
        )

        period = (
            fragment.get(
                "period"
            )
            or {}
        )

        bundle[
            "dim_coverage"
        ].append({
            "source_system":
                source_system,

            "coverage_id":
                coverage_id,

            "coverage_status":
                row.get(
                    "status"
                )
                or fragment.get(
                    "status"
                ),

            "subscriber_id":
                row.get(
                    "subscriber_id"
                )
                or fragment.get(
                    "subscriberId"
                ),

            "period_start":
                row.get(
                    "period_start"
                )
                or period.get(
                    "start"
                ),

            "period_end":
                row.get(
                    "period_end"
                )
                or period.get(
                    "end"
                ),

            "valid_from_pipeline_run_id":
                pipeline_run_id,

            "valid_to_pipeline_run_id":
                None,

            "is_current":
                True,

            "row_hash":
                row[
                    "raw_record_hash"
                ],

            "attributes_json":
                canonical_json({
                    "type":
                        fragment.get(
                            "type"
                        )
                }),
        })

    # ------------------------------------------------------
    # Financial concept dimension.
    # Dedupe domain-specific mapping rows to authoritative pair.
    # ------------------------------------------------------

    financial_lookup = {}
    financial_dim = {}

    for row in financial_mapping_rows:

        domain_key = (
            row["domain"],
            row["system_uri"],
            row["code"],
        )

        concept_key = (
            row["system_uri"],
            row["code"],
            row[
                "authority_version"
            ],
        )

        financial_lookup[
            domain_key
        ] = concept_key

        candidate = {
            "system_uri":
                row[
                    "system_uri"
                ],

            "code":
                row[
                    "code"
                ],

            "authority_version":
                row[
                    "authority_version"
                ],

            "authoritative_display":
                row[
                    "authoritative_display"
                ],

            "semantic_role":
                row[
                    "semantic_role"
                ],

            "aggregation_rule":
                row[
                    "aggregation_rule"
                ],

            "authority":
                row[
                    "authority"
                ],

            "authority_url":
                row[
                    "authority_url"
                ],

            "resolution_status":
                row[
                    "resolution_status"
                ],

            "kpi_status":
                row[
                    "kpi_status"
                ],
        }

        previous = financial_dim.get(
            concept_key
        )

        if (
            previous is not None
            and previous != candidate
        ):

            raise AnalyticsLoadError(
                "Conflicting authoritative "
                "financial concept mapping"
            )

        financial_dim[
            concept_key
        ] = candidate

    bundle[
        "dim_financial_concept"
    ] = [
        financial_dim[key]
        for key in sorted(
            financial_dim
        )
    ]

    # ------------------------------------------------------
    # Coded dimensions.
    # ------------------------------------------------------

    claim_type_pairs = set()

    for row in staging[
        "stg_eob_claim"
    ]:

        system = row.get(
            "claim_type_system"
        )

        code = row.get(
            "claim_type_code"
        )

        if system and code:

            fragment = parse_fragment(
                row
            )

            display = coding_display(
                fragment.get(
                    "type"
                ),
                system,
                code,
            )

            claim_type_pairs.add(
                (
                    system,
                    code,
                    display or "",
                )
            )

    bundle[
        "dim_claim_type"
    ] = _dimension_from_pairs(
        claim_type_pairs,
        "claim_type",
    )

    service_pairs = set()

    for entity in (
        "stg_eob_item",
        "stg_eob_item_detail",
    ):

        for row in staging[
            entity
        ]:

            system = row.get(
                "product_service_system"
            )

            code = row.get(
                "product_service_code"
            )

            if not (
                system
                and code
            ):
                continue

            fragment = parse_fragment(
                row
            )

            concept = (
                fragment.get(
                    "productOrService"
                )
                or {}
            )

            display = coding_display(
                concept,
                system,
                code,
            )

            service_pairs.add(
                (
                    system,
                    code,
                    display or "",
                )
            )

    bundle[
        "dim_service_code"
    ] = _dimension_from_pairs(
        service_pairs,
        "service",
    )

    diagnosis_pairs = set()

    for row in staging[
        "stg_eob_diagnosis"
    ]:

        system = row.get(
            "diagnosis_system"
        )

        code = row.get(
            "diagnosis_code"
        )

        if system and code:

            fragment = parse_fragment(
                row
            )

            display = coding_display(
                fragment.get(
                    "diagnosisCodeableConcept"
                ),
                system,
                code,
            )

            diagnosis_pairs.add(
                (
                    system,
                    code,
                    display or "",
                )
            )

    bundle[
        "dim_diagnosis"
    ] = _dimension_from_pairs(
        diagnosis_pairs,
        "diagnosis",
    )

    procedure_pairs = set()

    for row in staging[
        "stg_eob_procedure"
    ]:

        system = row.get(
            "procedure_system"
        )

        code = row.get(
            "procedure_code"
        )

        if system and code:

            fragment = parse_fragment(
                row
            )

            display = coding_display(
                fragment.get(
                    "procedureCodeableConcept"
                ),
                system,
                code,
            )

            procedure_pairs.add(
                (
                    system,
                    code,
                    display or "",
                )
            )

    bundle[
        "dim_procedure"
    ] = _dimension_from_pairs(
        procedure_pairs,
        "procedure",
    )

    support_pairs = set()

    for row in staging[
        "stg_eob_supporting_info"
    ]:

        system = row.get(
            "category_system"
        )

        code = row.get(
            "category_code"
        )

        if system and code:

            fragment = parse_fragment(
                row
            )

            display = coding_display(
                fragment.get(
                    "category"
                ),
                system,
                code,
            )

            support_pairs.add(
                (
                    system,
                    code,
                    display or "",
                )
            )

    bundle[
        "dim_supporting_info_category"
    ] = _dimension_from_pairs(
        support_pairs,
        "supporting_info",
    )

    # ------------------------------------------------------
    # Provider / payer dimensions.
    # ------------------------------------------------------

    bundle[
        "dim_provider"
    ] = build_identity_dimension(
        references[
            "provider_reference"
        ],
        unknown_required=True,
    )

    bundle[
        "dim_payer"
    ] = build_identity_dimension(
        references[
            "payer_reference"
        ],
        unknown_required=False,
    )

    provider_identity_set = {
        row[
            "identity_key_sha256"
        ]
        for row in bundle[
            "dim_provider"
        ]
        if row[
            "identity_key_sha256"
        ]
    }

    payer_identity_set = {
        row[
            "identity_key_sha256"
        ]
        for row in bundle[
            "dim_payer"
        ]
        if row[
            "identity_key_sha256"
        ]
    }

    # ------------------------------------------------------
    # Claim context.
    # ------------------------------------------------------

    claim_context = {}

    analytical_dates = []

    claim_provider_rows = {
        row[
            "parent_resource_id"
        ]:
            row
        for row in references[
            "provider_reference"
        ]
        if row.get(
            "source_context"
        )
        == "CLAIM_PROVIDER"
    }

    claim_payer_rows = {
        row[
            "parent_resource_id"
        ]:
            row
        for row in references[
            "payer_reference"
        ]
        if row.get(
            "source_context"
        )
        == "CLAIM_INSURER"
    }

    for row in staging[
        "stg_eob_claim"
    ]:

        eob_id = row.get(
            "eob_id"
        )

        fragment = parse_fragment(
            row
        )

        patient_reference = (
            row.get(
                "patient_reference"
            )
            or (
                fragment.get(
                    "patient"
                )
                or {}
            ).get(
                "reference"
            )
        )

        patient_id = (
            reference_target_id(
                patient_reference
            )
        )

        if patient_id not in patient_ids:

            raise AnalyticsLoadError(
                "Claim patient reference does "
                "not resolve to governed Patient"
            )

        created = (
            row.get(
                "created"
            )
            or fragment.get(
                "created"
            )
        )

        created_date_key = (
            date_key(
                created
            )
        )

        if created_date_key is None:

            raise AnalyticsLoadError(
                "Claim missing created date"
            )

        billable_period = (
            fragment.get(
                "billablePeriod"
            )
            or {}
        )

        billable_start = (
            row.get(
                "billable_period_start"
            )
            or billable_period.get(
                "start"
            )
        )

        billable_end = (
            row.get(
                "billable_period_end"
            )
            or billable_period.get(
                "end"
            )
        )

        analytical_dates.extend(
            [
                created,
                billable_start,
                billable_end,
            ]
        )

        provider = (
            claim_provider_rows.get(
                eob_id
            )
        )

        if provider is None:

            raise AnalyticsLoadError(
                "Claim missing normalized "
                "provider occurrence"
            )

        provider_identity = (
            provider.get(
                "identity_key_sha256"
            )
        )

        if provider_identity:

            if (
                provider_identity
                not in provider_identity_set
            ):

                raise AnalyticsLoadError(
                    "Claim provider identity "
                    "missing from dimension"
                )

            provider_unknown = False

        else:

            if (
                provider.get(
                    "resolution_status"
                )
                !=
                "SOURCE_IDENTITY_NOT_EXPLICIT"
            ):

                raise AnalyticsLoadError(
                    "Unexpected unresolved "
                    "claim provider state"
                )

            provider_unknown = True

        payer = (
            claim_payer_rows.get(
                eob_id
            )
        )

        payer_identity = None

        if payer is not None:

            payer_identity = (
                payer.get(
                    "identity_key_sha256"
                )
            )

            if (
                payer_identity
                and payer_identity
                not in payer_identity_set
            ):

                raise AnalyticsLoadError(
                    "Claim payer identity "
                    "missing from dimension"
                )

        claim_context[
            eob_id
        ] = {
            "patient_id":
                patient_id,

            "claim_created_date_key":
                created_date_key,

            "provider_identity_key_sha256":
                provider_identity,

            "provider_is_unknown":
                provider_unknown,

            "payer_identity_key_sha256":
                payer_identity,
        }

        bundle[
            "fact_claim"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                patient_id,

            "claim_created_date_key":
                created_date_key,

            "billable_start_date_key":
                date_key(
                    billable_start
                ),

            "billable_end_date_key":
                date_key(
                    billable_end
                ),

            "claim_type_system_uri":
                row.get(
                    "claim_type_system"
                ),

            "claim_type_code":
                row.get(
                    "claim_type_code"
                ),

            "provider_identity_key_sha256":
                provider_identity,

            "provider_is_unknown":
                provider_unknown,

            "payer_identity_key_sha256":
                payer_identity,

            "eob_id":
                eob_id,

            "claim_status":
                row.get(
                    "status"
                ),

            "claim_use":
                row.get(
                    "use"
                ),

            "claim_outcome":
                row.get(
                    "outcome"
                ),

            "claim_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Currency discovery.
    # ------------------------------------------------------

    currencies = set()

    for entity in (
        "stg_eob_total",
        "stg_eob_adjudication",
        "stg_eob_item_adjudication",
    ):

        for row in staging[
            entity
        ]:

            currency = row.get(
                "currency"
            )

            if currency:
                currencies.add(
                    currency
                )

    bundle[
        "dim_currency"
    ] = [
        {
            "currency_code":
                currency,

            "currency_name":
                None,
        }
        for currency in sorted(
            currencies
        )
    ]

    # ------------------------------------------------------
    # Child fact helper.
    # ------------------------------------------------------

    def context_for(row):

        eob_id = row.get(
            "eob_id"
        )

        context = (
            claim_context.get(
                eob_id
            )
        )

        if context is None:

            raise AnalyticsLoadError(
                f"Missing parent claim context: {eob_id}"
            )

        return (
            eob_id,
            context,
        )

    # ------------------------------------------------------
    # Fact Item.
    # ------------------------------------------------------

    for row in staging[
        "stg_eob_item"
    ]:

        eob_id, context = (
            context_for(row)
        )

        fragment = parse_fragment(
            row
        )

        serviced_date = (
            row.get(
                "serviced_date"
            )
            or fragment.get(
                "servicedDate"
            )
        )

        if serviced_date:
            analytical_dates.append(
                serviced_date
            )

        quantity_value, quantity_unit = (
            quantity_parts(
                row.get(
                    "quantity_json"
                )
                or fragment.get(
                    "quantity"
                )
            )
        )

        bundle[
            "fact_item"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "serviced_date_key":
                date_key(
                    serviced_date
                ),

            "service_system_uri":
                row.get(
                    "product_service_system"
                ),

            "service_code":
                row.get(
                    "product_service_code"
                ),

            "eob_id":
                eob_id,

            "item_sequence":
                row.get(
                    "item_sequence"
                ),

            "quantity_value":
                quantity_value,

            "quantity_unit":
                quantity_unit,

            "item_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Financial facts.
    # ------------------------------------------------------

    financial_sources = (
        (
            "fact_claim_total",
            "stg_eob_total",
            "CLAIM_TOTAL",
        ),
        (
            "fact_claim_adjudication",
            "stg_eob_adjudication",
            "CLAIM_ADJUDICATION",
        ),
        (
            "fact_item_adjudication",
            "stg_eob_item_adjudication",
            "ITEM_ADJUDICATION",
        ),
    )

    for (
        target,
        source,
        domain,
    ) in financial_sources:

        for row in staging[
            source
        ]:

            eob_id, context = (
                context_for(row)
            )

            system = row.get(
                "category_system"
            )

            code = row.get(
                "category_code"
            )

            concept = (
                financial_lookup.get(
                    (
                        domain,
                        system,
                        code,
                    )
                )
            )

            if concept is None:

                raise AnalyticsLoadError(
                    "Financial fact does not "
                    "resolve to authoritative mapping"
                )

            (
                concept_system,
                concept_code,
                authority_version,
            ) = concept

            fact = {
                "pipeline_run_id":
                    pipeline_run_id,

                "patient_source_system":
                    source_system,

                "patient_id":
                    context[
                        "patient_id"
                    ],

                "claim_created_date_key":
                    context[
                        "claim_created_date_key"
                    ],

                "financial_system_uri":
                    concept_system,

                "financial_code":
                    concept_code,

                "financial_authority_version":
                    authority_version,

                "currency_code":
                    row.get(
                        "currency"
                    ),

                "eob_id":
                    eob_id,

                "source_ordinal":
                    row.get(
                        "source_ordinal"
                    ),

                "amount":
                    row.get(
                        "amount"
                    ),

                "source_record_hash":
                    row[
                        "raw_record_hash"
                    ],
            }

            if (
                target
                ==
                "fact_claim_adjudication"
            ):

                fact[
                    "value"
                ] = row.get(
                    "value"
                )

            if (
                target
                ==
                "fact_item_adjudication"
            ):

                fact[
                    "item_sequence"
                ] = row.get(
                    "item_sequence"
                )

            bundle[
                target
            ].append(
                fact
            )

    # ------------------------------------------------------
    # Diagnosis.
    # ------------------------------------------------------

    for row in staging[
        "stg_eob_diagnosis"
    ]:

        eob_id, context = (
            context_for(row)
        )

        bundle[
            "fact_diagnosis_occurrence"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "diagnosis_system_uri":
                row.get(
                    "diagnosis_system"
                ),

            "diagnosis_code":
                row.get(
                    "diagnosis_code"
                ),

            "eob_id":
                eob_id,

            "diagnosis_sequence":
                row.get(
                    "diagnosis_sequence"
                ),

            "diagnosis_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Procedure.
    # ------------------------------------------------------

    for row in staging[
        "stg_eob_procedure"
    ]:

        eob_id, context = (
            context_for(row)
        )

        fragment = parse_fragment(
            row
        )

        procedure_date = (
            row.get(
                "procedure_date"
            )
            or fragment.get(
                "date"
            )
        )

        if procedure_date:
            analytical_dates.append(
                procedure_date
            )

        bundle[
            "fact_procedure_occurrence"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "procedure_date_key":
                date_key(
                    procedure_date
                ),

            "procedure_system_uri":
                row.get(
                    "procedure_system"
                ),

            "procedure_code":
                row.get(
                    "procedure_code"
                ),

            "eob_id":
                eob_id,

            "procedure_sequence":
                row.get(
                    "procedure_sequence"
                ),

            "procedure_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Care team.
    # ------------------------------------------------------

    care_provider_rows = {
        (
            row[
                "parent_resource_id"
            ],
            row.get(
                "parent_sequence"
            ),
        ):
            row
        for row in references[
            "provider_reference"
        ]
        if row.get(
            "source_context"
        )
        == "CARE_TEAM_PROVIDER"
    }

    for row in staging[
        "stg_eob_care_team"
    ]:

        eob_id, context = (
            context_for(row)
        )

        sequence = row.get(
            "careteam_sequence"
        )

        provider = (
            care_provider_rows.get(
                (
                    eob_id,
                    sequence,
                )
            )
        )

        if provider is None:

            raise AnalyticsLoadError(
                "Care-team provider occurrence "
                "does not resolve"
            )

        identity = provider.get(
            "identity_key_sha256"
        )

        if (
            not identity
            or identity
            not in provider_identity_set
        ):

            raise AnalyticsLoadError(
                "Care-team provider identity "
                "is not load-ready"
            )

        bundle[
            "fact_care_team_occurrence"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "provider_identity_key_sha256":
                identity,

            "provider_is_unknown":
                False,

            "eob_id":
                eob_id,

            "careteam_sequence":
                sequence,

            "role_json":
                row.get(
                    "role_json"
                ),

            "qualification_json":
                row.get(
                    "qualification_json"
                ),

            "care_team_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Supporting information.
    # ------------------------------------------------------

    for row in staging[
        "stg_eob_supporting_info"
    ]:

        eob_id, context = (
            context_for(row)
        )

        timing_date = (
            row.get(
                "timing_date"
            )
        )

        if timing_date:
            analytical_dates.append(
                timing_date
            )

        bundle[
            "fact_supporting_info_occurrence"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "timing_date_key":
                date_key(
                    timing_date
                ),

            "supporting_info_system_uri":
                row.get(
                    "category_system"
                ),

            "supporting_info_code":
                row.get(
                    "category_code"
                ),

            "eob_id":
                eob_id,

            "supporting_info_sequence":
                row.get(
                    "supporting_info_sequence"
                ),

            "value_string":
                row.get(
                    "value_string"
                ),

            "code_json":
                row.get(
                    "code_json"
                ),

            "value_quantity_json":
                row.get(
                    "value_quantity_json"
                ),

            "supporting_info_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Item details.
    # ------------------------------------------------------

    for row in staging[
        "stg_eob_item_detail"
    ]:

        eob_id, context = (
            context_for(row)
        )

        fragment = parse_fragment(
            row
        )

        quantity_value, quantity_unit = (
            quantity_parts(
                row.get(
                    "quantity_json"
                )
                or fragment.get(
                    "quantity"
                )
            )
        )

        bundle[
            "fact_item_detail"
        ].append({
            "pipeline_run_id":
                pipeline_run_id,

            "patient_source_system":
                source_system,

            "patient_id":
                context[
                    "patient_id"
                ],

            "claim_created_date_key":
                context[
                    "claim_created_date_key"
                ],

            "service_system_uri":
                row.get(
                    "product_service_system"
                ),

            "service_code":
                row.get(
                    "product_service_code"
                ),

            "eob_id":
                eob_id,

            "item_sequence":
                row.get(
                    "item_sequence"
                ),

            "detail_sequence":
                row.get(
                    "detail_sequence"
                ),

            "quantity_value":
                quantity_value,

            "quantity_unit":
                quantity_unit,

            "item_detail_row_count":
                1,

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Bridge Claim Coverage.
    # Association is ready even when Coverage identity is not.
    # ------------------------------------------------------

    for row in references[
        "bridge_claim_coverage"
    ]:

        eob_id = row.get(
            "eob_id"
        )

        if eob_id not in claim_context:

            raise AnalyticsLoadError(
                "Coverage bridge references "
                "unknown claim"
            )

        coverage_id = None

        if row.get(
            "coverage_identity_key_sha256"
        ):

            if (
                row.get(
                    "coverage_target_resource_type"
                )
                != "Coverage"
            ):

                raise AnalyticsLoadError(
                    "Resolved coverage reference "
                    "has unexpected target type"
                )

            candidate = row.get(
                "coverage_target_id"
            )

            if candidate not in coverage_ids:

                raise AnalyticsLoadError(
                    "Resolved coverage reference "
                    "does not match governed Coverage"
                )

            coverage_id = candidate

        bundle[
            "bridge_claim_coverage"
        ].append({
            "association_key_sha256":
                row[
                    "association_key_sha256"
                ],

            "pipeline_run_id":
                pipeline_run_id,

            "eob_id":
                eob_id,

            "coverage_source_system":
                (
                    source_system
                    if coverage_id
                    else None
                ),

            "coverage_id":
                coverage_id,

            "insurance_ordinal":
                row[
                    "insurance_ordinal"
                ],

            "focal":
                row.get(
                    "focal"
                ),

            "coverage_reference_form":
                row[
                    "coverage_reference_form"
                ],

            "coverage_resolution_status":
                row[
                    "coverage_resolution_status"
                ],

            "coverage_display":
                row.get(
                    "coverage_display"
                ),

            "source_record_hash":
                row[
                    "raw_record_hash"
                ],
        })

    # ------------------------------------------------------
    # Date dimension after every role has been discovered.
    # ------------------------------------------------------

    bundle[
        "dim_date"
    ] = build_date_rows(
        analytical_dates
    )

    # ------------------------------------------------------
    # Integrity checks.
    # ------------------------------------------------------

    unknown_providers = [
        row
        for row in bundle[
            "dim_provider"
        ]
        if row[
            "is_unknown"
        ]
    ]

    if len(
        unknown_providers
    ) != 1:

        raise AnalyticsLoadError(
            "Exactly one governed Unknown "
            "Provider member is required"
        )

    expected_financial_concepts = {
        (
            row["system_uri"],
            row["code"],
            row["authority_version"],
        )
        for row in financial_mapping_rows
    }

    if not expected_financial_concepts:

        raise AnalyticsLoadError(
            "Authoritative financial mapping "
            "contains no concepts"
        )

    if len(
        financial_dim
    ) != len(
        expected_financial_concepts
    ):

        raise AnalyticsLoadError(
            "Financial concept dimension does not "
            "match authoritative mapping artifact"
        )

    return bundle
