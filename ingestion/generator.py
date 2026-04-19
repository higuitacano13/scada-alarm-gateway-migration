import json
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Literal

SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL", None, 1, 2, 3]
TAGS = ["PUMP_01", "VALVE_02", "TEMP_03", None]
SOURCES = ["SCADA_A", "SCADA_B", "SCADA_C"]

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%dT%H:%M:%S",
]

def random_date() -> str:
    base = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))
    fmt = random.choice(DATE_FORMATS)
    return base.strftime(fmt)


def generate_alarm_record() -> dict:
    return {
        "tag": random.choice(TAGS),
        "description": "Alarm triggered",
        "severity": random.choice(SEVERITIES),
        "event_time": random_date(),
        "cleared_time": None,
        "source": random.choice(SOURCES),
    }


def generate_alarm_dataset(
    path: Path,
    size: int = 1000,
    file_format: Literal["json", "csv"] = "json"
):
    data = [generate_alarm_record() for _ in range(size)]

    path.parent.mkdir(parents=True, exist_ok=True)

    if file_format == "json":
        _write_json(path, data)
    elif file_format == "csv":
        _write_csv(path, data)
    else:
        raise ValueError(f"Formato no soportado: {file_format}")


def _write_json(path: Path, data: List[dict]):
    with open(path.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _write_csv(path: Path, data: List[dict]):
    if not data:
        return

    with open(path.with_suffix(".csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)