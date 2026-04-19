import pytest
from datetime import datetime
from unittest.mock import MagicMock
from services.alarm_service import AlarmService

def test_service_get_alarms():
    mock_repo = MagicMock()

    mock_repo.get_alarms.return_value = ([{"tag": "PUMP_01"}], 1)

    service = AlarmService(mock_repo)

    data, total = service.get_alarms(
        from_date=None,
        to_date=None,
        severity=None,
        tag=None,
        limit=50,
        offset=0
    )

    assert total == 1
    assert data[0]["tag"] == "PUMP_01"
    
def test_service_invalid_dates():
    mock_repo = MagicMock()
    service = AlarmService(mock_repo)

    with pytest.raises(ValueError):
        service.get_alarms(
            from_date=datetime(2025,1,2),
            to_date=datetime(2025,1,1),
            severity=None,
            tag=None,
            limit=50,
            offset=0
        )

def test_top_tags_success():
    mock_repo = MagicMock()

    mock_repo.get_top_tags.return_value = [
        {"tag": "PUMP_01", "total_events": 10},
        {"tag": "VALVE_02", "total_events": 5},
    ]

    service = AlarmService(mock_repo)

    result = service.top_tags(
        from_date=None,
        to_date=None,
        limit=10
    )

    assert "data" in result
    assert len(result["data"]) == 2
    assert result["data"][0]["tag"] == "PUMP_01"

def test_top_tags_success():
    mock_repo = MagicMock()

    mock_repo.get_top_tags.return_value = [
        {"tag": "PUMP_01", "total_events": 10},
        {"tag": "VALVE_02", "total_events": 5},
    ]

    service = AlarmService(mock_repo)

    result = service.top_tags(
        from_date=None,
        to_date=None,
        limit=10
    )

    assert "data" in result
    assert len(result["data"]) == 2
    assert result["data"][0]["tag"] == "PUMP_01"

def test_top_tags_empty_result():
    mock_repo = MagicMock()
    mock_repo.get_top_tags.return_value = []

    service = AlarmService(mock_repo)

    result = service.top_tags(None, None, 10)

    assert result == {"data": []}