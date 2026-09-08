"""Run the actual PySpark transformations on seeded synthetic fixtures."""

from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
from scripts.generate_synthetic_data import generate
from medlake.spark_transforms import (
    normalize_events,
    add_quality_flags,
    deduplicate_batch,
    daily_facility_kpis,
)
from medlake.streaming import parse_bronze


def evaluate(rows=1000, seed=42):
    from pyspark.sql import SparkSession

    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    spark = (
        SparkSession.builder.master("local[2]")
        .appName("MedLake reproducibility")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.ansi.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    events = generate(rows, seed)
    for i, field, value in [
        (0, "model_confidence", None),
        (1, "image_quality_score", 1.2),
        (2, "patient_id", ""),
        (3, "event_ts", "invalid"),
    ]:
        events[i][field] = value
    events += [events[-1].copy(), events[-2].copy()]
    raw = [json.dumps(x, sort_keys=True) for x in events]
    raw.append("{broken json")
    try:
        bronze = spark.createDataFrame([(x,) for x in raw], "json_payload string")
        checked = add_quality_flags(normalize_events(parse_bronze(bronze))).cache()
        invalid = checked.filter("NOT _is_valid")
        valid = deduplicate_batch(checked.filter("_is_valid")).cache()
        gold = daily_facility_kpis(valid)
        valid_count, invalid_count = valid.count(), invalid.count()
        gold_total = sum(x.screenings for x in gold.collect())
        repeated = deduplicate_batch(valid.unionByName(valid)).count()
        checks = {
            "invalid_rows_quarantined": invalid_count == 5,
            "expected_unique_valid_rows": valid_count == rows - 4,
            "gold_reconciles_to_silver": gold_total == valid_count,
            "replay_deduplication_idempotent": repeated == valid_count,
        }
        result = {
            "scope": "local PySpark on synthetic events; not Azure deployment",
            "seed": seed,
            "generated_rows": rows,
            "input_rows_with_faults_and_duplicates": len(raw),
            "unique_valid_rows": valid_count,
            "quarantined_rows": invalid_count,
            "duplicate_valid_rows_removed": len(raw) - invalid_count - valid_count,
            "gold_screenings": gold_total,
            "checks": checks,
            "fixture_sha256": hashlib.sha256("\n".join(raw).encode()).hexdigest(),
            "spark_version": spark.version,
        }
        if not all(checks.values()):
            raise AssertionError(result)
        preview = [
            x.asDict() for x in gold.orderBy("facility_id", "_event_date").limit(20).collect()
        ]
        return result, preview
    finally:
        spark.stop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--output", default="evaluation/local_spark.json")
    a = ap.parse_args()
    report, _ = evaluate(a.rows)
    p = Path(a.output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
