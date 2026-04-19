import json
import csv
from pathlib import Path

from ingestion.generator import (
    random_date,
    generate_alarm_record,
    generate_alarm_dataset,
    TAGS,
    SEVERITIES,
    SOURCES,
)


def test_random_date_returns_string():
    result = random_date()
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_alarm_record_structure():
    record = generate_alarm_record()

    assert "tag" in record
    assert "description" in record
    assert "severity" in record
    assert "event_time" in record
    assert "cleared_time" in record
    assert "source" in record


def test_generate_alarm_record_values():
    record = generate_alarm_record()

    assert record["tag"] in TAGS
    assert record["severity"] in SEVERITIES
    assert record["source"] in SOURCES


def test_generate_dataset_json(tmp_path: Path):
    file_path = tmp_path / "test.json"

    generate_alarm_dataset(file_path, size=10, file_format="json")

    assert file_path.with_suffix(".json").exists()

    with open(file_path.with_suffix(".json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 10


def test_generate_dataset_csv(tmp_path: Path):
    file_path = tmp_path / "test.csv"

    generate_alarm_dataset(file_path, size=5, file_format="csv")

    assert file_path.with_suffix(".csv").exists()

    with open(file_path.with_suffix(".csv"), "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 5


def test_generate_dataset_invalid_format(tmp_path: Path):
    file_path = tmp_path / "test.xyz"

    try:
        generate_alarm_dataset(file_path, file_format="xml")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True