# Event Hubs to Gold

Create the catalog and Bronze/Silver/Gold schemas with `sql/00_catalog_setup.sql`.
Deploy the streaming bundle. The consumer creates the empty Bronze table if needed before starting.
The two long-running tasks operate concurrently: ingestion appends raw JSON to Bronze;
the new consumer parses that table and uses checkpointed `foreachBatch` processing to quarantine invalid rows,
merge unique valid event IDs into `silver.stream_screening_events`, and recompute `gold.stream_daily_facility_kpis`.
Streaming tables are separate from batch tables, so batch overwrite jobs cannot erase streamed records.

Silver treats event IDs as immutable. Corrected events require new IDs; updates to an existing ID are not applied.
Gold recomputation is appropriate for this demonstration scale, not a claimed large-scale optimization.
Delta writes are idempotent per target, but not a transaction across all tables. Replaying a failed batch repairs
Gold after a Silver commit. Keep one writer per target and one checkpoint per stream.

`PYTHONPATH=.:src python scripts/evaluate_local.py` verifies the actual parsing, quality,
deduplication and aggregation transformations with injected nulls, malformed JSON, invalid ranges,
invalid timestamps, and repeated events. It does not verify Azure credentials, Event Hubs connectivity,
or Delta cloud operations. Those require an account deployment run.
