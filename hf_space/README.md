---
title: MedLake PySpark
emoji: ⚡
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 7860
pinned: true
license: mit
short_description: End-to-end PySpark lakehouse with verified data quality
tags:
- pyspark
- azure
- data-engineering
- lakehouse
- delta-lake
- streaming
- terraform
- ci-cd
- data-quality
- gradio
---

# MedLake PySpark — End-to-End Data Platform Deployment Project

**Author:** Ankit Kumar Singh  
**Positioning:** PySpark • Azure Data Platform • Lakehouse • Streaming • Data Quality • IaC • CI/CD  
**Live runtime:** Hugging Face Docker Space  
**Source repository:** https://github.com/singhankitsrf/MedLake-Azure-PySpark

MedLake is a recruiter-facing **end-to-end healthcare data-platform engineering project**. It demonstrates a medallion/lakehouse workflow with PySpark transformations, deterministic data-quality controls, quarantine handling, replay-safe deduplication, Gold KPI reconciliation, streaming design, Azure deployment assets, Terraform, and CI/CD.

> **Evidence boundary:** The Hugging Face Space executes the shared PySpark transformation logic locally on synthetic events. It does **not** claim a live Azure deployment, Azure latency benchmark, or cloud-cost result.

## What this project demonstrates

- synthetic healthcare-event generation for safe reproducible testing
- Bronze/Silver/Gold medallion architecture
- schema and quality validation
- quarantine path for invalid events
- deterministic duplicate removal
- replay/idempotency verification
- Gold aggregate reconciliation against Silver
- PySpark execution in the live demo
- checkpointed streaming design for Event Hubs → Silver/Gold
- Delta Lake / Databricks-oriented architecture
- ADLS Gen2 integration design
- Azure Data Factory orchestration assets
- Event Hubs streaming configuration
- Key Vault and Azure Monitor integration boundaries
- Terraform infrastructure-as-code
- GitHub Actions validation and publication

## End-to-end lakehouse flow

```text
Synthetic / incoming healthcare events
        ↓
Bronze ingestion
(raw, replayable event layer)
        ↓
Schema + quality validation
        ├─ invalid → quarantine
        └─ valid → continue
        ↓
Deterministic deduplication
        ↓
Silver conformed records
        ↓
Gold facility/day KPIs
        ↓
Reconciliation checks
        ↓
Replay/idempotency validation
        ↓
Dockerized interactive runtime
        ↓
GitHub Actions validation
        ↓
Hugging Face Space
```

## Measured reproducible PySpark evidence

The repository contains a saved seeded run produced by the same shared transformations used by the demo:

| Evidence | Result |
|---|---:|
| Seed | 42 |
| Generated synthetic rows | 1,000 |
| Input rows after injected faults/duplicates | 1,003 |
| Unique valid rows | 996 |
| Quarantined invalid rows | 5 |
| Duplicate valid rows removed | 2 |
| Gold screenings | 996 |
| Invalid rows quarantined | PASS |
| Expected unique valid rows | PASS |
| Gold reconciles to Silver | PASS |
| Replay deduplication idempotent | PASS |
| Spark version | 3.5.3 |

The saved fixture also records a SHA-256 hash so the seeded evidence can be tied to a concrete input fixture.

## Streaming architecture

```text
Azure Event Hubs
        ↓
Streaming Bronze table
        ↓
Checkpointed micro-batch consumer
        ↓
Shared quality transformations
        ├─ quarantine invalid records
        └─ deduplicate valid records
        ↓
Streaming Silver
        ↓
Gold KPI aggregation
        ↓
Operational monitoring / replay controls
```

The GitHub implementation preserves a replayable Bronze layer and uses checkpointed streaming/micro-batch processing so the same transformation contract can be exercised both locally and in the cloud-oriented design.

## Azure reference architecture

```text
Producers / batch sources
        ↓
Event Hubs / ADF
        ↓
ADLS Gen2 Bronze
        ↓
Databricks + PySpark + Delta
        ↓
Silver / Gold lakehouse tables
        ↓
Monitoring + downstream analytics

Supporting controls:
Terraform • Key Vault • Azure Monitor • GitHub Actions OIDC
```

## Reproducibility and data-quality controls

The project treats reconciliation as a release requirement rather than a dashboard afterthought. The local evaluation verifies:

- deterministic fixture generation
- explicit injected bad records
- quarantine accounting
- valid-row deduplication
- Gold-to-Silver count reconciliation
- replay/idempotency behavior
- runtime/Spark-version provenance

## Hugging Face deployment role

The public Space runs **actual local PySpark transformations** on user-selected synthetic row counts. It generates fictional events, injects controlled faults/duplicates, executes the pipeline, and returns:

- reconciliation results
- quarantine/deduplication checks
- replay/idempotency status
- Gold daily facility KPI preview
- saved seeded evaluation evidence

This makes the data-platform project directly executable for recruiters without pretending the browser session is an Azure Databricks workspace.

## CI/CD release controls

```text
Pull request / deployment change
        ↓
Stage tracked Space bundle
        ↓
Build exact Docker image
        ↓
Start Spark-enabled container
        ↓
HTTP application smoke test
        ↓
Publish validated Space to Hugging Face
```

## Engineering decisions

**Why preserve Bronze?**  
A replayable raw layer supports audit, recovery, schema evolution, and deterministic reprocessing.

**Why quarantine instead of silently dropping bad records?**  
Silent loss breaks reconciliation and obscures upstream quality problems. Quarantine makes invalid-data handling observable.

**Why test replay/idempotency?**  
Streaming and distributed pipelines can reprocess events. Deterministic deduplication prevents replay from inflating business metrics.

**Why separate local evidence from Azure claims?**  
Local PySpark execution proves transformation behavior; it does not prove cloud networking, scale, latency, cost, or account configuration.

## Responsible-use statement

MedLake uses synthetic data in the public demonstration. Production healthcare deployment would additionally require data-governance controls, access policies, encryption, retention rules, observability, incident response, privacy/compliance review, and organization-specific security approval.

## Explore the implementation

- **GitHub source:** https://github.com/singhankitsrf/MedLake-Azure-PySpark
- **Saved PySpark evaluation:** https://github.com/singhankitsrf/MedLake-Azure-PySpark/blob/main/evaluation/local_spark.json
- **Streaming design:** https://github.com/singhankitsrf/MedLake-Azure-PySpark/blob/main/docs/STREAMING_END_TO_END.md
- **Hugging Face Space:** https://huggingface.co/spaces/singhankit491/medlake-pyspark

### Portfolio signal

This project demonstrates **AI Lead / Senior Data Platform Engineering** capability across PySpark, lakehouse architecture, streaming, data quality, reconciliation, replay safety, infrastructure-as-code, CI/CD, Azure platform design, and evidence-backed technical communication.