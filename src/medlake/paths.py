from __future__ import annotations


def table_name(catalog: str, schema: str, table: str) -> str:
    values = [catalog, schema, table]
    if any(not x or "." in x for x in values):
        raise ValueError("Catalog/schema/table names must be simple non-empty identifiers.")
    return ".".join(values)


def checkpoint_path(base: str, stream_name: str) -> str:
    return f"{base.rstrip('/')}/{stream_name}/checkpoint"
