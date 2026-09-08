"""Shared transformations for local evaluation and Databricks jobs."""

from __future__ import annotations


def normalize_events(df):
    from pyspark.sql import functions as F

    return (
        df.withColumn("event_ts", F.to_timestamp("event_ts"))
        .withColumn("model_confidence", F.col("model_confidence").cast("double"))
        .withColumn("image_quality_score", F.col("image_quality_score").cast("double"))
        .withColumn("schema_version", F.col("schema_version").cast("int"))
        .withColumn("referred", F.col("referred").cast("boolean"))
        .withColumn("_processed_at", F.current_timestamp())
        .withColumn("_event_date", F.to_date("event_ts"))
    )


def add_quality_flags(df):
    from pyspark.sql import functions as F
    from .contracts import ALLOWED_CLASSES, ALLOWED_SCREENING_MODES

    checks = []
    for field in ("event_id", "patient_id", "facility_id"):
        checks.append(
            F.when(F.col(field).isNull() | (F.trim(F.col(field)) == ""), F.lit(field + "_not_null"))
        )
    for field, name in (
        ("model_confidence", "confidence_range"),
        ("image_quality_score", "quality_range"),
    ):
        checks.append(
            F.when(
                F.col(field).isNull() | F.isnan(field) | ~F.col(field).between(0, 1), F.lit(name)
            )
        )
    checks.extend(
        [
            F.when(F.col("event_ts").isNull(), F.lit("event_ts_invalid")),
            F.when(
                F.col("predicted_class").isNull()
                | ~F.col("predicted_class").isin(sorted(ALLOWED_CLASSES)),
                F.lit("unknown_predicted_class"),
            ),
            F.when(
                F.col("screening_mode").isNull()
                | ~F.col("screening_mode").isin(sorted(ALLOWED_SCREENING_MODES)),
                F.lit("unknown_screening_mode"),
            ),
            F.when(F.col("referred").isNull(), F.lit("referred_invalid")),
            F.when(
                F.col("schema_version").isNull() | (F.col("schema_version") != 1),
                F.lit("unsupported_schema_version"),
            ),
        ]
    )
    return df.withColumn("_quality_errors", F.array_compact(F.array(*checks))).withColumn(
        "_is_valid", F.size("_quality_errors") == 0
    )


def deduplicate_batch(df):
    from pyspark.sql import Window, functions as F

    stable_columns = sorted(c for c in df.columns if not c.startswith("_"))
    fingerprint = F.sha2(F.to_json(F.struct(*[F.col(c) for c in stable_columns])), 256)
    # event timestamp and content digest establish deterministic replay order.
    w = Window.partitionBy("event_id").orderBy(
        F.col("event_ts").desc_nulls_last(), fingerprint.desc()
    )
    return df.withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn") == 1).drop("_rn")


def daily_facility_kpis(df):
    from pyspark.sql import functions as F

    return df.groupBy("_event_date", "facility_id").agg(
        F.count("*").alias("screenings"),
        F.avg("model_confidence").alias("avg_model_confidence"),
        F.avg("image_quality_score").alias("avg_image_quality"),
        F.sum(F.col("referred").cast("int")).alias("referrals"),
        F.avg(F.col("referred").cast("double")).alias("referral_rate"),
    )


def class_mix_kpis(df):
    from pyspark.sql import functions as F

    totals = df.groupBy("_event_date", "facility_id").agg(F.count("*").alias("_total"))
    by_class = df.groupBy("_event_date", "facility_id", "predicted_class").agg(
        F.count("*").alias("class_count")
    )
    return (
        by_class.join(totals, ["_event_date", "facility_id"])
        .withColumn("class_share", F.col("class_count") / F.col("_total"))
        .drop("_total")
    )
