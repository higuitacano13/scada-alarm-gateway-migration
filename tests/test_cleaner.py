from ingestion.cleaner import parse_date, normalize_alarm
from datetime import timezone

def test_parse_date_valid():
    date = parse_date("2024-01-01 12:00:00")
    assert date is not None
    assert date.tzinfo == timezone.utc

def test_parse_date_invalid():
    assert parse_date("fecha_mala") is None

def test_normalize_alarm_valid():
    raw = {
        "tag": "PUMP_01",
        "severity": "HIGH",
        "event_time": "2024-01-01 12:00:00",
        "source": "SCADA_A"
    }

    alarm = normalize_alarm(raw)
    assert alarm is not None
    assert alarm["severity_level"] == 3
    assert alarm["tag"] == "PUMP_01"

def test_normalize_alarm_invalid_severity():
    raw = {
        "tag": "PUMP_01",
        "severity": "UNKNOWN",
        "event_time": "2024-01-01 12:00:00"
    }

    assert normalize_alarm(raw) is None
