import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from repositories.alarm_repository import AlarmRepository

def test_get_severity_map():
    repo = AlarmRepository()
    repo.db = MagicMock()

    repo.db.execute.return_value.all.return_value = [
        (1, 10),
        (2, 20),
    ]

    result = repo._get_severity_map()

    assert result == {
        1: 10,
        2: 20
    }

def test_get_source_system_id_exists():
    repo = AlarmRepository()
    repo.db = MagicMock()

    mock_source = MagicMock()
    mock_source.source_system_id = 5

    repo.db.execute.return_value.scalar_one_or_none.return_value = mock_source

    result = repo._get_source_system_id("SCADA_A")

    assert result == 5

def test_get_source_system_id_create():
    repo = AlarmRepository()
    repo.db = MagicMock()

    repo.db.execute.return_value.scalar_one_or_none.return_value = None

    mock_source = MagicMock()
    mock_source.source_system_id = 10

    repo.db.add = MagicMock()
    repo.db.commit = MagicMock()
    repo.db.refresh = lambda x: setattr(x, "source_system_id", 10)

    result = repo._get_source_system_id("NEW_SYSTEM")

    assert result == 10

@patch("repositories.alarm_repository.AlarmEvent")
def test_bulk_insert_success(mock_alarm_event):
    repo = AlarmRepository()
    repo.db = MagicMock()

    repo._get_severity_map = MagicMock(return_value={1: 100})
    repo._get_source_system_id = MagicMock(return_value=200)

    alarms = [
        {
            "tag": "PUMP_01",
            "severity_level": 1,
            "event_time": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "source_system": "SCADA_A"
        }
    ]

    inserted, failed = repo.bulk_insert(alarms, "path.json")

    assert inserted == 1
    assert failed == 0
    repo.db.bulk_save_objects.assert_called_once()

def test_bulk_insert_with_invalid_severity():
    repo = AlarmRepository()
    repo.db = MagicMock()

    repo._get_severity_map = MagicMock(return_value={})

    alarms = [
        {
            "tag": "PUMP_01",
            "severity_level": 99,
            "event_time": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "source_system": "SCADA_A"
        }
    ]

    inserted, failed = repo.bulk_insert(alarms, "path.json")

    assert inserted == 0
    assert failed == 1

def test_get_alarms_basic():
    repo = AlarmRepository()
    repo.db = MagicMock()

    mock_query = MagicMock()
    repo.db.query.return_value = mock_query

    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query

    mock_query.count.return_value = 1

    mock_alarm = MagicMock()
    mock_alarm.alarm_event_id = 1
    mock_alarm.tag = "PUMP_01"
    mock_alarm.description = "desc"
    mock_alarm.status = "ACTIVE"
    mock_alarm.event_time = datetime.now()
    mock_alarm.created_at = datetime.now()

    mock_query.all.return_value = [
        (mock_alarm, 3, "SCADA_A")
    ]

    data, total = repo.get_alarms()

    assert total == 1
    assert len(data) == 1
    assert data[0]["tag"] == "PUMP_01"

def test_get_top_tags():
    repo = AlarmRepository()
    repo.db = MagicMock()

    mock_query = MagicMock()
    repo.db.query.return_value = mock_query

    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query

    mock_query.all.return_value = [
        ("PUMP_01", 10),
        ("VALVE_02", 5),
    ]

    result = repo.get_top_tags()

    assert len(result) == 2
    assert result[0]["tag"] == "PUMP_01"