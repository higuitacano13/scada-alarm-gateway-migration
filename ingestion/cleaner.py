from datetime import datetime, timezone
from typing import Optional

SEVERITY_MAP = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
    1: 1,
    2: 2,
    3: 3,
}

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%dT%H:%M:%S",
]

def parse_date(value: str) -> Optional[datetime]:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def normalize_alarm(raw: dict) -> Optional[dict]:
    event_time = parse_date(raw.get("event_time", ""))
    cleared_time = parse_date(raw.get("cleared_time")) if raw.get("cleared_time") else None
    raw_severity = SEVERITY_MAP.get(raw.get("severity"))
    tag = raw.get("tag")

    if isinstance(raw_severity, str) and raw_severity.isdigit():
        raw_severity = int(raw_severity)

    severity = SEVERITY_MAP.get(raw_severity)

    if event_time is None or severity is None or not tag:
        return None

    return {
        "tag": tag,
        "description": raw.get("description"),
        "severity_level": severity,
        "event_time": event_time,
        "cleared_time": cleared_time,
        "status": "ACTIVE",
        "source_system": raw.get("source")
    }