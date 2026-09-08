import pytest
from medlake.paths import checkpoint_path, table_name


def test_table_name():
    assert table_name("medlake", "silver", "events") == "medlake.silver.events"


def test_table_name_rejects_dot():
    with pytest.raises(ValueError):
        table_name("med.lake", "silver", "events")


def test_checkpoint_path():
    assert (
        checkpoint_path("abfss://x/checkpoints/", "events")
        == "abfss://x/checkpoints/events/checkpoint"
    )
