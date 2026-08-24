from __future__ import annotations
def normalize_events(df):
    from pyspark.sql import functions as F
    return df.withColumn("event_ts",F.to_timestamp("event_ts")).withColumn("model_confidence",F.col("model_confidence").cast("double")).withColumn("image_quality_score",F.col("image_quality_score").cast("double")).withColumn("schema_version",F.col("schema_version").cast("int")).withColumn("referred",F.col("referred").cast("boolean")).withColumn("_processed_at",F.current_timestamp()).withColumn("_event_date",F.to_date("event_ts"))
def add_quality_flags(df):
    from pyspark.sql import functions as F
    return df.withColumn("_quality_errors",F.array_compact(F.array(F.when(F.col("event_id").isNull(),F.lit("event_id_not_null")),F.when(F.col("patient_id").isNull(),F.lit("patient_id_not_null")),F.when(F.col("facility_id").isNull(),F.lit("facility_id_not_null")),F.when((F.col("model_confidence")<0)|(F.col("model_confidence")>1),F.lit("confidence_range")),F.when((F.col("image_quality_score")<0)|(F.col("image_quality_score")>1),F.lit("quality_range"))))).withColumn("_is_valid",F.size("_quality_errors")==0)
def deduplicate_batch(df):
    from pyspark.sql import Window,functions as F
    w=Window.partitionBy("event_id").orderBy(F.col("_processed_at").desc()); return df.withColumn("_rn",F.row_number().over(w)).filter(F.col("_rn")==1).drop("_rn")
def daily_facility_kpis(df):
    from pyspark.sql import functions as F
    return df.groupBy("_event_date","facility_id").agg(F.count("*").alias("screenings"),F.avg("model_confidence").alias("avg_model_confidence"),F.avg("image_quality_score").alias("avg_image_quality"),F.sum(F.col("referred").cast("int")).alias("referrals"),F.avg(F.col("referred").cast("double")).alias("referral_rate"))
def class_mix_kpis(df):
    from pyspark.sql import functions as F
    totals=df.groupBy("_event_date","facility_id").agg(F.count("*").alias("_total")); by_class=df.groupBy("_event_date","facility_id","predicted_class").agg(F.count("*").alias("class_count")); return by_class.join(totals,["_event_date","facility_id"]).withColumn("class_share",F.col("class_count")/F.col("_total")).drop("_total")
