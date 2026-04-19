import json
import csv
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ingestion.loader import (
    read_dataset,
    load_alarm_dataset,
)

def test_read_json(tmp_path: Path):
    file_path = tmp_path / "data.json"

    sample = [{"a": 1}, {"a": 2}]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sample, f)

    result = read_dataset(file_path)

    assert result == sample


def test_read_csv(tmp_path: Path):
    file_path = tmp_path / "data.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["a"])
        writer.writeheader()
        writer.writerow({"a": "1"})
        writer.writerow({"a": "2"})

    result = read_dataset(file_path)

    assert len(result) == 2
    assert result[0]["a"] == "1"


def test_read_dataset_invalid_format(tmp_path: Path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("invalid")

    with pytest.raises(ValueError):
        read_dataset(file_path)


@patch("ingestion.loader.AlarmRepository")
@patch("ingestion.loader.normalize_alarm")
def test_load_alarm_dataset_success(mock_normalize, mock_repo_class, tmp_path):
    file_path = tmp_path / "data.json"

    raw_data = [{"a": 1}, {"a": 2}, {"a": 3}]
    file_path.write_text(json.dumps(raw_data))

    # mock normalize → todos válidos
    mock_normalize.side_effect = lambda x: {"normalized": True}

    # mock repo
    mock_repo = MagicMock()
    mock_repo.bulk_insert.return_value = (3, 0)
    mock_repo_class.return_value = mock_repo

    result = load_alarm_dataset(file_path)

    assert result["inserted"] == 3
    assert result["invalid"] == 0
    assert result["total"] == 3


@patch("ingestion.loader.AlarmRepository")
@patch("ingestion.loader.normalize_alarm")
def test_load_alarm_dataset_with_invalid_records(mock_normalize, mock_repo_class, tmp_path):
    file_path = tmp_path / "data.json"

    raw_data = [{"a": 1}, {"a": 2}, {"a": 3}]
    file_path.write_text(json.dumps(raw_data))

    # 1 inválido
    mock_normalize.side_effect = [
        {"ok": True},
        None,
        {"ok": True}
    ]

    mock_repo = MagicMock()
    mock_repo.bulk_insert.return_value = (2, 0)
    mock_repo_class.return_value = mock_repo

    result = load_alarm_dataset(file_path)

    assert result["inserted"] == 2
    assert result["invalid"] == 1
    assert result["total"] == 3


@patch("ingestion.loader.AlarmRepository")
@patch("ingestion.loader.normalize_alarm")
def test_load_alarm_dataset_repo_failure(mock_normalize, mock_repo_class, tmp_path):
    file_path = tmp_path / "data.json"

    raw_data = [{"a": 1}]
    file_path.write_text(json.dumps(raw_data))

    mock_normalize.return_value = {"ok": True}

    mock_repo = MagicMock()
    mock_repo.bulk_insert.return_value = (0, 1)
    mock_repo_class.return_value = mock_repo

    result = load_alarm_dataset(file_path)

    assert result["failed_db"] == 1