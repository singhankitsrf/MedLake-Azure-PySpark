# Architecture

Batch files enter through Databricks Auto Loader and real-time events enter through Azure Event Hubs/Structured Streaming. Both land in replayable Bronze Delta tables. Silver applies normalization, deduplication, reference enrichment and explicit quality quarantine. Gold publishes operational KPIs and quality observability. Terraform provisions the Azure platform; Databricks bundle resources define jobs; GitHub Actions demonstrates OIDC-based deployment.
