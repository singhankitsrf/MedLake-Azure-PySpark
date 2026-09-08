"""Run after starting Event Hubs ingestion; schemas must exist."""

import os
from medlake.streaming import process_bronze_batch

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

catalog = os.getenv("MEDLAKE_CATALOG", "medlake")
checkpoint = os.environ["MEDLAKE_CHECKPOINT_BASE"].rstrip("/") + "/silver-gold-v1"
spark.sql(
    f"CREATE TABLE IF NOT EXISTS {catalog}.bronze.screening_events_stream (_eventhub_ts TIMESTAMP, _eventhub_partition INT, _eventhub_offset BIGINT, json_payload STRING) USING DELTA"
)
query = (
    spark.readStream.table(f"{catalog}.bronze.screening_events_stream")
    .writeStream.foreachBatch(
        lambda frame, batch_id: process_bronze_batch(frame, batch_id, catalog)
    )
    .option("checkpointLocation", checkpoint)
    .trigger(processingTime="30 seconds")
    .start()
)
query.awaitTermination()
