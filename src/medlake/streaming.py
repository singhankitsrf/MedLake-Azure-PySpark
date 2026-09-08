"""Parse the Event Hubs Bronze table and incrementally curate Delta outputs."""

from __future__ import annotations
from .spark_transforms import (
    normalize_events,
    add_quality_flags,
    deduplicate_batch,
    daily_facility_kpis,
)

EVENT_SCHEMA = "event_id string, event_ts string, patient_id string, facility_id string, screening_mode string, device_type string, predicted_class string, model_confidence double, image_quality_score double, referred boolean, referral_reason string, ingestion_source string, schema_version int"


def parse_bronze(df):
    from pyspark.sql import functions as F

    return df.select(
        F.from_json("json_payload", EVENT_SCHEMA).alias("event"),
        F.sha2("json_payload", 256).alias("_payload_sha256"),
    ).select("event.*", "_payload_sha256")


def process_bronze_batch(batch, batch_id, catalog):
    from delta.tables import DeltaTable
    from pyspark.sql import functions as F

    spark = batch.sparkSession
    curated = add_quality_flags(normalize_events(parse_bronze(batch))).cache()
    try:
        valid = deduplicate_batch(curated.filter("_is_valid"))
        invalid = curated.filter("NOT _is_valid").dropDuplicates(["_payload_sha256"])
        for name, frame, key in (
            ("stream_screening_events", valid, "event_id"),
            ("stream_screening_events_quarantine", invalid, "_payload_sha256"),
        ):
            table = f"{catalog}.silver.{name}"
            if not spark.catalog.tableExists(table):
                frame.limit(0).write.format("delta").saveAsTable(table)
            merge = (
                DeltaTable.forName(spark, table)
                .alias("t")
                .merge(frame.alias("s"), f"t.{key} = s.{key}")
            )
            # Quarantine is immutable by payload hash. Silver uses append-only
            # event IDs: replay is idempotent and duplicate IDs do not overwrite.
            merge.whenNotMatchedInsertAll().execute()
        daily_facility_kpis(spark.table(f"{catalog}.silver.stream_screening_events")).write.format(
            "delta"
        ).mode("overwrite").saveAsTable(f"{catalog}.gold.stream_daily_facility_kpis")
    finally:
        curated.unpersist()
