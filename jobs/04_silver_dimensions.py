import os
from pyspark.sql import functions as F

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

catalog = os.getenv("MEDLAKE_CATALOG", "medlake")
patients = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(os.environ["MEDLAKE_PATIENT_PATH"])
    .dropDuplicates(["patient_id"])
    .withColumn("_loaded_at", F.current_timestamp())
)
facilities = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(os.environ["MEDLAKE_FACILITY_PATH"])
    .dropDuplicates(["facility_id"])
    .withColumn("_loaded_at", F.current_timestamp())
)
patients.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(
    f"{catalog}.silver.dim_patient"
)
facilities.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(
    f"{catalog}.silver.dim_facility"
)
