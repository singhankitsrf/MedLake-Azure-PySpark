# MedLake Azure PySpark — Project Charter

**Owner:** Ankit Kumar Singh  
**Portfolio role:** Data Platform Engineer / Azure Data Engineer / AI Platform Lead  
**Project type:** Healthcare lakehouse and streaming data-engineering reference implementation

## Product objective

Demonstrate an Azure-oriented medallion lakehouse that supports batch and streaming ingestion, reusable PySpark quality rules, quarantine, deduplication, replayable Bronze storage, Gold KPI marts, infrastructure-as-code, and reproducible data-platform delivery.

## Current delivered scope

- Bronze/Silver/Gold medallion architecture
- PySpark reusable data-quality modules
- batch ingestion and Structured Streaming patterns
- quarantine, schema-drift and deduplication logic
- Gold operational/data-quality KPIs
- Databricks job/bundle assets
- ADLS/Event Hubs/Data Factory/Key Vault/Azure Monitor reference architecture
- Terraform infrastructure definitions
- GitHub Actions CI/CD pattern
- synthetic local Spark evaluation evidence
- Hugging Face portfolio/evidence surface

## Delivery roadmap

### Phase 1 — Lakehouse foundation — COMPLETE
- [x] medallion architecture
- [x] PySpark transformation modules
- [x] quality/quarantine/deduplication controls
- [x] streaming design
- [x] Terraform + Databricks deployment assets
- [x] local reproducibility checks

### Phase 2 — Azure execution evidence — NEXT
- [ ] Deploy infrastructure in an owned Azure environment
- [ ] Run Databricks batch and streaming jobs
- [ ] Connect Event Hubs ingestion and checkpointed processing
- [ ] Validate ADLS/Delta replay and idempotency in cloud execution
- [ ] Capture Azure Monitor and Databricks job evidence
- [ ] Measure cost, throughput and end-to-end latency

### Phase 3 — Platform hardening
- [ ] Add Unity Catalog permissions and data-governance tests
- [ ] Add schema-evolution contract testing
- [ ] Add data-quality SLO dashboards
- [ ] Add backfill/replay runbooks
- [ ] Add disaster-recovery and failure-injection tests

## Success criteria

1. Bronze replay remains idempotent and Silver/Gold reconciliation is testable.
2. Invalid events are quarantined with traceable reasons.
3. Infrastructure and Databricks jobs are reproducible from code.
4. Cloud performance/cost claims are published only after measured Azure execution.

## Risks and controls

| Risk | Control |
|---|---|
| Duplicate/replayed events | deterministic deduplication + checkpointing |
| Invalid data entering marts | quality rules + quarantine |
| Schema drift | explicit evolution/contract handling |
| Unsupported cloud claims | local-vs-Azure evidence boundary |

## Recruiter signal

PySpark · Azure · Databricks · Delta Lake · Structured Streaming · Data Engineering · Terraform · Lakehouse · Data Quality · CI/CD
