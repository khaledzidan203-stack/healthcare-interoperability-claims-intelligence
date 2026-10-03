from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import re


ENTITIES = (
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
)


class TransformError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _hash(value: Any) -> str:
    return sha256(
        _json(value).encode("utf-8")
    ).hexdigest().upper()


def _coding(value: Any) -> dict[str, Any]:

    if not isinstance(value, dict):
        return {}

    codings = value.get("coding")

    if (
        not isinstance(codings, list)
        or not codings
        or not isinstance(codings[0], dict)
    ):
        return {}

    first = codings[0]

    return {
        "code": first.get("code"),
        "system": first.get("system"),
        "display": first.get("display"),
    }


def _page_number(name: str) -> int | None:

    match = re.search(
        r"_page_(\d+)\.json$",
        name,
        re.IGNORECASE,
    )

    return int(match.group(1)) if match else None


def _resource_id(resource: dict[str, Any]) -> str:

    value = resource.get("id")

    if not isinstance(value, str) or not value.strip():

        raise TransformError(
            f"{resource.get('resourceType', 'Unknown')} "
            "resource is missing FHIR id"
        )

    return value


def _sequence(
    element: dict[str, Any],
    label: str,
    eob_id: str,
) -> int:

    value = element.get("sequence")

    if not isinstance(value, int):

        raise TransformError(
            f"{label} in EOB {eob_id} "
            "is missing integer sequence"
        )

    return value


def _validate_sequences(
    elements: list[Any],
    label: str,
    eob_id: str,
) -> None:

    values = []

    for element in elements:

        if not isinstance(element, dict):

            raise TransformError(
                f"{label} in EOB {eob_id} is not an object"
            )

        values.append(
            _sequence(
                element,
                label,
                eob_id,
            )
        )

    if len(values) != len(set(values)):

        raise TransformError(
            f"Duplicate {label} sequence in EOB {eob_id}"
        )


def _base(
    *,
    run_id: str,
    source_file: str,
    resource_type: str,
    resource_id: str,
    fragment: dict[str, Any],
    parent_resource_id: str | None = None,
    source_sequence: int | None = None,
    source_ordinal: int | None = None,
) -> dict[str, Any]:

    return {
        "pipeline_run_id": run_id,
        "source_file": source_file,
        "source_page_number": _page_number(source_file),
        "source_resource_type": resource_type,
        "source_resource_id": resource_id,
        "parent_resource_id": parent_resource_id,
        "source_sequence": source_sequence,
        "source_ordinal": source_ordinal,
        "raw_record_hash": _hash(fragment),
        "source_fragment_json": _json(fragment),
    }


def empty_rows():

    return {
        name: []
        for name in ENTITIES
    }


def transform_resource(
    resource: dict[str, Any],
    *,
    run_id: str,
    source_file: str,
):

    rows = empty_rows()

    resource_type = resource.get("resourceType")
    resource_id = _resource_id(resource)

    # ----------------------------------------------------------
    # Patient
    # ----------------------------------------------------------

    if resource_type == "Patient":

        rows["stg_patient"].append({
            **_base(
                run_id=run_id,
                source_file=source_file,
                resource_type="Patient",
                resource_id=resource_id,
                fragment=resource,
            ),
            "patient_id": resource_id,
            "birth_date": resource.get("birthDate"),
            "gender": resource.get("gender"),
            "identifiers_json": _json(resource.get("identifier", [])),
            "address_json": _json(resource.get("address", [])),
            "communication_json": _json(resource.get("communication", [])),
            "profiles_json": _json(
                (resource.get("meta") or {}).get("profile", [])
            ),
        })

        return rows

    # ----------------------------------------------------------
    # Coverage
    # ----------------------------------------------------------

    if resource_type == "Coverage":

        beneficiary = resource.get("beneficiary")

        rows["stg_coverage"].append({
            **_base(
                run_id=run_id,
                source_file=source_file,
                resource_type="Coverage",
                resource_id=resource_id,
                fragment=resource,
            ),
            "coverage_id": resource_id,
            "status": resource.get("status"),
            "subscriber_id": resource.get("subscriberId"),
            "beneficiary_reference": (
                beneficiary.get("reference")
                if isinstance(beneficiary, dict)
                else None
            ),
            "relationship_json": _json(resource.get("relationship")),
            "period_start": (
                (resource.get("period") or {}).get("start")
            ),
            "period_end": (
                (resource.get("period") or {}).get("end")
            ),
            "coverage_type_json": _json(resource.get("type")),
            "payor_json": _json(resource.get("payor", [])),
            "class_json": _json(resource.get("class", [])),
        })

        return rows

    # ----------------------------------------------------------
    # ExplanationOfBenefit
    # ----------------------------------------------------------

    if resource_type != "ExplanationOfBenefit":

        raise TransformError(
            f"Unexpected resourceType: {resource_type}"
        )

    eob_id = resource_id
    patient = resource.get("patient")
    claim_type = _coding(resource.get("type"))

    rows["stg_eob_claim"].append({
        **_base(
            run_id=run_id,
            source_file=source_file,
            resource_type="ExplanationOfBenefit",
            resource_id=eob_id,
            fragment=resource,
        ),
        "eob_id": eob_id,
        "patient_reference": (
            patient.get("reference")
            if isinstance(patient, dict)
            else None
        ),
        "status": resource.get("status"),
        "use": resource.get("use"),
        "outcome": resource.get("outcome"),
        "claim_type_code": claim_type.get("code"),
        "claim_type_system": claim_type.get("system"),
        "created": resource.get("created"),
        "subtype_json": _json(resource.get("subType")),
        "billable_period_start": (
            (resource.get("billablePeriod") or {}).get("start")
        ),
        "billable_period_end": (
            (resource.get("billablePeriod") or {}).get("end")
        ),
        "provider_reference": (
            (resource.get("provider") or {}).get("reference")
            if isinstance(resource.get("provider"), dict)
            else None
        ),
        "insurer_reference": (
            (resource.get("insurer") or {}).get("reference")
            if isinstance(resource.get("insurer"), dict)
            else None
        ),
        "insurance_json": _json(resource.get("insurance", [])),
        "payment_json": _json(resource.get("payment")),
        "profiles_json": _json(
            (resource.get("meta") or {}).get("profile", [])
        ),
        "meta_source": (
            (resource.get("meta") or {}).get("source")
        ),
    })

    # ----------------------------------------------------------
    # Validate sequence-bearing children
    # ----------------------------------------------------------

    for name in (
        "item",
        "diagnosis",
        "procedure",
        "careTeam",
        "supportingInfo",
    ):

        _validate_sequences(
            resource.get(name, []) or [],
            name,
            eob_id,
        )

    # ----------------------------------------------------------
    # Items
    # ----------------------------------------------------------

    for ordinal, item in enumerate(
        resource.get("item", []) or [],
        start=1,
    ):

        item_sequence = item["sequence"]
        product = _coding(
            item.get("productOrService")
        )

        rows["stg_eob_item"].append({
            **_base(
                run_id=run_id,
                source_file=source_file,
                resource_type="ExplanationOfBenefit",
                resource_id=eob_id,
                parent_resource_id=eob_id,
                source_sequence=item_sequence,
                source_ordinal=ordinal,
                fragment=item,
            ),
            "eob_id": eob_id,
            "item_sequence": item_sequence,
            "product_service_code": product.get("code"),
            "product_service_system": product.get("system"),
            "quantity_json": _json(item.get("quantity")),
            "serviced_date": item.get("servicedDate"),
            "serviced_period_json": _json(item.get("servicedPeriod")),
            "location_json": _json(item.get("locationCodeableConcept")),
            "revenue_json": _json(item.get("revenue")),
            "modifier_json": _json(item.get("modifier", [])),
        })

        # Item adjudication

        for adj_ordinal, adj in enumerate(
            item.get("adjudication", []) or [],
            start=1,
        ):

            amount = (
                adj.get("amount")
                if isinstance(adj.get("amount"), dict)
                else {}
            )

            category = _coding(
                adj.get("category")
            )

            rows[
                "stg_eob_item_adjudication"
            ].append({
                **_base(
                    run_id=run_id,
                    source_file=source_file,
                    resource_type="ExplanationOfBenefit",
                    resource_id=eob_id,
                    parent_resource_id=eob_id,
                    source_sequence=item_sequence,
                    source_ordinal=adj_ordinal,
                    fragment=adj,
                ),
                "eob_id": eob_id,
                "item_sequence": item_sequence,
                "category_code": category.get("code"),
                "category_system": category.get("system"),
                "amount": amount.get("value"),
                "currency": amount.get("currency"),
                "reason_json": _json(adj.get("reason")),
            })

        # Item detail

        details = item.get("detail", []) or []

        _validate_sequences(
            details,
            f"item[{item_sequence}].detail",
            eob_id,
        )

        for detail_ordinal, detail in enumerate(
            details,
            start=1,
        ):

            detail_sequence = detail["sequence"]

            product = _coding(
                detail.get("productOrService")
            )

            rows[
                "stg_eob_item_detail"
            ].append({
                **_base(
                    run_id=run_id,
                    source_file=source_file,
                    resource_type="ExplanationOfBenefit",
                    resource_id=eob_id,
                    parent_resource_id=eob_id,
                    source_sequence=detail_sequence,
                    source_ordinal=detail_ordinal,
                    fragment=detail,
                ),
                "eob_id": eob_id,
                "item_sequence": item_sequence,
                "detail_sequence": detail_sequence,
                "product_service_code": product.get("code"),
                "product_service_system": product.get("system"),
                "quantity_json": _json(detail.get("quantity")),
            })

    # ----------------------------------------------------------
    # Diagnosis / Procedure / CareTeam / SupportingInfo
    # ----------------------------------------------------------

    simple_children = (
        (
            "diagnosis",
            "stg_eob_diagnosis",
            "diagnosis_sequence",
        ),
        (
            "procedure",
            "stg_eob_procedure",
            "procedure_sequence",
        ),
        (
            "careTeam",
            "stg_eob_care_team",
            "careteam_sequence",
        ),
        (
            "supportingInfo",
            "stg_eob_supporting_info",
            "supporting_info_sequence",
        ),
    )

    for source_name, target_name, key_name in simple_children:

        elements = resource.get(source_name, []) or []

        for ordinal, element in enumerate(
            elements,
            start=1,
        ):

            sequence = element["sequence"]

            row = {
                **_base(
                    run_id=run_id,
                    source_file=source_file,
                    resource_type="ExplanationOfBenefit",
                    resource_id=eob_id,
                    parent_resource_id=eob_id,
                    source_sequence=sequence,
                    source_ordinal=ordinal,
                    fragment=element,
                ),
                "eob_id": eob_id,
                key_name: sequence,
            }

            if source_name == "diagnosis":

                code = _coding(
                    element.get(
                        "diagnosisCodeableConcept"
                    )
                )

                row["diagnosis_code"] = code.get("code")
                row["diagnosis_system"] = code.get("system")
                row["diagnosis_type_json"] = _json(
                    element.get("type", [])
                )
                row["on_admission_json"] = _json(
                    element.get("onAdmission")
                )

            elif source_name == "procedure":

                code = _coding(
                    element.get(
                        "procedureCodeableConcept"
                    )
                )

                row["procedure_code"] = code.get("code")
                row["procedure_system"] = code.get("system")
                row["procedure_date"] = element.get("date")
                row["procedure_type_json"] = _json(
                    element.get("type", [])
                )

            elif source_name == "careTeam":

                provider = element.get("provider")

                identifier = (
                    provider.get("identifier")
                    if isinstance(provider, dict)
                    and isinstance(
                        provider.get("identifier"),
                        dict,
                    )
                    else {}
                )

                row["provider_identifier"] = (
                    identifier.get("value")
                )

                row["provider_identifier_system"] = (
                    identifier.get("system")
                )
                row["provider_display"] = (
                    provider.get("display")
                    if isinstance(provider, dict)
                    else None
                )
                row["provider_type"] = (
                    provider.get("type")
                    if isinstance(provider, dict)
                    else None
                )
                row["role_json"] = _json(element.get("role"))
                row["qualification_json"] = _json(
                    element.get("qualification")
                )

            elif source_name == "supportingInfo":

                category = _coding(
                    element.get("category")
                )

                row["category_code"] = category.get("code")
                row["category_system"] = category.get("system")
                row["code_json"] = _json(element.get("code"))
                row["timing_date"] = element.get("timingDate")
                row["timing_period_json"] = _json(
                    element.get("timingPeriod")
                )
                row["value_quantity_json"] = _json(
                    element.get("valueQuantity")
                )
                row["value_string"] = element.get("valueString")

            rows[target_name].append(row)

    # ----------------------------------------------------------
    # Claim-level adjudication
    # ----------------------------------------------------------

    for ordinal, adj in enumerate(
        resource.get("adjudication", []) or [],
        start=1,
    ):

        amount = (
            adj.get("amount")
            if isinstance(adj.get("amount"), dict)
            else {}
        )

        category = _coding(
            adj.get("category")
        )

        rows["stg_eob_adjudication"].append({
            **_base(
                run_id=run_id,
                source_file=source_file,
                resource_type="ExplanationOfBenefit",
                resource_id=eob_id,
                parent_resource_id=eob_id,
                source_ordinal=ordinal,
                fragment=adj,
            ),
            "eob_id": eob_id,
            "category_code": category.get("code"),
            "category_system": category.get("system"),
            "amount": amount.get("value"),
            "currency": amount.get("currency"),
            "value": adj.get("value"),
            "reason_json": _json(adj.get("reason")),
        })

    # ----------------------------------------------------------
    # Claim totals
    # ----------------------------------------------------------

    for ordinal, total in enumerate(
        resource.get("total", []) or [],
        start=1,
    ):

        amount = (
            total.get("amount")
            if isinstance(total.get("amount"), dict)
            else {}
        )

        category = _coding(
            total.get("category")
        )

        rows["stg_eob_total"].append({
            **_base(
                run_id=run_id,
                source_file=source_file,
                resource_type="ExplanationOfBenefit",
                resource_id=eob_id,
                parent_resource_id=eob_id,
                source_ordinal=ordinal,
                fragment=total,
            ),
            "eob_id": eob_id,
            "category_code": category.get("code"),
            "category_system": category.get("system"),
            "amount": amount.get("value"),
            "currency": amount.get("currency"),
        })

    return rows


def transform_run(run_dir: Path):

    run_dir = Path(run_dir)

    if not run_dir.is_dir():

        raise TransformError(
            f"RAW run directory not found: {run_dir}"
        )

    result = empty_rows()

    seen = set()

    for path in sorted(
        run_dir.glob("*_bundle_page_*.json")
    ):

        bundle = json.loads(
            path.read_text(encoding="utf-8")
        )

        if bundle.get("resourceType") != "Bundle":

            raise TransformError(
                f"{path.name} is not a FHIR Bundle"
            )

        for entry in bundle.get("entry", []) or []:

            if not isinstance(entry, dict):
                continue

            resource = entry.get("resource")

            if not isinstance(resource, dict):
                continue

            if resource.get("resourceType") not in {
                "Patient",
                "Coverage",
                "ExplanationOfBenefit",
            }:
                continue

            key = (
                resource["resourceType"],
                _resource_id(resource),
            )

            if key in seen:

                raise TransformError(
                    "Duplicate RAW resource: "
                    f"{key[0]}/{key[1]}"
                )

            seen.add(key)

            part = transform_resource(
                resource,
                run_id=run_dir.name,
                source_file=path.name,
            )

            for entity in ENTITIES:
                result[entity].extend(
                    part[entity]
                )

    return result
