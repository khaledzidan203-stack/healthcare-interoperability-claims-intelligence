# Canonical Grain Contract

> Status: HISTORICAL checkpoint/design evidence. Statements of current state and run-specific counts apply to that checkpoint only. See [current release evidence](../validation/RELEASE_VALIDATION_EVIDENCE.md) and [release architecture](../architecture/RELEASE_ARCHITECTURE.md). Current source takes precedence.

## Project
Healthcare Interoperability & Claims Intelligence Platform

## Status
Checkpoint 2B — Proposed Canonical Grain Contract

## Governing Principle

Every canonical entity must answer:

> One row = exactly one defined business/FHIR entity at one stable grain.

Nested repeating FHIR arrays must not be flattened blindly into the parent row,
because doing so would multiply records and corrupt counts and financial values.

---

## 1. Patient

**Canonical entity:** `Patient`

**One row =** one FHIR Patient resource.

**Source identity:** `Patient.id`

**Candidate canonical key:**

`patient_id`

**Parent:** none.

---

## 2. Coverage

**Canonical entity:** `Coverage`

**One row =** one FHIR Coverage resource.

**Source identity:** `Coverage.id`

**Candidate canonical key:**

`coverage_id`

**Parent relationship:**

`Coverage.beneficiary.reference` → Patient

---

## 3. EOB Claim

**Canonical entity:** `EOB_Claim`

**One row =** one FHIR ExplanationOfBenefit resource.

**Source identity:** `ExplanationOfBenefit.id`

**Candidate canonical key:**

`eob_id`

**Parent relationships:**

- Patient reference
- Coverage reference where available
- Provider / insurer references where supplied

This is the claim/header grain.

---

## 4. EOB Item

**Canonical entity:** `EOB_Item`

**One row =** one `ExplanationOfBenefit.item[]` element.

**Source sequence:** `item.sequence`

**Candidate canonical key:**

`eob_id + item_sequence`

**Parent:**

`EOB_Claim`

Do not aggregate multiple item rows into the claim row during canonicalization.

---

## 5. EOB Diagnosis

**Canonical entity:** `EOB_Diagnosis`

**One row =** one `ExplanationOfBenefit.diagnosis[]` element.

**Source sequence:** `diagnosis.sequence`

**Candidate canonical key:**

`eob_id + diagnosis_sequence`

**Parent:**

`EOB_Claim`

---

## 6. EOB Procedure

**Canonical entity:** `EOB_Procedure`

**One row =** one `ExplanationOfBenefit.procedure[]` element.

**Source sequence:** `procedure.sequence`

**Candidate canonical key:**

`eob_id + procedure_sequence`

**Parent:**

`EOB_Claim`

---

## 7. EOB Care Team

**Canonical entity:** `EOB_CareTeam`

**One row =** one `ExplanationOfBenefit.careTeam[]` element.

**Source sequence:** `careTeam.sequence`

**Candidate canonical key:**

`eob_id + careteam_sequence`

**Parent:**

`EOB_Claim`

---

## 8. EOB Supporting Information

**Canonical entity:** `EOB_SupportingInfo`

**One row =** one `ExplanationOfBenefit.supportingInfo[]` element.

**Source sequence:** `supportingInfo.sequence`

**Candidate canonical key:**

`eob_id + supporting_info_sequence`

**Parent:**

`EOB_Claim`

---

## 9. Claim-Level Adjudication

**Canonical entity:** `EOB_Adjudication`

**One row =** one `ExplanationOfBenefit.adjudication[]` element.

No explicit source sequence was observed in the validated payload.

**Candidate canonical key:**

`eob_id + source_ordinal`

**Parent:**

`EOB_Claim`

`source_ordinal` must preserve original array order and must not be interpreted
as business meaning unless later source evidence supports that interpretation.

---

## 10. Claim Total

**Canonical entity:** `EOB_Total`

**One row =** one `ExplanationOfBenefit.total[]` element.

**Candidate canonical key:**

`eob_id + source_ordinal`

**Parent:**

`EOB_Claim`

Category coding must be retained because different total rows represent
different financial meanings.

---

## 11. Item-Level Adjudication

**Canonical entity:** `EOB_Item_Adjudication`

**One row =** one `item[].adjudication[]` element.

**Candidate canonical key:**

`eob_id + item_sequence + source_ordinal`

**Parent:**

`EOB_Item`

This grain must remain separate from claim-level adjudication.

---

## 12. Item Detail

**Canonical entity:** `EOB_Item_Detail`

**One row =** one `item[].detail[]` element.

**Source sequence:** `detail.sequence`

**Candidate canonical key:**

`eob_id + item_sequence + detail_sequence`

**Parent:**

`EOB_Item`

---

# Secondary Repeating Structures

The live payload also contains repeating structures such as:

- identifiers;
- codings;
- extensions;
- modifiers;
- contained resources;
- diagnosisSequence;
- informationSequence;
- type codings;
- revenue codings.

These are confirmed source structures but are **not yet automatically promoted
to independent canonical tables**.

Checkpoint 2C/2D must decide whether each should become:

1. a normalized child entity;
2. selected canonical columns;
3. a governed reference/mapping structure;
4. retained JSON/source lineage only.

No repeated structure may be discarded silently.

---

# Key Rules

1. Preserve the original FHIR resource ID.
2. Preserve source sequence values where supplied.
3. When FHIR supplies no sequence, preserve deterministic array ordinal.
4. Never use array ordinal as business meaning.
5. Child tables must retain their parent key.
6. Canonicalization must not change the RAW files.
7. No nested one-to-many array may be flattened into a parent table if it
   causes row multiplication.
8. Missing optional structures remain missing; they must not be invented.
9. Source coding system and code must be retained together.
10. Financial values must retain their currency where supplied.

---

# Current Canonical Entity Set

| Entity | Grain |
|---|---|
| Patient | one Patient resource |
| Coverage | one Coverage resource |
| EOB_Claim | one ExplanationOfBenefit resource |
| EOB_Item | one item within one EOB |
| EOB_Diagnosis | one diagnosis within one EOB |
| EOB_Procedure | one procedure within one EOB |
| EOB_CareTeam | one care-team member within one EOB |
| EOB_SupportingInfo | one supportingInfo element within one EOB |
| EOB_Adjudication | one claim-level adjudication element |
| EOB_Total | one claim total element |
| EOB_Item_Adjudication | one adjudication element within one item |
| EOB_Item_Detail | one detail element within one item |

---

# Modeling Boundary

This document defines canonical grain only.

It does **not** yet define:

- SQL tables;
- surrogate keys;
- final warehouse/star schema;
- Power BI relationships;
- KPI formulas;
- analytical measures.

Those decisions require later checkpoints.
