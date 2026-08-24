import os
from pyspark.sql import functions as F
catalog=os.getenv("MEDLAKE_CATALOG","medlake"); landing_path=os.environ["MEDLAKE_LANDING_PATH"]; schema_path=f"{os.environ['MEDLAKE_SCHEMA_BASE'].rstrip('/')}/screening-events"; checkpoint_path=f"{os.environ['MEDLAKE_CHECKPOINT_BASE'].rstrip('/')}/screening-events-batch"; target=f"{catalog}.bronze.screening_events_raw"
raw=(spark.readStream.format("cloudFiles").option("cloudFiles.format","json").option("cloudFiles.schemaLocation",schema_path).option("cloudFiles.schemaEvolutionMode","rescue").option("rescuedDataColumn","_rescued_data").load(landing_path).withColumn("_ingested_at",F.current_timestamp()).withColumn("_source_file",F.input_file_name()))
query=raw.writeStream.format("delta").option("checkpointLocation",checkpoint_path).option("mergeSchema","true").trigger(availableNow=True).toTable(target); query.awaitTermination()
