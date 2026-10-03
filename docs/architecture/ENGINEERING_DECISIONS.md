# Engineering decisions

Status: CURRENT / RELEASE. Observed implementation choices, not newly approved architecture.

| Decision | Evidence and reason | Boundary |
|---|---|---|
| Authorization Code + PKCE S256/state | `oauth.py` binds exchange to a verifier and checks callback state. | Interactive loopback authorization; no production identity lifecycle. |
| Next links plus unique resource keys | `fhir.py` and tests validate pagination; historical source exception records misleading totals. | Bundle.total alone is not completeness evidence. |
| Run identity across layers | STAGING/analytics keys, reconciliation, report filter and DAX guards. | No implicit cross-run totals. |
| Curated public synthetic inputs | Manifest and ignore policy. | Private snapshot/caches omitted; source checks cannot recreate populated screenshots. |
| Normalize references before dimensions | `reference_normalization.py` retains identity and limitations. | Display text does not manufacture Coverage/provider/payer identity. |
| Separate financial grains | Three financial families and guarded hidden measures. | No consolidated financial KPI approval. |
| Expose mapping status | Source labels and statuses remain in report pages. | Pending clinical enrichment is not authoritative mapping. |
| Exclude Coverage relationships | Current TMDL and relationship file. | Upstream Coverage retained; no silent semantic expansion. |
| PBIP/PBIR/TMDL delivery | Inspectable definitions alongside screenshots. | Credentials, caches and runtime validation stay local. |
| Standard library and src layout | No external runtime imports; 94 unittest cases. | Explicit orchestration still needed beyond CLI ingestion. |
| Preserve validated implementation | Changes confined to release surfaces. | Historical source status constants documented rather than casually changing tested behavior. |
