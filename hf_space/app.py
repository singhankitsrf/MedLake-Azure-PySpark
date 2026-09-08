"""Run the shared PySpark transformations on CPU in a Docker Space."""

from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import gradio as gr
from scripts.evaluate_local import evaluate


def run_pipeline(rows):
    n = int(rows)
    if not 100 <= n <= 3000:
        raise gr.Error("Choose 100–3,000 generated events.")
    report, preview = evaluate(rows=n, seed=42)
    return report, pd.DataFrame(preview)


ROOT = Path(__file__).resolve().parents[1]
with gr.Blocks(title="MedLake | Ankit Kumar Singh") as demo:
    gr.Markdown(
        "# MedLake PySpark\n### Synthetic events → quality checks → Silver records → Gold KPIs\nBuilt by **Ankit Kumar Singh** · [GitHub source](https://github.com/singhankitsrf/MedLake-Azure-PySpark)"
    )
    gr.Markdown(
        "This application runs **actual local PySpark transformations**. It generates fictional events, injects bad records and duplicates, and verifies the resulting aggregates. Azure services are not contacted."
    )
    with gr.Tab("Run the pipeline"):
        rows = gr.Slider(100, 3000, value=1000, step=100, label="Synthetic events")
        button = gr.Button("Run and verify", variant="primary")
        results = gr.JSON(label="Reconciliation and replay checks")
        preview = gr.Dataframe(label="Gold daily facility KPIs — first 20 rows", interactive=False)
        button.click(
            run_pipeline, rows, [results, preview], api_name="evaluate", concurrency_limit=1
        )
    with gr.Tab("Saved evaluation"):
        gr.JSON(
            json.loads((ROOT / "evaluation/local_spark.json").read_text()),
            label="Measured seeded run",
        )
    with gr.Tab("Azure deployment"):
        gr.Markdown(
            "The GitHub project retains Terraform, Databricks and Event Hubs configurations. A new consumer connects the streaming Bronze table to Silver and Gold through checkpointed micro-batches.\n\nLocal checks validate shared transformations. They do not establish successful Azure deployment, cloud latency, or cloud cost.\n\n[Streaming design and operational limits](https://github.com/singhankitsrf/MedLake-Azure-PySpark/blob/main/docs/STREAMING_END_TO_END.md)"
        )


if __name__ == "__main__":
    demo.queue(max_size=8, default_concurrency_limit=1).launch(
        server_name="0.0.0.0", server_port=7860, share=False, show_error=False
    )
