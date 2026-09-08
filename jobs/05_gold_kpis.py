import os
from medlake.spark_transforms import class_mix_kpis, daily_facility_kpis

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

catalog = os.getenv("MEDLAKE_CATALOG", "medlake")
events = spark.table(f"{catalog}.silver.screening_events")
daily_facility_kpis(events).write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).saveAsTable(f"{catalog}.gold.facility_daily_kpis")
class_mix_kpis(events).write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).saveAsTable(f"{catalog}.gold.facility_class_mix")
