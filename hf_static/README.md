---
title: MedLake Azure PySpark
emoji: 🧱
colorFrom: indigo
colorTo: blue
sdk: static
app_file: index.html
pinned: true
license: mit
short_description: Azure PySpark lakehouse with measured pipeline evidence
tags:
- pyspark
- azure
- databricks
- delta-lake
- data-engineering
- lakehouse
- terraform
- mlops
- ci-cd
---

# MedLake Azure PySpark — End-to-End Data Platform Deployment Project

**Author:** Ankit Kumar Singh  
**Positioning:** Data Engineering • PySpark • Azure • Databricks • Delta Lake • Streaming • Terraform • CI/CD

MedLake is a healthcare-oriented lakehouse engineering project that connects synthetic event generation, Bronze/Silver/Gold transformations, data-quality controls, quarantine, deduplication, reconciliation and streaming architecture.

The public Hugging Face Space is a free static evidence explorer. The actual PySpark transformations remain in GitHub and were executed in a seeded validation run; the Space reports those measured outputs without claiming an Azure deployment that was not executed.

## Measured seeded run

| Measure | Value |
|---|---:|
| Generated rows | 1,000 |
| Rows after injected faults/duplicates | 1,003 |
| Unique valid Silver rows | 996 |
| Quarantined rows | 5 |
| Valid duplicates removed | 2 |
| Gold screenings | 996 |
| Invalid rows quarantined | Pass |
| Gold reconciles to Silver | Pass |
| Replay deduplication idempotent | Pass |
| Spark version | 3.5.3 |

## End-to-end platform flow

```text
Synthetic/event input
→ Bronze ingestion
→ schema + quality validation
→ quarantine invalid records
→ Silver normalization + deduplication
→ Gold KPI aggregation
→ reconciliation + replay/idempotency checks
→ Event Hubs / Databricks streaming design
→ Terraform + GitHub Actions
→ Hugging Face evidence Space
```

## Evidence boundary

- PySpark seeded validation: executed
- local Spark reconciliation/idempotency checks: executed
- Azure Terraform/Databricks/Event Hubs architecture: implemented in GitHub
- actual Azure deployment, cloud latency and cloud cost: not claimed
- all demonstration records: synthetic

- GitHub: https://github.com/singhankitsrf/MedLake-Azure-PySpark
- Space: https://huggingface.co/spaces/singhankit491/medlake-pyspark
