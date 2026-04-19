
import csv
from pathlib import Path
import json
from typing import Dict, List
from ingestion.cleaner import normalize_alarm
from repositories.alarm_repository import AlarmRepository

def load_alarm_dataset(path: Path) -> dict:
    raw_data = read_dataset(path)

    clean_alarms = []
    invalid_count = 0

    for record in raw_data:
        normalized = normalize_alarm(record)
        if normalized:
            clean_alarms.append(normalized)
        else:
            invalid_count += 1

    repo = AlarmRepository()
    inserted, failed = repo.bulk_insert(
        clean_alarms,
        raw_payload_path=str(path)
    )
    repo.close()

    return {
        "inserted": inserted,
        "failed_db": failed,
        "invalid": invalid_count,
        "total": len(raw_data)
    }

def read_dataset(path: Path) -> List[Dict]:
    suffix = path.suffix.lower()

    if suffix == ".json":
        return _read_json(path)
    elif suffix == ".csv":
        return _read_csv(path)
    else:
        raise ValueError(f"Formato no soportado: {suffix}")

def _read_json(path: Path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _read_csv(path: Path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)