# Release data and semantic dictionary

Status: CURRENT / RELEASE. Derived from current `dimensional_model.py`, SQL DDL and TMDL on 2026-10-03. Grain/key descriptions below are source contract text, not inferred business definitions. TMDL columns and relationship endpoints are transcribed from checked-in source.

## Scope

Physical analytics has 13 dimensions, 10 facts and one Coverage bridge. Semantic scope is 12 dimensions and 10 facts plus the empty disconnected `_Measures` host. `dim_coverage` and `bridge_claim_coverage` remain upstream only.

## Logical grain and key contracts

| Physical table | Source grain | Logical natural key (contract) | Warehouse key |
|---|---|---|---|
| `dim_claim_type` | One claim-type system/code concept | `system_uri + code` | `claim_type_key` |
| `dim_currency` | One currency code | `currency_code` | `currency_key` |
| `dim_date` | One calendar date | `calendar_date` | `date_key` |
| `dim_diagnosis` | One diagnosis coding system/code concept | `system_uri + code` | `diagnosis_key` |
| `dim_financial_concept` | One authoritative financial system/code concept version | `system_uri + code + authority_version` | `financial_concept_key` |
| `dim_patient` | One governed patient dimension version | `source_system + patient_id + dimensional_version` | `patient_key` |
| `dim_payer` | One normalized payer/insurer identity/version | `normalized payer identity` | `payer_key` |
| `dim_pipeline_run` | One governed pipeline run | `pipeline_run_id` | `pipeline_run_key` |
| `dim_procedure` | One procedure coding system/code concept | `system_uri + code` | `procedure_key` |
| `dim_provider` | One normalized provider identity/version | `normalized provider identity` | `provider_key` |
| `dim_service_code` | One service/product coding system/code concept | `system_uri + code` | `service_code_key` |
| `dim_supporting_info_category` | One supporting-information system/code concept | `system_uri + code` | `supporting_info_category_key` |
| `fact_care_team_occurrence` | One care-team participation occurrence attached to one claim | `pipeline_run_id + eob_id + careteam_sequence` | `fact_care_team_occurrence_key` |
| `fact_claim` | One governed FHIR ExplanationOfBenefit claim | `pipeline_run_id + eob_id` | `fact_claim_key` |
| `fact_claim_adjudication` | One claim-level adjudication element at its exact source ordinal | `pipeline_run_id + eob_id + source_ordinal` | `fact_claim_adjudication_key` |
| `fact_claim_total` | One claim-total element at its exact source ordinal | `pipeline_run_id + eob_id + source_ordinal` | `fact_claim_total_key` |
| `fact_diagnosis_occurrence` | One diagnosis occurrence attached to one claim | `pipeline_run_id + eob_id + diagnosis_sequence` | `fact_diagnosis_occurrence_key` |
| `fact_item` | One governed EOB item within one claim | `pipeline_run_id + eob_id + item_sequence` | `fact_item_key` |
| `fact_item_adjudication` | One item-level adjudication element at its exact source ordinal | `pipeline_run_id + eob_id + item_sequence + source_ordinal` | `fact_item_adjudication_key` |
| `fact_item_detail` | One EOB item-detail element within one claim item | `pipeline_run_id + eob_id + item_sequence + detail_sequence` | `fact_item_detail_key` |
| `fact_procedure_occurrence` | One procedure occurrence attached to one claim | `pipeline_run_id + eob_id + procedure_sequence` | `fact_procedure_occurrence_key` |
| `fact_supporting_info_occurrence` | One supporting-information occurrence attached to one claim | `pipeline_run_id + eob_id + supporting_info_sequence` | `fact_supporting_info_occurrence_key` |

## Physical SQL uniqueness constraints

These expressions are extracted separately from current analytics DDL. Logical version/identity descriptions above are not literal SQL column names. Primary keys are the warehouse keys above; the upstream Coverage objects are also listed here. Partial unique indexes are additional constraints in the SQL file.

| Table | UNIQUE columns / expression |
|---|---|
| `dim_date` | `calendar_date` |
| `dim_pipeline_run` | `pipeline_run_id` |
| `dim_patient` | `source_system, patient_id, valid_from_pipeline_run_id` |
| `dim_coverage` | `source_system, coverage_id, valid_from_pipeline_run_id` |
| `dim_financial_concept` | `system_uri, code, authority_version` |
| `dim_currency` | `currency_code` |
| `dim_claim_type` | `system_uri, code` |
| `dim_service_code` | `system_uri, code` |
| `dim_diagnosis` | `system_uri, code` |
| `dim_procedure` | `system_uri, code` |
| `dim_provider` | `identity_key_sha256` |
| `dim_payer` | `identity_key_sha256` |
| `dim_supporting_info_category` | `system_uri, code` |
| `fact_claim` | `pipeline_run_key, eob_id` |
| `fact_item` | `pipeline_run_key, eob_id, item_sequence` |
| `fact_claim_total` | `pipeline_run_key, eob_id, source_ordinal` |
| `fact_claim_adjudication` | `pipeline_run_key, eob_id, source_ordinal` |
| `fact_item_adjudication` | `pipeline_run_key, eob_id, item_sequence, source_ordinal` |
| `fact_diagnosis_occurrence` | `pipeline_run_key, eob_id, diagnosis_sequence` |
| `fact_procedure_occurrence` | `pipeline_run_key, eob_id, procedure_sequence` |
| `fact_care_team_occurrence` | `pipeline_run_key, eob_id, careteam_sequence` |
| `fact_supporting_info_occurrence` | `pipeline_run_key, eob_id, supporting_info_sequence` |
| `fact_item_detail` | `pipeline_run_key, eob_id, item_sequence, detail_sequence` |
| `bridge_claim_coverage` | `pipeline_run_key, fact_claim_key, insurance_ordinal`; `association_key_sha256` |

## Columns in semantic source

Fields below retain original names, types and hidden status. They are not newly approved KPI definitions.

### analytics dim_claim_type

| Column | TMDL type | Hidden |
|---|---|---|
| `claim_type_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 01b7ad1c-77b1-46f8-b217-3c35c68408d7
		summarizeBy: none
		sourceColumn: claim_type_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: 359e2901-c330-46e8-9e81-512498031cc6
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: d2f9ca44-af25-4daa-8aaa-32e08e200b70
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column source_display
		dataType: string
		lineageTag: 856ec7ef-deff-491c-b536-b3afc00b0e2d
		summarizeBy: none
		sourceColumn: source_display

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: 3bbd535d-8e52-44dd-8463-5cdfef4e70e4
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column mapping_status
		dataType: string
		lineageTag: 402f4c46-7436-43cd-813c-aa34478bd9c5
		summarizeBy: none
		sourceColumn: mapping_status

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: 553e5a57-10f3-41b0-a7f5-1df5cb2061fb
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: 8765f452-2ff4-42e5-8be0-9bc6377d57f5
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_claim_type' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_claim_type = Source{[Schema="analytics",Item="dim_claim_type"]}[Data]
				in
				    analytics_dim_claim_type

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_currency

| Column | TMDL type | Hidden |
|---|---|---|
| `currency_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 5ab99a8d-86a1-4d9d-aa3e-fc97a771510a
		summarizeBy: none
		sourceColumn: currency_key

		annotation SummarizationSetBy = Automatic

	column currency_code
		dataType: string
		lineageTag: 8d34dce4-691a-4951-8bb4-bc6eaee40727
		summarizeBy: none
		sourceColumn: currency_code

		annotation SummarizationSetBy = Automatic

	column currency_name
		dataType: string
		lineageTag: 4c06fc1b-0f6b-4023-8b8e-343c960c3729
		summarizeBy: none
		sourceColumn: currency_name

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_currency' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_currency = Source{[Schema="analytics",Item="dim_currency"]}[Data]
				in
				    analytics_dim_currency

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_date

| Column | TMDL type | Hidden |
|---|---|---|
| `date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 75fbb88c-2d72-486b-a7dd-a97be57e174c
		summarizeBy: none
		sourceColumn: date_key

		annotation SummarizationSetBy = Automatic

	column calendar_date
		dataType: dateTime
		isKey
		formatString: Long Date
		lineageTag: e5924deb-f7c2-43b3-9465-1ed774f1dd99
		summarizeBy: none
		sourceColumn: calendar_date

		annotation SummarizationSetBy = Automatic

		annotation UnderlyingDateTimeDataType = Date

	column calendar_year
		dataType: int64
		formatString: 0
		lineageTag: 89a1c2f2-3277-47bf-a599-eace1d222525
		summarizeBy: none
		sourceColumn: calendar_year

		annotation SummarizationSetBy = Automatic

	column calendar_quarter
		dataType: int64
		formatString: 0
		lineageTag: b2726a02-60bc-4543-b959-551a012ec18c
		summarizeBy: none
		sourceColumn: calendar_quarter

		annotation SummarizationSetBy = Automatic

	column month_number
		dataType: int64
		formatString: 0
		lineageTag: 98b5ca2a-a225-4df5-8dfe-7748556d8cd4
		summarizeBy: none
		sourceColumn: month_number

		annotation SummarizationSetBy = Automatic

	column month_name
		dataType: string
		lineageTag: 2b4a054a-1d0d-475f-8c99-954bb8f400f6
		summarizeBy: none
		sourceColumn: month_name

		annotation SummarizationSetBy = Automatic

	column day_of_month
		dataType: int64
		formatString: 0
		lineageTag: c062f154-2baf-40ec-ab3f-26b66de4ebbc
		summarizeBy: none
		sourceColumn: day_of_month

		annotation SummarizationSetBy = Automatic

	column day_of_week
		dataType: int64
		formatString: 0
		lineageTag: 016a226d-efe8-4fc0-8e17-f12b3593325d
		summarizeBy: none
		sourceColumn: day_of_week

		annotation SummarizationSetBy = Automatic

	column day_name
		dataType: string
		lineageTag: 1056e351-9e1e-4abe-9cd6-e41b32c024a5
		summarizeBy: none
		sourceColumn: day_name

		annotation SummarizationSetBy = Automatic

	column is_weekend
		dataType: boolean
		formatString: """TRUE"";""TRUE"";""FALSE"""
		lineageTag: 5e223930-8fc6-40a1-8f7c-dd1f9ab81764
		summarizeBy: none
		sourceColumn: is_weekend

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_date' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_date = Source{[Schema="analytics",Item="dim_date"]}[Data]
				in
				    analytics_dim_date

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_diagnosis

| Column | TMDL type | Hidden |
|---|---|---|
| `diagnosis_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 554b21fe-d8fc-463f-b23c-7f39363b808e
		summarizeBy: none
		sourceColumn: diagnosis_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: 216061ca-2afd-4c88-88f0-112ee08c7ed2
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: 049501e7-1bee-4668-8e14-dd23657b3699
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column source_display
		dataType: string
		lineageTag: f245bbb6-9223-41a0-aa0c-e737100013a7
		summarizeBy: none
		sourceColumn: source_display

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: 97f148ef-2827-4c73-91e6-4cc50b0a2775
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column mapping_status
		dataType: string
		lineageTag: 1e5753d8-9b7d-4a03-9049-4f3c14e29c8d
		summarizeBy: none
		sourceColumn: mapping_status

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: 50c5f13e-2152-400b-ab3e-c792ff79485a
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: 71a2116d-3824-4f23-abc1-2869bfae8052
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_diagnosis' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_diagnosis = Source{[Schema="analytics",Item="dim_diagnosis"]}[Data]
				in
				    analytics_dim_diagnosis

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_financial_concept

| Column | TMDL type | Hidden |
|---|---|---|
| `financial_concept_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 5727c065-baef-4c7e-bcd0-5cddb9c5bb40
		summarizeBy: none
		sourceColumn: financial_concept_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: afb97f55-57e2-4587-97c1-bfe8d585d2b6
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: 455d1cc3-1f12-4a75-8d64-8dcd27b4bf2f
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: e52512e1-aeba-4b22-b36d-625972a70ca8
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: 2c5d13bb-df32-42df-9e0a-3e69b3d18bdd
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column semantic_role
		dataType: string
		lineageTag: 85120786-de71-4c94-8fd1-e471f342ee2b
		summarizeBy: none
		sourceColumn: semantic_role

		annotation SummarizationSetBy = Automatic

	column aggregation_rule
		dataType: string
		lineageTag: a2552c93-1757-4bd3-9e5e-75fa083558e5
		summarizeBy: none
		sourceColumn: aggregation_rule

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: fec7fde7-d22c-4cab-90f3-cb6d3eb4a66a
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_url
		dataType: string
		lineageTag: 3f4ddd85-da31-4f62-947b-8168a3781e67
		summarizeBy: none
		sourceColumn: authority_url

		annotation SummarizationSetBy = Automatic

	column resolution_status
		dataType: string
		lineageTag: 8b3a8511-6072-4709-b502-210584fea999
		summarizeBy: none
		sourceColumn: resolution_status

		annotation SummarizationSetBy = Automatic

	column kpi_status
		dataType: string
		lineageTag: bbd8ad50-d0a2-45e4-a927-b523c692d060
		summarizeBy: none
		sourceColumn: kpi_status

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_financial_concept' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_financial_concept = Source{[Schema="analytics",Item="dim_financial_concept"]}[Data]
				in
				    analytics_dim_financial_concept

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_patient

| Column | TMDL type | Hidden |
|---|---|---|
| `patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: ac16c1d7-86d2-4f4e-ac81-3af6daa96775
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column source_system
		dataType: string
		lineageTag: 67dc4a8e-1a4c-4c6b-860d-2ceb28772793
		summarizeBy: none
		sourceColumn: source_system

		annotation SummarizationSetBy = Automatic

	column patient_id
		dataType: string
		lineageTag: cf854cb6-38ab-4882-acd2-ac9aa9638d61
		summarizeBy: none
		sourceColumn: patient_id

		annotation SummarizationSetBy = Automatic

	column birth_date
		dataType: dateTime
		formatString: Long Date
		lineageTag: 91ecda65-81d3-4931-9eb2-60cc599214d9
		summarizeBy: none
		sourceColumn: birth_date

		annotation SummarizationSetBy = Automatic

		annotation UnderlyingDateTimeDataType = Date

	column gender
		dataType: string
		lineageTag: bf1b7d6e-c862-4872-bc2f-2067b84f07f5
		summarizeBy: none
		sourceColumn: gender

		annotation SummarizationSetBy = Automatic

	column valid_from_pipeline_run_id
		dataType: string
		lineageTag: 83ef859a-265f-472c-8739-30103004fb4d
		summarizeBy: none
		sourceColumn: valid_from_pipeline_run_id

		annotation SummarizationSetBy = Automatic

	column valid_to_pipeline_run_id
		dataType: string
		lineageTag: d14c6eee-7e7c-4551-ac2f-78a2f05319a6
		summarizeBy: none
		sourceColumn: valid_to_pipeline_run_id

		annotation SummarizationSetBy = Automatic

	column is_current
		dataType: boolean
		isHidden
		formatString: """TRUE"";""TRUE"";""FALSE"""
		lineageTag: 5d455356-f1c2-4ed7-aedc-b27f3f4b111d
		summarizeBy: none
		sourceColumn: is_current

		annotation SummarizationSetBy = Automatic

	column row_hash
		dataType: string
		isHidden
		lineageTag: ad299a80-3356-4f59-86ce-ad4ea7fa94b8
		summarizeBy: none
		sourceColumn: row_hash

		annotation SummarizationSetBy = Automatic

	column attributes_json
		dataType: string
		lineageTag: db45a5ba-5b75-4aca-aefb-8c5a0c66018b
		summarizeBy: none
		sourceColumn: attributes_json

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_patient' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_patient = Source{[Schema="analytics",Item="dim_patient"]}[Data]
				in
				    analytics_dim_patient

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_payer

| Column | TMDL type | Hidden |
|---|---|---|
| `payer_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 3fe8b8f6-9c2b-47f1-833e-b2c18c146aa9
		summarizeBy: none
		sourceColumn: payer_key

		annotation SummarizationSetBy = Automatic

	column identity_key_sha256
		dataType: string
		isHidden
		lineageTag: adea5283-aa70-48a4-ac03-d39a439a228f
		summarizeBy: none
		sourceColumn: identity_key_sha256

		annotation SummarizationSetBy = Automatic

	column identity_status
		dataType: string
		lineageTag: c5134e38-532d-4471-8294-947cb60a9905
		summarizeBy: none
		sourceColumn: identity_status

		annotation SummarizationSetBy = Automatic

	column target_resource_type
		dataType: string
		lineageTag: 4389e319-193e-45fe-8131-43e50cbe3d95
		summarizeBy: none
		sourceColumn: target_resource_type

		annotation SummarizationSetBy = Automatic

	column identifier_system
		dataType: string
		lineageTag: 883b9695-f3f7-433d-b13b-8ad8a3cb05eb
		summarizeBy: none
		sourceColumn: identifier_system

		annotation SummarizationSetBy = Automatic

	column identifier_value
		dataType: string
		lineageTag: 242753e3-7e01-4eb4-9bdc-83d786f98f8f
		summarizeBy: none
		sourceColumn: identifier_value

		annotation SummarizationSetBy = Automatic

	column display
		dataType: string
		lineageTag: 2f56d591-bc54-43a4-90cf-c489cbc5cee6
		summarizeBy: none
		sourceColumn: display

		annotation SummarizationSetBy = Automatic

	column is_unknown
		dataType: boolean
		formatString: """TRUE"";""TRUE"";""FALSE"""
		lineageTag: 42f2c62d-2ad0-47f1-b285-6fa6fb746f33
		summarizeBy: none
		sourceColumn: is_unknown

		annotation SummarizationSetBy = Automatic

	column attributes_json
		dataType: string
		lineageTag: b2ccd120-9493-4431-99fb-9dcb991932ca
		summarizeBy: none
		sourceColumn: attributes_json

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_payer' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_payer = Source{[Schema="analytics",Item="dim_payer"]}[Data]
				in
				    analytics_dim_payer

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_pipeline_run

| Column | TMDL type | Hidden |
|---|---|---|
| `pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 49a03579-1658-437e-b0b2-44c7decb4ecb
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_id
		dataType: string
		isHidden
		lineageTag: d9ba6adf-55a5-433f-aaf5-25576aec84da
		summarizeBy: none
		sourceColumn: pipeline_run_id

		annotation SummarizationSetBy = Automatic

	column run_status
		dataType: string
		lineageTag: 48aa7de8-9706-42e4-a119-df1ea7bc2e8f
		summarizeBy: none
		sourceColumn: run_status

		annotation SummarizationSetBy = Automatic

	column raw_manifest_sha256
		dataType: string
		isHidden
		lineageTag: 984532f4-0bf3-410f-8854-9fd222111d21
		summarizeBy: none
		sourceColumn: raw_manifest_sha256

		annotation SummarizationSetBy = Automatic

	column staging_manifest_sha256
		dataType: string
		isHidden
		lineageTag: 49395a40-7988-4a31-80a5-f47fe450af4b
		summarizeBy: none
		sourceColumn: staging_manifest_sha256

		annotation SummarizationSetBy = Automatic

	column loaded_at
		dataType: dateTime
		formatString: General Date
		lineageTag: 3982d426-f77a-4073-99b4-ec524b4fd5f2
		summarizeBy: none
		sourceColumn: loaded_at

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_pipeline_run' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_pipeline_run = Source{[Schema="analytics",Item="dim_pipeline_run"]}[Data]
				in
				    analytics_dim_pipeline_run

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_procedure

| Column | TMDL type | Hidden |
|---|---|---|
| `procedure_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 66879a96-454f-4c7d-b68a-3a11a54c91b8
		summarizeBy: none
		sourceColumn: procedure_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: e8869c98-58f1-42d2-9721-10dd6ccd18e2
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: 88aede8e-5cc9-469a-a220-b8a52b5373d7
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column source_display
		dataType: string
		lineageTag: 4239d25f-04b3-4519-92fc-9418a886f429
		summarizeBy: none
		sourceColumn: source_display

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: 3210b170-1ea3-41d7-b4e2-7f912cbcdbef
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column mapping_status
		dataType: string
		lineageTag: 7b6d49fe-177b-4ba5-bcdd-d0f9ae5461d8
		summarizeBy: none
		sourceColumn: mapping_status

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: d5664d5a-4db5-42da-b949-707d58a4ef92
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: 3ec75465-9414-4158-b45f-3dccdf99bf83
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_procedure' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_procedure = Source{[Schema="analytics",Item="dim_procedure"]}[Data]
				in
				    analytics_dim_procedure

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_provider

| Column | TMDL type | Hidden |
|---|---|---|
| `provider_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 91c62270-4a3a-458e-84dc-7c96df309a17
		summarizeBy: none
		sourceColumn: provider_key

		annotation SummarizationSetBy = Automatic

	column identity_key_sha256
		dataType: string
		isHidden
		lineageTag: e40f9a73-a552-4862-893a-4c64cd561004
		summarizeBy: none
		sourceColumn: identity_key_sha256

		annotation SummarizationSetBy = Automatic

	column identity_status
		dataType: string
		lineageTag: 335e0e61-df34-44e3-902d-8188b6f87fc5
		summarizeBy: none
		sourceColumn: identity_status

		annotation SummarizationSetBy = Automatic

	column target_resource_type
		dataType: string
		lineageTag: ac01ee43-cc9e-4f95-8bba-1e33b0c2e58a
		summarizeBy: none
		sourceColumn: target_resource_type

		annotation SummarizationSetBy = Automatic

	column identifier_system
		dataType: string
		lineageTag: 5f6161e8-bd5f-4780-bb84-094c6aab8d65
		summarizeBy: none
		sourceColumn: identifier_system

		annotation SummarizationSetBy = Automatic

	column identifier_value
		dataType: string
		lineageTag: 0b7456fc-98ca-4bb7-8571-c3f542ac6dc6
		summarizeBy: none
		sourceColumn: identifier_value

		annotation SummarizationSetBy = Automatic

	column display
		dataType: string
		lineageTag: 4a16ac5e-b18a-4c89-8a1c-a8351c9692e8
		summarizeBy: none
		sourceColumn: display

		annotation SummarizationSetBy = Automatic

	column is_unknown
		dataType: boolean
		formatString: """TRUE"";""TRUE"";""FALSE"""
		lineageTag: 93a80749-4124-42cb-a3e2-d986863f6747
		summarizeBy: none
		sourceColumn: is_unknown

		annotation SummarizationSetBy = Automatic

	column attributes_json
		dataType: string
		lineageTag: 985dd7e1-5ebf-4b98-a156-1a8b5eae44d3
		summarizeBy: none
		sourceColumn: attributes_json

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_provider' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_provider = Source{[Schema="analytics",Item="dim_provider"]}[Data]
				in
				    analytics_dim_provider

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_service_code

| Column | TMDL type | Hidden |
|---|---|---|
| `service_code_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 287644f9-b549-412a-98c0-857888c1660d
		summarizeBy: none
		sourceColumn: service_code_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: d7cb1805-ed59-441f-bf1d-0526f54be17e
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: c87c57ca-275a-47c9-be8f-3c34a24f371f
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column source_display
		dataType: string
		lineageTag: af493d8c-7059-4f6b-95a1-25b6ab799277
		summarizeBy: none
		sourceColumn: source_display

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: c40793cd-bbd3-4320-9849-a581ac00d9a2
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column mapping_status
		dataType: string
		lineageTag: 3bd21185-3ecc-4478-91ff-4da596e3a029
		summarizeBy: none
		sourceColumn: mapping_status

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: 7ad20930-08a8-4b86-9017-09c78717ceef
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: 4ad55e74-b2a4-4aca-8d88-8a40a60e7f4d
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_service_code' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_service_code = Source{[Schema="analytics",Item="dim_service_code"]}[Data]
				in
				    analytics_dim_service_code

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics dim_supporting_info_category

| Column | TMDL type | Hidden |
|---|---|---|
| `supporting_info_category_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 8d5d64e6-e1d4-420d-b478-d41fd04133d1
		summarizeBy: none
		sourceColumn: supporting_info_category_key

		annotation SummarizationSetBy = Automatic

	column system_uri
		dataType: string
		lineageTag: 05f424e0-2ef6-4292-8153-4912bfffbd32
		summarizeBy: none
		sourceColumn: system_uri

		annotation SummarizationSetBy = Automatic

	column code
		dataType: string
		lineageTag: e7801c8b-2d51-4cf1-be41-530c30d21453
		summarizeBy: none
		sourceColumn: code

		annotation SummarizationSetBy = Automatic

	column source_display
		dataType: string
		lineageTag: 0ef4e837-0892-4ee8-9dd0-d909cca80446
		summarizeBy: none
		sourceColumn: source_display

		annotation SummarizationSetBy = Automatic

	column authoritative_display
		dataType: string
		lineageTag: 1fa22546-7249-415d-ae80-82a3321856b9
		summarizeBy: none
		sourceColumn: authoritative_display

		annotation SummarizationSetBy = Automatic

	column mapping_status
		dataType: string
		lineageTag: 32bf7cf1-7016-412d-b3e6-2eb4269013ee
		summarizeBy: none
		sourceColumn: mapping_status

		annotation SummarizationSetBy = Automatic

	column authority
		dataType: string
		lineageTag: 1e6b4ae2-a37f-4912-b690-d30237ccc871
		summarizeBy: none
		sourceColumn: authority

		annotation SummarizationSetBy = Automatic

	column authority_version
		dataType: string
		lineageTag: e4dd8f67-aa65-47e0-b2ec-b5cdb8e58b8c
		summarizeBy: none
		sourceColumn: authority_version

		annotation SummarizationSetBy = Automatic

	partition 'analytics dim_supporting_info_category' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_dim_supporting_info_category = Source{[Schema="analytics",Item="dim_supporting_info_category"]}[Data]
				in
				    analytics_dim_supporting_info_category

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_care_team_occurrence

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_care_team_occurrence_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: d76e2135-d0d5-4e96-bffa-70b9574a4338
		summarizeBy: none
		sourceColumn: fact_care_team_occurrence_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 4c5532d4-dd40-4c6f-9da4-17289b49d3d9
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: c6e8f2b0-cda5-4a25-ba2b-a3a1b2162477
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 77515bf5-1ef1-489f-ad2a-8fba02c3773d
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column provider_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 567c266f-c52e-43dc-9905-81ac7d46ca89
		summarizeBy: none
		sourceColumn: provider_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: bb002234-99dd-4b49-8c90-ddfa439f0f32
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column careteam_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 2c9bf822-edb0-411e-bdec-9f8d5be9800b
		summarizeBy: none
		sourceColumn: careteam_sequence

		annotation SummarizationSetBy = Automatic

	column role_json
		dataType: string
		lineageTag: 42a43155-6cdc-4aa0-8699-67d1c49497fc
		summarizeBy: none
		sourceColumn: role_json

		annotation SummarizationSetBy = Automatic

	column qualification_json
		dataType: string
		lineageTag: d5d48fcf-3163-42de-a294-82e68e1677b4
		summarizeBy: none
		sourceColumn: qualification_json

		annotation SummarizationSetBy = Automatic

	column care_team_row_count
		dataType: int64
		formatString: 0
		lineageTag: ef3648e8-79df-4591-8176-bb571b290633
		summarizeBy: none
		sourceColumn: care_team_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 01b844eb-8e88-4f03-a642-43beb4cbdd5f
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_care_team_occurrence' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_care_team_occurrence = Source{[Schema="analytics",Item="fact_care_team_occurrence"]}[Data]
				in
				    analytics_fact_care_team_occurrence

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_claim

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_claim_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: c6a79093-ad70-4118-b1d6-6d836cf6d753
		summarizeBy: none
		sourceColumn: fact_claim_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 92e7b67c-3093-4fd8-bcfd-7d5d5dfdbb0a
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: da82d9bd-7f61-4a6b-8c92-979b3587ee21
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 3110c04a-bf10-4e93-8f44-99bc3106805a
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column billable_start_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: aa6f5a58-378d-4d10-8f89-4897ffc5d209
		summarizeBy: none
		sourceColumn: billable_start_date_key

		annotation SummarizationSetBy = Automatic

	column billable_end_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: b07a163e-fb4f-430f-a679-a588b7c69ed1
		summarizeBy: none
		sourceColumn: billable_end_date_key

		annotation SummarizationSetBy = Automatic

	column claim_type_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 4e0c56e1-1a2b-4bf9-b8e7-1e25cbdc9606
		summarizeBy: none
		sourceColumn: claim_type_key

		annotation SummarizationSetBy = Automatic

	column provider_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: cb731c23-55cc-4092-930e-a900726b9d8f
		summarizeBy: none
		sourceColumn: provider_key

		annotation SummarizationSetBy = Automatic

	column payer_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 814dd2f7-b0f0-40f3-831b-a2187c3734d5
		summarizeBy: none
		sourceColumn: payer_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: 9f3fb83e-f8f2-456e-a0b3-3605efd4e337
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column claim_status
		dataType: string
		lineageTag: 9d3ff139-5301-4f74-8e26-6605fab198a0
		summarizeBy: none
		sourceColumn: claim_status

		annotation SummarizationSetBy = Automatic

	column claim_use
		dataType: string
		lineageTag: 48b5ee19-d1a0-46ff-af7b-416b016e7ee0
		summarizeBy: none
		sourceColumn: claim_use

		annotation SummarizationSetBy = Automatic

	column claim_outcome
		dataType: string
		lineageTag: 595ca851-7b18-45fb-92ed-e1354b2ce3f1
		summarizeBy: none
		sourceColumn: claim_outcome

		annotation SummarizationSetBy = Automatic

	column claim_row_count
		dataType: int64
		formatString: 0
		lineageTag: a2814d3f-5768-4fe5-8996-12e5a2d07d9e
		summarizeBy: none
		sourceColumn: claim_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 1e0c88c3-c18b-4fc6-ad74-763b25955056
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_claim' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_claim = Source{[Schema="analytics",Item="fact_claim"]}[Data]
				in
				    analytics_fact_claim

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_claim_adjudication

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_claim_adjudication_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 628cc6fe-2ca9-42c9-95d4-86322b40b555
		summarizeBy: none
		sourceColumn: fact_claim_adjudication_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 1c8abb8c-ff75-4c43-93b4-091283d9a6a5
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 1d3db9e3-a5b8-439a-a155-1a6a3a8c05f8
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 4c8e0e82-1b10-46dc-a377-3e4e21a50a2d
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column financial_concept_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: b7c98d4e-21c7-4397-a891-37b2b81ec1ef
		summarizeBy: none
		sourceColumn: financial_concept_key

		annotation SummarizationSetBy = Automatic

	column currency_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 8fc19661-f9fb-4027-b370-4660ed68feaa
		summarizeBy: none
		sourceColumn: currency_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: e3e8e4ab-3c8d-4adb-a0ed-3ab53b0ff8ca
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column source_ordinal
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 96f7144b-5678-444d-b462-dd546186b05f
		summarizeBy: none
		sourceColumn: source_ordinal

		annotation SummarizationSetBy = Automatic

	column amount
		dataType: double
		isHidden
		lineageTag: 9856c87c-515e-4e42-9754-0608058a877f
		summarizeBy: none
		sourceColumn: amount

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column value
		dataType: double
		isHidden
		lineageTag: 62b23fbb-984c-442f-92f7-f56958c2ca86
		summarizeBy: none
		sourceColumn: value

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 0269da55-b0bb-40eb-b3b2-97f794f1ab1d
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_claim_adjudication' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_claim_adjudication = Source{[Schema="analytics",Item="fact_claim_adjudication"]}[Data]
				in
				    analytics_fact_claim_adjudication

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_claim_total

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_claim_total_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 16fdf4b1-5c4c-4506-96fe-6808ecfb9bb9
		summarizeBy: none
		sourceColumn: fact_claim_total_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 502be377-04a7-4b64-b57e-371bd49c9f67
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: f4d246de-6bbd-4435-a1ca-3ef0e4f7d7e3
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: b678218f-3d10-4c48-a677-4f90f7044256
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column financial_concept_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: c276c22a-dee1-4fb4-9e7d-c90f732190fb
		summarizeBy: none
		sourceColumn: financial_concept_key

		annotation SummarizationSetBy = Automatic

	column currency_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 056863de-5e27-4a74-aaf3-7f641826f3e3
		summarizeBy: none
		sourceColumn: currency_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: f86474c2-9992-4f05-8cf6-7e27f67a7adf
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column source_ordinal
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: f82990d6-e91d-4af2-a1bf-6e0ac8d97be8
		summarizeBy: none
		sourceColumn: source_ordinal

		annotation SummarizationSetBy = Automatic

	column amount
		dataType: double
		isHidden
		lineageTag: c72c45ae-d2f9-4220-8b70-8b0eb4de07fa
		summarizeBy: none
		sourceColumn: amount

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 3eb370cf-bd83-4da5-ad43-57c75888a954
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_claim_total' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_claim_total = Source{[Schema="analytics",Item="fact_claim_total"]}[Data]
				in
				    analytics_fact_claim_total

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_diagnosis_occurrence

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_diagnosis_occurrence_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: af19e9d2-0380-4ed3-a585-b608a56a6070
		summarizeBy: none
		sourceColumn: fact_diagnosis_occurrence_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 26e87060-f1d8-4973-9e65-48d024e04d66
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 449e5356-83ec-4862-9ff3-856301f2bee9
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 95d6697a-6ab1-4ee0-bbae-cdb8d567fee5
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column diagnosis_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: a6fb9386-c4c8-4cec-938e-c06b33c85645
		summarizeBy: none
		sourceColumn: diagnosis_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: b04c11db-edb3-40b3-969f-325db8cb4a9f
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column diagnosis_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: c732c35a-de72-47e7-b208-56582e4f1bb4
		summarizeBy: none
		sourceColumn: diagnosis_sequence

		annotation SummarizationSetBy = Automatic

	column diagnosis_row_count
		dataType: int64
		formatString: 0
		lineageTag: 8f2472cc-6bf9-4c17-a57b-168000b08a45
		summarizeBy: none
		sourceColumn: diagnosis_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: dffbd5ab-1fb5-4d3e-99c2-9606a927f738
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_diagnosis_occurrence' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_diagnosis_occurrence = Source{[Schema="analytics",Item="fact_diagnosis_occurrence"]}[Data]
				in
				    analytics_fact_diagnosis_occurrence

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_item

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_item_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 6ebe8048-531b-45ab-bb1f-65cc8391cc80
		summarizeBy: none
		sourceColumn: fact_item_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: e64cfcf7-2431-4e9c-b4c9-666f8cef8232
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 3bd7b178-59e7-4397-b0db-259e3455e4ab
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: c81d3d1e-0d56-4f00-b5f4-147ce2dbd889
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column serviced_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 47ed9b1f-59a6-4360-a7bf-fd0a0c12d179
		summarizeBy: none
		sourceColumn: serviced_date_key

		annotation SummarizationSetBy = Automatic

	column service_code_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 0eb30ba5-9314-450e-964f-bee2377e916d
		summarizeBy: none
		sourceColumn: service_code_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: 27d22477-d3cd-43ca-873b-25d0a831fc79
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column item_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 8a200a70-1dc2-4ef8-af5a-1732ced375fe
		summarizeBy: none
		sourceColumn: item_sequence

		annotation SummarizationSetBy = Automatic

	column quantity_value
		dataType: double
		lineageTag: 2ef8e5bf-8094-4089-8256-abd1f3f2d74b
		summarizeBy: none
		sourceColumn: quantity_value

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column quantity_unit
		dataType: string
		lineageTag: fcc5ba00-a425-43d1-b9e5-3dc92b50ecf3
		summarizeBy: none
		sourceColumn: quantity_unit

		annotation SummarizationSetBy = Automatic

	column item_row_count
		dataType: int64
		formatString: 0
		lineageTag: ac16b223-5298-4270-8c5f-fd2c86d5ddc2
		summarizeBy: none
		sourceColumn: item_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 633f1d48-8531-4c6c-8b50-8e90dc113b9d
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_item' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_item = Source{[Schema="analytics",Item="fact_item"]}[Data]
				in
				    analytics_fact_item

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_item_adjudication

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_item_adjudication_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: a5cb29eb-fd52-4df1-815f-a13b2da619d6
		summarizeBy: none
		sourceColumn: fact_item_adjudication_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 4be85603-8bf3-4985-a7aa-d4059796bd32
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: f5017b2e-4dbb-4ad1-9f7f-31f7ef03f748
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 51059d53-fcb7-4959-ab3b-ab8060c84634
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column financial_concept_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 13cc9bb9-befd-4840-90d2-2c7089c28c8e
		summarizeBy: none
		sourceColumn: financial_concept_key

		annotation SummarizationSetBy = Automatic

	column currency_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 7d905153-2031-441a-bd28-52baef530eea
		summarizeBy: none
		sourceColumn: currency_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: a5765063-7f6b-4334-9e65-65200e31d0ff
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column item_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 437410ae-fee4-4805-8b82-7559b97d9f05
		summarizeBy: none
		sourceColumn: item_sequence

		annotation SummarizationSetBy = Automatic

	column source_ordinal
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 3234fe63-87c0-4d3b-9345-c951b9578447
		summarizeBy: none
		sourceColumn: source_ordinal

		annotation SummarizationSetBy = Automatic

	column amount
		dataType: double
		isHidden
		lineageTag: 2a655389-306b-4b02-bef9-1170de28a6b3
		summarizeBy: none
		sourceColumn: amount

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 79d05479-1855-485d-92c9-eaa860604ab3
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_item_adjudication' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_item_adjudication = Source{[Schema="analytics",Item="fact_item_adjudication"]}[Data]
				in
				    analytics_fact_item_adjudication

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_item_detail

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_item_detail_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 050dfbd9-ea4f-4220-b25e-efd9b191a57b
		summarizeBy: none
		sourceColumn: fact_item_detail_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 26d93a40-0f37-4e73-9e19-8f8aa5bdeb63
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 7de160f0-5080-4bf4-8dc9-11701bb2f8c9
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 60e0d650-7d8f-4376-945a-69649f7d292a
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column service_code_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: a59e3d33-c124-408d-859e-d2a679f82fb6
		summarizeBy: none
		sourceColumn: service_code_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: 8878526c-a261-4e47-9b59-1bac64c397ae
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column item_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 02bcbcbe-d7d4-4ff9-8e56-f8261b20a21d
		summarizeBy: none
		sourceColumn: item_sequence

		annotation SummarizationSetBy = Automatic

	column detail_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: b777f544-7598-4d75-ad0b-72acb17a99b7
		summarizeBy: none
		sourceColumn: detail_sequence

		annotation SummarizationSetBy = Automatic

	column quantity_value
		dataType: double
		lineageTag: f46bb69d-2159-430d-9833-e1ed0308ca43
		summarizeBy: none
		sourceColumn: quantity_value

		annotation SummarizationSetBy = Automatic

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column quantity_unit
		dataType: string
		lineageTag: 91f84bd2-f743-487d-bd09-34dbfe4c1a1b
		summarizeBy: none
		sourceColumn: quantity_unit

		annotation SummarizationSetBy = Automatic

	column item_detail_row_count
		dataType: int64
		formatString: 0
		lineageTag: e137faed-ccfb-4ebc-b5ad-dfce0e5d17f6
		summarizeBy: none
		sourceColumn: item_detail_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 92df4825-1868-4f25-94e7-b4ce325fcf2f
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_item_detail' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_item_detail = Source{[Schema="analytics",Item="fact_item_detail"]}[Data]
				in
				    analytics_fact_item_detail

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_procedure_occurrence

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_procedure_occurrence_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 5807f471-40dc-485f-8654-157d98636c16
		summarizeBy: none
		sourceColumn: fact_procedure_occurrence_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 99a4a1ca-005c-4095-8d13-23489931b1dd
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 751b8b1d-c929-46b8-814f-bbab7091ea32
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 72400ea6-b480-4cc4-982b-a5b30e086de0
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column procedure_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 7a434afa-8171-47f0-a497-c0f840393ad5
		summarizeBy: none
		sourceColumn: procedure_date_key

		annotation SummarizationSetBy = Automatic

	column procedure_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 8b0a6914-f1a1-463c-9d1d-8482dd616b9e
		summarizeBy: none
		sourceColumn: procedure_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: 3a7b4365-e3c1-44fe-9be3-a6a8c3a3aff4
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column procedure_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: a1da1da2-2f77-4b6c-a2c4-4a21c1bcfeaa
		summarizeBy: none
		sourceColumn: procedure_sequence

		annotation SummarizationSetBy = Automatic

	column procedure_row_count
		dataType: int64
		formatString: 0
		lineageTag: 814b9ee8-eee6-4444-a133-73f2a92c7160
		summarizeBy: none
		sourceColumn: procedure_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: 234cab98-a49a-464f-84a9-6e42925f95ab
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_procedure_occurrence' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_procedure_occurrence = Source{[Schema="analytics",Item="fact_procedure_occurrence"]}[Data]
				in
				    analytics_fact_procedure_occurrence

	annotation PBI_ResultType = Table
` | unspecified | no |

### analytics fact_supporting_info_occurrence

| Column | TMDL type | Hidden |
|---|---|---|
| `fact_supporting_info_occurrence_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 0809c847-471f-44d0-b4fa-f9cf35c985df
		summarizeBy: none
		sourceColumn: fact_supporting_info_occurrence_key

		annotation SummarizationSetBy = Automatic

	column pipeline_run_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: debde9cb-1f50-46d3-ae28-08ae0b3e9c15
		summarizeBy: none
		sourceColumn: pipeline_run_key

		annotation SummarizationSetBy = Automatic

	column patient_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 8127400c-cffb-44d2-aaa3-0a491e1368dc
		summarizeBy: none
		sourceColumn: patient_key

		annotation SummarizationSetBy = Automatic

	column claim_created_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 77439a76-454f-46a6-a748-7064d54d51e0
		summarizeBy: none
		sourceColumn: claim_created_date_key

		annotation SummarizationSetBy = Automatic

	column timing_date_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: f20d056b-12b9-44d0-bb5c-873259e5504a
		summarizeBy: none
		sourceColumn: timing_date_key

		annotation SummarizationSetBy = Automatic

	column supporting_info_category_key
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: a3f5a472-117a-45c4-9285-a47624567936
		summarizeBy: none
		sourceColumn: supporting_info_category_key

		annotation SummarizationSetBy = Automatic

	column eob_id
		dataType: string
		lineageTag: 09f42fff-740e-4017-9943-c38bf9650bd3
		summarizeBy: none
		sourceColumn: eob_id

		annotation SummarizationSetBy = Automatic

	column supporting_info_sequence
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: f6ff9165-843e-4fb3-ab2b-37c471a1931b
		summarizeBy: none
		sourceColumn: supporting_info_sequence

		annotation SummarizationSetBy = Automatic

	column value_string
		dataType: string
		lineageTag: ce25afac-9f94-4a66-b936-7db60838c4ad
		summarizeBy: none
		sourceColumn: value_string

		annotation SummarizationSetBy = Automatic

	column code_json
		dataType: string
		lineageTag: d0f1f09e-1df9-4998-aa86-b1af5b5608ed
		summarizeBy: none
		sourceColumn: code_json

		annotation SummarizationSetBy = Automatic

	column value_quantity_json
		dataType: string
		lineageTag: 7335038c-1f2a-4e39-9dcd-87f447bb65b5
		summarizeBy: none
		sourceColumn: value_quantity_json

		annotation SummarizationSetBy = Automatic

	column supporting_info_row_count
		dataType: int64
		formatString: 0
		lineageTag: 729b5d53-4412-4629-822b-805fb5e40f28
		summarizeBy: none
		sourceColumn: supporting_info_row_count

		annotation SummarizationSetBy = Automatic

	column source_record_hash
		dataType: string
		isHidden
		lineageTag: ebaab75d-251c-42f0-bc95-eec00eddfa83
		summarizeBy: none
		sourceColumn: source_record_hash

		annotation SummarizationSetBy = Automatic

	partition 'analytics fact_supporting_info_occurrence' = m
		mode: import
		source =
				let
				    Source = PostgreSQL.Database("localhost", "healthcare_interoperability_claims"),
				    analytics_fact_supporting_info_occurrence = Source{[Schema="analytics",Item="fact_supporting_info_occurrence"]}[Data]
				in
				    analytics_fact_supporting_info_occurrence

	annotation PBI_ResultType = Table
` | unspecified | no |

## Relationship endpoints

TMDL omits default properties. ?Default? below means omitted in source, not a newly declared cardinality. Five relationships explicitly set `isActive: false`. Coverage endpoints and fact-to-fact relationships are absent.

| From column | To column | Active |
|---|---|---|
| `'analytics fact_claim'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_claim'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_claim'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_item'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_item'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_item'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_claim_total'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_claim_total'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_claim_total'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_claim_adjudication'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_claim_adjudication'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_claim_adjudication'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_item_adjudication'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_item_adjudication'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_item_adjudication'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_diagnosis_occurrence'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_diagnosis_occurrence'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_diagnosis_occurrence'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_procedure_occurrence'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_procedure_occurrence'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_procedure_occurrence'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_care_team_occurrence'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_care_team_occurrence'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_care_team_occurrence'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_supporting_info_occurrence'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_supporting_info_occurrence'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_supporting_info_occurrence'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_item_detail'.pipeline_run_key` | `'analytics dim_pipeline_run'.pipeline_run_key` | default |
| `'analytics fact_item_detail'.patient_key` | `'analytics dim_patient'.patient_key` | default |
| `'analytics fact_item_detail'.claim_created_date_key` | `'analytics dim_date'.date_key` | default |
| `'analytics fact_claim'.billable_start_date_key` | `'analytics dim_date'.date_key` | false |
| `'analytics fact_claim'.billable_end_date_key` | `'analytics dim_date'.date_key` | false |
| `'analytics fact_item'.serviced_date_key` | `'analytics dim_date'.date_key` | false |
| `'analytics fact_procedure_occurrence'.procedure_date_key` | `'analytics dim_date'.date_key` | false |
| `'analytics fact_supporting_info_occurrence'.timing_date_key` | `'analytics dim_date'.date_key` | false |
| `'analytics fact_claim'.claim_type_key` | `'analytics dim_claim_type'.claim_type_key` | default |
| `'analytics fact_claim'.provider_key` | `'analytics dim_provider'.provider_key` | default |
| `'analytics fact_claim'.payer_key` | `'analytics dim_payer'.payer_key` | default |
| `'analytics fact_item'.service_code_key` | `'analytics dim_service_code'.service_code_key` | default |
| `'analytics fact_claim_total'.financial_concept_key` | `'analytics dim_financial_concept'.financial_concept_key` | default |
| `'analytics fact_claim_total'.currency_key` | `'analytics dim_currency'.currency_key` | default |
| `'analytics fact_claim_adjudication'.financial_concept_key` | `'analytics dim_financial_concept'.financial_concept_key` | default |
| `'analytics fact_claim_adjudication'.currency_key` | `'analytics dim_currency'.currency_key` | default |
| `'analytics fact_item_adjudication'.financial_concept_key` | `'analytics dim_financial_concept'.financial_concept_key` | default |
| `'analytics fact_item_adjudication'.currency_key` | `'analytics dim_currency'.currency_key` | default |
| `'analytics fact_diagnosis_occurrence'.diagnosis_key` | `'analytics dim_diagnosis'.diagnosis_key` | default |
| `'analytics fact_procedure_occurrence'.procedure_key` | `'analytics dim_procedure'.procedure_key` | default |
| `'analytics fact_care_team_occurrence'.provider_key` | `'analytics dim_provider'.provider_key` | default |
| `'analytics fact_supporting_info_occurrence'.supporting_info_category_key` | `'analytics dim_supporting_info_category'.supporting_info_category_key` | default |
| `'analytics fact_item_detail'.service_code_key` | `'analytics dim_service_code'.service_code_key` | default |

## Governed measures

Exact expressions from `_Measures.tmdl`. All require one run. The final three are hidden financial primitives and also require one concept/currency; they are not consolidated business KPIs.

### Claim Count

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_claim'), BLANK())
```

### Item Count

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_item'), BLANK())
```

### Diagnosis Occurrences

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_diagnosis_occurrence'), BLANK())
```

### Procedure Occurrences

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_procedure_occurrence'), BLANK())
```

### Care Team Occurrences

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_care_team_occurrence'), BLANK())
```

### Supporting Info Occurrences

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]), COUNTROWS('analytics fact_supporting_info_occurrence'), BLANK())
```

### Claim Total Amount

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_claim_total'[amount]), BLANK())
```

### Claim Adjudication Amount

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_claim_adjudication'[amount]), BLANK())
```

### Item Adjudication Amount

```dax
IF(HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key]) && HASONEVALUE('analytics dim_financial_concept'[financial_concept_key]) && HASONEVALUE('analytics dim_currency'[currency_key]), SUM('analytics fact_item_adjudication'[amount]), BLANK())
```

## Source fingerprints

| Source | SHA-256 |
|---|---|
| `src/healthcare_claims/dimensional_model.py` | `b2b0770b5b806131623db79cfd02a7719bae65ff5a98c08f7b5cf28a345531c9` |
| `sql/04_create_analytics_model.sql` | `e4d853d06ed2ec057ff2e9f1aac9d0b5bb170bad528634f6bd2b286c4c353958` |
| `powerbi/HealthcareInteroperabilityClaims.SemanticModel/definition/relationships.tmdl` | `011ab5e1769b49be2e1719dd1d6d7483d9cc98e227cf1d29b7b79894a29b526a` |
| `powerbi/HealthcareInteroperabilityClaims.SemanticModel/definition/tables/_Measures.tmdl` | `0964c36d9275e5229b1dc2c3dbd26223825ccf4ce7bdbb3f6c30ff4d388699fb` |
