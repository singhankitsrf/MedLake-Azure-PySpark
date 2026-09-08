from __future__ import annotations


def build_scd2_changes(source_df, target_df, key: str, tracked_columns: list[str]):
    from pyspark.sql import functions as F

    src = source_df.alias("s")
    tgt = target_df.filter(F.col("is_current") == True).alias("t")
    joined = src.join(tgt, F.col(f"s.{key}") == F.col(f"t.{key}"), "left")
    changed_expr = F.lit(False)
    for col_name in tracked_columns:
        expr = ~F.col(f"s.{col_name}").eqNullSafe(F.col(f"t.{col_name}"))
        changed_expr = changed_expr | expr
    return (
        joined.withColumn(
            "_scd_action",
            F.when(F.col(f"t.{key}").isNull(), F.lit("insert"))
            .when(changed_expr, F.lit("change"))
            .otherwise(F.lit("no_change")),
        )
        .filter(F.col("_scd_action") != "no_change")
        .select("s.*", "_scd_action")
    )
